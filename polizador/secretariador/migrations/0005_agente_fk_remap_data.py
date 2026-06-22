from django.db import migrations

# (app_label, model_name, fk_field) for every real FK that used to target
# secretariador.Comisionado and now targets personalizador.Agente.
FK_FIELDS = [
    ('secretariador', 'Vehiculo', 'vehiculo_titular_agente'),
    ('secretariador', 'Solicitud', 'solicitud_solicitante'),
    ('secretariador', 'ComisionadoSolicitud', 'comisionadosolicitud_nombre'),
    ('secretariador', 'Incorporacion', 'incorporacion_solicitante'),
]


def remap_fk_ids(apps, schema_editor):
    """
    Each row is targeted by its own unique pk, never by the FK value being
    rewritten: secretariador.Comisionado ids and personalizador.Agente ids
    overlap numerically (both start at 1), so filtering UPDATEs by the
    mutable old/new id itself lets an already-converted row get re-matched
    (and corrupted) by a later iteration that happens to target the same
    number.
    """
    Comisionado = apps.get_model('secretariador', 'Comisionado')
    Agente = apps.get_model('personalizador', 'Agente')

    agente_id_by_dni = dict(Agente.objects.values_list('dni', 'id'))
    comisionado_dni_by_id = dict(Comisionado.objects.values_list('id', 'comisionado_dni'))

    for app_label, model_name, fk_field in FK_FIELDS:
        Model = apps.get_model(app_label, model_name)
        fk_column = f'{fk_field}_id'
        for row in Model.objects.exclude(**{fk_column: None}).only('id', fk_column):
            old_id = getattr(row, fk_column)
            dni = comisionado_dni_by_id.get(old_id)
            new_id = agente_id_by_dni.get(dni) if dni is not None else None
            if new_id is None:
                raise RuntimeError(
                    f"{app_label}.{model_name}.{fk_field}: no personalizador.Agente "
                    f"found for old Comisionado id={old_id} (dni={dni})."
                )
            Model.objects.filter(pk=row.pk).update(**{fk_column: new_id})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    """
    Phase 2 of the FK repoint: now that db_constraint=False (0004) lets us write
    arbitrary integers into these columns, remap every old Comisionado id to the
    matching personalizador.Agente id (via dni). This is a separate migration
    (own transaction) from the AlterField that restores the constraint in 0006
    -- Postgres refuses "ALTER TABLE ... ADD CONSTRAINT" on a table that still
    has pending trigger events from an UPDATE earlier in the same transaction.
    """

    dependencies = [
        ('secretariador', '0004_agente_fk_drop_constraint'),
    ]

    operations = [
        migrations.RunPython(remap_fk_ids, noop),
    ]
