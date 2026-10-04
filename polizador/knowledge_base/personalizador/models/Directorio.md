---
symbol: Directorio
kind: class
module: personalizador/models.py
lines: 385-400
signature_hash: sha1:32ab1b8423205df66f1aec1d93197aaec6b015a5
authored: true
---

# Directorio

**Módulo:** `personalizador/models.py` (líneas 385-400) · hereda de `models.Model`

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
