"""CONTROLADOR de sensores: crea los sensores de cada bar, toma medidas y
decide el color de cada bar (semáforo), los LEDs y el ventilador.

REGLAS
    Semáforo de cada sensor:
        verde    -> todo bien
        amarillo -> precaución (se acerca al límite)
        rojo     -> PELIGRO
    Semáforo del bar = el peor color de sus 3 sensores.

    LED ROJO   -> temperatura en peligro (más de 30 °C).
    LED AZUL   -> humedad en peligro (menos de 30 % o más de 70 %).
    LED VERDE  -> calidad del aire en peligro ("Mala": 1200 ppm de CO2 o más).
    VENTILADOR -> se enciende si hay más de 30 °C Y ADEMÁS el aire es "Mala".
"""
# "datetime" da la fecha y hora; "timedelta" sirve para restar horas.
from datetime import datetime, timedelta

# Los locales que ya existen en la aplicación (del CRUD de locales).
from src.models.local import cargar_locales

# Datos y umbrales de los sensores.
from src.models.sensor import (
    CO2_MALO,
    CO2_MODERADO,
    HUMEDAD_PELIGRO_MAXIMA,
    HUMEDAD_PELIGRO_MINIMA,
    HUMEDAD_PRECAUCION_MAXIMA,
    HUMEDAD_PRECAUCION_MINIMA,
    LED_SENSOR,
    TEMPERATURA_PELIGRO,
    TEMPERATURA_PRECAUCION,
    TIPOS_SENSOR,
    cargar_historial,
    cargar_sensores,
    guardar_historial,
    guardar_sensores,
)

# El simulador que se inventa las medidas.
from src.models.simulador_sensores import siguiente_valor, valor_al_azar


def fecha_actual():
    """Fecha y hora de ahora como texto. Ejemplo: "2026-11-13 21:30"."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


class SensorController:
    def __init__(self):
        # Escenario de cada bar: "normal" o "alerta". Ejemplo: {"NEG-001": "alerta"}.
        # Si un bar no aparece aquí, está en "normal".
        self.escenarios = {}
        # Nos aseguramos de que todos los bares tienen sus sensores.
        self.preparar_sensores()

    # ------------------------------------------------------------------
    # CREAR SENSORES
    # ------------------------------------------------------------------
    def preparar_sensores(self):
        """Da 3 sensores (con historial) a cada bar que aún no los tenga.

        También quita los sensores de los bares que se hayan eliminado.
        """
        # Lista con los códigos de los locales que existen (ej. ["NEG-001", "NEG-003"]).
        codigos = []
        for local in cargar_locales():
            codigos.append(local.codigo)

        # Nos quedamos solo con los sensores de locales que existen.
        sensores = []
        for sensor in cargar_sensores():
            if sensor["local"] in codigos:
                sensores.append(sensor)

        # Creamos los sensores de los locales que no tienen ninguno.
        historial = cargar_historial()
        for codigo in codigos:
            if not self.sensores_de(codigo, sensores):
                for tipo in TIPOS_SENSOR:
                    # Primero inventamos sus medidas de las últimas 24 horas.
                    ultimo = self.crear_historial(codigo, tipo, historial)
                    # El sensor empieza con el valor de su última medida.
                    sensores.append(
                        {"local": codigo, "tipo": tipo, "valor": ultimo["valor"], "fecha": ultimo["fecha"]}
                    )

        guardar_sensores(sensores)
        guardar_historial(historial)

    def crear_historial(self, codigo, tipo, historial):
        """Añade al historial una medida por hora de las últimas 24 horas.

        Entre las 23:00 y la 01:59 el bar está lleno, así que esas horas se
        inventan con el escenario "alerta" (y salen alertas en el historial).
        Devuelve la última medida creada.
        """
        ahora = datetime.now()
        medida = None
        # range(24, -1, -1) cuenta hacia atrás: 24, 23, 22, ... 1, 0 (horas atrás).
        for horas_atras in range(24, -1, -1):
            momento = ahora - timedelta(hours=horas_atras)
            if momento.hour >= 23 or momento.hour <= 1:
                escenario = "alerta"
            else:
                escenario = "normal"
            medida = {
                "local": codigo,
                "tipo": tipo,
                "valor": valor_al_azar(tipo, escenario),
                "fecha": momento.strftime("%Y-%m-%d %H:%M"),
            }
            historial.append(medida)
        return medida

    # ------------------------------------------------------------------
    # CONSULTAR
    # ------------------------------------------------------------------
    def sensores_de(self, codigo, sensores=None):
        """Los 3 sensores de un bar (en el orden temperatura, humedad, aire)."""
        # Si no nos pasan la lista, la leemos del archivo.
        if sensores is None:
            sensores = cargar_sensores()
        resultado = []
        for sensor in sensores:
            if sensor["local"] == codigo:
                resultado.append(sensor)
        return resultado

    def valor(self, codigo, tipo):
        """El último valor de un sensor concreto de un bar."""
        for sensor in self.sensores_de(codigo):
            if sensor["tipo"] == tipo:
                return sensor["valor"]
        return 0

    def historial_de(self, codigo, tipo, cantidad):
        """Las últimas "cantidad" medidas de un sensor, de la más nueva a la más antigua."""
        medidas = []
        for medida in cargar_historial():
            if medida["local"] == codigo and medida["tipo"] == tipo:
                medidas.append(medida)
        # medidas[-cantidad:] son las últimas; reversed() les da la vuelta (la más nueva primero).
        return list(reversed(medidas[-cantidad:]))

    # ------------------------------------------------------------------
    # REGLAS (semáforo, LEDs y ventilador)
    # ------------------------------------------------------------------
    def calidad_aire(self, ppm):
        """Convierte los ppm de CO2 en "Buena", "Moderada" o "Mala"."""
        if ppm >= CO2_MALO:
            return "Mala"
        if ppm >= CO2_MODERADO:
            return "Moderada"
        return "Buena"

    def color_sensor(self, tipo, valor):
        """Semáforo de UN sensor: "verde", "amarillo" o "rojo"."""
        if tipo == "temperatura":
            if valor > TEMPERATURA_PELIGRO:
                return "rojo"
            if valor > TEMPERATURA_PRECAUCION:
                return "amarillo"
            return "verde"
        if tipo == "humedad":
            if valor < HUMEDAD_PELIGRO_MINIMA or valor > HUMEDAD_PELIGRO_MAXIMA:
                return "rojo"
            if valor < HUMEDAD_PRECAUCION_MINIMA or valor > HUMEDAD_PRECAUCION_MAXIMA:
                return "amarillo"
            return "verde"
        # Si no es temperatura ni humedad, es calidad del aire.
        calidad = self.calidad_aire(valor)
        if calidad == "Mala":
            return "rojo"
        if calidad == "Moderada":
            return "amarillo"
        return "verde"

    def color_bar(self, codigo):
        """Semáforo del BAR: el peor color de sus sensores."""
        color = "verde"
        for sensor in self.sensores_de(codigo):
            color_del_sensor = self.color_sensor(sensor["tipo"], sensor["valor"])
            # El rojo gana a todo; el amarillo solo gana al verde.
            if color_del_sensor == "rojo":
                color = "rojo"
            elif color_del_sensor == "amarillo" and color == "verde":
                color = "amarillo"
        return color

    def leds(self, codigo):
        """Qué LEDs están encendidos en un bar. Ejemplo: {"rojo": True, "azul": False, "verde": True}."""
        encendidos = {"rojo": False, "azul": False, "verde": False}
        for sensor in self.sensores_de(codigo):
            if self.color_sensor(sensor["tipo"], sensor["valor"]) == "rojo":
                # Cada sensor enciende su LED (temperatura -> rojo, etc.).
                encendidos[LED_SENSOR[sensor["tipo"]]] = True
        return encendidos

    def ventilador(self, codigo):
        """True si el ventilador del bar debe estar encendido."""
        hace_calor = self.valor(codigo, "temperatura") > TEMPERATURA_PELIGRO
        aire_malo = self.calidad_aire(self.valor(codigo, "calidad_aire")) == "Mala"
        # Tienen que cumplirse LAS DOS cosas ("and").
        return hace_calor and aire_malo

    # ------------------------------------------------------------------
    # SIMULAR MEDIDAS
    # ------------------------------------------------------------------
    def escenario(self, codigo):
        """Escenario del bar: "alerta" si se ha forzado, si no "normal"."""
        if codigo in self.escenarios:
            return self.escenarios[codigo]
        return "normal"

    def forzar_alerta(self, codigo):
        """Las próximas medidas de ese bar irán subiendo hasta valores peligrosos."""
        self.escenarios[codigo] = "alerta"

    def volver_normal(self, codigo):
        """Las próximas medidas de ese bar volverán a valores normales."""
        self.escenarios[codigo] = "normal"

    def medir_todos(self):
        """Toma una medida nueva de TODOS los sensores de TODOS los bares."""
        # Por si se ha creado o borrado algún local desde la última vez.
        self.preparar_sensores()
        sensores = cargar_sensores()
        historial = cargar_historial()
        fecha = fecha_actual()
        for sensor in sensores:
            escenario = self.escenario(sensor["local"])
            sensor["valor"] = siguiente_valor(sensor["tipo"], sensor["valor"], escenario)
            sensor["fecha"] = fecha
            # La medida también se apunta en el historial.
            historial.append(
                {"local": sensor["local"], "tipo": sensor["tipo"], "valor": sensor["valor"], "fecha": fecha}
            )
        guardar_sensores(sensores)
        guardar_historial(historial)
