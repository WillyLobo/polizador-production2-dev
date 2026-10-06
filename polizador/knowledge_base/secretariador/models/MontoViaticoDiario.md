---
symbol: MontoViaticoDiario
kind: class
module: secretariador/models.py
lines: 293-313
signature_hash: sha1:a49391c2378016a5efb44fdcd9cde538be6bc426
authored: true
---
# MontoViaticoDiario

**Módulo:** `secretariador/models.py` (líneas 293-313) · hereda de `models.Model`

## Propósito

Los ocho montos de viático diario (4 estratos × dentro/fuera de la Provincia) que un `InstrumentosLegalesDecretos` reglamenta — la tabla de tarifas que `ComisionadoSolicitud.valor_viatico_dia()` consulta para calcular cuánto cobra cada comisionado.

## Firma

```python
class MontoViaticoDiario(models.Model):
```

## Uso real

`ComisionadoSolicitud.valor_viatico_dia()` (mismo módulo, más abajo) resuelve el campo `montoviaticodiario_estrato_<N>_{interior,exterior}` correspondiente según el escalafón y si el destino es dentro o fuera del Chaco.

## Ver también

- [ComisionadoSolicitud](ComisionadoSolicitud.md)
- [InstrumentosLegalesDecretos](InstrumentosLegalesDecretos.md)