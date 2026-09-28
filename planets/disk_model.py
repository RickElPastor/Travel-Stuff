import math
import random

from planets.protoplanetary_disk import (
    DiscoProtoplanetario,
)
from planets.disk_structure_model import (
    ModeloEstructuraDisco,
)
from planets.snow_line_model import (
    ModeloLineaHielo,
)
from planets.gas_disk_model import (
    ModeloGasDisco,
)


class ModeloDiscoProtoplanetario:
    nombre = "Pascucci et al. 2016 " "masa de polvo - masa estelar"

    MASA_ESTELAR_MIN = 0.03
    MASA_ESTELAR_MAX = 2.0

    # Chamaeleon I, ~2-3 Myr.
    #
    # log10(Mpolvo / Mtierra)
    # =
    # alpha * log10(Mestrella / Msol)
    # + beta
    #
    # Relación con temperatura del polvo
    # dependiente de la luminosidad estelar.
    ALPHA = 1.3
    BETA = 1.1

    DISPERSION_DEX = 0.8

    def __init__(self):
        self.modelo_estructura = ModeloEstructuraDisco()
        self.modelo_linea_hielo = ModeloLineaHielo()
        self.modelo_gas = ModeloGasDisco()

    def admite_estrella(
        self,
        masa_estelar,
        metalicidad_z,
    ):
        masa = float(masa_estelar)

        # La relación observacional utilizada
        # no representa estrellas Pop III Z=0.
        if metalicidad_z == 0:
            return False

        return self.MASA_ESTELAR_MIN <= masa <= self.MASA_ESTELAR_MAX

    def motivo_no_admitida(
        self,
        masa_estelar,
        metalicidad_z,
    ):
        if metalicidad_z == 0:
            return "el modelo observacional de discos " "no representa Z=0"

        if masa_estelar < self.MASA_ESTELAR_MIN:
            return "masa estelar menor que " f"{self.MASA_ESTELAR_MIN} Msol"

        if masa_estelar > self.MASA_ESTELAR_MAX:
            return "masa estelar mayor que " f"{self.MASA_ESTELAR_MAX} Msol"

        return "estrella fuera del modelo de disco"

    def generar_disco(
        self,
        seed,
        identificador,
        estrella_nombre,
        masa_estelar,
        metalicidad_z,
        sistema_nombre=None,
        radio_exterior_au=None,
        truncado_por_companera=False,
    ):
        if not self.admite_estrella(
            masa_estelar,
            metalicidad_z,
        ):
            raise ValueError(
                self.motivo_no_admitida(
                    masa_estelar,
                    metalicidad_z,
                )
            )

        semilla_local = f"{int(seed)}:" f"{identificador}:" "disco_protoplanetario"

        rng = random.Random(semilla_local)

        dispersion = rng.gauss(
            0.0,
            self.DISPERSION_DEX,
        )

        log_masa_polvo = self.ALPHA * math.log10(masa_estelar) + self.BETA + dispersion

        masa_polvo_tierra = 10**log_masa_polvo

        radio_caracteristico_au = (
            self.modelo_estructura.calcular_radio_caracteristico_au(masa_estelar)
        )

        linea_hielo_au = self.modelo_linea_hielo.calcular_linea_hielo_au(masa_estelar)

        propiedades_gas = self.modelo_gas.generar_propiedades(
            seed=seed,
            identificador=identificador,
            masa_polvo_tierra=(masa_polvo_tierra),
        )

        return DiscoProtoplanetario(
            estrella_nombre=(estrella_nombre),
            sistema_nombre=(sistema_nombre),
            masa_estelar_msol=(masa_estelar),
            masa_polvo_tierra=(masa_polvo_tierra),
            radio_exterior_au=(radio_exterior_au),
            truncado_por_companera=(truncado_por_companera),
            radio_caracteristico_au=(radio_caracteristico_au),
            radio_interior_au=(self.modelo_estructura.RADIO_INTERIOR_AU),
            gamma_perfil=(self.modelo_estructura.GAMMA),
            linea_hielo_au=(linea_hielo_au),
            modelo=self.nombre,
            masa_gas_referencia_tierra=(propiedades_gas["masa_gas_referencia_tierra"]),
            relacion_gas_polvo=(propiedades_gas["relacion_gas_polvo"]),
            vida_gas_myr=(propiedades_gas["vida_gas_myr"]),
        )
