---
symbol: TituloProfesional
kind: class
module: personalizador/models.py
lines: 191-202
signature_hash: sha1:ea7eb00d6ffbf5a1ab4e898d026b92ed9887deaa
authored: true
---

# TituloProfesional

**Módulo:** `personalizador/models.py` (líneas 191-202) · hereda de `models.Model`

## Propósito

Catálogo de títulos profesionales (nombre completo sin abreviaturas + abreviatura + grado académico) — compartido entre `Agente.titulo_profesional` (M2M) y `RepresentanteTecnico.representantetecnico_profesion` (FK).

## Firma

```python
class TituloProfesional(models.Model):
```

## Uso real

`CrearTituloProfesional`/`UpdateTituloProfesional` (`personalizador/views/tituloprofesionalviews.py`).

## Ver también

- [Agente](Agente.md)
- [RepresentanteTecnico](RepresentanteTecnico.md)
