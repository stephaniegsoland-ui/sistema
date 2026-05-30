import reflex as rx
from ..states.stock_state import StockState

def stock_resumen_view() -> rx.Component:
    return rx.vstack(
        rx.text("Filtros rápidos:"),
        rx.hstack(
            rx.button(
                "Todos", 
                on_click=lambda: StockState.set_filter("Todos"), 
                variant="surface"
            ),
            rx.button(
                "Herramientas", 
                on_click=lambda: StockState.set_filter("Herramientas"), 
                variant="surface"
            ),
        ),
        width="100%"
    )