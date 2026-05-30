import reflex as rx
from ..states.stock_state import StockState

def management_view() -> rx.Component:
    return rx.vstack(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Producto"),
                    rx.table.column_header_cell("Cantidad"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    StockState.filtered_stock,
                    lambda i: rx.table.row(
                        rx.table.cell(i.nombre),
                        rx.table.cell(i.cantidad),
                    )
                )
            ),
        ),
        width="100%"
    )