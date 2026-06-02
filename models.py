import reflex as rx
from sqlmodel import Field

class Usuario(rx.Model, table=True):
    """Modelo alineado exactamente con las columnas reales de MySQL"""
    id: int = Field(primary_key=True)
    nombre_usuario: str = Field(unique=True, index=True)
    password: str
    nivel: int = 2          # 1: Admin, 2: Personal
    estado: str = "ACTIVO"  # ¡Aquí guardamos los permisos strings! ej: "dash, stock, ia" o "TODOS"