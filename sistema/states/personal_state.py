import reflex as rx
from sqlmodel import select
from typing import List, Optional
from sistema.api.models import Usuario
import hashlib

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
    # Editing id when updating an existing user
    editing_id: Optional[int] = None
    # Pending deletion id for confirmation modal
    pending_delete_id: Optional[int] = None

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
    # Search query for filtering usuarios
    search_query: str = ""
    # Additional person fields
    input_telefono: str = ""
    input_direccion: str = ""
    input_notas: str = ""
    input_cv_url: str = ""
    input_foto_url: str = ""
    input_vehiculo_asignado: str = ""

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
            # Buscamos por nombre y luego verificamos hash/plan text
            user = session.exec(select(Usuario).where(Usuario.nombre_usuario == self.username_input)).first()

            # Si existe usuario, verificar contraseña: soporta hashes sha256 migrados o texto plano
            if user:
                input_hashed = hashlib.sha256(self.password_input.encode()).hexdigest()
                if user.password == input_hashed:
                    valid = True
                elif user.password == self.password_input:
                    # contraseña almacenada en texto plano; migramos a hash
                    user.password = input_hashed
                    session.add(user)
                    session.commit()
                    valid = True
                else:
                    valid = False
            else:
                valid = False
            if valid:
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
    def logout_usuario(self):
        """Resetea la sesión y redirige al Login real"""
        self.usuario_logueado = "Invitado"
        self.nivel_usuario = 3
        self.permisos_raw = ""
        self.username_input = ""
        self.password_input = ""
        return rx.redirect("/login")

    @rx.event
    def salir_sistema(self):
        return self.logout_usuario()

    # --- LÓGICA DE MÓDULO DE PERSONAL ---
    @rx.event
    def cargar_usuarios(self):
        """Pobla la lista de colaboradores en la tabla"""
        with rx.session() as session:
            query = select(Usuario)
            if self.search_query:
                # Use SQL contains to filter by username
                query = query.where(Usuario.nombre_usuario.contains(self.search_query))
            self.usuarios = session.exec(query).all()

    # Este es el alias del evento que busca tu decorator on_load de la página
    @rx.event
    def cargar_usuarios_bd(self):
        return self.cargar_usuarios()

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value or ""
        # reload users with filter
        return self.cargar_usuarios()

    @rx.event
    def set_input_telefono(self, value: str):
        self.input_telefono = value

    @rx.event
    def set_input_direccion(self, value: str):
        self.input_direccion = value

    @rx.event
    def set_input_notas(self, value: str):
        self.input_notas = value

    @rx.event
    def set_input_cv_url(self, value: str):
        self.input_cv_url = value

    @rx.event
    def set_input_foto_url(self, value: str):
        self.input_foto_url = value

    @rx.event
    def set_input_vehiculo_asignado(self, value: str):
        self.input_vehiculo_asignado = value

    # --- Setters para inputs y checkboxes del formulario ---
    @rx.event
    def set_input_usuario(self, value: str):
        self.input_usuario = value

    @rx.event
    def set_input_password(self, value: str):
        self.input_password = value

    @rx.event
    def set_perfil_jerarquico(self, value: str):
        # Allow select to pass labels; map known labels to numeric codes
        mapping = {"Admin": "1", "Supervisor": "2", "Empleado": "3"}
        self.perfil_jerarquico = mapping.get(value, value)

    @rx.event
    def set_modulo_dashboard(self, checked: bool):
        self.modulo_dashboard = bool(checked)

    @rx.event
    def set_modulo_stock(self, checked: bool):
        self.modulo_stock = bool(checked)

    @rx.event
    def set_modulo_procura(self, checked: bool):
        self.modulo_procura = bool(checked)

    @rx.event
    def set_modulo_epp(self, checked: bool):
        self.modulo_epp = bool(checked)

    @rx.event
    def set_modulo_vehiculos(self, checked: bool):
        self.modulo_vehiculos = bool(checked)

    @rx.event
    def set_modulo_hoja_tiempo(self, checked: bool):
        self.modulo_hoja_tiempo = bool(checked)

    @rx.event
    def set_modulo_ia(self, checked: bool):
        self.modulo_ia = bool(checked)

    @rx.event
    def registrar_colaborador(self):
        if not self.input_usuario:
            return rx.toast.error("El usuario es obligatorio.")

        # If creating a new user (not editing), password is required
        creating = self.editing_id is None
        if creating and not self.input_password:
            return rx.toast.error("La contraseña es obligatoria para nuevos usuarios.")

        # Basic password strength validation when password provided
        if self.input_password and len(self.input_password) < 6:
            return rx.toast.error("La contraseña debe tener al menos 6 caracteres.")

        # Recolectamos los módulos marcados en el formulario
        lista_permisos = []
        if self.modulo_dashboard: lista_permisos.append("dash")
        if self.modulo_stock: lista_permisos.append("stock")
        if self.modulo_procura: lista_permisos.append("proc")
        if self.modulo_epp: lista_permisos.append("epp")
        if self.modulo_vehiculos: lista_permisos.append("fleet")
        if self.modulo_hoja_tiempo: lista_permisos.append("time")
        if self.modulo_ia: lista_permisos.append("ia")

        # Normalize perfil_jerarquico to an int (accept labels or numeric strings)
        rev_map = {"admin": 1, "supervisor": 2, "empleado": 3, "1": 1, "2": 2, "3": 3}
        pk = str(self.perfil_jerarquico).strip().lower()
        nivel_int = rev_map.get(pk)
        try:
            if nivel_int is None:
                nivel_int = int(pk)
        except Exception:
            nivel_int = 3

        # Si el usuario es nivel 1 (Admin), le damos pase completo automático
        if nivel_int == 1:
            cadena_final = "TODOS, all"
        else:
            cadena_final = ", ".join(lista_permisos)

        with rx.session() as session:
            # If editing, update existing record
            if self.editing_id is not None:
                usuario_obj = session.get(Usuario, self.editing_id)
                if not usuario_obj:
                    return rx.toast.error("Usuario no encontrado para actualizar.")
                usuario_obj.nombre_usuario = self.input_usuario
                # Update password only if a new one was provided
                if self.input_password:
                    hashed = hashlib.sha256(self.input_password.encode()).hexdigest()
                    usuario_obj.password = hashed
                usuario_obj.nivel = nivel_int
                usuario_obj.estado = cadena_final
                usuario_obj.telefono = self.input_telefono
                usuario_obj.direccion = self.input_direccion
                usuario_obj.notas = self.input_notas
                usuario_obj.cv_url = self.input_cv_url
                usuario_obj.foto_url = self.input_foto_url
                usuario_obj.vehiculo_asignado = self.input_vehiculo_asignado
                session.add(usuario_obj)
                session.commit()
                mensaje = f"Colaborador '{usuario_obj.nombre_usuario}' actualizado exitosamente"
            else:
                existe = session.exec(select(Usuario).where(Usuario.nombre_usuario == self.input_usuario)).first()
                if existe:
                    return rx.toast.error("Este nombre de usuario ya existe.")
                # Hash password before storing
                hashed = hashlib.sha256(self.input_password.encode()).hexdigest()
                nuevo = Usuario(
                    nombre_usuario=self.input_usuario,
                    password=hashed,
                    nivel=nivel_int,
                    estado=cadena_final,  # Insertamos la cadena de permisos en tu columna real de la BD
                    telefono=self.input_telefono,
                    direccion=self.input_direccion,
                    notas=self.input_notas,
                    cv_url=self.input_cv_url,
                    foto_url=self.input_foto_url,
                    vehiculo_asignado=self.input_vehiculo_asignado,
                )
                session.add(nuevo)
                session.commit()
                mensaje = f"¡Colaborador '{nuevo.nombre_usuario}' creado con éxito!"

        # Reset and reload
        self.limpiar_formulario()
        self.editing_id = None
        self.cargar_usuarios()
        return rx.toast.success(mensaje)

    @rx.event
    def editar_colaborador(self, user_id: int):
        """Carga un usuario existente en el formulario para editarlo."""
        with rx.session() as session:
            user = session.get(Usuario, user_id)
            if not user:
                return rx.toast.error("Usuario no encontrado.")
            self.editing_id = user.id
            self.input_usuario = user.nombre_usuario
            # Do not pre-fill password with hash; require entering a new password to change
            self.input_password = ""
            # set perfil as numeric string for the select
            self.perfil_jerarquico = str(user.nivel)
            # Parse permisos string into checkboxes
            perms = (user.estado or "").lower()
            self.modulo_dashboard = "dash" in perms or "todos" in perms or "all" in perms
            self.modulo_stock = "stock" in perms or "todos" in perms or "all" in perms
            self.modulo_procura = "proc" in perms or "todos" in perms or "all" in perms
            self.modulo_epp = "epp" in perms or "todos" in perms or "all" in perms
            self.modulo_vehiculos = "fleet" in perms or "todos" in perms or "all" in perms
            self.modulo_hoja_tiempo = "time" in perms or "todos" in perms or "all" in perms
            self.modulo_ia = "ia" in perms or "todos" in perms or "all" in perms
            # Populate extended fields
            self.input_telefono = user.telefono or ""
            self.input_direccion = user.direccion or ""
            self.input_notas = user.notas or ""
            self.input_cv_url = user.cv_url or ""
            self.input_foto_url = user.foto_url or ""
            self.input_vehiculo_asignado = user.vehiculo_asignado or ""

    @rx.event
    def eliminar_colaborador(self, user_id: int):
        """Elimina un colaborador por id."""
        with rx.session() as session:
            obj = session.get(Usuario, user_id)
            if not obj:
                return rx.toast.error("Usuario no encontrado.")
            session.delete(obj)
            session.commit()
        self.pending_delete_id = None
        self.cargar_usuarios()
        return rx.toast.success("Usuario eliminado correctamente.")

    @rx.event
    def confirmar_eliminar_colaborador(self, user_id: int):
        """Setea el id pendiente para mostrar modal de confirmación"""
        self.pending_delete_id = user_id

    @rx.event
    def cancelar_eliminar(self):
        self.pending_delete_id = None

    @rx.event
    def cancelar_edicion(self):
        self.limpiar_formulario()
        self.editing_id = None

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
        # Clear extended fields
        self.input_telefono = ""
        self.input_direccion = ""
        self.input_notas = ""
        self.input_cv_url = ""
        self.input_foto_url = ""
        self.input_vehiculo_asignado = ""


# --- ALIAS DE COMPATIBILIDAD SIN PARÉNTESIS (FUERA DE LA CLASE) ---
PersonalState = SessionState