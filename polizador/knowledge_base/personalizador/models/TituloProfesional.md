---
symbol: TituloProfesional
kind: class
module: personalizador/models.py
lines: 230-241
signature_hash: sha1:ab4dae04f021004f6e0a8a02d7036d3e2ede6a91
authored: true
---

# TituloProfesional

**Módulo:** `personalizador/models.py` (líneas 230-241) · hereda de `models.Model`

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
