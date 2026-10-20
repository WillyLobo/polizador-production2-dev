"""Pasa los instrumentos de aportes que no son del IPDUV a InstrumentoAgente.

- aportes_ley_resolucion con tipo DIS (Disposicion): InstrumentoAgente tipo DIS.
- aportes_ley_resolucion sin tipo: si matchea una Resolucion/Decreto se vincula a ella; si
  no, InstrumentoAgente tipo OTR.
- aportes_anses: InstrumentoAgente tipo OTR, organismo ANSES.

La numeracion se guarda tal cual. Los aportes con tipo RES/DEC los vincula el comando
vincular_instrumentos_agente (igual que el resto de los conceptos).
"""
from django.db import migrations

from personalizador.instrumentos import buscar, RES


def _instrumento(InstrumentoAgente, tipo, organismo, numero):
    instrumento, _ = InstrumentoAgente.objects.get_or_create(
        instrumentoagente_tipo=tipo,
        instrumentoagente_organismo=organismo,
        instrumentoagente_numero=numero.strip(),
    )
    return instrumento


def migrar_aportes(apps, schema_editor):
    Agente = apps.get_model("personalizador", "Agente")
    InstrumentoAgente = apps.get_model("personalizador", "InstrumentoAgente")
    Resolucion = apps.get_model("secretariador", "InstrumentosLegalesResoluciones")
    Decreto = apps.get_model("secretariador", "InstrumentosLegalesDecretos")

    for agente in Agente.objects.exclude(aportes_ley_resolucion__isnull=True).exclude(aportes_ley_resolucion=""):
        tipo = agente.aportes_ley_resolucion_tipo
        if tipo == "DIS":
            cambios = {"instrumento_aportes_ley_externo": _instrumento(InstrumentoAgente, "DIS", "", agente.aportes_ley_resolucion)}
        elif not tipo:
            resultado = buscar(None, agente.aportes_ley_resolucion, Resolucion, Decreto)
            if resultado.instrumento is not None:
                campo = "instrumento_aportes_ley_resolucion" if resultado.tipo == RES else "instrumento_aportes_ley_decreto"
                cambios = {campo: resultado.instrumento}
            else:
                cambios = {"instrumento_aportes_ley_externo": _instrumento(InstrumentoAgente, "OTR", "", agente.aportes_ley_resolucion)}
        else:
            continue
        Agente.objects.filter(pk=agente.pk).update(aportes_ley_resolucion=None, aportes_ley_resolucion_tipo=None, **cambios)

    for agente in Agente.objects.exclude(aportes_anses__isnull=True).exclude(aportes_anses=""):
        Agente.objects.filter(pk=agente.pk).update(
            aportes_anses=None,
            instrumento_aportes_anses_externo=_instrumento(InstrumentoAgente, "OTR", "ANSES", agente.aportes_anses),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("personalizador", "0030_agente_instrumentos_fk"),
    ]

    operations = [
        migrations.RunPython(migrar_aportes, migrations.RunPython.noop),
    ]
