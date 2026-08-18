---
symbol: build_foja_item_formset_class
kind: function
module: carga/forms/fojademedicionforms.py
lines: 218-228
signature_hash: sha1:8094647571c1d79e57b9b8d82a012dde5c8b4752
authored: true
---

# build_foja_item_formset_class

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 218-228)

## Propósito

Fábrica de `FojaDeMedicionItemFormset` con un número de filas extra (`extra=`) igual a la cantidad de items del Rubro elegido — necesario porque `CrearFojaDeMedicion` no sabe de antemano cuántos items va a tener la Foja hasta que el usuario elige el Rubro (a diferencia del formset fijo `extra=0` que usa `UpdateFojaDeMedicion`, donde los items ya existen).

## Firma

```python
def build_foja_item_formset_class(extra):
```

## Uso real

`CrearFojaDeMedicion.get/post` (`carga/views/fojademedicionviews.py`).

## Ver también

- [FojaDeMedicionItemForm](FojaDeMedicionItemForm.md)
- [CrearFojaDeMedicion](../../views/fojademedicionviews/CrearFojaDeMedicion.md)
