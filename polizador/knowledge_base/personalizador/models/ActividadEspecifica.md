---
symbol: ActividadEspecifica
kind: class
module: personalizador/models.py
lines: 298-308
signature_hash: sha1:71f5542e3735030f7470865ee0a466527a2aa3a1
authored: true
---

# ActividadEspecifica

**Módulo:** `personalizador/models.py` (líneas 298-308) · hereda de `models.Model`

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
