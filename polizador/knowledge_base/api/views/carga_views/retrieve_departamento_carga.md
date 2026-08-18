---
symbol: retrieve_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 469-470
signature_hash: sha1:02400196ad59520015f5b7e2b6a517a9329e175d
authored: true
---

# retrieve_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 469-470)

## Propósito

Devuelve un `Departamento` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_departamento_carga(request, id: int):
```

## Uso real

`GET /v1/api/departamentos-carga/{{id}}/` — response=`DepartamentoOut`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
