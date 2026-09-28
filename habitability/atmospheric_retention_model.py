import math


class ModeloRetencionAtmosferica:
    """
    Filtro empírico de retención atmosférica.

    Usa la cosmic shoreline clásica:

        S_crit = 5e-16 * v_escape^4

    donde:
    - v_escape está en m/s
    - S_crit queda expresado en flujo terrestre

    Esto NO demuestra que exista una atmósfera.
    Solo estima si el planeta está del lado
    favorable a retenerla.
    """

    G = 6.67430e-11

    MASA_TIERRA_KG = 5.9722e24
    RADIO_TIERRA_M = 6.371e6

    CONSTANTE_SHORELINE = 5.0e-16

    def evaluar(
        self,
        planeta,
    ):
        self.limpiar(planeta)

        if planeta.masa_tierra <= 0:
            return

        if planeta.radio_tierra is None or planeta.radio_tierra <= 0:
            return

        if planeta.flujo_estelar_tierra is None:
            return

        masa_kg = planeta.masa_tierra * self.MASA_TIERRA_KG

        radio_m = planeta.radio_tierra * self.RADIO_TIERRA_M

        velocidad_escape_ms = math.sqrt(2.0 * self.G * masa_kg / radio_m)

        flujo_critico = self.CONSTANTE_SHORELINE * velocidad_escape_ms**4

        planeta.velocidad_escape_kms = velocidad_escape_ms / 1000.0

        planeta.shoreline_flujo_critico_tierra = flujo_critico

        if not planeta.candidato_terrestre_hz:
            return

        planeta.retencion_atmosferica_aprox = (
            planeta.flujo_estelar_tierra <= flujo_critico
        )

    def limpiar(
        self,
        planeta,
    ):
        planeta.velocidad_escape_kms = None

        planeta.shoreline_flujo_critico_tierra = None

        planeta.retencion_atmosferica_aprox = False
