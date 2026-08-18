---
symbol: Obra
kind: class
module: carga/models.py
lines: 323-543
signature_hash: sha1:e3b2ff46f70d8f242347c1373f68026a8a170e03
authored: true
---

# Obra

**Módulo:** `carga/models.py` (líneas 323-543) · hereda de `models.Model`

## Propósito

El modelo central de `carga`: una obra pública IPDUV, con su empresa contratista, ubicación
geográfica (Región/Departamento/Municipio/Localidad, todos M2M salvo Región),
financiamiento total desglosado por Nación/Provincia/Terceros (pesos y UVI), resolución de
adjudicación, y las relaciones hacia Contrato/PlanDeTrabajos/Certificado/Póliza que cuelgan
de ella. Es, con 220 líneas y ~25 métodos/propiedades, el modelo más grande de `carga`
junto con `Certificado`.

Dos ideas de diseño no obvias:

- **Los montos de contrato son desnormalizados, no calculados al vuelo.**
  `obra_contrato_{nacion,provincia,terceros}_{pesos,uvi,uvi_fecha}` son campos reales en
  la tabla, mantenidos sincronizados por la señal
  [recalcular_montos_obra](../signals/recalcular_montos_obra.md) cada vez que cambia un
  `ContratoMonto` de cualquier Contrato de la Obra — ver ese método
  (`recalcular_montos_contrato()`) para el detalle del recálculo.
  `obra_contrato_total_pesos`/`obra_contrato_total_uvi` sí son `GeneratedField` (calculados
  por la base de datos, `db_persist=True`), la suma de los tres desnormalizados.
- **"Vigente" es siempre el más reciente por fecha, no un flag.** `plan_vigente()` y
  `contrato_vigente()` no filtran por ningún campo "activo": toman el
  `PlanDeTrabajos`/`Contrato` con `fecha` (y `pk` como desempate) más grande. Ambos
  métodos tienen la misma optimización: si la relación inversa ya viene precargada vía
  `prefetch_related`, ordenan en Python sobre esa colección en memoria en vez de disparar
  un `.order_by().first()` que ignoraría el prefetch y traería una instancia nueva sin sus
  propios prefetches anidados.

`ultimo_certificado_avance()` tiene su propia complejidad: solo cuenta como "certificado de
avance real" a los de tipo PARCIAL/HECHO_CONSUMADO/ETAPA (o LEGACY con
`certificado_rubro_obra>0`) — un Anticipo es un pool sobre toda la Obra, no un avance de
rubro puntual, y si fuera el certificado más reciente "taparía" el % de avance real con un
0 si se lo tomara como el último sin más.

## Firma

```python
class Obra(models.Model):
```

## Uso real

```python
# carga/views/obraviews.py (CrearObra.form_valid, ModelForm estándar)
self.object = form.save()
```

`recalcular_montos_contrato()` en particular se usa así, disparado por la señal (no a mano):

```python
# carga/signals.py:62 (recalcular_montos_obra)
instance.contratomonto_contrato.contrato_obra.recalcular_montos_contrato()
```

## Ver también

- [recalcular_montos_obra](../signals/recalcular_montos_obra.md) — señal que mantiene sincronizados los montos desnormalizados de este modelo.
- [Contrato](Contrato.md)
- [PlanDeTrabajos](PlanDeTrabajos.md)
- [Certificado](Certificado.md)
- [obras_con_acumulado_anotado](obras_con_acumulado_anotado.md)
