---
symbol: GenerarCertificadosDesdeFoja
kind: class
module: carga/views/certificadoviews.py
lines: 73-111
signature_hash: sha1:dd889c375efc61d312da7c7b7fefcac178d22c3b
authored: true
---

# GenerarCertificadosDesdeFoja

**Módulo:** `carga/views/certificadoviews.py` (líneas 73-111) · hereda de `PermissionRequiredMixin, generic.View`

## Propósito

El flujo normal de certificación: a partir de una Foja de Medición ya cargada, construye
(sin guardar — `preview=True`) los Certificados que correspondería generar
(`construir_certificados_desde_foja`, `carga/certificacion.py`), se los muestra al
usuario, y solo los persiste (`generar_certificados_desde_foja`) cuando confirma
explícitamente (`"confirmar" in request.POST`) — un patrón de "vista previa antes de
confirmar" para una operación que no es trivialmente reversible. Atrapa tanto
`ValidationError` (reglas de negocio) como `Ley27397Error` (fallas del cálculo de
indexación) y las muestra como error de formulario en vez de un 500.

La tabla de la vista previa ya no calcula aparte el "monto a cobrar". Cada fila es
`{"certificado": c}` y el template usa `certificado_importe_abonar_pesos()`/`_uvi()` del
propio modelo, que también descuentan el Fondo de Reparo. Así la vista previa muestra lo
mismo que la hoja impresa.

## Firma

```python
class GenerarCertificadosDesdeFoja(PermissionRequiredMixin, generic.View):
```

## Uso real

`GenerarCertificadosDesdeFoja` (`carga:generar-certificados-foja`), enlazada desde la ficha de la Foja de Medición.

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [Certificado](../../models/Certificado.md)
