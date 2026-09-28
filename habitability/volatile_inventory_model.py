class ModeloInventarioVolatiles:
    """
    Inventario inicial de agua de Fase 1.

    Prescripción adoptada:

    material interior de la línea de hielo:
        0% H2O

    material exterior:
        5% H2O

    No representa agua líquida superficial.

    Es el inventario de agua incorporado en los
    sólidos durante la formación.
    """

    FRACCION_AGUA_INTERIOR = 0.0
    FRACCION_AGUA_EXTERIOR = 0.05

    def evaluar(
        self,
        planeta,
    ):
        planeta.masa_agua_inicial_tierra = None
        planeta.fraccion_agua_inicial = None

        if planeta.masa_solida_tierra <= 0:
            return

        if (
            planeta.masa_material_interior_hielo_tierra is None
            or planeta.masa_material_exterior_hielo_tierra is None
        ):
            return

        agua_interior = (
            planeta.masa_material_interior_hielo_tierra * self.FRACCION_AGUA_INTERIOR
        )

        agua_exterior = (
            planeta.masa_material_exterior_hielo_tierra * self.FRACCION_AGUA_EXTERIOR
        )

        masa_agua = agua_interior + agua_exterior

        planeta.masa_agua_inicial_tierra = masa_agua

        planeta.fraccion_agua_inicial = masa_agua / planeta.masa_solida_tierra
