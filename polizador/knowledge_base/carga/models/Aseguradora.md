---
symbol: Aseguradora
kind: class
module: carga/models.py
lines: 119-133
signature_hash: sha1:12a514aeaf1df7aa0e63b87e0241cc582c4b212c
authored: true
---

# Aseguradora

**Módulo:** `carga/models.py` (líneas 119-133) · hereda de `models.Model`

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
