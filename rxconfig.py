import reflex as rx

config = rx.Config(
    app_name="sistema",
    # Esta línea es la clave:
    api_url="http://localhost:8001", 
    db_url="mysql+pymysql://root:root_password@gestion_db/sistema_laravel_db",
    upload_dest="assets",
)