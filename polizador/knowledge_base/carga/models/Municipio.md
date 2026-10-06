---
symbol: Municipio
kind: class
module: carga/models.py
lines: 382-398
signature_hash: sha1:3012c4d99e49478846e7036fa2fbbd9b63c966ab
authored: true
---

# Municipio

**Módulo:** `carga/models.py` (líneas 382-398) · hereda de `models.Model`

## Propósito

Tabla de referencia geográfica intermedia entre Departamento y Localidad, con un `Region` asociado (agrupación administrativa interna, no geográfica).

## Firma

```python
class Municipio(models.Model):
```

## Uso real

Tabla de solo lectura desde la UI — `Obra.obra_municipio_m` es un `ManyToManyField` hacia acá.

## Ver también

- [Obra](Obra.md)
- [Departamento](Departamento.md)
- [Localidad](Localidad.md)
- [Region](Region.md)
