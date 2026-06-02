import reflex as rx
from sistema.states.personal_state import SessionState


# --- En tu archivo sidebar.py ---


def sidebar_header() -> rx.Component:
    return rx.vstack(
        # Contenedor del Logo con márgenes externos bien compactos
        rx.center(
            rx.image(
                src="/logo.png",
                width="194px",           # Aumentamos un poco el tamaño
                height="102px",
                border_radius="60%",     # Círculo perfecto
                object_fit="cover",      # <--- CRÍTICO: Fuerza a la imagen a rellenar y cubrir todo el espacio
                border="0px solid #FFD700", # El borde amarillo brillante de la referencia
                padding="0px",           # Nos aseguramos de que no haya separación interna
            ),
            width="100%",
            padding_top="15px",          # Reducido para evitar exceso de espacio arriba
            margin_bottom="5px",         # Reducido para acercarlo más al texto SOLAND
        ),
        
        # Textos de la marca alineados al centro debajo del logo
        rx.vstack(
            rx.heading(
                "SOLAND", 
                color="#FFD700", 
                size="6", 
                letter_spacing="2px",
                weight="bold"
            ),
            rx.text(
                "Sistema de Suministros", 
                size="1", 
                color="gray",
                letter_spacing="0.5px"
            ),
            spacing="0",                 # Pegamos el subtítulo al título
            align_items="center",
            width="100%",
        ),
        
        align_items="center",
        width="100%",
        margin_bottom="15px",
        padding_bottom="15px",
        border_bottom="1px solid #222225", # Línea divisoria antes de las opciones
    )
# ... El resto de tus funciones (sidebar_item y sidebar) se mantienen igual ...

def sidebar_item(text: str, icon: str, href: str, active: bool = False) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(tag=icon, size=18),
            rx.text(text, font_size="14px"),
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

def sidebar(current_page: str = "") -> rx.Component:
    # Si eres Admin por nivel (1) o tu string dice TODOS o all, tienes pase total
    es_admin = (SessionState.nivel_usuario == 1) | SessionState.permisos_raw.contains("TODOS") | SessionState.permisos_raw.contains("all")
    p = SessionState.permisos_raw

    return rx.vstack(
        sidebar_header(),
        
        rx.vstack(
            # 1. DASHBOARD
            rx.cond(
                es_admin | p.contains("dash") | p.contains("Dashboard Principal"),
                sidebar_item("Dashboard", "layout_dashboard", "/dashboard", current_page == "/dashboard"),
            ),
            
            rx.text("GESTIÓN", size="1", color="gray", padding_x="15px", margin_top="10px"),
            
            # 2. STOCK
            rx.cond(
                es_admin | p.contains("stock") | p.contains("Inventario / Stock"),
                sidebar_item("Stock", "boxes", "/stock", current_page == "/stock"),
            ),
            
            # 3. PROCURA
            rx.cond(
                es_admin | p.contains("proc") | p.contains("Procura de Materiales"),
                sidebar_item("Procura", "shopping_cart", "/procura", current_page == "/procura"),
            ),
            
            # 4. PERSONAL (Módulo maestro de control, restringido de forma segura)
            rx.cond(
                es_admin,
                sidebar_item("Personal", "users", "/personal", current_page == "/personal"),
            ),
            
            # 5. SEGURIDAD EPP
            rx.cond(
                es_admin | p.contains("epp") | p.contains("Seguridad EPP") | p.contains("Control de EPP"),
                sidebar_item("Seguridad EPP", "shield_check", "/epp", current_page == "/epp"),
            ),
            
            # 6. VEHÍCULOS
            rx.cond(
                es_admin | p.contains("fleet") | p.contains("Vehículos") | p.contains("Control de Vehículos") | p.contains("Flota"),
                sidebar_item("Vehículos", "truck", "/fleet", current_page == "/fleet"),
            ),
            
            rx.text("OPERACIONES", size="1", color="gray", padding_x="15px", margin_top="10px"),
            
            # 7. HOJA DE TIEMPO
            rx.cond(
                es_admin | p.contains("time") | p.contains("Hoja de Tiempo"),
                sidebar_item("Hoja de Tiempo", "clock", "/timesheet", current_page == "/timesheet"),
            ),
            
            rx.text("ANÁLISIS", size="1", color="gray", padding_x="15px", margin_top="10px"),
            
            # 8. MÓDULO INTELIGENCIA ARTIFICIAL
            rx.cond(
                es_admin | p.contains("ia") | p.contains("IA"),
                sidebar_item("IA", "brain", "/ia", current_page == "/ia"),
            ),
            
            width="100%",
            spacing="1",
            align_items="stretch",
        ),
        
        rx.spacer(),
        
        # Perfil inferior
        rx.vstack(
            rx.hstack(
                rx.avatar(fallback=SessionState.usuario_logueado[0:2].upper(), size="2", color_scheme="yellow"),
                rx.vstack(
                    rx.text(SessionState.usuario_logueado, size="2", weight="bold", color="white"),
                    rx.text(
                        rx.cond(SessionState.nivel_usuario == 1, "Administrador", "Colaborador"), 
                        size="1", color="gray"
                    ),
                    spacing="0",
                    align_items="start"
                ),
                spacing="3",
                padding_x="15px",
                margin_bottom="10px"
            ),
            rx.button(
                rx.hstack(rx.icon("log_out", size=16), rx.text("Salir")),
                on_click=SessionState.logout_usuario,
                color_scheme="yellow",
                variant="solid",
                width="90%",
                margin_x="auto",
                margin_bottom="20px",
                type="button",
            ),
            width="100%"
        ),
        
        width="260px",
        height="100vh",
        background_color="#111113",
        border_right="1px solid #222225",
        # ¡ELIMINADOS!: position="fixed", top="0", left="0", z_index="1000"
    )