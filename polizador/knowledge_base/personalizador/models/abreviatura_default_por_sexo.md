---
symbol: abreviatura_default_por_sexo
kind: function
module: personalizador/models.py
lines: 19-23
signature_hash: sha1:72576e412ba226912fd9a566595ff2637f46508b
authored: true
---

# abreviatura_default_por_sexo

**Módulo:** `personalizador/models.py` (líneas 19-23)

## Propósito

Devuelve "Sr."/"Sra." según el `GeneroAgente` (comparando el nombre "Masculino" a mano, no un campo booleano/código) — el mismo criterio de género binario que usa el resto del código para pronombres ("el"/"la"). Sirve de default cuando no se carga una abreviatura explícita.

## Firma

```python
def abreviatura_default_por_sexo(sexo):
```

## Uso real

`Agente.save()` / `ComisionadoExterno.save()` (mismo módulo, más abajo): `self.abreviatura = abreviatura_default_por_sexo(self.sexo)` si `abreviatura` está vacío.

## Ver también

- [Agente](Agente.md)
- [ComisionadoExterno](ComisionadoExterno.md)
- [GeneroAgente](GeneroAgente.md)
