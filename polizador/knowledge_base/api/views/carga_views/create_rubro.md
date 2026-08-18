---
symbol: create_rubro
kind: function
module: api/views/carga_views.py
lines: 1203-1204
signature_hash: sha1:8c3b00de006221f74f950841f33e04566989d08b
authored: true
---

# create_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1203-1204)

## Propósito

Alta de `CertificadoRubro` desde `CertificadoRubroCreate` (`payload.model_dump()` directo a `CertificadoRubro.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_rubro(request, payload: CertificadoRubroCreate):
```

## Uso real

`POST /v1/api/rubros/` — response=`CertificadoRubroOut`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
