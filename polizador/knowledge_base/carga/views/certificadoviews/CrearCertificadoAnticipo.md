---
symbol: CrearCertificadoAnticipo
kind: class
module: carga/views/certificadoviews.py
lines: 282-312
signature_hash: sha1:7592dc00d0285d85dda7cb0c74e4638550b585cf
authored: true
---

# CrearCertificadoAnticipo

**Módulo:** `carga/views/certificadoviews.py` (líneas 282-312) · hereda de `PermissionRequiredMixin, generic.CreateView`

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
