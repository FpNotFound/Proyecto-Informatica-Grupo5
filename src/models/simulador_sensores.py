"""MODELO: SIMULADOR que se inventa las medidas de los sensores.

No tenemos sensores de verdad, así que este archivo genera números creíbles.
Hay dos situaciones ("escenarios"):
    "normal" -> valores tranquilos, sin alertas.
    "alerta" -> mucho calor, mucha humedad y aire cargado (para ver las alertas).
"""
# "random" viene con Python y sirve para sacar números al azar.
import random

# Entre qué valores se mueve cada sensor en cada escenario: (mínimo, máximo).
RANGOS = {
    "normal": {
        "temperatura": (21, 26),
        "humedad": (40, 60),
        "calidad_aire": (450, 900),
    },
    "alerta": {
        "temperatura": (31, 34),
        "humedad": (72, 82),
        "calidad_aire": (1300, 1700),
    },
}


def redondear(tipo, valor):
    """El CO2 se da sin decimales; la temperatura y la humedad con 1 decimal."""
    if tipo == "calidad_aire":
        return round(valor)
    return round(valor, 1)


def valor_al_azar(tipo, escenario):
    """Un valor cualquiera dentro del rango del escenario."""
    minimo, maximo = RANGOS[escenario][tipo]
    # random.uniform da un número con decimales entre minimo y maximo.
    return redondear(tipo, random.uniform(minimo, maximo))


def siguiente_valor(tipo, valor_actual, escenario):
    """La próxima medida: va a mitad de camino entre el valor actual y uno nuevo al azar.

    Así los valores cambian poco a poco, como en un sensor real, y no a saltos.
    """
    destino = valor_al_azar(tipo, escenario)
    return redondear(tipo, (valor_actual + destino) / 2)
