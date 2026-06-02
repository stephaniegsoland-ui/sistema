import os
from sqlmodel import Session, create_engine, select, SQLModel
from sistema.api.models import Usuario

def crear_super_usuario_por_codigo():
    print("🔄 Conectando directamente a la base de datos local (Nativo SQLModel)...")
    
    # 1. Definimos la URL local de manera explícita y aislada de Reflex
    # Usamos 'gestion_db' porque es el nombre del servicio en Docker.
    # Esto permite que el script corra automáticamente dentro del contenedor.
    DATABASE_LOCAL_URL = "mysql+pymysql://root:root_password@gestion_db:3306/sistema_laravel_db"
    
    # 2. Creamos nuestro propio motor de conexión independiente
    engine = create_engine(DATABASE_LOCAL_URL, echo=False)
    
    try:
        # Aseguramos que las tablas existan antes de operar
        SQLModel.metadata.create_all(engine)
        
        # 3. Abrimos la sesión nativa de SQLModel
        with Session(engine) as session:
            # Validamos si ya existe el administrador
            statement = select(Usuario).where(Usuario.nombre_usuario == "admin_soland")
            usuario_existente = session.exec(statement).first()
            
            if usuario_existente:
                print("⚠️ El usuario 'admin_soland' ya existe en la base de datos.")
                return
            
            # Creamos la instancia con el modelo importado
            nuevo_admin = Usuario(
                nombre_usuario="admin_soland",
                password="Soland2026*",
                nivel=1,                   # Nivel Administrador Maestro
                estado="TODOS, all"        # Desbloquea todas las llaves en el sidebar
            )
            
            # Guardamos los cambios de forma limpia
            session.add(nuevo_admin)
            session.commit()
            print("✅ ¡Súper usuario 'admin_soland' creado con éxito y permisos globales asignados!")
            
    except Exception as e:
        print(f"❌ Error al intentar conectar o guardar en la BD: {e}")

if __name__ == "__main__":
    crear_super_usuario_por_codigo()