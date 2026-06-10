"""
Script para comunicarse con las APIs públicas del Banco Central de la República Argentina (BCRA).

APIs cubiertas:
  - Estadísticas Cambiarias v1.0
  - Estadísticas Monetarias v4.0
  - Central de Deudores v1.0
  - Cheques Denunciados v1.0
  - Régimen de Transparencia v1.0

Documentación oficial: https://www.bcra.gob.ar/apis-banco-central/
Base URL: https://api.bcra.gob.ar
"""

import requests
from datetime import date, timedelta
from typing import Optional


BASE_URL = "https://api.bcra.gob.ar"
DEFAULT_TIMEOUT = 30


class BCRAError(Exception):
    """Excepción base para errores de la API del BCRA."""


class BCAPI:
    """Cliente Python para las APIs públicas del BCRA."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _url(path: str) -> str:
        return f"{BASE_URL}{path}"

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        url = self._url(path)
        resp = self.session.get(url, params=params, timeout=self.timeout)
        if resp.status_code == 404:
            raise BCRAError(f"Endpoint no encontrado: {resp.url}")
        resp.raise_for_status()
        return resp.json()

    # -------------------------------------------------------------------------
    # Estadísticas Cambiarias v1.0
    # -------------------------------------------------------------------------

    def get_divisas(self) -> dict:
        """Lista todas las monedas ISO vigentes con su denominación."""
        return self._get("/estadisticascambiarias/v1.0/Maestros/Divisas")

    def get_cotizaciones(self, fecha: Optional[str] = None) -> dict:
        """Retorna cotizaciones de divisas del BCRA para una fecha.

        Args:
            fecha: Fecha en formato YYYY-MM-DD (default: última disponible).
        """
        params = {"fecha": fecha} if fecha else None
        return self._get("/estadisticascambiarias/v1.0/Cotizaciones", params=params)

    def get_evolucion_moneda(
        self,
        moneda: str,
        desde: Optional[str] = None,
        hasta: Optional[str] = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> dict:
        """Evolución de cotización de una moneda en un rango de fechas.

        Args:
            moneda: Código ISO (ej: "USD", "EUR", "BRL").
            desde: Fecha inicio YYYY-MM-DD (default: primera de la serie).
            hasta: Fecha fin YYYY-MM-DD (default: última de la serie).
            limit: Max registros (10-1000).
            offset: Paginado.
        """
        params = {"limit": min(max(limit, 10), 1000), "offset": offset}
        if desde:
            params["fechaDesde"] = desde
        if hasta:
            params["fechaHasta"] = hasta
        return self._get(f"/estadisticascambiarias/v1.0/Cotizaciones/{moneda}", params=params)

    # -------------------------------------------------------------------------
    # Estadísticas Monetarias v4.0
    # -------------------------------------------------------------------------

    def get_variables(
        self,
        id_variable: Optional[int] = None,
        categoria: Optional[str] = None,
        periodicidad: Optional[str] = None,
        offset: int = 0,
        limit: int = 1000,
    ) -> dict:
        """Lista las variables monetarias del BCRA (reservas, tipo de cambio, inflación, etc.).

        Args:
            id_variable: Filtra por ID.
            categoria: ej "Principales Variables".
            periodicidad: D (diaria), M (mensual), T/Q (trimestral).
            offset: Paginado.
            limit: Max registros (max 1000).
        """
        params = {"Offset": offset, "Limit": min(max(limit, 1), 1000)}
        if id_variable is not None:
            params["IdVariable"] = id_variable
        if categoria:
            params["Categoria"] = categoria
        if periodicidad:
            params["Periodicidad"] = periodicidad
        return self._get("/estadisticas/v4.0/Monetarias", params=params)

    def get_variable_historico(
        self,
        id_variable: int,
        desde: Optional[str] = None,
        hasta: Optional[str] = None,
        offset: int = 0,
        limit: int = 1000,
    ) -> dict:
        """Historial de una variable monetaria en un rango de fechas.

        Args:
            id_variable: ID obtenido de get_variables().
            desde: YYYY-MM-DD (default: primera fecha).
            hasta: YYYY-MM-DD (default: última fecha).
            offset: Paginado.
            limit: Max registros (max 3000).
        """
        params = {"Offset": offset, "Limit": min(max(limit, 1), 3000)}
        if desde:
            params["Desde"] = desde
        if hasta:
            params["Hasta"] = hasta
        return self._get(f"/estadisticas/v4.0/Monetarias/{id_variable}", params=params)

    # -------------------------------------------------------------------------
    # Central de Deudores v1.0
    # -------------------------------------------------------------------------

    def get_deudores(self, identificacion: str) -> dict:
        """Situación crediticia actual de una persona o empresa (deuda, días atraso, entidad).

        Args:
            identificacion: CUIT/CUIL/CDI de 11 dígitos sin guiones ni espacios.
        """
        return self._get(f"/centraldedeudores/v1.0/Deudas/{identificacion}")

    def get_deudores_historico(self, identificacion: str) -> dict:
        """Historial crediticio últimos 24 meses.

        Args:
            identificacion: CUIT/CUIL/CDI de 11 dígitos sin guiones ni espacios.
        """
        return self._get(f"/centraldedeudores/v1.0/Deudas/Historicas/{identificacion}")

    def get_cheques_rechazados(self, identificacion: str) -> dict:
        """Cheques rechazados y causales para un CUIT/CUIL/CDI.

        Args:
            identificacion: CUIT/CUIL/CDI de 11 dígitos sin guiones ni espacios.
        """
        return self._get(f"/centraldedeudores/v1.0/Deudas/ChequesRechazados/{identificacion}")

    # -------------------------------------------------------------------------
    # Cheques Denunciados v1.0
    # -------------------------------------------------------------------------

    def get_entidades(self) -> dict:
        """Lista todas las entidades bancarias con su código."""
        return self._get("/cheques/v1.0/entidades")

    def get_cheque(self, codigo_entidad: int, numero_cheque: int) -> dict:
        """Consulta si un cheque está registrado como denunciado.

        Args:
            codigo_entidad: Código de la entidad (ver get_entidades()).
            numero_cheque: Número del cheque.
        """
        return self._get(f"/cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}")

    # -------------------------------------------------------------------------
    # Régimen de Transparencia v1.0
    # -------------------------------------------------------------------------

    def get_cajas_ahorro(self, codigo_entidad: Optional[int] = None) -> dict:
        """Cajas de ahorro (opcionalmente filtra por entidad)."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/CajasAhorros", params=params)

    def get_paquetes_productos(self, codigo_entidad: Optional[int] = None) -> dict:
        """Paquetes de productos ofrecidos por entidades."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/PaquetesProductos", params=params)

    def get_plazos_fijos(self, codigo_entidad: Optional[int] = None) -> dict:
        """Tasas y condiciones de plazos fijos."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/PlazosFijos", params=params)

    def get_prestamos_prendarios(self, codigo_entidad: Optional[int] = None) -> dict:
        """Tasas y condiciones de préstamos prendarios."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/Prestamos/Prendarios", params=params)

    def get_prestamos_hipotecarios(self, codigo_entidad: Optional[int] = None) -> dict:
        """Tasas y condiciones de préstamos hipotecarios."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/Prestamos/Hipotecarios", params=params)

    def get_prestamos_personales(self, codigo_entidad: Optional[int] = None) -> dict:
        """Tasas y condiciones de préstamos personales."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/Prestamos/Personales", params=params)

    def get_tarjetas_credito(self, codigo_entidad: Optional[int] = None) -> dict:
        """Tasas y condiciones de tarjetas de crédito."""
        params = {"codigoEntidad": codigo_entidad} if codigo_entidad else None
        return self._get("/transparencia/v1.0/TarjetasCredito", params=params)

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def close(self):
        """Cierra la sesión HTTP."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# =============================================================================
# Funciones de conveniencia (sin instanciar clase)
# =============================================================================

def get_cotizacion_hoy(moneda: str = "USD") -> dict:
    """Obtiene la cotización del día actual para una moneda.

    Usage:
        data = get_cotizacion_hoy("USD")
        print(data["fecha"], data["cotizacion"])  # ejemplo
    """
    hoy = date.today().isoformat()
    with BCAPI() as client:
        cotizaciones = client.get_cotizaciones(hoy)
    for c in cotizaciones.get("Cotizaciones", []):
        if c.get("Moneda") == moneda or c.get("CodigoMoneda") == moneda:
            return c
    raise BCRAError(f"Cotización no encontrada para {moneda} en {hoy}")


def get_cotizaciones_del_dia() -> list[dict]:
    """Retorna todas las cotizaciones del día actual."""
    hoy = date.today().isoformat()
    with BCAPI() as client:
        return client.get_cotizaciones(hoy).get("Cotizaciones", [])


def get_evolucion_usd_mes_actual(limit: int = 1000) -> list[dict]:
    """Evolución del USD en el mes actual."""
    hoy = date.today()
    primer_dia = hoy.replace(day=1).isoformat()
    with BCAPI() as client:
        resp = client.get_evolucion_moneda("USD", desde=primer_dia, hasta=hoy.isoformat(), limit=limit)
    return resp.get("Cotizaciones", [])


if __name__ == "__main__":
    import json

    def _dump(obj, label: str):
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
        if isinstance(obj, dict):
            keys = list(obj.keys())[:10]
            for k in keys:
                val = obj[k]
                if isinstance(val, (list, dict)):
                    print(f"  {k}: [{len(val) if isinstance(val, list) else '...'} items]")
                else:
                    print(f"  {k}: {val}")
        elif isinstance(obj, list):
            print(f"  {len(obj)} items")
            for item in obj[:3]:
                print(f"    - {json.dumps(item, ensure_ascii=False)[:200]}")

    with BCAPI() as client:
        # 1. Monedas ISO vigentes
        _dump(client.get_divisas(), "Monedas ISO (Divisas)")

        # 2. Cotizaciones de hoy
        cotizaciones = client.get_cotizaciones()
        _dump(cotizaciones, f"Cotizaciones del dia ({cotizaciones.get('Fecha', 'N/A')})")

        # 3. Evolución USD (ultimo mes)
        hoy = date.today()
        hoy_str = hoy.isoformat()
        desde = hoy.replace(day=1).isoformat()
        evolucion = client.get_evolucion_moneda("USD", desde=desde, hasta=hoy_str, limit=60)
        _dump(evolucion, "Evolución USD (mes actual)")

        # 4. Variables monetarias disponibles
        variables = client.get_variables(limit=50)
        _dump(variables, "Variables Monetarias")

        # 5. Entidades bancarias (para cheques denunciados)
        entidades = client.get_entidades()
        _dump(entidades, "Entidades Bancarias")
