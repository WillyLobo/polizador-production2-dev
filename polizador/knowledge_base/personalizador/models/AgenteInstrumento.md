---
symbol: AgenteInstrumento
kind: class
module: personalizador/models.py
lines: 264-346
signature_hash: sha1:b1b8d51efb28c6653061718a92c611bd174defba
authored: false
---

# AgenteInstrumento

**Módulo:** `personalizador/models.py` (líneas 264-346)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class AgenteInstrumento(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `personalizador/models.py:126` — `# Instrumentos legales: filas de AgenteInstrumento (varias por concepto), ver`
- `personalizador/models.py:157` — `# esta en cada AgenteInstrumento de aportes.`
- `personalizador/models.py:218` — `filas son los AgenteInstrumento del concepto (con link al PDF o a la edicion de cada`
- `personalizador/views/agenteviews.py:9` — `from personalizador.models import Agente, AgenteInstrumento`
- `personalizador/views/agenteviews.py:72` — `Prefetch("instrumentos_legales", queryset=AgenteInstrumento.objects.select_related("resolucion", "decreto", "externo")),`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
