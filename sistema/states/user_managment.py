import reflex as rx
from sqlmodel import select
from ..api.models import Usuario
from ..db_init import get_session
from .auth_state import AuthState

class UserManagementState(rx.State):
    usuarios: list[Usuario] = []
    
    def get_all_users(self):
        with get_session() as session:
            self.usuarios = session.exec(select(Usuario)).all()

    def add_user(self, form_data: dict):
        if not AuthState.es_admin:
            return rx.window_alert("No tienes permisos")
            
        with get_session() as session:
            nuevo = Usuario(
                nombre_usuario=form_data["nuevo_user"],
                password=form_data["nuevo_pass"],
                nivel=int(form_data["nivel"])
            )
            session.add(nuevo)
            session.commit()
        return [rx.window_alert("Usuario Creado"), self.get_all_users()]