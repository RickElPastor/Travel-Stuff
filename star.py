from format_utils import formatear_identificador


class Star:
    def __init__(
        self,
        nombre,
        masa_inicial,
        metalicidad_z,
        modelo_evolutivo=None,
        anio_nacimiento=0,
    ):
        if masa_inicial <= 0:
            raise ValueError("La masa inicial debe ser " "mayor que 0.")

        if not 0 <= metalicidad_z <= 1:
            raise ValueError("La metalicidad Z debe " "estar entre 0 y 1.")

        self.nombre = nombre

        self.masa_inicial = float(masa_inicial)

        self.masa_actual = float(masa_inicial)

        self.metalicidad_z = float(metalicidad_z)

        self.anio_nacimiento = int(anio_nacimiento)

        self.edad = 0
        self.edad_estado_modelo = 0

        self.etapa = "sin_modelar"
        self.viva = True

        self.temperatura_efectiva = None
        self.luminosidad = None
        self.radio = None

        self.masa_nucleo_helio = None
        self.masa_nucleo_carbono_oxigeno = None

        self.tipo_espectral = None

        self.tipo_remanente = None
        self.masa_remanente = None

        self.remanente_creado = False

        self.modelo_evolutivo = modelo_evolutivo

    def establecer_modelo_evolutivo(
        self,
        modelo,
    ):
        self.modelo_evolutivo = modelo

    def actualizar_estado_fisico(self):
        if self.modelo_evolutivo is None:
            return False

        estado = self.modelo_evolutivo.obtener_estado(
            masa_inicial=(self.masa_inicial),
            metalicidad_z=(self.metalicidad_z),
            edad=self.edad,
        )

        if estado.masa_actual < 0:
            raise ValueError("El modelo devolvió " "una masa negativa.")

        self.masa_actual = float(estado.masa_actual)

        self.etapa = estado.etapa
        self.viva = bool(estado.viva)

        if estado.edad_modelo_anios is not None:
            self.edad_estado_modelo = estado.edad_modelo_anios

        self.temperatura_efectiva = estado.temperatura_efectiva

        self.luminosidad = estado.luminosidad

        self.radio = estado.radio

        self.masa_nucleo_helio = estado.masa_nucleo_helio

        self.masa_nucleo_carbono_oxigeno = estado.masa_nucleo_carbono_oxigeno

        self.tipo_espectral = estado.tipo_espectral

        self.tipo_remanente = estado.tipo_remanente

        self.masa_remanente = estado.masa_remanente

        return True

    def envejecer(
        self,
        anios,
    ):
        if anios < 0:
            raise ValueError(
                "Una estrella no puede " "envejecer una cantidad " "negativa."
            )

        if not self.viva:
            return

        self.edad += anios

        self.actualizar_estado_fisico()

    def obtener_temperatura(self):
        return self.temperatura_efectiva

    def obtener_tipo_espectral(self):
        return self.tipo_espectral

    def obtener_etapa_visible(self):
        return formatear_identificador(self.etapa)

    def obtener_destino_visible(self):
        return formatear_identificador(self.tipo_remanente)

    def obtener_destino_estelar(self):
        return self.tipo_remanente

    def esta_viva(self):
        return self.viva

    def necesita_remanente(self):
        return (
            not self.viva
            and self.tipo_remanente is not None
            and self.masa_remanente is not None
            and not self.remanente_creado
        )

    def ha_finalizado(self):
        return not self.viva

    def obtener_nombre_modelo(self):
        if self.modelo_evolutivo is None:
            return "sin modelo"

        return getattr(
            self.modelo_evolutivo,
            "nombre",
            (self.modelo_evolutivo.__class__.__name__),
        )

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "masa_inicial": (self.masa_inicial),
            "masa_actual": (self.masa_actual),
            "metalicidad_z": (self.metalicidad_z),
            "anio_nacimiento": (self.anio_nacimiento),
            "edad": self.edad,
            "edad_estado_modelo": (self.edad_estado_modelo),
            "etapa": self.etapa,
            "viva": self.viva,
            "temperatura_efectiva": (self.temperatura_efectiva),
            "luminosidad": (self.luminosidad),
            "radio": self.radio,
            "masa_nucleo_helio": (self.masa_nucleo_helio),
            "masa_nucleo_carbono_oxigeno": (self.masa_nucleo_carbono_oxigeno),
            "tipo_espectral": (self.tipo_espectral),
            "tipo_remanente": (self.tipo_remanente),
            "masa_remanente": (self.masa_remanente),
            "remanente_creado": (self.remanente_creado),
            "modelo": (self.obtener_nombre_modelo()),
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
        modelo_evolutivo=None,
    ):
        estrella = cls(
            nombre=datos["nombre"],
            masa_inicial=(datos["masa_inicial"]),
            metalicidad_z=(datos["metalicidad_z"]),
            modelo_evolutivo=(modelo_evolutivo),
            anio_nacimiento=(
                datos.get(
                    "anio_nacimiento",
                    0,
                )
            ),
        )

        estrella.masa_actual = datos.get(
            "masa_actual",
            estrella.masa_inicial,
        )

        estrella.edad = datos.get(
            "edad",
            0,
        )

        estrella.edad_estado_modelo = datos.get(
            "edad_estado_modelo",
            0,
        )

        estrella.etapa = datos.get(
            "etapa",
            "sin_modelar",
        )

        estrella.viva = datos.get(
            "viva",
            True,
        )

        estrella.temperatura_efectiva = datos.get("temperatura_efectiva")

        estrella.luminosidad = datos.get("luminosidad")

        estrella.radio = datos.get("radio")

        estrella.masa_nucleo_helio = datos.get("masa_nucleo_helio")

        estrella.masa_nucleo_carbono_oxigeno = datos.get("masa_nucleo_carbono_oxigeno")

        estrella.tipo_espectral = datos.get("tipo_espectral")

        estrella.tipo_remanente = datos.get("tipo_remanente")

        estrella.masa_remanente = datos.get("masa_remanente")

        estrella.remanente_creado = datos.get(
            "remanente_creado",
            False,
        )

        return estrella
