import random


class ModeloColoniasCelulares:
    """Primeras agrupaciones simbólicas de unidades de un mismo linaje."""

    PROBABILIDAD_COHESION = 0.0625  # Parámetro de diseño, no tasa medida.

    def ambiente_apto(self, planeta):
        return (
            planeta.vida_activa
            and planeta.estado_agua_preclima == "liquida"
            and planeta.candidato_quimica_prebiotica
            and planeta.alcanzo_organicos_simples
        )

    def adquiere_cohesion(self, planeta, seed, nacimiento):
        if not self.ambiente_apto(planeta):
            return False
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:cohesion:{nacimiento}"
        )
        return generador.random() < self.PROBABILIDAD_COHESION

    def contar_colonias(self, planeta):
        if not self.ambiente_apto(planeta):
            return 0
        unidades_por_linaje = {}
        for linaje in planeta.linajes_unicelulares_vivos:
            if linaje in planeta.linajes_cohesivos:
                unidades_por_linaje[linaje] = unidades_por_linaje.get(linaje, 0) + 1
        return sum(unidades // 2 for unidades in unidades_por_linaje.values())

    def registrar_intervalo(self, planeta):
        if self.contar_colonias(planeta) > 0:
            planeta.alcanzo_colonia_multicelular = True

    def evaluar(self, planeta):
        planeta.colonias_multicelulares_activas = self.contar_colonias(planeta)
        if planeta.colonias_multicelulares_activas > 0:
            planeta.alcanzo_colonia_multicelular = True
