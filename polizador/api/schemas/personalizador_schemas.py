# personalizador app schemas - generated from Django models
from pydantic import BaseModel
from typing import Optional


class CustomUserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    usuario_dni: Optional[float] = None

class CustomUserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    usuario_dni: Optional[float] = None

class CustomUserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    usuario_dni: Optional[float] = None


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
