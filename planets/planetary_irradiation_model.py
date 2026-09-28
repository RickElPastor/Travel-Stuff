import math


class ModeloIrradiacionPlanetaria:
    """
    Calcula la irradiación actual de un planeta
    a partir de la luminosidad actual de su estrella.

    La temperatura calculada usa:

    - albedo de Bond = 0
    - redistribución uniforme del calor

    Por tanto NO es una temperatura superficial.
    Es una temperatura de equilibrio de referencia.
    """

    FLUJO_SOLAR_TIERRA_W_M2 = 1361.0

    STEFAN_BOLTZMANN = 5.670374419e-8

    def actualizar(
        self,
        planeta,
        estrella,
    ):
        if estrella is None:
            self.limpiar(planeta)
            return

        if not estrella.viva:
            self.limpiar(planeta)
            return

        if estrella.luminosidad is None or estrella.luminosidad <= 0:
            self.limpiar(planeta)
            return

        semieje = planeta.semieje_mayor_au

        if semieje <= 0:
            self.limpiar(planeta)
            return

        excentricidad = planeta.excentricidad

        if not 0 <= excentricidad < 1:
            self.limpiar(planeta)
            return

        factor_excentricidad = 1.0 / math.sqrt(1.0 - excentricidad**2)

        flujo_relativo = estrella.luminosidad / semieje**2 * factor_excentricidad

        irradiancia = self.FLUJO_SOLAR_TIERRA_W_M2 * flujo_relativo

        temperatura_equilibrio = (irradiancia / (4.0 * self.STEFAN_BOLTZMANN)) ** 0.25

        planeta.flujo_estelar_tierra = flujo_relativo

        planeta.irradiancia_media_w_m2 = irradiancia

        planeta.temperatura_equilibrio_cero_albedo_k = temperatura_equilibrio

    def limpiar(
        self,
        planeta,
    ):
        planeta.flujo_estelar_tierra = None
        planeta.irradiancia_media_w_m2 = None

        planeta.temperatura_equilibrio_cero_albedo_k = None
