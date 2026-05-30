import reflex as rx
from sistema.states.personal_state import SessionState

def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("SOLAND", size="7", color="#FFD700", margin_bottom="2px"),
            rx.text("Sistema de Suministros - Acceso", size="2", color="gray", margin_bottom="15px"),
            
            # Asegúrate de que use SessionState
            rx.input(
                placeholder="Nombre de Usuario", 
                value=SessionState.username_input,
                on_change=SessionState.set_username_input,
                width="100%",
                size="3"
            ),
            rx.input(
                placeholder="Contraseña", 
                type="password",
                value=SessionState.password_input, # ¡Ojo aquí! Tenías un typo con username_input antes
                on_change=SessionState.set_password_input,
                width="100%",
                size="3"
            ),
            
            rx.button(
                "Iniciar Sesión", 
                on_click=SessionState.login_usuario,
                color_scheme="yellow", 
                width="100%",
                size="3",
                margin_top="10px"
            ),
            
            spacing="3",
            width="100%",
            max_width="360px",
            padding="6",
            background_color="#111113",
            border="1px solid #222225",
            border_radius="var(--radius-4)",
        ),
        height="100vh",
        background_color="#0b0b0b"
    )