---
symbol: ResolucionWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 40-45
signature_hash: sha1:a14fcf5edb6b0eb07fa9f2dccda343be8d4f7df2
authored: true
---

# ResolucionWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 40-45) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir una `InstrumentosLegalesResoluciones`, buscando por su representación corta, el formato SGT, o la descripción libre.

## Firma

```python
class ResolucionWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Solicitud.solicitud_resolucion`, `Incorporacion.incorporacion_resolucion` (`secretariador`), `Obra.obra_resolucion_fk`, `Contrato.contrato_resolucion_fk`, `ConjuntoLicitado.conjunto_resolucion_fk` (`carga`, vía import directo — ver `carga/forms/obraforms.py`).

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
