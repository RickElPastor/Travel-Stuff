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
        hz_flujo_interior=None,
        hz_flujo_exterior=None,
        en_zona_habitable_radiativa=False,
        candidato_terrestre_hz=False,
        velocidad_escape_kms=None,
        shoreline_flujo_critico_tierra=None,
        retencion_atmosferica_aprox=False,
        masa_material_interior_hielo_tierra=None,
        masa_material_exterior_hielo_tierra=None,
        masa_material_sin_clasificar_tierra=None,
        masa_agua_inicial_tierra=None,
        fraccion_agua_inicial=None,
        reservorio_h2o_interior_tierra=None,
        reservorio_h2o_total_tierra=None,
        reservorio_carbono_tierra=None,
        reservorio_nitrogeno_tierra=None,
        actividad_geologica_relativa=None,
        fraccion_volatiles_desgasificada=None,
        geologicamente_activo=False,
        h2o_desgasificada_tierra=None,
        carbono_desgasificado_tierra=None,
        nitrogeno_desgasificado_tierra=None,
        tiene_atmosfera_secundaria=False,
        masa_atmosfera_secundaria_tierra=None,
        presion_atmosferica_bruta_bar=None,
        fraccion_molar_h2o_bruta=None,
        fraccion_molar_co2_bruta=None,
        fraccion_molar_n2_bruta=None,
        masa_agua_superficial_total_tierra=None,
        masa_h2o_vapor_tierra=None,
        masa_h2o_condensada_tierra=None,
        presion_h2o_preclima_bar=None,
        presion_co2_preclima_bar=None,
        presion_n2_preclima_bar=None,
        presion_atmosferica_preclima_bar=None,
        tiene_agua_condensada=False,
        estado_agua_preclima=None,
        pco2_max_greenhouse_bar=None,
        co2_dentro_max_greenhouse=False,
        candidato_habitable_fase1=False,
        estado_habitabilidad_fase1="no_evaluado",
        tiene_ingredientes_prebioticos=False,
        ruta_uv_prebiotica=False,
        ruta_geoquimica_prebiotica=False,
        candidato_quimica_prebiotica=False,
        estado_quimica_prebiotica="no_evaluado",
        tuvo_entorno_prebiotico=False,
        tuvo_ruta_uv_prebiotica=False,
        tuvo_ruta_geoquimica_prebiotica=False,
        regimen_mundo="sin_asignar",
        tipo_regla_extraordinaria=None,
        intensidad_extraordinaria=0.0,
        alcanzo_organicos_simples=False,
        ruta_organicos_simples=None,
        etapa_quimica_historica="sin_progreso",
        alcanzo_concentracion_prebiotica=False,
        mecanismo_concentracion_prebiotica=None,
        alcanzo_precursores_complejos=False,
        ruta_precursores_complejos=None,
        alcanzo_polimerizacion_prebiotica=False,
        mecanismo_polimerizacion_prebiotica=None,
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

        self.hz_flujo_interior = (
            None if hz_flujo_interior is None else float(hz_flujo_interior)
        )

        self.hz_flujo_exterior = (
            None if hz_flujo_exterior is None else float(hz_flujo_exterior)
        )

        self.en_zona_habitable_radiativa = bool(en_zona_habitable_radiativa)

        self.candidato_terrestre_hz = bool(candidato_terrestre_hz)

        self.velocidad_escape_kms = (
            None if velocidad_escape_kms is None else float(velocidad_escape_kms)
        )

        self.shoreline_flujo_critico_tierra = (
            None
            if shoreline_flujo_critico_tierra is None
            else float(shoreline_flujo_critico_tierra)
        )

        self.retencion_atmosferica_aprox = bool(retencion_atmosferica_aprox)

        self.masa_material_interior_hielo_tierra = (
            None
            if masa_material_interior_hielo_tierra is None
            else float(masa_material_interior_hielo_tierra)
        )

        self.masa_material_exterior_hielo_tierra = (
            None
            if masa_material_exterior_hielo_tierra is None
            else float(masa_material_exterior_hielo_tierra)
        )

        self.masa_material_sin_clasificar_tierra = (
            None
            if masa_material_sin_clasificar_tierra is None
            else float(masa_material_sin_clasificar_tierra)
        )

        self.masa_agua_inicial_tierra = (
            None
            if masa_agua_inicial_tierra is None
            else float(masa_agua_inicial_tierra)
        )

        self.fraccion_agua_inicial = (
            None if fraccion_agua_inicial is None else float(fraccion_agua_inicial)
        )

        self.reservorio_h2o_interior_tierra = (
            None
            if reservorio_h2o_interior_tierra is None
            else float(reservorio_h2o_interior_tierra)
        )

        self.reservorio_h2o_total_tierra = (
            None
            if reservorio_h2o_total_tierra is None
            else float(reservorio_h2o_total_tierra)
        )

        self.reservorio_carbono_tierra = (
            None
            if reservorio_carbono_tierra is None
            else float(reservorio_carbono_tierra)
        )

        self.reservorio_nitrogeno_tierra = (
            None
            if reservorio_nitrogeno_tierra is None
            else float(reservorio_nitrogeno_tierra)
        )

        self.actividad_geologica_relativa = (
            None
            if actividad_geologica_relativa is None
            else float(actividad_geologica_relativa)
        )

        self.fraccion_volatiles_desgasificada = (
            None
            if fraccion_volatiles_desgasificada is None
            else float(fraccion_volatiles_desgasificada)
        )

        self.geologicamente_activo = bool(geologicamente_activo)

        self.h2o_desgasificada_tierra = (
            None
            if h2o_desgasificada_tierra is None
            else float(h2o_desgasificada_tierra)
        )

        self.carbono_desgasificado_tierra = (
            None
            if carbono_desgasificado_tierra is None
            else float(carbono_desgasificado_tierra)
        )

        self.nitrogeno_desgasificado_tierra = (
            None
            if nitrogeno_desgasificado_tierra is None
            else float(nitrogeno_desgasificado_tierra)
        )

        self.tiene_atmosfera_secundaria = bool(tiene_atmosfera_secundaria)

        self.masa_atmosfera_secundaria_tierra = (
            None
            if masa_atmosfera_secundaria_tierra is None
            else float(masa_atmosfera_secundaria_tierra)
        )

        self.presion_atmosferica_bruta_bar = (
            None
            if presion_atmosferica_bruta_bar is None
            else float(presion_atmosferica_bruta_bar)
        )

        self.fraccion_molar_h2o_bruta = (
            None
            if fraccion_molar_h2o_bruta is None
            else float(fraccion_molar_h2o_bruta)
        )

        self.fraccion_molar_co2_bruta = (
            None
            if fraccion_molar_co2_bruta is None
            else float(fraccion_molar_co2_bruta)
        )

        self.fraccion_molar_n2_bruta = (
            None if fraccion_molar_n2_bruta is None else float(fraccion_molar_n2_bruta)
        )

        self.masa_agua_superficial_total_tierra = (
            None
            if masa_agua_superficial_total_tierra is None
            else float(masa_agua_superficial_total_tierra)
        )

        self.masa_h2o_vapor_tierra = (
            None if masa_h2o_vapor_tierra is None else float(masa_h2o_vapor_tierra)
        )

        self.masa_h2o_condensada_tierra = (
            None
            if masa_h2o_condensada_tierra is None
            else float(masa_h2o_condensada_tierra)
        )

        self.presion_h2o_preclima_bar = (
            None
            if presion_h2o_preclima_bar is None
            else float(presion_h2o_preclima_bar)
        )

        self.presion_co2_preclima_bar = (
            None
            if presion_co2_preclima_bar is None
            else float(presion_co2_preclima_bar)
        )

        self.presion_n2_preclima_bar = (
            None if presion_n2_preclima_bar is None else float(presion_n2_preclima_bar)
        )

        self.presion_atmosferica_preclima_bar = (
            None
            if presion_atmosferica_preclima_bar is None
            else float(presion_atmosferica_preclima_bar)
        )

        self.tiene_agua_condensada = bool(tiene_agua_condensada)

        self.estado_agua_preclima = estado_agua_preclima

        self.pco2_max_greenhouse_bar = (
            None if pco2_max_greenhouse_bar is None else float(pco2_max_greenhouse_bar)
        )

        self.co2_dentro_max_greenhouse = bool(co2_dentro_max_greenhouse)

        self.candidato_habitable_fase1 = bool(candidato_habitable_fase1)

        self.estado_habitabilidad_fase1 = estado_habitabilidad_fase1

        self.tiene_ingredientes_prebioticos = bool(tiene_ingredientes_prebioticos)

        self.ruta_uv_prebiotica = bool(ruta_uv_prebiotica)

        self.ruta_geoquimica_prebiotica = bool(ruta_geoquimica_prebiotica)

        self.candidato_quimica_prebiotica = bool(candidato_quimica_prebiotica)

        self.estado_quimica_prebiotica = estado_quimica_prebiotica

        self.tuvo_entorno_prebiotico = bool(tuvo_entorno_prebiotico)

        self.tuvo_ruta_uv_prebiotica = bool(tuvo_ruta_uv_prebiotica)

        self.tuvo_ruta_geoquimica_prebiotica = bool(tuvo_ruta_geoquimica_prebiotica)

        self.regimen_mundo = regimen_mundo

        self.tipo_regla_extraordinaria = tipo_regla_extraordinaria

        self.intensidad_extraordinaria = float(intensidad_extraordinaria)

        self.alcanzo_organicos_simples = bool(alcanzo_organicos_simples)

        self.ruta_organicos_simples = ruta_organicos_simples

        self.etapa_quimica_historica = etapa_quimica_historica

        self.alcanzo_concentracion_prebiotica = bool(alcanzo_concentracion_prebiotica)

        self.mecanismo_concentracion_prebiotica = mecanismo_concentracion_prebiotica

        self.alcanzo_precursores_complejos = bool(alcanzo_precursores_complejos)

        self.ruta_precursores_complejos = ruta_precursores_complejos

        self.alcanzo_polimerizacion_prebiotica = bool(alcanzo_polimerizacion_prebiotica)

        self.mecanismo_polimerizacion_prebiotica = mecanismo_polimerizacion_prebiotica

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
            "hz_flujo_interior": (self.hz_flujo_interior),
            "hz_flujo_exterior": (self.hz_flujo_exterior),
            "en_zona_habitable_radiativa": (self.en_zona_habitable_radiativa),
            "candidato_terrestre_hz": (self.candidato_terrestre_hz),
            "velocidad_escape_kms": (self.velocidad_escape_kms),
            "shoreline_flujo_critico_tierra": (self.shoreline_flujo_critico_tierra),
            "retencion_atmosferica_aprox": (self.retencion_atmosferica_aprox),
            "masa_material_interior_hielo_tierra": (
                self.masa_material_interior_hielo_tierra
            ),
            "masa_material_exterior_hielo_tierra": (
                self.masa_material_exterior_hielo_tierra
            ),
            "masa_material_sin_clasificar_tierra": (
                self.masa_material_sin_clasificar_tierra
            ),
            "masa_agua_inicial_tierra": (self.masa_agua_inicial_tierra),
            "fraccion_agua_inicial": (self.fraccion_agua_inicial),
            "reservorio_h2o_interior_tierra": (self.reservorio_h2o_interior_tierra),
            "reservorio_h2o_total_tierra": (self.reservorio_h2o_total_tierra),
            "reservorio_carbono_tierra": (self.reservorio_carbono_tierra),
            "reservorio_nitrogeno_tierra": (self.reservorio_nitrogeno_tierra),
            "actividad_geologica_relativa": (self.actividad_geologica_relativa),
            "fraccion_volatiles_desgasificada": (self.fraccion_volatiles_desgasificada),
            "geologicamente_activo": (self.geologicamente_activo),
            "h2o_desgasificada_tierra": (self.h2o_desgasificada_tierra),
            "carbono_desgasificado_tierra": (self.carbono_desgasificado_tierra),
            "nitrogeno_desgasificado_tierra": (self.nitrogeno_desgasificado_tierra),
            "tiene_atmosfera_secundaria": (self.tiene_atmosfera_secundaria),
            "masa_atmosfera_secundaria_tierra": (self.masa_atmosfera_secundaria_tierra),
            "presion_atmosferica_bruta_bar": (self.presion_atmosferica_bruta_bar),
            "fraccion_molar_h2o_bruta": (self.fraccion_molar_h2o_bruta),
            "fraccion_molar_co2_bruta": (self.fraccion_molar_co2_bruta),
            "fraccion_molar_n2_bruta": (self.fraccion_molar_n2_bruta),
            "masa_agua_superficial_total_tierra": (
                self.masa_agua_superficial_total_tierra
            ),
            "masa_h2o_vapor_tierra": (self.masa_h2o_vapor_tierra),
            "masa_h2o_condensada_tierra": (self.masa_h2o_condensada_tierra),
            "presion_h2o_preclima_bar": (self.presion_h2o_preclima_bar),
            "presion_co2_preclima_bar": (self.presion_co2_preclima_bar),
            "presion_n2_preclima_bar": (self.presion_n2_preclima_bar),
            "presion_atmosferica_preclima_bar": (self.presion_atmosferica_preclima_bar),
            "tiene_agua_condensada": (self.tiene_agua_condensada),
            "estado_agua_preclima": (self.estado_agua_preclima),
            "pco2_max_greenhouse_bar": (self.pco2_max_greenhouse_bar),
            "co2_dentro_max_greenhouse": (self.co2_dentro_max_greenhouse),
            "candidato_habitable_fase1": (self.candidato_habitable_fase1),
            "estado_habitabilidad_fase1": (self.estado_habitabilidad_fase1),
            "tiene_ingredientes_prebioticos": (self.tiene_ingredientes_prebioticos),
            "ruta_uv_prebiotica": (self.ruta_uv_prebiotica),
            "ruta_geoquimica_prebiotica": (self.ruta_geoquimica_prebiotica),
            "candidato_quimica_prebiotica": (self.candidato_quimica_prebiotica),
            "estado_quimica_prebiotica": (self.estado_quimica_prebiotica),
            "tuvo_entorno_prebiotico": (self.tuvo_entorno_prebiotico),
            "tuvo_ruta_uv_prebiotica": (self.tuvo_ruta_uv_prebiotica),
            "tuvo_ruta_geoquimica_prebiotica": (self.tuvo_ruta_geoquimica_prebiotica),
            "regimen_mundo": (self.regimen_mundo),
            "tipo_regla_extraordinaria": (self.tipo_regla_extraordinaria),
            "intensidad_extraordinaria": (self.intensidad_extraordinaria),
            "alcanzo_organicos_simples": (self.alcanzo_organicos_simples),
            "ruta_organicos_simples": (self.ruta_organicos_simples),
            "etapa_quimica_historica": (self.etapa_quimica_historica),
            "alcanzo_concentracion_prebiotica": (self.alcanzo_concentracion_prebiotica),
            "mecanismo_concentracion_prebiotica": (
                self.mecanismo_concentracion_prebiotica
            ),
            "alcanzo_precursores_complejos": (self.alcanzo_precursores_complejos),
            "ruta_precursores_complejos": (self.ruta_precursores_complejos),
            "alcanzo_polimerizacion_prebiotica": (
                self.alcanzo_polimerizacion_prebiotica
            ),
            "mecanismo_polimerizacion_prebiotica": (
                self.mecanismo_polimerizacion_prebiotica
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
            hz_flujo_interior=datos.get("hz_flujo_interior"),
            hz_flujo_exterior=datos.get("hz_flujo_exterior"),
            en_zona_habitable_radiativa=datos.get(
                "en_zona_habitable_radiativa",
                False,
            ),
            candidato_terrestre_hz=datos.get(
                "candidato_terrestre_hz",
                False,
            ),
            velocidad_escape_kms=datos.get("velocidad_escape_kms"),
            shoreline_flujo_critico_tierra=datos.get("shoreline_flujo_critico_tierra"),
            retencion_atmosferica_aprox=datos.get(
                "retencion_atmosferica_aprox",
                False,
            ),
            masa_material_interior_hielo_tierra=datos.get(
                "masa_material_interior_hielo_tierra"
            ),
            masa_material_exterior_hielo_tierra=datos.get(
                "masa_material_exterior_hielo_tierra"
            ),
            masa_material_sin_clasificar_tierra=datos.get(
                "masa_material_sin_clasificar_tierra"
            ),
            masa_agua_inicial_tierra=datos.get("masa_agua_inicial_tierra"),
            fraccion_agua_inicial=datos.get("fraccion_agua_inicial"),
            reservorio_h2o_interior_tierra=datos.get("reservorio_h2o_interior_tierra"),
            reservorio_h2o_total_tierra=datos.get("reservorio_h2o_total_tierra"),
            reservorio_carbono_tierra=datos.get("reservorio_carbono_tierra"),
            reservorio_nitrogeno_tierra=datos.get("reservorio_nitrogeno_tierra"),
            actividad_geologica_relativa=datos.get("actividad_geologica_relativa"),
            fraccion_volatiles_desgasificada=datos.get(
                "fraccion_volatiles_desgasificada"
            ),
            geologicamente_activo=datos.get(
                "geologicamente_activo",
                False,
            ),
            h2o_desgasificada_tierra=datos.get("h2o_desgasificada_tierra"),
            carbono_desgasificado_tierra=datos.get("carbono_desgasificado_tierra"),
            nitrogeno_desgasificado_tierra=datos.get("nitrogeno_desgasificado_tierra"),
            tiene_atmosfera_secundaria=datos.get(
                "tiene_atmosfera_secundaria",
                False,
            ),
            masa_atmosfera_secundaria_tierra=datos.get(
                "masa_atmosfera_secundaria_tierra"
            ),
            presion_atmosferica_bruta_bar=datos.get("presion_atmosferica_bruta_bar"),
            fraccion_molar_h2o_bruta=datos.get("fraccion_molar_h2o_bruta"),
            fraccion_molar_co2_bruta=datos.get("fraccion_molar_co2_bruta"),
            fraccion_molar_n2_bruta=datos.get("fraccion_molar_n2_bruta"),
            masa_agua_superficial_total_tierra=datos.get(
                "masa_agua_superficial_total_tierra"
            ),
            masa_h2o_vapor_tierra=datos.get("masa_h2o_vapor_tierra"),
            masa_h2o_condensada_tierra=datos.get("masa_h2o_condensada_tierra"),
            presion_h2o_preclima_bar=datos.get("presion_h2o_preclima_bar"),
            presion_co2_preclima_bar=datos.get("presion_co2_preclima_bar"),
            presion_n2_preclima_bar=datos.get("presion_n2_preclima_bar"),
            presion_atmosferica_preclima_bar=datos.get(
                "presion_atmosferica_preclima_bar"
            ),
            tiene_agua_condensada=datos.get(
                "tiene_agua_condensada",
                False,
            ),
            estado_agua_preclima=datos.get("estado_agua_preclima"),
            pco2_max_greenhouse_bar=datos.get("pco2_max_greenhouse_bar"),
            co2_dentro_max_greenhouse=datos.get(
                "co2_dentro_max_greenhouse",
                False,
            ),
            candidato_habitable_fase1=datos.get(
                "candidato_habitable_fase1",
                False,
            ),
            estado_habitabilidad_fase1=datos.get(
                "estado_habitabilidad_fase1",
                "no_evaluado",
            ),
            tiene_ingredientes_prebioticos=datos.get(
                "tiene_ingredientes_prebioticos",
                False,
            ),
            ruta_uv_prebiotica=datos.get(
                "ruta_uv_prebiotica",
                False,
            ),
            ruta_geoquimica_prebiotica=datos.get(
                "ruta_geoquimica_prebiotica",
                False,
            ),
            candidato_quimica_prebiotica=datos.get(
                "candidato_quimica_prebiotica",
                False,
            ),
            estado_quimica_prebiotica=datos.get(
                "estado_quimica_prebiotica",
                "no_evaluado",
            ),
            tuvo_entorno_prebiotico=datos.get(
                "tuvo_entorno_prebiotico",
                False,
            ),
            tuvo_ruta_uv_prebiotica=datos.get(
                "tuvo_ruta_uv_prebiotica",
                False,
            ),
            tuvo_ruta_geoquimica_prebiotica=datos.get(
                "tuvo_ruta_geoquimica_prebiotica",
                False,
            ),
            regimen_mundo=datos.get(
                "regimen_mundo",
                "sin_asignar",
            ),
            tipo_regla_extraordinaria=datos.get("tipo_regla_extraordinaria"),
            intensidad_extraordinaria=datos.get(
                "intensidad_extraordinaria",
                0.0,
            ),
            alcanzo_organicos_simples=datos.get(
                "alcanzo_organicos_simples",
                False,
            ),
            ruta_organicos_simples=datos.get("ruta_organicos_simples"),
            etapa_quimica_historica=datos.get(
                "etapa_quimica_historica",
                "sin_progreso",
            ),
            alcanzo_concentracion_prebiotica=datos.get(
                "alcanzo_concentracion_prebiotica",
                False,
            ),
            mecanismo_concentracion_prebiotica=datos.get(
                "mecanismo_concentracion_prebiotica"
            ),
            alcanzo_precursores_complejos=datos.get(
                "alcanzo_precursores_complejos",
                False,
            ),
            ruta_precursores_complejos=datos.get("ruta_precursores_complejos"),
            alcanzo_polimerizacion_prebiotica=datos.get(
                "alcanzo_polimerizacion_prebiotica",
                False,
            ),
            mecanismo_polimerizacion_prebiotica=datos.get(
                "mecanismo_polimerizacion_prebiotica"
            ),
        )
