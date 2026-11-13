"""CONTROLADOR de vigilancia: alertas a la policía, cierres temporales,
reclamaciones de los propietarios, log de incidencias y notificaciones.

QUIÉN PUEDE HACER QUÉ
    Autoridad (policía):
        - recibe una notificación cuando un bar llega a niveles peligrosos (rojo)
        - cierra temporalmente un bar (antes tiene que escribir el motivo)
        - reabre un bar
        - decide si una reclamación es "Justificado" o "No justificado"
    Propietario:
        - recibe una notificación si cierran su bar, con el motivo que escribió la policía
        - puede presentar UNA reclamación por cada cierre
    Todos:
        - ven el log de incidencias de cada bar

Las funciones que cambian algo devuelven "" si todo ha ido bien, o un texto
con el error (igual que LocalController).
"""
# Datos de vigilancia (incidencias, cierres y notificaciones).
from src.models.vigilancia import (
    cargar_cierres,
    cargar_incidencias,
    cargar_notificaciones,
    guardar_cierres,
    guardar_incidencias,
    guardar_notificaciones,
)

# Para poner la fecha de ahora.
from src.controllers.sensor_controller import fecha_actual

# Para saber los locales que existen.
from src.models.local import cargar_locales

# Mínimo de letras que debe tener el motivo de un cierre (para que sea una explicación de verdad).
MINIMO_LETRAS_MOTIVO = 20

# Tipos de incidencia que aparecen en el log.
TIPO_PELIGRO = "Nivel peligroso"
TIPO_NORMALIZADO = "Niveles normalizados"
TIPO_CIERRE = "Cierre temporal"
TIPO_REAPERTURA = "Reapertura"
TIPO_RECLAMACION = "Reclamación"
TIPO_RESOLUCION = "Resolución de reclamación"


def nombre_policia(usuario):
    """Texto que identifica al policía. Ejemplo: "Ayuntamiento Demo (POL-0001)"."""
    return f"{usuario.nombre} ({usuario.id_policial})"


class VigilanciaController:
    # ------------------------------------------------------------------
    # LOG DE INCIDENCIAS
    # ------------------------------------------------------------------
    def apuntar_incidencia(self, codigo, tipo, autor, descripcion):
        """Añade una línea al log de incidencias de un bar."""
        incidencias = cargar_incidencias()
        incidencias.append(
            {"local": codigo, "fecha": fecha_actual(), "tipo": tipo, "autor": autor, "descripcion": descripcion}
        )
        guardar_incidencias(incidencias)

    def incidencias_de(self, codigo):
        """Log de incidencias de un bar, de la más nueva a la más antigua."""
        resultado = []
        for incidencia in cargar_incidencias():
            if incidencia["local"] == codigo:
                resultado.append(incidencia)
        # reversed() da la vuelta a la lista para que la más nueva salga primero.
        return list(reversed(resultado))

    # ------------------------------------------------------------------
    # NOTIFICACIONES
    # ------------------------------------------------------------------
    def notificar(self, para, titulo, mensaje):
        """Crea un aviso. "para" es "Autoridad" o el código de un local."""
        notificaciones = cargar_notificaciones()
        notificaciones.append(
            {"para": para, "fecha": fecha_actual(), "titulo": titulo, "mensaje": mensaje, "leida": False}
        )
        guardar_notificaciones(notificaciones)

    def es_para(self, notificacion, usuario):
        """True si esa notificación le corresponde a ese usuario."""
        # Las de "Autoridad" las ven todos los policías.
        if notificacion["para"] == "Autoridad":
            return usuario.rol == "Autoridad"
        # Las demás llevan un código de local: las ve el propietario de ese local.
        return usuario.rol == "Propietario" and usuario.codigo_negocio == notificacion["para"]

    def notificaciones_de(self, usuario):
        """Avisos de un usuario, del más nuevo al más antiguo."""
        resultado = []
        for notificacion in cargar_notificaciones():
            if self.es_para(notificacion, usuario):
                resultado.append(notificacion)
        return list(reversed(resultado))

    def sin_leer(self, usuario):
        """Cuántos avisos no ha leído todavía el usuario."""
        total = 0
        for notificacion in self.notificaciones_de(usuario):
            if not notificacion["leida"]:
                total = total + 1
        return total

    def marcar_leidas(self, usuario):
        """Marca como leídos todos los avisos del usuario."""
        notificaciones = cargar_notificaciones()
        for notificacion in notificaciones:
            if self.es_para(notificacion, usuario):
                notificacion["leida"] = True
        guardar_notificaciones(notificaciones)

    # ------------------------------------------------------------------
    # ALERTAS AUTOMÁTICAS (niveles peligrosos)
    # ------------------------------------------------------------------
    def alerta_abierta(self, codigo):
        """True si el bar tiene una alerta de peligro que aún no se ha normalizado.

        Miramos la última incidencia automática del bar: si es "Nivel peligroso",
        la alerta sigue abierta; si es "Niveles normalizados" (o no hay), no.
        """
        abierta = False
        for incidencia in cargar_incidencias():
            if incidencia["local"] == codigo and incidencia["tipo"] == TIPO_PELIGRO:
                abierta = True
            if incidencia["local"] == codigo and incidencia["tipo"] == TIPO_NORMALIZADO:
                abierta = False
        return abierta

    def revisar_alertas(self, sensor_controller):
        """Revisa todos los bares después de cada medida.

        - Si un bar pasa a ROJO: se apunta en su log y se avisa a la policía.
        - Si un bar que estaba en rojo se normaliza: se apunta en su log.
        """
        for local in cargar_locales():
            codigo = local.codigo
            en_peligro = sensor_controller.color_bar(codigo) == "rojo"
            ya_avisado = self.alerta_abierta(codigo)

            if en_peligro and not ya_avisado:
                # Texto con los valores actuales, para que la policía sepa qué pasa.
                detalle = (
                    f"Temperatura {sensor_controller.valor(codigo, 'temperatura')} °C, "
                    f"humedad {sensor_controller.valor(codigo, 'humedad')} %, "
                    f"CO2 {sensor_controller.valor(codigo, 'calidad_aire')} ppm."
                )
                self.apuntar_incidencia(codigo, TIPO_PELIGRO, "Sistema de sensores", detalle)
                self.notificar(
                    "Autoridad",
                    f"Niveles peligrosos en {local.nombre} ({codigo})",
                    detalle,
                )

            if not en_peligro and ya_avisado:
                self.apuntar_incidencia(
                    codigo, TIPO_NORMALIZADO, "Sistema de sensores", "Los sensores vuelven a valores seguros."
                )

    # ------------------------------------------------------------------
    # CIERRES TEMPORALES
    # ------------------------------------------------------------------
    def cierre_activo(self, codigo):
        """El cierre que tiene ahora mismo el bar, o None si está abierto."""
        for cierre in cargar_cierres():
            if cierre["local"] == codigo and cierre["activo"]:
                return cierre
        return None

    def ultimo_cierre(self, codigo):
        """El último cierre que ha tenido el bar (activo o no), o None si nunca lo han cerrado."""
        ultimo = None
        for cierre in cargar_cierres():
            if cierre["local"] == codigo:
                ultimo = cierre
        return ultimo

    def cerrados(self):
        """Lista de todos los cierres activos (bares cerrados ahora mismo)."""
        resultado = []
        for cierre in cargar_cierres():
            if cierre["activo"]:
                resultado.append(cierre)
        return resultado

    def cerrar_local(self, usuario, codigo, motivo):
        """La policía cierra temporalmente un bar. El motivo es obligatorio."""
        # 1. Solo la Autoridad.
        if usuario.rol != "Autoridad":
            return "Solo la policía puede cerrar un local."
        # 2. El motivo tiene que estar escrito y explicar algo.
        motivo = motivo.strip()
        if len(motivo) < MINIMO_LETRAS_MOTIVO:
            return f"Escribe el motivo del cierre (mínimo {MINIMO_LETRAS_MOTIVO} letras)."
        # 3. No se puede cerrar un bar que ya está cerrado.
        if self.cierre_activo(codigo):
            return "Este local ya está cerrado."
        # 4. Guardamos el cierre.
        cierres = cargar_cierres()
        cierres.append(
            {
                "local": codigo,
                "fecha": fecha_actual(),
                "policia": nombre_policia(usuario),
                "motivo": motivo,
                "activo": True,
                "reclamacion": "",
                "estado_reclamacion": "",
                "respuesta": "",
            }
        )
        guardar_cierres(cierres)
        # 5. Lo apuntamos en el log del bar.
        self.apuntar_incidencia(codigo, TIPO_CIERRE, nombre_policia(usuario), motivo)
        # 6. Avisamos al propietario del bar, con el motivo.
        self.notificar(
            codigo,
            "Tu local ha sido cerrado temporalmente",
            f"Motivo escrito por la policía: {motivo} "
            f"Si crees que no está justificado, puedes presentar una reclamación.",
        )
        return ""

    def reabrir_local(self, usuario, codigo, nota):
        """La policía vuelve a abrir un bar cerrado."""
        if usuario.rol != "Autoridad":
            return "Solo la policía puede reabrir un local."
        cierres = cargar_cierres()
        for cierre in cierres:
            if cierre["local"] == codigo and cierre["activo"]:
                cierre["activo"] = False
                guardar_cierres(cierres)
                texto = nota.strip() or "El local puede volver a abrir."
                self.apuntar_incidencia(codigo, TIPO_REAPERTURA, nombre_policia(usuario), texto)
                self.notificar(codigo, "Tu local ya puede volver a abrir", texto)
                return ""
        return "Este local no está cerrado."

    # ------------------------------------------------------------------
    # RECLAMACIONES
    # ------------------------------------------------------------------
    def reclamar(self, usuario, codigo, texto):
        """El propietario reclama un cierre que cree injustificado."""
        # 1. Solo el propietario de ESE local.
        if usuario.rol != "Propietario" or usuario.codigo_negocio != codigo:
            return "Solo el propietario del local puede reclamar."
        texto = texto.strip()
        if not texto:
            return "Escribe por qué crees que el cierre no está justificado."
        cierres = cargar_cierres()
        for cierre in cierres:
            if cierre["local"] == codigo and cierre["activo"]:
                # 2. Solo una reclamación por cierre.
                if cierre["estado_reclamacion"]:
                    return "Ya has presentado una reclamación para este cierre."
                # 3. La guardamos como "Pendiente".
                cierre["reclamacion"] = texto
                cierre["estado_reclamacion"] = "Pendiente"
                guardar_cierres(cierres)
                # 4. Log y aviso a la policía.
                self.apuntar_incidencia(codigo, TIPO_RECLAMACION, usuario.nombre, texto)
                self.notificar("Autoridad", f"Nueva reclamación del local {codigo}", texto)
                return ""
        return "Tu local no está cerrado."

    def reclamaciones_pendientes(self):
        """Cierres con una reclamación que la policía aún no ha valorado."""
        resultado = []
        for cierre in cargar_cierres():
            if cierre["estado_reclamacion"] == "Pendiente":
                resultado.append(cierre)
        return resultado

    def resolver_reclamacion(self, usuario, codigo, justificado, respuesta):
        """La policía valora una reclamación.

        justificado = True  -> el cierre estaba bien hecho: el local sigue cerrado.
        justificado = False -> el cierre no estaba justificado: el local se reabre.
        """
        if usuario.rol != "Autoridad":
            return "Solo la policía puede valorar reclamaciones."
        respuesta = respuesta.strip()
        if not respuesta:
            return "Escribe una respuesta para el propietario."
        cierres = cargar_cierres()
        for cierre in cierres:
            if cierre["local"] == codigo and cierre["estado_reclamacion"] == "Pendiente":
                cierre["respuesta"] = respuesta
                if justificado:
                    cierre["estado_reclamacion"] = "Justificado"
                    titulo = "Reclamación rechazada: el cierre está justificado"
                else:
                    cierre["estado_reclamacion"] = "No justificado"
                    # El cierre no era justo: el local se reabre.
                    cierre["activo"] = False
                    titulo = "Reclamación aceptada: tu local puede volver a abrir"
                guardar_cierres(cierres)
                self.apuntar_incidencia(
                    codigo, TIPO_RESOLUCION, nombre_policia(usuario), f"{cierre['estado_reclamacion']}. {respuesta}"
                )
                self.notificar(codigo, titulo, respuesta)
                return ""
        return "No hay ninguna reclamación pendiente de este local."
