import reflex as rx
from sistema.states.personal_state import SessionState as PersonalState
from sistema.api.models import Usuario

def formulario_registro() -> rx.Component:
    return rx.vstack(
        rx.heading("Registrar Colaborador", size="4", color="#FFD700"),
        
        rx.input(placeholder="Nombre de Usuario / Login", value=PersonalState.input_usuario, on_change=PersonalState.set_input_usuario, width="100%"),
        rx.input(placeholder="Contraseña", type="password", value=PersonalState.input_password, on_change=PersonalState.set_input_password, width="100%"),
        
        rx.text("Perfil Jerárquico:", size="1", color="gray"),
        rx.select(
            ["1", "2", "3"],
            value=PersonalState.perfil_jerarquico,
            on_change=PersonalState.set_perfil_jerarquico,
            width="100%"
        ),
        
        rx.text("Asignación de Módulos (Permisos):", size="1", color="gray", margin_top="10px"),
        
        rx.vstack(
            rx.checkbox("Dashboard Principal", checked=PersonalState.modulo_dashboard, on_change=PersonalState.set_modulo_dashboard),
            rx.checkbox("Inventario / Stock", checked=PersonalState.modulo_stock, on_change=PersonalState.set_modulo_stock),
            rx.checkbox("Procura de Materiales", checked=PersonalState.modulo_procura, on_change=PersonalState.set_modulo_procura),
            rx.checkbox("Seguridad EPP", checked=PersonalState.modulo_epp, on_change=PersonalState.set_modulo_epp),
            rx.checkbox("Control de Vehículos", checked=PersonalState.modulo_vehiculos, on_change=PersonalState.set_modulo_vehiculos),
            rx.checkbox("Hoja de Tiempo", checked=PersonalState.modulo_hoja_tiempo, on_change=PersonalState.set_modulo_hoja_tiempo),
            rx.checkbox("Módulo de IA", checked=PersonalState.modulo_ia, on_change=PersonalState.set_modulo_ia),
            spacing="2",
            align_items="start",
            width="100%"
        ),
        
        rx.button(
            "Guardar en Base de Datos", 
            on_click=PersonalState.registrar_colaborador,
            color_scheme="yellow", 
            width="100%",
            margin_top="15px"
        ),
        
        spacing="3",
        width="100%",
        max_width="380px",
        padding="5",
        background_color="#1e1e1e",
        border="1px solid #333333",
        border_radius="var(--radius-3)"
    )

def tabla_personal() -> rx.Component:
    def fila_usuario(user: Usuario):
        color_badge = rx.cond(user.nivel == 1, "red", rx.cond(user.nivel == 2, "blue", "green"))
        texto_badge = rx.cond(user.nivel == 1, "Admin", rx.cond(user.nivel == 2, "Supervisor", "Empleado"))

        return rx.table.row(
            rx.table.cell(user.nombre_usuario, weight="bold"),
            rx.table.cell(rx.badge(texto_badge, color_scheme=color_badge)),
            rx.table.cell(user.estado, size="1", color="#aaaaaa"),
            rx.table.cell("Activo", color="green")
        )

    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Usuario (Login)"),
                    rx.table.column_header_cell("Perfil"),
                    rx.table.column_header_cell("Módulos Autorizados"),
                    rx.table.column_header_cell("Estado"),
                )
            ),
            rx.table.body(rx.foreach(PersonalState.usuarios, fila_usuario)),
            width="100%"
        ),
        width="100%"
    )