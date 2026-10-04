---
symbol: Aseguradora
kind: class
module: carga/models.py
lines: 127-141
signature_hash: sha1:be32e9016faea207c978baaa2c456556eb466a69
authored: true
---

# Aseguradora

**Módulo:** `carga/models.py` (líneas 127-141) · hereda de `models.Model`

## Propósito

Catálogo de compañías aseguradoras que emiten Pólizas de garantía sobre una Obra.

## Firma

```python
class Aseguradora(models.Model):
```

## Uso real

Alta/edición vía `AseguradoraForm` (`carga/forms/aseguradoraforms.py`). Referenciada desde `Poliza.poliza_aseguradora`.

## Ver también

- [Poliza](Poliza.md)
