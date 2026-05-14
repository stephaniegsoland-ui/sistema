import reflex as rx
from ..states.epp_state import EPPState

def epp_analysis_view():
    return rx.vstack(
        # Encabezado estilo SOLAND
        rx.hstack(
            rx.icon(tag="circle_help", color="gold", size=30),
            rx.vstack(
                rx.heading("Análisis de EPP Laboral", size="7", color="white"),
                rx.text("Verificación de seguridad industrial con IA Vision.", color="gray"),
                align_items="start",
            ),
            spacing="3", width="100%", padding_bottom="1.5em"
        ),
        
        rx.grid(
            # Columna 1: Carga
            rx.vstack(
                rx.heading("Cargar imagen", size="5"),
                rx.upload(
                    rx.vstack(
                        rx.icon(tag="camera", size=40, color="gold"),
                        rx.text("Selecciona una imagen"),
                        rx.text("JPG, PNG, WEBP", size="1", color="gray"),
                    ),
                    id="upload_epp", border="2px dashed #333", padding="3em", border_radius="15px", width="100%"
                ),
                rx.button(
                    "Analizar con IA",
                    on_click=EPPState.handle_upload(rx.selected_files("upload_epp")),
                    width="100%", height="3em", color_scheme="yellow", 
                    loading=EPPState.image_processing
                ),
                bg="#111", padding="2em", border_radius="20px", spacing="4"
            ),

            # Columna 2: Vista Previa Real
            rx.vstack(
                rx.heading("Vista previa", size="5"),
                rx.box(
                    rx.cond(
                        EPPState.image_url,
                        rx.image(src=EPPState.image_url, width="100%", border_radius="10px"),
                        rx.center(rx.text("No hay imagen cargada", color="gray"), height="300px")
                    ),
                    bg="#0a0a0a", border="1px solid #222", border_radius="15px", width="100%", overflow="hidden"
                ),
                bg="#111", padding="2em", border_radius="20px", width="100%"
            ),

            # Columna 3: Resultados de la IA
            rx.vstack(
                rx.heading("Resultado del análisis", size="5"),
                # Banner dinámico (Rojo/Verde)
                rx.box(
                    rx.hstack(
                        rx.icon(
                            tag=rx.cond(EPPState.analysis_status == "APROBADO", "circle_check", "circle_x"),
                            color=rx.cond(EPPState.analysis_status == "APROBADO", "#4ade80", "#ff4d4d")
                        ),
                        rx.text(EPPState.analysis_status, font_weight="bold"),
                    ),
                    bg=rx.cond(EPPState.analysis_status == "APROBADO", "#062010", "#2a1010"),
                    padding="1em", border_radius="10px", width="100%", border="1px solid #333"
                ),
                # Checklist generado por IA
                rx.foreach(
                    EPPState.analysis_checks,
                    lambda check: rx.box(
                        rx.hstack(
                            rx.icon(
                                tag=rx.cond(check["status"], "circle_check", "circle_alert"),
                                color=rx.cond(check["status"], "cyan", "orange"), size=18
                            ),
                            rx.vstack(
                                rx.text(check["item"], font_weight="bold", size="2"),
                                rx.text(check["desc"], size="1", color="gray"),
                                align_items="start", spacing="0"
                            )
                        ),
                        bg="#1a1a1a", padding="0.8em", border_radius="10px", width="100%"
                    )
                ),
                rx.button("Guardar en Historial", variant="outline", width="100%", on_click=EPPState.save_record),
                bg="#111", padding="2em", border_radius="20px", spacing="4"
            ),
            columns=rx.breakpoints(initial="1", lg="3"), spacing="6", width="100%"
        ),
        width="100%", padding="2em"
    )