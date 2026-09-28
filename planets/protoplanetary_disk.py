import math

from planets.planetary_embryo import (
    EmbrionPlanetario,
)
from planets.protoplanet import (
    Protoplaneta,
)


class DiscoProtoplanetario:
    def __init__(
        self,
        estrella_nombre,
        masa_polvo_tierra,
        modelo,
        sistema_nombre=None,
        masa_estelar_msol=None,
        radio_exterior_au=None,
        truncado_por_companera=False,
        radio_caracteristico_au=None,
        radio_interior_au=0.05,
        gamma_perfil=1.0,
        linea_hielo_au=None,
        embriones=None,
        protoplanetas=None,
        masa_planetesimales_tierra=None,
        masa_gas_referencia_tierra=None,
        relacion_gas_polvo=None,
        vida_gas_myr=None,
        masa_gas_capturada_tierra=0.0,
        masa_gas_no_capturada_tierra=None,
        masa_gas_runaway_capturada_tierra=0.0,
    ):
        if masa_polvo_tierra < 0:
            raise ValueError("La masa de polvo no puede ser negativa.")

        if radio_exterior_au is not None and radio_exterior_au <= 0:
            raise ValueError("El radio exterior debe ser mayor que 0.")

        if radio_caracteristico_au is not None and radio_caracteristico_au <= 0:
            raise ValueError("El radio característico debe ser mayor que 0.")

        if radio_interior_au <= 0:
            raise ValueError("El radio interior debe ser mayor que 0.")

        if linea_hielo_au is not None and linea_hielo_au <= 0:
            raise ValueError("La línea de hielo debe ser mayor que 0.")

        self.estrella_nombre = str(estrella_nombre)

        self.sistema_nombre = sistema_nombre

        self.masa_estelar_msol = (
            None if masa_estelar_msol is None else float(masa_estelar_msol)
        )

        self.masa_polvo_tierra = float(masa_polvo_tierra)

        self.radio_exterior_au = (
            None if radio_exterior_au is None else float(radio_exterior_au)
        )

        self.truncado_por_companera = bool(truncado_por_companera)

        self.radio_caracteristico_au = (
            None if radio_caracteristico_au is None else float(radio_caracteristico_au)
        )

        self.radio_interior_au = float(radio_interior_au)

        self.gamma_perfil = float(gamma_perfil)

        self.linea_hielo_au = None if linea_hielo_au is None else float(linea_hielo_au)

        self.modelo = str(modelo)

        self.embriones = list(embriones if embriones is not None else [])

        self.protoplanetas = list(protoplanetas if protoplanetas is not None else [])

        self.masa_planetesimales_tierra = (
            self.masa_polvo_tierra
            if masa_planetesimales_tierra is None
            else float(masa_planetesimales_tierra)
        )

        self.masa_gas_referencia_tierra = (
            None
            if masa_gas_referencia_tierra is None
            else float(masa_gas_referencia_tierra)
        )

        self.relacion_gas_polvo = (
            None if relacion_gas_polvo is None else float(relacion_gas_polvo)
        )

        self.vida_gas_myr = None if vida_gas_myr is None else float(vida_gas_myr)

        self.masa_gas_capturada_tierra = float(masa_gas_capturada_tierra)

        self.masa_gas_no_capturada_tierra = (
            self.masa_gas_referencia_tierra
            if masa_gas_no_capturada_tierra is None
            else float(masa_gas_no_capturada_tierra)
        )

        self.masa_gas_runaway_capturada_tierra = float(
            masa_gas_runaway_capturada_tierra
        )

    def obtener_fraccion_polvo_entre(
        self,
        radio_min_au,
        radio_max_au,
    ):
        if self.radio_caracteristico_au is None:
            return 0.0

        if self.gamma_perfil != 1.0:
            raise NotImplementedError("El cálculo actual requiere gamma = 1.")

        radio_min = max(
            float(radio_min_au),
            self.radio_interior_au,
        )

        radio_max = float(radio_max_au)

        if self.radio_exterior_au is not None:
            radio_max = min(
                radio_max,
                self.radio_exterior_au,
            )

        if radio_max <= radio_min:
            return 0.0

        rc = self.radio_caracteristico_au

        limite_interior = self.radio_interior_au

        limite_exterior = self.radio_exterior_au

        masa_normalizada_total = math.exp(-limite_interior / rc)

        if limite_exterior is not None:
            masa_normalizada_total -= math.exp(-limite_exterior / rc)

        if masa_normalizada_total <= 0:
            return 0.0

        masa_intervalo = math.exp(-radio_min / rc) - math.exp(-radio_max / rc)

        fraccion = masa_intervalo / masa_normalizada_total

        return max(
            0.0,
            min(
                1.0,
                fraccion,
            ),
        )

    def obtener_densidad_superficial_polvo(
        self,
        radio_au,
    ):
        if self.radio_caracteristico_au is None:
            return 0.0

        if self.gamma_perfil != 1.0:
            raise NotImplementedError("La densidad actual requiere gamma = 1.")

        radio = float(radio_au)

        if radio < self.radio_interior_au:
            return 0.0

        if self.radio_exterior_au is not None and radio > self.radio_exterior_au:
            return 0.0

        rc = self.radio_caracteristico_au

        normalizacion = math.exp(-self.radio_interior_au / rc)

        if self.radio_exterior_au is not None:
            normalizacion -= math.exp(-self.radio_exterior_au / rc)

        if normalizacion <= 0:
            return 0.0

        constante = self.masa_polvo_tierra / (2.0 * math.pi * rc * normalizacion)

        densidad = constante / radio * math.exp(-radio / rc)

        return max(
            0.0,
            densidad,
        )

    def obtener_radio_exterior_efectivo_au(
        self,
        fraccion_masa=0.99,
    ):
        if self.radio_caracteristico_au is None:
            return None

        if not 0 < fraccion_masa < 1:
            raise ValueError("La fracción de masa debe estar entre 0 y 1.")

        rc = self.radio_caracteristico_au

        interior_exp = math.exp(-self.radio_interior_au / rc)

        if self.radio_exterior_au is None:
            exterior_exp = 0.0

        else:
            exterior_exp = math.exp(-self.radio_exterior_au / rc)

        valor_objetivo = interior_exp - fraccion_masa * (interior_exp - exterior_exp)

        if valor_objetivo <= 0:
            return None

        radio = -rc * math.log(valor_objetivo)

        if self.radio_exterior_au is not None:
            radio = min(
                radio,
                self.radio_exterior_au,
            )

        return radio

    def obtener_masa_polvo_entre(
        self,
        radio_min_au,
        radio_max_au,
    ):
        fraccion = self.obtener_fraccion_polvo_entre(
            radio_min_au,
            radio_max_au,
        )

        return self.masa_polvo_tierra * fraccion

    def obtener_fraccion_polvo_interior_a(
        self,
        radio_au,
    ):
        if self.radio_caracteristico_au is None:
            return 0.0

        radio = float(radio_au)

        if radio <= self.radio_interior_au:
            return 0.0

        if self.radio_exterior_au is not None and radio >= self.radio_exterior_au:
            return 1.0

        rc = self.radio_caracteristico_au

        limite_exterior = self.radio_exterior_au

        masa_total = math.exp(-self.radio_interior_au / rc)

        if limite_exterior is not None:
            masa_total -= math.exp(-limite_exterior / rc)

        if masa_total <= 0:
            return 0.0

        masa_interior = math.exp(-self.radio_interior_au / rc) - math.exp(-radio / rc)

        fraccion = masa_interior / masa_total

        return max(
            0.0,
            min(
                1.0,
                fraccion,
            ),
        )

    def obtener_masa_polvo_interior_a(
        self,
        radio_au,
    ):
        return self.masa_polvo_tierra * self.obtener_fraccion_polvo_interior_a(radio_au)

    def obtener_masa_polvo_exterior_a(
        self,
        radio_au,
    ):
        masa_interior = self.obtener_masa_polvo_interior_a(radio_au)

        return max(
            0.0,
            self.masa_polvo_tierra - masa_interior,
        )

    def obtener_masa_polvo_interior_linea_hielo(
        self,
    ):
        if self.linea_hielo_au is None:
            return None

        return self.obtener_masa_polvo_interior_a(self.linea_hielo_au)

    def obtener_masa_polvo_exterior_linea_hielo(
        self,
    ):
        if self.linea_hielo_au is None:
            return None

        return self.obtener_masa_polvo_exterior_a(self.linea_hielo_au)

    def establecer_embriones(
        self,
        embriones,
    ):
        self.embriones = list(embriones)

        masa_embriones = sum(embrion.masa_tierra for embrion in self.embriones)

        self.masa_planetesimales_tierra = max(
            0.0,
            self.masa_polvo_tierra - masa_embriones,
        )

    def obtener_masa_embriones_tierra(
        self,
    ):
        return sum(embrion.masa_tierra for embrion in self.embriones)

    def obtener_cantidad_embriones(
        self,
    ):
        return len(self.embriones)

    def establecer_protoplanetas(
        self,
        protoplanetas,
    ):
        self.protoplanetas = list(protoplanetas)

    def obtener_cantidad_protoplanetas(
        self,
    ):
        return len(self.protoplanetas)

    def obtener_masa_protoplanetas_tierra(
        self,
    ):
        return sum(protoplaneta.masa_tierra for protoplaneta in self.protoplanetas)

    def a_dict(self):
        return {
            "estrella_nombre": (self.estrella_nombre),
            "sistema_nombre": (self.sistema_nombre),
            "masa_polvo_tierra": (self.masa_polvo_tierra),
            "radio_exterior_au": (self.radio_exterior_au),
            "truncado_por_companera": (self.truncado_por_companera),
            "radio_caracteristico_au": (self.radio_caracteristico_au),
            "radio_interior_au": (self.radio_interior_au),
            "gamma_perfil": (self.gamma_perfil),
            "linea_hielo_au": (self.linea_hielo_au),
            "modelo": self.modelo,
            "masa_estelar_msol": (self.masa_estelar_msol),
            "embriones": [embrion.a_dict() for embrion in self.embriones],
            "protoplanetas": [
                protoplaneta.a_dict() for protoplaneta in self.protoplanetas
            ],
            "masa_planetesimales_tierra": (self.masa_planetesimales_tierra),
            "masa_gas_referencia_tierra": (self.masa_gas_referencia_tierra),
            "relacion_gas_polvo": (self.relacion_gas_polvo),
            "vida_gas_myr": (self.vida_gas_myr),
            "masa_gas_capturada_tierra": (self.masa_gas_capturada_tierra),
            "masa_gas_no_capturada_tierra": (self.masa_gas_no_capturada_tierra),
            "masa_gas_runaway_capturada_tierra": (
                self.masa_gas_runaway_capturada_tierra
            ),
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
            radio_caracteristico_au=datos.get("radio_caracteristico_au"),
            radio_interior_au=datos.get(
                "radio_interior_au",
                0.05,
            ),
            gamma_perfil=datos.get(
                "gamma_perfil",
                1.0,
            ),
            linea_hielo_au=datos.get("linea_hielo_au"),
            modelo=datos["modelo"],
            masa_estelar_msol=datos.get("masa_estelar_msol"),
            embriones=[
                EmbrionPlanetario.desde_dict(datos_embrion)
                for datos_embrion in datos.get(
                    "embriones",
                    [],
                )
            ],
            protoplanetas=[
                Protoplaneta.desde_dict(datos_protoplaneta)
                for datos_protoplaneta in datos.get(
                    "protoplanetas",
                    [],
                )
            ],
            masa_planetesimales_tierra=datos.get("masa_planetesimales_tierra"),
            masa_gas_referencia_tierra=datos.get("masa_gas_referencia_tierra"),
            relacion_gas_polvo=datos.get("relacion_gas_polvo"),
            vida_gas_myr=datos.get("vida_gas_myr"),
            masa_gas_capturada_tierra=datos.get(
                "masa_gas_capturada_tierra",
                0.0,
            ),
            masa_gas_no_capturada_tierra=datos.get("masa_gas_no_capturada_tierra"),
            masa_gas_runaway_capturada_tierra=datos.get(
                "masa_gas_runaway_capturada_tierra",
                0.0,
            ),
        )
