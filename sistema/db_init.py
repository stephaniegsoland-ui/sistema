import os
from sqlmodel import SQLModel, create_engine, select, Session
from .api.models import Usuario, Producto


def get_db_url() -> str:
    return os.getenv("DB_URL", "sqlite:///sistema.db")


def create_db_engine():
    db_url = get_db_url()
    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(db_url, echo=False, connect_args=connect_args)


engine = create_db_engine()


def get_session() -> Session:
    return Session(engine)


def initialize_database() -> None:
    # Crear tablas para todos los modelos registrados
    SQLModel.metadata.create_all(engine)

    with get_session() as session:
        # Datos iniciales de usuarios
        if session.exec(select(Usuario)).first() is None:
            admin = Usuario(
                nombre_usuario="admin",
                password="admin123",
                nivel=1,
                estado="activo",
            )
            supervisor = Usuario(
                nombre_usuario="supervisor",
                password="supervisor123",
                nivel=2,
                estado="activo",
            )
            usuario = Usuario(
                nombre_usuario="usuario",
                password="usuario123",
                nivel=3,
                estado="activo",
            )
            session.add_all([admin, supervisor, usuario])

        # Datos iniciales de productos
        if session.exec(select(Producto)).first() is None:
            productos = [
                Producto(nombre="Laptop", cantidad=15, categoria="Almacén Central"),
                Producto(nombre="Mouse", cantidad=50, categoria="Logística"),
                Producto(nombre="Teclado", cantidad=30, categoria="Almacén Central"),
                Producto(nombre="Monitor", cantidad=12, categoria="Oficina"),
                Producto(nombre="Impresora", cantidad=8, categoria="Oficina"),
            ]
            session.add_all(productos)

        session.commit()
