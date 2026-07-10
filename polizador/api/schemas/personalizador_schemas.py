# personalizador app schemas
from ninja import Schema
from uuid import UUID
from typing import Optional


class CustomUserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    usuario_dni: Optional[float] = None

class CustomUserCreate(Schema):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    usuario_dni: Optional[float] = None

class CustomUserUpdate(Schema):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    usuario_dni: Optional[float] = None


class GerenciaOut(Schema):
    id: int
    gerencia_uuid: UUID
    gerencia_directorio_id: int
    gerencia_nombre: str
    gerencia_cuof: str

class GerenciaCreate(Schema):
    gerencia_directorio_id: int
    gerencia_nombre: str
    gerencia_cuof: str

class GerenciaUpdate(Schema):
    gerencia_directorio_id: Optional[int] = None
    gerencia_nombre: Optional[str] = None
    gerencia_cuof: Optional[str] = None


class DireccionOut(Schema):
    id: int
    direccion_uuid: UUID
    direccion_nombre: str
    direccion_cuof: str

class DireccionCreate(Schema):
    direccion_nombre: str
    direccion_cuof: str

class DireccionUpdate(Schema):
    direccion_nombre: Optional[str] = None
    direccion_cuof: Optional[str] = None


class DepartamentoPerOut(Schema):
    id: int
    departamento_uuid: UUID
    departamento_nombre: str
    departamento_cuof: str

class DepartamentoPerCreate(Schema):
    departamento_nombre: str
    departamento_cuof: str

class DepartamentoPerUpdate(Schema):
    departamento_nombre: Optional[str] = None
    departamento_cuof: Optional[str] = None
