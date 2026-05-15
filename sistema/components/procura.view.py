import reflex as rx
from ..components.sidebar import sidebar
from ..states.procura_state import ProcuraState


def status_badge(value: bool, true_label: str, false_label: str):
    return rx.badge(
        true_label if value else false_label,
        color_scheme=rx.cond(value, "green", "orange"),
        variant="soft",
    )


@rx.page(route="/procura", title="Procura de Materiales - SOLAND", on_load=ProcuraState.load_solicitudes)
def procura_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="/procura"),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Procura de Materiales", size="7", weight="bold"),
                            rx.text("Solicita materiales, haz seguimiento y actualiza el estado de revisión, compra y envío.", color_secondary=True),
                            align_items="start",
                        ),
                        rx.segmented_control.root(
                            rx.segmented_control.item("Todas", value="Todas"),
                            rx.segmented_control.item("Pendientes", value="Pendientes"),
                            rx.segmented_control.item("Revisadas", value="Revisadas"),
                            rx.segmented_control.item("Compradas", value="Compradas"),
                            rx.segmented_control.item("Enviadas", value="Enviadas"),
                            value=ProcuraState.view_tab,
                            on_change=ProcuraState.set_tab,
                            radius="large",
                            size="3",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.grid(
                        rx.card(
                            rx.vstack(
                                rx.text("Solicitudes Totales", color_alpha="0.8"),
                                rx.heading(ProcuraState.total_solicitudes.to(str), size="5", weight="bold"),
                            ),
                            variant="surface",
                            padding="1.2em",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Pendientes de revisión", color_alpha="0.8"),
                                rx.heading(ProcuraState.total_pendientes.to(str), size="5", weight="bold"),
                            ),
                            variant="surface",
                            padding="1.2em",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Materiales comprados", color_alpha="0.8"),
                                rx.heading(ProcuraState.total_compradas.to(str), size="5", weight="bold"),
                            ),
                            variant="surface",
                            padding="1.2em",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Materiales enviados", color_alpha="0.8"),
                                rx.heading(ProcuraState.total_enviadas.to(str), size="5", weight="bold"),
                            ),
                            variant="surface",
                            padding="1.2em",
                        ),
                        columns="4",
                        spacing="4",
                        width="100%",
                    ),

                    rx.card(
                        rx.vstack(
                            rx.text("Nueva solicitud al departamento", weight="bold"),
                            rx.form(
                                rx.grid(
                                    rx.input(placeholder="Solicitante", name="solicitante", width="100%"),
                                    rx.select(ProcuraState.departamentos, placeholder="Departamento receptor", name="departamento", width="100%"),
                                    rx.select(ProcuraState.categorias, placeholder="Categoría", name="categoria", width="100%"),
                                    rx.input(placeholder="Material requerido", name="material", width="100%"),
                                    rx.input(placeholder="Cantidad", name="cantidad", type_="number", width="100%"),
                                    rx.input(type_="date", name="fecha_entrega", width="100%"),
                                    rx.select(["Normal", "Urgente"], placeholder="Prioridad", name="prioridad", width="100%"),
                                    rx.textarea(placeholder="Detalle / propósito / Observaciones", name="detalle", width="100%", grid_column="span 2"),
                                    rx.button("Solicitar Material", type_="submit", color_scheme="gold"),
                                    columns="2",
                                    gap="1.5em",
                                ),
                                on_submit=ProcuraState.crear_solicitud,
                                width="100%",
                            ),
                        ),
                        variant="surface",
                        padding="1.5em",
                        width="100%",
                    ),

                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Seguimiento de solicitudes", weight="bold"),
                                rx.spacer(),
                                rx.input(placeholder="Buscar por material o solicitante...", on_change=ProcuraState.set_search, width="300px"),
                                rx.button(rx.icon(tag="download"), variant="ghost"),
                            ),
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("#"),
                                        rx.table.column_header_cell("Solicitante"),
                                        rx.table.column_header_cell("Departamento"),
                                        rx.table.column_header_cell("Material"),
                                        rx.table.column_header_cell("Cant."),
                                        rx.table.column_header_cell("Estado Actual"),
                                        rx.table.column_header_cell("Acciones"),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        ProcuraState.solicitudes_filtradas,
                                        lambda item: rx.table.row(
                                            rx.table.cell(str(item.id)),
                                            rx.table.cell(item.solicitante),
                                            rx.table.cell(item.departamento),
                                            rx.table.cell(item.material),
                                            rx.table.cell(str(item.cantidad)),
                                            rx.table.cell(status_badge(item.revisado, "Sí", "No")),
                                            rx.table.cell(status_badge(item.comprado, "Sí", "No")),
                                            rx.table.cell(status_badge(item.enviado, "Sí", "No")),
                                            rx.table.cell(
                                                rx.hstack(
                                                    rx.button(
                                                        "Revisado",
                                                        size="1",
                                                        variant="outline",
                                                        disabled=item.revisado,
                                                        on_click=lambda request_id=item.id: ProcuraState.marcar_revisado(request_id),
                                                    ),
                                                    rx.button(
                                                        "Comprado",
                                                        size="1",
                                                        variant="outline",
                                                        disabled=not item.revisado or item.comprado,
                                                        on_click=lambda request_id=item.id: ProcuraState.marcar_comprado(request_id),
                                                    ),
                                                    rx.button(
                                                        "Enviado",
                                                        size="1",
                                                        variant="outline",
                                                        disabled=not item.comprado or item.enviado,
                                                        on_click=lambda request_id=item.id: ProcuraState.marcar_enviado(request_id),
                                                    ),
                                                    spacing="2",
                                                    wrap="wrap",
                                                )
                                            ),
                                        )
                                    )
                                ),
                                width="100%",
                            ),
                        ),
                        variant="surface",
                        padding="1.5em",
                        width="100%",
                        border=f"1px solid rgba(255,215,0,0.15)",
                    ),
                    spacing="6",
                    width="100%",
                ),
                padding_y="2em",
                size="4",
            ),
            width="100%",
            bg="#09090b",
            min_height="100vh",
        ),
        width="100%",
    )
