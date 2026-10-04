---
symbol: FojaDeMedicionForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 10-136
signature_hash: sha1:83d6f50eb1a54000e0c233ecdfa15035336fcc26
authored: true
---

# FojaDeMedicionForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 10-136) · hereda de `forms.ModelForm`

## Propósito

El form más elaborado de `carga` junto con `ObraForm`. Dos campos no-modelo:
`foja_numero_manual` (solo usado si `foja_legacy`, ver `clean()`) y
`foja_legacy_certificados` (para vincular Certificados históricos, ver
[certificadolegacywidget](../../views/ajaxviews/certificadolegacywidget.md)).

`__init__` hace bastante trabajo dinámico: acota `foja_rubro` a rubros de Planes vigentes;
si ya hay un rubro elegido (en `self.data` o `self.initial`), calcula los inspectores
candidatos (Agentes que inspeccionan la Obra dueña del rubro) y precarga
`foja_inspector` con todos ellos por defecto en una Foja nueva. Además agrega hasta dos
campos de fecha obligatorios: `obra_fecha_inicio` ("Fecha de Inicio de Obra") si la
**Obra** todavía no tiene Acta de Inicio, y `trabajos_fecha_inicio` ("Fecha de Reinicio de
Obra") si el Rubro viene de una reprogramación (`rubro_anterior`) y su Plan todavía no tiene
esa fecha. La vista (`CrearFojaDeMedicion._save_fecha_inicio`) guarda cada una en su
modelo.

En una Foja nueva que **no** es legacy, `clean()` rechaza un `foja_rubro` sin Etapas
Proyectadas en su Plan: primero se cargan las etapas y después se miden Fojas.

El resto de `clean()` aplica sólo si `foja_legacy=True`: valida que el número manual sea menor al
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

- [PlanDeTrabajosEtapa](../../models/PlanDeTrabajosEtapa.md) — debe existir al menos una para el Rubro.
