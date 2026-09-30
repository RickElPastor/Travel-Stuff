import math
import random


class ModeloOrbitalEstelar:
    nombre = "Distribución orbital empírica"

    # Para estrellas tipo solar:
    # Raghavan et al. (2010)
    SOLAR_LOGP_MEDIA = 5.03
    SOLAR_LOGP_SIGMA = 2.28

    # Para enanas M usamos una distribución
    # observacional de separaciones.
    M_LOGA_MEDIA = 1.3
    M_LOGA_SIGMA = 1.3

    # Límites prácticos para evitar órbitas
    # absurdamente pequeñas o enormes.
    LOGP_MIN = 0.2
    LOGP_MAX = 8.0

    def generar_orbita(
        self,
        seed,
        identificador,
        masa_primaria,
    ):
        masa = float(masa_primaria)

        if masa <= 0:
            raise ValueError("La masa primaria debe ser mayor que 0.")

        semilla_local = f"{int(seed)}:" f"{identificador}:" "orbita"

        rng = random.Random(semilla_local)

        if masa < 0.6:
            periodo_dias = self._generar_periodo_baja_masa(
                rng,
                masa,
            )

            metodo = "lognormal_separacion_enana_m"

        elif masa < 2.0:
            periodo_dias = self._generar_periodo_solar(rng)

            metodo = "lognormal_periodo_solar"

        else:
            periodo_dias = self._generar_periodo_masivo(
                rng,
                masa,
            )

            metodo = "power_law_dependiente_masa"

        log_periodo = math.log10(periodo_dias)

        return {
            "periodo_dias": periodo_dias,
            "log_periodo": log_periodo,
            "metodo": metodo,
        }

    def completar_orbita(
        self,
        seed,
        identificador,
        masa_primaria,
        masa_secundaria,
        periodo_dias,
    ):
        semieje_mayor_au = self.calcular_semieje_mayor_au(
            masa_primaria=masa_primaria,
            masa_secundaria=masa_secundaria,
            periodo_dias=periodo_dias,
        )

        excentricidad = self.generar_excentricidad(
            seed=seed,
            identificador=identificador,
            masa_primaria=masa_primaria,
            periodo_dias=periodo_dias,
        )

        return {
            "semieje_mayor_au": (semieje_mayor_au),
            "excentricidad": (excentricidad),
        }

    def calcular_semieje_mayor_au(
        self,
        masa_primaria,
        masa_secundaria,
        periodo_dias,
    ):
        if masa_primaria <= 0:
            raise ValueError("La masa primaria debe ser mayor que 0.")

        if masa_secundaria <= 0:
            raise ValueError("La masa secundaria debe ser mayor que 0.")

        if periodo_dias <= 0:
            raise ValueError("El periodo orbital debe ser mayor que 0.")

        masa_total = float(masa_primaria) + float(masa_secundaria)

        periodo_anios = float(periodo_dias) / 365.25

        semieje_mayor_au = (masa_total * periodo_anios**2) ** (1.0 / 3.0)

        return semieje_mayor_au

    def generar_excentricidad(
        self,
        seed,
        identificador,
        masa_primaria,
        periodo_dias,
    ):
        if periodo_dias <= 0:
            raise ValueError("El periodo orbital debe ser mayor que 0.")

        periodo_dias = float(periodo_dias)

        masa_primaria = float(masa_primaria)

        log_periodo = math.log10(periodo_dias)

        # Los sistemas extremadamente cerrados
        # se consideran circularizados.
        if periodo_dias <= 2.0:
            return 0.0

        if masa_primaria <= 5.0:
            eta = 0.6 - 0.7 / (log_periodo - 0.5)

        else:
            eta = 0.9 - 0.2 / (log_periodo - 0.5)

        # Para periodos muy cortos la parametrización
        # puede producir exponentes demasiado negativos.
        # Aproximamos esos sistemas como casi circulares.
        if eta <= -1.0:
            return 0.0

        excentricidad_maxima = 1.0 - (periodo_dias / 2.0) ** (-2.0 / 3.0)

        excentricidad_maxima = max(
            0.0,
            min(
                excentricidad_maxima,
                0.999,
            ),
        )

        semilla_local = (
            f"{int(seed)}:" f"{identificador}:" f"{periodo_dias:.12g}:" "excentricidad"
        )

        rng = random.Random(semilla_local)

        u = rng.random()

        excentricidad = excentricidad_maxima * u ** (1.0 / (eta + 1.0))

        return excentricidad

    def _generar_periodo_baja_masa(
        self,
        rng,
        masa_primaria,
    ):
        log_separacion_au = rng.gauss(
            self.M_LOGA_MEDIA,
            self.M_LOGA_SIGMA,
        )

        # Evitamos extremos patológicos.
        log_separacion_au = max(
            -2.0,
            min(
                log_separacion_au,
                4.5,
            ),
        )

        separacion_au = 10**log_separacion_au

        # Aproximación usada solamente para
        # transformar la distribución observada
        # de separaciones en una de periodos.
        #
        # q_referencia = M2 / M1 = 0.5
        masa_total_referencia = masa_primaria * 1.5

        # Tercera ley de Kepler:
        #
        # P^2 = a^3 / M
        #
        # usando:
        # P en años
        # a en AU
        # M en masas solares.
        periodo_anios = math.sqrt(separacion_au**3 / masa_total_referencia)

        periodo_dias = periodo_anios * 365.25

        return self._limitar_periodo(periodo_dias)

    def _generar_periodo_solar(
        self,
        rng,
    ):
        log_periodo = rng.gauss(
            self.SOLAR_LOGP_MEDIA,
            self.SOLAR_LOGP_SIGMA,
        )

        log_periodo = max(
            self.LOGP_MIN,
            min(
                log_periodo,
                self.LOGP_MAX,
            ),
        )

        return 10**log_periodo

    def _generar_periodo_masivo(
        self,
        rng,
        masa_primaria,
    ):
        # Aproximación a la dependencia observada
        # entre masa primaria y distribución
        # de periodos.
        gamma = 0.7 - 0.9 * math.log10(masa_primaria)

        log_periodo = self._muestrear_power_law(
            rng,
            gamma,
            0.5,
            7.5,
        )

        return 10**log_periodo

    def _muestrear_power_law(
        self,
        rng,
        gamma,
        minimo,
        maximo,
    ):
        u = rng.random()

        if math.isclose(
            gamma,
            -1.0,
        ):
            return minimo * (maximo / minimo) ** u

        exponente = gamma + 1.0

        minimo_elevado = minimo**exponente

        maximo_elevado = maximo**exponente

        return (minimo_elevado + u * (maximo_elevado - minimo_elevado)) ** (
            1.0 / exponente
        )

    def _limitar_periodo(
        self,
        periodo_dias,
    ):
        log_periodo = math.log10(periodo_dias)

        log_periodo = max(
            self.LOGP_MIN,
            min(
                log_periodo,
                self.LOGP_MAX,
            ),
        )

        return 10**log_periodo
