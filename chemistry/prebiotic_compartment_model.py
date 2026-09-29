class ModeloCompartimentalizacionPrebiotica:
    """
    Sexta etapa histórica de complejidad química.

    Representa microambientes capaces de mantener
    juntas moléculas, polímeros y redes químicas.

    Posibles entornos de Fase 1:
    - interfaces de hielo + minerales
    - microambientes en hielo
    - poros minerales

    NO representa todavía:
    - una célula
    - metabolismo biológico
    - replicación
    - vida
    """

    def evaluar(
        self,
        planeta,
    ):
        # Logro histórico:
        # una vez alcanzado no se pierde.
        if planeta.alcanzo_compartimentalizacion_prebiotica:
            return

        if not planeta.alcanzo_red_quimica_primitiva:
            return

        # Para crear nuevos compartimentos seguimos
        # necesitando condiciones prebióticas activas.
        if not planeta.candidato_quimica_prebiotica:
            return

        if not planeta.tiene_agua_condensada:
            return

        tipo = self._obtener_tipo_compartimento(planeta)

        if tipo is None:
            return

        planeta.alcanzo_compartimentalizacion_prebiotica = True

        planeta.tipo_compartimento_prebiotico = tipo

        planeta.etapa_quimica_historica = "compartimentalizacion_prebiotica"

    def _obtener_tipo_compartimento(
        self,
        planeta,
    ):
        estado_agua = planeta.estado_agua_preclima

        geoquimica = planeta.ruta_geoquimica_prebiotica

        if estado_agua == "hielo" and geoquimica:
            return "hielo_y_minerales"

        if estado_agua == "hielo":
            return "microambientes_en_hielo"

        if estado_agua == "liquida" and geoquimica:
            return "poros_minerales"

        return None
