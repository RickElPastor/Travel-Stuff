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
        tiempo_nucleo_myr=None,
        gas_disponible_al_formarse=False,
        gcr_envoltura=0.0,
        tiempo_acrecion_gas_myr=None,
        candidato_runaway=False,
        masa_nucleo_acrecion_tierra=None,
        masa_gas_runaway_tierra=0.0,
        tiempo_runaway_myr=None,
        entro_runaway=False,
        radio_tierra=None,
        densidad_g_cm3=None,
        gravedad_superficial_ms2=None,
        flujo_estelar_tierra=None,
        irradiancia_media_w_m2=None,
        temperatura_equilibrio_cero_albedo_k=None,
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

        self.masa_nucleo_acrecion_tierra = (
            self.masa_solida_tierra
            if masa_nucleo_acrecion_tierra is None
            else float(masa_nucleo_acrecion_tierra)
        )

        self.masa_gas_tierra = float(masa_gas_tierra)

        self.candidato_captura_gas = bool(candidato_captura_gas)

        self.origen_protoplaneta = origen_protoplaneta

        self.embriones_fusionados = int(embriones_fusionados)

        self.tiempo_nucleo_myr = (
            None if tiempo_nucleo_myr is None else float(tiempo_nucleo_myr)
        )

        self.gas_disponible_al_formarse = bool(gas_disponible_al_formarse)

        self.gcr_envoltura = float(gcr_envoltura)

        self.tiempo_acrecion_gas_myr = (
            None if tiempo_acrecion_gas_myr is None else float(tiempo_acrecion_gas_myr)
        )

        self.candidato_runaway = bool(candidato_runaway)

        self.masa_gas_runaway_tierra = float(masa_gas_runaway_tierra)

        self.tiempo_runaway_myr = (
            None if tiempo_runaway_myr is None else float(tiempo_runaway_myr)
        )

        self.entro_runaway = bool(entro_runaway)

        self.radio_tierra = None if radio_tierra is None else float(radio_tierra)

        self.densidad_g_cm3 = None if densidad_g_cm3 is None else float(densidad_g_cm3)

        self.gravedad_superficial_ms2 = (
            None
            if gravedad_superficial_ms2 is None
            else float(gravedad_superficial_ms2)
        )

        self.flujo_estelar_tierra = (
            None if flujo_estelar_tierra is None else float(flujo_estelar_tierra)
        )

        self.irradiancia_media_w_m2 = (
            None if irradiancia_media_w_m2 is None else float(irradiancia_media_w_m2)
        )

        self.temperatura_equilibrio_cero_albedo_k = (
            None
            if temperatura_equilibrio_cero_albedo_k is None
            else float(temperatura_equilibrio_cero_albedo_k)
        )

    def obtener_periastro_au(self):
        return self.semieje_mayor_au * (1.0 - self.excentricidad)

    def obtener_apoastro_au(self):
        return self.semieje_mayor_au * (1.0 + self.excentricidad)

    def obtener_fraccion_gas(self):
        if self.masa_tierra <= 0:
            return 0.0

        return self.masa_gas_tierra / self.masa_tierra

    def obtener_estado_formacion(self):
        if self.entro_runaway:
            return "gigante_runaway"

        if self.masa_gas_tierra > 0:
            return "con_envoltura"

        if self.composicion_inicial == "rocosa":
            return "solido_rocoso"

        if self.composicion_inicial == "rica_en_hielos":
            return "solido_rico_en_hielos"

        if self.composicion_inicial == "mixta":
            return "solido_mixto"

        return "solido_indeterminado"

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
            "masa_nucleo_acrecion_tierra": (self.masa_nucleo_acrecion_tierra),
            "masa_gas_tierra": (self.masa_gas_tierra),
            "candidato_captura_gas": (self.candidato_captura_gas),
            "origen_protoplaneta": (self.origen_protoplaneta),
            "embriones_fusionados": (self.embriones_fusionados),
            "tiempo_nucleo_myr": (self.tiempo_nucleo_myr),
            "gas_disponible_al_formarse": (self.gas_disponible_al_formarse),
            "gcr_envoltura": (self.gcr_envoltura),
            "tiempo_acrecion_gas_myr": (self.tiempo_acrecion_gas_myr),
            "candidato_runaway": (self.candidato_runaway),
            "masa_gas_runaway_tierra": (self.masa_gas_runaway_tierra),
            "tiempo_runaway_myr": (self.tiempo_runaway_myr),
            "entro_runaway": (self.entro_runaway),
            "radio_tierra": (self.radio_tierra),
            "densidad_g_cm3": (self.densidad_g_cm3),
            "gravedad_superficial_ms2": (self.gravedad_superficial_ms2),
            "flujo_estelar_tierra": (self.flujo_estelar_tierra),
            "irradiancia_media_w_m2": (self.irradiancia_media_w_m2),
            "temperatura_equilibrio_cero_albedo_k": (
                self.temperatura_equilibrio_cero_albedo_k
            ),
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
            masa_nucleo_acrecion_tierra=datos.get("masa_nucleo_acrecion_tierra"),
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
            tiempo_nucleo_myr=datos.get("tiempo_nucleo_myr"),
            gas_disponible_al_formarse=datos.get(
                "gas_disponible_al_formarse",
                False,
            ),
            gcr_envoltura=datos.get(
                "gcr_envoltura",
                0.0,
            ),
            tiempo_acrecion_gas_myr=datos.get("tiempo_acrecion_gas_myr"),
            candidato_runaway=datos.get(
                "candidato_runaway",
                False,
            ),
            masa_gas_runaway_tierra=datos.get(
                "masa_gas_runaway_tierra",
                0.0,
            ),
            tiempo_runaway_myr=datos.get("tiempo_runaway_myr"),
            entro_runaway=datos.get(
                "entro_runaway",
                False,
            ),
            radio_tierra=datos.get("radio_tierra"),
            densidad_g_cm3=datos.get("densidad_g_cm3"),
            gravedad_superficial_ms2=datos.get("gravedad_superficial_ms2"),
            flujo_estelar_tierra=datos.get("flujo_estelar_tierra"),
            irradiancia_media_w_m2=datos.get("irradiancia_media_w_m2"),
            temperatura_equilibrio_cero_albedo_k=datos.get(
                "temperatura_equilibrio_cero_albedo_k"
            ),
        )
