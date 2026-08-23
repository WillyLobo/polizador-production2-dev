---
symbol: _listar_meses
kind: function
module: secretariador/views/paqueteresolucionesviews.py
lines: 16-67
signature_hash: sha1:6a0811627c6bf537d1bd32f989c664bab13de601
authored: true
---

# _listar_meses

**Módulo:** `secretariador/views/paqueteresolucionesviews.py` (líneas 16-67)

## Propósito

Lee los subdirectorios `{ano}-{mes}/` bajo `DESTINO_PREFIJO` en el bucket de GCS (ver
`secretariador/paquetes_resoluciones.py`, fuera del alcance de este manifest) y arma, para
cada uno, la lista de `paquete-NN.zip`/`paquete-NN.pdf` que contiene — un mes puede tener
uno, otro, o ambos formatos, según qué management command se haya corrido. Ignora blobs
bajo el prefijo `_scratch/` (temporales de una corrida interrumpida). La clave de cada mes
(`{ano}-{mes:02d}`) se arma a mano en vez de dejar que el template la formatee, porque
`USE_THOUSAND_SEPARATOR` con `LANGUAGE_CODE=es-AR` convertiría "2026" en "2.026" al pasar
por el filtro de localización de números, rompiendo el selector CSS del acordeón
Bootstrap que usa esa clave como id de DOM.

## Firma

```python
def _listar_meses(bucket):
```

## Uso real

`PaginaListaPaquetesResoluciones` (mismo módulo, más abajo).

## Ver también

- [PaginaListaPaquetesResoluciones](PaginaListaPaquetesResoluciones.md)
