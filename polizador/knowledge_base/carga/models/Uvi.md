---
symbol: Uvi
kind: class
module: carga/models.py
lines: 1668-1689
signature_hash: sha1:4ca5bbac94ab0f0c5f66e3c78ebf3f4367cc3238
authored: true
---
# Uvi

**Módulo:** `carga/models.py` (líneas 1668-1689) · hereda de `models.Model`

## Propósito

Cotización diaria de la UVI (Unidad de Vivienda), la unidad de indexación en la que se
expresan buena parte de los montos de este módulo (Obra, Certificado, ContratoMonto,
PlanDeTrabajosRubro...). `pesos_equivalentes(monto_uvi, fecha)` es el método realmente
usado en todo el código: convierte un monto UVI a pesos con la cotización vigente a esa
fecha, o la anterior más cercana si no hay una cotización exacta para ese día
(`filter(uvi_fecha__lte=fecha).order_by('-uvi_fecha').first()`) — nunca la cotización
*futura* más cercana, siempre hacia atrás en el tiempo.

## Firma

```python
class Uvi(models.Model):
```

## Uso real

```python
# carga/models.py:499 (Obra.obra_contrato_nacion_pesos_actualizado)
return Uvi.pesos_equivalentes(self.obra_contrato_nacion_uvi, datetime.today())
```

Los valores se sincronizan desde la API pública del BCRA vía el management command
`bcra_uvi` (ver `carga/bcra_api.py`, CLAUDE.md).

## Ver también

- [Obra](Obra.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)