class Event:
    def __init__(self, tipo, anio, mensaje, ambito="universo", entidad=None):
        self.tipo = tipo
        self.anio = anio
        self.mensaje = mensaje
        self.ambito = ambito
        self.entidad = entidad

    def __str__(self):
        anio = f"{self.anio:,.0f}".replace(",", " ")

        return f"[Año {anio}] " f"{self.tipo}: {self.mensaje}"

    def a_dict(self):
        return {"tipo": self.tipo, "anio": self.anio, "mensaje": self.mensaje,
                "ambito": self.ambito, "entidad": self.entidad}

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            tipo=datos["tipo"],
            anio=datos.get("anio", datos.get("año", 0)),
            mensaje=datos["mensaje"],
            ambito=datos.get("ambito", "universo"),
            entidad=datos.get("entidad"),
        )


class EventManager:
    def __init__(self):
        self.eventos = []

    def agregar_evento(self, tipo, anio, mensaje, ambito="universo", entidad=None):
        evento = Event(tipo, anio, mensaje, ambito, entidad)

        self.eventos.append(evento)

        return evento

    def obtener_eventos(self):
        return self.eventos

    def obtener_recientes(self, cantidad=5):
        if cantidad <= 0:
            return []

        return self.eventos[-cantidad:]

    def obtener_por_entidad(self, ambito, entidad):
        return [evento for evento in self.eventos
                if evento.ambito == ambito and evento.entidad == entidad]

    def limpiar(self):
        self.eventos.clear()
