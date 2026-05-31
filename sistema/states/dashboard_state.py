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

    @rx.event
    async def start_log_stream(self):
        """Manejador nativo de Reflex usando Yield para mantener el flujo vivo"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        
        event_pool = [
            ("SYS", "Sincronización exitosa con Base de Datos Laravel.", "#10b981"),
            ("AI", "Módulo IA: Procesamiento de análisis de EPP completado.", "#6366f1"),
            ("NET", "Cisco Catalyst 3560: Interface GigabitEthernet0/1 cambiado a UP.", "#eab308"),
            ("SYS", "Usuario admin_soland actualizó permisos de colaborador.", "#3b82f6"),
            ("NET", "Syslog Server: Recibido Keep-Alive de Switch Core.", "#eab308"),
            ("AI", "Google Generative AI: Datos de Procura estructurados con éxito.", "#6366f1"),
            ("SYS", "Cola de Tickets: Ticket TK-2847 pasó a estado [En Proceso].", "#f97316"),
        ]

        # Convertimos el método en un Event Generator infinito
        while self.is_monitoring:
            await asyncio.sleep(random.randint(4, 8))
            
            now = datetime.now().strftime("%H:%M:%S")
            log_type, msg, color = random.choice(event_pool)
            
            new_log = LogEvent(time=now, log_type=log_type, msg=msg, color=color)
            
            # Mutamos el estado directamente (Reflex se encarga del backend-to-frontend por el yield)
            self.syslog_events.insert(0, new_log)
            if len(self.syslog_events) > 4:
                self.syslog_events.pop()
                
            # Emitimos el cambio al frontend inmediatamente
            yield

    @rx.event
    def stop_log_stream(self):
        """Por si necesitas detener el monitoreo de logs desde la UI"""
        self.is_monitoring = False