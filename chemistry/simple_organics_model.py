class ModeloOrganicosSimples:
    """
    Primera etapa histórica de complejidad química.

    Registra que un planeta con un entorno
    prebiótico previo alcanzó condiciones
    compatibles con síntesis abiótica de
    compuestos orgánicos simples.

    NO representa todavía:
    - proteínas
    - RNA
    - polímeros
    - metabolismo
    - vida
    """

    def evaluar(
        self,
        planeta,
    ):
        # Es un logro histórico.
        # Una vez alcanzado no se borra.
        if planeta.alcanzo_organicos_simples:
            return

        if not planeta.tuvo_entorno_prebiotico:
            return

        if not self._tiene_ingredientes(planeta):
            return

        ruta = self._obtener_ruta(planeta)

        if ruta is None:
            return

        planeta.alcanzo_organicos_simples = True

        planeta.ruta_organicos_simples = ruta

        planeta.etapa_quimica_historica = "organicos_simples"

    def _tiene_ingredientes(
        self,
        planeta,
    ):
        tiene_agua = (
            planeta.reservorio_h2o_total_tierra is not None
            and planeta.reservorio_h2o_total_tierra > 0
        )

        tiene_carbono = (
            planeta.reservorio_carbono_tierra is not None
            and planeta.reservorio_carbono_tierra > 0
        )

        tiene_nitrogeno = (
            planeta.reservorio_nitrogeno_tierra is not None
            and planeta.reservorio_nitrogeno_tierra > 0
        )

        return tiene_agua and tiene_carbono and tiene_nitrogeno

    def _obtener_ruta(
        self,
        planeta,
    ):
        uv = planeta.tuvo_ruta_uv_prebiotica

        geoquimica = planeta.tuvo_ruta_geoquimica_prebiotica

        if uv and geoquimica:
            return "uv_y_geoquimica"

        if uv:
            return "uv"

        if geoquimica:
            return "geoquimica"

        return None
