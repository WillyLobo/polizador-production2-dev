---
symbol: TipoLicenciaPermiso
kind: class
module: personalizador/models.py
lines: 483-533
signature_hash: sha1:1b3f942bb3bcd3ee8341b82629ff9e2e40556230
authored: true
---

# TipoLicenciaPermiso

**Módulo:** `personalizador/models.py` (líneas 483-533) · hereda de `models.Model`

## Propósito

Catálogo normalizado de tipos de licencia/permiso según la Ley 645-A (ordinaria,
extraordinaria, permiso), con toda la parametrización que define cómo se computa cada
tipo: unidad (días corridos/hábiles/horas), tope y período del tope, si es remunerada,
antigüedad mínima requerida, si requiere certificado, si genera compensación horaria a
devolver. Se carga vía management command (`cargar_tipos_licencia`, ver CLAUDE.md), no
hay flujo de alta pensado para uso frecuente desde la UI aunque el CRUD exista.

Es el catálogo que toda la lógica de cálculo de saldos en `personalizador/licencias.py`
consulta — en particular, dos nombres de tipo están hardcodeados como constantes ahí
(`LICENCIA_ANUAL_ORDINARIA_NOMBRE = "Anual"`, `LICENCIA_ANUAL_INVIERNO_NOMBRE = "Anual de
Invierno"`, `LICENCIA_ANUAL_ADELANTADA_NOMBRE = "Anual Proporcional"`): renombrar estos
tres registros del catálogo rompería silenciosamente el cálculo de balances, porque el
código los busca por `tipolicenciapermiso_nombre` exacto, no por un flag dedicado.

## Firma

```python
class TipoLicenciaPermiso(models.Model):
```

## Uso real

`CrearTipoLicenciaPermiso`/`UpdateTipoLicenciaPermiso` (`personalizador/views/tipolicenciapermisoviews.py`); consumido extensamente por `personalizador/licencias.py`.

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
