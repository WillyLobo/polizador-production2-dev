---
symbol: CrearCertificadoHechoConsumado
kind: class
module: carga/views/certificadoviews.py
lines: 149-177
signature_hash: sha1:f9b2b73dcc732d2f34b62dda925c9654cc9f78ae
authored: true
---

# CrearCertificadoHechoConsumado

**Módulo:** `carga/views/certificadoviews.py` (líneas 149-177) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Mismo patrón que `CrearCertificadoAnticipo` pero para tipo HECHO_CONSUMADO: fuerza el tipo en `get_form_kwargs`, calcula `certificado_rubro_obra` correlativo, y delega en `certificacion.calcular_monto_hecho_consumado` + `certificacion.aplicar_descuento_anticipo` (un Hecho Consumado también puede tener descuento de anticipo pendiente aplicado).

## Firma

```python
class CrearCertificadoHechoConsumado(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCertificadoHechoConsumado` (`carga:crear-certificado-hechoconsumado`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [CrearCertificadoAnticipo](CrearCertificadoAnticipo.md)
