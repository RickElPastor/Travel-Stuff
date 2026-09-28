from planets.planet import Planet

from planets.core_growth_model import (
    ModeloCrecimientoNucleo,
)

from planets.gas_accretion_model import (
    ModeloAcrecionGas,
)

from planets.runaway_gas_model import (
    ModeloRunawayGas,
)
from planets.planet_physics_model import (
    ModeloFisicaPlanetaria,
)


class ModeloFormacionPlanetasSolidos:
    """
    Convierte los protoplanetas resultantes de la
    fase de impactos gigantes en planetas.

    Después calcula:

    - tiempo de crecimiento del núcleo
    - disponibilidad de gas
    - acreción inicial de envoltura
    - runaway gaseoso
    """

    MASA_NUCLEO_CANDIDATO_GAS = 10.0
    MASA_NUCLEO_ACRECION_MAX = 20.0

    def __init__(self):
        self.modelo_crecimiento_nucleo = ModeloCrecimientoNucleo()
        self.modelo_acrecion_gas = ModeloAcrecionGas()
        self.modelo_runaway_gas = ModeloRunawayGas()
        self.modelo_fisica_planetaria = ModeloFisicaPlanetaria()

    def generar_planetas(
        self,
        disco,
    ):
        planetas = []

        for indice, protoplaneta in enumerate(
            disco.protoplanetas,
            start=1,
        ):
            composicion = self._clasificar_composicion(protoplaneta.zona_material)

            candidato_gas = protoplaneta.masa_tierra >= self.MASA_NUCLEO_CANDIDATO_GAS

            masa_nucleo_acrecion = min(
                protoplaneta.masa_tierra,
                self.MASA_NUCLEO_ACRECION_MAX,
            )

            tiempo_nucleo_myr = None
            gas_disponible = False

            if candidato_gas:
                planeta_temporal = Planet(
                    nombre="temporal",
                    masa_tierra=(protoplaneta.masa_tierra),
                    masa_solida_tierra=(protoplaneta.masa_tierra),
                    masa_nucleo_acrecion_tierra=(masa_nucleo_acrecion),
                    masa_gas_tierra=0.0,
                    semieje_mayor_au=(protoplaneta.semieje_mayor_au),
                )

                tiempo_nucleo_myr = (
                    self.modelo_crecimiento_nucleo.calcular_tiempo_nucleo_myr(
                        disco,
                        planeta_temporal,
                    )
                )

                gas_disponible = (
                    tiempo_nucleo_myr is not None
                    and disco.vida_gas_myr is not None
                    and tiempo_nucleo_myr < disco.vida_gas_myr
                )

            planeta = Planet(
                nombre=(f"Planeta-" f"{disco.estrella_nombre}-" f"{indice:03d}"),
                masa_tierra=(protoplaneta.masa_tierra),
                masa_solida_tierra=(protoplaneta.masa_tierra),
                masa_nucleo_acrecion_tierra=(masa_nucleo_acrecion),
                masa_gas_tierra=0.0,
                semieje_mayor_au=(protoplaneta.semieje_mayor_au),
                excentricidad=0.0,
                sistema_nombre=(disco.sistema_nombre),
                estrella_anfitriona=(disco.estrella_nombre),
                tipo_orbita=("circumestelar"),
                composicion_inicial=(composicion),
                candidato_captura_gas=(candidato_gas),
                origen_protoplaneta=(protoplaneta.nombre),
                embriones_fusionados=(protoplaneta.embriones_fusionados),
                tiempo_nucleo_myr=(tiempo_nucleo_myr),
                gas_disponible_al_formarse=(gas_disponible),
            )

            planetas.append(planeta)

        self.modelo_acrecion_gas.aplicar_acrecion(
            disco,
            planetas,
        )

        self.modelo_runaway_gas.aplicar_runaway(
            disco,
            planetas,
        )

        for planeta in planetas:
            self.modelo_fisica_planetaria.calcular_propiedades(planeta)

        return planetas

    def _clasificar_composicion(
        self,
        zona_material,
    ):
        if zona_material == "interior_hielo":
            return "rocosa"

        if zona_material == "exterior_hielo":
            return "rica_en_hielos"

        if zona_material == "mixta":
            return "mixta"

        return "indeterminada"
