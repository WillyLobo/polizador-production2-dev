---
symbol: generate_name_polizas
kind: function
module: carga/models.py
lines: 39-47
signature_hash: sha1:7775197d31dcb71d83716ddbe206e934e27c0d06
authored: true
---

# generate_name_polizas

**Módulo:** `carga/models.py` (líneas 39-47)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

Mismo patrón que `generate_name_certificados` pero para Pólizas: `polizas/<año>/<mes>/`
según `poliza_fecha`, nombrado `<poliza_uuid>_<poliza_expediente>.pdf`.

## Firma

```python
def generate_name_polizas(instance, filename):
```

## Uso real

`Poliza.poliza_digital = models.FileField(upload_to=generate_name_polizas, ...)` (carga/models.py:185).

## Ver también

- [Poliza](Poliza.md)
