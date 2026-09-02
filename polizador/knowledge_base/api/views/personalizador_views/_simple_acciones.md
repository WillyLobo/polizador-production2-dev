---
symbol: _simple_acciones
kind: function
module: api/views/personalizador_views.py
lines: 263-268
signature_hash: sha1:4a1345b9335c15b3f289dbc895f680695ccee71f
authored: true
---
# _simple_acciones

**Módulo:** `api/views/personalizador_views.py` (líneas 263-268)

## Propósito

Helper compartido por la mayoría de los `_X_datatable_row` de este módulo: arma la columna `acciones` (editar+eliminar, o solo editar, o vacío) según `delete_perm`/`change_perm` del usuario — el mismo `if/elif/else` de tres ramas que el resto de `carga_views.py` repite inline en cada función, factorizado acá una sola vez.

## Firma

```python
def _simple_acciones(user, delete_perm, change_perm, editarlink, eliminarlink):
```

## Uso real

`_generoagente_datatable_row`, `_tituloprofesional_datatable_row`, `_categoria_datatable_row`, y la mayoría de los demás `_X_datatable_row` de este módulo.

## Ver también

_(sin referencias cruzadas)_