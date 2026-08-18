---
symbol: CrearCorteLicencia
kind: class
module: personalizador/views/cortelicenciaviews.py
lines: 15-39
signature_hash: sha1:64a1d8243c2a1841af66abbe3416fafebbc76321
authored: true
---

# CrearCorteLicencia

**Módulo:** `personalizador/views/cortelicenciaviews.py` (líneas 15-39) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un Corte de Licencia sobre una `LicenciaPermiso` puntual (`licenciapermiso_pk` en
la URL, no un querystring). `get_initial` precarga la licencia interrumpida y calcula un
valor por defecto de `cortelicencia_fecha_vencimiento`: el 30 de abril del año siguiente
a la fecha de inicio de la licencia — un default administrativo (probablemente el
vencimiento típico del período de licencias), editable por el usuario si corresponde otra
fecha.

## Firma

```python
class CrearCorteLicencia(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCorteLicencia` (`personalizador:crear-cortelicencia`), enlazada desde `VerLicenciaPermiso` cuando `es_licencia_anual`.

## Ver también

- [CorteLicencia](../../models/CorteLicencia.md)
- [LicenciaPermiso](../../models/LicenciaPermiso.md)
- [VerLicenciaPermiso](../licenciapermisoviews/VerLicenciaPermiso.md)
