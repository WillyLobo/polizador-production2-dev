---
symbol: Empresa
kind: class
module: carga/models.py
lines: 143-166
signature_hash: sha1:926ae9fc9b8b3a6933f468fc0fa3094c0275a17a
authored: true
---

# Empresa

**Módulo:** `carga/models.py` (líneas 143-166) · hereda de `models.Model`

## Propósito

Empresa constructora contratista. Es tanto la adjudicataria de una Obra
(`Obra.obra_empresa`) como, potencialmente, la tomadora de una Póliza de garantía
(`Poliza.poliza_tomador`) — son dos roles distintos que el modelo no distingue por campo,
solo por cuál FK la referencia.

## Firma

```python
class Empresa(models.Model):
```

## Uso real

`ObraForm`/`EmpresaForm` (`carga/forms/obraforms.py`, `carga/forms/empresaforms.py`), `ModelForm`s estándar.

## Ver también

- [Obra](Obra.md)
- [Poliza](Poliza.md)
