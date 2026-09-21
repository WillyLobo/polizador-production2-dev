"""
Borra los grupos "*_invitados", que no tienen ningun usuario desde hace tiempo.

Parte de la migracion de gates por nombre de grupo a gates por permiso (ver
core/management/commands/verificar_permisos_ui.py): mientras los gates se
escribian como '"x" in groups', un grupo vacio era inofensivo; ahora que la UI
pregunta por permisos, un grupo vacio con 11/25 permisos asignados es solo una
fuente de confusion al revisar quien puede que cosa.

Defensiva a proposito: si al aplicarse el grupo TIENE usuarios (alguien lo
empezo a usar despues de que se escribio esta migracion), no lo toca. Revertir
recrea los grupos con exactamente los permisos que tenian, por eso la lista
esta escrita aca y no se deriva de la base.
"""
from django.conf import settings
from django.db import migrations

PERMISOS_POR_GRUPO = {
    "dirgral_invitados": [
        "secretariador.view_comisionado",
        "secretariador.view_comisionadosolicitud",
        "secretariador.view_incorporacion",
        "secretariador.view_instrumentoslegalesdecretos",
        "secretariador.view_instrumentoslegalesmemorandum",
        "secretariador.view_instrumentoslegalesresoluciones",
        "secretariador.view_instrumentoslegalesresolucionesdirectorio",
        "secretariador.view_montoviaticodiario",
        "secretariador.view_organigrama",
        "secretariador.view_solicitud",
        "secretariador.view_vehiculo",
    ],
    "gciaoperativa_invitados": [
        "carga.view_agente",
        "carga.view_area",
        "carga.view_aseguradora",
        "carga.view_certificado",
        "carga.view_certificadofinanciamiento",
        "carga.view_certificadorubro",
        "carga.view_conjuntolicitado",
        "carga.view_contrato",
        "carga.view_contratomonto",
        "carga.view_contratorubro",
        "carga.view_contratosdigitales",
        "carga.view_departamento",
        "carga.view_empresa",
        "carga.view_indec",
        "carga.view_localidad",
        "carga.view_municipio",
        "carga.view_obra",
        "carga.view_plandetrabajos",
        "carga.view_poliza",
        "carga.view_poliza_movimiento",
        "carga.view_programa",
        "carga.view_prototipo",
        "carga.view_receptor",
        "carga.view_resolucionesdigitales",
        "carga.view_uvi",
    ],
}


def borrar_grupos_vacios(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    for nombre in PERMISOS_POR_GRUPO:
        grupo = Group.objects.filter(name=nombre).first()
        if grupo is None:
            continue
        if User.objects.filter(groups=grupo).exists():
            # Alguien lo empezo a usar: no es el grupo muerto que se quiso borrar.
            continue
        grupo.delete()


def recrear_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    for nombre, permisos in PERMISOS_POR_GRUPO.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        objs = []
        for p in permisos:
            app_label, codename = p.split(".")
            perm = Permission.objects.filter(
                content_type__app_label=app_label, codename=codename
            ).first()
            if perm is not None:
                objs.append(perm)
        grupo.permissions.set(objs)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_formvalidationerror"),
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(borrar_grupos_vacios, recrear_grupos),
    ]
