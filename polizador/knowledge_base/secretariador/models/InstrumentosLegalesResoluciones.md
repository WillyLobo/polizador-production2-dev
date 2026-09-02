---
symbol: InstrumentosLegalesResoluciones
kind: class
module: secretariador/models.py
lines: 137-230
signature_hash: sha1:fa3dc89b4e1a30e26ee83abdae07b428f2e66b1e
authored: true
---
# InstrumentosLegalesResoluciones

**Módulo:** `secretariador/models.py` (líneas 137-230) · hereda de `models.Model`

## Propósito

Una resolución institucional (Presidencia o Directorio), con acción clasificada
(Adjudicatoria/Aprobatoria/Ratificatoria/Ampliatoria) y estado de escaneo. Dos
`GeneratedField` construyen representaciones textuales distintas del mismo número:
`instrumentolegalresoluciones_str` (para mostrar, formato corto `numero-acta-ano` en
Directorio o `numero-ano` en Presidencia) e `instrumentolegalresoluciones_numero_sgt`
(formato largo `RES-ano-numero-10-{acta|1}`, pensado para calzar con el formato que usa
el SGT — Sistema de Gestión de Trámites, ver `carga/management/commands/sync_resoluciones_sgt`
y `personalizador/management/commands` en CLAUDE.md — al importar/exportar resoluciones).
`get_absolute_url` deriva a una de dos vistas de edición distintas (Presidencia/Directorio)
según `instrumentolegalresoluciones_tipo`.

## Firma

```python
class InstrumentosLegalesResoluciones(models.Model):
```

## Uso real

`Obra.obra_resolucion_fk`, `Contrato.contrato_resolucion_fk`, `ConjuntoLicitado.conjunto_resolucion_fk` (`carga`), `Solicitud.solicitud_resolucion`, `Incorporacion.incorporacion_resolucion` (mismo módulo) — el instrumento legal más referenciado entre apps del proyecto.

## Ver también

- [Solicitud](Solicitud.md)
- [Incorporacion](Incorporacion.md)