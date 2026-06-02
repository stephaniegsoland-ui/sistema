import reflex as rx
from ..components.sidebar import sidebar
from ..states.reportes_state import ReportesState

def kpi_card(label: str, value: str, icon_tag: str, color: str) -> rx.Component:
    """Crea una tarjeta de indicador clave (KPI)"""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(label, size="2", color_alpha="0.7"),
                rx.heading(value, size="6", weight="bold"),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.center(
                rx.icon(tag=icon_tag, size=24, color=rx.color(color, 9)),
                bg=rx.color(color, 3),
                padding="0.5em",
                border_radius="md",
            ),
            width="100%",
            align="center",
        ),
        variant="surface",
        width="100%",
    )

@rx.page(route="/vehiculos/reportes", on_load=ReportesState.load_reportes)
def reportes_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="/vehiculos/reportes"),
        rx.box(
            rx.container(
                rx.vstack(
                    # --- Header de la página ---
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Historial de Inspecciones", size="7", weight="bold"),
                            rx.text("Administración centralizada de reportes de flota", color_secondary=True),
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.segmented_control.root(
                            rx.segmented_control.item("Resumen", value="Resumen"),
                            rx.segmented_control.item("Todos", value="Todos"),
                            rx.segmented_control.item("Recientes", value="Recientes"),
                            value=ReportesState.view_tab,
                            on_change=ReportesState.set_tab,
                            radius="large",
                            size="3",
                        ),
                        width="100%",
                        align="center",
                    ),

                    # --- Fila de KPIs ---
                    rx.grid(
                        kpi_card("Total Reportes", ReportesState.total_reportes.to(str), "file-text", "blue"),
                        kpi_card("Daños Detectados", ReportesState.total_con_dano.to(str), "alert-triangle", "amber"),
                        kpi_card("Unidades Operativas", ReportesState.total_sin_dano.to(str), "check-circle", "green"),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),

                    # --- Barra de Acciones y Filtros ---
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="filter", size=18),
                                rx.text("Filtros de búsqueda", weight="bold"),
                                spacing="2",
                            ),
                            rx.form(
                                rx.flex(
                                    rx.input(placeholder="Placa...", name="placa", width="150px"),
                                    rx.input(placeholder="Modelo...", name="modelo", width="150px"),
                                    rx.select(["SIN DAÑOS", "DAÑO DETECTADO"], placeholder="Estado", name="filter_estado", width="180px"),
                                    rx.input(type_="date", name="fecha_desde", width="160px"),
                                    rx.button("Filtrar", type_="submit", color_scheme="amber"),
                                    rx.button(rx.icon(tag="refresh-ccw", size=16), on_click=ReportesState.reset_filters, variant="soft"),
                                    spacing="3",
                                    flex_wrap="wrap",
                                ),
                                on_submit=ReportesState.apply_filters,
                            ),
                        ),
                        width="100%",
                    ),

                    # --- Contenido Dinámico ---
                    rx.cond(
                        ReportesState.view_tab == "Todos",
                        rx.card(
                            rx.vstack(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Unidad"),
                                            rx.table.column_header_cell("Responsable"),
                                            rx.table.column_header_cell("Fecha"),
                                            rx.table.column_header_cell("Estado"),
                                            rx.table.column_header_cell("Acción"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            ReportesState.reportes_filtrados.to(list[dict]),
                                            lambda item: rx.table.row(
                                                rx.table.cell(rx.text(item["placa"], weight="bold")),
                                                rx.table.cell(item["responsable"]),
                                                rx.table.cell(item["fecha"].to(str)[0:10]),
                                                rx.table.cell(
                                                    rx.badge(
                                                        item["estado_final"],
                                                        color_scheme=rx.cond(item["estado_final"] == "SIN DAÑOS", "green", "red"),
                                                        variant="soft",
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.button("Detalle", size="1", variant="ghost", on_click=lambda: ReportesState.select_report(item["id"]))
                                                ),
                                            )
                                        )
                                    ),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(rx.icon(tag="file-down", size=16), "Excel", color_scheme="green", on_click=ReportesState.export_to_excel),
                                    padding_top="1em",
                                    width="100%",
                                ),
                            ),
                            width="100%",
                        ),
                    ),
                    
                    # --- Modal de Detalle (Condicional) ---
                    rx.cond(
                        ReportesState.selected_report_id,
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.badge(f"ID: {ReportesState.selected_report_id}", variant="outline"),
                                    rx.heading(f"Detalle Unidad {ReportesState.selected_report['placa']}", size="4"),
                                    rx.spacer(),
                                    rx.icon_button("x", on_click=ReportesState.clear_selected_report, variant="ghost"),
                                    width="100%", align="center",
                                ),
                                rx.separator(),
                                rx.grid(
                                    rx.vstack(
                                        rx.text("Recomendación Técnica", weight="bold", size="2"),
                                        rx.text(ReportesState.selected_report['recomendacion'], color_secondary=True, size="2"),
                                        rx.text("Hallazgos", weight="bold", size="2", padding_top="1em"),
                                        rx.text(ReportesState.selected_report['hallazgos_text'], size="2", white_space="pre-line"),
                                        align_items="start",
                                    ),
                                    rx.hstack(
                                        rx.image(src=rx.get_upload_url(ReportesState.selected_report['url_lunes']), border_radius="md", width="150px"),
                                        rx.image(src=rx.get_upload_url(ReportesState.selected_report['url_viernes']), border_radius="md", width="150px"),
                                        spacing="3",
                                    ),
                                    columns="2",
                                    spacing="4",
                                    width="100%",
                                ),
                            ),
                            width="100%",
                            border=f"1px solid {rx.color('amber', 7)}",
                        ),
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
        spacing="0",
        width="100%",
    )