---
symbol: generate_name_resoluciones
kind: function
module: carga/models.py
lines: 71-79
signature_hash: sha1:fda9c9f49f09fa0f726fbfc2dafddd7bb39c97d3
authored: true
---

# generate_name_resoluciones

**Módulo:** `carga/models.py` (líneas 71-79)

## Propósito

**Código muerto retenido a propósito.** Su propio docstring lo explica: existió para un
modelo `ResolucionesDigitales` que ya no está en `models.py`, pero migraciones viejas
todavía referencian esta función por dotted path (`carga.models.generate_name_resoluciones`)
como valor de `upload_to` congelado en su historial. Si se borrara, Django fallaría al
reproducir esas migraciones desde cero (`migrate` en una base nueva, o cualquier replay
completo del historial). No tiene ningún call site vivo en el código actual — no la uses
como referencia para un `FileField` nuevo, mirá `generate_name_obra_documento` o
`generate_name_rubro_documento` en su lugar.

## Firma

```python
def generate_name_resoluciones(instance, filename):
```

## Uso real

Ninguno vivo — solo la referencia congelada en migraciones antiguas de `carga`.

## Ver también

_(sin referencias cruzadas)_
