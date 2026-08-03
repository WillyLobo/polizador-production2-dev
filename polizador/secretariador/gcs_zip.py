"""
Arma un ZIP válido directamente en Google Cloud Storage usando la operación
compose() del bucket, sin descargar el contenido de los PDF originales al
proceso de Django.

Por qué funciona: un archivo ZIP es, a nivel de bytes, la concatenación
secuencial de [encabezado local + datos] por cada entrada, seguida del
directorio central y el registro de fin de archivo (EOCD). compose() concatena
objetos de GCS en el orden dado; si subimos un blob chiquito por cada
encabezado local (los únicos bytes que hace falta generar) y usamos el PDF ya
existente como los "datos" de esa entrada, componer todo en el orden correcto
da un ZIP idéntico al que se obtendría bajando y re-subiendo los archivos,
pero sin mover el contenido pesado por el servidor de Django.

La única pieza que GCS no guarda y que el encabezado ZIP necesita es el CRC-32
(GCS calcula CRC32C, un polinomio distinto); por eso se cachea en
InstrumentosLegalesResoluciones.instrumentolegalresoluciones_crc32 al subir
cada archivo (ver signals.py) — este módulo asume que ya viene calculado.

compose() acepta como máximo MAX_FUENTES_POR_COMPOSE objetos fuente por
llamada, así que combinar más piezas requiere un árbol de composes
intermedios (_reducir_en_arbol), todos bajo un prefijo "scratch" que se borra
al terminar salvo por el blob final.
"""
import struct
import zipfile
from dataclasses import dataclass, field
from datetime import datetime

MAX_FUENTES_POR_COMPOSE = 32


@dataclass
class EntradaZip:
    """Una resolución a incluir en el ZIP compuesto."""

    nombre_archivo: str        # nombre dentro del zip, p.ej. "1234-2026-P.pdf"
    tamano: int                # bytes, igual a blob_origen.size
    crc32: int                 # CRC-32 estándar (IEEE) del contenido del PDF
    blob_origen: object        # google.cloud.storage.Blob del PDF; se usa tal cual como "datos"
    date_time: tuple = field(default_factory=lambda: datetime.now().timetuple()[:6])


def _zipinfo(entrada, header_offset):
    if not entrada.nombre_archivo.isascii():
        raise ValueError(
            f"Nombre de archivo no ascii ({entrada.nombre_archivo!r}): "
            "el armado vía compose no soporta el flag UTF-8 de nombre de archivo."
        )
    zinfo = zipfile.ZipInfo(filename=entrada.nombre_archivo, date_time=entrada.date_time)
    zinfo.compress_type = zipfile.ZIP_STORED
    zinfo.file_size = entrada.tamano
    zinfo.compress_size = entrada.tamano
    zinfo.CRC = entrada.crc32
    zinfo.header_offset = header_offset
    zinfo.external_attr = 0o600 << 16
    return zinfo


def _central_directory_record(zinfo):
    """Registro de directorio central para zinfo, con el mismo layout de bytes
    que arma zipfile.ZipFile._write_end_record en la stdlib."""
    dt = zinfo.date_time
    dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
    dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
    filename = zinfo.filename.encode("ascii")

    centdir = struct.pack(
        zipfile.structCentralDir,
        zipfile.stringCentralDir,
        20, 0, 20, 0,               # create_version, create_system, extract_version, reserved
        0,                          # flag_bits: sin data descriptor, sin flag de nombre UTF-8
        zipfile.ZIP_STORED,
        dostime, dosdate,
        zinfo.CRC, zinfo.compress_size, zinfo.file_size,
        len(filename), 0, 0,        # filename_len, extra_len, comment_len
        0, 0, zinfo.external_attr,  # disk_num_start, internal_attr, external_attr
        zinfo.header_offset,
    )
    return centdir + filename


def _end_of_central_directory(cantidad_entradas, tamano_directorio_central, offset_directorio_central):
    return struct.pack(
        zipfile.structEndArchive,
        zipfile.stringEndArchive,
        0, 0,                                   # disco actual, disco del directorio central
        cantidad_entradas, cantidad_entradas,   # entradas en este disco, entradas totales
        tamano_directorio_central,
        offset_directorio_central,
        0,                                       # largo del comentario
    )


def _reducir_en_arbol(bucket, blobs, prefijo_scratch, etiqueta):
    """Combina una lista ORDENADA de blobs en uno solo vía compose(), respetando
    el límite de MAX_FUENTES_POR_COMPOSE fuentes por llamada (árbol de
    composes intermedios). Devuelve (blob_final, [blobs_intermedios_creados])."""
    intermedios = []
    nivel = list(blobs)
    ronda = 0
    while len(nivel) > 1:
        siguiente_nivel = []
        for indice, inicio in enumerate(range(0, len(nivel), MAX_FUENTES_POR_COMPOSE)):
            grupo = nivel[inicio:inicio + MAX_FUENTES_POR_COMPOSE]
            if len(grupo) == 1:
                siguiente_nivel.append(grupo[0])
                continue
            destino = bucket.blob(f"{prefijo_scratch}/{etiqueta}-r{ronda}-{indice}")
            destino.content_type = "application/octet-stream"
            destino.compose(grupo)
            intermedios.append(destino)
            siguiente_nivel.append(destino)
        nivel = siguiente_nivel
        ronda += 1
    return nivel[0], intermedios


def componer_zip(bucket, entradas, destino_nombre, prefijo_scratch):
    """
    Arma un ZIP en `destino_nombre` (dentro de `bucket`) a partir de `entradas`
    (lista ORDENADA de EntradaZip), usando compose() en vez de descargar y
    re-subir el contenido de cada PDF.

    Sube blobs chiquitos (encabezados + directorio central) y objetos
    intermedios de compose bajo `prefijo_scratch`; devuelve
    (blob_final, blobs_temporales) — quien llama es responsable de borrar
    blobs_temporales una vez que ya no los necesita (ver limpiar_temporales).
    Los blobs originales de las resoluciones (entrada.blob_origen) nunca se
    tocan ni se borran.
    """
    blobs_temporales = []
    piezas = []
    zinfos = []
    offset = 0

    for indice, entrada in enumerate(entradas):
        zinfo = _zipinfo(entrada, header_offset=offset)
        zinfos.append(zinfo)

        header_bytes = zinfo.FileHeader()
        header_blob = bucket.blob(f"{prefijo_scratch}/header-{indice}")
        header_blob.upload_from_string(header_bytes, content_type="application/octet-stream")
        blobs_temporales.append(header_blob)

        piezas.append(header_blob)
        piezas.append(entrada.blob_origen)

        offset += len(header_bytes) + entrada.tamano

    offset_directorio_central = offset
    directorio_central = b"".join(_central_directory_record(z) for z in zinfos)
    eocd = _end_of_central_directory(len(entradas), len(directorio_central), offset_directorio_central)

    cola_blob = bucket.blob(f"{prefijo_scratch}/central-directory")
    cola_blob.upload_from_string(directorio_central + eocd, content_type="application/octet-stream")
    blobs_temporales.append(cola_blob)
    piezas.append(cola_blob)

    resultado, intermedios = _reducir_en_arbol(bucket, piezas, prefijo_scratch, "armado")
    blobs_temporales.extend(intermedios)

    destino = bucket.blob(destino_nombre)
    destino.content_type = "application/zip"
    destino.compose([resultado])

    return destino, blobs_temporales


def limpiar_temporales(blobs_temporales):
    """Borra los blobs de scratch (encabezados, directorio central,
    intermedios de compose). Sigue borrando el resto aunque alguno falle."""
    for blob in blobs_temporales:
        try:
            blob.delete()
        except Exception:
            pass
