---
symbol: Provincia
kind: class
module: carga/models.py
lines: 229-241
signature_hash: sha1:9be96fddd9477620c40240a00defc5d92a76834d
authored: true
---

# Provincia

**Módulo:** `carga/models.py` (líneas 229-241) · hereda de `models.Model`

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
