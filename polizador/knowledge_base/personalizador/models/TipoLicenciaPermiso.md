---
symbol: TipoLicenciaPermiso
kind: class
module: personalizador/models.py
lines: 577-627
signature_hash: sha1:454b3250c3421c9d8c0426adc3622463cf7dd3ad
authored: true
---

# TipoLicenciaPermiso

**Módulo:** `personalizador/models.py` (líneas 577-627) · hereda de `models.Model`

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

El comando `cargar_tipos_licencia` (que hace `update_or_create` por `(categoria, nombre)`)
mitiga el riesgo simétrico — que alguien renombre un tipo a mano en el admin sin
actualizar `TIPOS_DATA` — con un chequeo previo (`--dry-run` para solo reportar) que
compara por `articulo` (más estable que `nombre`) y avisa de posibles renombres/duplicados
antes de escribir; encontró y permitió reconciliar un duplicado real (`pk=13` "Permiso por
Exámenes" vs `pk=42` "Exámenes", mismo Art. 36/37) que había quedado de una corrida
anterior sin este chequeo.

## Firma

```python
class TipoLicenciaPermiso(models.Model):
```

## Uso real

`CrearTipoLicenciaPermiso`/`UpdateTipoLicenciaPermiso` (`personalizador/views/tipolicenciapermisoviews.py`); consumido extensamente por `personalizador/licencias.py`.

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
