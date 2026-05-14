import reflex as rx
from typing import List
from ..api.models import Vehiculo


class FleetState(rx.State):

    vehiculos: List[Vehiculo] = [
        Vehiculo(nombre="Hilux", modelo="Toyota Hilux Diesel", placa="ABC-123", imagen_url="/hilux.png"),
        Vehiculo(nombre="Hilux", modelo="Toyota Hilux Gasolina", placa="ABC-123", imagen_url="/hilux.png"),
        Vehiculo(nombre="Jack", modelo="Jack 2026", placa="JACK-2026", imagen_url="/jack.png"),
        Vehiculo(nombre="kia", modelo="kia 2016", placa="KIA-2016", imagen_url="/kia.png"),
        Vehiculo(nombre="Duty", modelo="Super duty", placa="---", imagen_url="/super_duty.png"),
    ]

    def iniciar_comparacion(self, placa: str):
        # Aquí redirigirías a la página de inspección con IA
        return rx.console_log(f"Iniciando inspección para placa: {placa}")