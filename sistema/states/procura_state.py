import reflex as rx
from typing import List
from datetime import datetime
from sqlmodel import select
from ..api.models import ProcuraSolicitud, Producto, Usuario, MovimientoStock
from ..db_init import get_session
from typing import Any
from typing import Dict

class ProcuraState(rx.State):
    @rx.var
    def stats_adicionales(self) -> dict:
        """Calcula métricas de rendimiento logístico"""
        total = len(self.solicitudes)
        if total == 0:
            return {"tiempo_promedio": "0d", "eficiencia": "100%", "insumo_top": "N/A"}
        
        # Simulación de eficiencia basada en pedidos a tiempo vs retrasados
        enviados = len([s for s in self.solicitudes if s.enviado])
        eficiencia = int((enviados / total) * 100) if total > 0 else 100
        
        return {
            "tiempo_promedio": "1.2d", # Aquí podrías restar fechas reales
            "eficiencia": f"{eficiencia}%",
            "insumo_top": max(set([s.material for s in self.solicitudes]), key=[s.material for s in self.solicitudes].count) if total > 0 else "N/A"
        }
    @rx.var
    def analisis_ia_insumos(self) -> Dict:
        """Simulación de IA que analiza tendencias de consumo"""
        if not self.solicitudes:
            return {"mensaje": "Esperando datos...", "nivel": "info"}
        
        # Lógica de IA: Buscamos el material más repetido
        conteo = {}
        for s in self.solicitudes:
            nombre = s.material.strip().capitalize()
            conteo[nombre] = conteo.get(nombre, 0) + 1
        
        max_material = max(conteo, key=conteo.get)
        if conteo[max_material] > 3:
            return {
                "mensaje": f"Análisis IA: Se detectó una alta demanda de '{max_material}'. Sugerimos revisar proveedores para compra al mayor y reducir costos.",
                "nivel": "warning"
            }
        return {
            "mensaje": "Análisis IA: Consumo estable. No se requieren compras de emergencia actualmente.",
            "nivel": "success"
        }

    @rx.var
    def tabla_reporte_pedidos(self) -> List[Dict]:
        """Formatea los datos para la tabla de reportes final"""
        return [
            {
                "id": s.id,
                "fecha": "15/05/26", # Aquí usarías s.fecha_creacion
                "solicitante": s.solicitante,
                "material": s.material,
                "cantidad": s.cantidad,
                "estado": "Finalizado" if s.enviado else "En Proceso",
                "prioridad": "Alta" if s.cantidad > 10 else "Normal"
            }
            for s in self.solicitudes
        ]
    
    @rx.var
    def mensaje_estado_actual(self) -> str:
        if self.total_pendientes > 5:
            return "⚠️ Carga de trabajo alta: Hay varios pedidos pendientes de revisión."
        if self.total_pendientes > 0:
            return "🕒 Sistema operativo: Procesando solicitudes pendientes."
        return "✅ Todo al día: No hay solicitudes pendientes de despacho."
    
    def guardar_solicitud(self, data):
        # ... lógica de guardado ...
        yield rx.toast.info(
            f"Nueva solicitud creada por {data['solicitante']}",
            description=f"Material: {data['material']}",
            position="top-right",
            duration=5000,
        )

    @rx.var
    def data_historica(self) -> list[dict]:
        """Genera los datos para la gráfica de tendencia mensual"""
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        # Inicializamos todos los meses en 0
        conteo = {mes: 0 for mes in meses}
        
        # Simulamos o agrupamos por mes actual (Mayo en este caso)
        # Cuando tengas un campo 'fecha' real, aquí harías la lógica de conteo
        total_puntos = len(self.solicitudes)
        conteo["May"] = total_puntos 
        
        return [{"mes": k, "total": v} for k, v in conteo.items()]
    @rx.var
    def actividad_reciente(self) -> list[dict]:
        """Retorna las últimas 5 acciones registradas"""
        actividades = []
        sol_ordenadas = sorted(self.solicitudes, key=lambda x: x.id, reverse=True)[:5]
        for s in sol_ordenadas:
            status = (
                "Devuelto" if s.devuelto else
                "Entregado" if s.enviado else
                "Comprado" if s.comprado else
                "Revisado" if s.revisado else
                "Pendiente"
            )
            actividades.append({
                "descripcion": f"{s.solicitante} solicitó {s.material}",
                "status": status,
                "info": f"Cant: {s.cantidad}"
            })
        return actividades

    # El estado de las solicitudes se guarda directamente en el modelo SQLModel.

    @rx.var
    def stats_embudo_progreso(self) -> List[Dict]:
        """Datos para ver cuántas solicitudes hay en cada etapa"""
        estados = {"Pendientes": 0, "Revisadas": 0, "Compradas": 0, "Enviadas": 0}
        for s in self.solicitudes:
            if s.enviado: estados["Enviadas"] += 1
            elif s.comprado: estados["Compradas"] += 1
            elif s.revisado: estados["Revisadas"] += 1
            else: estados["Pendientes"] += 1
        return [{"name": k, "value": v} for k, v in estados.items()]

    @rx.var
    def top_departamentos_gastos(self) -> List[Dict]:
        """Calcula quién está pidiendo más (frecuencia por ahora)"""
        conteo = {}
        for s in self.solicitudes:
            depto = s.departamento if s.departamento else "General"
            conteo[depto] = conteo.get(depto, 0) + 1
        return [{"name": k, "pedidos": v} for k, v in conteo.items()]

    @rx.var
    def alerta_ia_reabastecimiento(self) -> str:
        """Simulación de lógica predictiva para insumos críticos"""
        if not self.solicitudes:
            return "Sin datos suficientes para predecir."
        # Aquí podrías conectar con Gemini en el futuro
        return "Sugerencia: El consumo de 'Hojas' ha subido un 20%. Se recomienda reabastecer antes del fin de semana."
    
    @rx.var
    def data_grafica_insumos(self) -> List[Dict]:
        """Cuenta cuántas veces se pide cada material"""
        conteo = {}
        for s in self.solicitudes:
            # Normalizamos a mayúsculas para evitar duplicados por tildes o minúsculas
            nombre = (s.material if s.material else "N/A").strip().capitalize()
            conteo[nombre] = conteo.get(nombre, 0) + 1
        
        # Formato para Recharts: [{"name": "Pilas", "count": 10}]
        return [{"name": k, "count": v} for k, v in sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:6]]

    @rx.var
    def data_grafica_departamentos(self) -> List[Dict]:
        """Cuenta solicitudes por departamento"""
        conteo = {}
        for s in self.solicitudes:
            depto = (s.departamento if s.departamento else "General").strip().capitalize()
            conteo[depto] = conteo.get(depto, 0) + 1
        return [{"name": k, "value": v} for k, v in conteo.items()]
    
    solicitudes: List[ProcuraSolicitud] = []
    view_tab: str = "Todas"
    search_text: str = ""
    
    categorias: List[str] = [
        "Herramientas",
        "Botas",
        "Bragas",
        "Suministros",
        "Lentes",
        "Equipos",
        "Otros",
    ]
    prioridades: List[str] = ["Normal", "Urgente"]
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
    def total_devueltas(self) -> int:
        return sum(1 for item in self.solicitudes if item.devuelto)

    @rx.var
    def solicitudes_filtradas(self) -> List[ProcuraSolicitud]:
        results = self.solicitudes
        if self.search_text:
            query = self.search_text.lower()
            results = [
                item for item in results
                if query in item.material.lower()
                or query in item.solicitante.lower()
                or query in item.departamento.lower()
                or query in item.estado.lower()
            ]

        if self.view_tab == "Pendientes":
            return [item for item in results if not item.revisado]
        if self.view_tab == "Revisadas":
            return [item for item in results if item.revisado and not item.comprado]
        if self.view_tab == "Compradas":
            return [item for item in results if item.comprado and not item.enviado]
        if self.view_tab == "Enviadas":
            return [item for item in results if item.enviado and not item.devuelto]
        if self.view_tab == "Devueltas":
            return [item for item in results if item.devuelto]
        return results

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

    def _record_stock_movement(self, producto_nombre: str, cantidad: int, tipo: str, nota: str):
        with get_session() as session:
            producto = session.exec(select(Producto).where(Producto.nombre == producto_nombre)).first()
            if producto:
                producto.cantidad = max(0, producto.cantidad + cantidad)
                session.add(producto)
                session.commit()
                movimiento = MovimientoStock(
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    fecha=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                    cambio=cantidad,
                    tipo=tipo,
                    nota=nota,
                )
                session.add(movimiento)
                session.commit()

    def _actualizar_estado(self, solicitud_id: int, tipo_accion: str):
        with get_session() as session:
            solicitud = session.get(ProcuraSolicitud, solicitud_id)
            if solicitud:
                if tipo_accion == "Revisada":
                    solicitud.revisado = True
                    solicitud.estado = "Revisada"
                elif tipo_accion == "Comprada":
                    solicitud.comprado = True
                    solicitud.estado = "Comprada"
                elif tipo_accion == "Enviada":
                    solicitud.enviado = True
                    solicitud.estado = "Entregada"
                    if solicitud.cantidad > 0:
                        self._record_stock_movement(solicitud.material, -solicitud.cantidad, "Salida", "Material entregado desde solicitud")
                elif tipo_accion == "Devuelta":
                    solicitud.devuelto = True
                    solicitud.estado = "Devuelta"
                    if solicitud.cantidad > 0:
                        self._record_stock_movement(solicitud.material, solicitud.cantidad, "Retorno", "Material devuelto a inventario")

                session.add(solicitud)
                session.commit()
        return self.load_solicitudes()

    def aprobar_solicitud(self, id: int):
        self._actualizar_estado(id, "Aprobada")

    def rechazar_solicitud(self, id: int, motivo: str):
        self._actualizar_estado(id, "Rechazada")

    def marcar_revisado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Revisada")

    def marcar_comprado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Comprada")

    def marcar_enviado(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Enviada")

    def marcar_devuelto(self, solicitud_id: int):
        self._actualizar_estado(solicitud_id, "Devuelta")
