---
symbol: TextoResolucionCertificado
kind: class
module: carga/models.py
lines: 1015-1095
signature_hash: sha1:4d170933bf981d481198638adb0bf533ff809d14
authored: true
---

# TextoResolucionCertificado

**Módulo:** `carga/models.py` (líneas 1015-1095) · hereda de `models.Model`

## Propósito

Plantilla, en Jinja, del texto de la resolución que aprueba un Certificado. El
articulado cambia según el Programa, el financiamiento (Nación/Provincia/Terceros) y el tipo
de certificado (un anticipo no dice lo mismo que un avance). Esas combinaciones las conoce
el área y no el desarrollador, por eso el texto se guarda en la base y se carga desde la
web, a diferencia de las resoluciones de viáticos, cuyo texto está fijo en
`secretariador/docx_texto.py`.

El **alcance** es la terna (`textoresolucion_programa`, `textoresolucion_financiamiento`,
`textoresolucion_tipo`), única por `UniqueConstraint`. `textoresolucion_tipo=""` es el
comodín: el texto genérico de ese programa y financiamiento, para cuando no hay uno
específico del tipo. Es `""` y no NULL a propósito, porque en Postgres dos NULL no chocan y
la restricción dejaría cargar comodines duplicados. `TIPO` es `Certificado.TIPO` sin
`LEGACY`: a los certificados históricos no se les redactan resoluciones nuevas.

`textoresolucion_bloques` es una lista JSON de `{clase, label, texto}` (`clase` ∈ visto,
bloque, considerando, resuelve, articulo; ver `CLASE_CHOICES` en
`carga/forms/textoresolucionforms.py`), donde cada `texto` es fuente Jinja que
`carga/resolucion_texto.py` evalúa contra `contexto_certificado()`.

`para_certificado(certificado)` resuelve la plantilla en una sola query: filtra por el
programa de la obra, el financiamiento del certificado y `tipo in [tipo, ""]`, ordena para
que gane la coincidencia exacta sobre el comodín y devuelve `None` si no hay ninguna.
`alcance` es la etiqueta legible de la terna para el listado. Tiene `HistoricalRecords`, y
el snapshot de cada certificado guarda qué fila histórica se usó (ver
[_history_id](../views/textoresolucionviews/_history_id.md)).

## Firma

```python
class TextoResolucionCertificado(models.Model):
```

## Uso real

```python
# carga/views/textoresolucionviews.py (_texto_certificado)
plantilla = TextoResolucionCertificado.para_certificado(certificado)
if plantilla is None:
    return None, set(), None, None
```
Alta/edición desde [CrearTextoResolucion](../views/textoresolucionviews/CrearTextoResolucion.md)/[UpdateTextoResolucion](../views/textoresolucionviews/UpdateTextoResolucion.md).

## Ver también

- [Certificado](Certificado.md) — `certificado_texto_resolucion` guarda el texto ya resuelto.
- [TextoResolucionEditorMixin](../views/textoresolucionviews/TextoResolucionEditorMixin.md)
- [editar_texto_resolucion_certificado](../views/textoresolucionviews/editar_texto_resolucion_certificado.md)
- [Programa](Programa.md)
