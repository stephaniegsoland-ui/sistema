import reflex as rx
from ..states.stock_state import StockState

def management_view():
    return rx.vstack(
        rx.hstack(
            rx.heading(f"Gestión de {StockState.view}", color="gold"),
            rx.spacer(),
            rx.button("Excel", icon="download", on_click=StockState.export_to_excel, color_scheme="green")
        ),
        rx.form(
            rx.hstack(
                rx.input(placeholder="Nombre", name="nombre", id="nombre"),
                rx.input(placeholder="Detalle/Talla", name="detalle", id="detalle"),
                rx.input(placeholder="Cant.", name="cantidad", id="cantidad", type_="number", width="100px"),
                rx.button("Anexar", type_="submit", bg="gold", color="black"),
            ),
            on_submit=StockState.add_item, bg="#111", padding="1em", border_radius="10px", width="100%"
        ),
        rx.table.root(
            rx.table.header(rx.table.row(rx.table.column_header_cell("Ítem"), rx.table.column_header_cell("Detalle"), rx.table.column_header_cell("Stock"))),
            rx.table.body(
                rx.foreach(StockState.inventory[StockState.view], lambda i: rx.table.row(
                    rx.table.cell(i.nombre), rx.table.cell(i.detalle), rx.table.cell(i.cantidad)
                ))
            ),
            width="100%", variant="surface"
        ),
        width="100%", spacing="4"
    )