---
symbol: FojaDeMedicionItem
kind: class
module: carga/models.py
lines: 1224-1257
signature_hash: sha1:11a6c0cf2467622b2d382ce4413e15c7fc8f6b48
authored: true
---
# FojaDeMedicionItem

**Módulo:** `carga/models.py` (líneas 1224-1257) · hereda de `models.Model`

## Propósito

El avance real del mes (`fojaitem_pct_avance_mes`, cargado a mano) de un
`PlanDeTrabajosItem` puntual, dentro de una Foja. `fojaitem_pct_acumulado` es el campo
clave del sistema de certificación: se calcula en `save()` como
`anterior.fojaitem_pct_acumulado + self.fojaitem_pct_avance_mes` (o solo
`fojaitem_pct_avance_mes` si no hay Foja anterior) — es una **copia calculada al momento
de guardar**, no un valor derivado que se recalcula solo en cada lectura. Esa decisión de
diseño es exactamente lo que hace necesaria la señal
[recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md)
(ver esa página para el detalle completo de la cascada hacia adelante que dispara este
`save()`).

El `UniqueConstraint` sobre (`fojaitem_foja`, `fojaitem_planitem`) impide cargar el mismo
item dos veces en la misma Foja.

## Firma

```python
class FojaDeMedicionItem(models.Model):
```

## Uso real

Ver [recalcular_acumulado_fojas_siguientes § Uso real](../signals/recalcular_acumulado_fojas_siguientes.md#uso-real) — se guarda siempre vía el formset inline de `UpdateFojaDeMedicion`/`CrearFojaDeMedicion`, nunca suelto.

## Ver también

- [FojaDeMedicion](FojaDeMedicion.md)
- [recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md) — explica la cascada que dispara este `save()`.
- [PlanDeTrabajosEtapaItem](PlanDeTrabajosEtapaItem.md) — mismo patrón de cálculo, sin cascada (lado proyectado).