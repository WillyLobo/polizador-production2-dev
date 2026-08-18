---
symbol: ActividadEspecifica
kind: class
module: personalizador/models.py
lines: 259-269
signature_hash: sha1:1377b1e26e5b51b0810c027f0fe3ce11143c1236
authored: true
---

# ActividadEspecifica

**Módulo:** `personalizador/models.py` (líneas 259-269) · hereda de `models.Model`

## Propósito

Catálogo de actividades específicas (código + nombre) — usado en `Agente.actividad_especifica`, complementario al campo `activdad_central` (charfield libre, no FK, con "actividad" mal escrito en el nombre del campo pero así está en la base).

## Firma

```python
class ActividadEspecifica(models.Model):
```

## Uso real

`CrearActividadEspecifica`/`UpdateActividadEspecifica` (`personalizador/views/actividadespecificaviews.py`).

## Ver también

- [Agente](Agente.md)
