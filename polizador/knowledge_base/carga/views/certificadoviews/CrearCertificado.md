---
symbol: CrearCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 192-226
signature_hash: sha1:8f1e456bdced07d9c9b6322a6141953754da7b0b
authored: true
---

# CrearCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 192-226) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta manual de un Certificado (`CertificadoForm`, sin tipo forzado — a diferencia de
`CrearCertificadoAnticipo`/`CrearCertificadoHechoConsumado`). Si viene `?foja=<id>` por
querystring, precarga Obra/Foja/mes%/acumulado% desde esa Foja. `form_valid` decide
`certificado_fecha_carga`: si no es legacy, la fecha de carga es "ahora"; si es legacy, se
usa la propia `certificado_fecha` (para no falsear cuándo se cargó un certificado viejo).

## Firma

```python
class CrearCertificado(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCertificado` (`carga:crear-certificado`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [GenerarCertificadosDesdeFoja](GenerarCertificadosDesdeFoja.md) — el flujo normal (no manual) de generar certificados.
