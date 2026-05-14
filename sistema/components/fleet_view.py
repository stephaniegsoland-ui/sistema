import reflex as rx
from ..states.fleet_state import FleetState

def vehiculo_card(vehi):
    return rx.vstack(
        rx.text(f"🚗 {vehi.nombre}", color="gold", font_weight="bold", align_self="start"),
        rx.cond(
            vehi.registrado,
            rx.vstack(
                rx.image(src=vehi.imagen_url, height="120px", border_radius="md"),
                rx.vstack(
                    rx.text(f"Placa: {vehi.placa}", size="1", color="gray"),
                    rx.text(f"Modelo: {vehi.modelo}", font_weight="bold"),
                    rx.text("Comparar salida Lunes vs regreso Viernes", size="1", color="gray"),
                    align_items="start", spacing="0"
                ),
                rx.button(
                    "Comparar Salida Lunes vs Regreso Viernes",
                    on_click=lambda: FleetState.iniciar_comparacion(vehi.placa),
                    width="100%", color_scheme="blue", size="2"
                ),
                width="100%", spacing="3"
            ),
            # Estado no registrado (como Carro y Duty en image_ca8cec.jpg)
            rx.center(
                rx.vstack(
                    rx.icon(tag="truck", size=40, color="gray"),
                    rx.text("Vehículo no registrado", color="gray", size="2"),
                ),
                height="200px", border="1px dashed #444", width="100%", border_radius="md"
            )
        ),
        bg="#1a1a1a", border="1px solid #333", padding="1.5em", border_radius="lg", width="100%"
    )

def fleet_comparison_view():
    return rx.vstack(
        # Banner Superior
        rx.hstack(
            rx.icon(tag="car", color="purple", size=20),
            rx.heading("COMPARACIÓN SEMANAL - SALIDA LUNES vs REGRESO VIERNES", size="4", color="gold"),
            rx.spacer(),
            spacing="2", width="100%", border_bottom="1px solid #333", padding_bottom="0.5em"
        ),
        rx.text("Compara el estado del vehículo para detectar cambios o daños durante la semana.", color="gray", size="2"),

        # Grid de Vehículos
        rx.grid(
            rx.foreach(FleetState.vehiculos, vehiculo_card),
            columns="2", spacing="4", width="100%", padding_y="1em"
        ),

        # Sección Informativa Inferior (Pasos del 1 al 4)
        rx.vstack(
            rx.heading("📋 ¿Cómo funciona la comparación semanal?", size="3", color="white"),
            rx.hstack(rx.badge("1", color_scheme="blue"), rx.text("Selecciona el vehículo que quieres monitorear semanalmente", size="2")),
            rx.hstack(rx.badge("2", color_scheme="green"), rx.text("Cada lunes toma fotos del vehículo antes de que salga", size="2")),
            rx.hstack(rx.badge("3", color_scheme="orange"), rx.text("Cada viernes toma fotos del vehículo al regresar", size="2")),
            rx.hstack(rx.badge("4", color_scheme="red"), rx.text("El sistema detectará automáticamente cambios o daños", size="2")),
            align_items="start", spacing="2", bg="#111", padding="1.5em", border_radius="md", width="100%"
        ),
        width="100%", spacing="4"
    )