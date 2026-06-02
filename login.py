import reflex as rx
from ..states.auth import AuthState

def login_page():
    return rx.center(
        rx.vstack(
            rx.heading("Iniciar Sesión"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Usuario", name="username"),
                    rx.input(
                        placeholder="Contraseña", 
                        name="password", 
                        type_="password"
                    ),
                    rx.button(
                        "Entrar", 
                        type_="submit", 
                        width="100%",
                        loading=AuthState.cargando
                    ),
                ),
                on_submit=AuthState.login,
            ),
            padding="2em",
            border="1px solid #ddd",
            border_radius="10px",
        ),
        height="100vh",
    )