class ModeloHabitabilidadFinal:
    """
    Clasificación final de habitabilidad de Fase 1.

    NO afirma que exista vida.

    Identifica mundos que mantienen una combinación
    compatible con habitabilidad superficial según
    los filtros que ya hemos construido.
    """

    PCO2_MAX_ANCLAS = (
        (2300.0, 19.74),
        (3800.0, 12.24),
        (5200.0, 9.07),
        (6000.0, 7.92),
        (7600.0, 6.32),
    )

    def evaluar(
        self,
        planeta,
        estrella,
    ):
        self.limpiar(planeta)

        if not planeta.en_zona_habitable_radiativa:
            planeta.estado_habitabilidad_fase1 = "fuera_hz"
            return

        if not planeta.candidato_terrestre_hz:
            planeta.estado_habitabilidad_fase1 = "no_terrestre"
            return

        if not planeta.retencion_atmosferica_aprox:
            planeta.estado_habitabilidad_fase1 = "pierde_atmosfera"
            return

        if not planeta.tiene_atmosfera_secundaria:
            planeta.estado_habitabilidad_fase1 = "sin_atmosfera_secundaria"
            return

        if estrella is None:
            planeta.estado_habitabilidad_fase1 = "sin_estrella_activa"
            return

        if estrella.temperatura_efectiva is None:
            planeta.estado_habitabilidad_fase1 = "sin_datos_estelares"
            return

        agua_total = planeta.masa_agua_superficial_total_tierra

        if agua_total is None or agua_total <= 0:
            planeta.estado_habitabilidad_fase1 = "seco"
            return

        presion_co2 = planeta.presion_co2_preclima_bar

        if presion_co2 is None:
            planeta.estado_habitabilidad_fase1 = "sin_datos_co2"
            return

        pco2_max = self._interpolar_pco2_max(estrella.temperatura_efectiva)

        planeta.pco2_max_greenhouse_bar = pco2_max

        planeta.co2_dentro_max_greenhouse = presion_co2 <= pco2_max

        if not planeta.co2_dentro_max_greenhouse:
            planeta.estado_habitabilidad_fase1 = "co2_excesivo"
            return

        if not planeta.geologicamente_activo:
            planeta.estado_habitabilidad_fase1 = "geologia_inactiva"
            return

        if planeta.estado_agua_preclima == "vapor":
            planeta.estado_habitabilidad_fase1 = "agua_en_vapor"
            return

        planeta.candidato_habitable_fase1 = True

        if planeta.estado_agua_preclima == "liquida":
            planeta.estado_habitabilidad_fase1 = "candidato_temperado"

        elif planeta.estado_agua_preclima == "hielo":
            planeta.estado_habitabilidad_fase1 = "candidato_glaciado"

        else:
            planeta.estado_habitabilidad_fase1 = "candidato_habitable"

    def _interpolar_pco2_max(
        self,
        temperatura,
    ):
        puntos = self.PCO2_MAX_ANCLAS

        if temperatura <= puntos[0][0]:
            return puntos[0][1]

        if temperatura >= puntos[-1][0]:
            return puntos[-1][1]

        for indice in range(len(puntos) - 1):
            temperatura_1, presion_1 = puntos[indice]

            temperatura_2, presion_2 = puntos[indice + 1]

            if temperatura_1 <= temperatura <= temperatura_2:
                fraccion = (temperatura - temperatura_1) / (
                    temperatura_2 - temperatura_1
                )

                return presion_1 + fraccion * (presion_2 - presion_1)

        return puntos[-1][1]

    def limpiar(
        self,
        planeta,
    ):
        planeta.pco2_max_greenhouse_bar = None

        planeta.co2_dentro_max_greenhouse = False

        planeta.candidato_habitable_fase1 = False

        planeta.estado_habitabilidad_fase1 = "no_evaluado"
