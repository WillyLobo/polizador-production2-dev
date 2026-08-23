---
symbol: Departamento
kind: class
module: personalizador/models.py
lines: 400-418
signature_hash: sha1:5c7536e1c9265f3668c5ba99bac002018d33da05
authored: true
---

# Departamento

**Módulo:** `personalizador/models.py` (líneas 400-418) · hereda de `models.Model`

## Propósito

Cuarto y último nivel del árbol organizacional — puede colgar de cualquiera de los tres niveles superiores. **No confundir con `carga.Departamento`** (división geográfica, sin relación alguna con este modelo salvo el nombre).

## Firma

```python
class Departamento(models.Model):
```

## Uso real

`CrearDepartamento`/`UpdateDepartamento` (`personalizador/views/departamentoviews.py`); nivel más específico consumido por [Oficina](Oficina.md).

## Ver también

- [Direccion](Direccion.md)
- [Oficina](Oficina.md)
