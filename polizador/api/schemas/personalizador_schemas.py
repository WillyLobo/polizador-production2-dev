# personalizador app schemas - generated from Django models
from pydantic import BaseModel
from typing import Optional



class GerenciaOut(BaseModel):
    id: int
    gerencia_uuid: str
    gerencia_nombre: str
    gerencia_cuof: str

class GerenciaCreate(BaseModel):
    gerencia_nombre: str
    gerencia_cuof: str

class GerenciaUpdate(BaseModel):
    gerencia_nombre: Optional[str] = None
    gerencia_cuof: Optional[str] = None


class DireccionOut(BaseModel):
    id: int
    direccion_uuid: str
    direccion_nombre: str
    direccion_cuof: str

class DireccionCreate(BaseModel):
    direccion_nombre: str
    direccion_cuof: str

class DireccionUpdate(BaseModel):
    direccion_nombre: Optional[str] = None
    direccion_cuof: Optional[str] = None


class DepartamentoPerOut(BaseModel):
    id: int
    departamento_uuid: str
    departamento_nombre: str
    departamento_cuof: str

class DepartamentoPerCreate(BaseModel):
    departamento_nombre: str
    departamento_cuof: str

class DepartamentoPerUpdate(BaseModel):
    departamento_nombre: Optional[str] = None
    departamento_cuof: Optional[str] = None
