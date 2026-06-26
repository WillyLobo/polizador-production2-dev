from django.db import migrations
from django.utils import timezone

LEGADO_DESCRIPCION = "Migración: reconciliación de montos históricos"


def _contratos_reales(contrato_qs):
    return contrato_qs.exclude(contrato_autocarga=True).exclude(contrato_descripcion=LEGADO_DESCRIPCION)


def _elegir_contrato(obra, contratos_reales, tipo_nombre):
    """
    Devuelve (contrato, ambiguo) para una Obra dada, intentando matchear el
    nombre del tipo de documento contra la descripción de sus Contratos reales
    cuando hay más de uno. `ambiguo=True` si se usó el fallback (más antiguo)
    sin un match único, para poder avisar y revisar a mano.
    """
    contratos = list(contratos_reales.order_by("contrato_fecha", "pk"))
    if len(contratos) == 1:
        return contratos[0], False
    if len(contratos) > 1 and tipo_nombre:
        coincidencias = [c for c in contratos if c.contrato_descripcion.strip().lower() == tipo_nombre.strip().lower()]
        if len(coincidencias) == 1:
            return coincidencias[0], False
    return (contratos[0] if contratos else None), True


def vincular_documentos(apps, schema_editor):
    Obra = apps.get_model("carga", "Obra")
    Contrato = apps.get_model("carga", "Contrato")
    ContratosDigitales = apps.get_model("carga", "ContratosDigitales")
    ResolucionesDigitales = apps.get_model("carga", "ResolucionesDigitales")

    a_revisar = []

    for documento, campo_obra, campo_contrato, campo_tipo in (
        (ContratosDigitales, "contratodigital_obra", "contratodigital_contrato", "contratodigital_tipo"),
        (ResolucionesDigitales, "resoluciondigital_obra", "resoluciondigital_contrato", None),
    ):
        for doc in documento.objects.all().iterator():
            obras = list(getattr(doc, campo_obra).all())
            obra = obras[0] if obras else None
            if obra is None:
                continue

            tipo_nombre = None
            if campo_tipo:
                tipo = getattr(doc, campo_tipo, None)
                tipo_nombre = getattr(tipo, "contratorubro_tipo", None) if tipo else None

            contratos_reales = _contratos_reales(Contrato.objects.filter(contrato_obra=obra))
            contrato, ambiguo = _elegir_contrato(obra, contratos_reales, tipo_nombre)

            if contrato is None:
                contrato = Contrato.objects.create(
                    contrato_obra=obra,
                    contrato_fecha=obra.obra_fecha_contrato or timezone.now().date(),
                    contrato_descripcion=tipo_nombre or "Contrato Base",
                    contrato_autocarga=False,
                )

            setattr(doc, campo_contrato, contrato)
            doc.save()

            if ambiguo:
                a_revisar.append((documento.__name__, doc.pk, obra.pk))

    if a_revisar:
        print(
            f"\n[0023_vincular_documentos_digitales_a_contrato] ATENCIÓN: {len(a_revisar)} "
            f"documento(s) vinculados por fallback (Obra con varios Contratos reales, sin match "
            f"único), revisar manualmente: {a_revisar}"
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("carga", "0022_agregar_contrato_fk_documentos_digitales"),
    ]

    operations = [
        migrations.RunPython(vincular_documentos, noop),
    ]
