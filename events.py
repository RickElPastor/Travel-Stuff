
class Event:
    def __init__(self, tipo, año, mensaje):
        self.tipo = tipo
        self.anio = año
        self.mensaje = mensaje

    def __str__(self):
        return f"[Año {self.anio}] {self.tipo}: {self.mensaje}"

class EventManager:
    def __init__(self, random):
        self.eventos = []
        self.random = random

    def agregar_evento(self, tipo, año, mensaje):
        evento = Event(tipo, año, mensaje)
        self.eventos.append(evento)

    def obtener_eventos(self):
        return self.eventos

    def obtener_recientes(self, cantidad=5):
        return self.eventos[-cantidad:]

    def actualizar(self, año):
        probabilidad = self.random.randint(1, 100)

        if probabilidad <= 20:
            self.agregar_evento(
                "Estrella",
                año,
                "Una estrella ha comenzado a formarse."
            )
        elif probabilidad <= 30:
            self.agregar_evento(
                "Supernova",
                año,
                "Una estrella ha explotado."
            )

