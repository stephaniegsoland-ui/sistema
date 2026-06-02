import reflex as rx
from typing import List, Dict
import datetime

class TimesheetState(rx.State):
    actividades_quincena: list[dict] = []
    @rx.var
    def actividades_quincena(self) -> list[dict]:
        """Esta es la Computed Var. Ahora ya no hace 'shadow' porque la base se llama distinto."""
        # Filtramos la lista base
        return [
            a for a in self.lista_actividades 
            if a.get("periodo") == self.id_quincena_actual
        ]
    historial_quincenas: list[dict] = [
        {"periodo": "2026-05-Q1", "total_horas": 82, "viaticos": 150, "estado": "Cerrado"},
    ]
    quincena_cerrada: bool = False

    def cerrar_quincena(self):
        if self.total_horas_quincena < 80:
            return rx.window_alert("No puedes cerrar la quincena sin completar las 80 horas.")
        
        # Lógica para bloquear y guardar
        self.quincena_cerrada = True
        nuevo_registro = {
            "periodo": f"2026-{self.mes_seleccionado}-Q{self.quincena_seleccionada}",
            "total_horas": self.total_horas_quincena,
            "viaticos": self.total_viaticos_quincena,
            "estado": "Cerrado"
        }
        self.historial_quincenas.append(nuevo_registro)
        return rx.toast.success("Quincena cerrada y guardada con éxito.")
    
    # Estructura: { "2026-05-1": [...], "2026-05-2": [...] } (Año-Mes-Quincena)
    historial_quincenal: Dict[str, List[Dict]] = {}
    lista_actividades: list[dict] = []
    # Formulario actual
    fecha_actividad: str = datetime.date.today().strftime("%Y-%m-%d")
    actividad: str = ""
    quincena_seleccionada: str = "1" # "1" o "2"
    mes_seleccionado: str = datetime.date.today().strftime("%m")
    horas: int = 8
    viaticos: float = 0.0

    # Agregamos setters manuales para convertir el String del input a Número
    def cambiar_horas(self, valor: str):
        try:
            self.horas = int(valor) if valor != "" else 0
        except ValueError:
            self.horas = 0

    def cambiar_viaticos(self, valor: str):
        try:
            # Reemplazamos coma por punto por si el usuario usa formato decimal latino
            valor = valor.replace(",", ".")
            self.viaticos = float(valor) if valor != "" else 0.0
        except ValueError:
            self.viaticos = 0.0
    @rx.var
    def id_quincena_actual(self) -> str:
        return f"2026-{self.mes_seleccionado}-{self.quincena_seleccionada}"

    @rx.var
    def actividades_quincena(self) -> List[Dict]:
        return self.historial_quincenal.get(self.id_quincena_actual, [])

    @rx.var
    def total_horas_quincena(self) -> int:
        return sum(int(a["horas"]) for a in self.actividades_quincena)

    @rx.var
    def total_viaticos_quincena(self) -> float:
        return sum(float(a["viaticos"]) for a in self.actividades_quincena)

    @rx.var
    def horas_hoy(self) -> int:
        return sum(int(a["horas"]) for a in self.actividades_quincena if a["fecha"] == self.fecha_actividad)

    @rx.var
    def progreso_dia(self) -> int:
        # Retorna el porcentaje de cumplimiento diario (meta 8h)
        return min(int((self.horas_hoy / 8) * 100), 100)

    def guardar_actividad(self):
        nueva_act = {
            "fecha": self.fecha_actividad,
            "actividad": self.actividad,
            "horas": self.horas,
            "viaticos": self.viaticos,
        }
        
        # Lógica de guardado por quincena
        key = self.id_quincena_actual
        if key not in self.historial_quincenal:
            self.historial_quincenal[key] = []
        
        self.historial_quincenal[key].append(nueva_act)
        self.actividad = ""
        self.viaticos = 0.0
        return rx.toast.success(f"Actividad guardada en la quincena {self.quincena_seleccionada}")