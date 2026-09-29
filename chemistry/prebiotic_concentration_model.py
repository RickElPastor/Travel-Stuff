class ModeloConcentracionPrebiotica:
    """
    Segunda etapa histórica de complejidad química.

    Después de existir orgánicos simples,
    buscamos ambientes capaces de concentrarlos.

    Rutas de Fase 1:
    - concentración por congelación
    - gradientes geoquímicos/hidrotermales

    Todavía NO representa:
    - polímeros
    - RNA
    - proteínas
    - protocélulas
    - vida
    """

    def evaluar(
        self,
        planeta,
    ):
        # Logro histórico:
        # una vez alcanzado no se elimina.
        if planeta.alcanzo_concentracion_prebiotica:
            return

        if not planeta.alcanzo_organicos_simples:
            return

        # Para alcanzar esta nueva etapa exigimos
        # que exista nuevamente un entorno
        # prebiótico activo.
        if not planeta.candidato_quimica_prebiotica:
            return

        mecanismo = self._obtener_mecanismo(planeta)

        if mecanismo is None:
            return

        planeta.alcanzo_concentracion_prebiotica = True

        planeta.mecanismo_concentracion_prebiotica = mecanismo

        planeta.etapa_quimica_historica = "precursores_concentrados"

    def _obtener_mecanismo(
        self,
        planeta,
    ):
        estado_agua = planeta.estado_agua_preclima

        # El congelamiento puede excluir solutos
        # del hielo y concentrarlos en pequeñas
        # regiones de fase líquida.
        if estado_agua == "hielo" and planeta.tiene_agua_condensada:
            if planeta.ruta_geoquimica_prebiotica:
                return "hielo_y_geoquimica"

            return "concentracion_por_hielo"

        # Para agua no congelada usamos por ahora
        # los gradientes geoquímicos que ya
        # modelamos.
        if estado_agua == "liquida" and planeta.ruta_geoquimica_prebiotica:
            return "gradientes_geoquimicos"

        return None
