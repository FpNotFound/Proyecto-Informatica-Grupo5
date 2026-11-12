"""CONTROLADOR de acceso: comprueba los datos del registro y del login.

Sus dos funciones devuelven dos cosas: el usuario (None si algo ha fallado)
y un mensaje de error para mostrar en pantalla.
"""
# Controlador de locales: lo usamos para comprobar que el código de negocio existe.
from src.controllers.local_controller import LocalController

# Controlador de usuarios: crea y busca usuarios.
from src.controllers.user_controller import UserController


class LoginController:
    def __init__(self):
        # Guardamos un controlador de usuarios y otro de locales para usarlos después.
        self.users = UserController()
        self.locales = LocalController()

    def registrar(self, nombre, email, password, confirmar, rol, codigo):
        """Da de alta a un usuario nuevo.

        "codigo" es el código de negocio (si el rol es Propietario) o el
        ID policial (si el rol es Autoridad). Para Vecino se ignora.
        """
        # strip() quita los espacios sobrantes al principio y al final.
        nombre = nombre.strip()
        # lower() pasa el correo a minúsculas para que "Ana@x.es" y "ana@x.es" sean iguales.
        email = email.strip().lower()
        # upper() pasa el código a mayúsculas para que "neg-001" sirva igual que "NEG-001".
        codigo = codigo.strip().upper()

        # --- Comprobaciones comunes a todos los roles ---
        # "not nombre" es verdad cuando el nombre está vacío.
        if not nombre or not email or not password:
            return None, "Todos los campos son obligatorios."
        # Un correo válido debe llevar al menos una @ y un punto.
        if "@" not in email or "." not in email:
            return None, "El correo electrónico no tiene un formato válido."
        # len() cuenta cuántos caracteres tiene la contraseña.
        if len(password) < 4:
            return None, "La contraseña debe tener al menos 4 caracteres."
        # Las dos contraseñas escritas deben ser iguales.
        if password != confirmar:
            return None, "Las contraseñas no coinciden."
        # Hay que haber elegido un rol en el desplegable.
        if not rol:
            return None, "Debes seleccionar un rol."
        # No puede haber dos cuentas con el mismo correo.
        if self.users.buscar_por_email(email):
            return None, "Ya existe un usuario registrado con ese correo."

        # Por defecto ningún usuario tiene código de negocio ni ID policial.
        codigo_negocio = ""
        id_policial = ""

        # --- Comprobaciones especiales del Propietario ---
        if rol == "Propietario":
            # Es obligatorio escribir el código de negocio.
            if not codigo:
                return None, "Los propietarios deben introducir su código de negocio."
            # El código tiene que pertenecer a un local que ya exista.
            if self.locales.buscar(codigo) is None:
                return None, "Ese código de negocio no corresponde a ningún local."
            # Cada local solo puede tener un propietario registrado.
            if self.users.buscar_por_codigo_negocio(codigo):
                return None, "Ese local ya tiene un propietario registrado."
            # Todo correcto: este usuario queda unido a ese local.
            codigo_negocio = codigo

        # --- Comprobaciones especiales de la Autoridad ---
        if rol == "Autoridad":
            # Es obligatorio escribir el ID policial.
            if not codigo:
                return None, "La autoridad debe introducir su ID de identificación policial."
            # El ID tiene que estar en la lista oficial (ids_policiales.json).
            if not self.users.id_policial_valido(codigo):
                return None, "Ese ID policial no es válido."
            # Un mismo ID no se puede usar para dos cuentas.
            if self.users.buscar_por_id_policial(codigo):
                return None, "Ese ID policial ya está registrado."
            # Todo correcto: guardamos el ID en el usuario.
            id_policial = codigo

        # Si hemos llegado aquí, todo está bien: creamos el usuario y no hay error ("").
        usuario = self.users.crear_usuario(nombre, email, password, rol, codigo_negocio, id_policial)
        return usuario, ""

    def autenticar(self, email, password):
        """Comprueba el correo y la contraseña al iniciar sesión."""
        # Limpiamos el correo igual que en el registro.
        email = email.strip().lower()
        # Los dos campos son obligatorios.
        if not email or not password:
            return None, "Introduce tu correo y tu contraseña."

        # Buscamos al usuario por su correo.
        usuario = self.users.buscar_por_email(email)
        # Si no existe o la contraseña no coincide, damos el mismo mensaje
        # (así no revelamos si el correo está registrado o no).
        if usuario is None or not self.users.password_correcta(usuario, password):
            return None, "Correo o contraseña incorrectos."

        # Todo correcto: devolvemos el usuario y ningún error.
        return usuario, ""
