---
symbol: _articulo_dos_inicial
kind: function
module: secretariador/views/textoactuacionviews.py
lines: 16-26
signature_hash: sha1:7c015ca46858068710ef64546e2823d092132b18
authored: true
---

# _articulo_dos_inicial

**Módulo:** `secretariador/views/textoactuacionviews.py` (líneas 16-26)

## Propósito

Arma las filas iniciales del formset de Artículo Dos: siempre una fila por cada comisionado *actual* (`articulo_dos_default`, recién calculado desde los datos de hoy) — si hay texto ya guardado para ese comisionado específico (`comisionado_id`), usa el guardado; si no, el recién calculado. Así, agregar un comisionado nuevo después de haber editado el texto a mano no pierde las ediciones de los comisionados que ya estaban.

## Firma

```python
def _articulo_dos_inicial(articulo_dos_default, texto_guardado):
```

## Uso real

`revisar_texto_actuacion` (mismo módulo, más abajo).

## Ver también

- [revisar_texto_actuacion](revisar_texto_actuacion.md)
