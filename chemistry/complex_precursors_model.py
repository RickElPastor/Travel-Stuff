class ModeloPrecursoresComplejos:
    """
    Tercera etapa histórica de complejidad química.

    Representa la aparición de una química
    prebiótica más rica a partir de:

    - orgánicos simples
    - mecanismos de concentración
    - un entorno químico favorable

    NO representa todavía:
    - RNA funcional
    - proteínas
    - polímeros largos
    - replicación
    - metabolismo
    - vida

    En Fase 1 no modelamos la cinética exacta.
    """

    def evaluar(
        self,
        planeta,
    ):
        if planeta.alcanzo_precursores_complejos:
            return

        if not planeta.alcanzo_organicos_simples:
            return

        if not planeta.alcanzo_concentracion_prebiotica:
            return

        if not planeta.candidato_quimica_prebiotica:
            return

        ruta = self._obtener_ruta(planeta)

        if ruta is None:
            return

        planeta.alcanzo_precursores_complejos = True

        planeta.ruta_precursores_complejos = ruta

        planeta.etapa_quimica_historica = "precursores_complejos"

    def _obtener_ruta(
        self,
        planeta,
    ):
        mecanismo = planeta.mecanismo_concentracion_prebiotica

        if mecanismo == "hielo_y_geoquimica":
            return "concentracion_mixta"

        if mecanismo == "concentracion_por_hielo":
            return "hielo"

        if mecanismo == "gradientes_geoquimicos":
            return "geoquimica"

        return None
