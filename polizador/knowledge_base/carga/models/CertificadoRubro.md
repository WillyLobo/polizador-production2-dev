---
symbol: CertificadoRubro
kind: class
module: carga/models.py
lines: 693-704
signature_hash: sha1:cac96662f08f0581d98d2214cca88c76553d62db
authored: true
---

# CertificadoRubro

**Módulo:** `carga/models.py` (líneas 693-704) · hereda de `models.Model`

## Propósito

Catálogo normalizado de "rubros" de certificación (Vivienda, Infraestructura Frentista,
Terreno, Redeterminación, Nexos y Redes, Complementario, Deductivo...). Reemplaza al
`CharField` con `choices` original (`Certificado.RUBRO`, todavía presente en el modelo
como `certificado_rubro`, marcado "Obsoleto" en un comentario) — `certificado_rubro_db`
es el FK real hacia acá, usado por el código actual.

## Firma

```python
class CertificadoRubro(models.Model):
```

## Uso real

Referenciado desde `Certificado.certificado_rubro_db` y `PlanDeTrabajosRubro.rubro_certificado_rubro` (para poder ubicar el `ContratoMonto` correcto al generar un certificado desde una Foja).

## Ver también

- [Certificado](Certificado.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)
