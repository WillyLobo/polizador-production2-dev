"""Pasa los instrumentos legales del Agente (una FK por concepto y tipo) a filas de
AgenteInstrumento, para poder cargar varios por concepto.

Los años/meses/dias de aportes (Ley/Resolucion y ANSES) pasan a la fila del instrumento de
aportes; si el agente tenia tiempo reconocido sin instrumento vinculado, queda una fila sin
instrumento con ese tiempo.

Las columnas viejas se borran en 0036 (separado: en Postgres no se puede alterar la tabla
de agentes en la misma transaccion en que se insertan filas que la referencian).
"""
from django.db import migrations

# concepto: {campo de AgenteInstrumento: FK vieja del Agente}, prefijo de los campos de tiempo
CONCEPTOS = {
    "pase_planta": ({"decreto": "instrumento_pase_planta_decreto"}, None),
    "bonificacion": ({"resolucion": "instrumento_bonificacion_resolucion", "decreto": "instrumento_bonificacion_decreto"}, None),
    "contrato_servicio": ({"resolucion": "instrumento_contrato_servicio_resolucion", "decreto": "instrumento_contrato_servicio_decreto"}, None),
    "cargo_interno": ({"resolucion": "instrumento_cargo_interno_resolucion", "decreto": "instrumento_cargo_interno_decreto"}, None),
    "transferencia_definitiva": ({"decreto": "instrumento_transferencia_definitiva_decreto", "externo": "instrumento_transferencia_definitiva_externo"}, None),
    "aportes_ley": ({"resolucion": "instrumento_aportes_ley_resolucion", "decreto": "instrumento_aportes_ley_decreto", "externo": "instrumento_aportes_ley_externo"}, "aportes_ley_resolucion"),
    "aportes_anses": ({"externo": "instrumento_aportes_anses_externo"}, "aportes_anses"),
}

TIEMPO = ("anios", "meses", "dias")


def a_filas(apps, schema_editor):
    Agente = apps.get_model("personalizador", "Agente")
    AgenteInstrumento = apps.get_model("personalizador", "AgenteInstrumento")
    filas = []
    for agente in Agente.objects.all().iterator():
        for clave, (fks, prefijo_tiempo) in CONCEPTOS.items():
            tiempo = {campo: getattr(agente, f"{prefijo_tiempo}_{campo}") or 0 for campo in TIEMPO} if prefijo_tiempo else {}
            instrumentos = {campo: getattr(agente, f"{fk}_id") for campo, fk in fks.items() if getattr(agente, f"{fk}_id")}
            if not instrumentos and not any(tiempo.values()):
                continue
            # Agente.clean impedia mas de una FK por concepto; por las dudas, una fila por FK
            # (el tiempo va con la primera).
            if not instrumentos:
                filas.append(AgenteInstrumento(agente_id=agente.pk, concepto=clave, **tiempo))
            for i, (campo, pk) in enumerate(instrumentos.items()):
                filas.append(AgenteInstrumento(agente_id=agente.pk, concepto=clave, **{f"{campo}_id": pk}, **(tiempo if i == 0 else {})))
    AgenteInstrumento.objects.bulk_create(filas)


def a_columnas(apps, schema_editor):
    """Reversa: la primera fila con instrumento de cada concepto vuelve a su FK y el tiempo
    de aportes se suma. Si habia varios instrumentos por concepto, el resto se pierde."""
    Agente = apps.get_model("personalizador", "Agente")
    AgenteInstrumento = apps.get_model("personalizador", "AgenteInstrumento")
    cambios = {}
    for fila in AgenteInstrumento.objects.order_by("agente_id", "concepto", "id"):
        fks, prefijo_tiempo = CONCEPTOS[fila.concepto]
        datos = cambios.setdefault(fila.agente_id, {})
        for campo, fk in fks.items():
            pk = getattr(fila, f"{campo}_id")
            if pk and not any(datos.get(f"{otra}_id") for otra in fks.values()):
                datos[f"{fk}_id"] = pk
        if prefijo_tiempo:
            for campo in TIEMPO:
                clave = f"{prefijo_tiempo}_{campo}"
                datos[clave] = datos.get(clave, 0) + getattr(fila, campo)
    for agente_id, datos in cambios.items():
        Agente.objects.filter(pk=agente_id).update(**datos)


class Migration(migrations.Migration):

    dependencies = [
        ("personalizador", "0034_agenteinstrumento"),
    ]

    operations = [
        migrations.RunPython(a_filas, a_columnas),
    ]
