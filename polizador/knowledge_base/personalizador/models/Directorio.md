---
symbol: Directorio
kind: class
module: personalizador/models.py
lines: 346-361
signature_hash: sha1:c13b022f568745f21196b2b388dc5feee2f6aaee
authored: true
---

# Directorio

**Módulo:** `personalizador/models.py` (líneas 346-361) · hereda de `models.Model`

## Propósito

El nivel más alto del árbol organizacional (ej. Presidencia, Vocalía 1, Vocalía 2 — ver el comentario en `Meta`). `directorio_autoridad_a_cargo_fk` es el `Agente` real a cargo (usado, por ejemplo, para resolver firmantes institucionales en documentos generados desde `carga`/`secretariador`); `directorio_autoridad_a_cargo` es el mismo dato como texto libre, probablemente el campo legado antes de vincularlo a un Agente real.

## Firma

```python
class Directorio(models.Model):
```

## Uso real

Raíz del árbol usado por [Oficina](Oficina.md); `directoriowidget` en varios forms.

## Ver también

- [Oficina](Oficina.md)
- [Gerencia](Gerencia.md)
- [Agente](Agente.md)
