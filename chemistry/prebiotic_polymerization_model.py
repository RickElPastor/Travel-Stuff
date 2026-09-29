class ModeloPolimerizacionPrebiotica:
    """
    Cuarta etapa histórica de complejidad química.

    Representa la formación de oligómeros o
    cadenas químicas cortas a partir de
    precursores complejos.

    Rutas de Fase 1:
    - ciclos asociados a hielo/congelación
    - superficies y gradientes geoquímicos
    - combinación de ambos

    NO representa todavía:
    - RNA funcional
    - proteínas funcionales
    - replicación
    - metabolismo
    - vida
    """

    def evaluar(
        self,
        planeta,
    ):
        # Es un logro histórico.
        if planeta.alcanzo_polimerizacion_prebiotica:
            return

        if not planeta.alcanzo_precursores_complejos:
            return

        # Para avanzar una etapa nueva seguimos
        # exigiendo que el planeta tenga actualmente
        # un entorno prebiótico funcional.
        if not planeta.candidato_quimica_prebiotica:
            return

        mecanismo = self._obtener_mecanismo(planeta)

        if mecanismo is None:
            return

        planeta.alcanzo_polimerizacion_prebiotica = True

        planeta.mecanismo_polimerizacion_prebiotica = mecanismo

        planeta.etapa_quimica_historica = "oligomeros_prebioticos"

    def _obtener_mecanismo(
        self,
        planeta,
    ):
        mecanismo_concentracion = planeta.mecanismo_concentracion_prebiotica

        if mecanismo_concentracion == "hielo_y_geoquimica":
            return "frio_y_geoquimica"

        if mecanismo_concentracion == "concentracion_por_hielo":
            return "ciclos_de_congelacion"

        if mecanismo_concentracion == "gradientes_geoquimicos":
            return "superficies_geoquimicas"

        return None
