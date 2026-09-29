class ModeloRedQuimicaPrimitiva:
    """
    Quinta etapa histórica de complejidad química.

    Representa la aparición de conjuntos de
    reacciones químicas acopladas.

    Estas redes pueden incluir ciclos y
    realimentación química rudimentaria.

    NO representan todavía:
    - metabolismo biológico
    - replicación genética
    - células
    - vida

    Es una aproximación conceptual de Fase 1.
    """

    def evaluar(
        self,
        planeta,
    ):
        # Logro histórico.
        # Una vez alcanzado no se elimina.
        if planeta.alcanzo_red_quimica_primitiva:
            return

        if not planeta.alcanzo_polimerizacion_prebiotica:
            return

        # Para formar una red nueva todavía
        # necesitamos condiciones prebióticas activas.
        if not planeta.candidato_quimica_prebiotica:
            return

        tipo_red = self._obtener_tipo_red(planeta)

        if tipo_red is None:
            return

        planeta.alcanzo_red_quimica_primitiva = True

        planeta.tipo_red_quimica_primitiva = tipo_red

        planeta.etapa_quimica_historica = "red_quimica_primitiva"

    def _obtener_tipo_red(
        self,
        planeta,
    ):
        mecanismo = planeta.mecanismo_polimerizacion_prebiotica

        if mecanismo == "frio_y_geoquimica":
            return "red_mixta"

        if mecanismo == "ciclos_de_congelacion":
            return "red_ciclica_frio"

        if mecanismo == "superficies_geoquimicas":
            return "red_geoquimica"

        return None
