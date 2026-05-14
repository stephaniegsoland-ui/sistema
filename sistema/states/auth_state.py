import reflex as rx
from sqlmodel import select
from ..api.models import Usuario
from ..db_init import get_session
from typing import Optional

class AuthState(rx.State):
    usuario_actual: Optional[Usuario] = None
    error_message: str = ""

    def registrar_usuario(self, datos: dict):
        """Para crear usuarios nuevos desde el sistema o DBeaver"""
        with get_session() as session:
           
            nuevo_usuario = Usuario(
                nombre_usuario=datos["user"],
                password=datos["pass"],
                nivel=datos.get("nivel", 3)
            )
            session.add(nuevo_usuario)
            session.commit()

    def login(self, form_data: dict):
        username = form_data["username"]
        password = form_data["password"]

        with get_session() as session:
            user = session.exec(
                select(Usuario).where(
                    (Usuario.nombre_usuario == username) & 
                    (Usuario.password == password)
                )
            ).first()

            if user:
                self.usuario_actual = user
                self.error_message = ""
                return rx.redirect("/dashboard")
            else:
                self.error_message = "Credenciales incorrectas"
    def check_login(self):
        if not self.usuario_actual:
            return rx.redirect("/")
    @rx.var
    def es_admin(self) -> bool:
        return self.usuario_actual is not None and self.usuario_actual.nivel == 1

    def logout(self):
        self.usuario_actual = None
        return rx.redirect("/")