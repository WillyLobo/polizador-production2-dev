---
symbol: Oficina
kind: class
module: personalizador/models.py
lines: 271-331
signature_hash: sha1:ef6624976743e0278ca6749b9808a459b978b074
authored: true
---

# Oficina

**Módulo:** `personalizador/models.py` (líneas 271-331) · hereda de `models.Model`

## Propósito

Un nodo del árbol organizacional Directorio > Gerencia > Dirección > Departamento — pero
no es un catálogo más de "oficinas" con nombre propio: es la combinación de FKs
(`cargo_directorio`/`cargo_gerencia`/`cargo_direccion`/`cargo_departamento`) que ubica a
un `Agente` (`Agente.oficina`) en ese árbol, y su `__str__` arma el nombre concatenando
los niveles no vacíos.

`clean()` es la pieza real: una Oficina se ubica en el nivel **más profundo** que se le
asigna (Departamento, si no Dirección, si no Gerencia), y los niveles superiores se
**derivan** de ese nodo en vez de elegirse por separado — así no puede quedar una
inconsistencia como "una Dirección que en realidad depende de otra Gerencia". Si el
usuario ya cargó a mano un nivel superior que no coincide con el derivado, `clean()`
rechaza el guardado con un `ValidationError` en vez de sobreescribirlo silenciosamente.

## Firma

```python
class Oficina(models.Model):
```

## Uso real

`CrearOficina`/`UpdateOficina` (`personalizador/views/oficinaviews.py`), con los widgets dependientes `oficina_gerenciawidget`/`oficina_direccionwidget`/`oficina_departamentowidget` (`personalizador/views/ajaxviews.py`) acotando las opciones según lo ya elegido.

## Ver también

- [Directorio](Directorio.md)
- [Gerencia](Gerencia.md)
- [Direccion](Direccion.md)
- [Departamento](Departamento.md)
- [Agente](Agente.md)
