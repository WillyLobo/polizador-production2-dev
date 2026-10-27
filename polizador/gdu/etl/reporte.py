import csv
from collections import Counter, defaultdict
from dataclasses import dataclass, field

# Una incidencia de tipo DESCARTE significa que la fila no se cargó; ADVERTENCIA,
# que se cargó pero algo merece revisión (dato no clasificable, duplicado, etc.).
DESCARTE = "descarte"
ADVERTENCIA = "advertencia"


@dataclass
class ResumenTabla:
    origen: str
    destino: str
    leidas: int = 0
    cargadas: int = 0
    incidencias: Counter = field(default_factory=Counter)


class Reporte:
    """Reporte de conciliación de una corrida del ETL: conteos origen/destino por tabla
    y la lista completa de incidencias (en CSV, para revisarla con el área)."""

    def __init__(self):
        self.tablas = {}
        self.filas = []
        self.notas = []

    def tabla(self, origen, destino):
        return self.tablas.setdefault(destino, ResumenTabla(origen, destino))

    def incidencia(self, destino, id_legacy, tipo, motivo, detalle=""):
        self.tablas[destino].incidencias[(tipo, motivo)] += 1
        self.filas.append((destino, id_legacy, tipo, motivo, detalle))

    def nota(self, texto):
        self.notas.append(texto)

    @property
    def descartes(self):
        return sum(1 for f in self.filas if f[2] == DESCARTE)

    def escribir_csv(self, ruta):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["tabla", "id_legacy", "tipo", "motivo", "detalle"])
            writer.writerows(self.filas)

    def markdown(self):
        lineas = [
            "# Reporte de conciliación ETL GDU", "",
            "| destino | origen | leídas | cargadas | descartes | advertencias |",
            "|---|---|---:|---:|---:|---:|",
        ]
        for t in self.tablas.values():
            descartes = sum(n for (tipo, _), n in t.incidencias.items() if tipo == DESCARTE)
            advertencias = sum(n for (tipo, _), n in t.incidencias.items() if tipo == ADVERTENCIA)
            lineas.append(f"| {t.destino} | {t.origen} | {t.leidas} | {t.cargadas} | {descartes} | {advertencias} |")

        por_tabla = defaultdict(list)
        for t in self.tablas.values():
            for (tipo, motivo), n in sorted(t.incidencias.items(), key=lambda x: -x[1]):
                por_tabla[t.destino].append(f"- {tipo}: {motivo} ({n})")
        if por_tabla:
            lineas += ["", "## Incidencias por tabla", ""]
            for destino, items in por_tabla.items():
                lineas += [f"### {destino}", *items, ""]
        if self.notas:
            lineas += ["## Notas", "", *[f"- {n}" for n in self.notas], ""]
        return "\n".join(lineas)
