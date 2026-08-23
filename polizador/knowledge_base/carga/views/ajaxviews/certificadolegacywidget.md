---
symbol: certificadolegacywidget
kind: class
module: carga/views/ajaxviews.py
lines: 124-137
signature_hash: sha1:9da06354964f6a4a3aab27f3fe9396f67d6d208c
authored: true
---

# certificadolegacywidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 124-137) · hereda de `FojaRubroDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget de selección múltiple para vincular Certificados existentes a una Foja de
Medición cargada como "legacy" (`FojaDeMedicion.foja_legacy=True`) — el mecanismo para
asociar certificados históricos, cargados antes de que las Fojas existieran en el
sistema, a la Foja que se está reconstruyendo retroactivamente. Candidatos: Certificados
de la misma Obra (`FojaRubroDependentWidgetMixin`) que todavía no tienen ninguna Foja
asociada (`certificado_foja__isnull=True`) — así no se puede vincular dos veces el mismo
Certificado.

## Firma

```python
class certificadolegacywidget(FojaRubroDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`FojaDeMedicionForm` (campo `foja_legacy_certificados`), consumido en `CrearFojaDeMedicion._vincular_certificados_legacy`.

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [Certificado](../../models/Certificado.md)
- [CrearFojaDeMedicion](CrearFojaDeMedicion.md)
