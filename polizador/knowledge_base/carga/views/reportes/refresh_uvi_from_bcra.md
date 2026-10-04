---
symbol: refresh_uvi_from_bcra
kind: function
module: carga/views/reportes.py
lines: 194-196
signature_hash: sha1:3d9fe8b9e18ba170ec43a626f67336324329f201
authored: true
---
# refresh_uvi_from_bcra

**Módulo:** `carga/views/reportes.py` (líneas 194-196)

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