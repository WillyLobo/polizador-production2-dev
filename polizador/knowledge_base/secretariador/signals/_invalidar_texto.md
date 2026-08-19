---
symbol: _invalidar_texto
kind: function
module: secretariador/signals.py
lines: 57-63
signature_hash: sha1:5035a1850b57f2a644f3a2848db136a0a2f94607
authored: true
---

# _invalidar_texto

**Módulo:** `secretariador/signals.py` (líneas 57-63)

## Propósito

Helper genérico compartido por `Solicitud` e `Incorporacion`: si la fila `pk` de `model`
existe y su `campo_texto` (`solicitud_texto_actuacion`/`incorporacion_texto_actuacion`) no
es ya `None`, lo pone en `None` y guarda solo ese campo
(`obj.save(update_fields=[campo_texto])`). El `.exclude(**{campo_texto: None})` evita un
`UPDATE` (y el `post_save`/historial que dispara) cuando no hace falta — el texto ya
estaba vacío.

Recibe `model` como parámetro en vez de estar hardcodeado a `Solicitud` para no duplicar
la misma lógica de "buscar, comparar, limpiar, guardar" en dos funciones casi idénticas
para `Solicitud` e `Incorporacion`.

## Firma

```python
def _invalidar_texto(model, pk, campo_texto):
```

## Uso real

Instanciado para cada modelo por los dos wrappers de una línea del mismo módulo:
`_invalidar_texto(Solicitud, solicitud_id, "solicitud_texto_actuacion")` en
[_invalidar_texto_solicitud](_invalidar_texto_solicitud.md) y
`_invalidar_texto(Incorporacion, incorporacion_id, "incorporacion_texto_actuacion")` en
[_invalidar_texto_incorporacion](_invalidar_texto_incorporacion.md).

## Ver también

- [_invalidar_texto_solicitud](_invalidar_texto_solicitud.md)
- [_invalidar_texto_incorporacion](_invalidar_texto_incorporacion.md)
