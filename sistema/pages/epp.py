import reflex as rx
from ..components.sidebar import sidebar # El negro
from ..components.epp_view import epp_analysis_view         # El contenido de arriba
from .stock import menu_button                             # Estilo de botones

@rx.page(route="/epp", title="Seguridad - SOLAND")
def epp_page():
    return rx.hstack(
        # NIVEL 1: Sidebar Global
        sidebar(),

        # NIVEL 2: Sidebar del Módulo Seguridad
        rx.vstack(
            rx.text("SEGURIDAD", font_weight="bold", color="gold", padding="1em"),
            rx.divider(border_color="#222"),
            rx.vstack(
                menu_button("Escáner", "camera"),
                menu_button("Reportes", "file_text"),
                width="100%", padding="1em",
            ),
            width="200px", height="100vh", bg="#0f0f0f",
        ),

        # NIVEL 3: Contenido Dinámico
        rx.box(
            epp_analysis_view(),
            flex="1",
            padding="2em",
            bg="#050505",
            height="100vh",
            overflow_y="auto",
        ),
        spacing="0",
        width="100%",
    )