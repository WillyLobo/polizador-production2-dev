---
symbol: GeneroAgente
kind: class
module: personalizador/models.py
lines: 219-228
signature_hash: sha1:0c6770b7b06b4609baa3eb97e4c60670eb2b864e
authored: true
---

# GeneroAgente

**Módulo:** `personalizador/models.py` (líneas 219-228) · hereda de `models.Model`

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
