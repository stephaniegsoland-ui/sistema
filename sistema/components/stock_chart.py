import reflex as rx
from ..states.stock_state import StockState

def kpi_card(title: str, value: str, icon: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.icon(tag=icon, size=18, color="#FBBF24"), rx.text(title, size="2", color="gray"), spacing="2"),
            rx.heading(value, size="3", color="white"),
        ),
        padding="20px",
        background_color="#111113",
        border="1px solid #222225",
        border_radius="18px",
        width="100%",
        min_height="120px",
    )


def chart_card(title: str, content: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(title, weight="bold", color="gray"),
            content,
        ),
        padding="22px",
        background_color="#111113",
        border="1px solid #222225",
        border_radius="18px",
        width="100%",
    )


def category_bar_chart() -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#222225", vertical=False),
        rx.recharts.x_axis(data_key="categoria", stroke="gray", style={"fontSize": 12}, interval=0, angle=-20, text_anchor="end"),
        rx.recharts.y_axis(stroke="gray", style={"fontSize": 12}),
        rx.recharts.tooltip(content_style={"background": "#111113", "border": "1px solid #222225", "color": "white"}),
        rx.recharts.bar(data_key="cantidad", fill="#F59E0B", radius=[8, 8, 0, 0], name="Unidades"),
        data=StockState.category_summary,
        width="100%",
        height=280,
    )


def movement_area_chart() -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#222225"),
        rx.recharts.x_axis(data_key="fecha", stroke="gray", style={"fontSize": 12}),
        rx.recharts.y_axis(stroke="gray", style={"fontSize": 12}),
        rx.recharts.tooltip(content_style={"background": "#111113", "border": "1px solid #222225", "color": "white"}),
        rx.recharts.area(data_key="cantidad", stroke="#38BDF8", fill="#38BDF8", fill_opacity=0.18, name="Movimientos"),
        data=StockState.movement_trend,
        width="100%",
        height=240,
    )


def movement_pie_chart() -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=StockState.movement_type_summary,
            data_key="cantidad",
            name_key="tipo",
            inner_radius=50,
            outer_radius=80,
            label=True,
            fill="#FBBF24",
        ),
        rx.recharts.graphing_tooltip(),
        height=260,
    )


def stock_resumen_view() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Resumen de Stock", size="2", color="white"),
                rx.text("Monitorea inventario, movimientos y alertas en tiempo real.", color="gray"),
            ),
            rx.spacer(),
            rx.input(
                placeholder="Buscar producto...",
                value=StockState.search_text,
                on_change=StockState.set_search,
                width="320px",
                size="2",
                background_color="#111113",
                border="1px solid #222225",
                color="white",
            ),
            width="100%",
            align_items="center",
            spacing="4",
            margin_bottom="20px",
        ),

        rx.grid(
            kpi_card("Unidades totales", StockState.total_stock.to(str), "layers"),
            kpi_card("Productos", StockState.total_products.to(str), "box"),
            kpi_card("Categorías", StockState.total_categories.to(str), "tag"),
            kpi_card("Bajo stock", StockState.low_stock_count.to(str), "alert_triangle"),
            columns="4",
            spacing="4",
            width="100%",
            margin_bottom="24px",
        ),

        rx.box(
            rx.text("Filtros de categoría", weight="bold", color="gray"),
            rx.hstack(
                rx.foreach(
                    StockState.product_categories,
                    lambda category: rx.button(
                        category,
                        on_click=StockState.set_category(category),
                        variant=rx.cond(StockState.filter_category == category, "solid", "outline"),
                        color_scheme="yellow",
                            size="2",
                        border_radius="full",
                    ),
                ),
                spacing="2",
                wrap="wrap",
            ),
            padding="18px 0 6px",
            width="100%",
            margin_bottom="24px",
        ),

        rx.grid(
            chart_card("Stock por Categoría", category_bar_chart()),
            rx.vstack(
                chart_card("Movimientos Recientes", rx.vstack(
                    rx.foreach(
                        StockState.recent_movements,
                        lambda item: rx.hstack(
                            rx.vstack(
                                rx.text(item["producto_nombre"], weight="bold", color="white"),
                                rx.text(f"{item['tipo']} {item['cambio']} unidades", size="2", color="gray"),
                                rx.text(item["fecha"], size="1", color="gray"),
                            ),
                            rx.spacer(),
                            rx.badge(item["tipo"], color_scheme=rx.cond(item["tipo"] == "Ingreso", "green", "red"), variant="solid", size="2"),
                            width="100%",
                            align_items="center",
                            spacing="3",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                )),
                chart_card("Tendencia de Movimiento", movement_area_chart()),
                spacing="4",
                width="100%",
            ),
            grid_template_columns="1.5fr 1fr",
            spacing="4",
            width="100%",
        ),

        rx.grid(
            chart_card("Movimientos por Tipo", movement_pie_chart()),
            chart_card("Mejores Productos", rx.vstack(
                rx.foreach(
                    StockState.top_products,
                    lambda item: rx.hstack(
                        rx.vstack(
                            rx.text(item["nombre"], weight="bold", color="white"),
                            rx.text(item["categoria"], size="2", color="gray"),
                        ),
                        rx.spacer(),
                        rx.text(str(item["cantidad"]), color="white", weight="bold"),
                        width="100%",
                        align_items="center",
                    ),
                ),
                spacing="3",
                width="100%",
            )),
            grid_template_columns="1fr 1fr",
            spacing="4",
            width="100%",
        ),
    )