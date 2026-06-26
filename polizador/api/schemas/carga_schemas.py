# carga app schemas - generated from Django models
from django.db import models as dj_models
from decimal import Decimal, InvalidOperation
from pydantic import BaseModel, field_validator
from typing import Optional
import uuid


def _decimal_field(name: str) -> type:
    """Create a pydantic field for a Django DecimalField."""
    return float  # pydantic handles coercion

def _uuid_default():
    try:
        from uuid_utils.compat import uuid7 as _u7
        return _u7()
    except ImportError:
        return uuid.uuid4()


# === Receptor ===
class ReceptorOut(BaseModel):
    id: int
    receptor_nombre: str
    receptor_uuid: str

class ReceptorCreate(BaseModel):
    receptor_nombre: str

class ReceptorUpdate(BaseModel):
    receptor_nombre: Optional[str] = None

# === Area ===
class AreaOut(BaseModel):
    id: int
    area_uuid: str
    area_nombre: str

class AreaCreate(BaseModel):
    area_nombre: str

class AreaUpdate(BaseModel):
    area_nombre: Optional[str] = None

# === Aseguradora ===
class AseguradoraOut(BaseModel):
    id: int
    aseguradora_uuid: str
    aseguradora_nombre: str

class AseguradoraCreate(BaseModel):
    aseguradora_nombre: str

class AseguradoraUpdate(BaseModel):
    aseguradora_nombre: Optional[str] = None

# === Empresa ===
class EmpresaOut(BaseModel):
    id: int
    empresa_uuid: str
    empresa_nombre: str
    empresa_cuit: Optional[str] = None
    empresa_titular_titulo: Optional[str] = None
    empresa_titular_nombre: Optional[str] = None
    empresa_titular_dni: Optional[float] = None
    empresa_direccion: Optional[str] = None
    empresa_inscripcion: Optional[str] = None
    empresa_correo_p: Optional[str] = None
    empresa_correo_s: Optional[str] = None

class EmpresaCreate(BaseModel):
    empresa_nombre: str
    empresa_cuit: Optional[str] = None
    empresa_titular_titulo: Optional[str] = None
    empresa_titular_nombre: Optional[str] = None
    empresa_titular_dni: Optional[float] = None
    empresa_direccion: Optional[str] = None
    empresa_inscripcion: Optional[str] = None
    empresa_correo_p: Optional[str] = None
    empresa_correo_s: Optional[str] = None

class EmpresaUpdate(BaseModel):
    empresa_nombre: Optional[str] = None
    empresa_cuit: Optional[str] = None
    empresa_titular_titulo: Optional[str] = None
    empresa_titular_nombre: Optional[str] = None
    empresa_titular_dni: Optional[float] = None
    empresa_direccion: Optional[str] = None
    empresa_inscripcion: Optional[str] = None
    empresa_correo_p: Optional[str] = None
    empresa_correo_s: Optional[str] = None

# === Programa ===
class ProgramaOut(BaseModel):
    id: int
    programa_uuid: str
    programa_nombre: str

class ProgramaCreate(BaseModel):
    programa_nombre: str

class ProgramaUpdate(BaseModel):
    programa_nombre: Optional[str] = None

# === Provincia (manual PK) ===
class ProvinciaOut(BaseModel):
    id: int
    provincia_uuid: str
    provincia_nombre: str

class ProvinciaCreate(BaseModel):
    provincia_nombre: str

class ProvinciaUpdate(BaseModel):
    provincia_nombre: Optional[str] = None

# === Region ===
class RegionOut(BaseModel):
    id: int
    region_uuid: str
    region_numero: str

class RegionCreate(BaseModel):
    region_numero: str

class RegionUpdate(BaseModel):
    region_numero: Optional[str] = None

# === Departamento (manual PK) ===
class DepartamentoCargaOut(BaseModel):
    id: int
    departamento_uuid: str
    departamento_nombre: str

class DepartamentoCargaCreate(BaseModel):
    departamento_nombre: str

class DepartamentoCargaUpdate(BaseModel):
    departamento_nombre: Optional[str] = None

# === Municipio (manual PK) ===
class MunicipioOut(BaseModel):
    id: int
    municipio_uuid: str
    municipio_nombre: str
    municipio_departamento: Optional[int] = None
    municipio_region: Optional[int] = None

class MunicipioCreate(BaseModel):
    municipio_nombre: str
    municipio_departamento: Optional[int] = None
    municipio_region: Optional[int] = None

class MunicipioUpdate(BaseModel):
    municipio_nombre: Optional[str] = None
    municipio_departamento: Optional[int] = None
    municipio_region: Optional[int] = None

# === Localidad (manual PK) ===
class LocalidadOut(BaseModel):
    id: int
    localidad_uuid: str
    localidad_nombre: str
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento: Optional[int] = None
    localidad_municipio: Optional[int] = None

class LocalidadCreate(BaseModel):
    localidad_nombre: str
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento: Optional[int] = None
    localidad_municipio: Optional[int] = None

class LocalidadUpdate(BaseModel):
    localidad_nombre: Optional[str] = None
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento: Optional[int] = None
    localidad_municipio: Optional[int] = None

# === Obra ===
class ObraOut(BaseModel):
    id: int
    obra_uuid: str
    obra_nombre: str
    obra_soluciones: Optional[float] = None
    empresa_nombre: Optional[str] = None
    region_numero: Optional[str] = None
    departamento_ids: list[int] = []
    municipio_ids: list[int] = []
    localidad_ids: list[int] = []
    conjunto_id: Optional[int] = None
    grupo: Optional[str] = None
    plazo: Optional[str] = None
    programa_nombre: Optional[str] = None
    convenio: Optional[str] = None
    expediente: str
    resolucion: Optional[str] = None
    licitacion_tipo: Optional[str] = None
    licitacion_numero: Optional[float] = None
    licitacion_ano: Optional[float] = None
    nomenclatura: Optional[str] = None
    nomenclatura_plano: Optional[str] = None
    fecha_entrega: Optional[str] = None
    fecha_contrato: Optional[str] = None
    expediente_costo: Optional[str] = None
    inspector_ids: list[int] = []
    observaciones: Optional[str] = None
    contrato_nacion_pesos: float = 0.0
    contrato_nacion_uvi: float = 0.0
    contrato_nacion_uvi_fecha: Optional[str] = None
    contrato_provincia_pesos: float = 0.0
    contrato_provincia_uvi: float = 0.0
    contrato_total_pesos: float = 0.0

class ObraCreate(BaseModel):
    obra_nombre: str
    obra_soluciones: Optional[float] = None
    empresa_id: int
    region_id: Optional[int] = None
    departamento_ids: list[int] = []
    municipio_ids: list[int] = []
    localidad_ids: list[int] = []
    conjunto_id: Optional[int] = None
    grupo: Optional[str] = None
    plazo: Optional[str] = None
    programa_id: int
    convenio: Optional[str] = None
    expediente: str
    resolucion: Optional[str] = None
    licitacion_tipo: Optional[str] = None
    licitacion_numero: Optional[float] = None
    licitacion_ano: Optional[float] = None
    nomenclatura: Optional[str] = None
    nomenclatura_plano: Optional[str] = None
    fecha_entrega: Optional[str] = None
    fecha_contrato: Optional[str] = None
    expediente_costo: Optional[str] = None
    inspector_ids: list[int] = []
    observaciones: Optional[str] = None

class ObraUpdate(BaseModel):
    obra_nombre: Optional[str] = None
    obra_soluciones: Optional[float] = None
    empresa_id: Optional[int] = None
    region_id: Optional[int] = None
    departamento_ids: Optional[list[int]] = None
    municipio_ids: Optional[list[int]] = None
    localidad_ids: Optional[list[int]] = None
    conjunto_id: Optional[int] = None
    grupo: Optional[str] = None
    plazo: Optional[str] = None
    programa_id: Optional[int] = None
    convenio: Optional[str] = None
    expediente: Optional[str] = None
    resolucion: Optional[str] = None
    licitacion_tipo: Optional[str] = None
    licitacion_numero: Optional[float] = None
    licitacion_ano: Optional[float] = None
    nomenclatura: Optional[str] = None
    nomenclatura_plano: Optional[str] = None
    fecha_entrega: Optional[str] = None
    fecha_contrato: Optional[str] = None
    expediente_costo: Optional[str] = None
    inspector_ids: Optional[list[int]] = None
    observaciones: Optional[str] = None

# === Prototipo ===
class PrototipoOut(BaseModel):
    id: int
    prototipo_uuid: str
    prototipo_obra_id: int
    prototipo_tipo: str
    prototipo_cantidad: float
    prototipo_superficie: float
    prototipo_uvi: float
    prototipo_incremento: float
    prototipo_discapacitado: bool

class PrototipoCreate(BaseModel):
    prototipo_obra_id: int
    prototipo_tipo: str
    prototipo_cantidad: float
    prototipo_superficie: float
    prototipo_uvi: float
    prototipo_incremento: float
    prototipo_discapacitado: bool = False

class PrototipoUpdate(BaseModel):
    prototipo_obra_id: Optional[int] = None
    prototipo_tipo: Optional[str] = None
    prototipo_cantidad: Optional[float] = None
    prototipo_superficie: Optional[float] = None
    prototipo_uvi: Optional[float] = None
    prototipo_incremento: Optional[float] = None
    prototipo_discapacitado: Optional[bool] = None

# === CertificadoRubro ===
class CertificadoRubroOut(BaseModel):
    id: int
    certificadorubro_uuid: str
    certificadorubro_nombre: str
    certificadorubro_nombre_corto: str

class CertificadoRubroCreate(BaseModel):
    certificadorubro_nombre: str
    certificadorubro_nombre_corto: str

class CertificadoRubroUpdate(BaseModel):
    certificadorubro_nombre: Optional[str] = None
    certificadorubro_nombre_corto: Optional[str] = None

# === CertificadoFinanciamiento ===
class CertificadoFinanciamientoOut(BaseModel):
    id: int
    certificadofinanciamiento_uuid: str
    certificadofinanciamiento_nombre: str
    certificadofinanciamiento_nombre_corto: str

class CertificadoFinanciamientoCreate(BaseModel):
    certificadofinanciamiento_nombre: str
    certificadofinanciamiento_nombre_corto: str

class CertificadoFinanciamientoUpdate(BaseModel):
    certificadofinanciamiento_nombre: Optional[str] = None
    certificadofinanciamiento_nombre_corto: Optional[str] = None

# === Certificado ===
class CertificadoOut(BaseModel):
    id: int
    certificado_uuid: str
    obra_id: int
    finaciamiento: str
    rubro: str
    rubro_db_id: int
    rubro_anticipo: float
    rubro_obra: float
    rubro_devanticipo: float
    expediente: str
    periodo: Optional[str] = None
    monto_pesos: float
    mes_pct: float
    ante_pct: float
    acum_pct: float
    devolucion_expte: Optional[str] = None
    devolucion_monto: float
    devolucion_monto_uvi: float
    monto_uvi: float
    fecha: str
    monto_cobrar: float
    monto_cobrar_uvi: float
    fecha_carga: str

class CertificadoCreate(BaseModel):
    obra_id: int
    finaciamiento: str = "N"
    rubro: str = "V"
    rubro_db_id: int = 1
    rubro_anticipo: float = 0.0
    rubro_obra: float = 0.0
    rubro_devanticipo: float = 0.0
    expediente: str
    periodo: Optional[str] = None
    monto_pesos: float = 0.0
    mes_pct: float = 0.0
    ante_pct: float = 0.0
    acum_pct: float = 0.0
    devolucion_expte: Optional[str] = None
    devolucion_monto: float = 0.0
    devolucion_monto_uvi: float = 0.0
    monto_uvi: float = 0.0
    fecha: str

class CertificadoUpdate(BaseModel):
    obra_id: Optional[int] = None
    finaciamiento: Optional[str] = None
    rubro: Optional[str] = None
    rubro_db_id: Optional[int] = None
    rubro_anticipo: Optional[float] = None
    rubro_obra: Optional[float] = None
    rubro_devanticipo: Optional[float] = None
    expediente: Optional[str] = None
    periodo: Optional[str] = None
    monto_pesos: Optional[float] = None
    mes_pct: Optional[float] = None
    ante_pct: Optional[float] = None
    acum_pct: Optional[float] = None
    devolucion_expte: Optional[str] = None
    devolucion_monto: Optional[float] = None
    devolucion_monto_uvi: Optional[float] = None
    monto_uvi: Optional[float] = None
    fecha: Optional[str] = None

# === ConjuntoLicitado ===
class ConjuntoLicitadoOut(BaseModel):
    id: int
    conjunto_uuid: str
    conjunto_nombre: str
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    subconjunto_id: Optional[int] = None

class ConjuntoLicitadoCreate(BaseModel):
    conjunto_nombre: str
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    subconjunto_id: Optional[int] = None

class ConjuntoLicitadoUpdate(BaseModel):
    conjunto_nombre: Optional[str] = None
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    subconjunto_id: Optional[int] = None

# === PlanDeTrabajos ===
class PlanDeTrabajosOut(BaseModel):
    id: int
    trabajos_uuid: str
    obra_id: int

class PlanDeTrabajosCreate(BaseModel):
    obra_id: int

class PlanDeTrabajosUpdate(BaseModel):
    obra_id: Optional[int] = None

# === Contrato ===
class ContratoOut(BaseModel):
    id: int
    contrato_uuid: str
    obra_id: int
    fecha: str
    descripcion: str
    resolucion: Optional[str] = None
    autocarga: bool
    decreto: Optional[str] = None

class ContratoCreate(BaseModel):
    obra_id: int
    fecha: str
    descripcion: str = ""
    resolucion: Optional[str] = None
    decreto: Optional[str] = None

class ContratoUpdate(BaseModel):
    obra_id: Optional[int] = None
    fecha: Optional[str] = None
    descripcion: Optional[str] = None
    resolucion: Optional[str] = None
    decreto: Optional[str] = None

# === ContratoMonto ===
class ContratoMontoOut(BaseModel):
    id: int
    contratomonto_uuid: str
    contrato_id: int
    rubro_id: int
    financiamiento_id: int
    pesos: float
    uvi: float
    uvi_fecha: Optional[str] = None

class ContratoMontoCreate(BaseModel):
    contrato_id: int
    rubro_id: int
    financiamiento_id: int
    pesos: float = 0.0
    uvi: float = 0.0
    uvi_fecha: Optional[str] = None

class ContratoMontoUpdate(BaseModel):
    contrato_id: Optional[int] = None
    rubro_id: Optional[int] = None
    financiamiento_id: Optional[int] = None
    pesos: Optional[float] = None
    uvi: Optional[float] = None
    uvi_fecha: Optional[str] = None

# === ContratoRubro ===
class ContratoRubroOut(BaseModel):
    id: int
    contratorubro_uuid: str
    contratorubro_tipo: str

class ContratoRubroCreate(BaseModel):
    contratorubro_tipo: str

class ContratoRubroUpdate(BaseModel):
    contratorubro_tipo: Optional[str] = None

# === ContratosDigitales ===
class ContratosDigitalesOut(BaseModel):
    id: int
    contratodigital_uuid: str
    contrato_id: int
    nombre_archivo: Optional[str] = None
    descripcion: str
    tipo_id: int

class ContratosDigitalesCreate(BaseModel):
    contrato_id: int
    nombre_archivo: Optional[str] = None
    descripcion: str
    tipo_id: int

class ContratosDigitalesUpdate(BaseModel):
    contrato_id: Optional[int] = None
    nombre_archivo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_id: Optional[int] = None

# === ResolucionesDigitales ===
class ResolucionesDigitalesOut(BaseModel):
    id: int
    resoluciondigital_uuid: str
    contrato_id: int
    descripcion: str
    numero: str

class ResolucionesDigitalesCreate(BaseModel):
    contrato_id: int
    descripcion: str
    numero: str

class ResolucionesDigitalesUpdate(BaseModel):
    contrato_id: Optional[int] = None
    descripcion: Optional[str] = None
    numero: Optional[str] = None

# === Uvi ===
class UviOut(BaseModel):
    id: int
    uvi_uuid: str
    fecha: str
    valor: float

class UviCreate(BaseModel):
    fecha: str
    valor: float

class UviUpdate(BaseModel):
    fecha: Optional[str] = None
    valor: Optional[float] = None

# === INDEC ===
class INDECOut(BaseModel):
    id: int
    indec_uuid: str
    mes: str
    manodeobra: float
    albanileria: float
    carpinterias: float
    andamios: float
    iluminacion: float
    pvc: float
    gastos: float
    artefactos: float
    hormigon: float
    valvulas: float
    electrobombas: float
    quimicos: float
    motores: float
    asfaltos: float
    medidores: float
    membrana: float
    equipo: float
    pisos: float
    aceros: float
    cemento: float
    arena: float
    costo_financiero: float = 18.85
    transporte: float = 134.98

class INDECCreate(BaseModel):
    mes: str
    manodeobra: float
    albanileria: float
    carpinterias: float
    andamios: float
    iluminacion: float
    pvc: float
    gastos: float
    artefactos: float
    hormigon: float
    valvulas: float
    electrobombas: float
    quimicos: float
    motores: float
    asfaltos: float
    medidores: float
    membrana: float
    equipo: float
    pisos: float
    aceros: float
    cemento: float
    arena: float

class INDECUpdate(BaseModel):
    mes: Optional[str] = None
    manodeobra: Optional[float] = None
    albanileria: Optional[float] = None
    carpinterias: Optional[float] = None
    andamios: Optional[float] = None
    iluminacion: Optional[float] = None
    pvc: Optional[float] = None
    gastos: Optional[float] = None
    artefactos: Optional[float] = None
    hormigon: Optional[float] = None
    valvulas: Optional[float] = None
    electrobombas: Optional[float] = None
    quimicos: Optional[float] = None
    motores: Optional[float] = None
    asfaltos: Optional[float] = None
    medidores: Optional[float] = None
    membrana: Optional[float] = None
    equipo: Optional[float] = None
    pisos: Optional[float] = None
    aceros: Optional[float] = None
    cemento: Optional[float] = None
    arena: Optional[float] = None
