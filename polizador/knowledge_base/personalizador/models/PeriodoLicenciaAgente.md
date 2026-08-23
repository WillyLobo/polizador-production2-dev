---
symbol: PeriodoLicenciaAgente
kind: class
module: personalizador/models.py
lines: 548-574
signature_hash: sha1:451166359266a828090e4590f3bc7a0382cfdbee
authored: true
---

# PeriodoLicenciaAgente

**Módulo:** `personalizador/models.py` (líneas 548-574) · hereda de `models.Model`

## Propósito

Cupo (`periodolicenciaagente_dias_correspondientes`) congelado para un agente en un
[PeriodoLicencia](PeriodoLicencia.md) `LOR_ANUAL` dado, calculado una única vez por
`personalizador.licencias.get_or_create_periodo_agente` — la primera vez que se necesita
(al guardar la primera `LicenciaPermiso` de Art. 7/Art. 10 contra ese período). De ahí en
más, `balance_tipo` siempre lee este valor guardado en vez de recalcular
`dias_licencia_ordinaria_correspondientes(agente, año)` en vivo.

Existe para que una corrección posterior de `Agente.fecha_ingreso` (ej. un error de
carga, un reconocimiento de antigüedad) no altere retroactivamente el balance de un
período ya otorgado y parcial o totalmente usado — el tramo de antigüedad vigente al
momento de otorgarse queda fijado, tal como haya quedado reflejado en el decreto/
instrumento legal de ese año. No se usa para `LOR_INVIERNO`: esa licencia no tiene cupo
por antigüedad.

## Firma

```python
class PeriodoLicenciaAgente(models.Model):
```

## Uso real

```python
# personalizador/licencias.py — get_or_create_periodo_agente
PeriodoLicenciaAgente.objects.get_or_create(
    periodolicenciaagente_agente=agente, periodolicenciaagente_periodo=periodo,
    defaults={"periodolicenciaagente_dias_correspondientes": dias_licencia_ordinaria_correspondientes(agente, periodo.periodolicencia_anio)},
)
```
Llamado desde `LicenciaPermiso.clean()` para todo período `LOR_ANUAL` que se resuelve, y
desde `backfill_periodolicencia` (management command) al backfillear históricos.

## Ver también

- [PeriodoLicencia](PeriodoLicencia.md)
- [LicenciaPermiso](LicenciaPermiso.md)
