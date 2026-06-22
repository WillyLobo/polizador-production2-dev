from decimal import Decimal

from django.db import migrations

# carga.Agente rows with no DNI and no matching Comisionado, confirmed by a one-off
# audit of the dev DB. pk -> (dni, gender_code).
MANUAL_LOOKUP = {
    61: ("8300079", "M"),
    59: ("10735091", "M"),
    49: ("33683372", "M"),
    44: ("11016448", "M"),
}
# carga.Agente rows excluded from the merge entirely (confirmed with the user):
# pk=23 "SIN INSPECTOR" is a placeholder used on 200 Obra rows, pk=35 (Susana
# Acuña) is a real inspector on 26 Obra rows whose loss was explicitly accepted.
EXCLUDED_CARGA_PKS = {23, 35}

GENERO_NAMES = {"M": "Masculino", "F": "Femenino"}

PROFESION_TITULOS = {
    "A": ("Arquitecto", "Universitario"),
    "IC": ("Ingeniero Civil", "Universitario"),
    "IE": ("Ingeniero Electromecánico", "Universitario"),
    "MO": ("Maestro Mayor de Obras", "Secundario"),
}


def merge_agentes(apps, schema_editor):
    from secretariador.functions import get_cuil

    CargaAgente = apps.get_model("carga", "Agente")
    Comisionado = apps.get_model("secretariador", "Comisionado")
    Agente = apps.get_model("personalizador", "Agente")
    GeneroAgente = apps.get_model("personalizador", "GeneroAgente")
    TituloProfesional = apps.get_model("personalizador", "TituloProfesional")

    genero_cache = {}
    titulo_cache = {}

    def genero(code):
        if code not in genero_cache:
            genero_cache[code], _ = GeneroAgente.objects.get_or_create(
                generoagente_nombre=GENERO_NAMES[code]
            )
        return genero_cache[code]

    def titulo(code):
        if code not in titulo_cache:
            nombre, grado = PROFESION_TITULOS[code]
            titulo_cache[code], _ = TituloProfesional.objects.get_or_create(
                tituloprofesional_nombre=nombre,
                defaults={"tituloprofesional_grado": grado},
            )
        return titulo_cache[code]

    def upsert(dni, nombres, apellidos, sexo_code, cuil, abreviatura, flags,
               telefono=None, email=None, matricula=None, titulo_code=None):
        agente = Agente.objects.filter(dni=dni).first()
        if agente is None:
            agente = Agente.objects.create(
                dni=dni,
                agente_nombres=nombres,
                agente_apellidos=apellidos,
                sexo=genero(sexo_code),
                cuil=cuil,
                abreviatura=abreviatura,
                telefono=telefono,
                email=email,
                matricula=matricula,
                agente_verificado_contra_padron=flags.get("verificado", False),
                agente_personal_transitorio=flags.get("transitorio", False),
                agente_personal_de_gabinete=flags.get("gabinete", False),
                agente_es_inpector_obra=flags.get("inspector_obra", False),
            )
        else:
            changed = False
            for field, value in (
                ("telefono", telefono), ("email", email),
                ("matricula", matricula), ("abreviatura", abreviatura),
            ):
                if value and not getattr(agente, field):
                    setattr(agente, field, value)
                    changed = True
            for field, key in (
                ("agente_verificado_contra_padron", "verificado"),
                ("agente_personal_transitorio", "transitorio"),
                ("agente_personal_de_gabinete", "gabinete"),
                ("agente_es_inpector_obra", "inspector_obra"),
            ):
                if flags.get(key) and not getattr(agente, field):
                    setattr(agente, field, True)
                    changed = True
            if changed:
                agente.save()
        if titulo_code:
            agente.titulo_profesional.add(titulo(titulo_code))
        return agente

    comisionado_by_dni = {c.comisionado_dni: c for c in Comisionado.objects.all()}
    matched_comisionado_pks = set()

    for carga_agente in CargaAgente.objects.all():
        if carga_agente.pk in EXCLUDED_CARGA_PKS:
            continue

        dni = carga_agente.agente_dni
        comisionado = comisionado_by_dni.get(dni) if dni is not None else None

        if dni is not None and comisionado is not None:
            matched_comisionado_pks.add(comisionado.pk)
            sexo_code = comisionado.comisionado_sexo
            cuil = comisionado.comisionado_cuit
            abreviatura = comisionado.comisionado_abreviatura
            nombres, apellidos = comisionado.comisionado_nombres, comisionado.comisionado_apellidos
            flags = {
                "verificado": comisionado.comisionado_verificado_contra_padron,
                "transitorio": comisionado.comisionado_personal_transitorio,
                "gabinete": comisionado.comisionado_personal_de_gabinete,
                "inspector_obra": True,
            }
        elif carga_agente.pk in MANUAL_LOOKUP:
            dni_str, gender_code = MANUAL_LOOKUP[carga_agente.pk]
            dni = Decimal(dni_str)
            sexo_code = gender_code
            cuil = get_cuil(dni_str, gender_code)
            abreviatura = None
            nombres, apellidos = carga_agente.agente_nombre, carga_agente.agente_apellido
            flags = {"inspector_obra": True}
        else:
            raise RuntimeError(
                f"carga.Agente pk={carga_agente.pk} (dni={dni}) has no matching "
                "Comisionado and no manual DNI/gender lookup entry; the merge "
                "data migration needs an explicit mapping for this row."
            )

        upsert(
            dni, nombres, apellidos, sexo_code, cuil, abreviatura, flags,
            telefono=carga_agente.agente_telefono,
            email=carga_agente.agente_email,
            matricula=carga_agente.agente_matricula,
            titulo_code=carga_agente.agente_profesion,
        )

    for comisionado in Comisionado.objects.exclude(pk__in=matched_comisionado_pks):
        upsert(
            comisionado.comisionado_dni,
            comisionado.comisionado_nombres,
            comisionado.comisionado_apellidos,
            comisionado.comisionado_sexo,
            comisionado.comisionado_cuit,
            comisionado.comisionado_abreviatura,
            {
                "verificado": comisionado.comisionado_verificado_contra_padron,
                "transitorio": comisionado.comisionado_personal_transitorio,
                "gabinete": comisionado.comisionado_personal_de_gabinete,
            },
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("personalizador", "0011_agente_es_inpector_obra"),
        ("carga", "0008_alter_contratosdigitales_contratodigital_archivo_and_more"),
        ("secretariador", "0003_remove_comisionado_comisionado_cargo_decreto_and_more"),
    ]

    operations = [
        migrations.RunPython(merge_agentes, noop),
    ]
