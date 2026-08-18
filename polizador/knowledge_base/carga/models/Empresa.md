---
symbol: Empresa
kind: class
module: carga/models.py
lines: 135-158
signature_hash: sha1:97d01cd97275361e5e1e672791e2e420a5af578d
authored: false
---

# Empresa

**Módulo:** `carga/models.py` (líneas 135-158)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Empresa(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:181` — `poliza_tomador = models.ForeignKey("Empresa", verbose_name="Tomador", on_delete=models.CASCADE)`
- `carga/models.py:340` — `obra_empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, verbose_name="Empresa")`
- `carga/views/documentosdigitalesviews.py:121` — `# 		{"name": "certificado_empresa", "title":"Empresa", "foreign_field":"certificado_obra__obra_empresa__empresa_nombre","width":85},`
- `carga/views/empresaviews.py:7` — `from carga.models import Empresa`
- `carga/views/empresaviews.py:15` — `model = Empresa`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
