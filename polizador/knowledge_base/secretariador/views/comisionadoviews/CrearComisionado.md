---
symbol: CrearComisionado
kind: class
module: secretariador/views/comisionadoviews.py
lines: 13-29
signature_hash: sha1:7549e24f1c02f7633ef404575a2c2521c976e308
authored: true
---

# CrearComisionado

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 13-29) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un Agente **en su rol de comisionado** — es decir, la misma tabla `personalizador.Agente`, con un `ComisionadoForm` acotado a los campos relevantes para viáticos (nombre, sexo, oficina, DNI/CUIL, si es transitorio/gabinete) en vez del `AgenteForm` completo de RRHH. `secretariador` no tiene su propio modelo de "comisionado interno" — reusa `Agente` con un form más chico.

## Firma

```python
class CrearComisionado(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearComisionado` (`secretariador:crear-comisionado`).

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
