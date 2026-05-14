import reflex as rx
from sistema.components.sidebar import sidebar
from sistema.states.dashboard_state import DashboardState
from sistema.styles.colors import BG_DARK, ACCENT_YELLOW, CARD_BG, TEXT_GRAY

def bar_row(label: str, value: rx.Var, max_value: int, color: str):
    # Calculamos el porcentaje (0 a 100)
    # Usamos .to(float) para asegurar la operación matemática en el frontend
    width_percentage = (value.to(float) / max_value) * 100
    
    return rx.vstack(
        rx.hstack(
            rx.text(label, size="1", color="gray"),
            rx.text(value.to(str), size="1", color="white"),
            justify="between",
            width="100%",
        ),
        rx.box(
            rx.box(
                height="10px",
                # Convertimos el cálculo a string y le pegamos el '%'
                width=width_percentage.to(str) + "%",
                background_color=color,
                border_radius="full",
                transition="width 0.5s ease-in-out",
            ),
            height="10px",
            width="100%",
            background_color="#111",
            border_radius="full",
        ),
        spacing="2",
        width="100%",
    )

def clock_box(label: str, time_var: rx.Var):
    return rx.vstack(
        rx.text(label, size="1", color=TEXT_GRAY),
        rx.text(time_var, size="4", color=ACCENT_YELLOW, font_family="JetBrains Mono"),
        padding="12px",
        background_color="#0A0A0A",
        border="1px solid #222",
        border_radius="12px",
        width="135px",
        align="center",
    )

def dashboard_page() -> rx.Component:
    return rx.hstack(
        sidebar(current_page="dashboard"),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("MONITOREO GLOBAL DE SUMINISTROS", size="4", color="white"),
                    rx.spacer(),
                    rx.badge("SINCRONIZADO", color_scheme="green", variant="soft"),
                    width="100%",
                ),
                rx.text("Panel central de control operativo.", size="1", color="gray"),
                
                rx.grid(
                    # Columna 1: Métricas de Rendimiento
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Eficiencia del Sistema", size="3", font_weight="bold"),
                                rx.text(DashboardState.eficiencia, size="5", color=ACCENT_YELLOW),
                                rx.divider(border_color="#222"),
                                rx.text("Disponibilidad: " + DashboardState.disponibilidad, size="1", color="gray"),
                            ),
                            padding="20px", background_color=CARD_BG, border_radius="15px", width="100%"
                        ),
                        spacing="4",
                    ),
                    # Columna 2: Mapa y Relojes
                    rx.vstack(
                        rx.box(
                            rx.center(rx.text("MAPA DE NODOS LOGÍSTICOS", color="gray")),
                            height="300px", width="100%", background_color="#101010", border_radius="15px"
                        ),
                        rx.hstack(
                            clock_box("VENEZUELA", DashboardState.hora_venezuela),
                            clock_box("ESPAÑA", DashboardState.hora_espana),
                            spacing="4",
                        ),
                        width="100%",
                    ),
                    # Columna 3: Inventario
                    rx.box(
                        rx.vstack(
                            rx.text("Stock Crítico", size="3", font_weight="bold"),
                            bar_row("Alicates", DashboardState.inventario_alicate, 120, "#f5d142"),
                            bar_row("N95", DashboardState.inventario_n95, 200, "#ff6b6b"),
                        ),
                        padding="20px", background_color=CARD_BG, border_radius="15px", width="100%"
                    ),
                    template_columns="1fr 1.5fr 1fr",
                    gap="20px",
                    width="100%",
                ),
                width="100%",
            ),
            width="100%",
            padding="25px",
            background_color=BG_DARK,
            height="100vh",
            overflow_y="auto",
        ),
        spacing="0",
        width="100%",
    )