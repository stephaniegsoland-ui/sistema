from sqlalchemy import Column, Text
from sqlmodel import SQLModel, Field
from typing import Optional
import reflex as rx


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_usuario: str = Field(unique=True, nullable=False)
    password: str
    nivel: int = 1  # 1: Admin, 2: Supervisor, 3: Usuario
    estado: str = "activo"

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cantidad: int
    categoria: str # Ej: "Almacén Central", "Logística"

class InspeccionReporte(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str
    modelo: str
    responsable: str
    fecha: str
    estado_final: str
    recomendacion: str = Field(sa_column=Column(Text), default="")
    url_lunes: str
    url_viernes: str
    hallazgos_json: str = Field(sa_column=Column(Text), default="")
    damage_map_lunes_json: str = Field(sa_column=Column(Text), default="")
    damage_map_viernes_json: str = Field(sa_column=Column(Text), default="")

class Vehiculo(rx.Base):
    nombre: str
    modelo: str
    placa: str
    imagen_url: str
    registrado: bool = True