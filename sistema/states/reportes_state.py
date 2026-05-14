import datetime
import json
from typing import Any, Dict, List, Optional

import pandas as pd
import reflex as rx
from sqlmodel import select

from ..api.models import InspeccionReporte
from ..db_init import get_session


class ReportesState(rx.State):
    reportes: List[Dict[str, Any]] = []
    view_tab: str = "Resumen"
    search_text: str = ""
    filter_placa: str = ""
    filter_modelo: str = ""
    filter_responsable: str = ""
    filter_estado: str = ""
    fecha_desde: str = ""
    fecha_hasta: str = ""
    selected_report_id: Optional[int] = None

    # --- VARIABLES COMPUTADAS (@rx.var) ---
    
    @rx.var
    def tiene_reportes(self) -> bool:
        return bool(self.reportes)

    @rx.var
    def recientes(self) -> List[Dict[str, Any]]:
        """Retorna los últimos 5 reportes para la vista rápida."""
        return self.reportes[:5]

    @rx.var
    def selected_report(self) -> Dict[str, Any]:
        if self.selected_report_id is None:
            return {}
        return next((r for r in self.reportes if r["id"] == self.selected_report_id), {})

    @rx.var
    def reportes_filtrados(self) -> List[Dict[str, Any]]:
        filtered = self.reportes

        if self.search_text:
            query = self.search_text.lower()
            filtered = [
                r
                for r in filtered
                if query in r["placa"].lower()
                or query in r["modelo"].lower()
                or query in r["responsable"].lower()
                or query in r["estado_final"].lower()
                or query in r["hallazgos_text"].lower()
            ]

        if self.filter_placa:
            filtered = [
                r for r in filtered if self.filter_placa.lower() in r["placa"].lower()
            ]
        if self.filter_modelo:
            filtered = [
                r for r in filtered if self.filter_modelo.lower() in r["modelo"].lower()
            ]
        if self.filter_responsable:
            filtered = [
                r for r in filtered if self.filter_responsable.lower() in r["responsable"].lower()
            ]
        if self.filter_estado:
            filtered = [
                r for r in filtered if r["estado_final"] == self.filter_estado
            ]
        if self.fecha_desde:
            filtered = [
                r for r in filtered if r["fecha"][:10] >= self.fecha_desde
            ]
        if self.fecha_hasta:
            filtered = [
                r for r in filtered if r["fecha"][:10] <= self.fecha_hasta
            ]

        return filtered

    @rx.var
    def total_reportes(self) -> int:
        return len(self.reportes)

    @rx.var
    def total_con_dano(self) -> int:
        return len([r for r in self.reportes if r["estado_final"] != "SIN DAÑOS"])

    @rx.var
    def total_sin_dano(self) -> int:
        return len([r for r in self.reportes if r["estado_final"] == "SIN DAÑOS"])

    @rx.var
    def hallazgos_top(self) -> List[Dict[str, Any]]:
        totals: Dict[str, int] = {}
        for reporte in self.reportes:
            for hallazgo in reporte.get("hallazgos", []):
                tipo = hallazgo.get("tipo", "Desconocido")
                totals[tipo] = totals.get(tipo, 0) + 1
        return sorted(
            [{"tipo": tipo, "count": count} for tipo, count in totals.items()],
            key=lambda item: item["count"],
            reverse=True,
        )[:6]

    @rx.var
    def hallazgos_top_text(self) -> str:
        if not self.hallazgos_top:
            return "Sin hallazgos frecuentes."
        return "\n".join(
            f"{item.get('tipo', 'Desconocido')}: {item.get('count', 0)}"
            for item in self.hallazgos_top
        )

    # --- MÉTODOS DE ACCIÓN ---

    def set_tab(self, tab: str | list[str]): # Cambia 'str' por 'str | list[str]'
            # Como segmented_control solo devuelve un string en tu caso, 
            # nos aseguramos de guardar solo el string
            if isinstance(tab, list):
                self.view_tab = tab[0] if tab else "Resumen"
            else:
                self.view_tab = tab
            
            self.selected_report_id = None

    def select_report(self, report_id: int):
        self.selected_report_id = report_id

    def clear_selected_report(self):
        self.selected_report_id = None

    def apply_filters(self, form_data: Dict[str, Any]):
        self.search_text = form_data.get("search_text", "") or ""
        self.filter_placa = form_data.get("placa", "") or ""
        self.filter_modelo = form_data.get("modelo", "") or ""
        self.filter_responsable = form_data.get("responsable", "") or ""
        self.filter_estado = form_data.get("filter_estado", "") or ""
        self.fecha_desde = form_data.get("fecha_desde", "") or ""
        self.fecha_hasta = form_data.get("fecha_hasta", "") or ""
        self.selected_report_id = None

    def reset_filters(self):
        self.search_text = ""
        self.filter_placa = ""
        self.filter_modelo = ""
        self.filter_responsable = ""
        self.filter_estado = ""
        self.fecha_desde = ""
        self.fecha_hasta = ""
        self.selected_report_id = None

    def load_reportes(self):
        try:
            with get_session() as session:
                registros = session.exec(
                    select(InspeccionReporte).order_by(InspeccionReporte.id.desc())
                ).all()

            self.reportes = [
                {
                    "id": reporte.id,
                    "placa": reporte.placa,
                    "modelo": reporte.modelo,
                    "responsable": reporte.responsable,
                    "fecha": reporte.fecha,
                    "estado_final": reporte.estado_final,
                    "recomendacion": reporte.recomendacion,
                    "url_lunes": reporte.url_lunes,
                    "url_viernes": reporte.url_viernes,
                    "hallazgos": json.loads(reporte.hallazgos_json or "[]"),
                    "damage_map_lunes": json.loads(reporte.damage_map_lunes_json or "[]"),
                    "damage_map_viernes": json.loads(reporte.damage_map_viernes_json or "[]"),
                    "hallazgos_text": "\n".join(
                        f"{item.get('tipo', 'Hallazgo')}: {item.get('detalle', '')}"
                        for item in json.loads(reporte.hallazgos_json or "[]")
                    ),
                }
                for reporte in registros
            ]

            if not self.reportes:
                return rx.window_alert("No hay reportes guardados.")
        except Exception as exc:
            self.reportes = []
            return rx.window_alert(f"Error cargando reportes: {exc}")

    def export_to_excel(self):
        if not self.reportes_filtrados:
            return rx.window_alert("No hay reportes para exportar.")

        df = pd.DataFrame(
            [
                {
                    "ID": reporte["id"],
                    "Placa": reporte["placa"],
                    "Modelo": reporte["modelo"],
                    "Responsable": reporte["responsable"],
                    "Fecha": reporte["fecha"],
                    "Estado Final": reporte["estado_final"],
                    "Recomendación": reporte["recomendacion"],
                    "Hallazgos": reporte["hallazgos_text"],
                }
                for reporte in self.reportes_filtrados
            ]
        )
        filename = f"reportes_historial_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = rx.get_asset_path(filename)
        df.to_excel(file_path, index=False)
        return rx.download(url=f"/{filename}")

    def export_to_csv(self):
        if not self.reportes_filtrados:
            return rx.window_alert("No hay reportes para exportar.")

        df = pd.DataFrame(
            [
                {
                    "ID": reporte["id"],
                    "Placa": reporte["placa"],
                    "Modelo": reporte["modelo"],
                    "Responsable": reporte["responsable"],
                    "Fecha": reporte["fecha"],
                    "Estado Final": reporte["estado_final"],
                    "Recomendación": reporte["recomendacion"],
                    "Hallazgos": reporte["hallazgos_text"],
                }
                for reporte in self.reportes_filtrados
            ]
        )
        filename = f"reportes_historial_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = rx.get_asset_path(filename)
        df.to_csv(file_path, index=False)
        return rx.download(url=f"/{filename}")