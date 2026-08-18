---
symbol: CargoTipo
kind: class
module: personalizador/models.py
lines: 333-344
signature_hash: sha1:feb714b4d084f9202d6fd02f22bc0d3d1ab8a502
authored: true
---

# CargoTipo

**Módulo:** `personalizador/models.py` (líneas 333-344) · hereda de `models.Model`

## Propósito

Catálogo de tipos de cargo (ej. "Personal Transitorio", "Contrato de Servicio", "Planta Permanente", "Gabinete" — ver el comentario en `Meta`). No tiene ningún FK visible desde otro modelo de este archivo en el subconjunto que cubre este manifest — puede consumirse desde otro lado (templates, u otra app) sin que aparezca acá.

## Firma

```python
class CargoTipo(models.Model):
```

## Uso real

`CrearCargoTipo`/`UpdateCargoTipo` (`personalizador/views/cargotipoviews.py`).

## Ver también

_(sin referencias cruzadas)_
