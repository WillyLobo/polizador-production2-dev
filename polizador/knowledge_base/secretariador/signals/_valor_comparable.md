---
symbol: _valor_comparable
kind: function
module: secretariador/signals.py
lines: 45-54
signature_hash: sha1:09d5b09bf666ba1c899d928b5fd9012f0c8f8591
authored: true
---

# _valor_comparable

**Módulo:** `secretariador/signals.py` (líneas 45-54)

## Propósito

Normaliza el valor en memoria de `campo` en `instance` al mismo tipo que devuelve una
consulta `.values(...)` a la base, para que las comparaciones "¿cambió este campo?" en
`invalidar_texto_actuacion_por_cambio_de_datos`/`invalidar_texto_incorporacion_por_cambio_de_datos`
no den falsos positivos.

El caso concreto que motivó esto: un test creaba una `Solicitud` con
`solicitud_fecha_hasta="2026-01-02"` (string) — Django no llama a `to_python()` en una
asignación directa de atributo (solo lo hace `full_clean()`/la limpieza de un
`ModelForm`), así que ese string queda tal cual en el atributo hasta el próximo
`refresh_from_db()`. Compararlo sin normalizar contra el `datetime.date` que trae la fila
existente (`anterior[campo]`, ya tipado por la consulta) daba `True` aunque la fecha no
hubiera cambiado en absoluto, e invalidaba el texto guardado sin motivo.

Para los campos de FK guardados como `*_id` (p. ej. `solicitud_vehiculo_id`) no hace falta
normalizar — siempre son enteros simples en ambos lados — así que la función los devuelve
directo, sin pasar por `to_python()` (que además no aplica: `_meta.get_field()` con el
nombre del atributo `_id` no resuelve al campo real).

## Firma

```python
def _valor_comparable(instance, campo):
```

## Uso real

Usada por el closure `cambio()` dentro de
[invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md)
y directamente por
[invalidar_texto_incorporacion_por_cambio_de_datos](invalidar_texto_incorporacion_por_cambio_de_datos.md)
(`secretariador/signals.py:101` y `:116`), ambas dentro del mismo módulo.

## Ver también

- [invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md)
- [invalidar_texto_incorporacion_por_cambio_de_datos](invalidar_texto_incorporacion_por_cambio_de_datos.md)
