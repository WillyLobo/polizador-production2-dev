---
symbol: Region
kind: class
module: carga/models.py
lines: 243-256
signature_hash: sha1:581812bfda15800658e0a518d8419f04973d671a
authored: true
---

# Region

**Módulo:** `carga/models.py` (líneas 243-256) · hereda de `models.Model`

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
