---
symbol: RepresentanteTecnico
kind: class
module: personalizador/models.py
lines: 459-477
signature_hash: sha1:e430a9ff84160378b99d6e9b6f8b43754779e8ac
authored: true
---

# RepresentanteTecnico

**Módulo:** `personalizador/models.py` (líneas 459-477) · hereda de `models.Model`

## Propósito

Profesional externo (arquitecto, ingeniero...) responsable técnico de una Obra de `carga` — no es un `Agente` (no es empleado del organismo). Vive en `personalizador` pero su CRUD web está en `carga` (`carga/views/representantetecnicoviews.py`), ver esa página.

## Firma

```python
class RepresentanteTecnico(models.Model):
```

## Uso real

`Obra.obra_representantetecnico` (M2M, `carga/models.py`).

## Ver también

- [TituloProfesional](TituloProfesional.md)
