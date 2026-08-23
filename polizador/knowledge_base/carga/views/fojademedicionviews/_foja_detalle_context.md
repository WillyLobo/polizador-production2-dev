---
symbol: _foja_detalle_context
kind: function
module: carga/views/fojademedicionviews.py
lines: 13-46
signature_hash: sha1:5ca256f130bdba60e182063173f85b480023ce78
authored: true
---

# _foja_detalle_context

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 13-46)

## Propósito

Contexto de la ficha/impresión de una Foja: items con su % anterior/mes/acumulado, el responsable institucional (Gerente Operativo, resuelto por nombre fijo igual que en `_certificado_detalle_context`), totales de la fila, y las fotos adjuntas paginadas de a 3 por página (para el layout de impresión).

## Firma

```python
def _foja_detalle_context(foja):
```

## Uso real

`DetalleFojaDeMedicion.get_context_data` / `ImprimirFojaDeMedicion.get_context_data` (mismo módulo).

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [DetalleFojaDeMedicion](DetalleFojaDeMedicion.md)
