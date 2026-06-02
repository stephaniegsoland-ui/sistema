# sistema/states/inventory_state.py
import reflex as rx
from typing import Dict, List, Any

class InventoryState(rx.State):
    # Categoría activa en el menú lateral
    current_category: str = "Resumen"
    
    # Campos dinámicos del formulario
    form_data: Dict[str, str] = {}
    
    def set_category(self, category: str):
        self.current_category = category
        # Limpiar el formulario al cambiar de sección
        self.form_data = {}

    def handle_submit(self, form_values: Dict[str, Any]):
        """Recibe los datos del formulario y los procesa para la BD"""
        self.form_data = form_values
        
        # Aquí conectarás con tu BD 'gestion_db' usando tu modelo de SQLAlchemy
        # Ejemplo conceptual:
        # nuevo_item = Producto(nombre=form_values.get("nombre"), categoria=self.current_category, ...)
        
        # Feedback visual de éxito
        return rx.toast.info(
            f"Registrado con éxito en {self.current_category}: {form_values.get('nombre', 'Item')}",
            position="bottom-right"
        )