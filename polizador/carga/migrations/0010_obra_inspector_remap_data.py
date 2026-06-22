from decimal import Decimal

from django.db import migrations
from django.db.models import F

# Comfortably above both carga.Agente ids (~1-65) and personalizador.Agente
# ids (~1-700), so offsetting into this range can never numerically collide
# with any real id still sitting unconverted in the table.
ID_OFFSET = 10_000_000

# Same pk -> dni lookup used by personalizador's 0011 data migration, for the
# carga.Agente rows that have no DNI of their own (and so can't be matched to
# a Comisionado/Agente by DNI alone). pk=23 ("SIN INSPECTOR") and pk=35
# (Susana Acuña) are intentionally absent -- excluded from the merge entirely,
# their existing obra_inspector relations are dropped rather than remapped.
MANUAL_LOOKUP_DNI = {
    61: "8300079",
    59: "10735091",
    49: "33683372",
    44: "11016448",
}


def remap_obra_inspector_ids(apps, schema_editor):
    """
    Runs while the through table's agente_id column has no FK constraint at
    all (dropped in 0009), so it's safe to write personalizador.Agente ids
    that don't exist in carga_agente. Relations that can't be mapped (the
    excluded placeholder/no-DNI rows) are dropped instead of left pointing at
    a stale, possibly-coincidentally-valid integer.

    Each through-table row is targeted by its own unique pk, never by the
    agente_id value being rewritten: carga.Agente ids (1-65ish) and
    personalizador.Agente ids overlap numerically, so filtering UPDATEs by
    the mutable old/new value itself lets an already-converted row get
    re-matched (and corrupted) by a later iteration that happens to target
    the same number.

    Two different old carga.Agente rows can also merge into the same
    personalizador.Agente (e.g. one matched a Comisionado directly, the
    other shares that Comisionado's dni another way) -- if both were
    inspectors on the same Obra, remapping both would violate the through
    table's (obra_id, agente_id) uniqueness. The first row to claim a given
    (obra_id, new_id) pair keeps it; later duplicates are dropped instead of
    updated.

    Writing the final new_id directly is also unsafe even with the dedup
    above: carga.Agente ids and personalizador.Agente ids numerically
    overlap, so updating row A to its new_id can collide with row B's
    *old*, not-yet-converted agente_id on the same obra_id, purely because
    that old integer happens to equal A's new one -- the same class of
    collision as the pk-targeting fix, just one level removed (it's the
    target value colliding, not the filter). To dodge this regardless of
    iteration order, every kept row is first shifted to new_id + ID_OFFSET
    (a range no real old or new id can ever reach), and only once every row
    is safely up there does a second pass shift them all back down to their
    true new_id -- by then no unconverted row can still be sitting in that
    low range to collide with.
    """
    OldAgente = apps.get_model('carga', 'Agente')
    NewAgente = apps.get_model('personalizador', 'Agente')
    Through = apps.get_model('carga', 'Obra').obra_inspector.through

    dni_by_old_id = dict(OldAgente.objects.values_list('id', 'agente_dni'))
    for pk, dni_str in MANUAL_LOOKUP_DNI.items():
        dni_by_old_id[pk] = Decimal(dni_str)
    new_id_by_dni = dict(NewAgente.objects.values_list('dni', 'id'))

    to_delete_pks = []
    updated_pks = []
    seen_pairs = set()
    for row in Through.objects.all().only('id', 'agente_id', 'obra_id'):
        dni = dni_by_old_id.get(row.agente_id)
        new_id = new_id_by_dni.get(dni) if dni is not None else None
        if new_id is None:
            to_delete_pks.append(row.pk)
            continue
        pair = (row.obra_id, new_id)
        if pair in seen_pairs:
            to_delete_pks.append(row.pk)
            continue
        seen_pairs.add(pair)
        Through.objects.filter(pk=row.pk).update(agente_id=new_id + ID_OFFSET)
        updated_pks.append(row.pk)
    if to_delete_pks:
        Through.objects.filter(pk__in=to_delete_pks).delete()
    if updated_pks:
        Through.objects.filter(pk__in=updated_pks).update(agente_id=F('agente_id') - ID_OFFSET)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    """
    Phase 2: remap the through table's agente_id values now that the FK
    constraint isn't there to block it (separate migration/transaction from
    0009's DROP CONSTRAINT and 0011's ADD CONSTRAINT -- Postgres refuses DDL on
    a table that has pending trigger events from an UPDATE in the same
    transaction).
    """

    dependencies = [
        ('carga', '0009_obra_inspector_drop_constraint'),
        ('personalizador', '0012_agente_merge_data'),
    ]

    operations = [
        migrations.RunPython(remap_obra_inspector_ids, noop),
    ]
