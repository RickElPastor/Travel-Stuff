class ModeloViabilidadProtocelular:
    """Condiciones actuales para mantener sistemas protocelulares.

    Regla conceptual del simulador, no una medida de supervivencia individual.
    Se evalúa después de la química normal y de los apoyos extraordinarios.
    """

    TIPOS_CONOCIDOS = (
        "protocelula_criogenica",
        "protocelula_geoquimica",
        "protocelula_mixta",
    )

    def evaluar(self, planeta):
        planeta.protocelula_viable_normal = False
        planeta.protocelula_viable = False
        planeta.estado_viabilidad_protocelular = "sin_protocelula"

        if not planeta.alcanzo_protocelula:
            return
        if planeta.tipo_protocelula not in self.TIPOS_CONOCIDOS:
            planeta.estado_viabilidad_protocelular = "tipo_no_modelado"
            return
        if not planeta.candidato_habitable_fase1:
            planeta.estado_viabilidad_protocelular = "sin_habitabilidad_actual"
            return
        if not planeta.tiene_ingredientes_prebioticos:
            planeta.estado_viabilidad_protocelular = "sin_ingredientes"
            return
        if not planeta.tiene_agua_condensada:
            planeta.estado_viabilidad_protocelular = "sin_agua_condensada"
            return

        energia_normal = planeta.candidato_quimica_prebiotica
        confinamiento_normal = self._tiene_confinamiento_normal(planeta)
        planeta.protocelula_viable_normal = energia_normal and confinamiento_normal

        # Solo se aceptan los apoyos calculados para la regla correspondiente.
        extraordinario = planeta.regimen_mundo == "extraordinario"
        energia_extra = (
            extraordinario
            and planeta.tipo_regla_extraordinaria == "energia_exotica"
            and 0.0 < planeta.energia_quimica_exotica <= 1.0
        )
        confinamiento_extra = (
            extraordinario
            and planeta.tipo_regla_extraordinaria == "anomalia_fisica"
            and 0.0 < planeta.confinamiento_anomalo <= 1.0
        )

        if not (energia_normal or energia_extra):
            planeta.estado_viabilidad_protocelular = "sin_energia"
            return
        if not (confinamiento_normal or confinamiento_extra):
            planeta.estado_viabilidad_protocelular = "sin_confinamiento"
            return

        planeta.protocelula_viable = True
        planeta.estado_viabilidad_protocelular = (
            "viable_normal"
            if planeta.protocelula_viable_normal
            else "viable_extraordinaria"
        )

    def _tiene_confinamiento_normal(self, planeta):
        # Conservamos los entornos de las rutas de formación existentes.
        if planeta.tipo_protocelula == "protocelula_criogenica":
            return planeta.estado_agua_preclima == "hielo"
        if planeta.tipo_protocelula == "protocelula_geoquimica":
            return (
                planeta.estado_agua_preclima == "liquida"
                and planeta.ruta_geoquimica_prebiotica
            )
        return (
            planeta.estado_agua_preclima == "hielo"
            and planeta.ruta_geoquimica_prebiotica
        )
