# secretariador app schemas - generated from Django models
from pydantic import BaseModel
from typing import Optional


# === InstrumentosLegalesMemorandum ===
class MemoruandOut(BaseModel):
    id: int
    instrumentolegalmemorandum_tipo: str
    instrumentolegalmemorandum_numero: str
    instrumentolegalmemorandum_ano: str
    instrumentolegalmemorandum_fecha_aprobacion: str
    instrumentolegalmemorandum_descripcion: str
    instrumentolegalmemorandum_str: str

class MemorandCreate(BaseModel):
    instrumentolegalmemorandum_tipo: str = "P"
    instrumentolegalmemorandum_numero: str
    instrumentolegalmemorandum_ano: str
    instrumentolegalmemorandum_descripcion: str = ""

class MemorandUpdate(BaseModel):
    instrumentolegalmemorandum_tipo: Optional[str] = None
    instrumentolegalmemorandum_numero: Optional[str] = None
    instrumentolegalmemorandum_ano: Optional[str] = None
    instrumentolegalmemorandum_fecha_aprobacion: Optional[str] = None
    instrumentolegalmemorandum_descripcion: Optional[str] = None


# === InstrumentosLegalesResoluciones ===
class ResolucionOut(BaseModel):
    id: int
    instrumentolegalresoluciones_tipo: str
    instrumentolegalresoluciones_numero: str
    instrumentolegalresoluciones_acta: str
    instrumentolegalresoluciones_ano: str
    instrumentolegalresoluciones_fecha_aprobacion: str
    instrumentolegalresoluciones_descripcion: str
    instrumentolegalresoluciones_str: str

class ResolucionCreate(BaseModel):
    instrumentolegalresoluciones_tipo: str = "P"
    instrumentolegalresoluciones_numero: str
    instrumentolegalresoluciones_acta: str = ""
    instrumentolegalresoluciones_ano: str
    instrumentolegalresoluciones_descripcion: str = ""

class ResolucionUpdate(BaseModel):
    instrumentolegalresoluciones_tipo: Optional[str] = None
    instrumentolegalresoluciones_numero: Optional[str] = None
    instrumentolegalresoluciones_acta: Optional[str] = None
    instrumentolegalresoluciones_ano: Optional[str] = None
    instrumentolegalresoluciones_fecha_aprobacion: Optional[str] = None
    instrumentolegalresoluciones_descripcion: Optional[str] = None


# === InstrumentosLegalesResolucionesDirectorio ===
class ResolucionDirOut(BaseModel):
    id: int
    instrumentolegalresolucionesdirectorio_tipo: str
    instrumentolegalresolucionesdirectorio_numero: str
    instrumentolegalresolucionesdirectorio_acta: str
    instrumentolegalresolucionesdirectorio_ano: str
    instrumentolegalresolucionesdirectorio_fecha_aprobacion: str
    instrumentolegalresolucionesdirectorio_descripcion: str
    instrumentolegalresolucionesdirectorio_str: str

class ResolucionDirCreate(BaseModel):
    instrumentolegalresolucionesdirectorio_tipo: str = "D"
    instrumentolegalresolucionesdirectorio_numero: str
    instrumentolegalresolucionesdirectorio_acta: str = ""
    instrumentolegalresolucionesdirectorio_ano: str
    instrumentolegalresolucionesdirectorio_descripcion: str = ""

class ResolucionDirUpdate(BaseModel):
    instrumentolegalresolucionesdirectorio_tipo: Optional[str] = None
    instrumentolegalresolucionesdirectorio_numero: Optional[str] = None
    instrumentolegalresolucionesdirectorio_acta: Optional[str] = None
    instrumentolegalresolucionesdirectorio_ano: Optional[str] = None
    instrumentolegalresolucionesdirectorio_fecha_aprobacion: Optional[str] = None
    instrumentolegalresolucionesdirectorio_descripcion: Optional[str] = None


# === InstrumentosLegalesDecretos ===
class DecretoOut(BaseModel):
    id: int
    instrumentolegaldecretos_tipo: str
    instrumentolegaldecretos_numero: str
    instrumentolegaldecretos_ano: str
    instrumentolegaldecretos_fecha_aprobacion: str
    instrumentolegaldecretos_descripcion: str
    instrumentolegaldecretos_str: str

class DecretoCreate(BaseModel):
    instrumentolegaldecretos_tipo: str = "P"
    instrumentolegaldecretos_numero: str
    instrumentolegaldecretos_ano: str
    instrumentolegaldecretos_descripcion: str = "Escala de viáticos"

class DecretoUpdate(BaseModel):
    instrumentolegaldecretos_tipo: Optional[str] = None
    instrumentolegaldecretos_numero: Optional[str] = None
    instrumentolegaldecretos_ano: Optional[str] = None
    instrumentolegaldecretos_fecha_aprobacion: Optional[str] = None
    instrumentolegaldecretos_descripcion: Optional[str] = None


# === MontoViaticoDiario ===
class MontoViaticoOut(BaseModel):
    id: int
    montoviaticodiario_estrato_uno_interior: float
    montoviaticodiario_estrato_dos_interior: float
    montoviaticodiario_estrato_tres_interior: float
    montoviaticodiario_estrato_cuatro_interior: float
    montoviaticodiario_estrato_uno_exterior: float
    montoviaticodiario_estrato_dos_exterior: float
    montoviaticodiario_estrato_tres_exterior: float
    montoviaticodiario_estrato_cuatro_exterior: float
    decreto_reglamentario_id: int

class MontoViaticoCreate(BaseModel):
    monto_viatico_uno_interior: float = 0.0
    monto_viatico_dos_interior: float = 0.0
    monto_viatico_tres_interior: float = 0.0
    monto_viatico_cuatro_interior: float = 0.0
    monto_viatico_uno_exterior: float = 0.0
    monto_viatico_dos_exterior: float = 0.0
    monto_viatico_tres_exterior: float = 0.0
    monto_viatico_cuatro_exterior: float = 0.0
    decreto_reglamentario_id: int

class MontoViaticoUpdate(BaseModel):
    monto_viatico_uno_interior: Optional[float] = None
    monto_viatico_dos_interior: Optional[float] = None
    monto_viatico_tres_interior: Optional[float] = None
    monto_viatico_cuatro_interior: Optional[float] = None
    monto_viatico_uno_exterior: Optional[float] = None
    monto_viatico_dos_exterior: Optional[float] = None
    monto_viatico_tres_exterior: Optional[float] = None
    monto_viatico_cuatro_exterior: Optional[float] = None


# === Comisionado (personalizador.Agente) ===
class ComisionadoOut(BaseModel):
    id: int
    comisionado_nombres: str
    comisionado_apellidos: str
    comisionado_abreviatura: str
    sexo_id: int
    oficina_id: Optional[int] = None
    dni: float
    cuil: str

class ComisionadoCreate(BaseModel):
    comisionado_nombres: str
    comisionado_apellidos: str
    comisionado_abreviatura: str = "Sr."
    sexo_id: int
    oficina_id: Optional[int] = None
    dni: float
    cuil: str

class ComisionadoUpdate(BaseModel):
    comisionado_nombres: Optional[str] = None
    comisionado_apellidos: Optional[str] = None
    comisionado_abreviatura: Optional[str] = None
    sexo_id: Optional[int] = None
    oficina_id: Optional[int] = None
    dni: Optional[float] = None
    cuil: Optional[str] = None


# === Organigrama ===
class OrganigramaOut(BaseModel):
    id: int
    organigrama_cargo: str
    organigrama_escalafon: float

class OrganigramaCreate(BaseModel):
    organigrama_cargo: str
    organigrama_escalafon: float = 2

class OrganigramaUpdate(BaseModel):
    organigrama_cargo: Optional[str] = None
    organigrama_escalafon: Optional[float] = None


# === Vehiculo ===
class VehiculoOut(BaseModel):
    id: int
    vehiculo_caracter: str
    vehiculo_modelo: str
    vehiculo_patente: str
    vehiculo_poliza: Optional[str] = None
    poliza_aseguradora_id: Optional[int] = None
    titular_agente_id: Optional[int] = None
    titular_empresa_id: Optional[int] = None
    n_motor: Optional[str] = None
    n_chasis: Optional[str] = None
    modelo_ano: Optional[float] = None

class VehiculoCreate(BaseModel):
    vehiculo_caracter: str = "O"
    vehiculo_modelo: str
    vehiculo_patente: str
    vehiculo_poliza: Optional[str] = None
    poliza_aseguradora_id: Optional[int] = None
    titular_agente_id: Optional[int] = None
    titular_empresa_id: Optional[int] = None
    n_motor: Optional[str] = None
    n_chasis: Optional[str] = None
    modelo_ano: Optional[float] = None

class VehiculoUpdate(BaseModel):
    vehiculo_caracter: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    vehiculo_patente: Optional[str] = None
    vehiculo_poliza: Optional[str] = None
    poliza_aseguradora_id: Optional[int] = None
    titular_agente_id: Optional[int] = None
    titular_empresa_id: Optional[int] = None
    n_motor: Optional[str] = None
    n_chasis: Optional[str] = None
    modelo_ano: Optional[float] = None


# === Solicitud ===
class SolicitudOut(BaseModel):
    id: int
    solicitud_actuacion: str
    actuacion_jurisdiccion: str = "E10"
    actuacion_numero: float
    actuacion_ano: float
    solicitante_id: int
    provincia_id: int
    localidad_ids: list[int] = []
    ciudad: Optional[str] = None
    decreto_viaticos_id: int
    fecha_desde: str
    fecha_hasta: str
    tareas: str
    vehiculo_id: Optional[int] = None
    aereo: Optional[bool] = None
    dia_inhabil: bool
    resolucion_id: Optional[int] = None

class SolicitudCreate(BaseModel):
    solicitante_id: int
    provincia_id: int
    localidad_ids: list[int] = []
    ciudad: Optional[str] = None
    decreto_viaticos_id: int
    fecha_desde: str
    fecha_hasta: str
    tareas: str
    vehiculo_id: Optional[int] = None
    aereo: Optional[bool] = None
    dia_inhabil: bool

class SolicitudUpdate(BaseModel):
    solicitante_id: Optional[int] = None
    provincia_id: Optional[int] = None
    localidad_ids: Optional[list[int]] = None
    ciudad: Optional[str] = None
    decreto_viaticos_id: Optional[int] = None
    fecha_desde: Optional[str] = None
    fecha_hasta: Optional[str] = None
    tareas: Optional[str] = None
    vehiculo_id: Optional[int] = None
    aereo: Optional[bool] = None
    dia_inhabil: Optional[bool] = None


# === ComisionadoSolicitud ===
class ComisionadoSolicitudOut(BaseModel):
    id: int
    solicitud_foreign_id: Optional[int] = None
    incorporacion_foreign_id: Optional[int] = None
    comisionado_id: int
    colaborador: bool
    chofer: bool
    combustible: float
    pasaje: float
    gastos: float
    sin_viatico: bool

class ComisionadoSolicitudCreate(BaseModel):
    solicitud_foreign_id: Optional[int] = None
    incorporacion_foreign_id: Optional[int] = None
    comisionado_id: int
    colaborador: bool = False
    chofer: bool = False
    combustible: float = 0.0
    pasaje: float = 0.0
    gastos: float = 0.0
    sin_viatico: bool = False

class ComisionadoSolicitudUpdate(BaseModel):
    solicitud_foreign_id: Optional[int] = None
    incorporacion_foreign_id: Optional[int] = None
    comisionado_id: Optional[int] = None
    colaborador: Optional[bool] = None
    chofer: Optional[bool] = None
    combustible: Optional[float] = None
    pasaje: Optional[float] = None
    gastos: Optional[float] = None
    sin_viatico: Optional[bool] = None


# === Incorporacion ===
class IncorporacionOut(BaseModel):
    id: int
    solicitud_id: int
    actuacion: str
    solicitante_id: int
    resolucion_id: Optional[int] = None

class IncorporacionCreate(BaseModel):
    solicitud_id: int
    solicitante_id: int
    resolucion_id: Optional[int] = None

class IncorporacionUpdate(BaseModel):
    solicitud_id: Optional[int] = None
    solicitante_id: Optional[int] = None
    resolucion_id: Optional[int] = None
