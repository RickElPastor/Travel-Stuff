class ModeloEntornoDisco:
    nombre = "Truncamiento binario aproximado"

    FACTOR_TRUNCAMIENTO = 0.30

    def obtener_radio_exterior_au(
        self,
        sistema,
    ):
        # Si no hay geometría binaria,
        # no imponemos truncamiento estelar.
        if (
            sistema.semieje_mayor_au is None
            or sistema.excentricidad is None
            or sistema.q_real is None
        ):
            return None

        periastro = sistema.obtener_periastro_au()

        if periastro is None:
            return None

        radio_exterior = self.FACTOR_TRUNCAMIENTO * periastro

        return max(
            0.0,
            radio_exterior,
        )

    def esta_truncado_por_companera(
        self,
        sistema,
    ):
        return self.obtener_radio_exterior_au(sistema) is not None
