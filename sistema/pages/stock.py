import reflex as rx
from ..states.stock_state import StockState
from ..components.sidebar import sidebar
from ..components.stock_dashboard import dashboard_view
from ..components.inventory_view import management_view


def menu_button(text, icon):
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=14), 
            rx.text(text, font_size="0.85em")
        ),
        on_click=lambda: StockState.set_view(text),
        variant="ghost",
        width="100%",
        justify_content="start",
        # Efecto de botón activo
        color=rx.cond(StockState.view == text, "white", "#888"),
        bg=rx.cond(StockState.view == text, "#333", "transparent"),
        _hover={"bg": "#222", "color": "white"},
        padding="0.6em",
        border_radius="5px"
    )

def stock_page():
    return rx.hstack(
        # NIVEL 1: Sidebar Principal (Negro total con secciones)
        sidebar(), # Importado de tus componentes existentes

        # NIVEL 2: Sidebar de Módulo (Soland Stock - Sistema de Inventario)
        rx.vstack(
            rx.vstack(
                rx.icon(tag="package", size=24, color="white"),
                rx.text("Soland Stock", font_weight="bold", color="white", font_size="1em"),
                rx.text("Sistema de Inventario", color="gray", font_size="0.7em"),
                align_items="center",
                width="100%",
                padding_y="1.5em",
            ),
            rx.divider(border_color="#222"),
            rx.vstack(
                menu_button("Resumen", "layout_dashboard"),
                menu_button("Herramientas", "wrench"),
                menu_button("Botas", "footprints"),
                menu_button("Bragas", "shirt"),
                menu_button("Suministros", "package"),
                menu_button("Lentes", "eye"),
                menu_button("Equipos", "monitor"),
                width="100%",
                spacing="1",
                padding="1em",
            ),
            width="200px",
            height="100vh",
            bg="#0f0f0f", # Un gris casi negro para diferenciar del principal
            border_right="1px solid #1a1a1a",
        ),

        # NIVEL 3: Contenido Dinámico (Dashboard o Tablas)
        rx.box(
            rx.cond(
                StockState.view == "Resumen",
                dashboard_view(),
                management_view()
            ),
            flex="1",
            padding="2em",
            bg="#050505",
            height="100vh",
            overflow_y="auto"
        ),
        width="100%",
        spacing="0",
        bg="black"
    )

