import json

from universe import Universe
from events import Event

class SaveManager:

    def guardar(self, universe, nombre):
        import os

        os.makedirs("saves", exist_ok=True)

        ruta = os.path.join("saves", nombre + ".json")

        datos = {
            "seed": universe.seed,
            "edad_universo": universe.time.anio,
            "velocidad": universe.time.velocidad,
            "eventos": [
                {
                    "tipo": evento.tipo,
                    "año": evento.anio,
                    "mensaje": evento.mensaje
                }
                for evento in universe.event_manager.eventos
            ]
        }

        with open(ruta, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def cargar(self, nombre):
        import os

        ruta = os.path.join("saves", nombre)

        with open(ruta, "r") as archivo:
            datos = json.load(archivo)

        universe = Universe()

        universe.seed = datos["seed"]
        universe.random.seed(universe.seed)
        universe.time.anio = datos[f"edad_universo"]
        universe.time.velocidad = datos["velocidad"]
        for datos_evento in datos["eventos"]:
            evento = Event(
                datos_evento["tipo"],
                datos_evento["año"],
                datos_evento["mensaje"]
            )

            universe.event_manager.eventos.append(evento)

        return universe

    def listar_guardados(self):
        import os

        if not os.path.exists("saves"):
            return []

        archivos = os.listdir("saves")

        guardados = []

        for archivo in archivos:
            if archivo.endswith(".json"):
                guardados.append(archivo)

        return guardados

    def existe_guardado(self, nombre):
        import os

        ruta = os.path.join("saves", nombre + ".json")

        return os.path.exists(ruta)
