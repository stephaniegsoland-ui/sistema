import reflex as rx
from ..states.stock_state import StockState

def inventory_row(item: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item["nombre"]),
        rx.table.cell(item["categoria"]),
        rx.table.cell(str(item["cantidad"])),
        rx.table.cell(
            rx.button(
                "Seleccionar",
                on_click=StockState.select_product(item["id"]),
                variant=rx.cond(StockState.selected_product_id == item["id"], "solid", "outline"),
                color_scheme="yellow",
                size="2",
            ),
            justify_content="flex-end",
        ),
        bg=rx.cond(StockState.selected_product_id == item["id"], "rgba(255, 215, 0, 0.08)", "transparent"),
    )


def management_view() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Gestión de Inventario", size="2", color="white"),
                rx.text("Cargar stock, ajustar cantidades y seguir movimientos de productos.", color="gray"),
                spacing="1",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Buscar producto...",
                    value=StockState.search_text,
                    on_change=StockState.set_search,
                    width="100%",
                    background_color="#111113",
                    border="1px solid #222225",
                    color="white",
                ),
                rx.select(
                    StockState.product_categories,
                    value=StockState.filter_category,
                    on_change=StockState.set_category,
                    width="260px",
                    background_color="#111113",
                    border="1px solid #222225",
                    color="white",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
            align_items="flex-end",
            spacing="4",
        ),

        rx.grid(
            rx.hstack(
                rx.box(
                    rx.text("Productos", color="gray", size="2"),
                    rx.heading(StockState.total_products.to(str), size="3", color="white"),
                    padding="18px",
                    background_color="#111113",
                    border="1px solid #222225",
                    border_radius="18px",
                    width="100%",
                ),
                rx.box(
                    rx.text("Unidades totales", color="gray", size="2"),
                    rx.heading(StockState.total_stock.to(str), size="3", color="white"),
                    padding="18px",
                    background_color="#111113",
                    border="1px solid #222225",
                    border_radius="18px",
                    width="100%",
                ),
                rx.box(
                    rx.text("Bajo stock", color="gray", size="2"),
                    rx.heading(StockState.low_stock_count.to(str), size="3", color="white"),
                    padding="18px",
                    background_color="#111113",
                    border="1px solid #222225",
                    border_radius="18px",
                    width="100%",
                ),
                gap="20px",
                width="100%",
            ),
            grid_template_columns="repeat(3, minmax(0, 1fr))",
            width="100%",
            gap="20px",
        ),

        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Inventario actual", weight="bold", color="white"),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Producto"),
                                rx.table.column_header_cell("Categoría"),
                                rx.table.column_header_cell("Cantidad"),
                                rx.table.column_header_cell("Acción"),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                StockState.filtered_products,
                                lambda item: inventory_row(item),
                            )
                        ),
                    ),
                ),
                padding="20px",
                background_color="#111113",
                border="1px solid #222225",
                border_radius="18px",
                width="100%",
                overflow_x="auto",
            ),
            rx.vstack(
                rx.card(
                rx.vstack(
                    rx.heading("Cargar / Actualizar Stock", size="3", color="white"),
                    rx.input(
                        placeholder="Nombre del producto",
                        value=StockState.input_nombre_producto,
                        on_change=StockState.set_input_nombre_producto,
                        width="100%",
                        background_color="#111113",
                        border="1px solid #222225",
                        color="white",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Tipo de material",
                            value=StockState.input_categoria_producto,
                            on_change=StockState.set_input_categoria_producto,
                            width="100%",
                            background_color="#111113",
                            border="1px solid #222225",
                            color="white",
                        ),
                        rx.button(
                            "Limpiar",
                            on_click=lambda: StockState.set_input_categoria_producto(""),
                            color_scheme="gray",
                            size="2",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.box(
                        rx.foreach(
                            StockState.material_type_suggestions,
                            lambda tipo: rx.button(
                                tipo,
                                on_click=StockState.set_input_categoria_producto(tipo),
                                size="2",
                                color_scheme=rx.cond(
                                    StockState.input_categoria_producto == tipo,
                                    "yellow",
                                    "gray",
                                ),
                                variant="outline",
                                min_width="100px",
                            ),
                        ),
                        display="flex",
                        flex_wrap="wrap",
                        gap="10px",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Cantidad",
                        value=StockState.input_cantidad_producto,
                        on_change=StockState.set_input_cantidad_producto,
                        width="100%",
                        background_color="#111113",
                        border="1px solid #222225",
                        color="white",
                        type="number",
                    ),
                    rx.button(
                        "Agregar / Actualizar",
                        on_click=StockState.add_or_update_product,
                        color_scheme="yellow",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="20px",
                background_color="#111113",
                border="1px solid #222225",
                border_radius="18px",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Ajuste de Stock", size="3", color="white"),
                    rx.text(rx.cond(StockState.selected_product != None, "Producto: " + StockState.selected_product_name, "Selecciona un producto"), color="gray"),
                    rx.input(
                        placeholder="Cantidad (+/-)",
                        value=StockState.input_ajuste_cantidad,
                        on_change=StockState.set_input_ajuste_cantidad,
                        width="100%",
                        background_color="#111113",
                        border="1px solid #222225",
                        color="white",
                        type="number",
                    ),
                    rx.input(
                        placeholder="Nota de ajuste",
                        value=StockState.input_ajuste_nota,
                        on_change=StockState.set_input_ajuste_nota,
                        width="100%",
                        background_color="#111113",
                        border="1px solid #222225",
                        color="white",
                    ),
                    rx.hstack(
                        rx.button(
                            "-1",
                            on_click=StockState.change_selected_stock(-1),
                            color_scheme="red",
                            width="100%",
                        ),
                        rx.button(
                            "+1",
                            on_click=StockState.change_selected_stock(1),
                            color_scheme="green",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.button(
                        "Aplicar Ajuste",
                        on_click=StockState.adjust_stock,
                        color_scheme="yellow",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="20px",
                background_color="#111113",
                border="1px solid #222225",
                border_radius="18px",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Historial de Movimientos", size="3", color="white"),
                    rx.text(
                        rx.cond(
                            StockState.selected_product != None,
                            "Mostrando movimientos para: " + StockState.selected_product_name,
                            "Movimientos recientes de todo el inventario"
                        ),
                        color="gray",
                        size="2",
                    ),
                    rx.box(
                        rx.foreach(
                            StockState.selected_movements,
                            lambda movement: rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(movement["producto_nombre"], weight="bold", color="white"),
                                        rx.text(f"{movement['tipo']} {movement['cambio']} unidades", size="2", color="gray"),
                                        rx.text(movement.get("nota", ""), size="2", color="#bbbbbb"),
                                    ),
                                    rx.spacer(),
                                    rx.text(movement["fecha"], size="2", color="gray"),
                                ),
                                rx.divider(border_color="#222225"),
                                spacing="2",
                                width="100%",
                            ),
                        ),
                        max_height="320px",
                        overflow_y="auto",
                        width="100%",
                    ),
                ),
                padding="20px",
                background_color="#111113",
                border="1px solid #222225",
                border_radius="18px",
            ),
            spacing="4",
            width="100%",
        ),
        grid_template_columns="2.5fr 1fr",
        gap="24px",
        align_items="start",
        width="100%",
    )
)