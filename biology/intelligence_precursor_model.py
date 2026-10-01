from biology.colony_model import ModeloColoniasCelulares
from biology.niche_model import ModeloNichosEcologicos


class ModeloPrecursoresInteligencia:
    """Consulta especies con colonias activas y varios recursos disponibles."""

    RECURSOS_MINIMOS = 2  # Umbral de diseño; no mide inteligencia real.

    def __init__(self):
        self.colonias = ModeloColoniasCelulares()
        self.nichos = ModeloNichosEcologicos()

    def linajes_con_colonia(self, planeta):
        if not self.colonias.ambiente_apto(planeta):
            return {}
        unidades_cohesivas = {}
        for linaje in planeta.linajes_unicelulares_vivos:
            if linaje in planeta.linajes_cohesivos:
                unidades_cohesivas[linaje] = unidades_cohesivas.get(linaje, 0) + 1
        return {
            linaje: unidades // 2
            for linaje, unidades in sorted(unidades_cohesivas.items())
            if unidades >= 2
        }

    def candidatas(self, planeta):
        ocupacion = self.nichos.ocupacion_por_especie(planeta)
        colonias_por_especie = {}
        for linaje, colonias in self.linajes_con_colonia(planeta).items():
            especie = planeta.clasificacion_especies_unicelulares[linaje][
                "especie_id"
            ]
            colonias_por_especie[especie] = (
                colonias_por_especie.get(especie, 0) + colonias
            )

        candidatas = {}
        for especie in sorted(colonias_por_especie):
            recursos = [
                nombre for nombre in self.nichos.RECURSOS
                if ocupacion[especie][nombre] > 0
            ]
            if len(recursos) >= self.RECURSOS_MINIMOS:
                candidatas[especie] = {
                    "colonias": colonias_por_especie[especie],
                    "recursos": recursos,
                }
        return candidatas
