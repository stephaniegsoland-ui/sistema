import reflex as rx
from sqlmodel import select
from typing import List
from sistema.api.models import Usuario

class SessionState(rx.State):
    # Variables globales leídas de forma reactiva por el sidebar
    usuario_logueado: str = "Invitado"
    nivel_usuario: int = 3          # 1: Admin, 2: Supervisor, 3: Empleado
    permisos_raw: str = ""          # Almacena el string de módulos ej: "dashboard,stock,ia"
    
    # Inputs del formulario de Login
    username_input: str = ""
    password_input: str = ""

    # Inputs del Formulario de Personal
    input_usuario: str = ""
    input_password: str = ""
    perfil_jerarquico: str = "3"

    # Checkboxes de Permisos
    modulo_dashboard: bool = False
    modulo_stock: bool = False
    modulo_procura: bool = False
    modulo_epp: bool = False
    modulo_vehiculos: bool = False
    modulo_hoja_tiempo: bool = False
    modulo_ia: bool = False

    # Lista para alimentar la tabla de vista de personal
    usuarios: List[Usuario] = []

    @rx.var
    def esta_autenticado(self) -> bool:
        return self.usuario_logueado != "Invitado"

    # --- LÓGICA DE AUTENTICACIÓN (LOGIN) ---
    @rx.event
    def login_usuario(self):
        """Valida credenciales contra la BD e inyecta los datos al sidebar"""
        if not self.username_input or not self.password_input:
            return rx.toast.error("Por favor, rellene todos los campos.")

        with rx.session() as session:
            # Quitamos el filtro 'estado == ACTIVO' porque 'estado' guarda tus strings de permisos reales
            query = select(Usuario).where(
                Usuario.nombre_usuario == self.username_input,
                Usuario.password == self.password_input
            )
            user = session.exec(query).first()

            if user:
                # Actualizamos las llaves del SessionState que tu sidebar lee
                self.usuario_logueado = user.nombre_usuario
                self.nivel_usuario = user.nivel
                
                # REGLA CRÍTICA: Mapeamos la columna real 'estado' a tu variable del sidebar 'permisos_raw'
                self.permisos_raw = user.estado if user.estado else ""
                
                # Limpiamos inputs
                self.username_input = ""
                self.password_input = ""
                
                return rx.redirect("/dashboard")
            else:
                return rx.toast.error("Usuario o contraseña incorrectos.")

    @rx.event
    def salir_sistema(self):
        """Resetea la sesión y redirige al Login real"""
        self.usuario_logueado = "Invitado"
        self.nivel_usuario = 3
        self.permisos_raw = ""
        
        # Opción A: Si tu login es la página principal del sistema
        return rx.redirect("/")

    # --- LÓGICA DE MÓDULO DE PERSONAL ---
    @rx.event
    def cargar_usuarios(self):
        """Pobla la lista de colaboradores en la tabla"""
        with rx.session() as session:
            self.usuarios = session.exec(select(Usuario)).all()

    # Este es el alias del evento que busca tu decorator on_load de la página
    @rx.event
    def cargar_usuarios_bd(self):
        return self.cargar_usuarios()

    @rx.event
    def registrar_colaborador(self):
        if not self.input_usuario or not self.input_password:
            return rx.toast.error("El usuario y la contraseña son obligatorios.")

        # Recolectamos los módulos marcados en el formulario
        lista_permisos = []
        if self.modulo_dashboard: lista_permisos.append("dash")
        if self.modulo_stock: lista_permisos.append("stock")
        if self.modulo_procura: lista_permisos.append("proc")
        if self.modulo_epp: lista_permisos.append("epp")
        if self.modulo_vehiculos: lista_permisos.append("fleet")
        if self.modulo_hoja_tiempo: lista_permisos.append("time")
        if self.modulo_ia: lista_permisos.append("ia")

        # Si el usuario es nivel 1 (Admin), le damos pase completo automático
        if int(self.perfil_jerarquico) == 1:
            cadena_final = "TODOS, all"
        else:
            cadena_final = ", ".join(lista_permisos)

        with rx.session() as session:
            existe = session.exec(select(Usuario).where(Usuario.nombre_usuario == self.input_usuario)).first()
            if existe:
                return rx.toast.error("Este nombre de usuario ya existe.")

            nuevo = Usuario(
                nombre_usuario=self.input_usuario,
                password=self.input_password,
                nivel=int(self.perfil_jerarquico),
                estado=cadena_final  # Insertamos la cadena de permisos en tu columna real de la BD
            )
            session.add(nuevo)
            session.commit()

        self.limpiar_formulario()
        self.cargar_usuarios()
        return rx.toast.success(f"¡Colaborador '{nuevo.nombre_usuario}' creado con éxito!")

    def limpiar_formulario(self):
        self.input_usuario = ""
        self.input_password = ""
        self.perfil_jerarquico = "3"
        self.modulo_dashboard = False
        self.modulo_stock = False
        self.modulo_procura = False
        self.modulo_epp = False
        self.modulo_vehiculos = False
        self.modulo_hoja_tiempo = False
        self.modulo_ia = False


# --- ALIAS DE COMPATIBILIDAD SIN PARÉNTESIS (FUERA DE LA CLASE) ---
PersonalState = SessionState