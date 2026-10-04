---
symbol: _firmante_organigrama
kind: function
module: carga/views/polizaviews.py
lines: 14-32
signature_hash: sha1:73f8bd5ddad7b7e9fadd3ac4ab7fb3047175119b
authored: true
---

# _firmante_organigrama

**Módulo:** `carga/views/polizaviews.py` (líneas 14-32)

## Propósito

Arma el bloque de firma de un `Agente` según el organigrama: `{agente, cargo, unidad,
unidad_padre}`. La oficina es la designación temporal (`cargo_interno`) si tiene una y, si
no, su `oficina`. La `unidad` es la más específica de esa oficina (Departamento →
Dirección → Gerencia → Directorio). `unidad_padre` es la Gerencia, sólo cuando no coincide
con la unidad. Devuelve `None` sin agente, y `unidad=None` si el agente no tiene oficina
cargada.

## Firma

```python
def _firmante_organigrama(agente):
```

## Uso real

```python
# carga/views/polizaviews.py (ImprimirPolizaMovimiento.get_context_data)
context["firmante"] = _firmante_organigrama(agente)
```

## Ver también

- [ImprimirPolizaMovimiento](ImprimirPolizaMovimiento.md)
- [Agente](../../../personalizador/models/Agente.md)
