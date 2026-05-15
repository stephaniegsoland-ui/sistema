import reflex as rx
from typing import List
from datetime import datetime
from sqlmodel import select
from ..api.models import ProcuraSolicitud, Producto, Usuario
from ..db_init import get_session
from typing import Any

class ProcuraState(rx.State):
    solicitudes: List[ProcuraSolicitud] = []
    view_tab: str = "Todas"
    search_text: str = ""
    
    departamentos: List[str] = [
        "Compras",
        "Almacén",
        "Logística",
        "Operaciones",
        "Mantenimiento",
    ]

    @rx.var
    def total_solicitudes(self) -> int:
        return len(self.solicitudes)

    @rx.var
    def total_pendientes(self) -> int:
        return sum(1 for item in self.solicitudes if not item.revisado)

    @rx.var
    def total_compradas(self) -> int:
        return sum(1 for item in self.solicitudes if item.comprado)

    @rx.var
    def total_enviadas(self) -> int:
        return sum(1 for item in self.solicitudes if item.enviado)

    @rx.var
    def solicitudes_filtradas(self) -> List[ProcuraSolicitud]:
        if self.view_tab == "Pendientes":
            return [item for item in self.solicitudes if not item.revisado]
        if self.view_tab == "Revisadas":
            return [item for item in self.solicitudes if item.revisado]
        if self.view_tab == "Compradas":
            return [item for item in self.solicitudes if item.comprado]
        if self.view_tab == "Enviadas":
            return [item for item in self.solicitudes if item.enviado]
        return self.solicitudes

    def load_solicitudes(self):
        with get_session() as session:
            self.solicitudes = session.exec(
                select(ProcuraSolicitud).order_by(ProcuraSolicitud.id.desc())
            ).all()

    def set_tab(self, value: str | list[str]):
        if isinstance(value, list):
            self.view_tab = value[0] if value else "Resumen"
        else:
            self.view_tab = value
    def set_search(self, value: str):
        self.search_text = value

    def crear_solicitud(self, form_data: dict):
        # Validaciones robustas
        fields = {"solicitante": "Solicitante", "material": "Material", "cantidad": "Cantidad", "fecha_entrega": "Fecha de entrega"}
        for field, label in fields.items():
            if not form_data.get(field):
                return rx.window_alert(f"El campo {label} es obligatorio")

        try:
            cantidad = int(form_data.get("cantidad", 0))
            if cantidad <= 0 or cantidad > 1000:
                return rx.window_alert("La cantidad debe estar entre 1 y 1000")
        except: return rx.window_alert("Cantidad inválida")

        with get_session() as session:
            # Integración: Mostrar stock disponible (opcional en UI, validación aquí)
            stock_existente = session.exec(select(Producto).where(Producto.nombre == form_data["material"])).first()
            obs = f"Stock actual en almacén: {stock_existente.cantidad}" if stock_existente else "No hay existencias previas."

            nueva = ProcuraSolicitud(
                solicitante=form_data["solicitante"],
                departamento=form_data.get("departamento", "Compras"),
                categoria=form_data.get("categoria", "General"),
                material=form_data["material"],
                cantidad=cantidad,
                detalle=form_data.get("detalle", ""),
                prioridad=form_data.get("prioridad", "Normal"),
                fecha_entrega_deseada=form_data["fecha_entrega"],
                fecha_solicitud=datetime.utcnow().isoformat(),
                observaciones=obs,
                estado="Pendiente Aprobación"
            )
            session.add(nueva)
            session.commit()

        self.load_solicitudes()
        return rx.window_alert("Solicitud enviada a aprobación")

    def _actualizar_estado(self, solicitud_id: int, tipo_accion: str):
        with get_session() as session:
            solicitud = session.get(ProcuraSolicitud, solicitud_id)
            if solicitud:
                # En lugar de solicitud.estado = ..., usamos esto:
                if tipo_accion == "Revisada":
                    solicitud.revisado = True
                elif tipo_accion == "Comprada":
                    solicitud.comprado = True
                elif tipo_accion == "Enviada":
                    solicitud.enviado = True
                
                session.add(solicitud)
                session.commit()
        return self.load_solicitudes()
    def aprobar_solicitud(self, id: int):
        self._actualizar_estado(id, "Aprobada")

    def rechazar_solicitud(self, id: int, motivo: str):
        self._actualizar_estado(id, "Rechazada", motivo)

    def marcar_revisado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Revisada")

    def marcar_comprado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Comprada")

    def marcar_enviado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Enviada")
