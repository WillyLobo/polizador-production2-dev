---
symbol: FojaDeMedicionForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 10-124
signature_hash: sha1:3ca6be06f9810023a9cbfa707a2a68791a7e06fb
authored: true
---

# FojaDeMedicionForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 10-124) · hereda de `forms.ModelForm`

## Propósito

El form más elaborado de `carga` junto con `ObraForm`. Dos campos no-modelo:
`foja_numero_manual` (solo usado si `foja_legacy`, ver `clean()`) y
`foja_legacy_certificados` (para vincular Certificados históricos, ver
[certificadolegacywidget](../../views/ajaxviews/certificadolegacywidget.md)).

`__init__` hace bastante trabajo dinámico: acota `foja_rubro` a rubros de Planes vigentes;
si ya hay un rubro elegido (en `self.data` o `self.initial`), calcula los inspectores
candidatos (Agentes que inspeccionan la Obra dueña del rubro) y precarga
`foja_inspector` con todos ellos por defecto en una Foja nueva; y si el Rubro elegido
todavía no tiene `trabajos_fecha_inicio` en su Plan, agrega dinámicamente un campo
`trabajos_fecha_inicio` (con label distinto según sea la primera vez o un "reinicio" tras
reprogramación) — campo que la vista (`CrearFojaDeMedicion._save_fecha_inicio`) después
usa para setear esa fecha en el Plan.

`clean()` solo aplica si `foja_legacy=True`: valida que el número manual sea menor al
`rubro_foja_numero_inicial` configurado (si no, hay que configurar ese campo primero en
el Rubro) y que no choque con una Foja ya cargada para ese número — y si todo está bien,
setea `self.instance.foja_numero` directamente (saltándose la auto-numeración de la
señal, que ya de por sí no toca las fojas legacy).

## Firma

```python
class FojaDeMedicionForm(forms.ModelForm):
```

## Uso real

`CrearFojaDeMedicion`/`UpdateFojaDeMedicion` (`carga/views/fojademedicionviews.py`).

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [auto_increment_foja_numero](../../signals/auto_increment_foja_numero.md)
- [certificadolegacywidget](../../views/ajaxviews/certificadolegacywidget.md)
