import reflex as rx
import asyncio
import json
import google.generativeai as genai
from typing import List, Dict, Any

# Configura tu API KEY (Obtenla en Google AI Studio)
genai.configure(api_key="AIzaSyCbkEOepmalLBn_0gXbMc4w4Jp8vkjLf9s")

class EPPState(rx.State):
    image_processing: bool = False
    image_url: str = ""
    analysis_status: str = "Esperando imagen..."
    analysis_checks: List[Dict[str, Any]] = []

    async def handle_upload(self, files: List[rx.UploadFile]):
        if not files:
            return
        
        self.image_processing = True
        self.analysis_status = "Analizando con IA..."
        yield

        try:
            # 1. Guardar archivo para vista previa
            file = files[0]
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with open(outfile, "wb") as f:
                f.write(upload_data)
            
            self.image_url = rx.get_upload_url(file.filename)

            # 2. IA Vision (Gemini)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = """
            Analiza EPP: Casco, Chaleco, Guantes, Botas, Mascarilla.
            Responde SOLO en JSON:
            {
              "status": "APROBADO" o "DENEGADO",
              "checks": [{"item": "Nombre", "status": true/false, "desc": "detalle"}]
            }
            """
            
            response = model.generate_content([
                prompt, 
                {'mime_type': 'image/jpeg', 'data': upload_data}
            ])
            
            data = json.loads(response.text)
            
            self.analysis_status = data.get("status", "COMPLETADO")
            self.analysis_checks = data.get("checks", [])

        except Exception as e:
            self.analysis_status = "ERROR DE SISTEMA"
            self.analysis_checks = [{"item": "Error", "status": False, "desc": str(e)}]
        
        self.image_processing = False

    def save_record(self):
        # Lógica para persistir en tu DB de MySQL
        return rx.window_alert(f"Registro de {self.analysis_status} guardado en SQL.")