import math


class ModeloAguaSuperficial:
    """
    Partición preliminar del agua superficial.

    Divide el inventario disponible entre:

    - vapor atmosférico
    - agua condensada

    Usa Teq0 como temperatura térmica provisional.

    IMPORTANTE:
    Teq0 todavía NO es la temperatura superficial
    final. El clima y el efecto invernadero se
    calcularán después.
    """

    MASA_TIERRA_KG = 5.9722e24
    RADIO_TIERRA_M = 6.371e6

    PA_POR_BAR = 100_000.0

    T_TRIPLE_K = 273.16
    P_TRIPLE_PA = 611.657

    R_VAPOR_AGUA = 461.5

    CALOR_LATENTE_VAPORIZACION = 2.50e6
    CALOR_LATENTE_SUBLIMACION = 2.834e6

    MASA_MOLAR_CO2 = 44.0095
    MASA_MOLAR_C = 12.011

    def evaluar(
        self,
        planeta,
    ):
        self.limpiar(planeta)

        if not planeta.candidato_terrestre_hz:
            return

        if not planeta.retencion_atmosferica_aprox:
            return

        if planeta.temperatura_equilibrio_cero_albedo_k is None:
            return

        if planeta.radio_tierra is None or planeta.radio_tierra <= 0:
            return

        if (
            planeta.gravedad_superficial_ms2 is None
            or planeta.gravedad_superficial_ms2 <= 0
        ):
            return

        agua_acrecion = self._valor_o_cero(planeta.masa_agua_inicial_tierra)

        agua_desgasificada = self._valor_o_cero(planeta.h2o_desgasificada_tierra)

        agua_total = agua_acrecion + agua_desgasificada

        planeta.masa_agua_superficial_total_tierra = agua_total

        if agua_total <= 0:
            planeta.estado_agua_preclima = "sin_agua"

            self._calcular_presiones_secas(planeta)

            return

        temperatura = planeta.temperatura_equilibrio_cero_albedo_k

        presion_saturacion_bar = self._calcular_presion_saturacion_bar(temperatura)

        masa_vapor_maxima = self._presion_a_masa_tierra(
            planeta,
            presion_saturacion_bar,
        )

        masa_vapor = min(
            agua_total,
            masa_vapor_maxima,
        )

        masa_condensada = max(
            0.0,
            agua_total - masa_vapor,
        )

        presion_h2o = self._masa_a_presion_bar(
            planeta,
            masa_vapor,
        )

        planeta.masa_h2o_vapor_tierra = masa_vapor

        planeta.masa_h2o_condensada_tierra = masa_condensada

        planeta.presion_h2o_preclima_bar = presion_h2o

        planeta.tiene_agua_condensada = masa_condensada > 0

        if masa_condensada > 0:
            if temperatura < self.T_TRIPLE_K:
                planeta.estado_agua_preclima = "hielo"

            else:
                planeta.estado_agua_preclima = "liquida"

        else:
            planeta.estado_agua_preclima = "vapor"

        self._calcular_presiones_secas(planeta)

    def _calcular_presion_saturacion_bar(
        self,
        temperatura,
    ):
        if temperatura <= 0:
            return 0.0

        if temperatura < self.T_TRIPLE_K:
            calor_latente = self.CALOR_LATENTE_SUBLIMACION

        else:
            calor_latente = self.CALOR_LATENTE_VAPORIZACION

        exponente = (
            -calor_latente
            / self.R_VAPOR_AGUA
            * (1.0 / temperatura - 1.0 / self.T_TRIPLE_K)
        )

        presion_pa = self.P_TRIPLE_PA * math.exp(exponente)

        return presion_pa / self.PA_POR_BAR

    def _calcular_presiones_secas(
        self,
        planeta,
    ):
        carbono = self._valor_o_cero(planeta.carbono_desgasificado_tierra)

        nitrogeno = self._valor_o_cero(planeta.nitrogeno_desgasificado_tierra)

        masa_co2 = carbono * (self.MASA_MOLAR_CO2 / self.MASA_MOLAR_C)

        masa_n2 = nitrogeno

        presion_co2 = self._masa_a_presion_bar(
            planeta,
            masa_co2,
        )

        presion_n2 = self._masa_a_presion_bar(
            planeta,
            masa_n2,
        )

        presion_h2o = (
            planeta.presion_h2o_preclima_bar
            if planeta.presion_h2o_preclima_bar is not None
            else 0.0
        )

        planeta.presion_co2_preclima_bar = presion_co2

        planeta.presion_n2_preclima_bar = presion_n2

        planeta.presion_atmosferica_preclima_bar = (
            presion_h2o + presion_co2 + presion_n2
        )

    def _masa_a_presion_bar(
        self,
        planeta,
        masa_tierra,
    ):
        if masa_tierra <= 0:
            return 0.0

        masa_kg = masa_tierra * self.MASA_TIERRA_KG

        radio_m = planeta.radio_tierra * self.RADIO_TIERRA_M

        area = 4.0 * math.pi * radio_m**2

        presion_pa = masa_kg * planeta.gravedad_superficial_ms2 / area

        return presion_pa / self.PA_POR_BAR

    def _presion_a_masa_tierra(
        self,
        planeta,
        presion_bar,
    ):
        if presion_bar <= 0:
            return 0.0

        presion_pa = presion_bar * self.PA_POR_BAR

        radio_m = planeta.radio_tierra * self.RADIO_TIERRA_M

        area = 4.0 * math.pi * radio_m**2

        masa_kg = presion_pa * area / planeta.gravedad_superficial_ms2

        return masa_kg / self.MASA_TIERRA_KG

    def _valor_o_cero(
        self,
        valor,
    ):
        if valor is None:
            return 0.0

        return max(
            0.0,
            float(valor),
        )

    def limpiar(
        self,
        planeta,
    ):
        planeta.masa_agua_superficial_total_tierra = None

        planeta.masa_h2o_vapor_tierra = None
        planeta.masa_h2o_condensada_tierra = None

        planeta.presion_h2o_preclima_bar = None
        planeta.presion_co2_preclima_bar = None
        planeta.presion_n2_preclima_bar = None

        planeta.presion_atmosferica_preclima_bar = None

        planeta.tiene_agua_condensada = False
        planeta.estado_agua_preclima = None
