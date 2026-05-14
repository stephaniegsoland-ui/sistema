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

class InspeccionState(rx.State):
# Atributos que faltaban
    modelo: str = "Cargando..."
    responsable: str = "Sin asignar"
    lista_hallazgos: List[Dict[str, str]] = []
    # Variables para las imágenes y resultados
    url_lunes: str = "/upload_placeholder_blue.png"
    url_viernes: str = "/upload_placeholder_green.png"
    mostrar_resultado: bool = False
    imagen_overlay_lunes_url: str = ""
    imagen_overlay_viernes_url: str = ""
    analisis_ia_datos: Dict[str, Any] = {"analisis_texto": []}

  
    async def handle_upload(self, files: List[rx.UploadFile], momento: str):
        if not files:
            return

        file = files[0]
        upload_data = await file.read()

        # Guardamos el archivo en la carpeta de uploads de Reflex
        outfile = rx.get_upload_dir() / file.filename
        with open(outfile, "wb") as fp:
            fp.write(upload_data)

        # Usamos la URL de subida para la previsualización inmediata
        upload_url = rx.get_upload_url(file.filename)

        if momento == "lunes":
            self.url_lunes = upload_url
        else:
            self.url_viernes = upload_url

    async def handle_upload_lunes(self, files: List[rx.UploadFile]):
        await self.handle_upload(files, "lunes")

    async def handle_upload_viernes(self, files: List[rx.UploadFile]):
        await self.handle_upload(files, "viernes")
        
    def generar_informe(self):
        """Simula el proceso de comparación de IA."""
        # Verificamos que ambas imágenes estén cargadas
        if self.url_lunes == "/upload_placeholder_blue.png" or \
           self.url_viernes == "/upload_placeholder_green.png":
            return rx.window_alert("Carga ambas imágenes antes de comparar.")

        # Disparamos la IA
        self.analisis_ia_datos = simulate_ia_analysis(self.url_lunes, self.url_viernes)
        
        # Usamos las imágenes subidas como overlays para mostrarlas
        self.imagen_overlay_lunes_url = self.url_lunes
        self.imagen_overlay_viernes_url = self.url_viernes
        
        # Mostramos el panel de resultados
        self.mostrar_resultado = True