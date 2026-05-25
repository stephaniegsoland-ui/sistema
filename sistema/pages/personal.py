import reflex as rx
from sistema.components.sidebar import sidebar 
from sistema.components.personal_view import barra_simulacion_login, formulario_registro, tabla_personal
from sistema.states.personal_state import PersonalState, SessionState

@rx.page(route="/personal", title="SOLAND - Personal", on_load=PersonalState.cargar_usuarios_bd)
def personal_page() -> rx.Component:
    return rx.hstack(
     
        
        # 2. Contenido de trabajo empujado exactamente lo necesario (260px del sidebar + espacio de aire)
        rx.vstack(
            barra_simulacion_login(),
            
            # Verificación por nivel (Nivel 1 es Administrador)
            rx.cond(
                SessionState.nivel_usuario == 1,
                rx.vstack(
                    rx.heading("Control de Personal, Accesos y Hojas de Vida", size="7", color="#FFD700"),
                    rx.flex(
                        formulario_registro(),
                        rx.box(tabla_personal(), flex="1", min_width="500px"),
                        spacing="5",
                        width="100%",
                        direction=rx.cond(rx.breakpoints({"sm": True, "md": False}), "column", "row")
                    ),
                    width="100%",
                    spacing="4"
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("lock", size=45, color="red"),
                        rx.heading("Módulo Restringido", size="5", color="red"),
                        rx.text("Tu nivel de acceso no tiene permisos de administración de personal.", color="gray"),
                        align="center",
                        spacing="2"
                    ),
                    height="60vh",
                    width="100%"
                )
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding_y="2rem",
        padding_right="2rem",
        padding_left="290px",  # Espaciado perfecto respecto al sidebar fijo
        background_color="#09090b",
        min_height="100vh",
        align_items="start",
        spacing="0"
    )