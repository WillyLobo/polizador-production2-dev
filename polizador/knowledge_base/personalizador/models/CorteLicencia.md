---
symbol: CorteLicencia
kind: class
module: personalizador/models.py
lines: 626-702
signature_hash: sha1:f51a56c62c6506909f9309a70afe2d2eb159806e
authored: true
---

# CorteLicencia

**Módulo:** `personalizador/models.py` (líneas 626-702) · hereda de `models.Model`

## Propósito

Interrupción de una Licencia Anual (Ordinaria o de Invierno) ya otorgada: el agente se
reintegra a sus tareas antes de agotar los días, y el saldo pendiente queda disponible
para usarse después — total o fraccionado, vía
`LicenciaPermiso.licenciapermiso_saldo_de_corte` — hasta `cortelicencia_fecha_vencimiento`.

`clean()` valida que la Licencia interrumpida sea de uno de los dos tipos que admiten
corte (importa las constantes de nombre desde `personalizador.licencias`, mismo patrón de
import diferido que `LicenciaPermiso.clean()`), que las fechas de reintegro caigan dentro
del rango de la licencia original, y que días gozados + días pendientes no superen la
cantidad total de la licencia.

`dias_restantes` (property) descuenta de `cortelicencia_dias_pendientes` lo que ya se
usó vía `usos_saldo` (la relación inversa desde `LicenciaPermiso.licenciapermiso_saldo_de_corte`,
sumando solo registros no anulados) — es el número que decide si un corte todavía tiene
algo para ofrecer. `vencido` combina eso con la fecha de vencimiento.

## Firma

```python
class CorteLicencia(models.Model):
```

## Uso real

`CrearCorteLicencia` (`personalizador/views/cortelicenciaviews.py`), enlazada desde la ficha de una `LicenciaPermiso` de tipo Anual/Anual de Invierno.

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
