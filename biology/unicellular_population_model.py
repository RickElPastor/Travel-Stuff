class ModeloPoblacionUnicelular:
    """Primer tamaño de población, expresado en unidades simbólicas."""

    INTERVALO_ANIOS = 1_000_000
    CAPACIDAD_INICIAL = 8

    def evaluar(self, planeta, anio_actual):
        if not planeta.vida_activa:
            planeta.poblacion_unicelular = 0
            planeta.proximo_crecimiento_unicelular_anio = None
            return

        if planeta.poblacion_unicelular == 0:
            planeta.poblacion_unicelular = 1
            planeta.proximo_crecimiento_unicelular_anio = (
                anio_actual + self.INTERVALO_ANIOS
            )
            return

        proximo = planeta.proximo_crecimiento_unicelular_anio
        if proximo is None:
            proximo = anio_actual + self.INTERVALO_ANIOS
        if anio_actual < proximo:
            planeta.proximo_crecimiento_unicelular_anio = proximo
            return

        intervalos = (anio_actual - proximo) // self.INTERVALO_ANIOS + 1
        planeta.poblacion_unicelular = min(
            self.CAPACIDAD_INICIAL,
            planeta.poblacion_unicelular + intervalos,
        )
        planeta.proximo_crecimiento_unicelular_anio = (
            proximo + intervalos * self.INTERVALO_ANIOS
        )
