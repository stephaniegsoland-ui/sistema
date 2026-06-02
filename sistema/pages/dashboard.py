# --- sistema/pages/dashboard.py ---
import reflex as rx
from sistema.components.sidebar import sidebar
from sistema.states.dashboard_state import DashboardState
# IMPORTAMOS SOLO LA FUNCIÓN CONTENEDORA GLOBAL
from sistema.components.dashboard_charts import general_dashboard_view 

@rx.page(
    route="/dashboard", 
    title="Monitor Global de Suministros - SOLAND"
)
def dashboard_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="/dashboard"),
        
        rx.box(
            # Aquí usamos el componente unificado que creamos
            general_dashboard_view(), 
            
            flex="1",
            height="100vh", 
            background_color="#0b0b0c", 
            overflow_y="auto"
        ),
        width="100%", 
        height="100vh",
        spacing="0",
        align_items="stretch",
        background_color="#0b0b0c",
        
        # El evento de montaje se mantiene en el componente raíz de la vista
        on_mount=DashboardState.start_log_stream 
    )