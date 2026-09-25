import math
import random
from dataclasses import dataclass

from cosmology import CosmologiaPlanck18


@dataclass(frozen=True)
class NacimientoEstelar:
    nombre: str
    anio: int
    redshift: float

    masa_inicial: float
    metalicidad_z: float

    poblacion: str
    modelo_imf: str


class FormacionEstelarCosmica:
    PASO_ANIOS = 1_000_000

    VOLUMEN_COMOVIL_MPC3 = 1.0

    # Estos dos valores NO son astronomía.
    # Solamente controlan cuántas estrellas mantiene
    # Travel Stuff como objetos Python.
    FRACCION_RASTREO_POPIII = 1.0
    FRACCION_RASTREO_POPII = 1e-6

    # -------------------------------------------------
    # POBLACIÓN III
    # Liu & Bromm (2020)
    # Rango publicado: z = 4 - 24
    # -------------------------------------------------

    POPIII_A = 765.7
    POPIII_B = -5.92
    POPIII_C = 12.83
    POPIII_D = -8.55

    POPIII_Z_MIN = 4.0
    POPIII_Z_MAX = 24.0

    # Modelo IMF LOG:
    # xi(M) proporcional a M^-1
    # Intervalo usado en estudios de Pop III.
    POPIII_MASA_MIN = 5.0
    POPIII_MASA_MAX = 550.0
    POPIII_ALPHA = 1.0

    # -------------------------------------------------
    # POBLACIÓN I / II
    # Madau & Dickinson (2014)
    # Rango publicado: z = 0 - 8
    # -------------------------------------------------

    POPII_A = 0.015
    POPII_B = 2.7
    POPII_C = 2.9
    POPII_D = 5.6

    POPII_Z_MIN = 0.0
    POPII_Z_MAX = 8.0

    # IMF Salpeter.
    POPII_MASA_MIN = 0.1
    POPII_MASA_MAX = 100.0
    POPII_ALPHA = 2.35

    # Metalicidad solar de referencia.
    Z_SOLAR = 0.0142

    def __init__(self, cosmologia=None):
        self.cosmologia = cosmologia or CosmologiaPlanck18()

        self.masa_media_popiii = self._masa_media_power_law(
            self.POPIII_ALPHA,
            self.POPIII_MASA_MIN,
            self.POPIII_MASA_MAX,
        )

        self.masa_media_popii = self._masa_media_power_law(
            self.POPII_ALPHA,
            self.POPII_MASA_MIN,
            self.POPII_MASA_MAX,
        )

    def generar_nacimientos(
        self,
        seed,
        anio_inicio,
        anio_fin,
    ):
        if anio_fin <= anio_inicio:
            return []

        primer_bin = int(anio_inicio // self.PASO_ANIOS)

        ultimo_bin = int(anio_fin // self.PASO_ANIOS) - 1

        if ultimo_bin < primer_bin:
            return []

        nacimientos = []

        for indice_bin in range(
            primer_bin,
            ultimo_bin + 1,
        ):
            inicio_bin = indice_bin * self.PASO_ANIOS

            fin_bin = inicio_bin + self.PASO_ANIOS

            mitad_bin = inicio_bin + self.PASO_ANIOS / 2

            redshift = self.cosmologia.redshift_desde_edad(mitad_bin)

            if redshift is None:
                continue

            nacimientos.extend(
                self._generar_popiii(
                    seed,
                    indice_bin,
                    inicio_bin,
                    fin_bin,
                    redshift,
                )
            )

            nacimientos.extend(
                self._generar_popii(
                    seed,
                    indice_bin,
                    inicio_bin,
                    fin_bin,
                    redshift,
                )
            )

        nacimientos.sort(key=lambda nacimiento: (nacimiento.anio))

        return nacimientos

    def _generar_popiii(
        self,
        seed,
        indice_bin,
        inicio_bin,
        fin_bin,
        redshift,
    ):
        if not (self.POPIII_Z_MIN <= redshift <= self.POPIII_Z_MAX):
            return []

        tasa = self._tasa_sfrd(
            redshift,
            self.POPIII_A,
            self.POPIII_B,
            self.POPIII_C,
            self.POPIII_D,
        )

        lambda_rastreo = self._lambda_estrellas(
            tasa,
            self.masa_media_popiii,
            self.FRACCION_RASTREO_POPIII,
        )

        rng = self._crear_rng(
            seed,
            indice_bin,
            3,
        )

        cantidad = self._poisson(
            rng,
            lambda_rastreo,
        )

        nacimientos = []

        for indice in range(cantidad):
            masa = self._muestrear_power_law(
                rng,
                self.POPIII_ALPHA,
                self.POPIII_MASA_MIN,
                self.POPIII_MASA_MAX,
            )

            anio = rng.randrange(
                inicio_bin,
                fin_bin,
            )

            nombre = f"Estrella-III-" f"{indice_bin:06d}-" f"{indice + 1:03d}"

            nacimientos.append(
                NacimientoEstelar(
                    nombre=nombre,
                    anio=anio,
                    redshift=redshift,
                    masa_inicial=masa,
                    metalicidad_z=0.0,
                    poblacion="III",
                    modelo_imf="LOG",
                )
            )

        return nacimientos

    def _generar_popii(
        self,
        seed,
        indice_bin,
        inicio_bin,
        fin_bin,
        redshift,
    ):
        if not (self.POPII_Z_MIN <= redshift <= self.POPII_Z_MAX):
            return []

        tasa = self._tasa_sfrd(
            redshift,
            self.POPII_A,
            self.POPII_B,
            self.POPII_C,
            self.POPII_D,
        )

        lambda_rastreo = self._lambda_estrellas(
            tasa,
            self.masa_media_popii,
            self.FRACCION_RASTREO_POPII,
        )

        rng = self._crear_rng(
            seed,
            indice_bin,
            2,
        )

        cantidad = self._poisson(
            rng,
            lambda_rastreo,
        )

        nacimientos = []

        for indice in range(cantidad):
            masa = self._muestrear_power_law(
                rng,
                self.POPII_ALPHA,
                self.POPII_MASA_MIN,
                self.POPII_MASA_MAX,
            )

            metalicidad = self._muestrear_metalicidad_popii(
                rng,
                redshift,
            )

            anio = rng.randrange(
                inicio_bin,
                fin_bin,
            )

            nombre = f"Estrella-II-" f"{indice_bin:06d}-" f"{indice + 1:03d}"

            nacimientos.append(
                NacimientoEstelar(
                    nombre=nombre,
                    anio=anio,
                    redshift=redshift,
                    masa_inicial=masa,
                    metalicidad_z=metalicidad,
                    poblacion="II/I",
                    modelo_imf="Salpeter",
                )
            )

        return nacimientos

    def _lambda_estrellas(
        self,
        tasa_sfrd,
        masa_media,
        fraccion_rastreo,
    ):
        masa_formada = tasa_sfrd * self.VOLUMEN_COMOVIL_MPC3 * self.PASO_ANIOS

        estrellas_fisicas_esperadas = masa_formada / masa_media

        return estrellas_fisicas_esperadas * fraccion_rastreo

    def _tasa_sfrd(
        self,
        redshift,
        a,
        b,
        c,
        d,
    ):
        return a * (1 + redshift) ** b / (1 + ((1 + redshift) / c) ** d)

    def _muestrear_metalicidad_popii(
        self,
        rng,
        redshift,
    ):
        media_log = math.log10(1.04) - 0.24 * redshift

        log_z_relativa = rng.gauss(
            media_log,
            0.20,
        )

        metalicidad = self.Z_SOLAR * 10**log_z_relativa

        return min(
            metalicidad,
            1.0,
        )

    def _muestrear_power_law(
        self,
        rng,
        alpha,
        masa_min,
        masa_max,
    ):
        u = rng.random()

        if math.isclose(
            alpha,
            1.0,
        ):
            return masa_min * (masa_max / masa_min) ** u

        exponente = 1.0 - alpha

        minimo = masa_min**exponente

        maximo = masa_max**exponente

        return (minimo + u * (maximo - minimo)) ** (1.0 / exponente)

    def _masa_media_power_law(
        self,
        alpha,
        masa_min,
        masa_max,
    ):
        numerador = self._integral_power_law(
            1.0 - alpha,
            masa_min,
            masa_max,
        )

        denominador = self._integral_power_law(
            -alpha,
            masa_min,
            masa_max,
        )

        return numerador / denominador

    def _integral_power_law(
        self,
        exponente,
        minimo,
        maximo,
    ):
        if math.isclose(
            exponente,
            -1.0,
        ):
            return math.log(maximo / minimo)

        nuevo_exponente = exponente + 1.0

        return (maximo**nuevo_exponente - minimo**nuevo_exponente) / nuevo_exponente

    def _poisson(
        self,
        rng,
        lambda_eventos,
    ):
        if lambda_eventos <= 0:
            return 0

        limite = math.exp(-lambda_eventos)

        producto = 1.0
        cantidad = 0

        while producto > limite:
            cantidad += 1
            producto *= rng.random()

        return cantidad - 1

    def _crear_rng(
        self,
        seed,
        indice_bin,
        poblacion_id,
    ):
        mascara = (1 << 64) - 1

        semilla = (
            (int(seed) * 6_364_136_223_846_793_005)
            + (indice_bin * 1_442_695_040_888_963_407)
            + (poblacion_id * 22_695_477)
        ) & mascara

        return random.Random(semilla)
