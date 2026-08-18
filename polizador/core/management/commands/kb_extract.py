"""
Pasada mecánica de la base de conocimiento del código (ver knowledge_base/README.md).

Recorre `models.py`, `signals.py`, `views/*.py` y `forms/*.py` de la app indicada con
`ast` (sin importar la app Django — rápido y sin efectos secundarios), y actualiza
`knowledge_base/manifest.json` con lo que encuentra. Por cada símbolo (clase o función de
nivel superior) sin `.md` todavía, crea un stub con secciones vacías para completar a
mano; si el `.md` ya existe, compara un hash de firma+docstring+rango de líneas contra el
guardado en su front matter y reporta si quedó desactualizado ("stale") — nunca lo
sobreescribe.

Este comando NO escribe la prosa (propósito, ejemplo de uso, flujo de datos): esa parte
es una pasada de autoría manual, hecha en una sesión de Claude Code con Repowise
conectado, usando los `candidate_usages` que este comando deja en cada stub como punto de
partida. `--render` es la única parte que sí es 100% automática en cada corrida: vuelca
cada `.md` a un `.html` hermano, lo que sí lee `core/views.py` en runtime.

    python manage.py kb_extract carga            # actualiza manifest + crea stubs
    python manage.py kb_extract carga --render    # además regenera .html desde cada .md
    python manage.py kb_extract carga --check     # solo reporta, no escribe nada
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core import knowledge_base as kb


class Command(BaseCommand):
    help = "Extrae clases/funciones de una app (ast) y actualiza knowledge_base/manifest.json."

    def add_arguments(self, parser):
        parser.add_argument("app_label", help="App a barrer, ej. 'carga'.")
        parser.add_argument(
            "--render", action="store_true",
            help="Además de actualizar el manifest, regenera el .html de cada .md de la app.",
        )
        parser.add_argument(
            "--check", action="store_true",
            help="No escribe nada (ni manifest ni stubs ni .html); termina con código de "
                 "salida distinto de cero si hay símbolos nuevos sin .md o páginas stale.",
        )

    def handle(self, *args, **options):
        app_label = options["app_label"]
        render = options["render"]
        check = options["check"]

        if check and render:
            raise CommandError("--check y --render son mutuamente excluyentes (--check no escribe nada).")

        app_dir = kb.app_dir_for(app_label)
        if not app_dir.is_dir():
            raise CommandError(f"No existe el directorio de app '{app_label}' ({app_dir}).")

        modules = kb.extract_app(app_label)
        if not modules:
            self.stdout.write(self.style.WARNING(
                f"No se encontraron símbolos en {app_label} (¿models.py/signals.py/views/*.py/forms/*.py vacíos?)."
            ))

        created, stale, ok = [], [], []
        for module_data in modules.values():
            for symbol in module_data["symbols"].values():
                page_path = symbol["page_path"]
                existing = kb.read_markdown_front_matter(page_path)

                if existing is None:
                    symbol["authored"] = False
                    symbol["stale"] = False
                    created.append(page_path)
                    if not check:
                        md_file = kb.markdown_path(page_path)
                        md_file.parent.mkdir(parents=True, exist_ok=True)
                        md_file.write_text(kb.render_stub_markdown(symbol), encoding="utf-8")
                else:
                    symbol["authored"] = existing.get("authored", "false") == "true"
                    symbol["stale"] = existing.get("signature_hash") != symbol["signature_hash"]
                    (stale if symbol["stale"] else ok).append(page_path)

        if not check:
            manifest = kb.load_manifest()
            manifest[app_label] = {"generated_at": timezone.now().isoformat(), "modules": modules}
            kb.save_manifest(manifest)

        for page_path in created:
            self.stdout.write(f"  creado:  {page_path}.md")
        for page_path in stale:
            self.stdout.write(self.style.WARNING(f"  stale:   {page_path}.md (la firma/docstring/líneas cambiaron)"))

        self.stdout.write(
            f"{app_label}: {len(created)} nuevo(s), {len(stale)} desactualizado(s), {len(ok)} al día."
        )

        if render:
            if not check:
                for module_data in modules.values():
                    for symbol in module_data["symbols"].values():
                        kb.render_html_for(symbol["page_path"])
                self.stdout.write(f"HTML regenerado para {sum(len(m['symbols']) for m in modules.values())} página(s).")

        if check and (created or stale):
            self.stderr.write(self.style.ERROR(
                f"{len(created)} símbolo(s) sin documentar y {len(stale)} página(s) desactualizada(s)."
            ))
            raise SystemExit(1)
