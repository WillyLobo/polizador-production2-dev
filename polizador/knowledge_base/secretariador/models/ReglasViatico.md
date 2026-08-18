---
symbol: ReglasViatico
kind: class
module: secretariador/models.py
lines: 311-335
signature_hash: sha1:dc3723381cf81638fdfe690d50913781185bd582
authored: true
---

# ReglasViatico

**Módulo:** `secretariador/models.py` (líneas 311-335) · hereda de `models.Model`

## Propósito

Configuración global (singleton, `pk` forzado a 1 vía `save()`/`get_solo()` — mismo
patrón que un modelo "solo una fila" de Django) de excepciones al cálculo estándar de
viáticos: si el personal de gabinete cobra viático, si las autoridades del Directorio
cobran dentro del Chaco, un escalafón fijo para autoridades (independiente del
`agente_escalafon` individual), la opción de forzar un único escalafón para todos, y si
los comisionados externos cobran viático (con su propio escalafón por defecto, ya que no
tienen `agente_escalafon`). Es una adición reciente (reemplazó un escalafón fijo
hardcodeado — ver historial de commits) que centraliza reglas que antes vivían dispersas
o hardcodeadas en el código de cálculo.

## Firma

```python
class ReglasViatico(models.Model):
```

## Uso real

`ComisionadoSolicitud.valor_viatico_dia()`: `reglas = ReglasViatico.get_solo()` al principio del cálculo.

## Ver también

- [ComisionadoSolicitud](ComisionadoSolicitud.md)
