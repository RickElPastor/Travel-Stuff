class ModeloPrimeraVida:
    """Criterio operativo de primera vida del simulador.

    Exige una línea activa que ya copió un patrón, produjo una variante
    y sometió esa variante a selección. Es una definición de diseño,
    no una prueba científica de que existió vida en ese planeta.
    """

    COPIAS_MINIMAS_LINEA = 3

    def evaluar(self, planeta, anio_actual):
        planeta.vida_activa = False

        if not planeta.protocelula_viable:
            return
        if not planeta.replicacion_prebiotica_activa:
            return
        if planeta.patron_copia not in (0, 1, 2):
            return
        if planeta.copias_linea < self.COPIAS_MINIMAS_LINEA:
            return
        if planeta.variaciones_linea < 1:
            return
        if planeta.comparaciones_linea < 1:
            return

        planeta.vida_activa = True
        if not planeta.alcanzo_primera_vida:
            planeta.alcanzo_primera_vida = True
            planeta.anio_primera_vida = anio_actual
