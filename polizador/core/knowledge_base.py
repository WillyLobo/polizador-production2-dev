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
import unicodedata
from pathlib import Path

from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe

# Fuentes cubiertas en la pasada mecánica. La mayoría de las apps de este proyecto
# organizan views/forms como paquetes (un módulo por modelo, ver CLAUDE.md), de ahí
# `views/*.py`/`forms/*.py`; algunas apps más chicas (ej. `core`) los tienen como archivo
# único, de ahí `views.py`/`forms.py` sueltos. Los `views.py`/`forms.py` sueltos que
# quedaron como stub muerto en apps con paquete (carga, secretariador, personalizador)
# no generan ningún símbolo, así que incluir el patrón acá es inocuo para esas apps.
SOURCE_GLOBS = ("models.py", "signals.py", "views.py", "views/*.py", "forms.py", "forms/*.py")

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


# --------------------------------------------------------------------------------------
# Búsqueda
# --------------------------------------------------------------------------------------

# Puntaje por término según dónde aparece. El nombre del símbolo pesa mucho más que la
# prosa: quien busca "Poliza" casi siempre quiere la página del modelo, no las 40 que lo
# mencionan en "Ver también".
SCORE_NAME_EXACT = 100
SCORE_NAME_PREFIX = 50
SCORE_NAME_CONTAINS = 30
SCORE_MODULE = 10
SCORE_BODY_MAX = 10  # tope de ocurrencias en el cuerpo que suman (1 punto cada una)
SCORE_PHRASE = 20  # la consulta entera, tal cual, aparece en el cuerpo

# Palabras que aparecen en casi todas las páginas: con ellas "fondo de reparo" ordenaba
# por cantidad de "de". Se ignoran, salvo que la consulta sea solo eso.
STOPWORDS = frozenset(
    "a al con de del el en es la las lo los o para por que se su sus un una y".split()
)

SNIPPET_RADIUS = 90

_MD_LINK_TEXT_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MD_NOISE_RE = re.compile(r"[`*#|]+|^\s*>", re.M)
_WHITESPACE_RE = re.compile(r"\s+")


def _fold(text: str) -> str:
    """Minúsculas y sin tildes, para que "poliza" encuentre "Póliza" y viceversa."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def _fold_with_map(text: str) -> tuple[str, list[int]]:
    """Como `_fold`, pero devuelve además, por cada carácter del texto plegado, el índice
    del carácter original del que salió — para resaltar sobre el texto original."""
    folded, index_map = [], []
    for i, char in enumerate(text):
        for c in _fold(char):
            folded.append(c)
            index_map.append(i)
    return "".join(folded), index_map


def _searchable_body(markdown_body: str) -> str:
    """Prosa de la página en texto plano: sin títulos (el de la página repite el nombre;
    los de sección, "Propósito"/"Ver también", están en todas), sin la línea **Módulo:**
    (el módulo ya puntúa por separado) y sin la sintaxis
    Markdown, pero conservando el código, para poder buscar por nombre de campo."""
    lines = [
        line for line in markdown_body.splitlines()
        if not line.startswith("#") and not line.startswith("**Módulo:**")
    ]
    text = _MD_LINK_TEXT_RE.sub(r"\1", "\n".join(lines))
    text = _MD_NOISE_RE.sub(" ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _highlight(text: str, terms: list[str]) -> str:
    """`text` escapado, con cada aparición de `terms` envuelta en <mark>."""
    folded, index_map = _fold_with_map(text)
    spans = []
    for term in terms:
        start = folded.find(term)
        while start != -1:
            end = start + len(term)
            spans.append((index_map[start], index_map[end - 1] + 1))
            start = folded.find(term, end)
    spans.sort()
    parts, cursor = [], 0
    for start, end in spans:
        if start < cursor:  # superpuesto con el anterior
            start = cursor
            if start >= end:
                continue
        parts.append(escape(text[cursor:start]))
        parts.append(f"<mark>{escape(text[start:end])}</mark>")
        cursor = end
    parts.append(escape(text[cursor:]))
    return "".join(parts)


def _snippet(body: str, folded_body: str, terms: list[str], phrase: str) -> str:
    """Fragmento del cuerpo centrado en la frase completa si aparece, si no en el término
    más largo que aparezca (el más específico). Si ninguno aparece en el cuerpo (matcheó
    solo por nombre/módulo), el comienzo."""
    positions = [folded_body.find(phrase)] if phrase in folded_body else []
    if not positions:
        positions = [folded_body.find(t) for t in sorted(terms, key=len, reverse=True) if t in folded_body][:1]
    if not positions:
        return _highlight(body[: SNIPPET_RADIUS * 2], terms) + ("…" if len(body) > SNIPPET_RADIUS * 2 else "")
    # Las posiciones son sobre el texto plegado; se mapean al original.
    _, index_map = _fold_with_map(body)
    center = index_map[min(positions)]
    start = max(0, center - SNIPPET_RADIUS)
    end = min(len(body), center + SNIPPET_RADIUS)
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(body) else ""
    return prefix + _highlight(body[start:end], terms) + suffix


def search(query: str, limit: int = 50) -> tuple[list[dict], int]:
    """Busca `query` en nombre, módulo y prosa de todas las páginas del manifest.

    Cada palabra de la consulta (salvo `STOPWORDS`) tiene que aparecer en algún lado
    (AND), sin distinguir mayúsculas ni tildes; la frase completa en el cuerpo suma extra. Devuelve `(resultados, total)`: los `limit` mejores ordenados
    por puntaje, y cuántas páginas matchearon en total. Lee los `.md` en cada llamada:
    son ~800 archivos chicos, solo para superusers, y así lo que se edita a mano se
    encuentra sin reiniciar nada."""
    words = _fold(query).split()
    terms = list(dict.fromkeys(w for w in words if w not in STOPWORDS)) or list(dict.fromkeys(words))
    if not terms:
        return [], 0
    phrase = " ".join(words) if len(words) > 1 else ""

    results = []
    for app_label, app_data in load_manifest().items():
        for module_key, module_data in app_data.get("modules", {}).items():
            for name, symbol in module_data.get("symbols", {}).items():
                page_path = symbol["page_path"]
                md_file = markdown_path(page_path)
                body = ""
                if md_file.exists():
                    _, markdown_body = parse_front_matter(md_file.read_text(encoding="utf-8"))
                    body = _searchable_body(markdown_body)
                folded_name = _fold(name)
                folded_module = _fold(f"{app_label}/{module_key}")
                folded_body = _fold(body)

                score = 0
                for term in terms:
                    if folded_name == term:
                        term_score = SCORE_NAME_EXACT
                    elif folded_name.startswith(term):
                        term_score = SCORE_NAME_PREFIX
                    elif term in folded_name:
                        term_score = SCORE_NAME_CONTAINS
                    else:
                        term_score = 0
                    if term in folded_module:
                        term_score += SCORE_MODULE
                    term_score += min(folded_body.count(term), SCORE_BODY_MAX)
                    if term_score == 0:
                        break
                    score += term_score
                else:
                    if phrase and phrase in folded_body:
                        score += SCORE_PHRASE
                    results.append({
                        "name": name,
                        "kind": symbol["kind"],
                        "page_path": page_path,
                        "module": f"{app_label}/{module_key}",
                        "authored": symbol.get("authored", False),
                        "stale": symbol.get("stale", False),
                        "score": score,
                        "_body": body,
                        "_folded_body": folded_body,
                    })

    results.sort(key=lambda r: (-r["score"], r["name"].casefold(), r["page_path"]))
    top = results[:limit]
    for result in top:
        result["snippet_html"] = mark_safe(_snippet(result.pop("_body"), result.pop("_folded_body"), terms, phrase or terms[0]))
    return top, len(results)
