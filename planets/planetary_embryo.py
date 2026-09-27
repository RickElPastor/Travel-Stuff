class EmbrionPlanetario:
    def __init__(
        self,
        nombre,
        estrella_nombre,
        sistema_nombre,
        masa_tierra,
        semieje_mayor_au,
        zona_material=None,
    ):
        if masa_tierra <= 0:
            raise ValueError("La masa del embrión debe ser mayor que 0.")

        if semieje_mayor_au <= 0:
            raise ValueError("El semieje mayor debe ser mayor que 0.")

        self.nombre = str(nombre)

        self.estrella_nombre = str(estrella_nombre)

        self.sistema_nombre = sistema_nombre

        self.masa_tierra = float(masa_tierra)

        self.semieje_mayor_au = float(semieje_mayor_au)

        self.zona_material = zona_material

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "estrella_nombre": (self.estrella_nombre),
            "sistema_nombre": (self.sistema_nombre),
            "masa_tierra": (self.masa_tierra),
            "semieje_mayor_au": (self.semieje_mayor_au),
            "zona_material": (self.zona_material),
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
    ):
        return cls(
            nombre=datos["nombre"],
            estrella_nombre=(datos["estrella_nombre"]),
            sistema_nombre=datos.get("sistema_nombre"),
            masa_tierra=(datos["masa_tierra"]),
            semieje_mayor_au=(datos["semieje_mayor_au"]),
            zona_material=datos.get("zona_material"),
        )
