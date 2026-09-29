class ModeloApoyoQuimicoExtraordinario:
    """Apoyos actuales de ficción, separados de la química física.

    Son índices de diseño entre 0 y 1, no tasas científicas.
    No crean ingredientes, logros químicos ni vida; tampoco consumen azar.
    """

    def evaluar(self, planeta):
        # Se recalculan: un apoyo actual puede desaparecer sin borrar historia.
        planeta.catalisis_arcana = 0.0
        planeta.confinamiento_anomalo = 0.0
        planeta.energia_quimica_exotica = 0.0

        if planeta.regimen_mundo != "extraordinario":
            return

        intensidad = planeta.intensidad_extraordinaria
        if not 0.0 < intensidad <= 1.0:
            return

        # Conservamos las condiciones materiales y la habitabilidad normales.
        if not planeta.tiene_ingredientes_prebioticos:
            return
        if not planeta.tiene_agua_condensada:
            return

        tipo = planeta.tipo_regla_extraordinaria
        if tipo == "arcano" and planeta.candidato_quimica_prebiotica:
            # Catálisis adicional para reacciones ya energéticamente posibles.
            planeta.catalisis_arcana = intensidad
        elif tipo == "anomalia_fisica" and planeta.candidato_quimica_prebiotica:
            # Confinamiento adicional cuando ya existen redes químicas.
            if planeta.alcanzo_red_quimica_primitiva:
                planeta.confinamiento_anomalo = intensidad
        elif tipo == "energia_exotica":
            # Fuente adicional, incluso sin UV o geoquímica activas.
            # No modifica las banderas de esas dos rutas físicas.
            planeta.energia_quimica_exotica = intensidad
