---
symbol: GeneroAgente
kind: class
module: personalizador/models.py
lines: 180-189
signature_hash: sha1:c93aa71e5255e355bc2d34c5afdac5435ff8a8bb
authored: true
---

# GeneroAgente

**Módulo:** `personalizador/models.py` (líneas 180-189) · hereda de `models.Model`

## Propósito

Catálogo de géneros (Masculino/Femenino, u otros que se carguen) — usado tanto para `Agente.sexo` como para inferir la abreviatura Sr./Sra. (ver `abreviatura_default_por_sexo`).

## Firma

```python
class GeneroAgente(models.Model):
```

## Uso real

`CrearGeneroAgente`/`UpdateGeneroAgente` (`personalizador/views/generoagenteviews.py`).

## Ver también

- [Agente](Agente.md)
- [abreviatura_default_por_sexo](abreviatura_default_por_sexo.md)
