import random


class ModeloDepredacion:
    """Una captura puede decidir la presa del recambio biológico habitual."""

    PROBABILIDAD_CAPACIDAD = 0.0625  # Diseño, no tasa medida.
    PROBABILIDAD_ENCUENTRO = 0.5  # Diseño, no tasa medida.

    def adquiere_capacidad(self, planeta, seed, nacimiento):
        if not planeta.vida_activa or planeta.poblacion_unicelular < 2:
            return False
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:predador:{nacimiento}"
        )
        return generador.random() < self.PROBABILIDAD_CAPACIDAD

    def elegir_captura(self, planeta, seed, nacimiento, unidades_anteriores):
        if not planeta.vida_activa or unidades_anteriores < 2:
            return None
        linajes = planeta.linajes_unicelulares_vivos
        especies = planeta.clasificacion_especies_unicelulares
        parejas = []
        for linaje in linajes:
            if linaje not in planeta.linajes_depredadores:
                continue
            especie_predadora = especies[linaje]["especie_id"]
            for indice in range(unidades_anteriores):
                especie_presa = especies[linajes[indice]]["especie_id"]
                if especie_presa != especie_predadora:
                    parejas.append((especie_predadora, especie_presa, indice))
        if not parejas:
            return None
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:captura:{nacimiento}"
        )
        if generador.random() >= self.PROBABILIDAD_ENCUENTRO:
            return None
        return generador.choice(parejas)

    def registrar_captura(self, planeta, captura):
        especie_predadora, especie_presa, _ = captura
        planeta.capturas_depredacion += 1
        planeta.ultima_especie_predadora_id = especie_predadora
        planeta.ultima_especie_presa_id = especie_presa
