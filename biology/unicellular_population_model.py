class ModeloPoblacionUnicelular:
    """Supervivencia y reproducción en unidades simbólicas, sin azar."""

    INTERVALO_ANIOS = 1_000_000
    CAPACIDAD_INICIAL = 8

    def evaluar(self, planeta, anio_actual):
        if not planeta.vida_activa:
            planeta.muertes_unicelulares += planeta.poblacion_unicelular
            planeta.poblacion_unicelular = 0
            planeta.proximo_crecimiento_unicelular_anio = None
            return

        if planeta.poblacion_unicelular == 0:
            planeta.poblacion_unicelular = 1
            planeta.nacimientos_unicelulares += 1
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
        crecimiento = min(
            self.CAPACIDAD_INICIAL - planeta.poblacion_unicelular,
            intervalos,
        )
        # En cada intervalo sobrevive la población salvo una unidad si hay
        # al menos dos. Un nacimiento la reemplaza; otro permite crecer.
        muertes = intervalos
        if planeta.poblacion_unicelular == 1:
            muertes -= 1  # En el primer intervalo no muere la fundadora.
        planeta.muertes_unicelulares += muertes
        planeta.nacimientos_unicelulares += muertes + crecimiento
        planeta.poblacion_unicelular = min(
            self.CAPACIDAD_INICIAL,
            planeta.poblacion_unicelular + crecimiento,
        )
        planeta.proximo_crecimiento_unicelular_anio = (
            proximo + intervalos * self.INTERVALO_ANIOS
        )
