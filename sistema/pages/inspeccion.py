import reflex as rx
from ..states.inspeccion_state import InspeccionState
from ..components.sidebar import sidebar 

def info_badge(label: str, value: rx.Var):
    return rx.vstack(
        rx.text(label, color="gray.400", size="1", text_transform="uppercase", letter_spacing="0.05em"),
        rx.text(value, color="white", size="2", font_weight="bold"),
        spacing="1",
        align_items="start",
    )

def upload_card(title: str, icon_tag: str, color_hex: str, image_url: rx.Var, upload_id: str, upload_handler: any):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag=icon_tag, color=color_hex, size=20),
                rx.heading(title, size="3", color=color_hex, font_weight="bold"),
                spacing="2",
                align="center",
            ),
            # Espacio de previsualización
            rx.box(
                rx.cond(
                    image_url != "",
                    rx.image(
                        src=image_url,
                        width="100%",
                        height="180px",
                        object_fit="cover",
                        border_radius="lg",
                        box_shadow="0 10px 20px rgba(0,0,0,0.4)"
                    ),
                    rx.center(
                        rx.icon(tag="image", size=40, color=color_hex, opacity="0.3"),
                        width="100%",
                        height="180px",
                        bg="rgba(255, 255, 255, 0.03)",
                        border=f"2px dashed {color_hex}55",
                        border_radius="lg",
                    )
                ),
                width="100%",
            ),
            # Input de carga (la subida se inicia al seleccionar el archivo)
            rx.input(
                id=upload_id,
                type_="file",
                accept="image/*",
                on_change=upload_handler(rx.selected_files(upload_id)),
                width="100%",
                border=f"1px solid {color_hex}33",
                border_radius="lg",
                padding="1em",
                bg="#111",
                color="white",
                _hover={"border_color": color_hex},
            ),
            rx.text("La imagen se sube automáticamente al seleccionarla.", color="gray.400", size="1"),
            spacing="3",
            width="100%"
        ),
        padding="1.2em",
        bg="linear-gradient(135deg, #111827 0%, #1f2937 100%)",
        border=f"1px solid {color_hex}66",
        border_radius="xl",
    )

def inspeccion_page() -> rx.Component:
    return rx.hstack(
        sidebar(), # Sidebar lateral del sistema
        rx.vstack(
            # Header
            rx.hstack(
                rx.button(
                    rx.icon("arrow-left", size=20),
                    "Volver",
                    on_click=lambda: rx.redirect("/vehiculos"), # Regresa al módulo de vehículos
                    variant="ghost",
                    color_scheme="gray"
                ),
                rx.spacer(),
                rx.heading("🔍 Inspección Técnica IA", size="5", color="#FFCC00", font_weight="bold"),
                width="100%",
                align="center",
            ),

            # Card de Información del Vehículo
            rx.card(
                rx.grid(
                    info_badge("Modelo de Unidad", InspeccionState.modelo),
                    info_badge("Número de Placa", InspeccionState.router.page.params.get('pid', '---')),
                    info_badge("Operador Responsable", InspeccionState.responsable),
                    columns="3",
                    width="100%",
                    spacing="4",
                ),
                width="100%",
                padding="1.5em",
                bg="linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
                border="2px solid #FFCC00",
                border_radius="2xl",
                box_shadow="0 10px 30px rgba(255, 204, 0, 0.15)"
            ),

            rx.divider(margin_y="1em", border_color="#FFCC00", opacity="0.2"),

            # Grid de Carga de Fotos
            rx.grid(
                upload_card(
                    "Salida Lunes", "calendar", "#3b82f6", 
                    InspeccionState.url_lunes, "upload_lunes",
                    InspeccionState.handle_upload_lunes # Se pasa la referencia a la función
                ),
                upload_card(
                    "Regreso Viernes", "calendar-check", "#10b981", 
                    InspeccionState.url_viernes, "upload_viernes",
                    InspeccionState.handle_upload_viernes # Se pasa la referencia a la función
                ),
                columns="2",
                spacing="4",
                width="100%"
            ),

            # Botón de Procesar
            rx.button(
                rx.hstack(rx.icon(tag="cpu"), rx.text("Iniciar Análisis Comparativo")),
                on_click=InspeccionState.generar_informe,
                size="4",
                width="100%",
                bg="#FFCC00",
                color="black",
                font_weight="bold",
                _hover={"bg": "#e6b800"}
            ),

            # Panel de Resultados (Solo visible tras el análisis)
            rx.cond(
                InspeccionState.mostrar_resultado,
                rx.vstack(
                    rx.divider(margin_y="1em", border_color="#FFCC00", opacity="0.4"),
                    rx.heading("📊 Reporte de Daños Detectados", size="4", color="#FFCC00"),
                    rx.grid(
                        rx.vstack(
                            rx.text("Estado Inicial (Lunes)", color="gray.400", size="2"),
                            rx.image(src=InspeccionState.imagen_overlay_lunes_url, width="100%", border_radius="md", border="1px solid #3b82f6"),
                        ),
                        rx.vstack(
                            rx.text("Estado Final (Viernes)", color="gray.400", size="2"),
                            rx.image(src=InspeccionState.imagen_overlay_viernes_url, width="100%", border_radius="md", border="1px solid #10b981"),
                        ),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID"),
                                rx.table.column_header_cell("Tipo de Hallazgo"),
                                rx.table.column_header_cell("Detalle del Análisis"),
                                rx.table.column_header_cell("Confianza"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                InspeccionState.lista_hallazgos,
                                lambda item: rx.table.row(
                                    rx.table.cell(item.id), 
                                    rx.table.cell(item.tipo),
                                    rx.table.cell(item.detalle),
                                    rx.table.cell(item.confianza),
                                )
                            )
                        ),
                        width="100%",
                        variant="surface",
                    ),
                    spacing="4",
                    width="100%",
                    padding="1.5em",
                    bg="rgba(0,0,0,0.2)",
                    border_radius="xl",
                )
            ),

            spacing="4",
            padding="2em",
            width="100%",
            bg="linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        ),
        width="100%",
        spacing="0",
    )