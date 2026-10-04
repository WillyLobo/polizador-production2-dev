---
symbol: Region
kind: class
module: carga/models.py
lines: 328-341
signature_hash: sha1:fa09606baf4974412e2ecc89f2645f3584c6c6ef
authored: true
---

# Region

**Módulo:** `carga/models.py` (líneas 328-341) · hereda de `models.Model`

## Propósito

Agrupación administrativa interna simple (`region_numero`), usada para clasificar Obras
(`Obra.obra_region`) y Municipios (`Municipio.municipio_region`). No es una división
geográfica real como Provincia/Departamento/Municipio/Localidad — es más bien una
etiqueta de agrupamiento propia del sistema, sin geometría ni jerarquía asociada.

## Firma

```python
class Region(models.Model):
```

## Uso real

Alta/edición vía `RegionForm` (`carga/forms/regionforms.py`).

## Ver también

- [Obra](Obra.md)
- [Municipio](Municipio.md)
