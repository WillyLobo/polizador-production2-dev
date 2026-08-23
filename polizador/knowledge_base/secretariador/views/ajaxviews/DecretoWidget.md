---
symbol: DecretoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 71-74
signature_hash: sha1:0088c5f3349eb55b16bafa51a7ab786bccf512e3
authored: true
---

# DecretoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 71-74) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir un `MontoViaticoDiario`, buscando por la representación textual del decreto reglamentario vinculado.

## Firma

```python
class DecretoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Solicitud.solicitud_decreto_viaticos` en `SolicitudForm`/`SolicitudExteriorForm`.

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)
