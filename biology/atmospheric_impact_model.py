class ModeloAporteAtmosfericoBiologico:
    """Proyección atmosférica simbólica separada de la física de Fase 1."""

    FRACCION_CO2_POR_PRODUCTOR = 0.01  # Parámetro de diseño.
    FRACCION_MAXIMA_CO2 = 0.05

    def evaluar(self, planeta):
        co2_fisico = planeta.presion_co2_preclima_bar
        planeta.presion_co2_con_vida_bar = co2_fisico
        planeta.aporte_o2_biologico_bar = (
            None if co2_fisico is None else 0.0
        )

        if (co2_fisico is None or co2_fisico <= 0
                or not planeta.vida_activa
                or planeta.unidades_productoras_activas <= 0):
            return

        fraccion = min(
            self.FRACCION_MAXIMA_CO2,
            planeta.unidades_productoras_activas * self.FRACCION_CO2_POR_PRODUCTOR,
        )
        co2_transformado = co2_fisico * fraccion
        planeta.presion_co2_con_vida_bar = co2_fisico - co2_transformado
        planeta.aporte_o2_biologico_bar = co2_transformado
