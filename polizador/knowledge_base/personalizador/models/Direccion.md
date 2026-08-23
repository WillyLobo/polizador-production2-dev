---
symbol: Direccion
kind: class
module: personalizador/models.py
lines: 381-398
signature_hash: sha1:16746bf2f0515293ca5632836f0c526aa9f7fbbe
authored: true
---

# Direccion

**Módulo:** `personalizador/models.py` (líneas 381-398) · hereda de `models.Model`

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
