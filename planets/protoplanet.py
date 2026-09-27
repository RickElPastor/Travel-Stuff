class Protoplaneta:
    def __init__(
        self,
        nombre,
        estrella_nombre,
        sistema_nombre,
        masa_tierra,
        semieje_mayor_au,
        zona_material=None,
        embriones_fusionados=1,
    ):
        if masa_tierra <= 0:
            raise ValueError("La masa del protoplaneta debe ser mayor que 0.")

        if semieje_mayor_au <= 0:
            raise ValueError("El semieje mayor debe ser mayor que 0.")

        if embriones_fusionados < 1:
            raise ValueError("Debe existir al menos un embrión de origen.")

        self.nombre = str(nombre)

        self.estrella_nombre = str(estrella_nombre)

        self.sistema_nombre = sistema_nombre

        self.masa_tierra = float(masa_tierra)

        self.semieje_mayor_au = float(semieje_mayor_au)

        self.zona_material = zona_material

        self.embriones_fusionados = int(embriones_fusionados)

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "estrella_nombre": (self.estrella_nombre),
            "sistema_nombre": (self.sistema_nombre),
            "masa_tierra": (self.masa_tierra),
            "semieje_mayor_au": (self.semieje_mayor_au),
            "zona_material": (self.zona_material),
            "embriones_fusionados": (self.embriones_fusionados),
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
            embriones_fusionados=datos.get(
                "embriones_fusionados",
                1,
            ),
        )
