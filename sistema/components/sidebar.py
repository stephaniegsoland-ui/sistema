import reflex as rx
# Importamos el estado para manejar el logout y el nombre del usuario
from sistema.states.auth_state import AuthState 

def sidebar_header(title: str):
    return rx.text(
        title,
        color="gray",
        font_size="10px",
        font_weight="bold",
        margin_top="15px",
        margin_bottom="5px",
        text_transform="uppercase",
        padding_x="15px",
    )

def sidebar_item(text: str, icon: str, href: str, active: bool = False):
    return rx.link(
        rx.hstack(
            rx.icon(tag=icon, size=18),
            rx.text(text, font_size="14px"),
            # Estilo condicional basado en si la página está activa
            bg=rx.cond(active, "rgba(255, 215, 0, 0.1)", "transparent"),
            color=rx.cond(active, "#FFD700", "#A0A0A0"),
            border_left=rx.cond(active, "3px solid #FFD700", "none"),
            padding="8px 15px",
            width="100%",
            _hover={"color": "#FFD700", "bg": "rgba(255, 255, 255, 0.05)"},
            transition="all 0.2s ease",
        ),
        href=href,
        text_decoration="none",
        width="100%",
    )

def sidebar(current_page: str = ""):
    return rx.vstack(
        # Logo y Encabezado
        rx.vstack(
            rx.heading("SOLAND", color="#FFD700", size="6"),
            rx.text("Sistema de Suministros", size="1", color="gray"),
            align_items="start",
            padding_x="15px",
            padding_top="20px",
            margin_bottom="10px",
        ),
        
        rx.divider(border_color="#222"),

        # Menú Desplazable
        rx.vstack(
            sidebar_header("Principal"),
            sidebar_item("Dashboard", "layout-dashboard", "/dashboard", active=current_page == "/dashboard"),

            sidebar_header("Gestión"),
            sidebar_item("Stock", "box", "/stock", active=current_page == "/stock"),
            sidebar_item("Procura", "shopping-cart", "/procura", active=current_page == "/procura"),
            sidebar_item("Personal", "users", "/personal", active=current_page == "/personal"),
            sidebar_item("Seguridad EPP", "shield-check", "/epp", active=current_page == "/epp"),
            sidebar_item("Vehículos", "truck", "/vehiculos", active=current_page.startswith("/vehiculos")),
            rx.vstack(
                sidebar_item("Reportes de vehículos", "file-text", "/vehiculos/reportes", active=current_page == "/vehiculos/reportes"),
                padding_left="20px",
                width="100%",
            ),
            sidebar_header("Operaciones"),
            sidebar_item("Seguridad", "lock", "/seguridad", active=current_page == "/seguridad"),
            sidebar_item("Scanner", "maximize", "/scanner", active=current_page == "/scanner"),
            sidebar_item("Hoja de Tiempo", "clock", "/tiempo", active=current_page == "/tiempo"),

            sidebar_header("Análisis"),
            sidebar_item("IA", "brain", "/ia", active=current_page == "/ia"),

            sidebar_header("Administración"),
            sidebar_item("Configuración", "settings", "/configuracion", active=current_page == "/configuracion"),
            
            width="100%",
            align_items="start",
            overflow_y="auto", 
            flex="1",
            padding_bottom="20px",
        ),

        # Pie de página (Usuario y Salir)
        rx.vstack(
            rx.divider(border_color="#222"),
            rx.hstack(
                rx.center(
                    rx.icon(tag="user", color="black", size=20),
                    bg="#FFD700",
                    width="40px",
                    height="40px",
                    border_radius="8px",
                ),
                rx.vstack(
                    # Usamos el estado real del usuario si está disponible
                    rx.text("Usuario Activo", color="white", font_size="14px", font_weight="bold"),
                    rx.text(AuthState.usuario_actual.nombre_usuario, color="gray", font_size="10px"),
                    spacing="0",
                    align_items="start",
                ),
                padding="10px",
                width="100%",
            ),
            rx.button(
                rx.hstack(rx.icon(tag="log-out", size=16), rx.text("Salir")),
                on_click=AuthState.logout, # Conectamos la acción de salir
                width="100%",
                bg="#FFD700",
                color="black",
                _hover={"bg": "#e6c200", "cursor": "pointer"},
                margin_top="5px",
            ),
            width="100%",
            padding="15px",
            bg="#080808", # Un tono ligeramente más oscuro para el pie
        ),

        width="260px",
        height="100vh",
        bg="#0B0B0B",
        border_right="1px solid #222",
        spacing="0",
        align_items="start",
    )