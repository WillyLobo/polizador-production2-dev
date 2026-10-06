---
symbol: generate_name_foja_foto
kind: function
module: carga/models.py
lines: 88-93
signature_hash: sha1:16b74eeba69c536a71b3e338bc4d6e021cb81fdf
authored: true
---

# generate_name_foja_foto

**Módulo:** `carga/models.py` (líneas 88-93)

## Propósito

Callback `upload_to` de un `FileField`: Django lo llama con la instancia (todavía sin
guardar del todo) y el nombre original del archivo, y espera de vuelta la ruta relativa
donde `GCloudAndLocalStorage` (ver CLAUDE.md) va a escribirlo, tanto en GCS como en
`MEDIA_ROOT` local.

Es el único de los siete que preserva la extensión original del archivo subido
(`os.path.splitext(filename)[1]`) en vez de forzar `.pdf` — porque estos son adjuntos de
imagen (`content_types=("image/jpeg", "image/png")`), no PDFs. Sin partición por fecha:
`fotos_foja_medicion/<fotofoja_uuid>.<ext>`.

## Firma

```python
def generate_name_foja_foto(instance, filename):
```

## Uso real

`FojaDeMedicionFoto.fotofoja_archivo = models.FileField(upload_to=generate_name_foja_foto, ...)` (carga/models.py:1276).

## Ver también

- [FojaDeMedicionFoto](FojaDeMedicionFoto.md)
