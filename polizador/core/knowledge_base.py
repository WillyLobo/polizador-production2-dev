"""Extracción y carga de la base de conocimiento del código.

`manage.py kb_extract <app>` usa las funciones de acá para recorrer el código fuente con
`ast` y armar/actualizar `knowledge_base/manifest.json`. `core/views.py` usa `load_tree` y
`resolve_page_path` para servir el índice y las páginas a los superusers. Ver
`knowledge_base/README.md` para el procedimiento completo (extracción mecánica + autoría
manual con Repowise).
"""
import ast
import hashlib
import json
import re
from pathlib import Path

from django.conf import settings

# Fuentes cubiertas en la pasada mecánica. `views/*.py` y `forms/*.py` porque cada app
# de este proyecto las organiza como paquetes (un módulo por modelo), no como
# views.py/forms.py únicos — ver CLAUDE.md.
SOURCE_GLOBS = ("models.py", "signals.py", "views/*.py", "forms/*.py")

FRONT_MATTER_DELIM = "---"


# --------------------------------------------------------------------------------------
# Descubrimiento de archivos fuente
# --------------------------------------------------------------------------------------

def app_dir_for(app_label: str) -> Path:
    return Path(settings.BASE_DIR) / app_label


def iter_source_files(app_dir: Path) -> list[Path]:
    files = []
    for pattern in SOURCE_GLOBS:
        files.extend(sorted(app_dir.glob(pattern)))
    return [f for f in files if f.name != "__init__.py"]


def _module_key(app_dir: Path, path: Path) -> str:
    return path.relative_to(app_dir).with_suffix("").as_posix()


# --------------------------------------------------------------------------------------
# Extracción AST
# --------------------------------------------------------------------------------------

def _function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args = ast.unparse(node.args)
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{prefix} {node.name}({args}){returns}:"


def _class_signature(node: ast.ClassDef, bases: list[str]) -> str:
    inner = ", ".join(bases)
    return f"class {node.name}({inner}):" if inner else f"class {node.name}:"


def _method_info(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict:
    return {
        "name": node.name,
        "signature": _function_signature(node),
        "docstring": ast.get_docstring(node),
        "decorators": [ast.unparse(d) for d in node.decorator_list],
        "lines": [node.lineno, node.end_lineno],
    }


def compute_signature_hash(signature: str, docstring: str | None, lines: tuple[int, int]) -> str:
    payload = f"{signature}\n{docstring or ''}\n{lines[0]}-{lines[1]}"
    return "sha1:" + hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _symbol_info(node: ast.AST, rel_file: str, app_label: str, module_key: str) -> dict:
    kind = "class" if isinstance(node, ast.ClassDef) else "function"
    lines = (node.lineno, node.end_lineno)
    docstring = ast.get_docstring(node)
    decorators = [ast.unparse(d) for d in node.decorator_list]

    if isinstance(node, ast.ClassDef):
        bases = [ast.unparse(b) for b in node.bases] + [
            f"{kw.arg}={ast.unparse(kw.value)}" for kw in node.keywords
        ]
        signature = _class_signature(node, bases)
        methods = [
            _method_info(child)
            for child in node.body
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
    else:
        bases = []
        signature = _function_signature(node)
        methods = []

    return {
        "name": node.name,
        "kind": kind,
        "module": rel_file,
        "page_path": f"{app_label}/{module_key}/{node.name}",
        "signature": signature,
        "docstring": docstring,
        "bases": bases,
        "decorators": decorators,
        "lines": list(lines),
        "methods": methods,
        "signature_hash": compute_signature_hash(signature, docstring, lines),
    }


def _extract_symbols_from_file(path: Path, rel_file: str, app_label: str, module_key: str) -> dict:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    symbols = {}
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            info = _symbol_info(node, rel_file, app_label, module_key)
            symbols[info["name"]] = info
    return symbols


def find_candidate_usages(
    name: str,
    files: list[Path],
    app_dir: Path,
    app_label: str,
    own_rel_file: str,
    own_lines: list[int],
    limit: int = 5,
) -> list[dict]:
    """Grep determinístico de posibles call-sites de `name`, como insumo para la
    autoría (ver knowledge_base/README.md) — no una respuesta final."""
    pattern = re.compile(rf"\b{re.escape(name)}\b")
    found = []
    for path in files:
        rel_file = f"{app_label}/{path.relative_to(app_dir).as_posix()}"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if rel_file == own_rel_file and own_lines[0] <= line_no <= own_lines[1]:
                continue
            if pattern.search(line):
                found.append({"file": rel_file, "line": line_no, "snippet": line.strip()})
                if len(found) >= limit:
                    return found
    return found


def extract_app(app_label: str) -> dict:
    """Devuelve {module_key: {"file": ..., "symbols": {name: {...}}}} para app_label,
    barriendo `models.py`, `signals.py`, `views/*.py` y `forms/*.py` con `ast`."""
    app_dir = app_dir_for(app_label)
    files = iter_source_files(app_dir)

    modules = {}
    for path in files:
        module_key = _module_key(app_dir, path)
        rel_file = f"{app_label}/{path.relative_to(app_dir).as_posix()}"
        symbols = _extract_symbols_from_file(path, rel_file, app_label, module_key)
        if symbols:
            modules[module_key] = {"file": rel_file, "symbols": symbols}

    for module_data in modules.values():
        for symbol in module_data["symbols"].values():
            symbol["candidate_usages"] = find_candidate_usages(
                symbol["name"], files, app_dir, app_label, symbol["module"], symbol["lines"]
            )

    return modules


# --------------------------------------------------------------------------------------
# Manifest (knowledge_base/manifest.json)
# --------------------------------------------------------------------------------------

def manifest_path() -> Path:
    # Función, no constante de módulo: así una app_settings.KNOWLEDGE_BASE_ROOT distinta
    # (ej. override_settings en tests) se respeta en cada llamada, no solo al importar.
    return settings.KNOWLEDGE_BASE_ROOT / "manifest.json"


def load_manifest() -> dict:
    path = manifest_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(manifest: dict) -> None:
    settings.KNOWLEDGE_BASE_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path().write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_tree() -> dict:
    """Árbol app -> módulo -> [símbolos] para las páginas de índice, con las badges
    authored/stale leídas del manifest."""
    manifest = load_manifest()
    tree = {}
    for app_label, app_data in sorted(manifest.items()):
        modules = app_data.get("modules", {})
        tree[app_label] = {
            module_key: [
                {
                    "name": name,
                    "kind": symbol["kind"],
                    "page_path": symbol["page_path"],
                    "authored": symbol.get("authored", False),
                    "stale": symbol.get("stale", False),
                }
                for name, symbol in sorted(module_data.get("symbols", {}).items())
            ]
            for module_key, module_data in sorted(modules.items())
        }
    return tree


def resolve_page_path(page_path: str) -> dict | None:
    """Devuelve el símbolo del manifest para `page_path`, o None si no es conocido.

    Whitelist anti path-traversal: solo hace lookups por clave exacta en el manifest, así
    que un `page_path` con `..` nunca puede matchear una entrada real. Las vistas deben
    resolver siempre por acá antes de tocar el filesystem — nunca construir un Path a
    partir del `page_path` crudo de la URL.
    """
    parts = page_path.split("/")
    if len(parts) < 2:
        return None
    app_label, symbol_name = parts[0], parts[-1]
    module_key = "/".join(parts[1:-1])
    manifest = load_manifest()
    module_data = manifest.get(app_label, {}).get("modules", {}).get(module_key)
    if not module_data:
        return None
    return module_data.get("symbols", {}).get(symbol_name)


# --------------------------------------------------------------------------------------
# Páginas Markdown (front matter + render a HTML)
# --------------------------------------------------------------------------------------

def markdown_path(page_path: str) -> Path:
    return settings.KNOWLEDGE_BASE_ROOT / f"{page_path}.md"


def html_path(page_path: str) -> Path:
    return settings.KNOWLEDGE_BASE_ROOT / f"{page_path}.html"


def parse_front_matter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_DELIM:
        return {}, text
    try:
        end = lines[1:].index(FRONT_MATTER_DELIM) + 1
    except ValueError:
        return {}, text
    front = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        front[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return front, body


def render_front_matter(data: dict) -> str:
    lines = [FRONT_MATTER_DELIM]
    for key, value in data.items():
        lines.append(f"{key}: {value}")
    lines.append(FRONT_MATTER_DELIM)
    return "\n".join(lines) + "\n"


def read_markdown_front_matter(page_path: str) -> dict | None:
    md_file = markdown_path(page_path)
    if not md_file.exists():
        return None
    front, _ = parse_front_matter(md_file.read_text(encoding="utf-8"))
    return front


def render_stub_markdown(symbol: dict) -> str:
    """Contenido inicial de un símbolo nunca antes documentado: front matter completo +
    secciones vacías a completar en la pasada de autoría (ver knowledge_base/README.md)."""
    front = render_front_matter({
        "symbol": symbol["name"],
        "kind": symbol["kind"],
        "module": symbol["module"],
        "lines": f"{symbol['lines'][0]}-{symbol['lines'][1]}",
        "signature_hash": symbol["signature_hash"],
        "authored": "false",
    })

    if symbol["candidate_usages"]:
        candidates = "\n".join(
            f"- `{c['file']}:{c['line']}` — `{c['snippet']}`" for c in symbol["candidate_usages"]
        )
    else:
        candidates = "_(sin candidatos detectados por grep)_"

    body = f"""
# {symbol['name']}

**Módulo:** `{symbol['module']}` (líneas {symbol['lines'][0]}-{symbol['lines'][1]})

## Propósito

_(pendiente de autoría)_

## Firma

```python
{symbol['signature']}
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

{candidates}

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
"""
    return front + body


def render_html_for(page_path: str) -> None:
    """Convierte el `.md` de `page_path` a un `.html` hermano. Único punto del proyecto
    donde se importa el paquete `markdown` — nunca en `core/views.py`, que solo lee el
    `.html` ya generado."""
    import markdown as markdown_lib

    md_file = markdown_path(page_path)
    _, body = parse_front_matter(md_file.read_text(encoding="utf-8"))
    html = markdown_lib.markdown(body, extensions=["fenced_code"])
    html_path(page_path).write_text(html, encoding="utf-8")
