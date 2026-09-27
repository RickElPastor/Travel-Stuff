from planets.planet import Planet


class ModeloFormacionPlanetasSolidos:
    """
    Convierte los protoplanetas resultantes de la
    fase de impactos gigantes en planetas sólidos.

    No añade gas.
    """

    MASA_NUCLEO_CANDIDATO_GAS = 10.0

    def generar_planetas(
        self,
        disco,
    ):
        planetas = []

        for indice, protoplaneta in enumerate(
            disco.protoplanetas,
            start=1,
        ):
            composicion = self._clasificar_composicion(protoplaneta.zona_material)

            candidato_gas = protoplaneta.masa_tierra >= self.MASA_NUCLEO_CANDIDATO_GAS

            planeta = Planet(
                nombre=(f"Planeta-" f"{disco.estrella_nombre}-" f"{indice:03d}"),
                masa_tierra=(protoplaneta.masa_tierra),
                masa_solida_tierra=(protoplaneta.masa_tierra),
                masa_gas_tierra=0.0,
                semieje_mayor_au=(protoplaneta.semieje_mayor_au),
                excentricidad=0.0,
                sistema_nombre=(disco.sistema_nombre),
                estrella_anfitriona=(disco.estrella_nombre),
                tipo_orbita=("circumestelar"),
                composicion_inicial=(composicion),
                candidato_captura_gas=(candidato_gas),
                origen_protoplaneta=(protoplaneta.nombre),
                embriones_fusionados=(protoplaneta.embriones_fusionados),
            )

            planetas.append(planeta)

        return planetas

    def _clasificar_composicion(
        self,
        zona_material,
    ):
        if zona_material == "interior_hielo":
            return "rocosa"

        if zona_material == "exterior_hielo":
            return "rica_en_hielos"

        if zona_material == "mixta":
            return "mixta"

        return "indeterminada"
