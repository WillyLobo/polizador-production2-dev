---
symbol: FojaDeMedicion
kind: class
module: carga/models.py
lines: 1413-1490
signature_hash: sha1:31c6f532c5ee8f9b1b038808067318980253abe8
authored: true
---
# FojaDeMedicion

**Módulo:** `carga/models.py` (líneas 1413-1490) · hereda de `models.Model`

## Propósito

Registro mensual de avance real de obra para un Rubro de Plan de Trabajos — el "gemelo
real" de `PlanDeTrabajosEtapa` (ver esa página para la comparación estructural completa).
`foja_numero` es correlativo dentro de la cadena de rubro reprogramado, asignado por
[auto_increment_foja_numero](../signals/auto_increment_foja_numero.md); `foja_legacy`
marca las Fojas cargadas a mano para preservar historial previo al sistema (esas se
saltean de la auto-numeración).

`foja_anterior()`/`foja_siguiente()` navegan la cadena (`rubro_cadena_ids()`/
`rubro_cadena_siguiente_ids()`) por `foja_numero`, no por `foja_periodo` — el período es
solo una etiqueta visual, el orden real es el número de foja. `anterior_items_map()` es un
`staticmethod` usado para prellenar formularios: da, para cada item de un rubro, el
acumulado que tenía en la última Foja ya cargada, sin necesidad de instanciar una Foja
completa.

## Firma

```python
class FojaDeMedicion(models.Model):
```

## Uso real

```python
# carga/views/fojademedicionviews.py (CrearFojaDeMedicion.form_valid)
self.object = form.save()  # -> pre_save: auto_increment_foja_numero
formset.save()               # -> cada FojaDeMedicionItem.save() + cascada hacia adelante
```

## Ver también

- [FojaDeMedicionItem](FojaDeMedicionItem.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md) — dueño de la cadena de reprogramación que estos métodos recorren.
- [PlanDeTrabajosEtapa](PlanDeTrabajosEtapa.md) — su equivalente proyectado.
- [auto_increment_foja_numero](../signals/auto_increment_foja_numero.md)