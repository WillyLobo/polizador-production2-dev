---
symbol: ComisionadoExterno
kind: class
module: personalizador/models.py
lines: 479-512
signature_hash: sha1:a504a6cb5bc9747900784aace2eae6bae3411691
authored: true
---

# ComisionadoExterno

**Módulo:** `personalizador/models.py` (líneas 479-512) · hereda de `models.Model`

## Propósito

Persona externa al Instituto (de otro organismo, contratada puntualmente) que puede
comisionarse a viajar en una Solicitud de viáticos de `secretariador`, sin ser un
`Agente` — explícitamente no debe aparecer en reportes de RRHH/organigrama/nómina (ver
el docstring del modelo). Expone deliberadamente los mismos nombres de atributo que
`Agente` (`agente_nombres`, `agente_apellidos`, `dni`, `cuil`, `sexo`...) para el
subconjunto de datos que necesita `secretariador.ComisionadoSolicitud.persona` — así ese
campo puede apuntar indistintamente a un `Agente` o a un `ComisionadoExterno` sin lógica
condicional por tipo en el código que solo lee esos atributos comunes.

Mismo patrón de `save()` que `Agente`: infiere `abreviatura` de `sexo` si no se cargó.

## Firma

```python
class ComisionadoExterno(models.Model):
```

## Uso real

`secretariador.ComisionadoSolicitud.persona` (GenericForeignKey o unión de tipos, ver `secretariador`).

## Ver también

- [Agente](Agente.md)
- [abreviatura_default_por_sexo](abreviatura_default_por_sexo.md)
