import reflex as rx

config = rx.Config(
    app_name="sistema",
    api_url="http://localhost:8001", 
    # CAMBIO: El final de la URL debe ser el nombre de la DB, no el del servicio
    # Cambia localhost por gestion_db
    DATABASE_URL = "mysql+pymysql://root:root@gestion_db:3306/sistema_laravel_db",
    upload_dest="assets",
)