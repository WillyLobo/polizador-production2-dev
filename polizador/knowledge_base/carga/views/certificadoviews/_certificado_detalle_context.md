---
symbol: _certificado_detalle_context
kind: function
module: carga/views/certificadoviews.py
lines: 82-180
signature_hash: sha1:b0f00805287e16bfc91b1eebad57c15879e7d77a
authored: true
---

# _certificado_detalle_context

**Módulo:** `carga/views/certificadoviews.py` (líneas 82-180)

## Propósito

El contexto completo de la ficha/impresión de un Certificado: financiamiento, plan
vigente, todos los `ContratoMonto` del Contrato relevante (el de origen si es Hecho
Consumado — elegido a mano, no necesariamente el vigente de la obra — o el vigente para
PARCIAL/ANTICIPO), el monto/incidencia % de este certificado dentro de su financiamiento,
el desglose por ítem ([_desglose_items_certificado](_desglose_items_certificado.md)), el
detalle de tramos Ley 27397 con sus montos recalculados, la cotización UVI efectivamente
usada, y los firmantes institucionales (Gerente Operativo, Directora de Certificaciones,
Jefe de Certificaciones) resueltos desde `personalizador.Directorio/Gerencia/Departamento`
por nombre fijo — no por configuración, así que un rename de esos cargos en RRHH rompería
silenciosamente esta función.

## Firma

```python
def _certificado_detalle_context(certificado):
```

## Uso real

`DetalleCertificado.get_context_data` / `ImprimirCertificado.get_context_data` (mismo módulo, más abajo).

## Ver también

- [Certificado](../../models/Certificado.md)
- [DetalleCertificado](DetalleCertificado.md)
