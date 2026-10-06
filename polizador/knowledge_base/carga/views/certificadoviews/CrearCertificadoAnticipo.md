---
symbol: CrearCertificadoAnticipo
kind: class
module: carga/views/certificadoviews.py
lines: 115-145
signature_hash: sha1:c6d86320d0ecd7308c7dc4e6ac75d55cc88701c8
authored: true
---

# CrearCertificadoAnticipo

**Módulo:** `carga/views/certificadoviews.py` (líneas 115-145) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta especializada de un Certificado tipo ANTICIPO. `get_form_kwargs` fuerza
`certificado_tipo="ANTICIPO"` en la instancia **antes** de que el `ModelForm` la valide —
necesario porque `Certificado.clean()` decide qué campos zapatear/exigir según el tipo, y
`clean()` corre dentro de `form.is_valid()`, antes de que `form_valid()` llegue a
ejecutarse. `form_valid` calcula `certificado_rubro_anticipo` (correlativo por
obra+financiamiento, vía `certificacion.siguiente_numero`) y delega en
`certificacion.calcular_monto_anticipo` el cálculo real del monto — este método no lo
hace, solo orquesta.

## Firma

```python
class CrearCertificadoAnticipo(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCertificadoAnticipo` (`carga:crear-certificado-anticipo`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [CrearCertificadoHechoConsumado](CrearCertificadoHechoConsumado.md) — mismo patrón de `get_form_kwargs`.
