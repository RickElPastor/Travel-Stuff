from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia


class ModeloHerramientasIniciales:
    """Reconoce ensayos simbólicos con un soporte orgánico externo."""

    def __init__(self):
        self.precursores = ModeloPrecursoresInteligencia()

    def restos_disponibles(self, planeta):
        return max(
            planeta.restos_organicos_unidades,
            planeta.restos_observados_intervalo,
        ) > 0

    def usos_actuales(self, planeta):
        if not self.restos_disponibles(planeta):
            return {}
        candidatas = self.precursores.candidatas(planeta)
        usos = {}
        for linaje in self.precursores.linajes_con_colonia(planeta):
            especie = planeta.clasificacion_especies_unicelulares[linaje][
                "especie_id"
            ]
            if (especie in candidatas
                    and "restos" in planeta.recursos_recordados_por_linaje.get(
                        linaje, []
                    )):
                usos.setdefault(especie, []).append(linaje)
        return usos

    def evaluar(self, planeta):
        planeta.especies_con_soporte_organico.update(self.usos_actuales(planeta))
