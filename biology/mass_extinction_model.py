from biology.species_model import ModeloEspeciesUnicelulares


class ModeloExtincionesMasivas:
    """Registra pérdidas simultáneas de varias especies en un planeta."""

    ESPECIES_MINIMAS = 2  # Umbral operativo de diseño, no definición científica.

    def __init__(self):
        self.especies = ModeloEspeciesUnicelulares()

    def registrar(self, planeta, especies_antes, anio_actual):
        if (planeta.vida_activa or planeta.poblacion_unicelular != 0
                or len(especies_antes) < self.ESPECIES_MINIMAS
                or planeta.anio_ultima_extincion_masiva == anio_actual):
            return []

        perdidas = sorted(especies_antes - self.especies.especies_vivas(planeta))
        if len(perdidas) < self.ESPECIES_MINIMAS:
            return []
        planeta.extinciones_masivas_locales += 1
        planeta.anio_ultima_extincion_masiva = anio_actual
        planeta.especies_ultima_extincion_masiva = perdidas
        return perdidas
