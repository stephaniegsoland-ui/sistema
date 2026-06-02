import reflex as rx
from sistema.components.sidebar import sidebar
from sistema.components.personal_view import formulario_registro, tabla_personal
from sistema.states.personal_state import PersonalState

@rx.page(route="/personal", title="Control de Personal - SOLAND", on_load=PersonalState.cargar_usuarios_bd)
def personal_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="/personal"),
        
        rx.box(
            rx.vstack(
                rx.heading("Control de Personal, Accesos y Permisos", size="7", color="#FFD700"),
                rx.flex(
                    formulario_registro(),
                    rx.box(tabla_personal(), flex="1", min_width="520px"),
                    spacing="8",
                    width="100%",
                    align_items="start",
                ),
                width="100%",
                spacing="4"
            ),
            flex="1",
            padding_y="2.5rem",
            padding_right="3rem",
            padding_left="260px",
            min_height="100vh",
            background_color="#09090b",
        ),
        width="100%",
        spacing="0",
        background_color="#09090b",
    )