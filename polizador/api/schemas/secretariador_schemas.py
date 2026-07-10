# secretariador app schemas
from ninja import Schema
from datetime import date
from decimal import Decimal
from typing import Optional


# === InstrumentosLegalesMemorandum ===
class MemorandumOut(Schema):
    id: int
    instrumentolegalmemorandum_tipo: str
    instrumentolegalmemorandum_numero: str
    instrumentolegalmemorandum_ano: str
    instrumentolegalmemorandum_fecha_aprobacion: date
    instrumentolegalmemorandum_descripcion: str
    instrumentolegalmemorandum_str: str

class MemorandumCreate(Schema):
    instrumentolegalmemorandum_tipo: str = "P"
    instrumentolegalmemorandum_numero: str
    instrumentolegalmemorandum_ano: str
    instrumentolegalmemorandum_descripcion: str = ""

class MemorandumUpdate(Schema):
    instrumentolegalmemorandum_tipo: Optional[str] = None
    instrumentolegalmemorandum_numero: Optional[str] = None
    instrumentolegalmemorandum_ano: Optional[str] = None
    instrumentolegalmemorandum_fecha_aprobacion: Optional[date] = None
    instrumentolegalmemorandum_descripcion: Optional[str] = None


# === InstrumentosLegalesResoluciones ===
class ResolucionOut(Schema):
    id: int
    instrumentolegalresoluciones_tipo: str
    instrumentolegalresoluciones_numero: str
    instrumentolegalresoluciones_acta: str
    instrumentolegalresoluciones_ano: str
    instrumentolegalresoluciones_fecha_aprobacion: date
    instrumentolegalresoluciones_descripcion: str
    instrumentolegalresoluciones_str: str

class ResolucionCreate(Schema):
    instrumentolegalresoluciones_tipo: str = "P"
    instrumentolegalresoluciones_numero: str
    instrumentolegalresoluciones_acta: str = ""
    instrumentolegalresoluciones_ano: str
    instrumentolegalresoluciones_descripcion: str = ""

class ResolucionUpdate(Schema):
    instrumentolegalresoluciones_tipo: Optional[str] = None
    instrumentolegalresoluciones_numero: Optional[str] = None
    instrumentolegalresoluciones_acta: Optional[str] = None
    instrumentolegalresoluciones_ano: Optional[str] = None
    instrumentolegalresoluciones_fecha_aprobacion: Optional[date] = None
    instrumentolegalresoluciones_descripcion: Optional[str] = None


# === InstrumentosLegalesDecretos ===
class DecretoOut(Schema):
    id: int
    instrumentolegaldecretos_tipo: str
    instrumentolegaldecretos_numero: str
    instrumentolegaldecretos_ano: str
    instrumentolegaldecretos_fecha_aprobacion: date
    instrumentolegaldecretos_descripcion: str
    instrumentolegaldecretos_str: str

class DecretoCreate(Schema):
    instrumentolegaldecretos_tipo: str = "P"
    instrumentolegaldecretos_numero: str
    instrumentolegaldecretos_ano: str
    instrumentolegaldecretos_descripcion: str = "Escala de viáticos"

class DecretoUpdate(Schema):
    instrumentolegaldecretos_tipo: Optional[str] = None
    instrumentolegaldecretos_numero: Optional[str] = None
    instrumentolegaldecretos_ano: Optional[str] = None
    instrumentolegaldecretos_fecha_aprobacion: Optional[date] = None
    instrumentolegaldecretos_descripcion: Optional[str] = None


# === MontoViaticoDiario ===
class MontoViaticoOut(Schema):
    id: int
    montoviaticodiario_estrato_uno_interior: float
    montoviaticodiario_estrato_dos_interior: float
    montoviaticodiario_estrato_tres_interior: float
    montoviaticodiario_estrato_cuatro_interior: float
    montoviaticodiario_estrato_uno_exterior: float
    montoviaticodiario_estrato_dos_exterior: float
    montoviaticodiario_estrato_tres_exterior: float
    montoviaticodiario_estrato_cuatro_exterior: float
    montoviaticodiario_decreto_reglamentario_id: int

class MontoViaticoCreate(Schema):
    montoviaticodiario_estrato_uno_interior: float = 0.0
    montoviaticodiario_estrato_dos_interior: float = 0.0
    montoviaticodiario_estrato_tres_interior: float = 0.0
    montoviaticodiario_estrato_cuatro_interior: float = 0.0
    montoviaticodiario_estrato_uno_exterior: float = 0.0
    montoviaticodiario_estrato_dos_exterior: float = 0.0
    montoviaticodiario_estrato_tres_exterior: float = 0.0
    montoviaticodiario_estrato_cuatro_exterior: float = 0.0
    montoviaticodiario_decreto_reglamentario_id: int

class MontoViaticoUpdate(Schema):
    montoviaticodiario_estrato_uno_interior: Optional[float] = None
    montoviaticodiario_estrato_dos_interior: Optional[float] = None
    montoviaticodiario_estrato_tres_interior: Optional[float] = None
    montoviaticodiario_estrato_cuatro_interior: Optional[float] = None
    montoviaticodiario_estrato_uno_exterior: Optional[float] = None
    montoviaticodiario_estrato_dos_exterior: Optional[float] = None
    montoviaticodiario_estrato_tres_exterior: Optional[float] = None
    montoviaticodiario_estrato_cuatro_exterior: Optional[float] = None
    montoviaticodiario_decreto_reglamentario_id: Optional[int] = None


# === Comisionado (personalizador.Agente) ===
class ComisionadoOut(Schema):
    id: int
    agente_nombres: str
    agente_apellidos: str
    abreviatura: Optional[str] = None
    sexo_id: int
    oficina_id: Optional[int] = None
    dni: float
    cuil: str

class ComisionadoCreate(Schema):
    agente_nombres: str
    agente_apellidos: str
    abreviatura: str = "Sr."
    sexo_id: int
    oficina_id: Optional[int] = None
    dni: float
    cuil: str

class ComisionadoUpdate(Schema):
    agente_nombres: Optional[str] = None
    agente_apellidos: Optional[str] = None
    abreviatura: Optional[str] = None
    sexo_id: Optional[int] = None
    oficina_id: Optional[int] = None
    dni: Optional[float] = None
    cuil: Optional[str] = None


# === Organigrama ===
class OrganigramaOut(Schema):
    id: int
    organigrama_cargo: str
    organigrama_escalafon: float

class OrganigramaCreate(Schema):
    organigrama_cargo: str
    organigrama_escalafon: float = 2

class OrganigramaUpdate(Schema):
    organigrama_cargo: Optional[str] = None
    organigrama_escalafon: Optional[float] = None


# === Vehiculo ===
class VehiculoOut(Schema):
    id: int
    vehiculo_caracter: str
    vehiculo_modelo: str
    vehiculo_patente: str
    vehiculo_poliza: Optional[str] = None
    vehiculo_poliza_aseguradora_id: Optional[int] = None
    vehiculo_titular_agente_id: Optional[int] = None
    vehiculo_titular_empresa_id: Optional[int] = None
    vehiculo_n_motor: Optional[str] = None
    vehiculo_n_chasis: Optional[str] = None
    vehiculo_modelo_ano: Optional[float] = None

class VehiculoCreate(Schema):
    vehiculo_caracter: str = "O"
    vehiculo_modelo: str
    vehiculo_patente: str
    vehiculo_poliza: Optional[str] = None
    vehiculo_poliza_aseguradora_id: Optional[int] = None
    vehiculo_titular_agente_id: Optional[int] = None
    vehiculo_titular_empresa_id: Optional[int] = None
    vehiculo_n_motor: Optional[str] = None
    vehiculo_n_chasis: Optional[str] = None
    vehiculo_modelo_ano: Optional[float] = None

class VehiculoUpdate(Schema):
    vehiculo_caracter: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    vehiculo_patente: Optional[str] = None
    vehiculo_poliza: Optional[str] = None
    vehiculo_poliza_aseguradora_id: Optional[int] = None
    vehiculo_titular_agente_id: Optional[int] = None
    vehiculo_titular_empresa_id: Optional[int] = None
    vehiculo_n_motor: Optional[str] = None
    vehiculo_n_chasis: Optional[str] = None
    vehiculo_modelo_ano: Optional[float] = None


# === Solicitud ===
class SolicitudOut(Schema):
    id: int
    solicitud_actuacion: str
    solicitud_actuacion_jurisdiccion: str = "E10"
    solicitud_actuacion_numero: float
    solicitud_actuacion_ano: float
    solicitud_solicitante_id: int
    solicitud_provincia_id: int
    solicitud_ciudad: Optional[str] = None
    solicitud_decreto_viaticos_id: int
    solicitud_fecha_desde: date
    solicitud_fecha_hasta: date
    solicitud_tareas: str
    solicitud_vehiculo_id: Optional[int] = None
    solicitud_aereo: Optional[bool] = None
    solicitud_dia_inhabil: bool
    solicitud_resolucion_id: Optional[int] = None
    solicitud_anulada: bool

class SolicitudCreate(Schema):
    solicitud_actuacion_jurisdiccion: str = "E10"
    solicitud_solicitante_id: int
    solicitud_provincia_id: int
    localidad_ids: list[int] = []
    solicitud_ciudad: Optional[str] = None
    solicitud_decreto_viaticos_id: int
    solicitud_fecha_desde: date
    solicitud_fecha_hasta: date
    solicitud_tareas: str
    solicitud_vehiculo_id: Optional[int] = None
    solicitud_aereo: Optional[bool] = None
    solicitud_dia_inhabil: bool = False

class SolicitudUpdate(Schema):
    solicitud_solicitante_id: Optional[int] = None
    solicitud_provincia_id: Optional[int] = None
    localidad_ids: Optional[list[int]] = None
    solicitud_ciudad: Optional[str] = None
    solicitud_decreto_viaticos_id: Optional[int] = None
    solicitud_fecha_desde: Optional[date] = None
    solicitud_fecha_hasta: Optional[date] = None
    solicitud_tareas: Optional[str] = None
    solicitud_vehiculo_id: Optional[int] = None
    solicitud_aereo: Optional[bool] = None
    solicitud_dia_inhabil: Optional[bool] = None
    solicitud_resolucion_id: Optional[int] = None
    solicitud_anulada: Optional[bool] = None


# === ComisionadoSolicitud ===
class ComisionadoSolicitudOut(Schema):
    id: int
    comisionadosolicitud_foreign_id: Optional[int] = None
    comisionadosolicitud_incorporacion_foreign_id: Optional[int] = None
    comisionadosolicitud_nombre_id: int
    comisionadosolicitud_colaborador: bool
    comisionadosolicitud_chofer: bool
    comisionadosolicitud_combustible: Optional[Decimal] = None
    comisionadosolicitud_pasaje: Optional[Decimal] = None
    comisionadosolicitud_gastos: Optional[Decimal] = None
    comisionadosolicitud_sin_viatico: bool

class ComisionadoSolicitudCreate(Schema):
    comisionadosolicitud_foreign_id: Optional[int] = None
    comisionadosolicitud_incorporacion_foreign_id: Optional[int] = None
    comisionadosolicitud_nombre_id: int
    comisionadosolicitud_colaborador: bool = False
    comisionadosolicitud_chofer: bool = False
    comisionadosolicitud_combustible: Decimal = Decimal("0.0")
    comisionadosolicitud_pasaje: Decimal = Decimal("0.0")
    comisionadosolicitud_gastos: Decimal = Decimal("0.0")
    comisionadosolicitud_sin_viatico: bool = False

class ComisionadoSolicitudUpdate(Schema):
    comisionadosolicitud_foreign_id: Optional[int] = None
    comisionadosolicitud_incorporacion_foreign_id: Optional[int] = None
    comisionadosolicitud_nombre_id: Optional[int] = None
    comisionadosolicitud_colaborador: Optional[bool] = None
    comisionadosolicitud_chofer: Optional[bool] = None
    comisionadosolicitud_combustible: Optional[Decimal] = None
    comisionadosolicitud_pasaje: Optional[Decimal] = None
    comisionadosolicitud_gastos: Optional[Decimal] = None
    comisionadosolicitud_sin_viatico: Optional[bool] = None


# === Incorporacion ===
class IncorporacionOut(Schema):
    id: int
    incorporacion_solicitud_id: int
    incorporacion_actuacion: str
    incorporacion_actuacion_jurisdiccion: str = "E10"
    incorporacion_actuacion_numero: float
    incorporacion_actuacion_ano: float
    incorporacion_solicitante_id: int
    incorporacion_resolucion_id: Optional[int] = None

class IncorporacionCreate(Schema):
    incorporacion_solicitud_id: int
    incorporacion_actuacion_jurisdiccion: str = "E10"
    incorporacion_solicitante_id: int
    incorporacion_resolucion_id: Optional[int] = None

class IncorporacionUpdate(Schema):
    incorporacion_solicitud_id: Optional[int] = None
    incorporacion_solicitante_id: Optional[int] = None
    incorporacion_resolucion_id: Optional[int] = None
