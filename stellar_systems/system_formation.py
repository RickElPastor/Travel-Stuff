from dataclasses import dataclass

from stellar_systems.companion_model import ModeloCompaneraEstelar
from stellar_systems.multiplicity_model import ModeloMultiplicidadEstelar
from stellar_systems.orbital_model import ModeloOrbitalEstelar


@dataclass(frozen=True)
class AsignacionSistema:
    sistema_id: str
    es_primaria: bool

    periodo_orbital_dias: float | None = None

    semieje_mayor_au: float | None = None
    excentricidad: float | None = None

    q_objetivo: float | None = None
    q_real: float | None = None


class FormadorSistemasEstelares:
    def __init__(
        self,
        modelo_multiplicidad=None,
        modelo_orbital=None,
        modelo_companera=None,
    ):
        self.modelo_multiplicidad = modelo_multiplicidad or ModeloMultiplicidadEstelar()

        self.modelo_orbital = modelo_orbital or ModeloOrbitalEstelar()

        self.modelo_companera = modelo_companera or ModeloCompaneraEstelar()

    def asignar_sistemas(
        self,
        seed,
        nacimientos,
    ):
        asignaciones = {}

        disponibles = sorted(
            nacimientos,
            key=lambda nacimiento: (
                -nacimiento.masa_inicial,
                nacimiento.nombre,
            ),
        )

        usados = set()

        for primaria in disponibles:
            if primaria.nombre in usados:
                continue

            sistema_id = f"Sistema-{primaria.nombre}"

            asignaciones[primaria.nombre] = AsignacionSistema(
                sistema_id=sistema_id,
                es_primaria=True,
            )

            usados.add(primaria.nombre)

            es_multiple = self.modelo_multiplicidad.es_multiple(
                seed=seed,
                identificador=primaria.nombre,
                masa_primaria=(primaria.masa_inicial),
            )

            if not es_multiple:
                continue

            orbita = self.modelo_orbital.generar_orbita(
                seed=seed,
                identificador=primaria.nombre,
                masa_primaria=(primaria.masa_inicial),
            )

            periodo_dias = orbita["periodo_dias"]

            companera_objetivo = self.modelo_companera.generar_companera(
                seed=seed,
                identificador=primaria.nombre,
                masa_primaria=(primaria.masa_inicial),
                periodo_dias=periodo_dias,
            )

            masa_objetivo = companera_objetivo["masa_secundaria"]

            secundaria = self._buscar_secundaria(
                primaria=primaria,
                nacimientos=disponibles,
                usados=usados,
                masa_objetivo=masa_objetivo,
            )

            if secundaria is None:
                continue

            q_real = secundaria.masa_inicial / primaria.masa_inicial

            geometria_orbital = self.modelo_orbital.completar_orbita(
                seed=seed,
                identificador=primaria.nombre,
                masa_primaria=(primaria.masa_inicial),
                masa_secundaria=(secundaria.masa_inicial),
                periodo_dias=periodo_dias,
            )

            semieje_mayor_au = geometria_orbital["semieje_mayor_au"]

            excentricidad = geometria_orbital["excentricidad"]

            asignaciones[primaria.nombre] = AsignacionSistema(
                sistema_id=sistema_id,
                es_primaria=True,
                periodo_orbital_dias=(periodo_dias),
                q_objetivo=(companera_objetivo["q"]),
                q_real=q_real,
                semieje_mayor_au=(semieje_mayor_au),
                excentricidad=(excentricidad),
            )

            asignaciones[secundaria.nombre] = AsignacionSistema(
                sistema_id=sistema_id,
                es_primaria=False,
                periodo_orbital_dias=(periodo_dias),
                q_objetivo=(companera_objetivo["q"]),
                q_real=q_real,
                semieje_mayor_au=(semieje_mayor_au),
                excentricidad=(excentricidad),
            )

            usados.add(secundaria.nombre)

        return asignaciones

    def _buscar_secundaria(
        self,
        primaria,
        nacimientos,
        usados,
        masa_objetivo,
    ):
        candidatas = [
            nacimiento
            for nacimiento in nacimientos
            if (
                nacimiento.nombre not in usados
                and nacimiento.nombre != primaria.nombre
                and nacimiento.masa_inicial <= primaria.masa_inicial
            )
        ]

        if not candidatas:
            return None

        return min(
            candidatas,
            key=lambda nacimiento: (
                abs(nacimiento.masa_inicial - masa_objetivo),
                nacimiento.nombre,
            ),
        )
