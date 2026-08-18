---
symbol: ActualizarEncabezado
kind: class
module: secretariador/views/encabezadoviews.py
lines: 11-31
signature_hash: sha1:98a5841a8d26230a45609c119f237b69349a7a8d
authored: true
---

# ActualizarEncabezado

**Módulo:** `secretariador/views/encabezadoviews.py` (líneas 11-31) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Sube un nuevo `EncabezadoDocumento` (`.docx` base con el encabezado institucional) y registra quién lo subió (`form_valid` setea `encabezadodocumento_subido_por` antes de guardar). Muestra los últimos 10 encabezados subidos como historial.

## Firma

```python
class ActualizarEncabezado(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`ActualizarEncabezado` (`secretariador:actualizar-encabezado`), enlazada desde el navbar ("Herramientas").

## Ver también

- [EncabezadoDocumento](../../models/EncabezadoDocumento.md)
