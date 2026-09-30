class ModeloEspeciesUnicelulares:
    """Clasificación simbólica por parentesco; no mide aislamiento reproductivo."""

    VARIACIONES_PARA_NUEVA_ESPECIE = 2  # Regla de diseño, no umbral científico.

    def clasificar_linaje(self, planeta, linaje):
        clasificacion = planeta.clasificacion_especies_unicelulares
        if linaje in clasificacion:
            return  # La identidad ya registrada se conserva.
        registro = planeta.historial_linajes_unicelulares[linaje]
        padre = clasificacion.get(registro["progenitor_id"])
        especie = linaje
        distancia = 0
        if registro["origen"] == "variacion" and padre is not None:
            distancia = padre["distancia"] + 1
            if distancia < self.VARIACIONES_PARA_NUEVA_ESPECIE:
                especie = padre["especie_id"]
            else:
                distancia = 0  # Este linaje inicia otra especie.
        clasificacion[linaje] = {"especie_id": especie, "distancia": distancia}

    def completar_clasificacion(self, planeta):
        # Los identificadores son números de nacimiento: el padre precede al
        # hijo. Los negativos provisionales de guardados antiguos van primero.
        for linaje in sorted(planeta.historial_linajes_unicelulares):
            self.clasificar_linaje(planeta, linaje)

    def especies_vivas(self, planeta):
        if planeta.poblacion_unicelular == 0:
            return set()
        return {
            planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
            for linaje in planeta.linajes_unicelulares_vivos
        }

    def especies_registradas(self, planeta):
        return {
            registro["especie_id"]
            for registro in planeta.clasificacion_especies_unicelulares.values()
        }

    def especies_extintas(self, planeta):
        return self.especies_registradas(planeta) - self.especies_vivas(planeta)

    def abundancia_por_especie(self, planeta):
        """Unidades simbólicas vivas de cada especie de este planeta."""
        abundancia = {}
        if planeta.poblacion_unicelular == 0:
            return abundancia
        for linaje in planeta.linajes_unicelulares_vivos:
            especie = planeta.clasificacion_especies_unicelulares[linaje]["especie_id"]
            abundancia[especie] = abundancia.get(especie, 0) + 1
        return abundancia

    def especie_progenitora(self, planeta, especie_id):
        """Especie del linaje que originó la nueva especie, si se conoce."""
        registro = planeta.historial_linajes_unicelulares.get(especie_id)
        if registro is None or registro["origen"] != "variacion":
            return None
        padre = planeta.clasificacion_especies_unicelulares.get(
            registro["progenitor_id"]
        )
        return None if padre is None else padre["especie_id"]

    def especies_hijas(self, planeta, especie_id):
        """Especies registradas que nacieron directamente de esta."""
        return sorted(
            especie for especie in self.especies_registradas(planeta)
            if self.especie_progenitora(planeta, especie) == especie_id
        )
