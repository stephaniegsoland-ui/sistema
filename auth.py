import reflex as rx
from ..api.models import Usuario
from sqlmodel import select

class AuthState(rx.State):
    usuario_autenticado: Usuario | None = None
    cargando: bool = False

    def login(self, datos: dict):
        self.cargando = True
        username = datos.get("username")
        password = datos.get("password")

        with rx.session() as session:
            query = select(Usuario).where(
                (Usuario.nombre_usuario == username) & 
                (Usuario.password == password)
            )
            user = session.exec(query).first()
            self.cargando = False

            if user:
                self.usuario_autenticado = user
                return rx.redirect("/dashboard")
            else:
                return rx.window_alert("Usuario o contraseña incorrectos")

    def logout(self):
        self.usuario_autenticado = None
        return rx.redirect("/")