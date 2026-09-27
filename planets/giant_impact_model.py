import math

from planets.protoplanet import (
    Protoplaneta,
)


class ModeloImpactosGigantes:
    """
    Aproximación determinista de Fase 1.

    Fusiona cuerpos vecinos demasiado próximos
    en radios de Hill mutuos.

    No es una integración N-body.
    """

    MASAS_TIERRA_POR_MSOL = 332946.0

    SEPARACION_OBJETIVO_HILL = 20.0

    def generar_protoplanetas(
        self,
        disco,
    ):
        if disco.masa_estelar_msol is None:
            return []

        if disco.masa_estelar_msol <= 0:
            return []

        if not disco.embriones:
            return []

        masa_estelar_tierra = disco.masa_estelar_msol * self.MASAS_TIERRA_POR_MSOL

        protoplanetas = [self._desde_embrion(embrion) for embrion in disco.embriones]

        protoplanetas.sort(key=lambda cuerpo: (cuerpo.semieje_mayor_au))

        hubo_fusion = True

        while hubo_fusion:
            hubo_fusion = False

            nuevos = []

            indice = 0

            while indice < len(protoplanetas):
                actual = protoplanetas[indice]

                if indice + 1 >= len(protoplanetas):
                    nuevos.append(actual)

                    indice += 1

                    continue

                siguiente = protoplanetas[indice + 1]

                separacion_hill = self._calcular_separacion_hill(
                    actual,
                    siguiente,
                    masa_estelar_tierra,
                )

                if separacion_hill < self.SEPARACION_OBJETIVO_HILL:
                    fusionado = self._fusionar(
                        actual,
                        siguiente,
                    )

                    nuevos.append(fusionado)

                    indice += 2

                    hubo_fusion = True

                else:
                    nuevos.append(actual)

                    indice += 1

            protoplanetas = sorted(
                nuevos,
                key=lambda cuerpo: (cuerpo.semieje_mayor_au),
            )

        for indice, protoplaneta in enumerate(
            protoplanetas,
            start=1,
        ):
            protoplaneta.nombre = (
                f"Protoplaneta-" f"{disco.estrella_nombre}-" f"{indice:03d}"
            )

        return protoplanetas

    def _desde_embrion(
        self,
        embrion,
    ):
        return Protoplaneta(
            nombre=embrion.nombre,
            estrella_nombre=(embrion.estrella_nombre),
            sistema_nombre=(embrion.sistema_nombre),
            masa_tierra=(embrion.masa_tierra),
            semieje_mayor_au=(embrion.semieje_mayor_au),
            zona_material=(embrion.zona_material),
            embriones_fusionados=1,
        )

    def _calcular_separacion_hill(
        self,
        cuerpo_1,
        cuerpo_2,
        masa_estelar_tierra,
    ):
        a_1 = cuerpo_1.semieje_mayor_au

        a_2 = cuerpo_2.semieje_mayor_au

        masa_total = cuerpo_1.masa_tierra + cuerpo_2.masa_tierra

        semieje_promedio = (a_1 + a_2) / 2.0

        radio_hill_mutuo = semieje_promedio * (
            masa_total / (3.0 * masa_estelar_tierra)
        ) ** (1.0 / 3.0)

        if radio_hill_mutuo <= 0:
            return float("inf")

        return (a_2 - a_1) / radio_hill_mutuo

    def _fusionar(
        self,
        cuerpo_1,
        cuerpo_2,
    ):
        masa_total = cuerpo_1.masa_tierra + cuerpo_2.masa_tierra

        # Aproximación:
        # conservamos el momento angular orbital
        # suponiendo órbitas inicialmente circulares,
        # coplanares y una fusión perfecta.
        raiz_a_nueva = (
            (cuerpo_1.masa_tierra * math.sqrt(cuerpo_1.semieje_mayor_au))
            + (cuerpo_2.masa_tierra * math.sqrt(cuerpo_2.semieje_mayor_au))
        ) / masa_total

        semieje_nuevo = raiz_a_nueva**2

        if cuerpo_1.zona_material == cuerpo_2.zona_material:
            zona_material = cuerpo_1.zona_material

        else:
            zona_material = "mixta"

        return Protoplaneta(
            nombre=(cuerpo_1.nombre),
            estrella_nombre=(cuerpo_1.estrella_nombre),
            sistema_nombre=(cuerpo_1.sistema_nombre),
            masa_tierra=(masa_total),
            semieje_mayor_au=(semieje_nuevo),
            zona_material=(zona_material),
            embriones_fusionados=(
                cuerpo_1.embriones_fusionados + cuerpo_2.embriones_fusionados
            ),
        )
