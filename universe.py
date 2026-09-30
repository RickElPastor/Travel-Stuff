import random

from abiogenesis.first_life_model import ModeloPrimeraVida

from abiogenesis.inheritance_variation_model import ModeloHerenciaVariacion

from abiogenesis.replication_model import ModeloReplicacionPrebiotica
from biology.unicellular_population_model import ModeloPoblacionUnicelular
from biology.inheritance_variation_model import ModeloHerenciaVariacionUnicelular

from chemistry.protocell_viability_model import ModeloViabilidadProtocelular

from extraordinary.chemistry_support_model import ModeloApoyoQuimicoExtraordinario

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
from planets.planet_formation_model import (
    ModeloFormacionPlanetasSolidos,
)
from planets.planetary_irradiation_model import (
    ModeloIrradiacionPlanetaria,
)
from habitability.habitable_zone_model import (
    ModeloZonaHabitable,
)
from habitability.terrestrial_candidate_model import (
    ModeloCandidatoTerrestre,
)
from habitability.atmospheric_retention_model import (
    ModeloRetencionAtmosferica,
)
from habitability.geologic_activity_model import (
    ModeloActividadGeologica,
)
from habitability.secondary_atmosphere_model import (
    ModeloAtmosferaSecundaria,
)
from habitability.surface_water_model import (
    ModeloAguaSuperficial,
)
from habitability.final_habitability_model import (
    ModeloHabitabilidadFinal,
)
from chemistry.prebiotic_environment_model import (
    ModeloEntornoPrebiotico,
)
from extraordinary.world_rules_model import (
    ModeloReglasMundo,
)
from chemistry.simple_organics_model import (
    ModeloOrganicosSimples,
)
from chemistry.prebiotic_concentration_model import (
    ModeloConcentracionPrebiotica,
)
from chemistry.complex_precursors_model import (
    ModeloPrecursoresComplejos,
)
from chemistry.prebiotic_polymerization_model import (
    ModeloPolimerizacionPrebiotica,
)
from chemistry.primitive_network_model import (
    ModeloRedQuimicaPrimitiva,
)
from chemistry.prebiotic_compartment_model import (
    ModeloCompartimentalizacionPrebiotica,
)
from chemistry.protocell_model import (
    ModeloProtocelula,
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
        self.planetas = []

        self.modelo_disco = ModeloDiscoProtoplanetario()

        self.modelo_formacion_embriones = ModeloFormacionEmbriones()

        self.modelo_impactos_gigantes = ModeloImpactosGigantes()

        self.modelo_formacion_planetas = ModeloFormacionPlanetasSolidos()

        self.modelo_entorno_disco = ModeloEntornoDisco()

        self.modelo_irradiacion_planetaria = ModeloIrradiacionPlanetaria()

        self.modelo_zona_habitable = ModeloZonaHabitable()

        self.modelo_candidato_terrestre = ModeloCandidatoTerrestre()

        self.modelo_retencion_atmosferica = ModeloRetencionAtmosferica()
        self.modelo_actividad_geologica = ModeloActividadGeologica()

        self.modelo_atmosfera_secundaria = ModeloAtmosferaSecundaria()

        self.modelo_agua_superficial = ModeloAguaSuperficial()

        self.modelo_habitabilidad_final = ModeloHabitabilidadFinal()

        self.modelo_entorno_prebiotico = ModeloEntornoPrebiotico()

        self.modelo_reglas_mundo = ModeloReglasMundo()

        self.modelo_organicos_simples = ModeloOrganicosSimples()

        self.modelo_concentracion_prebiotica = ModeloConcentracionPrebiotica()

        self.modelo_precursores_complejos = ModeloPrecursoresComplejos()

        self.modelo_polimerizacion_prebiotica = ModeloPolimerizacionPrebiotica()

        self.modelo_red_quimica_primitiva = ModeloRedQuimicaPrimitiva()

        self.modelo_compartimentalizacion_prebiotica = (
            ModeloCompartimentalizacionPrebiotica()
        )

        self.modelo_protocelula = ModeloProtocelula()
        self.modelo_viabilidad_protocelular = ModeloViabilidadProtocelular()
        self.modelo_replicacion_prebiotica = ModeloReplicacionPrebiotica()
        self.modelo_herencia_variacion = ModeloHerenciaVariacion()
        self.modelo_primera_vida = ModeloPrimeraVida()
        self.modelo_poblacion_unicelular = ModeloPoblacionUnicelular()
        self.modelo_herencia_unicelular = ModeloHerenciaVariacionUnicelular()
        self.modelo_seleccion_unicelular = self.modelo_herencia_unicelular.seleccion
        self.modelo_especies_unicelulares = self.modelo_herencia_unicelular.especies
        self.modelo_apoyo_extraordinario = ModeloApoyoQuimicoExtraordinario()

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

        planetas = self.modelo_formacion_planetas.generar_planetas(disco)

        for planeta in planetas:
            self.planetas.append(planeta)

            sistema.agregar_planeta(planeta)

        self.discos_protoplanetarios.append(disco)

        return disco

    def actualizar_irradiacion_planetaria(
        self,
    ):
        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in self.estrellas
        }

        for planeta in self.planetas:
            estrella = estrellas_por_nombre.get(planeta.estrella_anfitriona)

            self.modelo_irradiacion_planetaria.actualizar(
                planeta,
                estrella,
            )

    def actualizar_habitabilidad_radiativa(
        self,
    ):
        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in self.estrellas
        }

        for planeta in self.planetas:
            estrella = estrellas_por_nombre.get(planeta.estrella_anfitriona)

            self.modelo_zona_habitable.evaluar(
                planeta,
                estrella,
            )

    def actualizar_candidatos_terrestres(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_candidato_terrestre.evaluar(planeta)

    def actualizar_retencion_atmosferica(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_retencion_atmosferica.evaluar(planeta)

    def actualizar_actividad_geologica(
        self,
    ):
        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in self.estrellas
        }

        for planeta in self.planetas:
            estrella = estrellas_por_nombre.get(planeta.estrella_anfitriona)

            if estrella is None:
                continue

            self.modelo_actividad_geologica.evaluar(
                planeta,
                estrella.edad,
            )

    def actualizar_atmosferas_secundarias(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_atmosfera_secundaria.evaluar(planeta)

    def actualizar_agua_superficial(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_agua_superficial.evaluar(planeta)

    def actualizar_habitabilidad_final(
        self,
    ):
        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in self.estrellas
        }

        for planeta in self.planetas:
            estrella = estrellas_por_nombre.get(planeta.estrella_anfitriona)

            self.modelo_habitabilidad_final.evaluar(
                planeta,
                estrella,
            )

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

    def actualizar_quimica_prebiotica(
        self,
    ):
        estrellas_por_nombre = {
            estrella.nombre: estrella for estrella in self.estrellas
        }

        for planeta in self.planetas:
            estrella = estrellas_por_nombre.get(planeta.estrella_anfitriona)

            self.modelo_entorno_prebiotico.evaluar(
                planeta,
                estrella,
            )

    def actualizar_reglas_mundos(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_reglas_mundo.asignar(
                planeta,
                self.seed,
            )

    def actualizar_organicos_simples(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_organicos_simples.evaluar(planeta)

    def actualizar_concentracion_prebiotica(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_concentracion_prebiotica.evaluar(planeta)

    def actualizar_precursores_complejos(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_precursores_complejos.evaluar(planeta)

    def actualizar_polimerizacion_prebiotica(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_polimerizacion_prebiotica.evaluar(planeta)

    def actualizar_redes_quimicas_primitivas(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_red_quimica_primitiva.evaluar(planeta)

    def actualizar_compartimentalizacion_prebiotica(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_compartimentalizacion_prebiotica.evaluar(planeta)

    def actualizar_primera_vida(self):
        for planeta in self.planetas:
            self.modelo_primera_vida.evaluar(planeta, self.time.anio)

    def actualizar_poblacion_unicelular(self):
        for planeta in self.planetas:
            self.modelo_poblacion_unicelular.evaluar(planeta, self.time.anio)

    def actualizar_herencia_unicelular(self):
        for planeta in self.planetas:
            self.modelo_herencia_unicelular.evaluar(planeta, self.seed)

    def actualizar_herencia_variacion(self):
        for planeta in self.planetas:
            self.modelo_herencia_variacion.evaluar(
                planeta, self.seed, self.time.anio
            )

    def actualizar_replicacion_prebiotica(self):
        for planeta in self.planetas:
            self.modelo_replicacion_prebiotica.evaluar(planeta)

    def actualizar_viabilidad_protocelular(self):
        for planeta in self.planetas:
            self.modelo_viabilidad_protocelular.evaluar(planeta)

    def actualizar_apoyos_extraordinarios(self):
        for planeta in self.planetas:
            self.modelo_apoyo_extraordinario.evaluar(planeta)

    def actualizar_protocelulas(
        self,
    ):
        for planeta in self.planetas:
            self.modelo_protocelula.evaluar(planeta)

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

        self.actualizar_reglas_mundos()

        self.actualizar_irradiacion_planetaria()

        self.actualizar_habitabilidad_radiativa()

        self.actualizar_candidatos_terrestres()

        self.actualizar_retencion_atmosferica()

        self.actualizar_actividad_geologica()

        self.actualizar_atmosferas_secundarias()

        self.actualizar_agua_superficial()

        self.actualizar_habitabilidad_final()

        self.actualizar_quimica_prebiotica()

        self.actualizar_organicos_simples()

        self.actualizar_concentracion_prebiotica()

        self.actualizar_precursores_complejos()

        self.actualizar_polimerizacion_prebiotica()

        self.actualizar_redes_quimicas_primitivas()

        self.actualizar_compartimentalizacion_prebiotica()

        self.actualizar_protocelulas()

        self.actualizar_apoyos_extraordinarios()

        self.actualizar_viabilidad_protocelular()

        self.actualizar_replicacion_prebiotica()

        self.actualizar_herencia_variacion()

        self.actualizar_primera_vida()

        self.actualizar_poblacion_unicelular()

        self.actualizar_herencia_unicelular()

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
