import reflex as rx
from .sidebar import sidebar

def layout(component: rx.Component) -> rx.Component:
    """Envuelve cualquier página con el sidebar."""
    return rx.hstack(
        sidebar(), # El sidebar ya no importa páginas
        rx.box(component, width="100%"), # Tu contenido a la derecha
        align_items="start",
        width="100%",
        height="100vh"
    )