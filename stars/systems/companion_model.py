import math
import random


class ModeloCompaneraEstelar:
    nombre = "Razón de masas empírica"

    Q_MIN = 0.1
    Q_CORTE = 0.3
    Q_MAX = 1.0

    # Valores aproximados basados en las distribuciones
    # resumidas por Moe & Di Stefano (2017).
    #
    # Cada grupo contiene:
    #
    # log10(P / días)
    # gamma para q < 0.3
    # gamma para q >= 0.3
    #
    # La distribución sigue:
    #
    # p(q) proporcional a q ** gamma

    DATOS_Q = {
        "solar": {
            1.0: (0.3, -0.5),
            3.0: (0.3, -0.5),
            5.0: (0.3, -0.5),
            7.0: (0.3, -1.1),
        },
        "intermedia": {
            1.0: (0.2, -0.5),
            3.0: (0.1, -0.9),
            5.0: (-0.5, -1.4),
            7.0: (-1.0, -2.0),
        },
        "masiva": {
            1.0: (0.1, -0.5),
            3.0: (-0.2, -1.7),
            5.0: (-1.2, -2.0),
            7.0: (-1.5, -2.0),
        },
        "muy_masiva": {
            1.0: (0.1, -0.5),
            3.0: (-0.2, -1.7),
            5.0: (-1.2, -2.0),
            7.0: (-2.0, -2.0),
        },
    }

    def generar_companera(
        self,
        seed,
        identificador,
        masa_primaria,
        periodo_dias,
    ):
        if masa_primaria <= 0:
            raise ValueError("La masa primaria debe ser mayor que 0.")

        if periodo_dias <= 0:
            raise ValueError("El periodo orbital debe ser mayor que 0.")

        gamma_bajo, gamma_alto = self._obtener_exponentes(
            masa_primaria,
            periodo_dias,
        )

        semilla_local = (
            f"{int(seed)}:" f"{identificador}:" f"{periodo_dias:.12g}:" "companera"
        )

        rng = random.Random(semilla_local)

        q = self._muestrear_q(
            rng,
            gamma_bajo,
            gamma_alto,
        )

        masa_secundaria = float(masa_primaria) * q

        return {
            "q": q,
            "masa_secundaria": masa_secundaria,
        }

    def _obtener_exponentes(
        self,
        masa_primaria,
        periodo_dias,
    ):
        masa = float(masa_primaria)

        # Para estrellas de baja masa usamos por ahora
        # una distribución plana de q.
        #
        # Esto es una aproximación explícita.
        # Las observaciones de estrellas M son
        # compatibles aproximadamente con una
        # distribución plana en gran parte del rango.

        if masa < 0.8:
            return 0.0, 0.0

        if masa < 2.0:
            grupo = "solar"

        elif masa < 5.0:
            grupo = "intermedia"

        elif masa < 9.0:
            grupo = "masiva"

        else:
            grupo = "muy_masiva"

        log_periodo = math.log10(periodo_dias)

        return self._interpolar_periodo(
            grupo,
            log_periodo,
        )

    def _interpolar_periodo(
        self,
        grupo,
        log_periodo,
    ):
        datos = self.DATOS_Q[grupo]

        puntos = sorted(datos.keys())

        if log_periodo <= puntos[0]:
            return datos[puntos[0]]

        if log_periodo >= puntos[-1]:
            return datos[puntos[-1]]

        for izquierda, derecha in zip(
            puntos,
            puntos[1:],
        ):
            if izquierda <= log_periodo <= derecha:
                fraccion = (log_periodo - izquierda) / (derecha - izquierda)

                gamma_bajo_izq, gamma_alto_izq = datos[izquierda]

                gamma_bajo_der, gamma_alto_der = datos[derecha]

                gamma_bajo = self._interpolar(
                    fraccion,
                    gamma_bajo_izq,
                    gamma_bajo_der,
                )

                gamma_alto = self._interpolar(
                    fraccion,
                    gamma_alto_izq,
                    gamma_alto_der,
                )

                return (
                    gamma_bajo,
                    gamma_alto,
                )

        return datos[puntos[-1]]

    def _muestrear_q(
        self,
        rng,
        gamma_bajo,
        gamma_alto,
    ):
        peso_bajo = self._integral_power_law(
            gamma_bajo,
            self.Q_MIN,
            self.Q_CORTE,
        )

        continuidad = self.Q_CORTE ** (gamma_bajo - gamma_alto)

        peso_alto = continuidad * self._integral_power_law(
            gamma_alto,
            self.Q_CORTE,
            self.Q_MAX,
        )

        probabilidad_bajo = peso_bajo / (peso_bajo + peso_alto)

        if rng.random() < probabilidad_bajo:
            return self._muestrear_power_law(
                rng,
                gamma_bajo,
                self.Q_MIN,
                self.Q_CORTE,
            )

        return self._muestrear_power_law(
            rng,
            gamma_alto,
            self.Q_CORTE,
            self.Q_MAX,
        )

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

    def _integral_power_law(
        self,
        gamma,
        minimo,
        maximo,
    ):
        if math.isclose(
            gamma,
            -1.0,
        ):
            return math.log(maximo / minimo)

        exponente = gamma + 1.0

        return (maximo**exponente - minimo**exponente) / exponente

    def _interpolar(
        self,
        fraccion,
        valor_inicial,
        valor_final,
    ):
        return valor_inicial + fraccion * (valor_final - valor_inicial)
