import reflex as rx
from ..states.procura_state import ProcuraState
from ..components.sidebar import sidebar
from ..pages.procura import procura_page

from typing import List


def kpi_card_mini(title: str, value: str, icon: str, color: str):
    return rx.card(
        rx.hstack(
            rx.center(
                rx.icon(tag=icon, size=20, color=rx.color(color, 9)),
                bg=rx.color(color, 3),
                padding="8px",
                border_radius="8px",
                box_shadow=f"0 0 10px {rx.color(color, 5)}",
            ),
            rx.vstack(
                rx.text(title, size="1", color_secondary=True, margin_bottom="-5px"),
                rx.heading(value, size="4", weight="bold"),
                align_items="start",
                spacing="0",
            ),
            spacing="3",
            align="center",
        ),
        variant="surface",
        border=f"1px solid {rx.color(color, 4)}",
        padding="10px",
    )

def actividad_item(act: dict):
    return rx.hstack(
        rx.badge(act["status"], color_scheme="amber", variant="soft", size="1"),
        rx.vstack(
            rx.text(act["descripcion"], size="2", weight="medium"),
            rx.text(act["info"], size="1", color_secondary=True),
            spacing="0", align_items="start",
        ),
        rx.spacer(),
        rx.icon(tag="clock", size=12, color="gray"),
        width="100%", align="center", padding_y="2",
        border_bottom=f"1px solid {rx.color('gray', 3)}",
    )

def render_report_table():
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(tag="file-text", size=20, color="#FFD700"),
                    rx.heading("Reporte Detallado de Solicitudes", size="4"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(rx.icon(tag="download", size=16), rx.text("Exportar PDF")),
                    size="1", 
                    variant="outline",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
                padding_bottom="10px",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Solicitante"),
                        rx.table.column_header_cell("Material"),
                        rx.table.column_header_cell("Cant."),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Prioridad"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        ProcuraState.tabla_reporte_pedidos,
                        lambda item: rx.table.row(
                            rx.table.cell(item["id"]),
                            rx.table.cell(item["solicitante"]),
                            rx.table.cell(item["material"]),
                            rx.table.cell(item["cantidad"]),
                            rx.table.cell(
                                rx.badge(
                                    item["estado"], 
                                    color_scheme=rx.cond(item["estado"] == "Finalizado", "green", "amber"),
                                    variant="soft"
                                )
                            ),
                            rx.table.cell(
                                rx.text(
                                    item["prioridad"], 
                                    color=rx.cond(item["prioridad"] == "Alta", "red", "gray"),
                                    weight=rx.cond(item["prioridad"] == "Alta", "bold", "medium")
                                )
                            ),
                        ),
                    ),
                ),
                width="100%",
                variant="surface", 
            ),
            width="100%",
            spacing="0",
        ),
        width="135%", 
        margin_top="1em",
    )

def actividad_item(act: dict):
    """Renderiza una fila individual en la lista de actividad reciente"""
    return rx.hstack(
        rx.badge(
            act["status"], 
            color_scheme=rx.cond(act["status"] == "Enviado", "green", "amber"),
            variant="soft",
            size="1"
        ),
        rx.vstack(
            rx.text(act["descripcion"], size="2", weight="medium"),
            rx.text(act["info"], size="1", color_secondary=True),
            spacing="0",
            align_items="start",
        ),
        rx.spacer(),
        rx.icon(tag="clock", size=12, color="gray"),
        width="100%",
        align="center",
        padding_y="2",
        border_bottom=f"1px solid {rx.color('gray', 3)}",
    )

def render_advanced_stats() -> rx.Component:
    return rx.vstack(
        # Tarjetas de Resumen
        rx.grid(
            kpi_card_mini("Total Pedidos", ProcuraState.total_solicitudes.to(str), "shopping-bag", "amber"),
            kpi_card_mini("Por Entregar", ProcuraState.total_pendientes.to(str), "clock", "blue"),
            kpi_card_mini("Eficiencia", "92%", "zap", "green"),
            kpi_card_mini("Prom. Entrega", "3.5 días", "timer", "purple"),
            columns="4",
            spacing="6",
            width="134%",
        ),
        
        # Gráficas Principales
        rx.grid(
            # Gráfica de Embudo (Donut Chart)
            rx.card(
                rx.vstack(
                    rx.text("Estado del Ciclo Logístico", weight="bold"),
                    rx.recharts.pie_chart(
                        rx.recharts.pie(
                            data=ProcuraState.stats_embudo_progreso,
                            data_key="value",
                            name_key="name",
                            inner_radius=60,
                            outer_radius=80,
                            padding_angle=5,
                            fill=rx.color("amber", 8),
                            label=True,
                        ),
                        rx.recharts.graphing_tooltip(),
                        height=300,
                    ),
                    width="100%",
                )
            ),
            # Gráfica de Departamentos
            rx.card(
                rx.vstack(
                    rx.text("Distribución por Departamento", weight="bold"),
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="pedidos", 
                            fill=rx.color("blue", 9),
                            radius=[4, 4, 0, 0], # Redondeado solo arriba para un look moderno
                            label={"position": "top", "fill": "gray", "fontSize": 12}, # Muestra el número arriba de la barra
                        ),
                        rx.recharts.x_axis(data_key="name"),
                        rx.recharts.y_axis(),
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False), # Guías horizontales sutiles
                        data=ProcuraState.top_departamentos_gastos,
                        height=250,
                        width="100%",
                    ),
                    width="100%",
                )
            ),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="list-todo", size=18, color=rx.color("amber", 9)),
                        rx.text("Actividad Reciente", weight="bold"),
                    ),
                    rx.separator(),
                    # Usamos un vstack con scroll interno
                    rx.vstack(
                        rx.foreach(
                            ProcuraState.actividad_reciente, 
                            lambda item:actividad_item(item)
                        ), 
                        width="100%",
                        spacing="1",
                        max_height="250px", # Altura fija para que no crezca infinito
                        overflow_y="auto",   # Scroll si hay muchos items
                    ),
                    width="100%",
                ),
            ),
            rx.card(rx.vstack(rx.text("Tendencia de Consumo", weight="bold"), rx.recharts.area_chart(
            rx.recharts.area(data_key="total", stroke="#FFD700", fill="#FFD700", fill_opacity=0.1),
            rx.recharts.x_axis(data_key="mes"), rx.recharts.y_axis(),
            rx.recharts.graphing_tooltip(), data=ProcuraState.data_historica, width="100%", height=200))),
            columns="4", # Cambiamos a 4 columnas para llenar el ancho
            spacing="4",
            width="135%",
        ),
    )
