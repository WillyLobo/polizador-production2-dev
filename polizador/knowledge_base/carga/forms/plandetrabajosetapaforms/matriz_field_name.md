---
symbol: matriz_field_name
kind: function
module: carga/forms/plandetrabajosetapaforms.py
lines: 5-6
signature_hash: sha1:7e9658a01c2bf77939071f1ad4e282761f3f20fd
authored: true
---

# matriz_field_name

**Módulo:** `carga/forms/plandetrabajosetapaforms.py` (líneas 5-6)

## Propósito

Helper trivial: `f"item_{item_pk}_col_{col_index}"` — el nombre de campo dinámico que identifica una celda (item × columna/etapa) de la grilla de `build_matriz_form`. Factorizado aparte porque tanto el form dinámico como la vista (`PlanDeTrabajosEtapaMatriz`) necesitan generar/leer el mismo nombre de campo.

## Firma

```python
def matriz_field_name(item_pk, col_index):
```

## Uso real

`build_matriz_form` (mismo módulo) y `PlanDeTrabajosEtapaMatriz.get/post` (`carga/views/plandetrabajosetapaviews.py`).

## Ver también

- [build_matriz_form](build_matriz_form.md)
- [PlanDeTrabajosEtapaMatriz](../../views/plandetrabajosetapaviews/PlanDeTrabajosEtapaMatriz.md)
