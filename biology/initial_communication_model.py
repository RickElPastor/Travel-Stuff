from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia
from biology.initial_tool_model import ModeloHerramientasIniciales


class ModeloComunicacionInicial:
    """Consulta avisos actuales de recursos entre colonias de una especie."""

    def __init__(self):
        self.precursores = ModeloPrecursoresInteligencia()
        self.herramientas = ModeloHerramientasIniciales()

    def senales_actuales(self, planeta):
        candidatas = self.precursores.candidatas(planeta)
        colonias = self.precursores.linajes_con_colonia(planeta)
        capacidades = {
            "luz": planeta.linajes_fotosinteticos,
            "restos": planeta.linajes_descomponedores,
            "presas": planeta.linajes_depredadores,
        }
        senales = []
        for especie, datos in candidatas.items():
            linajes = [
                linaje for linaje in colonias
                if planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
                == especie
            ]
            for origen in linajes:
                recordados = planeta.recursos_recordados_por_linaje.get(origen, [])
                for recurso in datos["recursos"]:
                    if (recurso not in capacidades or recurso not in recordados
                            or origen not in capacidades[recurso]):
                        continue
                    if recurso == "restos" and not self.herramientas.restos_disponibles(planeta):
                        continue
                    for destino in linajes:
                        if destino != origen:
                            senales.append({
                                "especie": especie,
                                "origen": origen,
                                "destino": destino,
                                "recurso": recurso,
                            })
        return senales

    def evaluar(self, planeta):
        for senal in self.senales_actuales(planeta):
            planeta.especies_con_senal_recurso.add(senal["especie"])
