import reflex as rx
from ..states.stock_state import StockState

def summary_card(title: str, count: int, icon: str, color: str):
    return rx.vstack(
        rx.hstack(
            rx.icon(tag=icon, color=color, size=20), 
            rx.spacer(), 
            rx.badge(count, color_scheme="green", variant="solid")
        ),
        rx.text(title, font_size="1.2em", font_weight="bold", color="gold"),
        rx.button(
            "Gestionar", 
            width="100%", 
            variant="soft", 
            color_scheme="gray",
            on_click=lambda: StockState.set_view(title)
        ),
        padding="1.5em", 
        border="1px solid #333", 
        border_radius="10px", 
        bg="#111", 
        width="100%",
        _hover={"border": f"1px solid {color}"}
    )

def stock_submenu():
    """Submenú lateral interno (Soland Stock) visto en image_1c36f8.png"""
    items = [
        ("Herramientas", "wrench"),
        ("Botas", "footprints"),
        ("Bragas", "shirt"),
        ("Suministros", "package"),
        ("Lentes", "eye"),
        ("Equipos", "monitor"),
    ]
    return rx.vstack(
        # Cabecera del submenú
        rx.vstack(
            rx.box(
                rx.icon(tag="package", size=30, color="white"),
                padding="10px",
                border="1px solid #444",
                border_radius="10px"
            ),
            rx.text("Soland Stock", font_weight="bold", color="white", font_size="1.1em"),
            rx.text("Sistema de Inventario", color="gray", font_size="0.75em"),
            align_items="center",
            width="100%",
            padding_y="2em",
        ),
        # Lista de secciones
        rx.button(
            rx.hstack(rx.icon(tag="layout-grid", size=16), rx.text("Resumen")),
            width="90%",
            variant="soft",
            color_scheme="yellow", # Resaltado como en la imagen
            mb="1em"
        ),
        rx.vstack(
            *[
                rx.button(
                    rx.hstack(rx.icon(tag=icon, size=14), rx.text(name)),
                    variant="ghost",
                    color="gray",
                    width="100%",
                    justify_content="start",
                    # Al hacer clic se agrega stock y se cambia la vista
                    on_click=lambda n=name: StockState.agregar_al_stock(n),
                    _hover={"bg": "#222", "color": "gold"}
                )
                for name, icon in items
            ],
            width="100%",
            spacing="1",
            padding_x="1em",
        ),
        width="260px",
        height="100vh",
        bg="#121212",
        border_right="1px solid #222",
        align_items="center",
    )

def dashboard_view():
    """Contenido principal del dashboard con tarjetas y gráficos"""
    return rx.vstack(
        # Header del contenido
        rx.hstack(
            rx.hstack(
                rx.icon(tag="bar-chart-3", color="gold"),
                rx.heading("Resumen General del Inventario", color="gold", size="6"),
                spacing="3",
            ),
            rx.spacer(),
            rx.text("Total: 1000 items", color="gray", font_size="0.8em"),
            width="100%",
            padding_bottom="1.5em",
            align_items="center",
        ),
        
        # Grid de tarjetas
        rx.grid(
            summary_card("Herramientas", 140, "wrench", "#3b82f6"),
            summary_card("Botas", 87, "help-circle", "#eab308"),
            summary_card("Bragas", 98, "shirt", "#ef4444"),
            summary_card("Suministros", 555, "package", "#22c55e"),
            summary_card("Lentes", 115, "eye", "#a855f7"),
            summary_card("Equipos", 5, "monitor", "#f97316"),
            columns=rx.breakpoints(initial="1", sm="2", lg="3"), 
            spacing="4", 
            width="100%"
        ),
        
        # Sección de Gráficos
        rx.grid(
            # Gráfico de Distribución por Ítem
            rx.vstack(
                rx.hstack(rx.icon(tag="clock", size=16, color="gold"), rx.text("Distribución de Stock por ítem", color="gold")),
                rx.recharts.bar_chart(
                    rx.recharts.bar(data_key="cantidad", fill="#6366f1", radius=[4, 4, 0, 0]),
                    rx.recharts.x_axis(data_key="name"),
                    rx.recharts.y_axis(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False, stroke="#333"),
                    data=StockState.chart_data_items,
                    width="100%", height=250
                ),
                bg="#111", padding="1.5em", border_radius="12px", border="1px solid #222", width="100%"
            ),
            # Gráfico de Stock por Área
            rx.vstack(
                rx.hstack(rx.icon(tag="bar-chart", size=16, color="gold"), rx.text("Stock por Area", color="gold")),
                rx.recharts.bar_chart(
                    rx.recharts.bar(data_key="cantidad", fill="#10b981", radius=[4, 4, 0, 0]),
                    rx.recharts.x_axis(data_key="name"),
                    rx.recharts.y_axis(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False, stroke="#333"),
                    data=StockState.chart_data_areas,
                    width="100%", height=250
                ),
                bg="#111", padding="1.5em", border_radius="12px", border="1px solid #222", width="100%"
            ),
            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="4",
            width="100%",
            padding_top="2em"
        ),
        width="100%",
    )

def full_stock_dashboard_layout():
    """Layout que combina el submenú y el dashboard"""
    return rx.hstack(
        stock_submenu(),
        rx.box(
            dashboard_view(),
            padding="2em",
            width="100%",
            height="100vh",
            overflow_y="auto",
        ),
        width="100%",
        spacing="0",
        bg="#000",
    )