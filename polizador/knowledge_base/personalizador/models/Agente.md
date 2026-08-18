---
symbol: Agente
kind: class
module: personalizador/models.py
lines: 36-178
signature_hash: sha1:ff65a904827e4e0bc110472d0c3f184481377ff3
authored: true
---

# Agente

**Módulo:** `personalizador/models.py` (líneas 36-178) · hereda de `models.Model`

## Propósito

El modelo central de `personalizador`: un empleado del organismo, con sus datos
personales, de dependencia (categoría, cargo, oficina), antigüedad reconocida por
distintos instrumentos, y varios flags booleanos de clasificación. Con ~55 campos y dos
`GeneratedField` (nombre completo en dos formatos, para ordenar/mostrar según el
contexto), es el modelo más grande del módulo.

Dos piezas no obvias:

- **`agente_escalafon`** decide el viático diario que cobra el agente en el circuito de
  comisión de servicio de `secretariador` — salvo que sea una autoridad del Directorio,
  en cuyo caso `secretariador` usa el escalafón configurado en Reglas de Cálculo de
  Viáticos en su lugar, independientemente de este campo (ver el help_text del campo).
- **`antiguedad`** (property) no es solo `hoy - fecha_ingreso`: le suma los
  años/meses/días reconocidos por `aportes_ley_resolucion_*` y `aportes_anses_*`
  (antigüedad de otros organismos, reconocida por instrumento legal), con la convención
  de cómputo 30 días = 1 mes, 12 meses = 1 año aplicada al total combinado, no a cada
  fuente por separado.

`save()` solo hace una cosa no estándar: si no se cargó `abreviatura`, la infiere de
`sexo` vía [abreviatura_default_por_sexo](abreviatura_default_por_sexo.md).

## Firma

```python
class Agente(models.Model):
```

## Uso real

`CrearAgente`/`UpdateAgente` (`personalizador/views/agenteviews.py`).

## Ver también

- [CustomUser](CustomUser.md)
- [ComisionadoExterno](ComisionadoExterno.md) — mismo patrón para personas ajenas al organismo.
- [abreviatura_default_por_sexo](abreviatura_default_por_sexo.md)
