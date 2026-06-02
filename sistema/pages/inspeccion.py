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

def upload_card(title: str, icon_tag: str, color_hex: str, image_filename: rx.Var, upload_id: str, upload_handler: any):
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
                    image_filename != "",
                    rx.image(
                        src=rx.get_upload_url(image_filename),
                        width="100%",
                        height="240px",
                        object_fit="contain",
                        border_radius="lg",
                        box_shadow="0 10px 20px rgba(0,0,0,0.4)",
                        bg="#000",
                    ),
                    rx.center(
                        rx.icon(tag="image", size=40, color=color_hex, opacity="0.3"),
                        width="100%",
                        height="240px",
                        bg="rgba(255, 255, 255, 0.03)",
                        border=f"2px dashed {color_hex}55",
                        border_radius="lg",
                    )
                ),
                width="100%",
            ),
            rx.upload(
                rx.vstack(
                    rx.icon(tag="camera", size=40, color=color_hex),
                    rx.text("Selecciona o arrastra la imagen", color="gray.300"),
                    rx.text("JPG, PNG, WEBP", size="1", color="gray"),
                ),
                id=upload_id,
                accept={"image/*": [".jpg", ".jpeg", ".png"]},
                max_files=1,
                multiple=False,
                border=f"2px dashed {color_hex}55",
                padding="2.5em",
                border_radius="lg",
                width="100%",
                on_drop=upload_handler,
            ),
            rx.text("Se sube automáticamente al seleccionar la imagen.", color="gray.400", size="1"),
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

            # Botones de Procesar y Guardar
            rx.vstack(
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
                rx.button(
                    rx.hstack(rx.icon(tag="save"), rx.text("Guardar Reporte")),
                    on_click=InspeccionState.save_report,
                    size="4",
                    width="100%",
                    variant="outline",
                    color_scheme="yellow",
                    _hover={"bg": "#F59E0B", "color": "black"}
                ),
                rx.button(
                    rx.hstack(rx.icon(tag="file_text"), rx.text("Ver todos los reportes")),
                    on_click=lambda: rx.redirect("/vehiculos/reportes"),
                    size="4",
                    width="100%",
                    variant="outline",
                    color_scheme="cyan",
                    _hover={"bg": "#22d3ee", "color": "black"}
                ),
                spacing="3",
                width="100%"
            ),

            # Panel de Resultados (Solo visible tras el análisis)
            rx.cond(
                InspeccionState.mostrar_resultado,
                rx.vstack(
                    rx.divider(margin_y="1em", border_color="#FFCC00", opacity="0.4"),
                    rx.heading("📊 Reporte de Daños Detectados", size="4", color="#FFCC00"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Estado IA", color="gray.400", size="2"),
                            rx.text(InspeccionState.analisis_ia_datos.get("estado_final", "N/A"), color="white", size="3", font_weight="bold"),
                        ),
                        rx.spacer(),
                        rx.vstack(
                            rx.text("Recomendación", color="gray.400", size="2"),
                            rx.text(InspeccionState.analisis_ia_datos.get("recomendacion", "-"), color="white", size="2"),
                        ),
                        width="100%"
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Estado Inicial (Lunes)", color="gray.400", size="2"),
                            rx.box(
                                rx.image(src=rx.get_upload_url(InspeccionState.imagen_overlay_lunes_url), width="100%", height="260px", object_fit="contain", border_radius="md", border="1px solid #3b82f6"),
                                rx.foreach(
                                    InspeccionState.damage_map_lunes,
                                    lambda item: rx.box(
                                        rx.text(item["tipo"], color="white", font_size="xs", padding="0.2em", bg="rgba(255,0,0,0.8)", border_radius="sm", position="absolute", top=f"{item['y']}%", left=f"{item['x']}%", z_index="3"),
                                        position="absolute",
                                        top=f"{item['y']}%",
                                        left=f"{item['x']}%",
                                        width=f"{item['width']}%",
                                        height=f"{item['height']}%",
                                        border="2px solid rgba(252, 165, 165, 0.85)",
                                        bg="rgba(248, 113, 113, 0.12)",
                                        border_radius="md",
                                        z_index="2",
                                        pointer_events="none",
                                    )
                                ),
                                position="relative",
                                width="100%",
                                height="260px",
                                overflow="hidden",
                            ),
                        ),
                        rx.vstack(
                            rx.text("Estado Final (Viernes)", color="gray.400", size="2"),
                            rx.box(
                                rx.image(src=rx.get_upload_url(InspeccionState.imagen_overlay_viernes_url), width="100%", height="260px", object_fit="contain", border_radius="md", border="1px solid #10b981"),
                                rx.foreach(
                                    InspeccionState.damage_map_viernes,
                                    lambda item: rx.box(
                                        rx.text(item["tipo"], color="white", font_size="xs", padding="0.2em", bg="rgba(34,197,94,0.85)", border_radius="sm", position="absolute", top=f"{item['y']}%", left=f"{item['x']}%", z_index="3"),
                                        position="absolute",
                                        top=f"{item['y']}%",
                                        left=f"{item['x']}%",
                                        width=f"{item['width']}%",
                                        height=f"{item['height']}%",
                                        border="2px solid rgba(34,197,94,0.85)",
                                        bg="rgba(34,197,94,0.12)",
                                        border_radius="md",
                                        z_index="2",
                                        pointer_events="none",
                                    )
                                ),
                                position="relative",
                                width="100%",
                                height="260px",
                                overflow="hidden",
                            ),
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
                                            rx.table.cell(item["id"]), 
                                    rx.table.cell(item["tipo"]),
                                    rx.table.cell(item["detalle"]),
                                    rx.table.cell(item["confianza"]),
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