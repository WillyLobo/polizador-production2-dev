---
symbol: Direccion
kind: class
module: personalizador/models.py
lines: 420-437
signature_hash: sha1:d44994659dcdad0ec867bb718392a9636d5814ee
authored: true
---

# Direccion

**Módulo:** `personalizador/models.py` (líneas 420-437) · hereda de `models.Model`

## Propósito

Tercer nivel del árbol organizacional. Puede colgar directamente de un `Directorio` o de una `Gerencia` (ambos FK opcionales) — `Oficina.clean()` es quien deriva cuál corresponde según el nodo más específico elegido.

## Firma

```python
class Direccion(models.Model):
```

## Uso real

`direccionwidget`; tercer nivel consumido por [Oficina](Oficina.md).

## Ver también

- [Gerencia](Gerencia.md)
- [Departamento](Departamento.md)
- [Oficina](Oficina.md)
