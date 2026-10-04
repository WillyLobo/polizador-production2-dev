---
symbol: Certificado
kind: class
module: carga/models.py
lines: 719-1012
signature_hash: sha1:a01646905b8bba3a1affaf19d4995d8f704e78a9
authored: true
---

# Certificado

**Módulo:** `carga/models.py` (líneas 719-1012) · hereda de `models.Model`

## Propósito

El otro modelo central de `carga`: un certificado de pago (avance de obra) sobre una Obra.
Con ~290 líneas es el modelo más grande del módulo. Su complejidad viene de que
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

**Monto certificado vs. importe a abonarse.** `certificado_monto_cobrar` *no* descuenta el
Fondo de Reparo, porque se usa como monto certificado (acumulados, saldo de la obra,
reportes, legacy): el Fondo de Reparo se retiene pero la obra sigue estando certificada. El
"importe a abonarse" que figura en la hoja del certificado sale de
`certificado_importe_abonar_pesos()`/`_uvi()`: monto menos devolución, menos descuento de
anticipo y menos Fondo de Reparo. Se calcula desde los campos y no desde el
`GeneratedField`, así que también funciona con certificados todavía sin guardar (la
previsualización de `GenerarCertificadosDesdeFoja`).

**Retención adobe (Decreto 654/2015).** Se retiene el tres por mil
(`RETENCION_ADOBE_PCT = 0.3`) del monto bruto cuando el rubro del certificado es Vivienda
(`certificadorubro_nombre_corto == "V"`). Se decide por rubro y no por obra, de modo que
cubre también los certificados legacy, y aplica a cualquier `certificado_tipo`, ANTICIPO
incluido.

**Período certificado.** `certificado_periodo_fecha` es el mes que se certifica: el
`foja_periodo` de la Foja de origen si la tiene (PARCIAL/ETAPA) y si no, `certificado_fecha`.
Una foja de septiembre se certifica en octubre, así que la fecha de emisión no sirve como
período.

**Texto de la resolución.** `certificado_texto_resolucion` (JSON, `editable=False`) guarda
el texto de la resolución ya renderizado desde [TextoResolucionCertificado](TextoResolucionCertificado.md),
con los retoques que se le hayan hecho a mano desde la web, y registra de qué plantilla y de
qué versión salió. Si está vacío, el texto se vuelve a resolver desde la plantilla (ver
`editar_texto_resolucion_certificado`).

## Firma

```python
class Certificado(models.Model):
```

## Uso real

Un certificado PARCIAL se construye en `certificacion.py`, no directamente en una vista
(la vista arma los datos y delega el cálculo):

```python
# carga/certificacion.py:742
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
# carga/certificacion.py:677 (dentro del loop de tramos_pendientes)
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

- [TextoResolucionCertificado](TextoResolucionCertificado.md) — plantilla del texto de la resolución.
- [GenerarCertificadosDesdeFoja](../views/certificadoviews/GenerarCertificadosDesdeFoja.md)
