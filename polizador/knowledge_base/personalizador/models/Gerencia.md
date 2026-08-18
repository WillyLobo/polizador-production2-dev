---
symbol: Gerencia
kind: class
module: personalizador/models.py
lines: 363-379
signature_hash: sha1:167c33a7a95ff11bc64719681161187800529e98
authored: true
---

# Gerencia

**Módulo:** `personalizador/models.py` (líneas 363-379) · hereda de `models.Model`

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
