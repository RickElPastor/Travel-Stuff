import math

from planets.planetary_embryo import (
    EmbrionPlanetario,
)


class ModeloFormacionEmbriones:
    """
    Formación oligárquica simplificada.

    Los embriones se forman usando la densidad
    superficial local de sólidos y una separación
    basada en radios de Hill mutuos.
    """

    MASAS_TIERRA_POR_MSOL = 332946.0

    SEPARACION_HILL = 8.0

    FRACCION_MASA_EMBRIONES = 0.60

    # Aproximadamente una masa lunar.
    # Por debajo de esto el material permanece
    # representado como planetesimales.
    MASA_MIN_EMBRION_TIERRA = 0.01

    MAX_EMBRIONES_POR_DISCO = 200

    def generar_embriones(
        self,
        disco,
    ):
        if disco.masa_estelar_msol is None:
            return []

        if disco.masa_estelar_msol <= 0:
            return []

        radio_exterior = disco.obtener_radio_exterior_efectivo_au()

        if radio_exterior is None:
            return []

        radio = disco.radio_interior_au

        masa_estelar_tierra = disco.masa_estelar_msol * self.MASAS_TIERRA_POR_MSOL

        presupuesto = disco.masa_polvo_tierra * self.FRACCION_MASA_EMBRIONES

        masa_usada = 0.0

        embriones = []

        indice = 1

        while (
            radio < radio_exterior
            and masa_usada < presupuesto
            and len(embriones) < self.MAX_EMBRIONES_POR_DISCO
        ):
            densidad = disco.obtener_densidad_superficial_polvo(radio)

            if densidad <= 0:
                break

            masa_emb = self._calcular_masa_aislamiento(
                radio_au=radio,
                densidad_solidos=densidad,
                masa_estelar_tierra=(masa_estelar_tierra),
            )

            if masa_emb <= 0:
                break

            radio_hill = self._calcular_radio_hill_mutuo(
                radio_au=radio,
                masa_emb_tierra=masa_emb,
                masa_estelar_tierra=(masa_estelar_tierra),
            )

            separacion = self.SEPARACION_HILL * radio_hill

            if separacion <= 0:
                break

            if masa_emb >= self.MASA_MIN_EMBRION_TIERRA:
                masa_restante = presupuesto - masa_usada

                masa_final = min(
                    masa_emb,
                    masa_restante,
                )

                if masa_final >= self.MASA_MIN_EMBRION_TIERRA:
                    zona_material = self._obtener_zona_material(
                        disco,
                        radio,
                    )

                    embrion = EmbrionPlanetario(
                        nombre=(
                            f"Embrion-" f"{disco.estrella_nombre}-" f"{indice:03d}"
                        ),
                        estrella_nombre=(disco.estrella_nombre),
                        sistema_nombre=(disco.sistema_nombre),
                        masa_tierra=(masa_final),
                        semieje_mayor_au=(radio),
                        zona_material=(zona_material),
                    )

                    embriones.append(embrion)

                    masa_usada += masa_final

                    indice += 1

            radio += separacion

        return embriones

    def _calcular_masa_aislamiento(
        self,
        radio_au,
        densidad_solidos,
        masa_estelar_tierra,
    ):
        factor_hill = (2.0 / (3.0 * masa_estelar_tierra)) ** (1.0 / 3.0)

        termino = (
            2.0
            * math.pi
            * self.SEPARACION_HILL
            * radio_au**2
            * densidad_solidos
            * self.FRACCION_MASA_EMBRIONES
            * factor_hill
        )

        return termino**1.5

    def _calcular_radio_hill_mutuo(
        self,
        radio_au,
        masa_emb_tierra,
        masa_estelar_tierra,
    ):
        return radio_au * ((2.0 * masa_emb_tierra) / (3.0 * masa_estelar_tierra)) ** (
            1.0 / 3.0
        )

    def _obtener_zona_material(
        self,
        disco,
        radio_au,
    ):
        if disco.linea_hielo_au is None:
            return "sin_clasificar"

        if radio_au < disco.linea_hielo_au:
            return "interior_hielo"

        return "exterior_hielo"
