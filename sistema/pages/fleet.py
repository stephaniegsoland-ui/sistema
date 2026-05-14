import reflex as rx
from ..states.fleet_state import FleetState
from ..components.fleet_view import fleet_comparison_view # Importa la vista completa
from ..components.sidebar import sidebar  # Importa el sidebar para navegación

def fleet_page() -> rx.Component:
    """Esta es la función principal que Reflex registrará como página."""
    return rx.hstack(
        sidebar(),
        fleet_comparison_view()
    )

def vehiculo_card(vehi):
    """Renderiza una tarjeta individual para cada vehículo de la flota."""
    return rx.vstack(
        # Encabezado de la tarjeta con el nombre del vehículo
        rx.hstack(
            rx.text(f"🚗 {vehi.nombre}", color="gold", font_weight="bold"),
            rx.spacer(),
            spacing="2", width="100%"
        ),
        
        rx.cond(
            vehi.registrado,
            # Contenido para vehículos con registro activo (Hilux, Jack)
            rx.vstack(
                rx.image(
                    src=vehi.imagen_url, 
                    height="140px", 
                    width="auto",
                    border_radius="md",
                    object_fit="contain"
                ),
                rx.vstack(
                    rx.text(f"Placa: {vehi.placa}", size="1", color="gray"),
                    rx.text(f"Modelo: {vehi.modelo}", font_weight="bold", size="3"),
                    rx.text("Comparar salida Lunes vs regreso Viernes", size="1", color="gray"),
                    align_items="start", 
                    spacing="0",
                    width="100%"
                ),
                # Botón con enlace dinámico al módulo de inspección
                rx.link(
                    rx.button(
                        "Comparar Salida Lunes vs Regreso Viernes",
                        width="100%",
                        color_scheme="blue",
                        variant="solid",
                        cursor="pointer"
                    ),
                    href=f"/vehiculos/{vehi.placa}",
                    width="100%",
                ),
                width="100%", 
                spacing="3"
            ),
            # Estado para vehículos no registrados (Carro, Duty)
            rx.center(
                rx.vstack(
                    rx.icon(tag="truck", size=40, color="#333"),
                    rx.text("Vehículo no registrado", color="gray", size="2"),
                    spacing="2"
                ),
                height="220px", 
                border="1px dashed #444", 
                width="100%", 
                border_radius="md",
                bg="#0d0d0d"
            )
        ),
        # Estilo de la tarjeta (Dark Mode con acento Soland)
        bg="#1a1a1a", 
        border="1px solid #333", 
        padding="1.5em", 
        border_radius="lg", 
        width="100%",
        _hover={"border": "1px solid gold", "transition": "0.3s"}
    )

def fleet_comparison_view():
    """Vista principal del módulo de Gestión de Flota."""
    return rx.vstack(
        # Banner de Título Superior
        rx.vstack(
            rx.hstack(
                rx.icon(tag="car", color="purple", size=20),
                rx.heading(
                    "COMPARACIÓN SEMANAL - SALIDA LUNES vs REGRESO VIERNES", 
                    size="4", 
                    color="gold"
                ),
                spacing="2", 
                width="100%"
            ),
            rx.text(
                "Compara el estado del vehículo entre la salida del lunes y el regreso del viernes para detectar cambios o daños durante la semana.", 
                color="gray", 
                size="2"
            ),
            width="100%",
            border_bottom="1px solid #333",
            padding_bottom="1em",
            align_items="start"
        ),

        # Grid Responsivo de Vehículos (2 columnas en desktop)
        rx.grid(
            rx.foreach(FleetState.vehiculos, vehiculo_card),
            columns=rx.breakpoints(initial="1", sm="1", md="2", lg="2"),
            spacing="6",
            width="100%",
            padding_y="1.5em"
        ),

        # Panel Informativo de Pasos (Footer del módulo)
        rx.vstack(
            rx.heading("📋 ¿Cómo funciona la comparación semanal?", size="3", color="white"),
            rx.hstack(
                rx.badge("1", variant="solid", color_scheme="blue", border_radius="full"), 
                rx.text("Selecciona el vehículo que quieres monitorear semanalmente", size="2"),
                align_items="center"
            ),
            rx.hstack(
                rx.badge("2", variant="solid", color_scheme="green", border_radius="full"), 
                rx.text("Cada lunes toma fotos del vehículo antes de que salga", size="2"),
                align_items="center"
            ),
            rx.hstack(
                rx.badge("3", variant="solid", color_scheme="orange", border_radius="full"), 
                rx.text("Cada viernes toma fotos del vehículo al regresar", size="2"),
                align_items="center"
            ),
            rx.hstack(
                rx.badge("4", variant="solid", color_scheme="red", border_radius="full"), 
                rx.text("El sistema detectará automáticamente cambios o daños ocurridos durante la semana", size="2"),
                align_items="center"
            ),
            align_items="start", 
            spacing="3", 
            bg="#111", 
            padding="2em", 
            border_radius="15px", 
            width="100%",
            border="1px solid #222"
        ),
        width="100%", 
        spacing="4",
        padding="1em"
    )