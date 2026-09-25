class SistemaEstelar:
    def __init__(
        self,
        nombre,
        anio_formacion,
        estrellas=None,
    ):
        self.nombre = str(nombre)
        self.anio_formacion = int(anio_formacion)

        self.nombres_estrellas = []

        if estrellas:
            for estrella in estrellas:
                self.agregar_estrella(estrella)

    def agregar_estrella(
        self,
        estrella,
    ):
        if hasattr(estrella, "nombre"):
            nombre = estrella.nombre

        else:
            nombre = str(estrella)

        if nombre not in self.nombres_estrellas:
            self.nombres_estrellas.append(nombre)

    def quitar_estrella(
        self,
        estrella,
    ):
        if hasattr(estrella, "nombre"):
            nombre = estrella.nombre

        else:
            nombre = str(estrella)

        if nombre in self.nombres_estrellas:
            self.nombres_estrellas.remove(nombre)

    def obtener_cantidad_estrellas(self):
        return len(self.nombres_estrellas)

    def obtener_tipo(self):
        cantidad = self.obtener_cantidad_estrellas()

        if cantidad == 1:
            return "simple"

        if cantidad == 2:
            return "binario"

        if cantidad == 3:
            return "triple"

        if cantidad > 3:
            return "multiple"

        return "vacio"

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "anio_formacion": self.anio_formacion,
            "estrellas": list(self.nombres_estrellas),
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
    ):
        sistema = cls(
            nombre=datos["nombre"],
            anio_formacion=datos["anio_formacion"],
        )

        for nombre_estrella in datos.get(
            "estrellas",
            [],
        ):
            sistema.agregar_estrella(nombre_estrella)

        return sistema
