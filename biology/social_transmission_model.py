from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia


class ModeloTransmisionSocial:
    """Comparte rutas recordadas entre colonias de una misma especie."""

    def __init__(self):
        self.precursores = ModeloPrecursoresInteligencia()

    def evaluar(self, planeta):
        candidatas = self.precursores.candidatas(planeta)
        colonias = self.precursores.linajes_con_colonia(planeta)
        for especie in candidatas:
            linajes = [
                linaje for linaje in colonias
                if planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
                == especie
            ]
            if len(linajes) < 2:
                continue
            recuerdos_previos = {
                linaje: list(planeta.recursos_recordados_por_linaje.get(linaje, []))
                for linaje in linajes
            }
            for origen in linajes:
                for destino in linajes:
                    if origen == destino:
                        continue
                    conocidas = planeta.recursos_recordados_por_linaje.setdefault(
                        destino, []
                    )
                    for recurso in recuerdos_previos[origen]:
                        if recurso not in conocidas:
                            conocidas.append(recurso)
                            planeta.transmisiones_sociales += 1
