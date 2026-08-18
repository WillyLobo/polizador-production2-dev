---
symbol: obras_con_acumulado_anotado
kind: function
module: carga/models.py
lines: 546-558
signature_hash: sha1:6cf6bfc962f51195118d72edababba887d65d071
authored: true
---

# obras_con_acumulado_anotado

**Módulo:** `carga/models.py` (líneas 546-558)

## Propósito

Anota en una sola query (vía `Subquery`) el % acumulado del último Certificado de avance y
el % acumulado de Anticipo del último Certificado de Anticipo de cada Obra del queryset —
pensada para listados de Obras que necesitan mostrar esos dos números sin un N+1 (una
query de Certificado por Obra listada).

**Advertencia real, no hipotética:** está importada en `carga/views/obraviews.py` pero
ningún lugar de ese archivo la está llamando actualmente (`grep` no encuentra
`obras_con_acumulado_anotado(` en el código, solo el import). O quedó de una versión
anterior de la lista de Obras que la usaba y se dejó de usar sin limpiar el import, o está
pensada para una vista que todavía no la adoptó — antes de reusarla, confirmá si el
listado que la necesita sigue haciendo el cálculo por otro lado (ej. `ultimo_certificado_avance()`
llamado por fila, que sí es un N+1).

## Firma

```python
def obras_con_acumulado_anotado(queryset):
```

## Uso real

Ninguno vivo detectado — ver la advertencia arriba.

## Ver también

- [Obra](Obra.md)
- [Certificado](Certificado.md)
