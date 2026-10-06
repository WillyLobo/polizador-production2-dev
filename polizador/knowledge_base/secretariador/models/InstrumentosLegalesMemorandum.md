---
symbol: InstrumentosLegalesMemorandum
kind: class
module: secretariador/models.py
lines: 95-136
signature_hash: sha1:f1c58e0a7f0a3c4765c8f442d87abb364fa62254
authored: true
---

# InstrumentosLegalesMemorandum

**Módulo:** `secretariador/models.py` (líneas 95-136) · hereda de `models.Model`

## Propósito

Un memorandum institucional (Presidencia o Dirección General de Gestión Administrativa),
identificado por tipo+número+año (`UniqueConstraint`). `instrumentolegalmemorandum_str`
es un `GeneratedField` ("numero - ano - tipo") usado como texto de búsqueda en los
widgets select2 que lo referencian desde otras apps. Los campos `_autocarga`/`_document`
son para la extracción automática de texto vía OCR sobre el PDF escaneado (ver
`secretariador/management/commands/OCR*.py`, CLAUDE.md) — fuera del alcance de este
manifest.

## Firma

```python
class InstrumentosLegalesMemorandum(models.Model):
```

## Uso real

`CrearInstrumentoLegalMemorandum`/`UpdateInstrumentoLegalMemorandum` (`secretariador/views/instrumentolegalviews.py`).

## Ver también

- [LicenciaPermiso](../../personalizador/models/LicenciaPermiso.md) — puede vincular un Memorandum como instrumento legal.
