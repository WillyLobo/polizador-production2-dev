---
symbol: ContratosDigitales
kind: class
module: carga/models.py
lines: 1655-1666
signature_hash: sha1:c87018148be53d012f495576b43a1a09c721a851
authored: true
---
# ContratosDigitales

**Módulo:** `carga/models.py` (líneas 1655-1666) · hereda de `models.Model`

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