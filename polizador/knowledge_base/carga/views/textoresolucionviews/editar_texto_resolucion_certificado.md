---
symbol: editar_texto_resolucion_certificado
kind: function
module: carga/views/textoresolucionviews.py
lines: 206-240
signature_hash: sha1:3e86f16864b1db6d18648283895dff9a15d3e071
authored: true
---

# editar_texto_resolucion_certificado

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 206-240)

## Propósito

Revisión del texto ya resuelto de un Certificado, antes de emitir el `.docx`. Imita
`revisar_texto_actuacion` de viáticos: se guarda el **texto final** y no la plantilla.
Usa `BloqueTextoFormSet`, en el que sólo se edita la redacción (clase y etiqueta van
ocultas). En el POST guarda en `certificado_texto_resolucion`
`{textoresolucion_id, textoresolucion_history_id, bloques}`, es decir, de qué plantilla y
de qué versión de esa plantilla salió, para poder auditarlo
([_history_id](_history_id.md)). Con `accion=guardar` vuelve a la ficha del certificado; si
no, sigue directo a la descarga del `.docx`.

El template muestra las variables faltantes, el error de render si lo hubo y si lo que se
ve es un snapshot (`es_snapshot`), en cuyo caso ofrece restaurarlo desde la plantilla.
Exige `carga.change_certificado`.

## Firma

```python
def editar_texto_resolucion_certificado(request, pk):
```

## Uso real

`carga:editar-texto-resolucion-certificado`, enlazada desde la ficha del certificado (`certificado/certificado.html`). También es el destino de `resolucion_certificado_docx` cuando faltan datos.

## Ver también

- [_texto_certificado](_texto_certificado.md)
- [BloqueTextoForm](../../forms/textoresolucionforms/BloqueTextoForm.md)
- [restaurar_texto_resolucion_certificado](restaurar_texto_resolucion_certificado.md)
- [resolucion_certificado_docx](resolucion_certificado_docx.md)
- [invalidar_texto_resolucion_por_cambio_de_datos](../../signals/invalidar_texto_resolucion_por_cambio_de_datos.md)
