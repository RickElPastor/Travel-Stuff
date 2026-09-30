import random


class ModeloMetabolismoInicial:
    """Primera relación simbólica entre vida unicelular y energía ambiental."""

    PROBABILIDAD_ADAPTACION_FOTOSINTETICA = 0.125  # Diseño, no tasa medida.

    def ambiente_fotosintetico(self, planeta):
        return (
            planeta.estado_agua_preclima == "liquida"
            and planeta.irradiancia_media_w_m2 is not None
            and planeta.irradiancia_media_w_m2 > 0
            and planeta.presion_co2_preclima_bar is not None
            and planeta.presion_co2_preclima_bar > 0
        )

    def adquiere_fotosintesis(self, planeta, seed, nacimiento):
        """Solo una variante en un entorno apto puede fijar esta capacidad."""
        if not self.ambiente_fotosintetico(planeta):
            return False
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:foto:{nacimiento}"
        )
        return generador.random() < self.PROBABILIDAD_ADAPTACION_FOTOSINTETICA

    def evaluar(self, planeta, anio_actual):
        fuentes = []
        if (planeta.irradiancia_media_w_m2 is not None
                and planeta.irradiancia_media_w_m2 > 0):
            fuentes.append("luz")
        if planeta.ruta_geoquimica_prebiotica:
            fuentes.append("geoquimica")
        if (planeta.candidato_quimica_prebiotica
                and planeta.alcanzo_organicos_simples):
            # Los orgánicos históricos solo se consideran disponibles si el
            # entorno prebiótico sigue siendo candidato en este paso.
            fuentes.append("organicos_ambientales")
        planeta.fuentes_energia_potenciales = fuentes

        planeta.ruta_metabolica_inicial = None
        planeta.estado_ecosistema = "sin_vida"
        planeta.unidades_productoras_activas = 0
        if not planeta.vida_activa or planeta.poblacion_unicelular == 0:
            return

        organicos = "organicos_ambientales" in fuentes
        if self.ambiente_fotosintetico(planeta):
            planeta.unidades_productoras_activas = sum(
                linaje in planeta.linajes_fotosinteticos
                for linaje in planeta.linajes_unicelulares_vivos
            )
        productores = planeta.unidades_productoras_activas > 0

        if organicos and productores:
            planeta.ruta_metabolica_inicial = "consumo_organicos_y_fotosintesis"
            planeta.estado_ecosistema = "microbiano_productor_y_consumidor"
        elif productores:
            planeta.ruta_metabolica_inicial = "fotosintesis"
            planeta.estado_ecosistema = "microbiano_productor"
        elif organicos:
            planeta.ruta_metabolica_inicial = "consumo_organicos"
            planeta.estado_ecosistema = "microbiano_organicos_ambientales"
        else:
            planeta.estado_ecosistema = "vida_sin_fuente_modelada"

        if planeta.ruta_metabolica_inicial and not planeta.alcanzo_metabolismo_inicial:
            planeta.alcanzo_metabolismo_inicial = True
            planeta.anio_metabolismo_inicial = anio_actual
        if productores and not planeta.alcanzo_fotosintesis:
            planeta.alcanzo_fotosintesis = True
