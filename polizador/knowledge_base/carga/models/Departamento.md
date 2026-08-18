---
symbol: Departamento
kind: class
module: carga/models.py
lines: 259-273
signature_hash: sha1:46146712b5f1cf60ffc33899a03c5df20bab073a
authored: false
---

# Departamento

**Módulo:** `carga/models.py` (líneas 259-273)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Departamento(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:286` — `localidad_departamento	= models.ForeignKey("Departamento", verbose_name="Departamento", on_delete=models.RESTRICT)`
- `carga/models.py:292` — `# return "{} - Departamento {}".format(self.localidad_nombre, self.localidad_departamento)`
- `carga/models.py:305` — `municipio_departamento  = models.ForeignKey("Departamento", verbose_name="Departamento", on_delete=models.CASCADE)`
- `carga/models.py:342` — `obra_departamento_m = models.ManyToManyField("Departamento", related_name="obra_departamento", verbose_name="Departamento", blank=True)`
- `carga/views/certificadoviews.py:24` — `from personalizador.models import Departamento, Direccion, Directorio, Gerencia`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
