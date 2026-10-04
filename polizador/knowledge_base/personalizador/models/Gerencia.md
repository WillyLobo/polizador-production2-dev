---
symbol: Gerencia
kind: class
module: personalizador/models.py
lines: 402-418
signature_hash: sha1:16d36bbde7234c5b7c18a8f01e1c900c368b5d3c
authored: true
---

# Gerencia

**Módulo:** `personalizador/models.py` (líneas 402-418) · hereda de `models.Model`

## Propósito

Segundo nivel del árbol organizacional, colgando de un `Directorio`. Mismo patrón de autoridad a cargo (texto + FK) que `Directorio`.

## Firma

```python
class Gerencia(models.Model):
```

## Uso real

`gerenciawidget`; segundo nivel consumido por [Oficina](Oficina.md).

## Ver también

- [Directorio](Directorio.md)
- [Direccion](Direccion.md)
- [Oficina](Oficina.md)
