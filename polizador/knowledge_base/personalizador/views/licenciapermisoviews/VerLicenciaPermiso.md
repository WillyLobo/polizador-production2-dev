---
symbol: VerLicenciaPermiso
kind: class
module: personalizador/views/licenciapermisoviews.py
lines: 75-86
signature_hash: sha1:5f844743953b3cf87fc9e42671157ed72a953d76
authored: true
---

# VerLicenciaPermiso

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 75-86) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de una LicenciaPermiso. Agrega `es_licencia_anual` al contexto (si el tipo es "Anual" o "Anual de Invierno") — el template lo usa para mostrar u ocultar el botón de "Registrar Corte de Licencia", que solo aplica a esos dos tipos.

## Firma

```python
class VerLicenciaPermiso(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`VerLicenciaPermiso` (`personalizador:ver-licenciapermiso`) — también el destino post-guardado de `CrearCorteLicencia`/`UpdateCorteLicencia`.

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
- [CrearCorteLicencia](../cortelicenciaviews/CrearCorteLicencia.md)
