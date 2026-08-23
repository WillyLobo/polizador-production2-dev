---
symbol: LicenciaPermiso
kind: class
module: personalizador/models.py
lines: 629-744
signature_hash: sha1:c0693467e5c7ddc4d66737c0156cb55a5e90c39b
authored: true
---

# LicenciaPermiso

**Módulo:** `personalizador/models.py` (líneas 629-744) · hereda de `models.Model`

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
4. Para los 3 tipos "año-vencido" (Anual, Anual Proporcional, Anual de Invierno): importa
   `personalizador.licencias.resolver_periodo_para_licencia`/`get_or_create_periodo_agente`
   (import diferido, adentro del método, para evitar un ciclo ya que `licencias.py`
   importa este módulo), resuelve el [PeriodoLicencia](PeriodoLicencia.md) que corresponde
   a `licenciapermiso_tipo`/`licenciapermiso_fecha_desde` y lo guarda en
   `licenciapermiso_periodo` — si el período todavía no existe, `ValidationError` (no se
   autocrea). Si el período es `LOR_ANUAL`, además congela el cupo del agente
   ([PeriodoLicenciaAgente](PeriodoLicenciaAgente.md)) si es la primera vez.
5. **Solo para "Anual Proporcional" (adelanto, Art. 10)**: valida que la cantidad no
   supere el cupo disponible (`personalizador.licencias.balance_tipo`) del período de su
   propio `fecha_desde.year` (no del año siguiente: año vencido, el período abre el 15/12
   de ese mismo año, así que adelantarlo antes de esa fecha es lo que hace el Art. 10); y
   bloquea el adelanto si el agente tiene un saldo de `CorteLicencia` pendiente sin
   resolver de un período `LOR_ANUAL` anterior (evita acumular "deuda" de días sin gozar
   mientras ya se está tomando un adelanto de goce más próximo).

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

`personalizador.management.commands.importar_control_licencias` y
`backfill_periodolicencia` también pasan por acá (el primero vía `full_clean()`; el
segundo NO, para no rechazar datos históricos contra la regla nueva del punto 5 — solo
completa `licenciapermiso_periodo` directamente).

## Ver también

- [TipoLicenciaPermiso](TipoLicenciaPermiso.md)
- [CorteLicencia](CorteLicencia.md)
- [PeriodoLicencia](PeriodoLicencia.md)
- [Agente](Agente.md)
