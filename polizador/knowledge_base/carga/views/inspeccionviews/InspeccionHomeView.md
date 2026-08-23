---
symbol: InspeccionHomeView
kind: class
module: carga/views/inspeccionviews.py
lines: 10-36
signature_hash: sha1:9817dc23fb9cbec5f1b05e696e23320a3295bdc9
authored: true
---

# InspeccionHomeView

**Módulo:** `carga/views/inspeccionviews.py` (líneas 10-36) · hereda de `generic.ListView`

## Propósito

Home alternativa para el rol de inspección de obra (no el dashboard general): lista las
Obras donde el usuario logueado figura como `obra_inspector` (vía su `Agente` vinculado,
`request.user.agente`), y separado, las Fojas de Medición donde figura como
`foja_inspector` — ambos vacíos si el usuario no tiene un `Agente` asociado o no
pertenece al grupo `inspeccion`. Si además pertenece al grupo `certificadores`, agrega un
tercer listado: Fojas sin ningún Certificado generado todavía
(`certificado__isnull=True`) — la cola de trabajo pendiente de certificar.

## Firma

```python
class InspeccionHomeView(generic.ListView):
```

## Uso real

`path('home/', InspeccionHomeView.as_view(), name='home')` (`polizador/urls.py`) — la página `/home/` del sitio.

## Ver también

- [Obra](../../models/Obra.md)
- [FojaDeMedicion](../../models/FojaDeMedicion.md)
