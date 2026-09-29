class ModeloProtocelula:
    """
    Última etapa de Química Prebiótica de Fase 1.

    Representa un sistema protocelular:
    un compartimento que mantiene asociadas
    redes químicas y polímeros.

    Una protocélula de este modelo NO es todavía vida.

    No exigimos todavía:
    - replicación heredable
    - evolución darwiniana
    - genoma
    - metabolismo biológico completo

    Esos requisitos pertenecen a Abiogénesis.
    """

    def evaluar(
        self,
        planeta,
    ):
        # Logro histórico.
        if planeta.alcanzo_protocelula:
            return

        if not planeta.alcanzo_compartimentalizacion_prebiotica:
            return

        if not planeta.alcanzo_red_quimica_primitiva:
            return

        if not planeta.alcanzo_polimerizacion_prebiotica:
            return

        # La protocélula debe surgir mientras
        # todavía exista un entorno prebiótico activo.
        if not planeta.candidato_quimica_prebiotica:
            return

        tipo = self._determinar_tipo(planeta)

        if tipo is None:
            return

        planeta.alcanzo_protocelula = True

        planeta.tipo_protocelula = tipo

        planeta.etapa_quimica_historica = "protocelula"

    def _determinar_tipo(
        self,
        planeta,
    ):
        compartimento = planeta.tipo_compartimento_prebiotico

        polimerizacion = planeta.mecanismo_polimerizacion_prebiotica

        # Ruta mixta:
        # hielo + minerales + química geoquímica.
        if (
            compartimento == "hielo_y_minerales"
            and polimerizacion == "frio_y_geoquimica"
        ):
            return "protocelula_mixta"

        # Ruta dominada por ambientes fríos.
        if (
            compartimento == "microambientes_en_hielo"
            and polimerizacion == "ciclos_de_congelacion"
        ):
            return "protocelula_criogenica"

        # Ruta dominada por superficies minerales.
        if (
            compartimento == "poros_minerales"
            and polimerizacion == "superficies_geoquimicas"
        ):
            return "protocelula_geoquimica"

        return None
