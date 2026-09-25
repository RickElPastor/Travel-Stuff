import json
from pathlib import Path

from events import Event
from stellar_systems.stellar_system import SistemaEstelar
from remnant import RemanenteEstelar
from star import Star
from universe import Universe


class SaveManager:
    VERSION_GUARDADO = 3

    def __init__(self, carpeta="saves"):
        self.carpeta = Path(carpeta)

    def guardar(self, universe, nombre):
        ruta = self._obtener_ruta(nombre)

        self.carpeta.mkdir(parents=True, exist_ok=True)

        datos = {
            "version": (self.VERSION_GUARDADO),
            "seed": universe.seed,
            "random_state": (universe.random.getstate()),
            "tiempo": {
                "anio": (universe.time.anio),
                "indice_velocidad": (universe.time.indice_velocidad),
                "escala": (universe.time.escala),
                "acumulado": (universe.time.acumulado),
            },
            "estrellas": [estrella.a_dict() for estrella in universe.estrellas],
            "remanentes": [remanente.a_dict() for remanente in universe.remanentes],
            "sistemas_estelares": [
                sistema.a_dict() for sistema in universe.sistemas_estelares
            ],
            "eventos": [
                evento.a_dict() for evento in (universe.event_manager.obtener_eventos())
            ],
        }

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        return ruta

    def cargar(self, nombre, modelo_estelar=None):
        ruta = self._obtener_ruta(nombre)

        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        version = datos.get("version", 1)

        if version not in (
            2,
            self.VERSION_GUARDADO,
        ):
            raise ValueError(
                "El guardado pertenece a una "
                "versión incompatible con el "
                "sistema actual."
            )

        universe = Universe(seed=datos["seed"], modelo_estelar=modelo_estelar)

        tiempo = datos["tiempo"]

        universe.time.anio = tiempo["anio"]

        universe.time.indice_velocidad = tiempo["indice_velocidad"]

        universe.time.escala = tiempo["escala"]

        universe.time.acumulado = tiempo.get("acumulado", 0.0)

        estado_random = self._listas_a_tuplas(datos["random_state"])

        universe.random.setstate(estado_random)

        universe.estrellas = [
            Star.desde_dict(datos_estrella, modelo_evolutivo=(modelo_estelar))
            for datos_estrella in datos.get("estrellas", [])
        ]

        universe.remanentes = [
            RemanenteEstelar.desde_dict(datos_remanente)
            for datos_remanente in datos.get("remanentes", [])
        ]

        if version >= 3:
            universe.sistemas_estelares = [
                SistemaEstelar.desde_dict(datos_sistema)
                for datos_sistema in datos.get(
                    "sistemas_estelares",
                    [],
                )
            ]

        else:
            universe.sistemas_estelares = []

            for estrella in universe.estrellas:
                universe.crear_sistema_estelar(estrella)

        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in universe.estrellas
        }

        for remanente in universe.remanentes:
            if remanente.nombre_origen in estrellas_por_nombre:
                remanente.origen = estrellas_por_nombre[remanente.nombre_origen]

        universe.event_manager.eventos = [
            Event.desde_dict(datos_evento) for datos_evento in datos.get("eventos", [])
        ]

        return universe

    def listar_guardados(self):
        if not self.carpeta.exists():
            return []

        return sorted(
            archivo.name
            for archivo in self.carpeta.iterdir()
            if (archivo.is_file() and archivo.suffix == ".json")
        )

    def existe_guardado(self, nombre):
        return self._obtener_ruta(nombre).exists()

    def _obtener_ruta(self, nombre):
        if not nombre:
            raise ValueError("El guardado necesita " "un nombre.")

        nombre = Path(str(nombre)).name

        if nombre.endswith(".json"):
            nombre_archivo = nombre

        else:
            nombre_archivo = f"{nombre}.json"

        return self.carpeta / nombre_archivo

    def _listas_a_tuplas(self, valor):
        if isinstance(valor, list):
            return tuple(self._listas_a_tuplas(elemento) for elemento in valor)

        return valor
