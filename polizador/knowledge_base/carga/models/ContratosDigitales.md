---
symbol: ContratosDigitales
kind: class
module: carga/models.py
lines: 1376-1387
signature_hash: sha1:8d3d699a4da86780625333dfc5b7f20a4635eb6b
authored: true
---
# ContratosDigitales

**Módulo:** `carga/models.py` (líneas 1376-1387) · hereda de `models.Model`

## Propósito

Documento PDF adjunto a un Contrato, con un `ContratoRubro` (tipo de documento) — el equivalente de `ObraDocumento` pero para Contrato, y con categorización propia.

## Firma

```python
class ContratosDigitales(models.Model):
```

## Uso real

`Contrato.documentos_contrato` (related_name) es la relación inversa; también hay `Obra.documentos_contrato()`, que filtra por todos los Contratos de la Obra.

## Ver también

- [Contrato](Contrato.md)
- [ContratoRubro](ContratoRubro.md)
- [ObraDocumento](ObraDocumento.md)