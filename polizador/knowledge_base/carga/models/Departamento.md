---
symbol: Departamento
kind: class
module: carga/models.py
lines: 344-358
signature_hash: sha1:5ff4ba663724a9c83054a23463590848d961cbd6
authored: true
---

# Departamento

**Módulo:** `carga/models.py` (líneas 344-358) · hereda de `models.Model`

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
