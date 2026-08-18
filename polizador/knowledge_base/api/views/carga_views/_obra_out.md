---
symbol: _obra_out
kind: function
module: api/views/carga_views.py
lines: 725-759
signature_hash: sha1:8d447afa68c4d905d70345f4201b929b05fd4990
authored: true
---

# _obra_out

**Módulo:** `api/views/carga_views.py` (líneas 725-759)

## Propósito

Serializa una Obra a dict a mano (no delega en el schema ninja automático) porque incluye los M2M como listas de IDs (`departamento_ids`/`municipio_ids`/`localidad_ids`/`inspector_ids`, vía `.values_list('id', flat=True)`) — el shape que `retrieve_obra`/`create_obra`/`update_obra` devuelven, distinto del que armaría la serialización automática de un `ForeignKey`/`ManyToManyField` sin tratamiento especial.

## Firma

```python
def _obra_out(o: Obra) -> dict:
```

## Uso real

`retrieve_obra`, `create_obra`, `update_obra` (mismo módulo, todas debajo).

## Ver también

- [Obra](../../../carga/models/Obra.md)
