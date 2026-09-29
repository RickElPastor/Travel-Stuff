import math


class ModeloAtmosferaSecundaria:
    """
    Atmósfera secundaria bruta de Fase 1.

    Convierte los volátiles desgasificados en:

    H2O
    CO2
    N2

    La presión calculada supone que todo ese
    material permanece inicialmente en fase gaseosa.

    La condensación de H2O y la regulación de CO2
    se modelarán después.
    """

    MASA_TIERRA_KG = 5.9722e24
    RADIO_TIERRA_M = 6.371e6

    PA_POR_BAR = 100_000.0

    MASA_MOLAR_H2O = 18.01528
    MASA_MOLAR_CO2 = 44.0095
    MASA_MOLAR_N2 = 28.0134
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

        if planeta.radio_tierra is None or planeta.radio_tierra <= 0:
            return

        if (
            planeta.gravedad_superficial_ms2 is None
            or planeta.gravedad_superficial_ms2 <= 0
        ):
            return

        masa_h2o = self._valor_o_cero(planeta.h2o_desgasificada_tierra)

        masa_carbono = self._valor_o_cero(planeta.carbono_desgasificado_tierra)

        masa_nitrogeno = self._valor_o_cero(planeta.nitrogeno_desgasificado_tierra)

        masa_co2 = masa_carbono * (self.MASA_MOLAR_CO2 / self.MASA_MOLAR_C)

        # El nitrógeno cambia de forma química
        # a N2, pero su masa total de N se conserva.
        masa_n2 = masa_nitrogeno

        masa_total = masa_h2o + masa_co2 + masa_n2

        if masa_total <= 0:
            return

        presion_total = self._calcular_presion_bar(
            planeta,
            masa_total,
        )

        (
            fraccion_h2o,
            fraccion_co2,
            fraccion_n2,
        ) = self._calcular_fracciones_molares(
            masa_h2o,
            masa_co2,
            masa_n2,
        )

        planeta.tiene_atmosfera_secundaria = True

        planeta.masa_atmosfera_secundaria_tierra = masa_total

        planeta.presion_atmosferica_bruta_bar = presion_total

        planeta.fraccion_molar_h2o_bruta = fraccion_h2o

        planeta.fraccion_molar_co2_bruta = fraccion_co2

        planeta.fraccion_molar_n2_bruta = fraccion_n2

    def _calcular_presion_bar(
        self,
        planeta,
        masa_atmosfera_tierra,
    ):
        masa_atmosfera_kg = masa_atmosfera_tierra * self.MASA_TIERRA_KG

        radio_m = planeta.radio_tierra * self.RADIO_TIERRA_M

        area = 4.0 * math.pi * radio_m**2

        presion_pa = masa_atmosfera_kg * planeta.gravedad_superficial_ms2 / area

        return presion_pa / self.PA_POR_BAR

    def _calcular_fracciones_molares(
        self,
        masa_h2o,
        masa_co2,
        masa_n2,
    ):
        # Para calcular proporciones molares no
        # necesitamos convertir M_tierra a gramos:
        # el factor común se cancela.
        moles_h2o = masa_h2o / self.MASA_MOLAR_H2O

        moles_co2 = masa_co2 / self.MASA_MOLAR_CO2

        moles_n2 = masa_n2 / self.MASA_MOLAR_N2

        moles_totales = moles_h2o + moles_co2 + moles_n2

        if moles_totales <= 0:
            return (
                0.0,
                0.0,
                0.0,
            )

        return (
            moles_h2o / moles_totales,
            moles_co2 / moles_totales,
            moles_n2 / moles_totales,
        )

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
        planeta.tiene_atmosfera_secundaria = False

        planeta.masa_atmosfera_secundaria_tierra = None

        planeta.presion_atmosferica_bruta_bar = None

        planeta.fraccion_molar_h2o_bruta = None
        planeta.fraccion_molar_co2_bruta = None
        planeta.fraccion_molar_n2_bruta = None
