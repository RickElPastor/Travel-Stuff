class ModeloZonaHabitable:
    """
    Zona habitable radiativa de Kopparapu.

    Primera implementación:
    - zona conservadora
    - planeta terrestre de referencia de 1 M_tierra
    - estrellas entre 2600 K y 7200 K

    Esto NO determina habitabilidad real.
    Solo indica compatibilidad radiativa.
    """

    TEMPERATURA_MIN_K = 2600.0
    TEMPERATURA_MAX_K = 7200.0

    TEMPERATURA_REFERENCIA_K = 5780.0

    # Runaway greenhouse, 1 M_tierra
    RUNAWAY = (
        1.107,
        1.332e-4,
        1.580e-8,
        -8.308e-12,
        -1.931e-15,
    )

    # Maximum greenhouse
    MAX_GREENHOUSE = (
        0.356,
        6.171e-5,
        1.698e-9,
        -3.198e-12,
        -5.5e-16,
    )

    def evaluar(
        self,
        planeta,
        estrella,
    ):
        self.limpiar(planeta)

        if estrella is None:
            return

        if not estrella.viva:
            return

        if estrella.temperatura_efectiva is None:
            return

        if planeta.flujo_estelar_tierra is None:
            return

        temperatura = estrella.temperatura_efectiva

        if not (self.TEMPERATURA_MIN_K <= temperatura <= self.TEMPERATURA_MAX_K):
            return

        flujo_interior = self._calcular_limite(
            temperatura,
            self.RUNAWAY,
        )

        flujo_exterior = self._calcular_limite(
            temperatura,
            self.MAX_GREENHOUSE,
        )

        flujo_planeta = planeta.flujo_estelar_tierra

        planeta.hz_flujo_interior = flujo_interior

        planeta.hz_flujo_exterior = flujo_exterior

        planeta.en_zona_habitable_radiativa = (
            flujo_exterior <= flujo_planeta <= flujo_interior
        )

    def limpiar(
        self,
        planeta,
    ):
        planeta.hz_flujo_interior = None
        planeta.hz_flujo_exterior = None

        planeta.en_zona_habitable_radiativa = False

    def _calcular_limite(
        self,
        temperatura_efectiva,
        coeficientes,
    ):
        (
            seff_sol,
            a,
            b,
            c,
            d,
        ) = coeficientes

        t = temperatura_efectiva - self.TEMPERATURA_REFERENCIA_K

        return seff_sol + a * t + b * t**2 + c * t**3 + d * t**4
