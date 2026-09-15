class Time:
    def __init__(self):
        self.anio = 0
        self.velocidades = [0, 1, 10, 100, 1000, 10000]
        self.velocidad = 1
        self.acumulado = 0

    def avanzar(self, años):
        self.acumulado += años * self.velocidad
        ticks = 0

        while self.acumulado >= 1:
            self.anio += 1
            self.acumulado -= 1
            ticks += 1

        return ticks