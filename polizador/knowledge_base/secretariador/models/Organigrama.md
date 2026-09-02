---
symbol: Organigrama
kind: class
module: secretariador/models.py
lines: 347-358
signature_hash: sha1:593800ea065d26d022daca8a95fbe5f4efb9e7f2
authored: true
---
# Organigrama

**Módulo:** `secretariador/models.py` (líneas 347-358) · hereda de `models.Model`

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