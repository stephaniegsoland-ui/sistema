# --- sistema/components/dashboard_charts.py ---
import reflex as rx
# Importa aquí los componentes que ya tienes en stock_dashboard.py
from .stock_dashboard import (
    system_performance,
    ticket_queue,
    resolution_metrics,
    world_map_section,
    inventory_chart,
    orders_chart,
    fleet_status_panel
)

def general_dashboard_view() -> rx.Component:
    """Dashboard Global con el mapa y logs"""
    return rx.grid(
        rx.vstack(system_performance(), ticket_queue(), resolution_metrics(), spacing="3", width="100%"), 
        world_map_section(), 
        rx.vstack(inventory_chart(), orders_chart(), fleet_status_panel(), spacing="3", width="100%"), 
        grid_template_columns="340px 1fr 340px", 
        spacing="4",
        width="100%"
    )