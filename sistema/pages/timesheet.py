import reflex as rx
# Si vas a usar Inteligencia Artificial en esta página, descomenta la siguiente línea:
# import google.generativeai as genai

# 1. Definimos el estado de la página (para manejar formularios o datos)
class TimesheetState(rx.State):
    horas_trabajadas: str = ""
    notas: str = ""
    mensaje_confirmacion: str = ""

    def guardar_registro(self):
        # Aquí irá tu lógica para guardar en base de datos o procesar con Gemini
        if self.horas_trabajadas:
            self.mensaje_confirmacion = f"¡Registradas {self.horas_trabajadas} horas con éxito!"
        else:
            self.mensaje_confirmacion = "Por favor, introduce las horas."

# 2. La función principal que EXPORTA la página (El nombre que fallaba)
@rx.page(route="/timesheet", title="Control de Horas")
def timesheet_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Registro de Horas (Timesheet)", size="7"),
        rx.text("Introduce las horas trabajadas el día de hoy:"),
        
        # Formulario básico
        rx.vstack(
            rx.input(
                placeholder="Número de horas (ej. 8)", 
                on_change=TimesheetState.set_horas_trabajadas,
                type="number"
            ),
            rx.text_area(
                placeholder="¿En qué trabajaste hoy?", 
                on_change=TimesheetState.set_notas
            ),
            rx.button("Guardar Jornada", on_click=TimesheetState.guardar_registro),
            spacing="3",
            width="100%",
            max_width="400px",
        ),
        
        # Mensaje de feedback
        rx.cond(
            TimesheetState.mensaje_confirmacion != "",
            rx.text(TimesheetState.mensaje_confirmacion, color="green", weight="bold")
        ),
        
        spacing="5",
        padding="2rem",
        align="center",
        justify="center",
        min_height="80vh"
    )