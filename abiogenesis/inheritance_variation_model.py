import random

from abiogenesis.selection_model import ModeloSeleccionPrebiotica


class ModeloHerenciaVariacion:
    """Copia un patrón simbólico y registra cambios ocasionales.

    El patrón 0, 1 o 2 no representa una molécula identificada.
    Cada ciclo observado produce una copia de la línea modelada, no una
    población. La selección de variantes se delega a otro modelo.
    """

    PASO_OBSERVACION_ANIOS = 1_000_000
    PROBABILIDAD_VARIACION = 0.25  # Decisión de diseño, no dato científico.
    PATRON_INICIAL = 1

    def __init__(self):
        self.seleccion = ModeloSeleccionPrebiotica()

    def evaluar(self, planeta, seed, anio_actual):
        if not planeta.replicacion_prebiotica_activa:
            # Una interrupción termina esta línea de copias.
            planeta.patron_copia = None
            planeta.proxima_copia_anio = None
            planeta.copias_linea = 0
            planeta.variaciones_linea = 0
            planeta.comparaciones_linea = 0
            return

        if planeta.proxima_copia_anio is None:
            planeta.patron_copia = self.PATRON_INICIAL
            planeta.proxima_copia_anio = anio_actual
            planeta.copias_linea = 0
            planeta.variaciones_linea = 0
            planeta.comparaciones_linea = 0

        while planeta.proxima_copia_anio <= anio_actual:
            self._copiar(planeta, seed)
            planeta.proxima_copia_anio += self.PASO_OBSERVACION_ANIOS

    def _copiar(self, planeta, seed):
        numero = planeta.copias_heredables + 1
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:copia:{numero}"
        )

        # Por defecto, la copia recibe el patrón de la anterior.
        patron_anterior = planeta.patron_copia
        patron_nuevo = patron_anterior
        if generador.random() < self.PROBABILIDAD_VARIACION:
            # +1 o +2 (módulo 3) siempre produce un patrón diferente.
            patron_nuevo = (patron_nuevo + 1 + generador.randrange(2)) % 3
            planeta.variaciones_prebioticas += 1
            planeta.variaciones_linea += 1

            patron_nuevo = self.seleccion.elegir(
                planeta, patron_anterior, patron_nuevo
            )

        planeta.patron_copia = patron_nuevo
        planeta.copias_heredables = numero
        planeta.copias_linea += 1
