---
symbol: _build_organigrama_mermaid
kind: function
module: personalizador/views/organigramaviews.py
lines: 16-146
signature_hash: sha1:9f94ddba30815dd7718be823e725b2bb7693306b
authored: true
---

# _build_organigrama_mermaid

**Módulo:** `personalizador/views/organigramaviews.py` (líneas 16-146)

## Propósito

Arma el diagrama completo del organigrama institucional en sintaxis Mermaid
(`flowchart LR`), recorriendo la jerarquía `Directorio → Gerencia → Dirección →
Departamento` de `personalizador.models`, más el caso de dependencias directas de una
Dirección o Departamento bajo un Directorio sin Gerencia intermedia.

## Firma

```python
def _build_organigrama_mermaid():
```

## Uso real

Único caller: `OrganigramaView`, que renderiza el resultado en el template
`organigrama.html`. Candidatos detectados automáticamente:

- `personalizador/views/organigramaviews.py:152` — `mermaid_source, counts = _build_organigrama_mermaid()`

## Flujo de datos

Precarga `Directorio`/`Gerencia`/`Direccion`/`Departamento` en dicts por id (con
`select_related` en Dirección/Departamento) para recorrer la jerarquía sin N+1. Un caso
especial (comentado en el código) ubica "Vocal 1" y "Vocal 2" un rango antes que el nodo
raíz `IPDUV`, sin flecha — para que Mermaid las apile verticalmente a los costados en vez
de cruzarse con las flechas que salen de Presidencia. Cada nodo se etiquetea con
`_mermaid_label`. Devuelve `(mermaid_source, counts)`, donde `counts` es un dict con la
cantidad de unidades por tipo, usado en el template para mostrar totales.

## Ver también

- [_mermaid_label](../organigramaviews/_mermaid_label.md) — arma el texto de cada nodo.
- [OrganigramaView](../organigramaviews/OrganigramaView.md) — único caller.
