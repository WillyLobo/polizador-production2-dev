---
symbol: HistorialView
kind: class
module: core/views.py
lines: 29-47
signature_hash: sha1:40477ef8ec2545485ebd1ab9076db01cec381402
authored: true
---

# HistorialView

**Módulo:** `core/views.py` (líneas 29-47) · hereda de `LoginRequiredMixin, TemplateView`

## Propósito

Endpoint genérico de la barra lateral de historial: `/historial/<app_label>/<model_name>/<pk>/`
devuelve el fragmento `partials/historial-timeline.html` con la línea de tiempo de cambios
de cualquier objeto auditado con `simple_history`. `base.html` lo carga con el tag
`{% historial_sidebar %}` en toda página de un solo objeto (`object`, o `historial_object`
si la vista quiere mostrar la historia de otro objeto, como hace la matriz de Etapas con el
Plan).

Los chequeos van en orden: modelo inexistente o sin historial → 404, usuario sin permiso
de ver/cambiar el modelo (`can_view_history`) → 403, pk inválido o inexistente → 404. La
línea de tiempo sale de `core/history.py`: `sources_for(obj)` junta la historia propia más
la de los hijos registrados con `register(model, children=...)` (por ejemplo, Póliza con sus
movimientos y documentos) y `build_timeline()` la ordena, agrupa los cambios consecutivos
del mismo usuario (`GROUP_GAP`), oculta el hash de la contraseña y saltea los guardados que
sólo tocan `last_login`.

## Firma

```python
class HistorialView(LoginRequiredMixin, TemplateView):
```

## Uso real

`historial` (`polizador/urls.py`), pedido por AJAX desde la pestaña de historial de `base.html`.

## Ver también

- [LoginEvent](../models/LoginEvent.md)
- [CustomUser](../../personalizador/models/CustomUser.md) — su historial también audita grupos y permisos (`M2MHistoricalRecords`).
