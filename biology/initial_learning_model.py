from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia


class ModeloAprendizajeInicial:
    """Conserva las rutas adicionales conocidas por especies candidatas."""

    def __init__(self):
        self.precursores = ModeloPrecursoresInteligencia()

    def evaluar(self, planeta):
        candidatas = self.precursores.candidatas(planeta)
        colonias = self.precursores.linajes_con_colonia(planeta)
        for especie, datos in candidatas.items():
            rutas = planeta.recursos_recordados_por_especie.setdefault(especie, [])
            for recurso in datos["recursos"]:
                if recurso != "organicos" and recurso not in rutas:
                    rutas.append(recurso)
        capacidades = {
            "luz": planeta.linajes_fotosinteticos,
            "restos": planeta.linajes_descomponedores,
            "presas": planeta.linajes_depredadores,
        }
        for linaje in colonias:
            especie = planeta.clasificacion_especies_unicelulares[linaje][
                "especie_id"
            ]
            if especie not in candidatas:
                continue
            conocidas = planeta.recursos_recordados_por_linaje.setdefault(linaje, [])
            for recurso in candidatas[especie]["recursos"]:
                if (recurso in capacidades
                        and linaje in capacidades[recurso]
                        and recurso not in conocidas):
                    conocidas.append(recurso)

    def preferencia_actual(self, planeta, especie, recursos_actuales):
        for recurso in planeta.recursos_recordados_por_especie.get(especie, []):
            if recurso in recursos_actuales:
                return recurso
        return None
