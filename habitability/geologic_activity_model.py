import math


class ModeloActividadGeologica:
    """
    Aproximación térmica de Fase 1.

    Representa la disminución de la actividad
    geológica conforme un planeta envejece.

    NO modela explícitamente:
    - tectónica de placas
    - convección del manto
    - radionúclidos
    - viscosidad
    - plumas mantélicas

    La masa modifica la escala de enfriamiento:
    planetas mayores conservan calor durante
    más tiempo.
    """

    TAU_TIERRA_GYR = 4.0

    ACTIVIDAD_MIN_DESGASIFICACION = 0.05

    def evaluar(
        self,
        planeta,
        edad_planeta_anios,
    ):
        self.limpiar(planeta)

        if planeta.masa_solida_tierra <= 0:
            return

        if edad_planeta_anios is None:
            return

        if edad_planeta_anios < 0:
            return

        edad_gyr = edad_planeta_anios / 1_000_000_000.0

        escala_enfriamiento_gyr = self.TAU_TIERRA_GYR * math.sqrt(
            planeta.masa_solida_tierra
        )

        if escala_enfriamiento_gyr <= 0:
            return

        actividad = math.exp(-edad_gyr / escala_enfriamiento_gyr)

        fraccion_desgasificada = 1.0 - actividad

        planeta.actividad_geologica_relativa = actividad

        planeta.fraccion_volatiles_desgasificada = fraccion_desgasificada

        planeta.geologicamente_activo = actividad >= self.ACTIVIDAD_MIN_DESGASIFICACION

        self._calcular_volatiles_desgasificados(
            planeta,
            fraccion_desgasificada,
        )

    def _calcular_volatiles_desgasificados(
        self,
        planeta,
        fraccion,
    ):
        planeta.h2o_desgasificada_tierra = self._extraer_fraccion(
            planeta.reservorio_h2o_interior_tierra,
            fraccion,
        )

        planeta.carbono_desgasificado_tierra = self._extraer_fraccion(
            planeta.reservorio_carbono_tierra,
            fraccion,
        )

        planeta.nitrogeno_desgasificado_tierra = self._extraer_fraccion(
            planeta.reservorio_nitrogeno_tierra,
            fraccion,
        )

    def _extraer_fraccion(
        self,
        reservorio,
        fraccion,
    ):
        if reservorio is None:
            return None

        return reservorio * fraccion

    def limpiar(
        self,
        planeta,
    ):
        planeta.actividad_geologica_relativa = None

        planeta.fraccion_volatiles_desgasificada = None

        planeta.geologicamente_activo = False

        planeta.h2o_desgasificada_tierra = None
        planeta.carbono_desgasificado_tierra = None
        planeta.nitrogeno_desgasificado_tierra = None
