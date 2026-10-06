---
symbol: Prototipo
kind: class
module: carga/models.py
lines: 670-691
signature_hash: sha1:e7a7a096eb3101fe28c936f537e08f30dcf0dd1f
authored: true
---

# Prototipo

**Módulo:** `carga/models.py` (líneas 670-691) · hereda de `models.Model`

## Propósito

Modela un "prototipo habitacional" (tipología de vivienda: 1/2/3/4 dormitorios u otro) con
su cantidad, superficie y UVIs por m² dentro de una Obra — pensado para obras de vivienda
con varias tipologías de unidad.

**Aparentemente sin uso activo desde la UI de `carga`:** no aparece ningún `PrototipoForm`
ni vista en `carga/views/`/`carga/forms/` — solo está registrado en el admin de Django
(`carga/admin.py::PrototipoAdmin`, con soporte de import/export vía
`resources.PrototipoResource`). Si necesitás cargar/editar Prototipos hoy, es vía
`/admin/`, no desde el sitio.

## Firma

```python
class Prototipo(models.Model):
```

## Uso real

Alta/edición actual: `/admin/carga/prototipo/` (Django admin), no hay flujo en la UI de `carga`.

## Ver también

- [Obra](Obra.md)
