from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from secretariador.management.commands.empaquetar_resoluciones_mensual import DESTINO_PREFIJO

MESES = (
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)


def _listar_meses(bucket):
    """Lee los subdirectorios `{ano}-{mes}/` bajo DESTINO_PREFIJO y arma, para
    cada uno, la lista de paquete-NN.zip que contiene (ignorando el prefijo
    _scratch/ de blobs temporales que puede haber quedado de una corrida
    interrumpida)."""
    blobs = bucket.list_blobs(prefix=f"{DESTINO_PREFIJO}/", delimiter="/")
    list(blobs)  # hay que consumir el iterador para que se completen .prefixes

    meses = []
    for prefijo in sorted(blobs.prefixes, reverse=True):
        ano_mes = prefijo.rstrip("/").rsplit("/", 1)[-1]
        try:
            ano, mes = (int(parte) for parte in ano_mes.split("-"))
        except ValueError:
            continue

        paquetes = sorted(
            (blob for blob in bucket.list_blobs(prefix=prefijo) if blob.name.endswith(".zip")),
            key=lambda blob: blob.name,
        )
        if not paquetes:
            continue

        meses.append({
            "ano": ano,
            "mes": mes,
            "nombre_mes": MESES[mes] if 1 <= mes <= 12 else mes,
            "paquetes": [
                {"indice": indice, "tamano": blob.size}
                for indice, blob in enumerate(paquetes, start=1)
            ],
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
def descargar_paquete_resoluciones(request, ano, mes, indice):
    nombre = f"{DESTINO_PREFIJO}/{ano}-{mes:02d}/paquete-{indice:02d}.zip"
    bucket = default_storage.client.bucket(default_storage.bucket_name)
    blob = bucket.blob(nombre)
    if not blob.exists():
        raise Http404("El paquete solicitado no existe.")

    return HttpResponseRedirect(default_storage.url(nombre))
