import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from personalizador.models import Agente

DEFAULT_PATH = settings.BASE_DIR.parent / "env" / ".snipets" / "agentes_padron.json"


def _oficina_natural_key(oficina):
    """Identifica una Oficina por el C.U.O.F. de su unidad organizativa mas
    profunda en vez de por su PK, para poder resolverla contra el organigrama
    de otra base de datos (ver _resolver_oficina en importar_agentes_padron)."""
    if oficina is None:
        return None
    if oficina.cargo_departamento_id:
        return {"nivel": "departamento", "cuof": oficina.cargo_departamento.departamento_cuof}
    if oficina.cargo_direccion_id:
        return {"nivel": "direccion", "cuof": oficina.cargo_direccion.direccion_cuof}
    if oficina.cargo_gerencia_id:
        return {"nivel": "gerencia", "cuof": oficina.cargo_gerencia.gerencia_cuof}
    if oficina.cargo_directorio_id:
        return {"nivel": "directorio", "cuof": oficina.cargo_directorio.directorio_cuof}
    return None


class Command(BaseCommand):
    help = (
        "Exporta a un JSON, indexado por D.N.I., los campos de Agente completados o "
        "corregidos por dni_check, crear_agentes_faltantes e importar_informe_ipduv "
        "(nombre, apellido, domicilio, verificacion contra el padron, categoria, "
        "cargo, oficina, etc). Cada catalogo (Categoria, Oficina, DenominacionCargo, "
        "etc.) se referencia por su clave de negocio (codigo/nombre/CUOF) en vez de "
        "su PK, para poder aplicarse con importar_agentes_padron sobre otra base de "
        "datos (produccion) donde esos IDs no necesariamente coinciden con los de "
        "esta base."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output", default=str(DEFAULT_PATH),
            help="Ruta del JSON a generar (default: %(default)s)",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        verbosity = options.get("verbosity", 1)

        qs = Agente.objects.select_related(
            "sexo", "categoria", "denominacion_cargo", "apartado", "ceic", "grupo",
            "actividad_especifica", "oficina",
            "oficina__cargo_departamento", "oficina__cargo_direccion",
            "oficina__cargo_gerencia", "oficina__cargo_directorio",
        ).order_by("dni")

        registros = []
        for agente in qs:
            registro = {"dni": int(agente.dni)}

            # Campos que dni_check/crear_agentes_faltantes solo tocan cuando el
            # agente fue efectivamente encontrado (o recien creado) contra el
            # padron: se exportan juntos, bajo esa misma condicion.
            if agente.agente_verificado_contra_padron:
                registro["agente_verificado_contra_padron"] = True
                registro["agente_nombres"] = agente.agente_nombres
                registro["agente_apellidos"] = agente.agente_apellidos
                registro["cuil"] = agente.cuil
                registro["sexo"] = agente.sexo.generoagente_nombre
                if agente.domicilio_direccion:
                    registro["domicilio_direccion"] = agente.domicilio_direccion

            # Campos que importar_informe_ipduv completa independientemente de
            # la verificacion contra el padron.
            if agente.n_legajo is not None:
                registro["n_legajo"] = agente.n_legajo
            if agente.fecha_nacimiento is not None:
                registro["fecha_nacimiento"] = agente.fecha_nacimiento.isoformat()
            if agente.categoria_id is not None:
                registro["categoria_codigo"] = int(agente.categoria.categoria_codigo)
            if agente.denominacion_cargo_id is not None:
                registro["denominacion_cargo"] = agente.denominacion_cargo.denominacion
            if agente.apartado_id is not None:
                registro["apartado"] = agente.apartado.apartadocargo_denominacion
            if agente.ceic_id is not None:
                registro["ceic"] = agente.ceic.ceic
            if agente.grupo_id is not None:
                registro["grupo"] = int(agente.grupo.grupo_numero)
            if agente.activdad_central and agente.activdad_central != "1":
                registro["activdad_central"] = agente.activdad_central
            if agente.actividad_especifica_id is not None:
                registro["actividad_especifica_codigo"] = int(agente.actividad_especifica.actividad_especifica_codigo)
            oficina_key = _oficina_natural_key(agente.oficina)
            if oficina_key is not None:
                registro["oficina"] = oficina_key

            registros.append(registro)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)

        if verbosity >= 1:
            self.stdout.write(self.style.SUCCESS(f"Exportados {len(registros)} agentes a {output_path}"))
