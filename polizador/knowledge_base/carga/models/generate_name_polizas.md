---
symbol: generate_name_polizas
kind: function
module: carga/models.py
lines: 40-48
signature_hash: sha1:b88b039d53949fa6e396c21db5379b3ae1431b70
authored: true
---

# generate_name_polizas

**Módulo:** `carga/models.py` (líneas 40-48)

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
