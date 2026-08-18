---
symbol: Municipio
kind: class
module: carga/models.py
lines: 297-313
signature_hash: sha1:d3cb8abcf1a118aef8254eb5359fbc82805109dd
authored: true
---

# Municipio

**Módulo:** `carga/models.py` (líneas 297-313) · hereda de `models.Model`

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
