import reflex as rx
import sqlmodel
from typing import Optional
from sistema.api.models import Usuario

class AuthState(rx.State):
    # El usuario se mantiene en la sesión del navegador
    usuario_actual: Optional[Usuario] = None
    
    input_login_username: str = ""
    input_login_password: str = ""

    @rx.var
    def esta_autenticado(self) -> bool:
        return self.usuario_actual is not None

    @rx.var
    def nombre_desplegado(self) -> str:
        return self.usuario_actual.nombre_usuario if self.usuario_actual else "Invitado"

    @rx.var
    def rol_desplegado(self) -> str:
        if not self.usuario_actual: return "Colaborador"
        if self.usuario_actual.nivel == 1: return "Administrador Maestro"
        if self.usuario_actual.nivel == 2: return "Supervisor"
        return "Empleado"

    # Lógica de permisos computados para leer la propiedad 'estado' del modelo
    @rx.var
    def puede_ver_dashboard(self) -> bool:
        if not self.usuario_actual: return False
        return "dashboard" in self.usuario_actual.estado or "TODOS" in self.usuario_actual.estado

    @rx.var
    def puede_ver_stock(self) -> bool:
        if not self.usuario_actual: return False
        return "stock" in self.usuario_actual.estado or "TODOS" in self.usuario_actual.estado

    @rx.var
    def puede_ver_procura(self) -> bool:
        if not self.usuario_actual: return False
        return "procura" in self.usuario_actual.estado or "TODOS" in self.usuario_actual.estado

    @rx.var
    def puede_ver_personal(self) -> bool:
        # El módulo de control de personal solo es para nivel 1 (Administradores)
        if not self.usuario_actual: return False
        return self.usuario_actual.nivel == 1

    @rx.event
    def login_usuario(self):
        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(Usuario).where(
                    Usuario.nombre_usuario == self.input_login_username,
                    Usuario.password == self.input_login_password,
                    Usuario.tipo == "activo"
                )
            ).first()
            
            if not user:
                return rx.toast.error("Credenciales incorrectas o usuario inactivo")
            
            self.usuario_actual = user
            self.input_login_username = ""
            self.input_login_password = ""
            return rx.redirect("/dashboard") # O la ruta de tu página principal

    @rx.event
    def logout_usuario(self):
        self.usuario_actual = None
        return rx.redirect("/login")