class ModeloReplicacionPrebiotica:
    """Modelo conceptual de copia de polímeros dentro de protocélulas.

    Aquí no se modelan secuencias, tasas ni fidelidad.
    Una ruta activa permite que el módulo siguiente modele copias.
    """

    MECANISMOS = {
        ("protocelula_criogenica", "ciclos_de_congelacion"):
            "copia_en_hielo",
        ("protocelula_geoquimica", "superficies_geoquimicas"):
            "copia_en_poros_minerales",
        ("protocelula_mixta", "frio_y_geoquimica"):
            "copia_mixta",
    }

    def evaluar(self, planeta):
        # El estado actual se recalcula; el logro histórico se conserva.
        planeta.replicacion_prebiotica_activa = False

        if not planeta.alcanzo_protocelula:
            return
        if not planeta.protocelula_viable:
            return
        if not planeta.alcanzo_precursores_complejos:
            return
        if not planeta.alcanzo_polimerizacion_prebiotica:
            return
        if not planeta.alcanzo_red_quimica_primitiva:
            return
        if not planeta.alcanzo_compartimentalizacion_prebiotica:
            return

        ruta = self.MECANISMOS.get((
            planeta.tipo_protocelula,
            planeta.mecanismo_polimerizacion_prebiotica,
        ))
        if ruta is None:
            return

        # El confinamiento anómalo puede sostener una protocélula, pero
        # la ruta de copia aún necesita su entorno físico correspondiente.
        if ruta == "copia_en_hielo" and planeta.estado_agua_preclima != "hielo":
            return
        if ruta == "copia_en_poros_minerales" and not (
            planeta.estado_agua_preclima == "liquida"
            and planeta.ruta_geoquimica_prebiotica
        ):
            return
        if ruta == "copia_mixta" and not (
            planeta.estado_agua_preclima == "hielo"
            and planeta.ruta_geoquimica_prebiotica
        ):
            return

        planeta.replicacion_prebiotica_activa = True
        if not planeta.alcanzo_replicacion_prebiotica:
            planeta.alcanzo_replicacion_prebiotica = True
            planeta.mecanismo_replicacion_prebiotica = ruta
