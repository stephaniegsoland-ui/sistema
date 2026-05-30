import reflex as rx
from ..api.models import Usuario
from ..states.auth import AuthState

class PersonalState(rx.State):
    def registrar_personal(self, form_data: dict):
        nombre = form_data.get("nombre")
        clave = form_data.get("clave")

        if not nombre or not clave:
            return rx.window_alert("Error: Faltan datos")

        with rx.session() as session:
            nuevo = Usuario(
                nombre_usuario=nombre,
                password=clave, # En producción, usa hashing
                nivel=2,        # Nivel Personal
                estado="ACTIVO"
            )
            session.add(nuevo)
            session.commit()
        
        return rx.window_alert(f"Personal {nombre} creado. ¡Ya puede iniciar sesión!")

def personal_page():
    return rx.vstack(
        rx.heading("Registro de Personal"),
        rx.form(
            rx.vstack(
                rx.input(placeholder="Nombre de Usuario", name="nombre"),
                rx.input(placeholder="Contraseña", name="clave", type_="password"),
                rx.button("Crear Usuario de Personal", type_="submit"),
            ),
            on_submit=PersonalState.registrar_personal,
        ),
    )