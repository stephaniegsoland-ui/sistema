import reflex as rx
from ..states.auth_state import AuthState
from ..styles.colors import ACCENT_YELLOW, CARD_BG

def login_page():
    return rx.center(
        rx.form(
            rx.vstack(
                rx.heading("ACCESO SEGURO", color=ACCENT_YELLOW),
                rx.input(placeholder="Usuario", name="username", width="100%"),
                rx.input(placeholder="Contraseña", name="password", type="password", width="100%"),
                
                rx.cond(
                    AuthState.error_message != "",
                    rx.text(AuthState.error_message, color="red", size="2")
                ),
                
                rx.button("INGRESAR AL SISTEMA", type="submit", width="100%", background_color=ACCENT_YELLOW, color="black"),
                spacing="4",
                padding="40px",
                background_color=CARD_BG,
                border=f"1px solid {ACCENT_YELLOW}",
                border_radius="10px"
            ),
            on_submit=AuthState.login,
        ),
        height="100vh",
    )