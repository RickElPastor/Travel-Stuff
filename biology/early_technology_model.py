from biology.initial_language_model import ModeloLenguajeInicial
from biology.initial_tool_model import ModeloHerramientasIniciales


class ModeloTecnologiaTemprana:
    """Reconoce un método de soporte recuperado tras una escasez."""

    LINAJES_MINIMOS = 2  # Umbral de diseño, no medida de tecnología real.

    def __init__(self):
        self.herramientas = ModeloHerramientasIniciales()
        self.lenguaje = ModeloLenguajeInicial()

    def _usos_codificados(self, planeta):
        usos = self.herramientas.usos_actuales(planeta)
        codigos = self.lenguaje.repertorios_actuales(planeta)
        posibles = {}
        for especie, linajes in usos.items():
            if (len(linajes) >= self.LINAJES_MINIMOS
                    and "restos" in codigos.get(especie, {})):
                posibles[especie] = {
                    "linajes": list(linajes),
                    "codigo": codigos[especie]["restos"],
                }
        return posibles

    def tecnicas_actuales(self, planeta):
        return {
            especie: datos
            for especie, datos in self._usos_codificados(planeta).items()
            if especie in planeta.especies_con_tecnica_soporte
        }

    def evaluar(self, planeta):
        if not self.herramientas.restos_disponibles(planeta):
            precursores = self.herramientas.precursores
            candidatas = precursores.candidatas(planeta)
            for linaje in precursores.linajes_con_colonia(planeta):
                especie = planeta.clasificacion_especies_unicelulares[linaje][
                    "especie_id"
                ]
                codigos = planeta.codigos_senal_por_especie.get(especie, {})
                if (especie in candidatas
                        and especie in planeta.especies_con_soporte_organico
                        and "restos" in codigos
                        and "restos" in planeta.recursos_recordados_por_linaje.get(
                            linaje, []
                        )):
                    planeta.especies_soporte_con_escasez.add(especie)
        else:
            for especie in self._usos_codificados(planeta):
                if especie in planeta.especies_soporte_con_escasez:
                    planeta.especies_con_tecnica_soporte.add(especie)
