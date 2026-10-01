from biology.initial_communication_model import ModeloComunicacionInicial


class ModeloCulturaInicial:
    """Reconoce avisos recíprocos como práctica simbólica compartida."""

    def __init__(self):
        self.comunicacion = ModeloComunicacionInicial()

    def practicas_actuales(self, planeta):
        senales = self.comunicacion.senales_actuales(planeta)
        pares = {
            (senal["especie"], senal["origen"], senal["destino"],
             senal["recurso"])
            for senal in senales
        }
        practicas = {}
        for senal in senales:
            regreso = (senal["especie"], senal["destino"],
                       senal["origen"], senal["recurso"])
            if regreso not in pares:
                continue
            rutas = practicas.setdefault(senal["especie"], [])
            if senal["recurso"] not in rutas:
                rutas.append(senal["recurso"])
        return practicas

    def evaluar(self, planeta):
        for especie, recursos in self.practicas_actuales(planeta).items():
            historicas = planeta.rutas_culturales_por_especie.setdefault(
                especie, []
            )
            for recurso in recursos:
                if recurso not in historicas:
                    historicas.append(recurso)
