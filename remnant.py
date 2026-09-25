from format_utils import formatear_identificador


class RemanenteEstelar:
    def __init__(
        self, nombre, tipo, masa, origen=None, nombre_origen=None, anio_formacion=None
    ):
        if masa < 0:
            raise ValueError("La masa del remanente " "no puede ser negativa.")

        self.nombre = nombre
        self.tipo = tipo
        self.masa = float(masa)

        self.origen = origen

        if origen is not None:
            self.nombre_origen = origen.nombre
        else:
            self.nombre_origen = nombre_origen

        self.anio_formacion = anio_formacion

    def establecer_origen(self, estrella):
        self.origen = estrella
        self.nombre_origen = estrella.nombre

    def obtener_descripcion(self):
        return (
            f"{self.nombre} - "
            f"Tipo: {self.obtener_tipo_visible()} - "
            f"Masa: {self.masa:.3f} masas solares"
        )

    def obtener_tipo_visible(self):
        return formatear_identificador(self.tipo)

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "masa": self.masa,
            "origen": self.nombre_origen,
            "anio_formacion": self.anio_formacion,
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            nombre=datos["nombre"],
            tipo=datos["tipo"],
            masa=datos["masa"],
            origen=None,
            nombre_origen=datos.get("origen"),
            anio_formacion=datos.get("anio_formacion"),
        )
