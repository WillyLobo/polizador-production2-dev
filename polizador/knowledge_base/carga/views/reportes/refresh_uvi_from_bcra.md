---
symbol: refresh_uvi_from_bcra
kind: function
module: carga/views/reportes.py
lines: 189-191
signature_hash: sha1:4ec4fda2f5acb8aae9df9c2869a609ebc40019d4
authored: true
---

# refresh_uvi_from_bcra

**Módulo:** `carga/views/reportes.py` (líneas 189-191)

## Propósito

Dispara el management command `bcra_uvi` (sincroniza cotizaciones UVI desde la API pública del BCRA, ver `carga/bcra_api.py`/CLAUDE.md) directamente desde un request HTTP, y redirige de vuelta al listado de UVI. Nota: corre el comando **síncronamente dentro del request** (`call_command` sin cola de tareas) — si el BCRA responde lento, el usuario espera esa misma demora en el navegador.

## Firma

```python
def refresh_uvi_from_bcra(request):
```

## Uso real

Botón "Actualizar" en `Lista-uvi.html`, apuntando a esta vista.

## Ver también

- [CrearListaUvi](CrearListaUvi.md)
- [Uvi](../../models/Uvi.md)
