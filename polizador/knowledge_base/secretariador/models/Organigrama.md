---
symbol: Organigrama
kind: class
module: secretariador/models.py
lines: 337-348
signature_hash: sha1:419032e7a971537a3475f46119e8cdfd91d545e6
authored: true
---

# Organigrama

**Módulo:** `secretariador/models.py` (líneas 337-348) · hereda de `models.Model`

## Propósito

Catálogo simple (cargo + escalafón) — a diferencia de `personalizador.Oficina`/`Directorio`/`Gerencia`/etc. (el árbol organizacional real), este modelo parece una tabla de referencia standalone sin FK hacia/desde otros modelos de este manifest — posiblemente informativa o usada solo desde un reporte/template no cubierto acá.

## Firma

```python
class Organigrama(models.Model):
```

## Uso real

`OrganigramaForm` (`secretariador/forms/organigramaform.py`) — no se encontró una vista de listado/CRUD en `secretariador/views/*.py` que la use (podría gestionarse solo desde `/admin/`).

## Ver también

_(sin referencias cruzadas)_
