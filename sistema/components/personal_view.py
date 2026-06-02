import reflex as rx
from sistema.states.personal_state import SessionState as PersonalState
from sistema.states.fleet_state import FleetState
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
            rx.cond(PersonalState.editing_id != None, "Actualizar Colaborador", "Guardar en Base de Datos"),
            on_click=PersonalState.registrar_colaborador,
            color_scheme="yellow", 
            width="100%",
            margin_top="15px"
        ),
        # Extra person fields
        rx.input(placeholder="Teléfono", value=PersonalState.input_telefono, on_change=PersonalState.set_input_telefono, width="100%", margin_top="8px"),
        rx.input(placeholder="Dirección", value=PersonalState.input_direccion, on_change=PersonalState.set_input_direccion, width="100%", margin_top="8px"),
        rx.text_area(placeholder="Notas / Observaciones", value=PersonalState.input_notas, on_change=PersonalState.set_input_notas, width="100%", margin_top="8px"),
        rx.select(FleetState.placas, placeholder="Vehículo asignado (placa)", value=PersonalState.input_vehiculo_asignado, on_change=PersonalState.set_input_vehiculo_asignado, width="100%", margin_top="8px"),
        rx.input(placeholder="URL CV (o subir archivo)", value=PersonalState.input_cv_url, on_change=PersonalState.set_input_cv_url, width="100%", margin_top="8px"),
        rx.input(placeholder="URL Foto (o subir archivo)", value=PersonalState.input_foto_url, on_change=PersonalState.set_input_foto_url, width="100%", margin_top="8px"),
        rx.button("Limpiar formulario", on_click=PersonalState.limpiar_formulario, variant="ghost", width="100%", margin_top="8px"),
        rx.cond(
            PersonalState.editing_id != None,
            rx.button("Cancelar edición", on_click=PersonalState.cancelar_edicion, variant="ghost", width="100%", margin_top="8px"),
            None,
        ),
        # Small edit mode indicator
        rx.cond(PersonalState.editing_id != None, rx.text("Modo edición activo", color="#FFD700", size="1"), None),
        
        spacing="4",
        width="100%",
        max_width="440px",
        padding="1.25rem",
        background_color="#151515",
        border="1px solid #232323",
        border_radius="12px",
        box_shadow="0 6px 18px rgba(0,0,0,0.6)",
        align_items="stretch",
        margin_right="1.5rem"
    )

def tabla_personal() -> rx.Component:
    def card_usuario(user: Usuario):
        color_badge = rx.cond(user.nivel == 1, "red", rx.cond(user.nivel == 2, "blue", "green"))
        texto_badge = rx.cond(user.nivel == 1, "Admin", rx.cond(user.nivel == 2, "Supervisor", "Empleado"))

        return rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(user.nombre_usuario, weight="bold"),
                    rx.hstack(
                        rx.badge(texto_badge, color_scheme=color_badge),
                        rx.cond(user.estado != "", rx.text(user.estado, color="gray"), rx.text("-", color="gray")),
                    ),
                ),
                rx.vstack(
                    rx.button("Editar", on_click=PersonalState.editar_colaborador(user.id), size="2", variant="outline"),
                    rx.button("Eliminar", on_click=PersonalState.confirmar_eliminar_colaborador(user.id), size="2", color_scheme="red"),
                    spacing="2",
                    align_items="end",
                ),
                justify_content="space-between",
                width="100%",
            ),
            padding="1rem",
            background_color="#0f0f0f",
            border="1px solid #222",
            border_radius="8px",
            width="100%",
        )

    return rx.vstack(
        rx.box(
            rx.input(placeholder="Buscar usuario...", value=PersonalState.search_query, on_change=PersonalState.set_search_query, width="100%", margin_bottom="12px"),
            padding="0.75rem",
            background_color="transparent",
        ),
        rx.box(
            rx.grid(rx.foreach(PersonalState.usuarios, card_usuario), template_columns="repeat(auto-fit, minmax(320px, 1fr))", gap="16px", width="100%"),
            padding="0.5rem",
            background_color="transparent",
            width="100%",
        ),
        # Confirmation modal for deletion (overlay)
        rx.cond(
            PersonalState.pending_delete_id != None,
            rx.box(
                rx.box(
                    rx.heading("Confirmar eliminación", size="4", color="#FFD700"),
                    rx.text("¿Seguro que desea eliminar este colaborador? Esta acción no se puede deshacer."),
                    rx.hstack(
                        rx.button("Cancelar", on_click=PersonalState.cancelar_eliminar, variant="ghost"),
                        rx.button("Eliminar", on_click=PersonalState.eliminar_colaborador(PersonalState.pending_delete_id), color_scheme="red"),
                        spacing="3",
                    ),
                    padding="1.25rem",
                    background_color="#111",
                    border_radius="10px",
                    min_width="360px",
                    color="#fff",
                ),
                position="fixed",
                inset="0",
                display="flex",
                align_items="center",
                justify_content="center",
                background_color="rgba(0,0,0,0.6)",
                z_index=500,
            ),
            None,
        ),
        width="100%",
    )