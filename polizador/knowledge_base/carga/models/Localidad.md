---
symbol: Localidad
kind: class
module: carga/models.py
lines: 275-295
signature_hash: sha1:b95602f1a215c0db7af8a892f2d7718dee9ee574
authored: true
---

# Localidad

**Módulo:** `carga/models.py` (líneas 275-295) · hereda de `models.Model`

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
