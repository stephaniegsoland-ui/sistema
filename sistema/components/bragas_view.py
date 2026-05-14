import reflex as rx
from ..states.stock_state import StockState

def bragas_view():
    return rx.vstack(
        rx.heading("Inventario de Bragas", color="gold", size="lg"),
        
        # Formulario de entrada
        rx.form(
            rx.hstack(
                rx.input(placeholder="Nombre (ej. Térmica)", name="nombre", id="nombre", bg="#222", border_color="#444"),
                rx.select(["S", "M", "L", "XL"], name="talla", placeholder="Talla"),
                rx.input(placeholder="Cant.", name="cantidad", type_="number", width="100px", bg="#222"),
                rx.button("Anexar", type_="submit", bg="gold", color="black", _hover={"bg": "orange"}),
                width="100%",
                spacing="4",
            ),
            on_submit=StockState.add_braga,
            padding="2em",
            bg="#111",
            border_radius="10px",
            width="100%",
        ),

        # Tabla de resultados
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Talla"),
                    rx.table.column_header_cell("Cantidad"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    StockState.bragas,
                    lambda b: rx.table.row(
                        rx.table.cell(b.nombre),
                        rx.table.cell(b.talla),
                        rx.table.cell(b.cantidad),
                    )
                )
            ),
            width="100%",
            variant="surface",
            color_scheme="yellow",
        ),
        width="100%",
        spacing="6",
    )