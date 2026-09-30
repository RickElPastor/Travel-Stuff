import time


class Simulation:
    # La pantalla se refresca cada 0.05 s; el límite debe dejar pasar ese
    # intervalo completo para que x1 sea realmente un año por segundo.
    MAX_TRANS_CURRIDO_SEGUNDOS = 0.1

    def __init__(self, universe, reloj=None):
        self.universe = universe

        self._reloj = reloj or time.monotonic

        self.ultimo_tick = self._reloj()

    def actualizar(self):
        ahora = self._reloj()

        transcurrido = ahora - self.ultimo_tick

        self.ultimo_tick = ahora

        if transcurrido < 0:
            transcurrido = 0

        transcurrido = min(
            transcurrido,
            self.MAX_TRANS_CURRIDO_SEGUNDOS,
        )

        anios_transcurridos = self.universe.time.avanzar(transcurrido)

        if anios_transcurridos > 0:
            self.universe.actualizar(anios_transcurridos)

        return anios_transcurridos

    def reiniciar_reloj(self):
        self.ultimo_tick = self._reloj()

    def subir_velocidad(self):
        return self.universe.time.subir_velocidad()

    def bajar_velocidad(self):
        return self.universe.time.bajar_velocidad()

    def obtener_velocidad(self):
        return self.universe.time.obtener_velocidad_actual()
