import reflex as rx
from typing import List
# Importamos sqlmodel nativo para asegurar compatibilidad con tu modelo
import sqlmodel
from sistema.api.models import Usuario  # Tu modelo real

class SessionState(rx.State):
    """Maneja la sesión real del usuario logueado en SOLAND"""
    usuario_logueado: str = "Invitado"
    nivel_usuario: int = 3  # 1: Admin, 2: Supervisor, 3: Usuario
    autenticado: bool = False

    def login_real(self, username: str, password_input: str):
        """Busca el usuario en tu tabla para autenticar de forma compatible"""
        with rx.session() as session:
            # Sintaxis compatible con SQLModel puro heredado en tu proyecto
            statement = sqlmodel.select(Usuario).where(Usuario.nombre_usuario == username)
            user = session.exec(statement).first()
            
            if user and user.password == password_input:
                if user.estado != "activo":
                    return rx.window_alert("Error: Este usuario se encuentra inactivo.")
                
                self.usuario_logueado = user.nombre_usuario
                self.nivel_usuario = int(user.nivel)
                self.autenticado = True
                return rx.redirect("/personal")
            else:
                return rx.window_alert("Error: Credenciales incorrectas.")

    def cambiar_sesion_prueba(self, rol_nombre: str):
        """Permite cambiar el rol en la barra superior para pruebas de desarrollo"""
        if rol_nombre == "Administrador":
            self.nivel_usuario = 1
            self.usuario_logueado = "admin"
        elif rol_nombre == "Supervisor":
            self.nivel_usuario = 2
            self.usuario_logueado = "supervisor"
        else:
            self.nivel_usuario = 3
            self.usuario_logueado = "operario"


class PersonalState(rx.State):
    """Maneja el CRUD de personal apuntando a tu base de datos real"""
    usuarios: List[Usuario] = []

    # Campos del formulario coincidentes con tu modelo
    input_usuario: str = ""
    input_password: str = ""
    nivel_seleccionado: str = "3"  # Guardará "1", "2" o "3"

    # Módulos del Sidebar
    modulo_dashboard: bool = False
    modulo_stock: bool = False
    modulo_procura: bool = False
    modulo_seguridad_epp: bool = False
    modulo_vehiculos: bool = False
    modulo_hoja_tiempo: bool = False
    
    nombre_archivo_cv: str = "Sin Cargar"

    def cargar_usuarios_bd(self):
        """Carga los usuarios usando sqlmodel.select compatible con tu modelo"""
        with rx.session() as session:
            # CORRECCIÓN CLAVE: Usamos sqlmodel.select(Usuario) que acepta clases SQLModel puras
            statement = sqlmodel.select(Usuario)
            self.usuarios = session.exec(statement).all()

    @rx.var
    def modulos_seleccionados_str(self) -> str:
        if self.nivel_seleccionado == "1":
            return "TODOS"
        lista = []
        if self.modulo_dashboard: lista.append("Dashboard")
        if self.modulo_stock: lista.append("Stock")
        if self.modulo_procura: lista.append("Procura")
        if self.modulo_seguridad_epp: lista.append("Seguridad EPP")
        if self.modulo_vehiculos: lista.append("Vehículos")
        if self.modulo_hoja_tiempo: lista.append("Hoja de Tiempo")
        return ", ".join(lista) if lista else "Consulta Básica"

    async def manejar_subida_cv(self, archivos: List[rx.UploadFile]):
        if not archivos: return
        for archivo in archivos:
            try:
                nombre = archivo.filename
            except AttributeError:
                nombre = getattr(archivo, "client_filename", "archivo_cv.pdf")
            self.nombre_archivo_cv = nombre

    def crear_usuario(self):
        if not self.input_usuario or not self.input_password:
            return rx.window_alert("Error: Nombre de usuario y contraseña son obligatorios.")
        
        username_clean = self.input_usuario.strip()

        with rx.session() as session:
            # Verificamos duplicados con la nueva sintaxis limpia
            statement = sqlmodel.select(Usuario).where(Usuario.nombre_usuario == username_clean)
            usuario_existente = session.exec(statement).first()
            
            if usuario_existente:
                return rx.window_alert(f"El usuario '{username_clean}' ya está registrado en el sistema. Elige otro.")

            # Inserción limpia en tu MySQL
            nuevo = Usuario(
                nombre_usuario=username_clean,
                password=self.input_password,
                nivel=int(self.nivel_seleccionado),
                estado="activo"
            )
            session.add(nuevo)
            session.commit()
        
        # Refrescar la lista de la pantalla
        self.cargar_usuarios_bd()
        
        # Resetear campos del formulario
        self.input_usuario = ""
        self.input_password = ""
        self.nivel_seleccionado = "3"
        self.nombre_archivo_cv = "Sin Cargar"
        self.modulo_dashboard = False
        self.modulo_stock = False
        self.modulo_procura = False
        self.modulo_seguridad_epp = False
        self.modulo_vehiculos = False
        self.modulo_hoja_tiempo = False
        
        return rx.window_alert("¡Usuario guardado con éxito en la Base de Datos!")