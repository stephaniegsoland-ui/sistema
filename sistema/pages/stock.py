# sistema/pages/stock.py
import reflex as rx
from sistema.states.stock_state import StockState
from sistema.states.inventory_state import InventoryState
from sistema.components.sidebar import sidebar
from sistema.components.inventory_view import management_view
from sistema.components.stock_chart import stock_resumen_view
from sistema.components.crud_form import category_form_component

def main_content_area() -> rx.Component:
    """Renderiza el contenido dinámico central según la categoría seleccionada."""
    return rx.box(
        rx.cond(
            InventoryState.current_category == "Resumen",
            # 1. Cuando está en Resumen, monta tus KPIs y Gráficos reales de stock_chart
            stock_resumen_view(), 
            
            # 2. Cuando hace clic en Herramientas, Botas, etc., monta el formulario y la tabla
            rx.hstack(
                # Columna Izquierda: Formulario adaptativo de inserción
                category_form_component(),
                
                # Columna Derecha: Contenedor para la tabla de la BD o gestión existente
                rx.vstack(
                    rx.heading(f"Registros actuales en {InventoryState.current_category}", size="2", color="gray"),
                    # Aquí puedes mapear la tabla dinámica de productos
                    management_view(), 
                    width="100%",
                    padding="14px",
                    background_color="#111113",
                    border="1px solid #222225",
                    border_radius="8px"
                ),
                spacing="4",
                align_items="start",
                width="100%"
            )
        ),
        width="100%"
    )

def menu_button(text, icon):
    """Botón del menú que actualiza el estado global al hacer clic."""
    # Sincronizamos ambos estados para que la app sepa qué renderizar
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=14),
            rx.text(text, font_size="0.85em")
        ),
        on_click=[
            StockState.set_view(text), 
            InventoryState.set_category(text)
        ],
        variant="ghost",
        width="100%",
        justify_content="start",
        color=rx.cond(InventoryState.current_category == text, "white", "#888"),
        bg=rx.cond(InventoryState.current_category == text, "#222225", "transparent"),
        _hover={"bg": "#141416", "color": "white"},
        padding="0.7em 0.9em",
        border_radius="8px"
    )

@rx.page(route="/stock", title="Stock - SOLAND", on_load=StockState.load_products)
def stock_page() -> rx.Component:
    """Página raíz del inventario. Aquí se une el Layout Completo."""
    return rx.hstack(
        # Tu Sidebar importado
        sidebar(current_page="/stock"),

        # Menú Interno de Categorías (Módulos de Soland Stock)
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
                menu_button("Resumen", "layout-dashboard"),
                menu_button("Todos", "grid"),
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
            width="220px",
            min_height="100vh",
            bg="#0f0f0f",
            border_right="1px solid #1a1a1a",
        ),

        # Espacio de Contenido Central
        rx.box(
            main_content_area(),
            flex="1",
            padding="2em",
            bg="#050505",
            min_height="100vh",
            overflow_y="auto"
        ),
        width="100%",
        spacing="0",
        bg="black"
    )