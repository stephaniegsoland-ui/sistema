import reflex as rx
from typing import List, Dict, Any
import pandas as pd
from ..api.models import Producto

class StockItem(rx.Base):
    nombre: str
    detalle: str
    cantidad: int

class StockState(rx.State):

    productos: List[Dict[str, Any]] = []

    def on_load(self):
        # Aquí cargarías los datos de la DB
        self.productos = [
            {"nombre": "Casco", "cantidad": 50},
            {"nombre": "Guantes", "cantidad": 120}
        ]

    view: str = "Resumen"
    
    # Datos iniciales para las tablas (Frontend)
    inventory: Dict[str, List[StockItem]] = {
        "Herramientas": [StockItem(nombre="Martillo", detalle="Carpintería", cantidad=140)],
        "Botas": [StockItem(nombre="Bota PVC", detalle="Talla 42", cantidad=87)],
        "Bragas": [StockItem(nombre="Braga Ignífuga", detalle="Talla L", cantidad=98)],
        "Equipos": [StockItem(nombre="Laptop Dell", detalle="IT", cantidad=5)],
        "Suministros": [StockItem(nombre="Mascarillas N95", detalle="EPP", cantidad=555)],
        "Lentes": [StockItem(nombre="Lentes Seguridad", detalle="Claros", cantidad=115)],
    }

    @rx.var
    def chart_data_items(self) -> List[Dict]:
        """Calcula datos dinámicos para los gráficos."""
        # Puedes retornar datos estáticos o mapear tu inventory
        return [
            {"name": "Martillo", "cantidad": 40},
            {"name": "Alicate", "cantidad": 60},
            {"name": "Sierra", "cantidad": 30},
            {"name": "Máscaras", "cantidad": 180},
            {"name": "Baterías", "cantidad": 150},
            {"name": "Escritorio", "cantidad": 45},
        ]

    @rx.var
    def chart_data_areas(self) -> List[Dict]:
        """Agregamos esta var para evitar el AttributeError que tenías antes."""
        return [
            {"name": cat, "cantidad": sum(i.cantidad for i in items)}
            for cat, items in self.inventory.items()
        ]

    def set_view(self, new_view: str):
        self.view = new_view

    def add_item(self, form_data: Dict):
        """Agrega un item al diccionario local del inventario."""
        if not form_data.get("nombre"): 
            return rx.window_alert("Nombre requerido")
        
        new_entry = StockItem(
            nombre=form_data["nombre"],
            detalle=form_data.get("detalle", ""),
            cantidad=int(form_data["cantidad"]) if form_data.get("cantidad") else 0
        )
        
        # Verificamos que la categoría exista en el diccionario
        if self.view in self.inventory:
            self.inventory[self.view].append(new_entry)
        
        return [
            rx.set_value("nombre", ""), 
            rx.set_value("detalle", ""), 
            rx.set_value("cantidad", "")
        ]

    def export_to_excel(self):
        """Exporta la vista actual a Excel en la carpeta assets."""
        if self.view not in self.inventory:
            return rx.window_alert("No hay datos para exportar")

        df_data = [
            {"Nombre": i.nombre, "Detalle": i.detalle, "Cantidad": i.cantidad} 
            for i in self.inventory[self.view]
        ]
        df = pd.DataFrame(df_data)
        
        # Nombre del archivo basado en la vista actual
        filename = f"reporte_{self.view.lower()}.xlsx"
        # Ruta física en el contenedor
        file_path = rx.get_asset_path(filename)
        
        df.to_excel(file_path, index=False)
        return rx.download(url=f"/{filename}")
    
    def agregar_al_stock(self, item_name: str):
        """Actualiza la base de datos persistente (gestion_db)."""
        with rx.session() as session:
            producto = session.exec(
                rx.select(Producto).where(Producto.nombre == item_name)
            ).first()
            
            if producto:
                producto.cantidad += 1
                session.add(producto)
                session.commit()
                # Opcional: refrescar también el inventario local si es necesario
        
        # Si tienes una función para traer todo de la DB, llámala aquí
        # return self.get_all_products() 
        pass