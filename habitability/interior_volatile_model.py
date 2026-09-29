class ModeloVolatilesInteriores:
    """
    Reservorio potencial de volátiles de Fase 1.

    Usa abundancias terrestres como referencia:

    H2O interior:
        3000 ppm

    Carbono:
        500 ppm

    Nitrógeno:
        0.84 ppm

    IMPORTANTE:
    estos valores NO representan todavía
    una atmósfera.

    Son un reservorio interior disponible
    potencialmente para desgasificación.
    """

    PPM_H2O_REFERENCIA = 3000.0
    PPM_C_REFERENCIA = 500.0
    PPM_N_REFERENCIA = 0.84
    FRACCION_SILICATOS_REFERENCIA = 0.68

    def evaluar(
        self,
        planeta,
    ):
        self.limpiar(planeta)

        if planeta.masa_solida_tierra <= 0:
            return

        masa_solida = planeta.masa_solida_tierra

        masa_reservorio = masa_solida * self.FRACCION_SILICATOS_REFERENCIA

        planeta.reservorio_h2o_interior_tierra = masa_reservorio * self._ppm_a_fraccion(
            self.PPM_H2O_REFERENCIA
        )

        planeta.reservorio_carbono_tierra = masa_reservorio * self._ppm_a_fraccion(
            self.PPM_C_REFERENCIA
        )

        planeta.reservorio_nitrogeno_tierra = masa_reservorio * self._ppm_a_fraccion(
            self.PPM_N_REFERENCIA
        )

        agua_acrecion = (
            planeta.masa_agua_inicial_tierra
            if planeta.masa_agua_inicial_tierra is not None
            else 0.0
        )

        planeta.reservorio_h2o_total_tierra = (
            planeta.reservorio_h2o_interior_tierra + agua_acrecion
        )

    def limpiar(
        self,
        planeta,
    ):
        planeta.reservorio_h2o_interior_tierra = None
        planeta.reservorio_h2o_total_tierra = None
        planeta.reservorio_carbono_tierra = None
        planeta.reservorio_nitrogeno_tierra = None

    def _ppm_a_fraccion(
        self,
        ppm,
    ):
        return float(ppm) / 1_000_000.0
