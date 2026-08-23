---
symbol: generate_name_contratos
kind: function
module: carga/models.py
lines: 49-54
signature_hash: sha1:cd53b1b801e86883e6590322dcc3d39a7489ed76
authored: true
---

# generate_name_contratos

**Módulo:** `carga/models.py` (líneas 49-54)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

El más simple de los `upload_to` de este módulo: sin partición por fecha, todo va a
`contratos_obra/<contratodigital_uuid>.pdf` — a diferencia de Certificados/Pólizas, los
documentos digitales de un Contrato no tienen una fecha propia relevante para agrupar.

## Firma

```python
def generate_name_contratos(instance, filename):
```

## Uso real

`ContratosDigitales.contratodigital_archivo = models.FileField(upload_to=generate_name_contratos, ...)` (carga/models.py:1396).

## Ver también

- [ContratosDigitales](ContratosDigitales.md)
