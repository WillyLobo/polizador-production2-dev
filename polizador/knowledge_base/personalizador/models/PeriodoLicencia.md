---
symbol: PeriodoLicencia
kind: class
module: personalizador/models.py
lines: 483-545
signature_hash: sha1:6dac056ca667c4d2fd47f92f2f1bda800c3301c8
authored: true
---

# PeriodoLicencia

**Módulo:** `personalizador/models.py` (líneas 483-545) · hereda de `models.Model`

## Propósito

Ancla explícita de año calendario para los 3 tipos "año-vencido" de Licencia Anual (Art.
7, Art. 10 y Anual de Invierno, Ley 645-A). Reemplaza la inferencia implícita de año que
antes vivía en `personalizador/licencias.py` (vía `fecha_desde.year` +/- corrimientos
hardcodeados) — ver [LicenciaPermiso](LicenciaPermiso.md), que ahora resuelve y guarda el
período en `licenciapermiso_periodo` desde `clean()`.

`periodolicencia_categoria` distingue dos pozos independientes:

- `LOR_ANUAL`: compartido por Art. 7 (Anual) y Art. 10 (Anual Proporcional) — Art. 10 no
  tiene cupo propio, adelanta días del mismo pozo de Art. 7 de su propio
  `fecha_desde.year` (año vencido: el período `<año>` recién abre el 15/12 de ese año,
  así que tomarlo antes de esa fecha es "adelantarlo", no consumir el año siguiente).
  Usa `periodolicencia_apertura`/`periodolicencia_fecha_limite_solicitud` (este último
  solo dato de referencia, sin enforcement).
- `LOR_INVIERNO`: pozo propio, sin cupo por antigüedad. Usa los 4 campos de turno
  (`periodolicencia_turno1_desde/hasta`, `periodolicencia_turno2_desde/hasta`) en vez de
  apertura/límite — la Licencia de Invierno se fija por decreto en 2 turnos de fechas
  fijas cada año, sin fórmula (se cargan a mano).

`clean()` exige los 2 campos de `LOR_ANUAL` o los 4 de `LOR_INVIERNO` según corresponda
(nunca se autocompletan con un default calculado del lado del modelo: son datos legales
reales — fecha de un decreto — que el sistema no debe inventar en silencio; la precarga
15/12/&lt;año&gt;-31/03/&lt;año+1&gt; para `LOR_ANUAL` vive del lado del form, en JS, ver
[PeriodoLicenciaForm](../forms/periodolicenciaforms/PeriodoLicenciaForm.md)), y que el
Turno 2 empiece después de que termine el Turno 1.

## Firma

```python
class PeriodoLicencia(models.Model):
```

## Uso real

`personalizador.licencias.resolver_periodo_para_licencia`/`get_periodo` (resuelven cuál
`PeriodoLicencia` corresponde a una `LicenciaPermiso`, sin autocrear); `personalizador.
management.commands.backfill_periodolicencia` (backfill de registros históricos) e
`importar_control_licencias` (sí autocrea los de `LOR_ANUAL` con la fórmula legal, porque
ya conoce año/categoría por config de hoja).

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
- [PeriodoLicenciaAgente](PeriodoLicenciaAgente.md)
- [CrearPeriodoLicencia](../views/periodolicenciaviews/CrearPeriodoLicencia.md)
