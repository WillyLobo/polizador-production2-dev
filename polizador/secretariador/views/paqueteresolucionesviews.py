from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from secretariador.paquetes_resoluciones import DESTINO_PREFIJO

MESES = (
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)

EXTENSIONES_POR_FORMATO = {"zip": ".zip", "pdf": ".pdf"}


def _listar_meses(bucket):
    """Lee los subdirectorios `{ano}-{mes}/` bajo DESTINO_PREFIJO y arma, para
    cada uno, la lista de paquete-NN.zip y/o paquete-NN.pdf que contiene
    (ignorando el prefijo _scratch/ de blobs temporales que puede haber
    quedado de una corrida interrumpida). Un mes puede tener uno, otro o
    ambos formatos, según qué comando se haya corrido."""
    blobs = bucket.list_blobs(prefix=f"{DESTINO_PREFIJO}/", delimiter="/")
    list(blobs)  # hay que consumir el iterador para que se completen .prefixes

    meses = []
    for prefijo in sorted(blobs.prefixes, reverse=True):
        ano_mes = prefijo.rstrip("/").rsplit("/", 1)[-1]
        try:
            ano, mes = (int(parte) for parte in ano_mes.split("-"))
        except ValueError:
            continue

        blobs_mes = list(bucket.list_blobs(prefix=prefijo))

        formatos = {}
        for formato, extension in EXTENSIONES_POR_FORMATO.items():
            paquetes = sorted(
                (blob for blob in blobs_mes if blob.name.endswith(extension)),
                key=lambda blob: blob.name,
            )
            if paquetes:
                formatos[formato] = [
                    {"indice": indice, "tamano": blob.size}
                    for indice, blob in enumerate(paquetes, start=1)
                ]

        if not formatos:
            continue

        meses.append({
            "ano": ano,
            "mes": mes,
            "nombre_mes": MESES[mes] if 1 <= mes <= 12 else mes,
            "formatos": formatos,
            # zip y pdf se arman con el mismo agrupamiento (armar_paquetes),
            # así que comparten los mismos índices; tomamos el más largo por
            # si un mes solo tiene uno de los dos formatos generado.
            "cantidad_paquetes": max(len(paquetes) for paquetes in formatos.values()),
        })

    return meses


@login_required
@permission_required("secretariador.view_instrumentoslegalesresoluciones", raise_exception=True)
def PaginaListaPaquetesResoluciones(request):
    template_name = "instrumentoslegales/Lista-paquetes-resoluciones.html"
    bucket = default_storage.client.bucket(default_storage.bucket_name)

    return render(request, template_name, {"meses": _listar_meses(bucket)})


@login_required
@permission_required("secretariador.view_instrumentoslegalesresoluciones", raise_exception=True)
def descargar_paquete_resoluciones(request, ano, mes, formato, indice):
    extension = EXTENSIONES_POR_FORMATO.get(formato)
    if extension is None:
        raise Http404("Formato de paquete desconocido.")

    nombre = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}/paquete-{indice:02d}{extension}"
    bucket = default_storage.client.bucket(default_storage.bucket_name)
    blob = bucket.blob(nombre)
    if not blob.exists():
        raise Http404("El paquete solicitado no existe.")

    return HttpResponseRedirect(default_storage.url(nombre))
