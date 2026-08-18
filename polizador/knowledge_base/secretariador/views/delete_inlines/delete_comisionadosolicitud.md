---
symbol: delete_comisionadosolicitud
kind: function
module: secretariador/views/delete_inlines.py
lines: 15-28
signature_hash: sha1:7a58ef65018db140f7bab6e33c316b51852ed37d
authored: true
---

# delete_comisionadosolicitud

**Módulo:** `secretariador/views/delete_inlines.py` (líneas 15-28)

## Propósito

Borra un `ComisionadoSolicitud` puntual y redirige de vuelta a la edición de su
`Solicitud` — el mecanismo para sacar un comisionado de una Solicitud sin pasar por el
formset completo (ej. un link de borrado inline en la tabla de comisionados).

**Bug real detectado, no hipotético:** en la rama `except ComisionadoSolicitud.DoesNotExist`,
el código intenta `redirect('secretariador:update-solicitud', pk=comisionado.comisionadosolicitud_foreign.id)`
— pero `comisionado` nunca se asignó en esa rama (el `.get()` que lo asignaría es
justamente lo que falló), así que esto lanza `UnboundLocalError` en vez del `HttpResponseRedirect`
que el código claramente intenta devolver. En la práctica, si `pk` no existe, esta vista
rompe con un 500 en vez de mostrar el mensaje "Object Does not exist" que arma antes.

## Firma

```python
def delete_comisionadosolicitud(request, pk):
```

## Uso real

`delete_comisionadosolicitud` (`secretariador:delete-comisionadosolicitud` o similar — ver `secretariador/urls.py`), enlazada desde `UpdateSolicitud`.

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
