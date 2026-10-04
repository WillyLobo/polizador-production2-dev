---
symbol: datatable_certificados
kind: function
module: api/views/carga_views.py
lines: 1359-1399
signature_hash: sha1:d854a402e270cfd651f4f52e020b9abcde870800
authored: true
---

# datatable_certificados

**Módulo:** `api/views/carga_views.py` (líneas 1359-1399)

## Propósito

Listado datatable de Certificados a mano (no `register_simple_datatable`, por el `select_related` anidado sobre `certificado_obra__obra_empresa`).

## Firma

```python
def datatable_certificados(request, draw: int=1, start: int=0, length: int=50, search: str='', order_by: str='-id', filters: str='{}'):
```

## Uso real

`GET /v1/api/datatables/certificados/` — consumido por `Lista-certificados.html`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
- [_certificado_datatable_row](_certificado_datatable_row.md)
