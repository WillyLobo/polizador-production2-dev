# carga app schemas
from ninja import Schema
from uuid import UUID
from datetime import date
from typing import Optional


# === Receptor ===
class ReceptorOut(Schema):
    id: int
    receptor_nombre: str
    receptor_uuid: UUID

class ReceptorCreate(Schema):
    receptor_nombre: str

class ReceptorUpdate(Schema):
    receptor_nombre: Optional[str] = None

# === Area ===
class AreaOut(Schema):
    id: int
    area_uuid: UUID
    area_nombre: str

class AreaCreate(Schema):
    area_nombre: str

class AreaUpdate(Schema):
    area_nombre: Optional[str] = None

# === Aseguradora ===
class AseguradoraOut(Schema):
    id: int
    aseguradora_uuid: UUID
    aseguradora_nombre: str

class AseguradoraCreate(Schema):
    aseguradora_nombre: str

class AseguradoraUpdate(Schema):
    aseguradora_nombre: Optional[str] = None

# === Empresa ===
class EmpresaOut(Schema):
    id: int
    empresa_uuid: UUID
    empresa_nombre: str
    empresa_cuit: Optional[str] = None
    empresa_titular_titulo: Optional[str] = None
    empresa_titular_nombre: Optional[str] = None
    empresa_titular_dni: Optional[float] = None
    empresa_direccion: Optional[str] = None
    empresa_inscripcion: Optional[str] = None
    empresa_correo_p: Optional[str] = None
    empresa_correo_s: Optional[str] = None

class EmpresaCreate(Schema):
    empresa_nombre: str
    empresa_cuit: Optional[str] = None
    empresa_titular_titulo: Optional[str] = None
    empresa_titular_nombre: Optional[str] = None
    empresa_titular_dni: Optional[float] = None
    empresa_direccion: Optional[str] = None
    empresa_inscripcion: Optional[str] = None
    empresa_correo_p: Optional[str] = None
    empresa_correo_s: Optional[str] = None

class EmpresaUpdate(Schema):
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
class ProgramaOut(Schema):
    id: int
    programa_uuid: UUID
    programa_nombre: str

class ProgramaCreate(Schema):
    programa_nombre: str

class ProgramaUpdate(Schema):
    programa_nombre: Optional[str] = None

# === Provincia ===
class ProvinciaOut(Schema):
    id: int
    provincia_uuid: UUID
    provincia_nombre: str

class ProvinciaCreate(Schema):
    provincia_nombre: str

class ProvinciaUpdate(Schema):
    provincia_nombre: Optional[str] = None

# === Region ===
class RegionOut(Schema):
    id: int
    region_uuid: UUID
    region_numero: str

class RegionCreate(Schema):
    region_numero: str

class RegionUpdate(Schema):
    region_numero: Optional[str] = None

# === Departamento (carga) ===
class DepartamentoCargaOut(Schema):
    id: int
    departamento_uuid: UUID
    departamento_nombre: str

class DepartamentoCargaCreate(Schema):
    departamento_nombre: str

class DepartamentoCargaUpdate(Schema):
    departamento_nombre: Optional[str] = None

# === Municipio ===
class MunicipioOut(Schema):
    id: int
    municipio_uuid: UUID
    municipio_nombre: str
    municipio_departamento_id: int
    municipio_region_id: Optional[int] = None

class MunicipioCreate(Schema):
    municipio_nombre: str
    municipio_departamento_id: int
    municipio_region_id: Optional[int] = None

class MunicipioUpdate(Schema):
    municipio_nombre: Optional[str] = None
    municipio_departamento_id: Optional[int] = None
    municipio_region_id: Optional[int] = None

# === Localidad ===
class LocalidadOut(Schema):
    id: int
    localidad_uuid: UUID
    localidad_nombre: str
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento_id: int
    localidad_municipio_id: int

class LocalidadCreate(Schema):
    localidad_nombre: str
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento_id: int
    localidad_municipio_id: int

class LocalidadUpdate(Schema):
    localidad_nombre: Optional[str] = None
    localidad_centroide_lat: Optional[float] = None
    localidad_centroide_lon: Optional[float] = None
    localidad_funcion: Optional[str] = None
    localidad_departamento_id: Optional[int] = None
    localidad_municipio_id: Optional[int] = None

# === Obra ===
class ObraOut(Schema):
    id: int
    obra_uuid: UUID
    obra_nombre: str
    obra_soluciones: Optional[float] = None
    obra_empresa_id: int
    obra_region_id: Optional[int] = None
    departamento_ids: list[int] = []
    municipio_ids: list[int] = []
    localidad_ids: list[int] = []
    obra_conjunto_id: Optional[int] = None
    obra_grupo: Optional[str] = None
    obra_plazo: Optional[str] = None
    obra_programa_id: int
    obra_convenio: Optional[str] = None
    obra_expediente: str
    obra_resolucion: Optional[str] = None
    obra_resolucion_fk_id: Optional[int] = None
    obra_licitacion_tipo: Optional[str] = None
    obra_licitacion_numero: Optional[float] = None
    obra_licitacion_ano: Optional[float] = None
    obra_nomenclatura: Optional[str] = None
    obra_nomenclatura_plano: Optional[str] = None
    obra_fecha_entrega: Optional[date] = None
    obra_fecha_contrato: Optional[date] = None
    obra_expediente_costo: Optional[str] = None
    inspector_ids: list[int] = []
    obra_observaciones: Optional[str] = None
    obra_contrato_nacion_pesos: float = 0.0
    obra_contrato_nacion_uvi: float = 0.0
    obra_contrato_provincia_pesos: float = 0.0
    obra_contrato_provincia_uvi: float = 0.0
    obra_contrato_total_pesos: float = 0.0

class ObraCreate(Schema):
    obra_nombre: str
    obra_soluciones: Optional[float] = None
    obra_empresa_id: int
    obra_region_id: Optional[int] = None
    departamento_ids: list[int] = []
    municipio_ids: list[int] = []
    localidad_ids: list[int] = []
    obra_conjunto_id: Optional[int] = None
    obra_grupo: Optional[str] = None
    obra_plazo: Optional[str] = None
    obra_programa_id: int
    obra_convenio: Optional[str] = None
    obra_expediente: str
    obra_resolucion: Optional[str] = None
    obra_resolucion_fk_id: Optional[int] = None
    obra_licitacion_tipo: Optional[str] = None
    obra_licitacion_numero: Optional[float] = None
    obra_licitacion_ano: Optional[float] = None
    obra_nomenclatura: Optional[str] = None
    obra_nomenclatura_plano: Optional[str] = None
    obra_fecha_entrega: Optional[date] = None
    obra_fecha_contrato: Optional[date] = None
    obra_expediente_costo: Optional[str] = None
    inspector_ids: list[int] = []
    obra_observaciones: Optional[str] = None

class ObraUpdate(Schema):
    obra_nombre: Optional[str] = None
    obra_soluciones: Optional[float] = None
    obra_empresa_id: Optional[int] = None
    obra_region_id: Optional[int] = None
    departamento_ids: Optional[list[int]] = None
    municipio_ids: Optional[list[int]] = None
    localidad_ids: Optional[list[int]] = None
    obra_conjunto_id: Optional[int] = None
    obra_grupo: Optional[str] = None
    obra_plazo: Optional[str] = None
    obra_programa_id: Optional[int] = None
    obra_convenio: Optional[str] = None
    obra_expediente: Optional[str] = None
    obra_resolucion: Optional[str] = None
    obra_resolucion_fk_id: Optional[int] = None
    obra_licitacion_tipo: Optional[str] = None
    obra_licitacion_numero: Optional[float] = None
    obra_licitacion_ano: Optional[float] = None
    obra_nomenclatura: Optional[str] = None
    obra_nomenclatura_plano: Optional[str] = None
    obra_fecha_entrega: Optional[date] = None
    obra_fecha_contrato: Optional[date] = None
    obra_expediente_costo: Optional[str] = None
    inspector_ids: Optional[list[int]] = None
    obra_observaciones: Optional[str] = None

# === Prototipo ===
class PrototipoOut(Schema):
    id: int
    prototipo_uuid: UUID
    prototipo_obra_id: int
    prototipo_tipo: str
    prototipo_cantidad: float
    prototipo_superficie: float
    prototipo_uvi: float
    prototipo_incremento: float
    prototipo_discapacitado: bool

class PrototipoCreate(Schema):
    prototipo_obra_id: int
    prototipo_tipo: str
    prototipo_cantidad: float
    prototipo_superficie: float
    prototipo_uvi: float
    prototipo_incremento: float
    prototipo_discapacitado: bool = False

class PrototipoUpdate(Schema):
    prototipo_obra_id: Optional[int] = None
    prototipo_tipo: Optional[str] = None
    prototipo_cantidad: Optional[float] = None
    prototipo_superficie: Optional[float] = None
    prototipo_uvi: Optional[float] = None
    prototipo_incremento: Optional[float] = None
    prototipo_discapacitado: Optional[bool] = None

# === CertificadoRubro ===
class CertificadoRubroOut(Schema):
    id: int
    certificadorubro_uuid: UUID
    certificadorubro_nombre: str
    certificadorubro_nombre_corto: str

class CertificadoRubroCreate(Schema):
    certificadorubro_nombre: str
    certificadorubro_nombre_corto: str

class CertificadoRubroUpdate(Schema):
    certificadorubro_nombre: Optional[str] = None
    certificadorubro_nombre_corto: Optional[str] = None

# === CertificadoFinanciamiento ===
class CertificadoFinanciamientoOut(Schema):
    id: int
    certificadofinanciamiento_uuid: UUID
    certificadofinanciamiento_nombre: str
    certificadofinanciamiento_nombre_corto: str

class CertificadoFinanciamientoCreate(Schema):
    certificadofinanciamiento_nombre: str
    certificadofinanciamiento_nombre_corto: str

class CertificadoFinanciamientoUpdate(Schema):
    certificadofinanciamiento_nombre: Optional[str] = None
    certificadofinanciamiento_nombre_corto: Optional[str] = None

# === Certificado ===
class CertificadoOut(Schema):
    id: int
    certificado_uuid: UUID
    certificado_obra_id: int
    certificado_financiamiento: str
    certificado_rubro: str
    certificado_rubro_db_id: int
    certificado_expediente: str
    certificado_periodo: Optional[str] = None
    certificado_monto_pesos: float = 0.0
    certificado_fecha: date
    certificado_monto_cobrar: float = 0.0

class CertificadoCreate(Schema):
    certificado_obra_id: int
    certificado_financiamiento: str = "N"
    certificado_rubro_db_id: int = 1
    certificado_expediente: str
    certificado_monto_pesos: float = 0.0
    certificado_fecha: date

class CertificadoUpdate(Schema):
    certificado_obra_id: Optional[int] = None
    certificado_financiamiento: Optional[str] = None
    certificado_rubro_db_id: Optional[int] = None
    certificado_expediente: Optional[str] = None
    certificado_periodo: Optional[str] = None
    certificado_monto_pesos: Optional[float] = None
    certificado_fecha: Optional[date] = None

# === ConjuntoLicitado ===
class ConjuntoLicitadoOut(Schema):
    id: int
    conjunto_uuid: UUID
    conjunto_nombre: str
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    conjunto_resolucion_fk_id: Optional[int] = None

class ConjuntoLicitadoCreate(Schema):
    conjunto_nombre: str
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    conjunto_resolucion_fk_id: Optional[int] = None

class ConjuntoLicitadoUpdate(Schema):
    conjunto_nombre: Optional[str] = None
    conjunto_soluciones: Optional[float] = None
    conjunto_resolucion: Optional[str] = None
    conjunto_resolucion_fk_id: Optional[int] = None

# === PlanDeTrabajos ===
class PlanDeTrabajosOut(Schema):
    id: int
    trabajos_uuid: UUID
    trabajos_obra_id: int

class PlanDeTrabajosCreate(Schema):
    trabajos_obra_id: int

class PlanDeTrabajosUpdate(Schema):
    trabajos_obra_id: Optional[int] = None

# === Contrato ===
class ContratoOut(Schema):
    id: int
    contrato_uuid: UUID
    contrato_obra_id: int
    contrato_fecha: date
    contrato_descripcion: str
    contrato_resolucion: Optional[str] = None
    contrato_resolucion_fk_id: Optional[int] = None
    contrato_decreto: Optional[str] = None

class ContratoCreate(Schema):
    contrato_obra_id: int
    contrato_fecha: date
    contrato_descripcion: str = ""
    contrato_resolucion: Optional[str] = None
    contrato_resolucion_fk_id: Optional[int] = None
    contrato_decreto: Optional[str] = None

class ContratoUpdate(Schema):
    contrato_obra_id: Optional[int] = None
    contrato_fecha: Optional[date] = None
    contrato_descripcion: Optional[str] = None
    contrato_resolucion: Optional[str] = None
    contrato_resolucion_fk_id: Optional[int] = None
    contrato_decreto: Optional[str] = None

# === ContratoMonto ===
class ContratoMontoOut(Schema):
    id: int
    contratomonto_uuid: UUID
    contratomonto_contrato_id: int
    contratomonto_rubro_id: int
    contratomonto_financiamiento_id: int
    contratomonto_pesos: float
    contratomonto_uvi: float
    contratomonto_uvi_fecha: Optional[date] = None

class ContratoMontoCreate(Schema):
    contratomonto_contrato_id: int
    contratomonto_rubro_id: int
    contratomonto_financiamiento_id: int
    contratomonto_pesos: float = 0.0
    contratomonto_uvi: float = 0.0
    contratomonto_uvi_fecha: Optional[date] = None

class ContratoMontoUpdate(Schema):
    contratomonto_contrato_id: Optional[int] = None
    contratomonto_rubro_id: Optional[int] = None
    contratomonto_financiamiento_id: Optional[int] = None
    contratomonto_pesos: Optional[float] = None
    contratomonto_uvi: Optional[float] = None
    contratomonto_uvi_fecha: Optional[date] = None

# === ContratoRubro ===
class ContratoRubroOut(Schema):
    id: int
    contratorubro_uuid: UUID
    contratorubro_tipo: str

class ContratoRubroCreate(Schema):
    contratorubro_tipo: str

class ContratoRubroUpdate(Schema):
    contratorubro_tipo: Optional[str] = None

# === ContratosDigitales ===
class ContratosDigitalesOut(Schema):
    id: int
    contratodigital_uuid: UUID
    contratodigital_contrato_id: int
    contratodigital_nombre_archivo: Optional[str] = None
    contratodigital_descripcion: str
    contratodigital_tipo_id: int

class ContratosDigitalesCreate(Schema):
    contratodigital_contrato_id: int
    contratodigital_nombre_archivo: Optional[str] = None
    contratodigital_descripcion: str
    contratodigital_tipo_id: int

class ContratosDigitalesUpdate(Schema):
    contratodigital_contrato_id: Optional[int] = None
    contratodigital_nombre_archivo: Optional[str] = None
    contratodigital_descripcion: Optional[str] = None
    contratodigital_tipo_id: Optional[int] = None

# === Uvi ===
class UviOut(Schema):
    id: int
    uvi_uuid: UUID
    uvi_fecha: date
    uvi_valor: float

class UviCreate(Schema):
    uvi_fecha: date
    uvi_valor: float

class UviUpdate(Schema):
    uvi_fecha: Optional[date] = None
    uvi_valor: Optional[float] = None

# === INDEC ===
class INDECOut(Schema):
    id: int
    indec_uuid: UUID
    mes: date
    indec_manodeobra: float
    indec_albanileria: float
    indec_carpinterías: float
    indec_andamios: float
    indec_iluminación: float
    indec_pvc: float
    indec_gastos: float
    indec_artefactos: float
    indec_hormigon: float
    indec_valvulas: float
    indec_electrobombas: float
    indec_quimicos: float
    indec_motores: float
    indec_asfaltos: float
    indec_medidores: float
    indec_membrana: float
    indec_equipo: float
    indec_pisos: float
    indec_aceros: float
    indec_cemento: float
    indec_arena: float
    indec_costo_financiero: float = 18.85
    indec_transporte: float = 134.98

class INDECCreate(Schema):
    mes: date
    indec_manodeobra: float = 0
    indec_albanileria: float = 0
    indec_carpinterías: float = 0
    indec_andamios: float = 0
    indec_iluminación: float = 0
    indec_pvc: float = 0
    indec_gastos: float = 0
    indec_artefactos: float = 0
    indec_hormigon: float = 0
    indec_valvulas: float = 0
    indec_electrobombas: float = 0
    indec_quimicos: float = 0
    indec_motores: float = 0
    indec_asfaltos: float = 0
    indec_medidores: float = 0
    indec_membrana: float = 0
    indec_equipo: float = 0
    indec_pisos: float = 0
    indec_aceros: float = 0
    indec_cemento: float = 0
    indec_arena: float = 0
    indec_costo_financiero: float = 18.85
    indec_transporte: float = 134.98

class INDECUpdate(Schema):
    mes: Optional[date] = None
    indec_manodeobra: Optional[float] = None
    indec_albanileria: Optional[float] = None
    indec_carpinterías: Optional[float] = None
    indec_andamios: Optional[float] = None
    indec_iluminación: Optional[float] = None
    indec_pvc: Optional[float] = None
    indec_gastos: Optional[float] = None
    indec_artefactos: Optional[float] = None
    indec_hormigon: Optional[float] = None
    indec_valvulas: Optional[float] = None
    indec_electrobombas: Optional[float] = None
    indec_quimicos: Optional[float] = None
    indec_motores: Optional[float] = None
    indec_asfaltos: Optional[float] = None
    indec_medidores: Optional[float] = None
    indec_membrana: Optional[float] = None
    indec_equipo: Optional[float] = None
    indec_pisos: Optional[float] = None
    indec_aceros: Optional[float] = None
    indec_cemento: Optional[float] = None
    indec_arena: Optional[float] = None
    indec_costo_financiero: Optional[float] = None
    indec_transporte: Optional[float] = None

# === Poliza ===
class PolizaOut(Schema):
    id: int
    poliza_uuid: UUID
    poliza_fecha: date
    poliza_expediente: str
    poliza_numero: int
    poliza_concepto: str
    poliza_recibo: str
    poliza_aseguradora_id: int
    poliza_tomador_id: int
    poliza_obra_id: int

class PolizaCreate(Schema):
    poliza_fecha: date
    poliza_expediente: str
    poliza_numero: int
    poliza_concepto: str = "C"
    poliza_recibo: str
    poliza_aseguradora_id: int
    poliza_tomador_id: int
    poliza_obra_id: int

class PolizaUpdate(Schema):
    poliza_fecha: Optional[date] = None
    poliza_expediente: Optional[str] = None
    poliza_numero: Optional[int] = None
    poliza_concepto: Optional[str] = None
    poliza_recibo: Optional[str] = None
    poliza_aseguradora_id: Optional[int] = None
    poliza_tomador_id: Optional[int] = None
    poliza_obra_id: Optional[int] = None

# === Poliza_Movimiento ===
class PolizaMovimientoOut(Schema):
    id: int
    poliza_movimiento_uuid: UUID
    poliza_movimiento_fecha: date
    poliza_movimiento_receptor_id: int
    poliza_movimiento_area_id: int
    poliza_movimiento_numero_id: int

class PolizaMovimientoCreate(Schema):
    poliza_movimiento_fecha: date
    poliza_movimiento_receptor_id: int
    poliza_movimiento_area_id: int
    poliza_movimiento_numero_id: int

class PolizaMovimientoUpdate(Schema):
    poliza_movimiento_fecha: Optional[date] = None
    poliza_movimiento_receptor_id: Optional[int] = None
    poliza_movimiento_area_id: Optional[int] = None
    poliza_movimiento_numero_id: Optional[int] = None
