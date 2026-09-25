import random

from events import EventManager
from stellar_systems.stellar_system import SistemaEstelar
from remnant import RemanenteEstelar
from star import Star
from star_formation import FormacionEstelarCosmica
from world_time import Time


class Universe:
    def __init__(
        self,
        seed=None,
        modelo_estelar=None,
        formacion_estelar=None,
    ):
        if seed is None:
            seed = random.SystemRandom().randint(
                1,
                999_999_999,
            )

        self.seed = int(seed)

        self.random = random.Random(self.seed)

        self.event_manager = EventManager()

        self.time = Time()

        self.modelo_estelar = modelo_estelar

        self.formacion_estelar = formacion_estelar or FormacionEstelarCosmica()

        self.estrellas = []
        self.remanentes = []
        self.sistemas_estelares = []

    def establecer_modelo_estelar(
        self,
        modelo,
    ):
        self.modelo_estelar = modelo

        for estrella in self.estrellas:
            estrella.establecer_modelo_evolutivo(modelo)

    def crear_sistema_estelar(
        self,
        estrella,
    ):
        nombre = f"Sistema de {estrella.nombre}"

        sistema = SistemaEstelar(
            nombre=nombre,
            anio_formacion=estrella.anio_nacimiento,
            estrellas=[estrella],
        )

        self.sistemas_estelares.append(sistema)

        return sistema

    def crear_estrella(
        self,
        masa_inicial,
        metalicidad_z,
        nombre=None,
        anio_nacimiento=None,
        poblacion=None,
        redshift_nacimiento=None,
    ):
        if (
            self.modelo_estelar is not None
            and hasattr(
                self.modelo_estelar,
                "admite_estrella",
            )
            and not (
                self.modelo_estelar.admite_estrella(
                    masa_inicial,
                    metalicidad_z,
                )
            )
        ):
            return None

        if nombre is None:
            nombre = self._generar_nombre_estelar()

        if anio_nacimiento is None:
            anio_nacimiento = self.time.anio

        edad_inicial = max(
            0,
            (self.time.anio - anio_nacimiento),
        )

        estrella = Star(
            nombre=nombre,
            masa_inicial=masa_inicial,
            metalicidad_z=metalicidad_z,
            modelo_evolutivo=(self.modelo_estelar),
            anio_nacimiento=(anio_nacimiento),
        )

        estrella.edad = edad_inicial

        estrella.actualizar_estado_fisico()

        self.estrellas.append(estrella)

        self.crear_sistema_estelar(estrella)

        if poblacion:
            descripcion_poblacion = f"Población {poblacion}"

        else:
            descripcion_poblacion = "población no especificada"

        texto_redshift = ""

        if redshift_nacimiento is not None:
            texto_redshift = f", z=" f"{redshift_nacimiento:.2f}"

        self.event_manager.agregar_evento(
            "Nacimiento estelar",
            anio_nacimiento,
            (
                f"{estrella.nombre} nació como "
                f"{descripcion_poblacion}, con "
                f"{estrella.masa_inicial:.3f} "
                "masas solares, "
                f"Z={estrella.metalicidad_z:.6g}"
                f"{texto_redshift}."
            ),
        )

        if estrella.ha_finalizado():
            if estrella.necesita_remanente():
                self.crear_remanente(estrella)

            if estrella in self.estrellas:
                self.estrellas.remove(estrella)

        return estrella

    def _generar_nombre_estelar(self):
        nombres_existentes = {estrella.nombre for estrella in self.estrellas}

        while True:
            numero = self.random.randint(
                1,
                9_999_999,
            )

            nombre = f"Estrella-{numero:07d}"

            if nombre not in nombres_existentes:
                return nombre

    def crear_remanente(
        self,
        estrella,
    ):
        if not estrella.necesita_remanente():
            return None

        anio_formacion = int(estrella.anio_nacimiento + estrella.edad_estado_modelo)

        anio_formacion = min(
            anio_formacion,
            self.time.anio,
        )

        remanente = RemanenteEstelar(
            nombre=(f"Remanente de " f"{estrella.nombre}"),
            tipo=(estrella.tipo_remanente),
            masa=(estrella.masa_remanente),
            origen=estrella,
            anio_formacion=(anio_formacion),
        )

        self.remanentes.append(remanente)

        estrella.remanente_creado = True

        self.event_manager.agregar_evento(
            "Remanente estelar",
            anio_formacion,
            (
                f"{estrella.nombre} terminó "
                f"su evolución como "
                f"{remanente.obtener_tipo_visible()}, con "
                f"{remanente.masa:.3f} "
                "masas solares."
            ),
        )

        return remanente

    def actualizar(
        self,
        anios_transcurridos,
    ):
        if anios_transcurridos <= 0:
            return

        anio_final = self.time.anio

        anio_inicial = max(
            0,
            (anio_final - anios_transcurridos),
        )

        estrellas_finalizadas = []

        for estrella in list(self.estrellas):
            etapa_anterior = estrella.etapa

            estrella.envejecer(anios_transcurridos)

            if estrella.etapa != etapa_anterior:
                self.event_manager.agregar_evento(
                    "Evolución estelar",
                    anio_final,
                    (
                        f"{estrella.nombre}: "
                        f"{etapa_anterior.replace('_', ' ')} -> "
                        f"{estrella.obtener_etapa_visible()}."
                    ),
                )

            if estrella.ha_finalizado():
                if estrella.necesita_remanente():
                    self.crear_remanente(estrella)

                estrellas_finalizadas.append(estrella)

        for estrella in estrellas_finalizadas:
            if estrella in self.estrellas:
                self.estrellas.remove(estrella)

        nacimientos = self.formacion_estelar.generar_nacimientos(
            seed=self.seed,
            anio_inicio=anio_inicial,
            anio_fin=anio_final,
        )

        no_modeladas = {}

        for nacimiento in nacimientos:
            if (
                self.modelo_estelar is not None
                and hasattr(
                    self.modelo_estelar,
                    "admite_estrella",
                )
                and not (
                    self.modelo_estelar.admite_estrella(
                        nacimiento.masa_inicial,
                        nacimiento.metalicidad_z,
                    )
                )
            ):
                motivo = self.modelo_estelar.motivo_no_admitida(
                    nacimiento.masa_inicial,
                    nacimiento.metalicidad_z,
                )

                no_modeladas[motivo] = (
                    no_modeladas.get(
                        motivo,
                        0,
                    )
                    + 1
                )

                continue

            self.crear_estrella(
                masa_inicial=(nacimiento.masa_inicial),
                metalicidad_z=(nacimiento.metalicidad_z),
                nombre=(nacimiento.nombre),
                anio_nacimiento=(nacimiento.anio),
                poblacion=(nacimiento.poblacion),
                redshift_nacimiento=(nacimiento.redshift),
            )

        for motivo, cantidad in no_modeladas.items():
            self.event_manager.agregar_evento(
                "Formación fuera del modelo",
                anio_final,
                (
                    f"{cantidad} nacimientos "
                    "no fueron evolucionados "
                    f"por SEVN: {motivo}."
                ),
            )

        self.event_manager.eventos.sort(key=lambda evento: (evento.anio))
