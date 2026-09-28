class ModeloCandidatoTerrestre:
    """
    Primer filtro físico de habitabilidad.

    Un candidato terrestre debe:

    - estar dentro de la zona habitable radiativa
    - no haber entrado en runaway gaseoso
    - no conservar H/He primordial
    - tener composición rocosa o mixta
    - tener radio <= 1.6 R_tierra

    Esto NO significa que sea habitable.
    """

    RADIO_MAX_TERRESTRE_RT = 1.6

    COMPOSICIONES_ADMITIDAS = {
        "rocosa",
        "mixta",
    }

    def evaluar(
        self,
        planeta,
    ):
        planeta.candidato_terrestre_hz = False

        if not planeta.en_zona_habitable_radiativa:
            return

        if planeta.radio_tierra is None:
            return

        if planeta.entro_runaway:
            return

        if planeta.masa_gas_tierra > 0:
            return

        if planeta.composicion_inicial not in self.COMPOSICIONES_ADMITIDAS:
            return

        if planeta.radio_tierra > self.RADIO_MAX_TERRESTRE_RT:
            return

        planeta.candidato_terrestre_hz = True
