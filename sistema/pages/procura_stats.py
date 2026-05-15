import reflex as rx
from ..components.sidebar import sidebar
from ..states.procura_state import ProcuraState
from ..components.procura_charts import render_advanced_stats
from ..components.procura_charts import render_report_table


@rx.page(route="/procura/estadisticas", title="Estadísticas - SOLAND", on_load=ProcuraState.load_solicitudes)
def procura_stats_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="/procura/estadisticas"),
        rx.box(
                rx.vstack(
                    rx.heading("Análisis Inteligente de Procura", size="8", color="#FFD700"),
                    rx.text("Monitoreo logístico y predicción IA en tiempo real.", color_secondary=True),
                    rx.separator(color_alpha="0.8"),
                    
                    render_advanced_stats(), # Aquí es donde se dibujan los 4 cuadros y gráficas
                    render_report_table(), # Aquí se dibuja la tabla de reporte detallado

                    spacing="3", width="70%",
                ),
                size="4", padding_y="2em",
        
            bg="#09090b", width="100%", min_height="100vh",
        ),
    )