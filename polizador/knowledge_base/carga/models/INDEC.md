---
symbol: INDEC
kind: class
module: carga/models.py
lines: 1412-1446
signature_hash: sha1:5ebaa718231f4e8d835e388144cac7be4d18b949
authored: true
---
# INDEC

**Módulo:** `carga/models.py` (líneas 1412-1446) · hereda de `models.Model`

## Propósito

Tabla de referencia con los componentes del índice de costos de la construcción de INDEC
(mano de obra, materiales por rubro, gastos generales, costo financiero, transporte...)
por mes.

**Sin consumidores en el código actual:** a diferencia de `Uvi` (usado en cálculos por
todo el módulo), ningún archivo de `carga` (fuera de `models.py`, `admin.py` y
`resources.py`) referencia `INDEC` — no hay ninguna fórmula que lo use para actualizar
montos. Está registrado en el admin con soporte de import/export
(`resources.INDECResource`), así que probablemente sea una tabla de referencia mantenida
para consulta/exportación manual, no un insumo de cálculo automático como `Uvi`. Si estás
por escribir lógica que dependa de estos valores, confirmá primero que no exista ya en
otro lado (ej. `carga/ley27397.py`), porque el modelo en sí no la tiene.

## Firma

```python
class INDEC(models.Model):
```

## Uso real

Alta/edición: `/admin/carga/indec/` (Django admin) o import/export vía `resources.INDECResource`.

## Ver también

- [Uvi](Uvi.md) — el índice que sí tiene consumidores activos.