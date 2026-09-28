class ModeloFisicaPlanetaria:
    """
    Propiedades físicas básicas de Fase 1.

    Planetas sólidos:
    - relación masa-radio de tipo terrestre
    - ajuste simple para mundos ricos en hielos

    Planetas con H/He:
    - relación empírica de Chen & Kipping

    Después se calculan:
    - densidad media
    - gravedad superficial
    """

    DENSIDAD_TIERRA_G_CM3 = 5.513
    GRAVEDAD_TIERRA_MS2 = 9.80665

    EXPONENTE_SOLIDO = 0.274

    FACTOR_ROCOSO = 1.0

    # Proxy Fase 1:
    # aproximadamente 50% material rico en agua.
    FACTOR_RICO_HIELOS = 1.25

    # Interpolación nuestra entre rocoso
    # y rico en hielos.
    FACTOR_MIXTO = 1.125

    def calcular_propiedades(
        self,
        planeta,
    ):
        if planeta.masa_tierra <= 0:
            raise ValueError("La masa planetaria debe ser positiva.")

        radio_tierra = self._calcular_radio_tierra(planeta)

        densidad = self.DENSIDAD_TIERRA_G_CM3 * planeta.masa_tierra / radio_tierra**3

        gravedad = self.GRAVEDAD_TIERRA_MS2 * planeta.masa_tierra / radio_tierra**2

        planeta.radio_tierra = radio_tierra

        planeta.densidad_g_cm3 = densidad

        planeta.gravedad_superficial_ms2 = gravedad

    def _calcular_radio_tierra(
        self,
        planeta,
    ):
        if planeta.masa_gas_tierra > 0:
            return self._calcular_radio_con_gas(planeta.masa_tierra)

        return self._calcular_radio_solido(
            planeta.masa_tierra,
            planeta.composicion_inicial,
        )

    def _calcular_radio_solido(
        self,
        masa_tierra,
        composicion,
    ):
        factor = self.FACTOR_ROCOSO

        if composicion == "rica_en_hielos":
            factor = self.FACTOR_RICO_HIELOS

        elif composicion == "mixta":
            factor = self.FACTOR_MIXTO

        return factor * masa_tierra**self.EXPONENTE_SOLIDO

    def _calcular_radio_con_gas(
        self,
        masa_tierra,
    ):
        if masa_tierra < 2.04:
            return 1.008 * masa_tierra**0.279

        if masa_tierra < 131.6:
            return 0.8081 * masa_tierra**0.589

        return 17.74 * masa_tierra ** (-0.044)
