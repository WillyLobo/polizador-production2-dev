---
symbol: generate_name_rubro_documento
kind: function
module: carga/models.py
lines: 73-78
signature_hash: sha1:a77ce226d468a1990b378b487965abb67422cf6f
authored: true
---

# generate_name_rubro_documento

**Módulo:** `carga/models.py` (líneas 73-78)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

Sin partición por fecha: `documentos_rubro_plan/<rubro_uuid>.pdf`.

## Firma

```python
def generate_name_rubro_documento(instance, filename):
```

## Uso real

`PlanDeTrabajosRubro.rubro_documento_digital = models.FileField(upload_to=generate_name_rubro_documento, ...)` (carga/models.py:934).

## Ver también

- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)
