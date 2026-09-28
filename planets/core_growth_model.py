import math


class ModeloCrecimientoNucleo:
    """
    Tiempo de crecimiento oligárquico simplificado.

    Integra el crecimiento desde 0.01 M_tierra
    hasta un núcleo de 10 M_tierra usando una
    parametrización de acreción oligárquica.

    Se supone que las densidades superficiales
    locales permanecen constantes durante
    esta integración.
    """

    MASA_NUCLEO_OBJETIVO_TIERRA = 10.0
    MASA_INICIAL_TIERRA = 0.01

    B_ZONA_ALIMENTACION = 10.0

    MASA_PLANETESIMAL_G = 1.0e18

    MASA_TIERRA_G = 5.9722e27
    AU_CM = 1.495978707e13

    def calcular_tiempo_nucleo_myr(
        self,
        disco,
        planeta,
    ):
        if planeta.masa_solida_tierra < self.MASA_NUCLEO_OBJETIVO_TIERRA:
            return None

        if disco.masa_estelar_msol is None:
            return None

        if disco.masa_estelar_msol <= 0:
            return None

        if disco.relacion_gas_polvo is None or disco.relacion_gas_polvo <= 0:
            return None

        radio_au = planeta.semieje_mayor_au

        densidad_polvo = disco.obtener_densidad_superficial_polvo(radio_au)

        if densidad_polvo <= 0:
            return None

        sigma_solidos = self._convertir_masas_tierra_au2_a_g_cm2(densidad_polvo)

        sigma_gas = sigma_solidos * disco.relacion_gas_polvo

        if sigma_gas <= 0:
            return None

        tau_objetivo_anios = self._calcular_tau_caracteristico_anios(
            sigma_solidos=sigma_solidos,
            sigma_gas=sigma_gas,
            radio_au=radio_au,
            masa_nucleo_tierra=(self.MASA_NUCLEO_OBJETIVO_TIERRA),
            masa_estelar_msol=(disco.masa_estelar_msol),
        )

        masa_objetivo = self.MASA_NUCLEO_OBJETIVO_TIERRA

        masa_inicial = self.MASA_INICIAL_TIERRA

        constante_crecimiento = tau_objetivo_anios / masa_objetivo ** (1.0 / 3.0)

        tiempo_integrado_anios = (
            3.0
            * constante_crecimiento
            * (masa_objetivo ** (1.0 / 3.0) - masa_inicial ** (1.0 / 3.0))
        )

        return tiempo_integrado_anios / 1_000_000.0

    def _calcular_tau_caracteristico_anios(
        self,
        sigma_solidos,
        sigma_gas,
        radio_au,
        masa_nucleo_tierra,
        masa_estelar_msol,
    ):
        factor_zona = (self.B_ZONA_ALIMENTACION / 10.0) ** (-1.0 / 5.0)

        factor_gas = (sigma_gas / 2400.0) ** (-1.0 / 5.0)

        factor_radio_debil = radio_au ** (1.0 / 20.0)

        factor_planetesimal = (self.MASA_PLANETESIMAL_G / 1.0e18) ** (1.0 / 15.0)

        corchete = factor_zona * factor_gas * factor_radio_debil * factor_planetesimal

        return (
            1.2e5
            * (sigma_solidos / 10.0) ** -1.0
            * radio_au**0.5
            * masa_nucleo_tierra ** (1.0 / 3.0)
            * masa_estelar_msol ** (-1.0 / 6.0)
            * corchete**2
        )

    def _convertir_masas_tierra_au2_a_g_cm2(
        self,
        valor,
    ):
        return float(valor) * self.MASA_TIERRA_G / self.AU_CM**2
