# sistema/components/stock_dashboard.py
import reflex as rx
from sistema.states.dashboard_state import DashboardState

# Desestructuración limpia de los componentes de Recharts desde rx.recharts
bar_chart = rx.recharts.bar_chart
bar = rx.recharts.bar
x_axis = rx.recharts.x_axis
y_axis = rx.recharts.y_axis
cartesian_grid = rx.recharts.cartesian_grid
tooltip = rx.recharts.tooltip
legend = rx.recharts.legend
responsive_container = rx.recharts.responsive_container

# --- DATA STREAMS DE PRUEBA ---
rendimiento_data = {"eficiencia": 94, "resolucion": 88, "satisfaccion": 96, "disponibilidad": 100}

tickets_data = [
    {"status": "Pendientes", "count": 12, "color": "yellow"},
    {"status": "En Proceso", "count": 8, "color": "blue"},
    {"status": "Completados", "count": 24, "color": "green"}
]

inventario_data_stacked = [
    {"name": "Alicate", "Almacen_A": 50, "Almacen_B": 40},
    {"name": "Máscaras N95", "Almacen_A": 90, "Almacen_B": 60},
    {"name": "Escritorio", "Almacen_A": 20, "Almacen_B": 10}
]

pedidos_data = [
    {"name": "Botas", "count": 150}, 
    {"name": "Suministros", "count": 600}, 
    {"name": "Equipos", "count": 200}
]

criticos_data = [
    {"id": "TK-2847", "titulo": "Sistema de Inventario", "tiempo": "3hrs", "color": "#ef4444"},
    {"id": "TK-2839", "titulo": "Base de Datos", "tiempo": "5hrs", "color": "#f97316"}
]

flota_data = [
    {"unidad": "Chuto Volvo #01", "ruta": "Maturín - Caracas", "status": "En Ruta", "color": "blue"},
    {"unidad": "NPR Suministros", "ruta": "Despacho Local", "status": "Completado", "color": "green"},
    {"unidad": "PickUp Inspección", "ruta": "Zona Industrial", "status": "Standby", "color": "gray"}
]

# --- STRUCTS AUXILIARES ---
def metric_card(title, value, icon, color):
    return rx.hstack(
        rx.icon(tag=icon, color=color, size=18),
        rx.vstack(
            rx.text(title, size="1", color="gray"),
            rx.heading(f"{value}%", size="3", color=color),
            spacing="0", 
            align_items="start"
        ),
        padding="8px", 
        background_color="#141416", 
        border="1px solid #222225", 
        border_radius="6px", 
        width="100%"
    )

def ticket_status_item(label, count, color, desc):
    return rx.hstack(
        rx.box(width="8px", height="8px", bg=color, border_radius="2px"),
        rx.text(label, size="1", color="gray", width="80px"),
        rx.heading(str(count), size="2", color="white", width="30px", text_align="right"),
        rx.text(desc, size="1", color="gray"),
        spacing="3", 
        align_items="center"
    )

def world_clock(location, time_str, date_str):
    return rx.vstack(
        rx.text(location, size="1", weight="bold", color="gray"),
        rx.heading(time_str, size="3", color="#FFD700"),
        rx.text(date_str, size="1", color="gray"),
        padding="10px", 
        background_color="#141416", 
        border="1px solid #222225", 
        border_radius="8px", 
        text_align="center", 
        width="100%"
    )

# --- COMPONENTES PRINCIPALES DEL LAYOUT ---
def system_performance():
    return rx.vstack(
        rx.heading("SYSTEM PERFORMANCE", size="2", color="gray"),
        rx.hstack(
            rx.icon(tag="activity", color="green", size=14), 
            rx.text("Rendimiento del Sistema", color="white", size="1"), 
            spacing="2"
        ),
        rx.grid(
            metric_card("Eficiencia", rendimiento_data["eficiencia"], "zap", "green"),
            metric_card("Resolución", rendimiento_data["resolucion"], "help-circle", "blue"),
            metric_card("Satisfacción", rendimiento_data["satisfaccion"], "star", "yellow"),
            metric_card("Disponibilidad", rendimiento_data["disponibilidad"], "server", "purple"),
            columns="2", 
            spacing="2", 
            width="100%"
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%", 
        spacing="2", 
        align_items="start"
    )

def ticket_queue():
    return rx.vstack(
        rx.heading("SERVICE TICKET QUEUE", size="2", color="gray"),
        rx.hstack(
            rx.icon(tag="ticket", color="yellow", size=14), 
            rx.heading("Tickets Activos", size="1", color="white"), 
            spacing="2"
        ),
        rx.vstack(
            *[ticket_status_item(
                t["status"], 
                t["count"], 
                t["color"], 
                "requieren atención" if t["status"] == "Pendientes" else "siendo atendidos" if t["status"] == "En Proceso" else "esta semana"
            ) for t in tickets_data],
            spacing="2", 
            width="100%"
        ),
        rx.divider(border_color="#222225", margin_y="4px"),
        rx.text("Tickets por Prioridad", size="1", color="gray", weight="bold"),
        rx.vstack(
            rx.hstack(rx.text("Alta", size="1", width="40px"), rx.progress(value=15, color_scheme="red", width="100%"), rx.text("3", size="1", color="gray"), width="100%"),
            rx.hstack(rx.text("Media", size="1", width="40px"), rx.progress(value=35, color_scheme="yellow", width="100%"), rx.text("7", size="1", color="gray"), width="100%"),
            rx.hstack(rx.text("Baja", size="1", width="40px"), rx.progress(value=50, color_scheme="blue", width="100%"), rx.text("10", size="1", color="gray"), width="100%"),
            width="100%", 
            spacing="2"
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%", 
        spacing="2", 
        align_items="start"
    )

def resolution_metrics():
    return rx.vstack(
        rx.heading("MÉTRICAS DE RESOLUCIÓN", size="2", color="gray"),
        rx.grid(
            rx.hstack(rx.icon(tag="clock", color="aquamarine", size=14), rx.vstack(rx.text("Tiempo Promedio", size="1", color="gray"), rx.heading("2.4 hrs", size="2", color="aquamarine"), spacing="0")),
            rx.hstack(rx.icon(tag="percent", color="violet", size=14), rx.vstack(rx.text("Tasa SLA", size="1", color="gray"), rx.heading("96%", size="2", color="violet"), spacing="0")),
            columns="2", 
            width="100%", 
            spacing="2"
        ),
        rx.divider(border_color="#222225", margin_y="2px"),
        rx.hstack(rx.icon(tag="alert-triangle", color="#ef4444", size=12), rx.text("Críticos a Atender", size="1", color="#ef4444", weight="bold"), spacing="2"),
        rx.vstack(
            *[rx.hstack(
                rx.badge(item["id"], bg=item["color"], color="white", size="1"), 
                rx.text(item["titulo"], size="1", color="white", width="140px", is_truncated=True), 
                rx.spacer(), 
                rx.text(item["tiempo"], size="1", color="gray"), 
                width="100%"
            ) for item in criticos_data],
            spacing="2", 
            width="100%"
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%", 
        spacing="2", 
        align_items="start"
    )

def world_map_section():
    return rx.vstack(
        rx.heading("REGIONAL SUPPLY CHAIN STATUS", size="2", color="gray"),
        rx.box(
            rx.image(src="/logo.jpg", width="100%", height="auto", object_fit="cover"), 
            width="100%", 
            background_color="#111113", 
            border="1px solid #222225", 
            border_radius="8px", 
            overflow="hidden"
        ),
        rx.flex(
            rx.badge("Almacén Cebástica", color_scheme="green", variant="surface"),
            rx.badge("Logística Avanzada", color_scheme="purple", variant="surface"),
            rx.badge("HQ Principal", color_scheme="yellow", variant="surface"),
            rx.badge("Distribución Regional", color_scheme="blue", variant="surface"),
            rx.badge("Entrega Estratégica", color_scheme="red", variant="surface"),
            spacing="3", 
            justify="center", 
            width="100%", 
            wrap="wrap"
        ),
        rx.grid(
            world_clock("VENEZUELA", "09:51:51", "27/05/2026"),
            world_clock("ESTADOS UNIDOS", "09:51:51", "27/05/2026"),
            world_clock("ESPAÑA", "15:51:51", "27/05/2026"),
            world_clock("CHINA", "21:51:51", "27/05/2026"),
            columns="4", 
            spacing="3", 
            width="100%"
        ),
        
        # CONSOLA DE EVENTOS REALES VINCULADA AL ESTADO MODULAR
        rx.vstack(
            rx.hstack(
                rx.icon(tag="terminal", color="#FFD700", size=14), 
                rx.text("CONSOLA DE EVENTOS EN VIVO", size="1", color="white", weight="bold"), 
                spacing="2"
            ),
            rx.vstack(
                rx.foreach(
                    DashboardState.syslog_events,
                    lambda log: rx.hstack(
                        rx.text(f"[{log.time}]", color="gray", font_family="monospace", font_size="11px"),
                        rx.badge(log.log_type, variant="outline", size="1", border=f"1px solid {log.color}", color=log.color),
                        rx.text(log.msg, color="#E0E0E0", font_family="monospace", font_size="11px", is_truncated=True),
                        width="100%", 
                        spacing="2"
                    )
                ),
                spacing="2", 
                width="100%"
            ),
            width="100%", 
            min_height="125px", 
            padding="12px", 
            background_color="#0d0d0e", 
            border="1px solid #222225", 
            border_radius="6px", 
            align_items="start"
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%", 
        spacing="3"
    )

def inventory_chart():
    return rx.vstack(
        rx.heading("INVENTARIO DISPONIBLE", size="2", color="gray"),
        responsive_container(
            bar_chart(
                cartesian_grid(stroke_dasharray="3 3", stroke="#222225"),
                x_axis(data_key="name", stroke="gray", font_size=10),
                y_axis(stroke="gray", font_size=10),
                tooltip(content_style={"background": "#111113", "border": "1px solid #222225", "color": "white"}),
                legend(icon_type="circle", wrapper_style={"fontSize": 10}),
                bar(data_key="Almacen_A", stack_id="inv", fill="#3b82f6", name="Stock Planta"),
                bar(data_key="Almacen_B", stack_id="inv", fill="#10b981", radius=[4, 4, 0, 0], name="Stock Tránsito"),
                data=inventario_data_stacked,
            ),
            width="100%", 
            height=150,
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%"
    )

def orders_chart():
    return rx.vstack(
        rx.heading("PEDIDOS EN PROCESO", size="2", color="gray"),
        responsive_container(
            bar_chart(
                cartesian_grid(stroke_dasharray="3 3", stroke="#222225"),
                x_axis(data_key="name", stroke="gray", font_size=10),
                y_axis(stroke="gray", font_size=10),
                tooltip(content_style={"background": "#111113", "border": "1px solid #222225", "color": "white"}),
                bar(data_key="count", fill="#eab308", radius=[4, 4, 0, 0], name="Pedidos"),
                data=pedidos_data,
            ),
            width="100%", 
            height=150,
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%"
    )

def fleet_status_panel():
    return rx.vstack(
        rx.heading("MONITOR DE FLOTA (DISTRIBUCIÓN)", size="2", color="gray"),
        rx.vstack(
            *[
                rx.hstack(
                    rx.icon(tag="truck", color="white", size=14),
                    rx.vstack(
                        rx.text(veh["unidad"], size="1", color="white", weight="bold"),
                        rx.text(veh["ruta"], size="1", color="gray"),
                        spacing="0", 
                        align_items="start"
                    ),
                    rx.spacer(),
                    rx.badge(veh["status"], color_scheme=veh["color"], variant="solid", size="1"),
                    width="100%", 
                    padding="6px", 
                    border_bottom="1px solid #222225"
                ) for veh in flota_data
            ],
            spacing="1", 
            width="100%"
        ),
        padding="14px", 
        background_color="#111113", 
        border="1px solid #222225", 
        border_radius="8px", 
        width="100%", 
        align_items="start"
    )

# --- VIEWS EXPORTABLES PARA LAYOUTS GENERALES ---

def general_dashboard_view() -> rx.Component:
    """ESTA ES PARA /dashboard: Incluye el Mapa Regional y la Consola de Logs"""
    return rx.grid(
        # Columna 1: Rendimiento y Tickets
        rx.vstack(system_performance(), ticket_queue(), resolution_metrics(), spacing="3", width="100%"), 
        
        # Columna 2: Mapa Central y Consola en vivo
        world_map_section(), 
        
        # Columna 3: Inventarios y Flota
        rx.vstack(inventory_chart(), orders_chart(), fleet_status_panel(), spacing="3", width="100%"), 
        
        grid_template_columns="340px 1fr 340px", 
        spacing="4",
        width="100%"
    )

def stock_resumen_view() -> rx.Component:
    """ESTA ES PARA /stock: Enfocada puramente en Analítica de Almacén (Sin Mapa Central)"""
    return rx.grid(
        # Columna Left: Capacidad y Métricas de Rendimiento de Despacho
        rx.vstack(
            system_performance(), 
            resolution_metrics(), 
            spacing="3", 
            width="100%"
        ), 
        
        # Columna Center: Gráficos principales ampliados para control de existencias
        rx.vstack(
            inventory_chart(),  # Gráfico de barras de Stock Planta vs Tránsito
            orders_chart(),     # Gráfico de Pedidos en Proceso
            spacing="3",
            width="100%"
        ), 
        
        # Columna Right: Estado de la Flota de Distribución y Rutas activas
        rx.vstack(
            fleet_status_panel(), 
            spacing="3", 
            width="100%"
        ), 
        
        # Layout expandido para aprovechar el espacio que dejó el mapa
        grid_template_columns="1fr 1.5fr 1fr", 
        spacing="4",
        width="100%"
    )