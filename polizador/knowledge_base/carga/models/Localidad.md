---
symbol: Localidad
kind: class
module: carga/models.py
lines: 360-380
signature_hash: sha1:a801da8a8cb5534dc277fdc64132672a9e88afcb
authored: true
---

# Localidad

**Módulo:** `carga/models.py` (líneas 360-380) · hereda de `models.Model`

## Propósito

Tabla de referencia geográfica más granular (localidad dentro de un Departamento y un
Municipio), con centroide (`localidad_centroide_lat/lon`) usado para geolocalizar Obras
cuando no se carga una georeferencia puntual propia (ver `Obra.obra_georeferencia`,
`Obra.dd_to_dms()`).

## Firma

```python
class Localidad(models.Model):
```

## Uso real

Tabla de solo lectura desde la UI — `Obra.obra_localidad_m` es un `ManyToManyField` hacia acá, cargado desde el form de Obra.

## Ver también

- [Obra](Obra.md)
- [Departamento](Departamento.md)
- [Municipio](Municipio.md)
