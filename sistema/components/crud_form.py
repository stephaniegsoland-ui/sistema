# sistema/components/crud_form.py
import reflex as rx
from sistema.states.inventory_state import InventoryState
from sistema.states.stock_state import StockState

def input_field(
    placeholder: str,
    value: str,
    on_change,
    icon: str,
    type_field: str = "text",
):
    """Genera un campo de texto integrado y estilizado perfectamente para el Dashboard oscuro"""
    return rx.hstack(
        rx.icon(tag=icon, color="gray", size=16),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=type_field,
            variant="surface",
            color_scheme="gray",
            width="100%",
            style={
                "background_color": "transparent",
                "color": "white",
                "border": "none",
            },
        ),
        padding_x="12px",
        padding_y="6px",
        background_color="#141416",
        border="1px solid #222225",
        border_radius="6px",
        width="100%",
        align_items="center",
    )


def category_form_component() -> rx.Component:
    """Formulario dinámico de categoría para gestión de inventario."""
    return rx.card(
        rx.vstack(
            rx.heading("Formulario de Inventario", size="2", color="white"),
            rx.text(
                rx.cond(
                    InventoryState.current_category == "Resumen",
                    "Selecciona una categoría para registrar ítems.",
                    f"Categoría activa: {InventoryState.current_category}",
                ),
                color="gray",
                size="1",
            ),
            rx.box(
                rx.text("Categoría", color="gray", size="2"),
                rx.button(
                    rx.cond(
                        (InventoryState.current_category != "Resumen") & (InventoryState.current_category != "Todos"),
                        InventoryState.current_category,
                        "Elegir categoría",
                    ),
                    color_scheme="yellow",
                    variant="outline",
                    size="2",
                    width="100%",
                    justify_content="left",
                ),
                width="100%",
                padding="10px 0",
            ),
            rx.form(
                input_field(
                    "Nombre del producto",
                    StockState.input_nombre_producto,
                    StockState.set_input_nombre_producto,
                    "box",
                ),
                input_field(
                    "Cantidad",
                    StockState.input_cantidad_producto,
                    StockState.set_input_cantidad_producto,
                    "plus",
                    type_field="number",
                ),
                input_field(
                    "Tipo de material",
                    StockState.input_categoria_producto,
                    StockState.set_input_categoria_producto,
                    "layers",
                ),
                rx.button(
                    "Guardar",
                    type_="submit",
                    color_scheme="yellow",
                    width="100%",
                ),
                on_submit=StockState.add_or_update_product,
                spacing="4",
                width="100%",
            ),
        ),
        padding="22px",
        background_color="#111113",
        border="1px solid #222225",
        border_radius="18px",
        width="100%",
    )