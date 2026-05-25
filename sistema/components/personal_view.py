import reflex as rx
from sistema.states.personal_state import PersonalState, SessionState
from sistema.api.models import Usuario

def barra_simulacion_login() -> rx.Component:
    # Mapeo visual para entender los niveles numéricos de tu código
    rol_actual = rx.cond(SessionState.nivel_usuario == 1, "Administrador", 
                 rx.cond(SessionState.nivel_usuario == 2, "Supervisor", "Empleado"))
                 
    return rx.hstack(
        rx.text("Rol de Sesión Actual:", weight="bold", size="2", color="#aaaaaa"),
        rx.select(
            ["Empleado", "Supervisor", "Administrador"],
            value=rol_actual,
            on_change=SessionState.cambiar_sesion_prueba,
            color_scheme="yellow",
        ),
        rx.badge(f"Sesión: {SessionState.usuario_logueado}", color_scheme="yellow", variant="soft"),
        background_color="rgba(255, 255, 255, 0.03)",
        padding="3",
        border_radius="md",
        width="100%",
        spacing="3",
        border="1px dashed #333333",
        margin_bottom="4"
    )

def formulario_registro() -> rx.Component:
    
    return rx.card(
        rx.vstack(
            rx.heading("Registrar Colaborador", size="4", color="#FFD700"),
            
            rx.input(placeholder="Nombre de Usuario (Login)", value=PersonalState.input_usuario, on_change=PersonalState.set_input_usuario, width="100%"),
            rx.input(placeholder="Contraseña", type="password", value=PersonalState.input_password, on_change=PersonalState.set_input_password, width="100%"),
            
            rx.text("Nivel de Acceso:", size="1", color="gray", weight="bold"),
            rx.select(
                {"1": "1: Admin", "2": "2: Supervisor", "3": "3: Usuario"}, 
                value=PersonalState.nivel_seleccionado, 
                on_change=PersonalState.set_nivel_seleccionado, 
                width="100%"
            ),
            
            # Permisos basados en los módulos del Sidebar
            rx.vstack(
                rx.text("Otorgar Módulos Coincidentes:", size="1", color="gray", weight="bold"),
                rx.checkbox("Dashboard Principal", checked=PersonalState.modulo_dashboard, on_change=PersonalState.set_modulo_dashboard, color_scheme="yellow"),
                rx.checkbox("Inventario / Stock", checked=PersonalState.modulo_stock, on_change=PersonalState.set_modulo_stock, color_scheme="yellow"),
                rx.checkbox("Procura", checked=PersonalState.modulo_procura, on_change=PersonalState.set_modulo_procura, color_scheme="yellow"),
                rx.checkbox("Seguridad EPP", checked=PersonalState.modulo_seguridad_epp, on_change=PersonalState.set_modulo_seguridad_epp, color_scheme="yellow"),
                rx.checkbox("Vehículos", checked=PersonalState.modulo_vehiculos, on_change=PersonalState.set_modulo_vehiculos, color_scheme="yellow"),
                rx.checkbox("Hoja de Tiempo", checked=PersonalState.modulo_hoja_tiempo, on_change=PersonalState.set_modulo_hoja_tiempo, color_scheme="yellow"),
                align_items="start",
                spacing="2",
                width="100%"
            ),
            
            # Carga de CV / Hoja de vida
            rx.vstack(
                rx.text("Hoja de Vida (CV):", size="1", color="gray", weight="bold"),
                rx.upload(
                    rx.vstack(
                        rx.icon("upload", size=20, color="#FFD700"),
                        rx.text("Subir archivo de Hoja de Vida", size="1"),
                    ),
                    id="upload_cv_real",
                    border="1px dashed #555555",
                    padding="2",
                    border_radius="md",
                    width="100%",
                ),
                rx.button(
                    "Procesar CV", 
                    on_click=lambda: PersonalState.manejar_subida_cv(rx.upload_files(upload_id="upload_cv_real")),
                    size="1", variant="soft", width="100%"
                ),
                width="100%", spacing="2"
            ),
            
            rx.button("Guardar en Base de Datos", on_click=PersonalState.crear_usuario, color_scheme="yellow", width="100%", margin_top="2"),
            spacing="3",
        ),
        width="100%", max_width="390px", style={"background_color": "#18181b", "border": "1px solid #27272a"}
    )

def tabla_personal() -> rx.Component:
    def fila_usuario(user: Usuario):
        # 1. Mapeo del color_scheme del nivel (Usando rx.cond en cascada)
        color_perfil = rx.cond(
            user.nivel == 1, 
            "red", 
            rx.cond(user.nivel == 2, "blue", "green")
        )
        
        # 2. Mapeo del texto legible del nivel
        texto_perfil = rx.cond(
            user.nivel == 1, 
            "Admin", 
            rx.cond(user.nivel == 2, "Supervisor", "Usuario")
        )

        # 3. CORRECCIÓN CRÍTICA: Mapeo del color_scheme de estado usando rx.cond de Reflex
        color_estado = rx.cond(
            user.estado == "activo", 
            "green", 
            "gray"
        )
                 
        return rx.table.row(
            rx.table.cell(user.nombre_usuario, weight="bold"),
            rx.table.cell(rx.badge(texto_perfil, color_scheme=color_perfil)),
            rx.table.cell(rx.badge(user.estado, color_scheme=color_estado)),
            rx.table.cell("Asistencia: 100%", size="1"),
        )
        
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Usuario (Login)"),
                    rx.table.column_header_cell("Nivel"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Asistencia / CV"),
                )
            ),
            rx.table.body(rx.foreach(PersonalState.usuarios, fila_usuario)),
            width="100%"
        ),
        width="100%",
        style={"background_color": "#18181b", "border": "1px solid #27272a", "border_radius": "var(--radius-3)", "padding": "4"}
    )