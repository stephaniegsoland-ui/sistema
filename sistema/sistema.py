import reflex as rx
from .db_init import initialize_database

# 1. Importación de las páginas (vistas completas)
# Al importar estos archivos, se ejecutan los decoradores @rx.page
from .pages.login import login_page
from .pages.dashboard import dashboard_page
from .pages.stock import stock_page
from .pages.epp import epp_page  # Importante para que /epp funcione
from .pages.fleet import fleet_page
from .pages.inspeccion import inspeccion_page
from .pages.reportes import reportes_page
# 2. Inicializar la base de datos al arrancar
try:
    initialize_database()
except Exception as e:
    print(f"Error en initialize_database: {e}")

# 3. Configuración Global de la Aplicación
# Definimos el tema oscuro y el color acentuado (Gold) para todo el sistema
app = rx.App(
    theme=rx.theme(
        appearance="dark", 
        accent_color="gold",
        radius="large",
    )
)

# Registro de páginas
app.add_page(fleet_page, route="/vehiculos")
app.add_page(inspeccion_page, route="/vehiculos/[pid]")

# 4. Registro Centralizado de Rutas
# Aunque uses @rx.page, registrarlas aquí asegura que Reflex las reconozca al compilar
app.add_page(
    login_page, 
    route="/"
)

app.add_page(
    dashboard_page, 
    route="/dashboard"
)

app.add_page(
    stock_page, 
    route="/stock"
)

app.add_page(
    epp_page, 
    route="/epp"
)

app.add_page(
    reportes_page,
    route="/vehiculos/reportes"
)



# Al ejecutar 'reflex run', este archivo orquestará todos los módulos.