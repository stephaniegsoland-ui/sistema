import reflex as rx
from typing import List, Dict, Optional
from datetime import datetime
from sqlmodel import select
from ..db_init import get_session
from ..api.models import Producto, MovimientoStock

class StockState(rx.State):
    search_text: str = ""
    filter_category: str = "Todos"
    view: str = "Resumen"
    selected_product_id: Optional[int] = None

    input_nombre_producto: str = ""
    input_categoria_producto: str = ""
    input_cantidad_producto: str = "0"
    input_ajuste_cantidad: str = "0"
    input_ajuste_nota: str = ""

    products: List[Dict] = []
    movements: List[Dict] = []
    stock_threshold: int = 10

    default_material_types: List[str] = [
        "Herramientas",
        "Botas",
        "Bragas",
        "Suministros",
        "Lentes",
        "Equipos",
        "Otros",
    ]

    @rx.var
    def material_type_suggestions(self) -> List[str]:
        return self.default_material_types

    @rx.var
    def filtered_products(self) -> List[Dict]:
        items = self.products
        if self.view not in ("Resumen", "Todos"):
            items = [item for item in items if item["categoria"] == self.view]
        if self.filter_category != "Todos":
            items = [item for item in items if item["categoria"] == self.filter_category]
        if self.search_text:
            items = [item for item in items if self.search_text.lower() in item["nombre"].lower()]
        return items

    @rx.var
    def product_categories(self) -> List[str]:
        categories = sorted({item["categoria"] for item in self.products if item.get("categoria")})
        return ["Todos"] + categories

    @rx.var
    def selected_product(self) -> Optional[Dict]:
        if self.selected_product_id is None:
            return None
        return next((item for item in self.products if item["id"] == self.selected_product_id), None)

    @rx.var
    def selected_product_name(self) -> str:
        return self.selected_product["nombre"] if self.selected_product else "Ninguno"

    @rx.var
    def total_stock(self) -> int:
        return sum(item["cantidad"] for item in self.products)

    @rx.var
    def total_products(self) -> int:
        return len(self.products)

    @rx.var
    def total_categories(self) -> int:
        return len({item["categoria"] for item in self.products if item.get("categoria")})

    @rx.var
    def low_stock_count(self) -> int:
        return len([item for item in self.products if item["cantidad"] <= self.stock_threshold])

    @rx.var
    def low_stock_items(self) -> List[Dict]:
        return [item for item in self.products if item["cantidad"] <= self.stock_threshold]

    @rx.var
    def category_summary(self) -> List[Dict]:
        summary: Dict[str, int] = {}
        for item in self.products:
            summary[item["categoria"]] = summary.get(item["categoria"], 0) + item["cantidad"]
        return [{"categoria": cat, "cantidad": qty} for cat, qty in summary.items()]

    @rx.var
    def top_products(self) -> List[Dict]:
        return sorted(self.products, key=lambda item: item["cantidad"], reverse=True)[:6]

    @rx.var
    def recent_movements(self) -> List[Dict]:
        return self.movements[:8]

    @rx.var
    def selected_movements(self) -> List[Dict]:
        if self.selected_product_id is None:
            return self.movements[:8]
        return [movement for movement in self.movements if movement["producto_id"] == self.selected_product_id][:8]

    @rx.var
    def movement_trend(self) -> List[Dict]:
        trend: Dict[str, int] = {}
        for movement in reversed(self.movements[-12:]):
            fecha = movement["fecha"].split(" ")[0]
            trend[fecha] = trend.get(fecha, 0) + abs(movement["cambio"])
        return [{"fecha": fecha, "cantidad": cantidad} for fecha, cantidad in sorted(trend.items())]

    @rx.var
    def movement_type_summary(self) -> List[Dict]:
        summary: Dict[str, int] = {}
        for movement in self.movements:
            summary[movement["tipo"]] = summary.get(movement["tipo"], 0) + abs(movement["cambio"])
        return [{"tipo": tipo, "cantidad": cantidad} for tipo, cantidad in summary.items()]

    @rx.event
    def load_products(self):
        with get_session() as session:
            query = select(Producto).order_by(Producto.nombre)
            productos = session.exec(query).all()
            self.products = [product.dict() for product in productos]
        self.load_movements()

    @rx.event
    def load_movements(self):
        with get_session() as session:
            query = select(MovimientoStock).order_by(MovimientoStock.id.desc()).limit(50)
            movimientos = session.exec(query).all()
            self.movements = [movement.dict() for movement in movimientos]

    @rx.event
    def set_search(self, value: str):
        self.search_text = value

    @rx.event
    def set_category(self, category: str):
        self.filter_category = category

    @rx.event
    def set_input_nombre_producto(self, value: str):
        self.input_nombre_producto = value

    @rx.event
    def set_input_categoria_producto(self, value: str):
        self.input_categoria_producto = value

    @rx.event
    def set_input_cantidad_producto(self, value: str):
        self.input_cantidad_producto = value

    @rx.event
    def set_input_ajuste_cantidad(self, value: str):
        self.input_ajuste_cantidad = value

    @rx.event
    def set_input_ajuste_nota(self, value: str):
        self.input_ajuste_nota = value

    @rx.event
    def set_filter(self, category: str):
        self.set_category(category)

    @rx.event
    def set_view(self, new_view: str):
        self.view = new_view
        self.filter_category = "Todos" if new_view in ("Resumen", "Todos") else new_view
        self.selected_product_id = None
        if new_view in ("Resumen", "Todos"):
            self.input_categoria_producto = ""
        else:
            self.input_categoria_producto = new_view

    @rx.event
    def select_product(self, product_id: int):
        self.selected_product_id = product_id
        product = next((item for item in self.products if item["id"] == product_id), None)
        if not product:
            return
        self.input_nombre_producto = product["nombre"]
        self.input_categoria_producto = product.get("categoria", "")
        self.input_cantidad_producto = str(product.get("cantidad", 0))
        self.input_ajuste_cantidad = "0"
        self.input_ajuste_nota = ""

    def _record_movement(self, producto_id: int, cambio: int, tipo: str, nota: str = ""):
        with get_session() as session:
            producto = session.get(Producto, producto_id)
            if not producto:
                return
            movimiento = MovimientoStock(
                producto_id=producto_id,
                producto_nombre=producto.nombre,
                fecha=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                cambio=cambio,
                tipo=tipo,
                nota=nota,
            )
            session.add(movimiento)
            session.commit()
        self.load_movements()

    def _clear_product_inputs(self):
        self.input_nombre_producto = ""
        self.input_categoria_producto = ""
        self.input_cantidad_producto = "0"

    @rx.event
    def add_or_update_product(self):
        nombre = self.input_nombre_producto.strip()
        categoria = self.input_categoria_producto.strip() or "General"
        try:
            cantidad = int(self.input_cantidad_producto)
        except ValueError:
            return rx.window_alert("Cantidad inválida")

        if not nombre:
            return rx.window_alert("El nombre del producto es obligatorio")
        if cantidad <= 0:
            return rx.window_alert("La cantidad debe ser mayor a cero")

        with get_session() as session:
            producto = session.exec(select(Producto).where(Producto.nombre == nombre)).first()
            if producto:
                producto.cantidad += cantidad
                producto.categoria = categoria
                session.add(producto)
                session.commit()
                self._record_movement(producto.id, cantidad, "Ingreso", "Actualización de stock")
                message = "Stock del producto actualizado"
            else:
                producto = Producto(nombre=nombre, cantidad=cantidad, categoria=categoria)
                session.add(producto)
                session.commit()
                session.refresh(producto)
                self._record_movement(producto.id, cantidad, "Ingreso", "Producto registrado")
                message = "Producto creado y stock cargado"

        self.load_products()
        self.selected_product_id = producto.id
        self._clear_product_inputs()
        return rx.window_alert(message)

    @rx.event
    def adjust_stock(self):
        if self.selected_product_id is None:
            return rx.window_alert("Selecciona un producto primero")

        try:
            delta = int(self.input_ajuste_cantidad)
        except ValueError:
            return rx.window_alert("Cantidad inválida")

        if delta == 0:
            return rx.window_alert("Ingresa una cantidad diferente de cero")

        nota = self.input_ajuste_nota.strip() or "Ajuste manual"
        with get_session() as session:
            producto = session.get(Producto, self.selected_product_id)
            if not producto:
                return rx.window_alert("Producto no encontrado")
            producto.cantidad = max(0, producto.cantidad + delta)
            session.add(producto)
            session.commit()
            self._record_movement(producto.id, delta, "Ingreso" if delta > 0 else "Egreso", nota)

        self.load_products()
        self.input_ajuste_cantidad = "0"
        self.input_ajuste_nota = ""
        return rx.window_alert("Stock ajustado correctamente")

    @rx.event
    def change_selected_stock(self, delta: int):
        if self.selected_product_id is None:
            return
        with get_session() as session:
            producto = session.get(Producto, self.selected_product_id)
            if not producto:
                return
            producto.cantidad = max(0, producto.cantidad + delta)
            session.add(producto)
            session.commit()
            self._record_movement(producto.id, delta, "Ingreso" if delta > 0 else "Egreso", "Ajuste rápido")

        self.load_products()
