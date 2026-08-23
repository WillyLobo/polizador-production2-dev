---
symbol: build_matriz_form
kind: function
module: carga/forms/plandetrabajosetapaforms.py
lines: 9-63
signature_hash: sha1:cdb5505432e4c09d74f331864bd1b47835a6b5b3
authored: true
---

# build_matriz_form

**Módulo:** `carga/forms/plandetrabajosetapaforms.py` (líneas 9-63)

## Propósito

Fábrica de una clase `forms.Form` dinámica: un campo `DecimalField` por cada combinación
(`PlanDeTrabajosItem`, columna/etapa) — no un `ModelForm` ni un formset, porque la grilla
no mapea 1:1 a filas de una tabla sino a una matriz completa de valores que después la
vista (`PlanDeTrabajosEtapaMatriz.post`) traduce a instancias de
`PlanDeTrabajosEtapa`/`PlanDeTrabajosEtapaItem`.

`clean()` valida dos cosas a la vez: por fila (item), que la suma de todas sus columnas
más lo que ya llevaba acumulado (`anterior_map`) no supere su `planitem_incidencia_pct`;
y por columna (etapa), que la suma de todos los items de esa etapa no supere 100% —
mismas reglas que `BaseFojaDeMedicionItemFormset` aplica del lado real (Foja), pero acá
sobre valores *proyectados* y en una sola pasada de formulario en vez de un formset.

## Firma

```python
def build_matriz_form(items, total_columns, anterior_map):
```

## Uso real

`PlanDeTrabajosEtapaMatriz.get/post` (`carga/views/plandetrabajosetapaviews.py`) construyen la clase con `build_matriz_form(items, total_columns, anterior_map)` y la instancian.

## Ver también

- [matriz_field_name](matriz_field_name.md)
- [PlanDeTrabajosEtapaMatriz](../../views/plandetrabajosetapaviews/PlanDeTrabajosEtapaMatriz.md)
- [PlanDeTrabajosEtapaItem](../../models/PlanDeTrabajosEtapaItem.md)
