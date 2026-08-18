---
symbol: CertificadoRubro
kind: class
module: carga/models.py
lines: 600-611
signature_hash: sha1:eb0ec1cb5ce7fcedd060844262142d91ac48d705
authored: false
---

# CertificadoRubro

**Módulo:** `carga/models.py` (líneas 600-611)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class CertificadoRubro(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:644` — `# Obsoleto -> se migro a una tabla aparte(carga.models.CertificadoRubro)`
- `carga/models.py:668` — `certificado_rubro = models.CharField("Rubro", max_length=1, choices=RUBRO, default="V") # Obsoleto -> se migro a una tabla aparte(carga.models.CertificadoRubro)`
- `carga/models.py:669` — `certificado_rubro_db = models.ForeignKey("CertificadoRubro", verbose_name="Rubro", on_delete=models.PROTECT, default=1)`
- `carga/models.py:937` — `"CertificadoRubro",`
- `carga/models.py:1364` — `contratomonto_rubro = models.ForeignKey("CertificadoRubro", verbose_name="Rubro Certificado", on_delete=models.CASCADE)`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
