---
symbol: Provincia
kind: class
module: carga/models.py
lines: 314-326
signature_hash: sha1:dcd1a241b3b1d09a4d04aefb5c008cfd2c8b3591
authored: true
---

# Provincia

**Módulo:** `carga/models.py` (líneas 314-326) · hereda de `models.Model`

## Propósito

Tabla de referencia geográfica (provincias de Argentina). La `id` es un `IntegerField`
explícito, no autoincremental — se carga desde una fuente externa (probablemente el
nomenclador de INDEC/IGN) que ya trae sus propios códigos numéricos, y el modelo los
respeta en vez de generar sus propios PKs.

## Firma

```python
class Provincia(models.Model):
```

## Uso real

Tabla de solo lectura para el usuario final: no tiene form ni vista de creación en `carga` — se carga vía fixture/comando, no desde la UI.

## Ver también

- [Departamento](Departamento.md)
- [Localidad](Localidad.md)
