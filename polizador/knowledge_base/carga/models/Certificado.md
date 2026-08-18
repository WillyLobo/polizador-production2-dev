---
symbol: Certificado
kind: class
module: carga/models.py
lines: 626-857
signature_hash: sha1:90387eb8717b19fe9149d8d3feeb42c48d659e52
authored: true
---

# Certificado

**Módulo:** `carga/models.py` (líneas 626-857) · hereda de `models.Model`

## Propósito

El otro modelo central de `carga`: un certificado de pago (avance de obra) sobre una Obra.
Con 231 líneas es el modelo más grande del módulo. Su complejidad viene de que
`certificado_tipo` (`TIPO`) no es una simple etiqueta — cada tipo tiene reglas de negocio
propias, todas enforced en `clean()`:

- **PARCIAL**: certificado de avance mensual normal. Requiere `certificado_foja` (la Foja
  de Medición de origen) y **no** debe tener `certificado_contrato_origen`.
- **ANTICIPO**: adelanto financiero sobre toda la Obra (no un rubro puntual — es un
  "pool"). No lleva Foja. Usa `certificado_anticipo_pct` (cargado a mano) y los campos
  `editable=False` `certificado_anticipo_anterior`/`certificado_anticipo_acumulado`/
  `certificado_anticipo_saldo_pct`, todos calculados automáticamente por
  `certificacion.calcular_monto_anticipo`/`certificacion.aplicar_descuento_anticipo` (no
  por este modelo).
- **HECHO_CONSUMADO**: certificado sin Foja, amparado directamente por un
  Contrato/Resolución (`certificado_contrato_origen`, obligatorio acá).
- **ETAPA**: certificación por tramos fijos de Contrato (ver
  `Contrato.contrato_certificacion_por_etapas`) — requiere tanto `certificado_foja` (la
  Foja que alcanzó el umbral) como `certificado_contrato_tramo` (el `ContratoTramoPago`
  que salda), y tampoco lleva `certificado_contrato_origen`.
- **LEGACY**: certificados históricos sin clasificar, antes de que existiera esta
  distinción de tipos.

`certificado_monto_cobrar`/`certificado_monto_cobrar_uvi` son `GeneratedField` (calculados
por la base): monto menos devolución menos descuento de anticipo. `certificado_pct_principal`
es el % "genérico" para listados que no distinguen tipo (usa `certificado_anticipo_pct`,
`certificado_etapa_pct` o `certificado_mes_pct` según corresponda).

## Firma

```python
class Certificado(models.Model):
```

## Uso real

Un certificado PARCIAL se construye en `certificacion.py`, no directamente en una vista
(la vista arma los datos y delega el cálculo):

```python
# carga/certificacion.py:703
certificado = Certificado(
    certificado_obra=obra,
    certificado_tipo="PARCIAL",
    certificado_foja=foja,
    certificado_financiamiento=financiamiento,
    certificado_rubro_db=contratomonto.contratomonto_rubro,
    certificado_mes_pct=mes_pct,
    ...
)
```

Un certificado ETAPA, con la misma lógica pero disparado por tramos pendientes:

```python
# carga/certificacion.py:639 (dentro del loop de tramos_pendientes)
certificado = Certificado(
    certificado_obra=contrato.contrato_obra,
    certificado_tipo="ETAPA",
    certificado_foja=foja,
    certificado_contrato_tramo=tramo,
    ...
)
```

## Ver también

- [Obra](Obra.md)
- [FojaDeMedicion](FojaDeMedicion.md)
- [Contrato](Contrato.md) — `contrato_certificacion_por_etapas` decide si esta Obra genera certificados PARCIAL o ETAPA.
- [ContratoTramoPago](ContratoTramoPago.md)
- [CertificadoRubro](CertificadoRubro.md)
