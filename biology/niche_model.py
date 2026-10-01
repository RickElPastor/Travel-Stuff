class ModeloNichosEcologicos:
    """Consulta qué recursos modelados ocupa cada especie viva del planeta."""

    RECURSOS = ("organicos", "luz", "restos", "presas")

    def ocupacion_por_especie(self, planeta):
        if not planeta.vida_activa or planeta.poblacion_unicelular == 0:
            return {}

        ocupacion = {}
        organicos = "organicos_ambientales" in planeta.fuentes_energia_potenciales
        productores = planeta.unidades_productoras_activas > 0
        descomponedores = planeta.unidades_descomponedoras_activas > 0
        especies_vivas = {
            planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
            for linaje in planeta.linajes_unicelulares_vivos
        }
        for linaje in planeta.linajes_unicelulares_vivos:
            especie = planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
            registro = ocupacion.setdefault(
                especie, {"unidades": 0, "organicos": 0, "luz": 0,
                          "restos": 0, "presas": 0}
            )
            registro["unidades"] += 1
            if organicos:
                registro["organicos"] += 1
            if productores and linaje in planeta.linajes_fotosinteticos:
                registro["luz"] += 1
            if descomponedores and linaje in planeta.linajes_descomponedores:
                registro["restos"] += 1
            if linaje in planeta.linajes_depredadores and len(especies_vivas) > 1:
                registro["presas"] += 1
        return ocupacion

    def resumen(self, planeta):
        ocupacion = self.ocupacion_por_especie(planeta)
        return {
            **{
                recurso: sum(datos[recurso] > 0 for datos in ocupacion.values())
                for recurso in self.RECURSOS
            },
            "sin_recurso": sum(
                all(datos[recurso] == 0 for recurso in self.RECURSOS)
                for datos in ocupacion.values()
            ),
        }
