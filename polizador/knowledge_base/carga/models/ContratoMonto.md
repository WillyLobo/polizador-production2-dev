---
symbol: ContratoMonto
kind: class
module: carga/models.py
lines: 1357-1372
signature_hash: sha1:d6aca3c952661c05835e3fad07e60e8820f8f533
authored: false
---

# ContratoMonto

**Módulo:** `carga/models.py` (líneas 1357-1372)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class ContratoMonto(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:474` — `la suma/fecha más reciente de los ContratoMonto de todos los Contratos de la obra,`
- `carga/models.py:476` — `montos = ContratoMonto.objects.filter(contratomonto_contrato__contrato_obra=self)`
- `carga/models.py:508` — `# Los _uvi_fecha quedan en None cuando no hay un ContratoMonto que los origine`
- `carga/models.py:935` — `rubro_contratomonto = models.ForeignKey("ContratoMonto", verbose_name="Monto de Contrato", on_delete=models.SET_NULL, null=True, blank=True, related_name="rubros_plan")`
- `carga/models.py:943` — `"(ContratoMonto) al generar certificados desde una Foja.",`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
