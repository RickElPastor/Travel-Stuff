class ModeloAcrecionGas:
    """
    Captura inicial de envolturas gaseosas.

    Usa una aproximación del GCR de atmósferas
    polvorientas de Lee & Chiang.

    Esta etapa se detiene en el comienzo del
    runaway. El runaway se modelará aparte.
    """

    GCR_BASE = 0.16

    GCR_RUNAWAY = 0.48

    def aplicar_acrecion(
        self,
        disco,
        planetas,
    ):
        if (
            disco.masa_gas_referencia_tierra is None
            or disco.masa_gas_referencia_tierra <= 0
        ):
            return

        solicitudes = []

        for planeta in planetas:
            if not planeta.gas_disponible_al_formarse:
                continue

            if planeta.tiempo_nucleo_myr is None:
                continue

            if disco.vida_gas_myr is None:
                continue

            tiempo_disponible = disco.vida_gas_myr - planeta.tiempo_nucleo_myr

            if tiempo_disponible <= 0:
                continue

            masa_nucleo = planeta.masa_nucleo_acrecion_tierra

            if masa_nucleo is None or masa_nucleo <= 0:
                continue

            gcr_estimado = (
                self.GCR_BASE * tiempo_disponible**0.4 * (masa_nucleo / 5.0) ** 1.7
            )

            gcr_pre_runaway = min(
                gcr_estimado,
                self.GCR_RUNAWAY,
            )

            masa_gas_solicitada = masa_nucleo * gcr_pre_runaway

            solicitudes.append(
                (
                    planeta,
                    masa_gas_solicitada,
                    gcr_estimado,
                    tiempo_disponible,
                )
            )

        masa_solicitada_total = sum(solicitud[1] for solicitud in solicitudes)

        if masa_solicitada_total <= 0:
            return

        presupuesto_gas = disco.masa_gas_referencia_tierra

        factor_disponibilidad = min(
            1.0,
            presupuesto_gas / masa_solicitada_total,
        )

        masa_capturada_total = 0.0

        for (
            planeta,
            masa_gas_solicitada,
            gcr_estimado,
            tiempo_disponible,
        ) in solicitudes:
            masa_gas = masa_gas_solicitada * factor_disponibilidad

            planeta.masa_gas_tierra = masa_gas

            planeta.masa_tierra = planeta.masa_solida_tierra + planeta.masa_gas_tierra

            planeta.gcr_envoltura = planeta.masa_gas_tierra / planeta.masa_solida_tierra

            planeta.tiempo_acrecion_gas_myr = tiempo_disponible

            planeta.candidato_runaway = (
                gcr_estimado >= self.GCR_RUNAWAY
                and planeta.gcr_envoltura >= self.GCR_RUNAWAY * 0.999
            )

            masa_capturada_total += masa_gas

        disco.masa_gas_capturada_tierra = masa_capturada_total

        disco.masa_gas_no_capturada_tierra = max(
            0.0,
            disco.masa_gas_referencia_tierra - masa_capturada_total,
        )
