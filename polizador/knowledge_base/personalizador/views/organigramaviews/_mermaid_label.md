---
symbol: _mermaid_label
kind: function
module: personalizador/views/organigramaviews.py
lines: 7-13
signature_hash: sha1:f59091d3a4007638f01e25800076d688a25d5c7d
authored: true
---

# _mermaid_label

**Módulo:** `personalizador/views/organigramaviews.py` (líneas 7-13)

## Propósito

Arma el texto de un nodo del organigrama en sintaxis Mermaid: el nombre de la unidad,
más una línea `<br/>CUOF: ...` y/o `<br/>UNGI: ...` si esos códigos están cargados.
Escapa comillas dobles (reemplazadas por simples) para no romper la sintaxis `["..."]` de
Mermaid al interpolar el label.

## Firma

```python
def _mermaid_label(nombre, cuof=None, ungi=None):
```

## Uso real

Se llama una vez por cada Directorio/Gerencia/Dirección/Departamento que
`_build_organigrama_mermaid` agrega al diagrama, pasándole los campos `*_nombre`,
`*_cuof` y `*_ungi` del modelo correspondiente. Candidatos detectados automáticamente:

- `personalizador/views/organigramaviews.py:53` — `f'{indent}P{p.id}["{_mermaid_label(p.departamento_nombre, p.departamento_cuof, p.departamento_ungi)}"]'`
- `personalizador/views/organigramaviews.py:70` — `lines.append(f'    D{vocal1_id}["{_mermaid_label(d1.directorio_nombre, d1.directorio_cuof, d1.directorio_ungi)}"]')`
- `personalizador/views/organigramaviews.py:72` — `lines.append(f'    D{vocal2_id}["{_mermaid_label(d2.directorio_nombre, d2.directorio_cuof, d2.directorio_ungi)}"]')`
- `personalizador/views/organigramaviews.py:82` — `lines.append(f'    D{did}["{_mermaid_label(d.directorio_nombre, d.directorio_cuof, d.directorio_ungi)}"]')`
- `personalizador/views/organigramaviews.py:88` — `lines.append(f'        G{g.id}["{_mermaid_label(g.gerencia_nombre, g.gerencia_cuof, g.gerencia_ungi)}"]')`

## Flujo de datos

Campos `*_nombre`/`*_cuof`/`*_ungi` de los modelos de `personalizador`
(Directorio/Gerencia/Direccion/Departamento) → string interpolado directo en una línea
de sintaxis Mermaid dentro de `_build_organigrama_mermaid`.

## Ver también

- [_build_organigrama_mermaid](../organigramaviews/_build_organigrama_mermaid.md) — único caller, arma el diagrama completo.
- [OrganigramaView](../organigramaviews/OrganigramaView.md) — vista que sirve el diagrama.
