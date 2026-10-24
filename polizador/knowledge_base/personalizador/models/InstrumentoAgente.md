---
symbol: InstrumentoAgente
kind: class
module: personalizador/models.py
lines: 270-307
signature_hash: sha1:e3dd898522c8e4065acc37896a26b97942370f21
authored: false
---

# InstrumentoAgente

**Módulo:** `personalizador/models.py` (líneas 270-307)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class InstrumentoAgente(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `personalizador/models.py:120` — `# InstrumentoAgente (otros organismos); ver personalizador/instrumentos.py::CONCEPTOS. Las`
- `personalizador/models.py:154` — `instrumento_transferencia_definitiva_externo = models.ForeignKey("InstrumentoAgente", verbose_name="Instrumento externo de transferencia definitiva", related_name="agentes_transferencia_definitiva", on_delete=models.PROTECT, blank=True, null=True)`
- `personalizador/models.py:164` — `instrumento_aportes_ley_externo = models.ForeignKey("InstrumentoAgente", verbose_name="Instrumento externo de aportes", related_name="agentes_aportes_ley", on_delete=models.PROTECT, blank=True, null=True)`
- `personalizador/models.py:169` — `instrumento_aportes_anses_externo = models.ForeignKey("InstrumentoAgente", verbose_name="Instrumento de aportes ANSES", related_name="agentes_aportes_anses", on_delete=models.PROTECT, blank=True, null=True)`
- `personalizador/views/instrumentoagenteviews.py:7` — `from personalizador.models import InstrumentoAgente`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
