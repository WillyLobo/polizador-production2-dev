---
symbol: ConjuntoLicitado
kind: class
module: carga/models.py
lines: 859-892
signature_hash: sha1:b5b1317a64be2bc391558178677e0d9cf17c4b05
authored: false
---

# ConjuntoLicitado

**Módulo:** `carga/models.py` (líneas 859-892)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class ConjuntoLicitado(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:315` — `# Compartido por los campos de resolución cargados a mano (Obra/ConjuntoLicitado/Contrato),`
- `carga/models.py:345` — `obra_conjunto = models.ForeignKey("ConjuntoLicitado", verbose_name="Conjunto Licitado", on_delete=models.SET_NULL, null=True, blank=True)`
- `carga/views/conjuntoviews.py:7` — `from carga.models import ConjuntoLicitado`
- `carga/views/conjuntoviews.py:15` — `model = ConjuntoLicitado`
- `carga/views/conjuntoviews.py:23` — `model = ConjuntoLicitado`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
