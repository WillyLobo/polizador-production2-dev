---
symbol: GenerarCertificadosDesdeFoja
kind: class
module: carga/views/certificadoviews.py
lines: 230-278
signature_hash: sha1:7f81cb086103b9943a3ec9d3895a2aa286f0af02
authored: true
---

# GenerarCertificadosDesdeFoja

**Módulo:** `carga/views/certificadoviews.py` (líneas 230-278) · hereda de `PermissionRequiredMixin, generic.View`

## Propósito

El flujo normal de certificación: a partir de una Foja de Medición ya cargada, construye
(sin guardar — `preview=True`) los Certificados que correspondería generar
(`construir_certificados_desde_foja`, `carga/certificacion.py`), se los muestra al
usuario, y solo los persiste (`generar_certificados_desde_foja`) cuando confirma
explícitamente (`"confirmar" in request.POST`) — un patrón de "vista previa antes de
confirmar" para una operación que no es trivialmente reversible. Atrapa tanto
`ValidationError` (reglas de negocio) como `Ley27397Error` (fallas del cálculo de
indexación) y las muestra como error de formulario en vez de un 500.

## Firma

```python
class GenerarCertificadosDesdeFoja(PermissionRequiredMixin, generic.View):
```

## Uso real

`GenerarCertificadosDesdeFoja` (`carga:generar-certificados-foja`), enlazada desde la ficha de la Foja de Medición.

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [Certificado](../../models/Certificado.md)
