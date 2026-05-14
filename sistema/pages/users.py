import reflex as rx
from ..styles.colors import BG_DARK, ACCENT_YELLOW, CARD_BG
from ..state.user_management import UserManagementState
from ..api.models import Usuario

def user_row(user: Usuario):
    return rx.table.row(
        rx.table.cell(user.nombre_usuario),
        rx.table.cell(rx.cond(user.nivel == 1, "Admin", "Operador")),
        rx.table.cell(user.estado),
    )

@rx.page(route="/usuarios", on_load=UserManagementState.get_all_users)
def users_page():
    return rx.vstack(
        rx.heading("GESTIÓN DE PERSONAL TÁCTICO", color=ACCENT_YELLOW),
        
        # Formulario de Registro
        rx.form(
            rx.vstack(
                rx.text("Registrar Nuevo Usuario"),
                rx.input(placeholder="Nombre de Usuario", name="nuevo_user", width="300px"),
                rx.input(placeholder="Password", name="nuevo_pass", type="password", width="300px"),
                rx.select(
                    ["1", "2", "3"], 
                    placeholder="Nivel de Acceso", 
                    name="nivel",
                    width="300px"
                ),
                rx.button("REGISTRAR EN SISTEMA", type="submit", background_color=ACCENT_YELLOW, color="black"),
                spacing="3",
                padding="20px",
                background_color=CARD_BG,
                border=f"1px solid {ACCENT_YELLOW}",
            ),
            on_submit=UserManagementState.add_user,
        ),

        # Tabla de Usuarios Actuales
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Usuario"),
                    rx.table.column_header_cell("Rango/Nivel"),
                    rx.table.column_header_cell("Estado"),
                ),
            ),
            rx.table.body(
                rx.foreach(UserManagementState.usuarios, user_row)
            ),
            width="100%",
            variant="surface",
        ),
        padding="40px",
        background_color=BG_DARK,
        min_height="100vh",
    )