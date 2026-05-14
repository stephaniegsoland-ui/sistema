import reflex as rx
from typing import List, Dict, Any
import os

# Simulación de un modelo de IA de detección de daños
def simulate_ia_analysis(img_lunes: str, img_viernes: str) -> Dict[str, Any]:
    """Simula el análisis de IA que detecta daños y devuelve coordenadas."""
    return {
        # Imágenes que la IA generaría superponiendo círculos (overlays)
        "overlay_lunes": "/ia_overlay_lunes.png", # Imagen de lunes con círculos
        "overlay_viernes": "/ia_overlay_viernes.png", # Imagen de viernes con círculos
        "diff_images": ["/hilux_antes.png", "/hilux_despues.png"], # Imágenes base
        # Lista detallada de diferencias para el informe
        "analisis_texto": [
            {"id": "A", "tipo": "Daño detectado", "hora": "14/05/2026 12:59", "porcentaje": 0.02, "detalle": "Rayón visible en la puerta del conductor."},
            {"id": "S", "tipo": "Suciedad", "hora": "14/05/2026 12:59", "porcentaje": 0.05, "detalle": "Área con suciedad acumulada."}
        ],
        "estado_final": "Daño Detectado"
    }

class Hallazgo(rx.Base):
    id: str
    tipo: str
    detalle: str
    confianza: str = "N/A"

class InspeccionState(rx.State):
# Atributos que faltaban
    modelo: str = "Cargando..."
    responsable: str = "Sin asignar"
    lista_hallazgos: list[Hallazgo] = []
    # Variables para las imágenes y resultados
    url_lunes: str = "/upload_placeholder_blue.png"
    url_viernes: str = "/upload_placeholder_green.png"
    mostrar_resultado: bool = False
    imagen_overlay_lunes_url: str = ""
    imagen_overlay_viernes_url: str = ""
    analisis_ia_datos: Dict[str, Any] = {"analisis_texto": []}
    analisis_ia_texto: List[Dict[str, Any]] = [] # Añadimos esta línea

  
    async def handle_upload(self, files: List[rx.UploadFile], momento: str):
        for file in files:
            # Ahora 'file' será un objeto rx.UploadFile, no un string
            upload_data = await file.read() 
            
            nombre_archivo = file.filename
            dest_path = os.path.join("assets", nombre_archivo)
            
            with open(dest_path, "wb") as fp:
                fp.write(upload_data)
            
            # Asignamos la URL para la previsualización
            if momento == "lunes":
                self.url_lunes = f"/{nombre_archivo}"
            else:
                self.url_viernes = f"/{nombre_archivo}"

    async def handle_upload_lunes(self, files: List[rx.UploadFile]):
        await self.handle_upload(files, "lunes")

    async def handle_upload_viernes(self, files: List[rx.UploadFile]):
        await self.handle_upload(files, "viernes")
        
    def generar_informe(self):
        self.lista_hallazgos = [
            Hallazgo(id="1", tipo="Carrocería", detalle="Rayón detectado", confianza="95%"),
            Hallazgo(id="2", tipo="Neumáticos", detalle="Desgaste irregular", confianza="88%")
        ]
        self.mostrar_resultado = True