from biology.species_model import ModeloEspeciesUnicelulares


class ModeloRadiacionesEvolutivas:
    """Reconoce ramificaciones cercanas de especies que siguen coexistiendo."""

    VENTANA_NACIMIENTOS = 12  # Umbral de diseño, no tiempo biológico medido.

    def __init__(self):
        self.especies = ModeloEspeciesUnicelulares()

    def registrar_intervalo(self, planeta, especies_antes):
        if not planeta.vida_activa:
            return []
        vivas = self.especies.especies_vivas(planeta)
        registradas = []
        for nueva in sorted(vivas - especies_antes):
            ancestro = self.especies.especie_progenitora(planeta, nueva)
            if ancestro is None or ancestro in planeta.ancestros_con_radiacion:
                continue
            hermanas = sorted(
                especie for especie in vivas
                if especie != nueva
                and self.especies.especie_progenitora(planeta, especie) == ancestro
                and abs(especie - nueva) <= self.VENTANA_NACIMIENTOS
            )
            if not hermanas:
                continue
            pareja = sorted((nueva, hermanas[0]))
            planeta.ancestros_con_radiacion.add(ancestro)
            planeta.especies_ultima_radiacion = pareja
            registradas.append((ancestro, pareja))
        return registradas
