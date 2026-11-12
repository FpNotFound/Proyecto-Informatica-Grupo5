"""CONTROLADOR de locales: operaciones CRUD.

CRUD son las cuatro operaciones básicas con datos:
    C = Create (Crear)      -> crear()
    R = Read   (Leer)       -> listar() y buscar()
    U = Update (Actualizar) -> modificar()
    D = Delete (Borrar)     -> eliminar()

Antes de cambiar nada se comprueba que el usuario tiene permiso según su rol
(ver docs/ROLES.md). crear() y modificar() devuelven dos cosas: el local
(None si algo ha fallado) y un mensaje de error. eliminar() devuelve solo el mensaje.
"""
# Traemos del modelo el molde Local y las funciones que leen/escriben locales.json.
from src.models.local import Local, cargar_locales, guardar_locales


class LocalController:
    def __init__(self):
        # La primera vez que se abre la aplicación (no hay locales) crea uno de prueba.
        # Su código "NEG-001" es el que usa el propietario de prueba bar@arguelles.es.
        if not cargar_locales():
            guardar_locales([Local("NEG-001", "Bar Demo", "Calle Ferraz 10", "Bar", 80)])

    # ------------------------------------------------------------------
    # PERMISOS: qué puede hacer cada rol con los locales
    # ------------------------------------------------------------------
    def puede_crear(self, usuario):
        """Solo la Autoridad puede dar de alta locales."""
        # Devuelve True si el rol es "Autoridad" y False en cualquier otro caso.
        return usuario.rol == "Autoridad"

    def puede_eliminar(self, usuario):
        """Solo la Autoridad puede eliminar locales."""
        return usuario.rol == "Autoridad"

    def puede_editar(self, usuario, local):
        """La Autoridad puede editar cualquier local; el Propietario, solo el suyo."""
        # La Autoridad siempre puede.
        if usuario.rol == "Autoridad":
            return True
        # El Propietario solo si el código de su cuenta es el del local.
        if usuario.rol == "Propietario" and usuario.codigo_negocio == local.codigo:
            return True
        # Nadie más (por ejemplo, los Vecinos) puede editar.
        return False

    # ------------------------------------------------------------------
    # R = LEER
    # ------------------------------------------------------------------
    def listar(self):
        """Devuelve todos los locales. Todos los roles pueden verlos."""
        return cargar_locales()

    def buscar(self, codigo):
        """Devuelve el local con ese código de negocio, o None si no existe."""
        # Recorremos todos los locales guardados.
        for local in cargar_locales():
            # Si el código coincide, lo devolvemos.
            if local.codigo == codigo:
                return local
        # No se ha encontrado.
        return None

    def validar(self, nombre, direccion, tipo, aforo):
        """Revisa los datos del formulario. Devuelve "" si todo está bien o el error."""
        # El nombre y la dirección no pueden estar vacíos.
        if not nombre or not direccion:
            return "El nombre y la dirección son obligatorios."
        # Hay que elegir un tipo en el desplegable.
        if not tipo:
            return "Debes elegir el tipo de local."
        # isdigit() comprueba que el texto solo tiene cifras (0-9).
        # int() convierte el texto "80" en el número 80.
        if not aforo.isdigit() or int(aforo) == 0:
            return "El aforo debe ser un número entero mayor que 0."
        # Sin errores.
        return ""

    # ------------------------------------------------------------------
    # C = CREAR
    # ------------------------------------------------------------------
    def crear(self, usuario, codigo, nombre, direccion, tipo, aforo):
        """Da de alta un local nuevo (solo Autoridad)."""
        # 1. Permiso.
        if not self.puede_crear(usuario):
            return None, "Solo la Autoridad puede dar de alta locales."
        # 2. Limpiamos los textos (espacios sobrantes y código en mayúsculas).
        codigo = codigo.strip().upper()
        nombre = nombre.strip()
        direccion = direccion.strip()
        aforo = aforo.strip()
        # 3. El código es obligatorio y no se puede repetir.
        if not codigo:
            return None, "El código de negocio es obligatorio."
        if self.buscar(codigo):
            return None, "Ya existe un local con ese código de negocio."
        # 4. Revisamos el resto de datos; si hay error, lo devolvemos.
        error = self.validar(nombre, direccion, tipo, aforo)
        if error:
            return None, error
        # 5. Creamos el local (el aforo se guarda como número con int()).
        local = Local(codigo, nombre, direccion, tipo, int(aforo))
        # 6. Lo añadimos a la lista y guardamos el archivo.
        locales = cargar_locales()
        locales.append(local)
        guardar_locales(locales)
        # 7. Devolvemos el local creado y ningún error.
        return local, ""

    # ------------------------------------------------------------------
    # U = ACTUALIZAR
    # ------------------------------------------------------------------
    def modificar(self, usuario, codigo, nombre, direccion, tipo, aforo):
        """Cambia los datos de un local. El código de negocio no se puede cambiar."""
        # Limpiamos los textos.
        nombre = nombre.strip()
        direccion = direccion.strip()
        aforo = aforo.strip()
        # Leemos todos los locales.
        locales = cargar_locales()
        # Buscamos el que tiene ese código.
        for local in locales:
            if local.codigo == codigo:
                # Permiso: Autoridad o el Propietario de ese local.
                if not self.puede_editar(usuario, local):
                    return None, "No tienes permiso para modificar este local."
                # Revisamos los datos nuevos.
                error = self.validar(nombre, direccion, tipo, aforo)
                if error:
                    return None, error
                # Sustituimos los datos antiguos por los nuevos.
                local.nombre = nombre
                local.direccion = direccion
                local.tipo = tipo
                local.aforo = int(aforo)
                # Guardamos la lista completa (con el local ya cambiado).
                guardar_locales(locales)
                return local, ""
        # Si el bucle termina sin encontrarlo, es que alguien lo ha borrado.
        return None, "Este local ya no existe."

    # ------------------------------------------------------------------
    # D = BORRAR
    # ------------------------------------------------------------------
    def eliminar(self, usuario, codigo):
        """Borra un local (solo Autoridad). Devuelve "" si ha ido bien o el error."""
        # Permiso.
        if not self.puede_eliminar(usuario):
            return "Solo la Autoridad puede eliminar locales."
        # Creamos una lista nueva con todos los locales MENOS el que se borra.
        restantes = []
        for local in cargar_locales():
            # "!=" significa "distinto de".
            if local.codigo != codigo:
                restantes.append(local)
        # Guardamos la lista sin ese local.
        guardar_locales(restantes)
        # Sin errores.
        return ""
