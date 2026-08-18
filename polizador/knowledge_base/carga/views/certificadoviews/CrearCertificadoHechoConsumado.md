---
symbol: CrearCertificadoHechoConsumado
kind: class
module: carga/views/certificadoviews.py
lines: 316-344
signature_hash: sha1:17f5a410f8e5303260970a8bb204ebcbc3193161
authored: true
---

# CrearCertificadoHechoConsumado

**Módulo:** `carga/views/certificadoviews.py` (líneas 316-344) · hereda de `PermissionRequiredMixin, generic.CreateView`

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
