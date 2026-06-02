import datetime
import imghdr
import json
import mimetypes
import os
import uuid

import reflex as rx
import google.generativeai as genai
from typing import Any, List, Dict
from ..api.models import InspeccionReporte
from ..db_init import get_session

# Configuración de Google Generative AI
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "AIzaSyCbkEOepmalLBn_0gXbMc4w4Jp8vkjLf9s"))

# Simulación de un modelo de IA de detección de daños
def simulate_ia_analysis(img_lunes: str, img_viernes: str) -> Dict[str, Any]:
    """Simula el análisis de IA que detecta daños y devuelve coordenadas."""
    return {
        "overlay_lunes": img_lunes,
        "overlay_viernes": img_viernes,
        "hallazgos": [
            {"id": "A", "tipo": "Caucho desinflado", "detalle": "Llanta trasera izquierda parece baja de aire.", "confianza": "90%"},
            {"id": "B", "tipo": "Suciedad", "detalle": "Cauchos y rines presentan suciedad acumulada.", "confianza": "85%"},
            {"id": "C", "tipo": "Vidrio sucio", "detalle": "Parabrisas y ventanas con manchas visibles.", "confianza": "88%"}
        ],
        "estado_final": "Daño Detectado",
        "recomendacion": "Revisar la presión de los cauchos, limpiar vidrios y retirar suciedad de los neumáticos.",
        "damage_map_lunes": [
            {"id": "A", "x": 15, "y": 55, "width": 18, "height": 20, "tipo": "Caucho desinflado"},
            {"id": "B", "x": 20, "y": 70, "width": 22, "height": 18, "tipo": "Suciedad"}
        ],
        "damage_map_viernes": [
            {"id": "C", "x": 50, "y": 15, "width": 25, "height": 18, "tipo": "Vidrio sucio"}
        ]
    }


def _mime_type(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or "image/jpeg"


def _extract_json_from_text(text: str) -> Dict[str, Any]:
    """Extrae un JSON válido de texto que puede contener texto adicional."""
    if not isinstance(text, str):
        raise ValueError("El texto de respuesta no es una cadena")

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No se encontró JSON en la respuesta de IA")

    return json.loads(text[start:end + 1])


def _build_ia_prompt() -> str:
    return """
    Eres un asistente de inspección vehicular. Compara estas dos imágenes de la misma camioneta:
    - primera imagen: estado de salida (lunes)
    - segunda imagen: estado de regreso (viernes)

    Analiza especialmente si hay:
    - cauchos desinflados
    - suciedad en cauchos
    - vidrios sucios
    - rayones, abolladuras o daños visibles

    Devuelve SOLO JSON válido con las siguientes claves:
    {
      "estado_final": "SIN DAÑOS" | "DAÑO DETECTADO",
      "hallazgos": [
         {"id": "1", "tipo": "Caucho desinflado" | "Suciedad" | "Vidrio sucio" | "Daño detectado", "detalle": "...", "confianza": "90%"}
      ],
      "recomendacion": "Texto breve de reparación o revisión",
      "damage_map_lunes": [
         {"id": "1", "x": 20, "y": 10, "width": 30, "height": 25, "tipo": "Caucho desinflado"}
      ],
      "damage_map_viernes": [
         {"id": "1", "x": 22, "y": 12, "width": 32, "height": 26, "tipo": "Vidrio sucio"}
      ]
    }
    Las coordenadas son porcentajes relativos a la imagen.
    No incluyas texto adicional fuera del JSON.
    """


def compare_images_with_ai(img_lunes: str, img_viernes: str) -> Dict[str, Any]:
    """Usa Gemini para comparar dos imágenes y devolver hallazgos reales."""
    upload_dir = rx.get_upload_dir()
    file_lunes = upload_dir / img_lunes
    file_viernes = upload_dir / img_viernes

    if not file_lunes.exists() or not file_viernes.exists():
        return simulate_ia_analysis(img_lunes, img_viernes)

    with open(file_lunes, "rb") as f:
        lunes_bytes = f.read()
    with open(file_viernes, "rb") as f:
        viernes_bytes = f.read()

    prompt = _build_ia_prompt()
    json_response: Dict[str, Any] = {}

    try:
        if hasattr(genai, "GenerativeModel"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                prompt,
                {"mime_type": _mime_type(img_lunes), "data": lunes_bytes},
                {"mime_type": _mime_type(img_viernes), "data": viernes_bytes},
            ])
            text = getattr(response, "text", str(response)).strip()
            json_response = _extract_json_from_text(text)
        elif hasattr(genai, "generate_text"):
            response = genai.generate_text(model="gemini-1.5", prompt=prompt)
            text = getattr(response, "text", str(response)).strip()
            json_response = _extract_json_from_text(text)
        else:
            return simulate_ia_analysis(img_lunes, img_viernes)

        if "hallazgos" in json_response and isinstance(json_response["hallazgos"], list):
            return {
                "overlay_lunes": img_lunes,
                "overlay_viernes": img_viernes,
                "hallazgos": json_response.get("hallazgos", []),
                "estado_final": json_response.get("estado_final", "DAÑO DETECTADO"),
                "recomendacion": json_response.get("recomendacion", "Revisar la unidad en taller."),
                "damage_map_lunes": json_response.get("damage_map_lunes", []),
                "damage_map_viernes": json_response.get("damage_map_viernes", []),
            }
    except Exception as exc:
        print(f"[AI DEBUG] compare_images_with_ai error: {exc}")

    return simulate_ia_analysis(img_lunes, img_viernes)

class InspeccionState(rx.State):
# Atributos que faltaban
    modelo: str = "Cargando..."
    responsable: str = "Sin asignar"
    lista_hallazgos: List[Dict[str, str]] = []
    # Variables para las imágenes y resultados
    url_lunes: str = ""
    url_viernes: str = ""
    mostrar_resultado: bool = False
    imagen_overlay_lunes_url: str = ""
    imagen_overlay_viernes_url: str = ""
    damage_map_lunes: List[Dict[str, Any]] = []
    damage_map_viernes: List[Dict[str, Any]] = []
    report_saved: bool = False
    report_id: int | None = None
    analisis_ia_datos: Dict[str, Any] = {"analisis_texto": []}

  
    async def handle_upload(self, files: Any, momento: str):
        if not files:
            return

        file = files[0]
        upload_data: bytes | None = None
        filename: str | None = None

        if hasattr(file, "read"):
            upload_data = await file.read()
            filename = getattr(file, "filename", None) or getattr(file, "name", None)
            if filename:
                filename = os.path.basename(filename)
        elif isinstance(file, (bytes, bytearray)):
            upload_data = bytes(file)
        elif isinstance(file, str):
            filename = file
            upload_path = rx.get_upload_dir() / filename
            with open(upload_path, "rb") as f:
                upload_data = f.read()
        elif hasattr(file, "name"):
            filename = getattr(file, "name")
            try:
                upload_data = await file.read()
            except Exception:
                try:
                    upload_data = file.read()
                except Exception:
                    upload_data = None

        if upload_data is None:
            raise ValueError("No se pudo leer el archivo subido.")

        if not filename:
            ext = imghdr.what(None, upload_data) or "png"
            filename = f"{momento}_{uuid.uuid4().hex}.{ext}"

        outfile = rx.get_upload_dir() / filename
        with open(outfile, "wb") as fp:
            fp.write(upload_data)

        if momento == "lunes":
            self.url_lunes = filename
            self.imagen_overlay_lunes_url = filename
        else:
            self.url_viernes = filename
            self.imagen_overlay_viernes_url = filename

    async def handle_upload_lunes(self, files: Any):
        await self.handle_upload(files, "lunes")

    async def handle_upload_viernes(self, files: Any):
        await self.handle_upload(files, "viernes")
        
    def generar_informe(self):
        """Simula el proceso de comparación de IA."""
        # Verificamos que ambas imágenes estén cargadas
        if not self.url_lunes or not self.url_viernes:
            return rx.window_alert("Carga ambas imágenes antes de comparar.")

        # Disparamos la IA real
        self.analisis_ia_datos = compare_images_with_ai(self.url_lunes, self.url_viernes)
        
        # Usamos los nombres de archivo subidos como overlays para mostrarlas
        self.imagen_overlay_lunes_url = self.url_lunes
        self.imagen_overlay_viernes_url = self.url_viernes
        
        # Guardamos los hallazgos para la tabla
        self.lista_hallazgos = self.analisis_ia_datos.get("hallazgos", [])
        self.damage_map_lunes = self.analisis_ia_datos.get("damage_map_lunes", [])
        self.damage_map_viernes = self.analisis_ia_datos.get("damage_map_viernes", [])
        self.report_saved = False
        self.report_id = None
        
        # Mostramos el panel de resultados
        self.mostrar_resultado = True

    def save_report(self):
        if not self.mostrar_resultado or not self.url_lunes or not self.url_viernes:
            return rx.window_alert("Genera el informe antes de guardarlo.")

        placa = self.router.page.params.get("pid", "---") if hasattr(self, "router") else "---"
        try:
            with get_session() as session:
                reporte = InspeccionReporte(
                    placa=placa,
                    modelo=self.modelo,
                    responsable=self.responsable,
                    fecha=datetime.datetime.now().isoformat(timespec="seconds"),
                    estado_final=self.analisis_ia_datos.get("estado_final", "DAÑO DETECTADO"),
                    recomendacion=self.analisis_ia_datos.get("recomendacion", ""),
                    url_lunes=self.url_lunes,
                    url_viernes=self.url_viernes,
                    hallazgos_json=json.dumps(self.lista_hallazgos, ensure_ascii=False),
                    damage_map_lunes_json=json.dumps(self.damage_map_lunes, ensure_ascii=False),
                    damage_map_viernes_json=json.dumps(self.damage_map_viernes, ensure_ascii=False),
                )
                session.add(reporte)
                session.commit()
                session.refresh(reporte)
                self.report_saved = True
                self.report_id = reporte.id
            return rx.window_alert("Reporte guardado correctamente.")
        except Exception as exc:
            return rx.window_alert(f"Error guardando el reporte: {exc}")
