from django.db import migrations


def completar_jerarquia_oficinas(apps, schema_editor):
    """Para cada Oficina, deriva los niveles superiores (Direccion, Gerencia,
    Directorio) a partir del nivel mas especifico ya asignado (cargo_departamento,
    si no cargo_direccion, si no cargo_gerencia), usando la cadena de padres ya
    cargada en esos registros. Solo completa los campos que estan vacios: no
    pisa valores ya cargados, aunque no coincidan con la jerarquia derivada
    (ver Oficina.clean(), que sí valida esos casos de ahi en adelante)."""
    Oficina = apps.get_model("personalizador", "Oficina")

    for oficina in Oficina.objects.all():
        if oficina.cargo_departamento_id:
            departamento = oficina.cargo_departamento
            direccion = departamento.departamento_direccion
            gerencia = departamento.departamento_gerencia or (direccion.direccion_gerencia if direccion else None)
            directorio = (
                departamento.departamento_directorio
                or (gerencia.gerencia_directorio if gerencia else None)
                or (direccion.direccion_directorio if direccion else None)
            )
        elif oficina.cargo_direccion_id:
            direccion = oficina.cargo_direccion
            gerencia = direccion.direccion_gerencia
            directorio = direccion.direccion_directorio or (gerencia.gerencia_directorio if gerencia else None)
        elif oficina.cargo_gerencia_id:
            direccion = None
            gerencia = oficina.cargo_gerencia
            directorio = gerencia.gerencia_directorio
        else:
            continue

        update_fields = []
        if direccion and oficina.cargo_direccion_id is None:
            oficina.cargo_direccion = direccion
            update_fields.append("cargo_direccion")
        if gerencia and oficina.cargo_gerencia_id is None:
            oficina.cargo_gerencia = gerencia
            update_fields.append("cargo_gerencia")
        if directorio and oficina.cargo_directorio_id is None:
            oficina.cargo_directorio = directorio
            update_fields.append("cargo_directorio")

        if update_fields:
            oficina.save(update_fields=update_fields)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('personalizador', '0016_remove_historicaloficina_cargo_tipo_and_more'),
    ]

    operations = [
        migrations.RunPython(completar_jerarquia_oficinas, noop),
    ]
