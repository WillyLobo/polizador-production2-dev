---
symbol: generate_name_poliza_documento
kind: function
module: carga/models.py
lines: 49-54
signature_hash: sha1:a8557fa021895c7e0d89feaf86f9821d8b4a92f2
authored: false
---

# generate_name_poliza_documento

**Módulo:** `carga/models.py` (líneas 49-54)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def generate_name_poliza_documento(instance, filename):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:291` — `polizadocumento_archivo = models.FileField(verbose_name="Archivo", upload_to=generate_name_poliza_documento, validators=[FileValidator(max_size=14*1024*1024, min_size=None, content_types=("application/pdf",))], max_length=500)`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
