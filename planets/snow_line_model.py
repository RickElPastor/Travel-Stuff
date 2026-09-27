class ModeloLineaHielo:
    """
    Aproximación de Fase 1 para la línea de hielo.

    R_hielo = 2.7 * M_estelar^(1/3) AU

    La línea real evoluciona con el tiempo y depende
    también de acreción, opacidad y temperatura.
    """

    RADIO_SOLAR_AU = 2.7

    def calcular_linea_hielo_au(
        self,
        masa_estelar,
    ):
        masa = float(masa_estelar)

        if masa <= 0:
            raise ValueError("La masa estelar debe ser mayor que 0.")

        return self.RADIO_SOLAR_AU * masa ** (1.0 / 3.0)
