---
symbol: CargoTipo
kind: class
module: personalizador/models.py
lines: 372-383
signature_hash: sha1:1c8d46c16ae3673c21b1120f11b8265652f9b4d6
authored: true
---

# CargoTipo

**Módulo:** `personalizador/models.py` (líneas 372-383) · hereda de `models.Model`

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
