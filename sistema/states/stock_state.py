import reflex as rx
from typing import List, Dict, Any
import pandas as pd
from ..api.models import Producto

class StockItem(rx.Base):
    id: int = 0
    prod: str = ""
    cat: str = ""
    stock: int = 0
    status: str = "Active"
    nombre: str = ""      # Ensure these extra fields are also defined
    detalle: str = ""
    cantidad: int = 0

import reflex as rx
from typing import List, Dict

class StockItem(rx.Base):
    id: int = 0
    nombre: str = ""
    detalle: str = ""
    cantidad: int = 0
    cat: str = ""

class StockState(rx.State):
    # Variables de estado únicas
    search_text: str = ""
    filter_active: str = "Todos"
    view: str = "Resumen"
    
    # Inventario central (inicializado como lista vacía, no con elipsis)
    inventory: Dict[str, List[StockItem]] = {
        "Herramientas": [StockItem(id=1, nombre="Martillo", detalle="Carpintería", cantidad=140)],
        "Botas": [StockItem(id=2, nombre="Bota PVC", detalle="Talla 42", cantidad=87)],
    }

    @rx.var
    def filtered_stock(self) -> List[StockItem]:
        items = self.inventory.get(self.view, [])
        if self.search_text:
            items = [i for i in items if self.search_text.lower() in i.nombre.lower()]
        return items

    @rx.event
    def set_filter(self, filter_name: str):
        self.filter_active = filter_name

    @rx.event
    def set_search(self, value: str):
        self.search_text = value

    @rx.event
    def set_view(self, new_view: str):
        self.view = new_view