import random

from events import EventManager
from stellar_systems.stellar_system import SistemaEstelar
from planets.disk_environment_model import (
    ModeloEntornoDisco,
)
from planets.disk_model import (
    ModeloDiscoProtoplanetario,
)
from planets.embryo_formation_model import (
    ModeloFormacionEmbriones,
)
from planets.giant_impact_model import (
    ModeloImpactosGigantes,
)
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

        self.discos_protoplanetarios = []

        self.modelo_disco = ModeloDiscoProtoplanetario()

        self.modelo_formacion_embriones = ModeloFormacionEmbriones()

        self.modelo_impactos_gigantes = ModeloImpactosGigantes()

        self.modelo_entorno_disco = ModeloEntornoDisco()

    def establecer_modelo_estelar(
        self,
        modelo,
    ):
        self.modelo_estelar = modelo

        for estrella in self.estrellas:
            estrella.establecer_modelo_evolutivo(modelo)

    def buscar_sistema_estelar(
        self,
        nombre,
    ):
        for sistema in self.sistemas_estelares:
            if sistema.nombre == nombre:
                return sistema

        return None

    def crear_sistema_estelar(
        self,
        nombre,
        anio_formacion,
        estrella_primaria=None,
        periodo_orbital_dias=None,
        q_objetivo=None,
        q_real=None,
        semieje_mayor_au=None,
        excentricidad=None,
    ):
        sistema = self.buscar_sistema_estelar(nombre)

        if sistema is None:
            sistema = SistemaEstelar(
                nombre=nombre,
                anio_formacion=anio_formacion,
                periodo_orbital_dias=(periodo_orbital_dias),
                q_objetivo=q_objetivo,
                q_real=q_real,
                semieje_mayor_au=semieje_mayor_au,
                excentricidad=excentricidad,
            )

            self.sistemas_estelares.append(sistema)

        else:
            sistema.anio_formacion = min(
                sistema.anio_formacion,
                int(anio_formacion),
            )

            sistema.actualizar_datos_orbitales(
                periodo_orbital_dias=(periodo_orbital_dias),
                q_objetivo=q_objetivo,
                q_real=q_real,
                semieje_mayor_au=semieje_mayor_au,
                excentricidad=excentricidad,
            )

        if estrella_primaria is not None:
            sistema.establecer_estrella_primaria(estrella_primaria)

        return sistema

    def registrar_nacimiento_en_sistema(
        self,
        nacimiento,
    ):
        nombre_sistema = nacimiento.sistema_id

        if nombre_sistema is None:
            nombre_sistema = f"Sistema de {nacimiento.nombre}"

        sistema = self.crear_sistema_estelar(
            nombre=nombre_sistema,
            anio_formacion=nacimiento.anio,
            periodo_orbital_dias=(nacimiento.periodo_orbital_dias),
            q_objetivo=nacimiento.q_objetivo,
            q_real=nacimiento.q_real,
            semieje_mayor_au=(nacimiento.semieje_mayor_au),
            excentricidad=(nacimiento.excentricidad),
        )

        sistema.agregar_estrella(nacimiento.nombre)

        if nacimiento.es_primaria:
            sistema.establecer_estrella_primaria(nacimiento.nombre)

        self.crear_disco_para_nacimiento(
            nacimiento,
            sistema,
        )

        return sistema

    def buscar_disco_protoplanetario(
        self,
        estrella_nombre,
    ):
        for disco in self.discos_protoplanetarios:
            if disco.estrella_nombre == estrella_nombre:
                return disco

        return None

    def crear_disco_para_nacimiento(
        self,
        nacimiento,
        sistema,
    ):
        existente = self.buscar_disco_protoplanetario(nacimiento.nombre)

        if existente is not None:
            return existente

        if not self.modelo_disco.admite_estrella(
            nacimiento.masa_inicial,
            nacimiento.metalicidad_z,
        ):
            return None

        radio_exterior_au = self.modelo_entorno_disco.obtener_radio_exterior_au(sistema)

        truncado = radio_exterior_au is not None

        disco = self.modelo_disco.generar_disco(
            seed=self.seed,
            identificador=(nacimiento.nombre),
            estrella_nombre=(nacimiento.nombre),
            masa_estelar=(nacimiento.masa_inicial),
            metalicidad_z=(nacimiento.metalicidad_z),
            sistema_nombre=(sistema.nombre),
            radio_exterior_au=(radio_exterior_au),
            truncado_por_companera=(truncado),
        )

        embriones = self.modelo_formacion_embriones.generar_embriones(disco)

        disco.establecer_embriones(embriones)

        protoplanetas = self.modelo_impactos_gigantes.generar_protoplanetas(disco)

        disco.establecer_protoplanetas(protoplanetas)

        self.discos_protoplanetarios.append(disco)

        return disco

    def crear_estrella(
        self,
        masa_inicial,
        metalicidad_z,
        nombre=None,
        anio_nacimiento=None,
        poblacion=None,
        redshift_nacimiento=None,
        sistema_id=None,
        es_primaria=True,
        periodo_orbital_dias=None,
        q_objetivo=None,
        q_real=None,
        semieje_mayor_au=None,
        excentricidad=None,
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

        if sistema_id is None:
            sistema_id = f"Sistema de {estrella.nombre}"

        sistema = self.crear_sistema_estelar(
            nombre=sistema_id,
            anio_formacion=(estrella.anio_nacimiento),
            periodo_orbital_dias=(periodo_orbital_dias),
            semieje_mayor_au=(semieje_mayor_au),
            excentricidad=(excentricidad),
            q_objetivo=q_objetivo,
            q_real=q_real,
        )

        sistema.agregar_estrella(estrella)

        if es_primaria:
            sistema.establecer_estrella_primaria(estrella)

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
            self.registrar_nacimiento_en_sistema(nacimiento)
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
                nombre=nacimiento.nombre,
                anio_nacimiento=nacimiento.anio,
                poblacion=nacimiento.poblacion,
                redshift_nacimiento=(nacimiento.redshift),
                sistema_id=(nacimiento.sistema_id),
                es_primaria=(nacimiento.es_primaria),
                periodo_orbital_dias=(nacimiento.periodo_orbital_dias),
                semieje_mayor_au=(nacimiento.semieje_mayor_au),
                excentricidad=(nacimiento.excentricidad),
                q_objetivo=(nacimiento.q_objetivo),
                q_real=nacimiento.q_real,
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
