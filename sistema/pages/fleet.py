# --- sistema/pages/fleet.py ---
import reflex as rx
from sistema.components.sidebar import sidebar

# ==========================================
# 1. ESTADO DE LA FLOTA (Simulado o Importado)
# ==========================================
class VehiculoModel(rx.Base):
    nombre: str
    placa: str
    modelo: str
    imagen_url: str
    registrado: bool

class FleetState(rx.State):
    """Estado para manejar la lista de vehículos de la flota."""
    vehiculos: list[VehiculoModel] = [
        VehiculoModel(
            nombre="Toyota Hilux", 
            placa="AB123CD", 
            modelo="Hilux 4x4 Chasis", 
            imagen_url="/hilux.png", # Asegúrate de tener estas imágenes en tu carpeta 'assets/'
            registrado=True
        ),
        VehiculoModel(
            nombre="JAC Urban", 
            placa="EF456GH", 
            modelo="Urban HFC 1042", 
            imagen_url="/jac_urban.png", 
            registrado=True
        ),
        VehiculoModel(
            nombre="Ford Super Duty", 
            placa="F-350", 
            modelo="Super Duty F-350 XL", 
            imagen_url="", 
            registrado=False
        ),
    ]

# ==========================================
# 2. COMPONENTES DE INTERFAZ (UI)
# ==========================================
def layout(component: rx.Component) -> rx.Component:
    """Envuelve cualquier página con el sidebar."""
    return rx.hstack(
        sidebar(),  # Sidebar aquí
        rx.box(component, width="100%", padding="1em"), # Tu contenido aquí
        align_items="start",
        width="100%",
        height="100vh"
    )

def vehiculo_card(vehi: VehiculoModel):
    """Renderiza una tarjeta individual para cada vehículo de la flota."""
    return rx.vstack(
        # Encabezado de la tarjeta con el nombre del vehículo
        rx.hstack(
            rx.text(f"🚗 {vehi.nombre}", color="gold", font_weight="bold"),
            rx.spacer(),
            spacing="2", 
            width="100%"
        ),
        
        rx.cond(
            vehi.registrado,
            # Contenido para vehículos con registro activo (Hilux, JAC)
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
                    align_items="start", 
                    spacing="0",
                    width="100%"
                ),
                # Botón con enlace dinámico al módulo de inspección específica
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
            # Estado para vehículos no registrados (Super Duty)
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

def fleet_comparison_view() -> rx.Component:
    """Vista interna del módulo de Gestión de Flota."""
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

        # Grid Responsivo de Vehículos
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
                rx.text("El sistema detectará mediante IA daños u observaciones ocurridas en la semana", size="2"),
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

# ==========================================
# 3. EXPORTACIÓN DE LA PÁGINA PRINCIPAL
# ==========================================
@rx.page(route="/fleet", title="Gestión de Flota - SOLAND")
def fleet_page() -> rx.Component:
    """Esta es la función exacta que importa sistema.py en la línea 10."""
    return layout(fleet_comparison_view())