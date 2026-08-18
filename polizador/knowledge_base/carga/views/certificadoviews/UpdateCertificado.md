---
symbol: UpdateCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 354-365
signature_hash: sha1:78f4ba143e7751cd30899f1f5b61b60edef73979
authored: true
---

# UpdateCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 354-365) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Certificado ya cargado, sin restricción de tipo (a diferencia de las vistas de creación especializadas). `form_valid` guarda con `commit=False` primero — vestigial en su forma actual (no hace nada entre medio), probablemente un lugar preparado para lógica futura de recálculo al editar.

## Firma

```python
class UpdateCertificado(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateCertificado` (`carga:update-certificado`).

## Ver también

- [Certificado](../../models/Certificado.md)
