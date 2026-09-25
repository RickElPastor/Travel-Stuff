class Time:
    def __init__(self):
        self.anio = 0

        self.velocidades_planeta = [0, 1, 2, 3]

        self.velocidades_universo = [
            0,
            1,
            10,
            100,
            1_000,
            10_000,
            1_000_000,
            100_000_000,
            1_000_000_000,
        ]

        self.indice_velocidad = 1
        self.escala = "universo"
        self.acumulado = 0.0

    def avanzar(self, segundos_reales):
        if segundos_reales < 0:
            raise ValueError("El tiempo real transcurrido " "no puede ser negativo.")

        velocidad = self.obtener_velocidad_actual()

        self.acumulado += segundos_reales * velocidad

        anios_transcurridos = int(self.acumulado)

        if anios_transcurridos > 0:
            self.anio += anios_transcurridos

            self.acumulado -= anios_transcurridos

        return anios_transcurridos

    def obtener_velocidades_actuales(self):
        if self.escala == "planeta":
            return self.velocidades_planeta

        return self.velocidades_universo

    def obtener_velocidad_actual(self):
        velocidades = self.obtener_velocidades_actuales()

        self.indice_velocidad = min(self.indice_velocidad, len(velocidades) - 1)

        return velocidades[self.indice_velocidad]

    def subir_velocidad(self):
        velocidades = self.obtener_velocidades_actuales()

        if self.indice_velocidad < len(velocidades) - 1:
            self.indice_velocidad += 1

        return self.obtener_velocidad_actual()

    def bajar_velocidad(self):
        if self.indice_velocidad > 0:
            self.indice_velocidad -= 1

        return self.obtener_velocidad_actual()

    def establecer_escala(self, escala):
        if escala not in ("universo", "planeta"):
            raise ValueError("La escala debe ser " "'universo' o 'planeta'.")

        self.escala = escala

        velocidades = self.obtener_velocidades_actuales()

        self.indice_velocidad = min(self.indice_velocidad, len(velocidades) - 1)

    def obtener_descripcion_velocidad(self):
        velocidad = self.obtener_velocidad_actual()

        if velocidad == 0:
            return "Pausado"

        valor = f"{velocidad:,}".replace(",", " ")

        return f"{valor} años/s"
