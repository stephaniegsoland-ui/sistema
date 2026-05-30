# --- sistema/states/dashboard_state.py ---
import reflex as rx
import asyncio
from datetime import datetime
import random

class LogEvent(rx.Base):
    time: str
    log_type: str
    msg: str
    color: str

class DashboardState(rx.State):
    syslog_events: list[LogEvent] = [
        LogEvent(time="10:35:40", log_type="SYS", msg="Sistema Soland inicializado correctamente.", color="#10b981")
    ]
    is_monitoring: bool = False

    async def start_log_stream(self):
        """Manejador inicial que levanta de forma segura el bucle asíncrono"""
        if self.is_monitoring:
            return
        self.is_monitoring = True
        
        # Disparamos el bucle infinito sin bloquear la renderización de la página
        asyncio.create_task(self.run_logger_loop())

    async def run_logger_loop(self):
        """Bucle en segundo plano puro usando asyncio estándar"""
        event_pool = [
            ("SYS", "Sincronización exitosa con Base de Datos Laravel.", "#10b981"),
            ("AI", "Módulo IA: Procesamiento de análisis de EPP completado.", "#6366f1"),
            ("NET", "Cisco Catalyst 3560: Interface GigabitEthernet0/1 cambiado a UP.", "#eab308"),
            ("SYS", "Usuario admin_soland actualizó permisos de colaborador.", "#3b82f6"),
            ("NET", "Syslog Server: Recibido Keep-Alive de Switch Core.", "#eab308"),
            ("AI", "Google Generative AI: Datos de Procura estructurados con éxito.", "#6366f1"),
            ("SYS", "Cola de Tickets: Ticket TK-2847 pasó a estado [En Proceso].", "#f97316"),
        ]

        while True:
            await asyncio.sleep(random.randint(4, 8))
            now = datetime.now().strftime("%H:%M:%S")
            log_type, msg, color = random.choice(event_pool)
            
            # Para mutar el estado de Reflex desde una tarea en segundo plano de forma segura,
            # usamos el contexto modificado del state si tu versión lo requiere, o asignación directa:
            async with self:
                new_log = LogEvent(time=now, log_type=log_type, msg=msg, color=color)
                self.syslog_events.insert(0, new_log)
                if len(self.syslog_events) > 4:
                    self.syslog_events.pop()