class Planet:
    def __init__(
        self,
        nombre,
        masa_tierra,
        semieje_mayor_au,
        excentricidad=0.0,
        sistema_nombre=None,
        estrella_anfitriona=None,
        tipo_orbita="circumestelar",
        composicion_inicial="indeterminada",
        masa_solida_tierra=None,
        masa_gas_tierra=0.0,
        candidato_captura_gas=False,
        origen_protoplaneta=None,
        embriones_fusionados=1,
    ):
        if masa_tierra <= 0:
            raise ValueError("La masa del planeta debe ser mayor que 0.")

        if semieje_mayor_au <= 0:
            raise ValueError("El semieje mayor debe ser mayor que 0.")

        if not 0 <= excentricidad < 1:
            raise ValueError("La excentricidad debe estar entre 0 y 1.")

        if tipo_orbita not in (
            "circumestelar",
            "circumbinaria",
        ):
            raise ValueError(
                "El tipo de órbita debe ser " "'circumestelar' o 'circumbinaria'."
            )

        if masa_gas_tierra < 0:
            raise ValueError("La masa de gas no puede ser negativa.")

        self.nombre = str(nombre)

        self.masa_tierra = float(masa_tierra)

        self.semieje_mayor_au = float(semieje_mayor_au)

        self.excentricidad = float(excentricidad)

        self.sistema_nombre = sistema_nombre

        self.estrella_anfitriona = estrella_anfitriona

        self.tipo_orbita = tipo_orbita

        self.composicion_inicial = str(composicion_inicial)

        self.masa_solida_tierra = (
            self.masa_tierra
            if masa_solida_tierra is None
            else float(masa_solida_tierra)
        )

        self.masa_gas_tierra = float(masa_gas_tierra)

        self.candidato_captura_gas = bool(candidato_captura_gas)

        self.origen_protoplaneta = origen_protoplaneta

        self.embriones_fusionados = int(embriones_fusionados)

    def obtener_periastro_au(self):
        return self.semieje_mayor_au * (1.0 - self.excentricidad)

    def obtener_apoastro_au(self):
        return self.semieje_mayor_au * (1.0 + self.excentricidad)

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "masa_tierra": (self.masa_tierra),
            "semieje_mayor_au": (self.semieje_mayor_au),
            "excentricidad": (self.excentricidad),
            "sistema_nombre": (self.sistema_nombre),
            "estrella_anfitriona": (self.estrella_anfitriona),
            "tipo_orbita": (self.tipo_orbita),
            "composicion_inicial": (self.composicion_inicial),
            "masa_solida_tierra": (self.masa_solida_tierra),
            "masa_gas_tierra": (self.masa_gas_tierra),
            "candidato_captura_gas": (self.candidato_captura_gas),
            "origen_protoplaneta": (self.origen_protoplaneta),
            "embriones_fusionados": (self.embriones_fusionados),
        }

    @classmethod
    def desde_dict(
        cls,
        datos,
    ):
        return cls(
            nombre=datos["nombre"],
            masa_tierra=(datos["masa_tierra"]),
            semieje_mayor_au=(datos["semieje_mayor_au"]),
            excentricidad=datos.get(
                "excentricidad",
                0.0,
            ),
            sistema_nombre=datos.get("sistema_nombre"),
            estrella_anfitriona=datos.get("estrella_anfitriona"),
            tipo_orbita=datos.get(
                "tipo_orbita",
                "circumestelar",
            ),
            composicion_inicial=datos.get(
                "composicion_inicial",
                "indeterminada",
            ),
            masa_solida_tierra=datos.get("masa_solida_tierra"),
            masa_gas_tierra=datos.get(
                "masa_gas_tierra",
                0.0,
            ),
            candidato_captura_gas=datos.get(
                "candidato_captura_gas",
                False,
            ),
            origen_protoplaneta=datos.get("origen_protoplaneta"),
            embriones_fusionados=datos.get(
                "embriones_fusionados",
                1,
            ),
        )
