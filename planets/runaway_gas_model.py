from planets.gas_accretion_model import (
    ModeloAcrecionGas,
)


class ModeloRunawayGas:
    """
    Fase rápida de acreción gaseosa.

    Usa el tiempo de Kelvin-Helmholtz:

        tau_KH = 1e9 * M^-3 años

    y limita el crecimiento por:

    - gas restante del disco
    - límite superior del módulo planetario
    """

    KH_NORMALIZACION_ANIOS = 1.0e9

    MASA_JUPITER_TIERRA = 317.83

    MASA_MAX_PLANETA_TIERRA = 13.0 * MASA_JUPITER_TIERRA

    def aplicar_runaway(
        self,
        disco,
        planetas,
    ):
        if disco.masa_gas_no_capturada_tierra is None:
            return

        gas_disponible = disco.masa_gas_no_capturada_tierra

        if gas_disponible <= 0:
            return

        solicitudes = []

        for planeta in planetas:
            if not planeta.candidato_runaway:
                continue

            if planeta.tiempo_nucleo_myr is None:
                continue

            if disco.vida_gas_myr is None:
                continue

            masa_nucleo = planeta.masa_nucleo_acrecion_tierra

            if masa_nucleo is None or masa_nucleo <= 0:
                continue

            tiempo_disponible_total = disco.vida_gas_myr - planeta.tiempo_nucleo_myr

            tiempo_hasta_runaway = self._calcular_tiempo_hasta_runaway_myr(masa_nucleo)

            tiempo_runaway = tiempo_disponible_total - tiempo_hasta_runaway

            if tiempo_runaway <= 0:
                continue

            masa_inicial = planeta.masa_tierra

            capacidad_maxima = max(
                0.0,
                self.MASA_MAX_PLANETA_TIERRA - masa_inicial,
            )

            if capacidad_maxima <= 0:
                continue

            masa_solicitada = self._calcular_crecimiento_kh(
                masa_inicial,
                tiempo_runaway,
                capacidad_maxima,
            )

            if masa_solicitada <= 0:
                continue

            solicitudes.append(
                (
                    planeta,
                    masa_solicitada,
                    tiempo_runaway,
                )
            )

        masa_solicitada_total = sum(solicitud[1] for solicitud in solicitudes)

        if masa_solicitada_total <= 0:
            return

        factor_disponibilidad = min(
            1.0,
            gas_disponible / masa_solicitada_total,
        )

        masa_runaway_total = 0.0

        for (
            planeta,
            masa_solicitada,
            tiempo_runaway,
        ) in solicitudes:
            masa_capturada = masa_solicitada * factor_disponibilidad

            planeta.masa_gas_tierra += masa_capturada

            planeta.masa_tierra += masa_capturada

            planeta.masa_gas_runaway_tierra = masa_capturada

            planeta.tiempo_runaway_myr = tiempo_runaway

            planeta.entro_runaway = masa_capturada > 0

            planeta.gcr_envoltura = planeta.masa_gas_tierra / planeta.masa_solida_tierra

            masa_runaway_total += masa_capturada

        disco.masa_gas_runaway_capturada_tierra = masa_runaway_total

        disco.masa_gas_capturada_tierra += masa_runaway_total

        disco.masa_gas_no_capturada_tierra = max(
            0.0,
            gas_disponible - masa_runaway_total,
        )

    def _calcular_tiempo_hasta_runaway_myr(
        self,
        masa_nucleo,
    ):
        factor_masa = (masa_nucleo / 5.0) ** 1.7

        denominador = ModeloAcrecionGas.GCR_BASE * factor_masa

        if denominador <= 0:
            return float("inf")

        relacion = ModeloAcrecionGas.GCR_RUNAWAY / denominador

        return relacion ** (1.0 / 0.4)

    def _calcular_crecimiento_kh(
        self,
        masa_inicial,
        tiempo_runaway_myr,
        capacidad_maxima,
    ):
        tiempo_anios = tiempo_runaway_myr * 1_000_000.0

        termino = masa_inicial**-3.0 - (
            3.0 * tiempo_anios / self.KH_NORMALIZACION_ANIOS
        )

        # Si llega aquí, la solución matemática
        # entra formalmente en runaway divergente.
        # El crecimiento real queda entonces
        # limitado por el suministro del disco.
        if termino <= 0:
            return capacidad_maxima

        masa_final = termino ** (-1.0 / 3.0)

        masa_adicional = max(
            0.0,
            masa_final - masa_inicial,
        )

        return min(
            masa_adicional,
            capacidad_maxima,
        )
