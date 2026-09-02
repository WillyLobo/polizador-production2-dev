---
symbol: ComisionadoSolicitud
kind: class
module: secretariador/models.py
lines: 470-613
signature_hash: sha1:6cdb7e6c492b1ab5c06ed43bfa4eb5bcd44da878
authored: true
---
# ComisionadoSolicitud

**Módulo:** `secretariador/models.py` (líneas 470-613) · hereda de `models.Model`

## Propósito

Un agente (o persona externa) comisionado dentro de una `Solicitud` — o, alternativamente,
dentro de una `Incorporacion` posterior a esa Solicitud (`comisionadosolicitud_foreign` y
`comisionadosolicitud_incorporacion_foreign` son ambos opcionales, ninguno de los dos
mutuamente excluyente vía constraint como sí lo son agente/externo — `get_origin()`
resuelve cuál de los dos aplica). El `CheckConstraint` `comisionadosolicitud_agente_xor_externo`
exige exactamente uno de `comisionadosolicitud_nombre` (Agente) /
`comisionadosolicitud_externo` (ComisionadoExterno) — nunca ambos, nunca ninguno.
`persona` (property) devuelve el que corresponda, aprovechando que ambos modelos exponen
los mismos nombres de atributo (ver el docstring de
[ComisionadoExterno](../../personalizador/models/ComisionadoExterno.md)).

**El cálculo de viático vive acá, no en `Solicitud`:**

- `valor_viatico_dia()`: retorna 0 si es colaborador o `sin_viatico`; si no, resuelve las
  excepciones de [ReglasViatico](ReglasViatico.md) (gabinete, autoridades del Directorio
  dentro del Chaco, comisionados externos) y después el escalafón aplicable (único forzado,
  el de autoridades si `agente.directorio_set.exists()`, el propio `agente_escalafon`, o el
  default de externos) para indexar el campo correcto de
  [MontoViaticoDiario](MontoViaticoDiario.md) (estrato × interior/exterior según la
  Provincia de la Solicitud de origen).
- `viaticos_computado()`: días de la Solicitud/Incorporación de origen × valor diario.
- `viaticos_total()`: computado + combustible + gastos + pasaje.

`save()` recalcula y persiste los tres (`_cantidad_de_dias`, `_viatico_diario`,
`_viatico_computado`, `_viatico_total`) en cada guardado — son snapshots calculados al
momento de guardar, no propiedades derivadas en cada lectura (mismo patrón que
`carga.FojaDeMedicionItem.fojaitem_pct_acumulado`, aunque acá no hay una señal de cascada
hacia adelante porque no hay "comisionados siguientes" en una cadena).

## Firma

```python
class ComisionadoSolicitud(models.Model):
```

## Uso real

```python
# secretariador/views/solicitudviews.py (CrearSolicitud, vía FormsetViewMixin)
formset.save()  # -> cada ComisionadoSolicitud.save() recalcula sus 4 campos de viático
```

## Ver también

- [Solicitud](Solicitud.md)
- [ReglasViatico](ReglasViatico.md)
- [MontoViaticoDiario](MontoViaticoDiario.md)
- [ComisionadoExterno](../../personalizador/models/ComisionadoExterno.md)