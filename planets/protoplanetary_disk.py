class DiscoProtoplanetario:
    def __init__(
        self,
        estrella_nombre,
        masa_polvo_tierra,
        modelo,
        sistema_nombre=None,
        radio_exterior_au=None,
        truncado_por_companera=False,
    ):
        if masa_polvo_tierra < 0:
            raise ValueError("La masa de polvo no puede ser negativa.")

        if radio_exterior_au is not None and radio_exterior_au <= 0:
            raise ValueError("El radio exterior debe ser mayor que 0.")

        self.estrella_nombre = str(estrella_nombre)

        self.sistema_nombre = sistema_nombre

        self.masa_polvo_tierra = float(masa_polvo_tierra)

        self.radio_exterior_au = (
            None if radio_exterior_au is None else float(radio_exterior_au)
        )

        self.truncado_por_companera = bool(truncado_por_companera)

        self.modelo = str(modelo)

    def a_dict(self):
        return {
            "estrella_nombre": (self.estrella_nombre),
            "sistema_nombre": (self.sistema_nombre),
            "masa_polvo_tierra": (self.masa_polvo_tierra),
            "radio_exterior_au": (self.radio_exterior_au),
            "truncado_por_companera": (self.truncado_por_companera),
            "modelo": self.modelo,
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
    ):
        return cls(
            estrella_nombre=(datos["estrella_nombre"]),
            sistema_nombre=datos.get("sistema_nombre"),
            masa_polvo_tierra=(datos["masa_polvo_tierra"]),
            radio_exterior_au=datos.get("radio_exterior_au"),
            truncado_por_companera=datos.get(
                "truncado_por_companera",
                False,
            ),
            modelo=datos["modelo"],
        )
