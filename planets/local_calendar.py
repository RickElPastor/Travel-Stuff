"""Calendario numérico derivado del reloj universal; no avanza por separado."""

from decimal import Decimal
from math import sqrt


DIAS_ANIO_UNIVERSAL = Decimal("365.2425")
SEGUNDOS_DIA = Decimal(86_400)


def periodo_orbital_dias(semieje_mayor_au, masa_estelar_msol):
    """Aproximación kepleriana para órbitas circumestelares en años terrestres."""
    if masa_estelar_msol is None or masa_estelar_msol <= 0:
        return None
    return float(DIAS_ANIO_UNIVERSAL) * sqrt(
        semieje_mayor_au ** 3 / masa_estelar_msol
    )


def fecha_local(planeta, tiempo, anio_formacion=None, duracion_dias=None):
    """Devuelve año, mes, día, hora, minuto y segundo locales numéricos."""
    if anio_formacion is None:
        anio_formacion = planeta.anio_formacion
    if duracion_dias is None:
        duracion_dias = planeta.periodo_orbital_dias
    if anio_formacion is None or duracion_dias is None or duracion_dias <= 0:
        return None
    edad_anios = tiempo.anio - anio_formacion
    if edad_anios < 0:
        return None
    segundos = (Decimal(edad_anios) + Decimal(str(tiempo.acumulado))) * (
        DIAS_ANIO_UNIVERSAL * SEGUNDOS_DIA
    )
    segundos_orbita = Decimal(str(duracion_dias)) * SEGUNDOS_DIA
    anio, resto = divmod(segundos, segundos_orbita)
    segundos_mes = segundos_orbita / 12
    mes, resto = divmod(resto, segundos_mes)
    dia, resto = divmod(resto, SEGUNDOS_DIA)
    hora, resto = divmod(resto, Decimal(3600))
    minuto, resto = divmod(resto, Decimal(60))
    return (int(anio), int(mes) + 1, int(dia) + 1,
            int(hora), int(minuto), int(resto))
