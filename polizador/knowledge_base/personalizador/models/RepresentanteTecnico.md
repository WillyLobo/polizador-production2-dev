---
symbol: RepresentanteTecnico
kind: class
module: personalizador/models.py
lines: 420-438
signature_hash: sha1:401f5a0bb00d7eea7c37e33c1dcca9a6ce0cc081
authored: true
---

# RepresentanteTecnico

**Módulo:** `personalizador/models.py` (líneas 420-438) · hereda de `models.Model`

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
