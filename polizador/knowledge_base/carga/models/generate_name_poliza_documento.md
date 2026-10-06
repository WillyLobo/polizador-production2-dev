---
symbol: generate_name_poliza_documento
kind: function
module: carga/models.py
lines: 50-55
signature_hash: sha1:e09a49a1df6a0d8f232e33c13535ff016f15ad96
authored: true
---

# generate_name_poliza_documento

**Módulo:** `carga/models.py` (líneas 50-55)

## Propósito

`upload_to` de `PolizaDocumento.polizadocumento_archivo`. Guarda cada archivo como
`documentos_poliza/<polizadocumento_uuid>.pdf` e ignora el nombre original: así no hay
colisiones ni nombres con caracteres raros en GCS/`MEDIA_ROOT`. Es el mismo patrón que los
demás `generate_name_*` del módulo. La extensión es siempre `pdf`, cosa que el
`FileValidator` del campo ya garantiza.

## Firma

```python
def generate_name_poliza_documento(instance, filename):
```

## Uso real

```python
# carga/models.py (PolizaDocumento)
polizadocumento_archivo = models.FileField(verbose_name="Archivo", upload_to=generate_name_poliza_documento, ...)
```

## Ver también

- [PolizaDocumento](PolizaDocumento.md)
