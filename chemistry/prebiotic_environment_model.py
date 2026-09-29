class ModeloEntornoPrebiotico:
    """
    Primera capa de química prebiótica.

    No crea vida ni biomoléculas.

    Evalúa si un candidato habitable posee:

    - agua
    - carbono
    - nitrógeno
    - alguna fuente energética plausible

    Rutas de energía de Fase 1:

    - fot química UV
    - geoquímica
    """

    TEMPERATURA_UV_QUIESCENTE_K = 4400.0

    def evaluar(
        self,
        planeta,
        estrella,
    ):
        self.limpiar(planeta)

        if not planeta.candidato_habitable_fase1:
            planeta.estado_quimica_prebiotica = "no_habitable_fase1"
            return

        tiene_agua = (
            planeta.masa_agua_superficial_total_tierra is not None
            and planeta.masa_agua_superficial_total_tierra > 0
        )

        tiene_carbono = (
            planeta.reservorio_carbono_tierra is not None
            and planeta.reservorio_carbono_tierra > 0
        )

        tiene_nitrogeno = (
            planeta.reservorio_nitrogeno_tierra is not None
            and planeta.reservorio_nitrogeno_tierra > 0
        )

        planeta.tiene_ingredientes_prebioticos = (
            tiene_agua and tiene_carbono and tiene_nitrogeno
        )

        if not planeta.tiene_ingredientes_prebioticos:
            planeta.estado_quimica_prebiotica = "ingredientes_insuficientes"
            return

        if (
            estrella is not None
            and estrella.viva
            and estrella.temperatura_efectiva is not None
        ):
            planeta.ruta_uv_prebiotica = (
                estrella.temperatura_efectiva >= self.TEMPERATURA_UV_QUIESCENTE_K
            )

        planeta.ruta_geoquimica_prebiotica = (
            planeta.geologicamente_activo and planeta.tiene_agua_condensada
        )

        if planeta.ruta_uv_prebiotica and planeta.ruta_geoquimica_prebiotica:
            planeta.estado_quimica_prebiotica = "uv_y_geoquimica"

        elif planeta.ruta_uv_prebiotica:
            planeta.estado_quimica_prebiotica = "fotoprebiotica"

        elif planeta.ruta_geoquimica_prebiotica:
            planeta.estado_quimica_prebiotica = "geoquimica"

        else:
            planeta.estado_quimica_prebiotica = "sin_fuente_energetica_modelada"
            return

        planeta.candidato_quimica_prebiotica = True

        self._registrar_historial(planeta)

    def _registrar_historial(
        self,
        planeta,
    ):
        planeta.tuvo_entorno_prebiotico = True

        if planeta.ruta_uv_prebiotica:
            planeta.tuvo_ruta_uv_prebiotica = True

        if planeta.ruta_geoquimica_prebiotica:
            planeta.tuvo_ruta_geoquimica_prebiotica = True

    def limpiar(
        self,
        planeta,
    ):
        planeta.tiene_ingredientes_prebioticos = False
        planeta.ruta_uv_prebiotica = False
        planeta.ruta_geoquimica_prebiotica = False

        planeta.candidato_quimica_prebiotica = False

        planeta.estado_quimica_prebiotica = "no_evaluado"
