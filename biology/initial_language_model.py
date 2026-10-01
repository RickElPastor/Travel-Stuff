from biology.initial_culture_model import ModeloCulturaInicial


class ModeloLenguajeInicial:
    """Asocia códigos estables a dos o más rutas culturales de una especie."""

    RUTAS_MINIMAS = 2  # Umbral de diseño, no definición científica de lenguaje.

    def __init__(self):
        self.cultura = ModeloCulturaInicial()

    def repertorios_actuales(self, planeta):
        repertorios = {}
        for especie, rutas in self.cultura.practicas_actuales(planeta).items():
            codigos = planeta.codigos_senal_por_especie.get(especie, {})
            activos = {
                recurso: codigos[recurso]
                for recurso in rutas if recurso in codigos
            }
            if len(activos) >= self.RUTAS_MINIMAS:
                repertorios[especie] = activos
        return repertorios

    def evaluar(self, planeta):
        for especie, rutas in self.cultura.practicas_actuales(planeta).items():
            if len(rutas) < self.RUTAS_MINIMAS:
                continue
            codigos = planeta.codigos_senal_por_especie.setdefault(especie, {})
            for recurso in rutas:
                if recurso not in codigos:
                    codigos[recurso] = f"C{len(codigos) + 1}"
