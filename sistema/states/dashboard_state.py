import reflex as rx
import datetime
import pytz
from sqlmodel import select
from ..api.models import Producto
from ..db_init import get_session

class DashboardState(rx.State):
    # Variables de tiempo
    @rx.var
    def hora_venezuela(self) -> str:
        return datetime.datetime.now(pytz.timezone("America/Caracas")).strftime("%H:%M:%S")

    @rx.var
    def hora_espana(self) -> str:
        return datetime.datetime.now(pytz.timezone("Europe/Madrid")).strftime("%H:%M:%S")

    @rx.var
    def hora_usa(self) -> str:
        return datetime.datetime.now(pytz.timezone("US/Eastern")).strftime("%H:%M:%S")

    @rx.var
    def hora_china(self) -> str:
        return datetime.datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%H:%M:%S")

    @rx.var
    def eficiencia(self) -> str:
        return "94%"

    @rx.var
    def resolucion(self) -> str:
        return "88%"

    @rx.var
    def satisfaccion(self) -> str:
        return "96%"

    @rx.var
    def disponibilidad(self) -> str:
        return "100%"

    # Lógica de Stock desde la BD
    @rx.var
    def total_stock(self) -> str:
        try:
            with get_session() as session:
                productos = session.exec(select(Producto)).all()
                total = sum(p.cantidad for p in productos)
                return f"{total:,}"
        except Exception:
            return "0"

    @rx.var
    def tickets_pendientes(self) -> str:
        return "12"

    @rx.var
    def tickets_en_proceso(self) -> str:
        return "8"

    @rx.var
    def tickets_completados(self) -> str:
        return "24"

    @rx.var
    def alta_prioridad(self) -> str:
        return "3"

    @rx.var
    def media_prioridad(self) -> str:
        return "7"

    @rx.var
    def baja_prioridad(self) -> str:
        return "10"

    @rx.var
    def tiempo_promedio(self) -> str:
        return "2.4 hrs"

    @rx.var
    def tasa_sla(self) -> str:
        return "96%"

    @rx.var
    def inventario_alicate(self) -> int:
        return 48

    @rx.var
    def inventario_mascaras(self) -> int:
        return 92

    @rx.var
    def inventario_n95(self) -> int:
        return 124

    @rx.var
    def inventario_escritorio(self) -> int:
        return 56

    @rx.var
    def pedido_botas(self) -> int:
        return 82

    @rx.var
    def pedido_suministros(self) -> int:
        return 520

    @rx.var
    def pedido_equipos(self) -> int:
        return 260

    def check_login(self):
        if not self.is_hydrated:
            return
        pass