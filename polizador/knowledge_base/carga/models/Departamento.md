---
symbol: Departamento
kind: class
module: carga/models.py
lines: 259-273
signature_hash: sha1:46146712b5f1cf60ffc33899a03c5df20bab073a
authored: true
---

# Departamento

**Módulo:** `carga/models.py` (líneas 259-273) · hereda de `models.Model`

## Propósito

Tabla de referencia geográfica (departamentos de la provincia). Mismo patrón que `Provincia`: `id` explícito, no autoincremental, cargado desde una fuente externa.

## Firma

```python
class Departamento(models.Model):
```

## Uso real

Tabla de solo lectura desde la UI de `carga` — se carga vía fixture/comando.

## Ver también

- [Provincia](Provincia.md)
- [Localidad](Localidad.md)
- [Municipio](Municipio.md)
