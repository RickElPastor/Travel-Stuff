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
        masa_interior_hielo_tierra=None,
        masa_exterior_hielo_tierra=None,
        masa_sin_clasificar_tierra=None,
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

        if (
            masa_interior_hielo_tierra is None
            and masa_exterior_hielo_tierra is None
            and masa_sin_clasificar_tierra is None
        ):
            self.masa_interior_hielo_tierra = (
                self.masa_tierra if self.zona_material == "interior_hielo" else 0.0
            )

            self.masa_exterior_hielo_tierra = (
                self.masa_tierra if self.zona_material == "exterior_hielo" else 0.0
            )

            self.masa_sin_clasificar_tierra = (
                self.masa_tierra
                if self.zona_material
                not in {
                    "interior_hielo",
                    "exterior_hielo",
                }
                else 0.0
            )

        else:
            self.masa_interior_hielo_tierra = float(masa_interior_hielo_tierra or 0.0)

            self.masa_exterior_hielo_tierra = float(masa_exterior_hielo_tierra or 0.0)

            self.masa_sin_clasificar_tierra = float(masa_sin_clasificar_tierra or 0.0)

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "estrella_nombre": (self.estrella_nombre),
            "sistema_nombre": (self.sistema_nombre),
            "masa_tierra": (self.masa_tierra),
            "semieje_mayor_au": (self.semieje_mayor_au),
            "zona_material": (self.zona_material),
            "embriones_fusionados": (self.embriones_fusionados),
            "masa_interior_hielo_tierra": (self.masa_interior_hielo_tierra),
            "masa_exterior_hielo_tierra": (self.masa_exterior_hielo_tierra),
            "masa_sin_clasificar_tierra": (self.masa_sin_clasificar_tierra),
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
            masa_interior_hielo_tierra=datos.get("masa_interior_hielo_tierra"),
            masa_exterior_hielo_tierra=datos.get("masa_exterior_hielo_tierra"),
            masa_sin_clasificar_tierra=datos.get("masa_sin_clasificar_tierra"),
        )
