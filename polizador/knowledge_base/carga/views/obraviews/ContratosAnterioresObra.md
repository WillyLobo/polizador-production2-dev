---
symbol: ContratosAnterioresObra
kind: class
module: carga/views/obraviews.py
lines: 149-162
signature_hash: sha1:379a7e4372070300fdacb12e0566278a706532a5
authored: true
---

# ContratosAnterioresObra

**Módulo:** `carga/views/obraviews.py` (líneas 149-162) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Mismo patrón que `PlanesAnterioresObra` pero para Contratos: lista los que no son el vigente (`Obra.contrato_vigente()`).

## Firma

```python
class ContratosAnterioresObra(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ContratosAnterioresObra` (`carga:contratos-anteriores-obra`), enlazada desde `UpdateObra` cuando `tiene_contratos_anteriores`.

## Ver también

- [Contrato](../../models/Contrato.md)
- [Obra](../../models/Obra.md)
