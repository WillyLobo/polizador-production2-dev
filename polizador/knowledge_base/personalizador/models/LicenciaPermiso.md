---
symbol: LicenciaPermiso
kind: class
module: personalizador/models.py
lines: 535-617
signature_hash: sha1:96a347e1bff42c97e02cf6e284ed494be5cf23c9
authored: true
---

# LicenciaPermiso

**Módulo:** `personalizador/models.py` (líneas 535-617) · hereda de `models.Model`

## Propósito

Registro administrativo de una licencia/permiso ya otorgado a un agente — sin flujo de
solicitud/aprobación propio (a diferencia del circuito de viáticos de `secretariador`):
se carga el hecho consumado, respaldado o no por un instrumento legal formal
(Resolución/Decreto/Memorandum, mutuamente excluyentes).

`clean()` hace varias validaciones cruzadas:

1. A lo sumo un instrumento legal vinculado (no dos a la vez).
2. `fecha_hasta` no puede ser anterior a `fecha_desde`.
3. Si consume el saldo de un `CorteLicencia` (`licenciapermiso_saldo_de_corte`): que el
   corte sea del mismo agente y tipo que la licencia original, que no haya vencido, y que
   la cantidad no supere el saldo restante del corte (recalculando el saldo "como si"
   esta edición no existiera todavía, para permitir reducir una cantidad ya cargada sin
   que se autobloquee contra sí misma).
4. **Solo para el tipo "Anual Proporcional" (adelanto, Art. 10)**: importa
   `personalizador.licencias.balance_tipo` (import diferido, adentro del método, para
   evitar un ciclo de import ya que `licencias.py` importa este módulo) y valida que la
   cantidad no supere el cupo disponible del año *siguiente* — un adelanto consume cupo
   futuro, no el del año en que se carga.

Es, junto con `Oficina`, el modelo con la lógica de negocio más densa de
`personalizador`.

## Firma

```python
class LicenciaPermiso(models.Model):
```

## Uso real

```python
# personalizador/views/licenciapermisoviews.py (CrearLicenciaPermiso.form_valid, vía FormsetViewMixin)
self.object = form.save()  # -> LicenciaPermiso.clean() corre dentro de full_clean()
```

## Ver también

- [TipoLicenciaPermiso](TipoLicenciaPermiso.md)
- [CorteLicencia](CorteLicencia.md)
- [Agente](Agente.md)
