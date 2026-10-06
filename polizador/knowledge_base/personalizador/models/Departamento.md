---
symbol: Departamento
kind: class
module: personalizador/models.py
lines: 439-457
signature_hash: sha1:7aa6df6551fa73725ceefd09a7da5472cc167645
authored: true
---

# Departamento

**Módulo:** `personalizador/models.py` (líneas 439-457) · hereda de `models.Model`

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
