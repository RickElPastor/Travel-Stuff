import math
import random


class ModeloGasDisco:
    """
    Aproximación de Fase 1 para el reservorio gaseoso.

    - Relación gas/polvo de referencia: 100.
    - Vida del gas muestreada de una distribución
      exponencial con tiempo característico de 2.5 Myr.

    La relación 100 no es universal ni representa
    una medición individual de cada disco.
    """

    RELACION_GAS_POLVO_REFERENCIA = 100.0

    TIEMPO_CARACTERISTICO_MYR = 2.5

    def generar_propiedades(
        self,
        seed,
        identificador,
        masa_polvo_tierra,
    ):
        if masa_polvo_tierra < 0:
            raise ValueError("La masa de polvo no puede ser negativa.")

        masa_gas_referencia = (
            float(masa_polvo_tierra) * self.RELACION_GAS_POLVO_REFERENCIA
        )

        semilla_local = f"{int(seed)}:" f"{identificador}:" "gas_disco"

        rng = random.Random(semilla_local)

        u = rng.random()

        u = max(
            1e-12,
            min(
                1.0 - 1e-12,
                u,
            ),
        )

        vida_gas_myr = -self.TIEMPO_CARACTERISTICO_MYR * math.log(1.0 - u)

        return {
            "masa_gas_referencia_tierra": (masa_gas_referencia),
            "relacion_gas_polvo": (self.RELACION_GAS_POLVO_REFERENCIA),
            "vida_gas_myr": (vida_gas_myr),
        }
