class ModeloSeleccionUnicelular:
    """Compara variantes nuevas y linajes vivos según el agua actual."""

    RASGO_FAVORECIDO_POR_AGUA = {
        "hielo": 0,
        "liquida": 2,
    }

    def rasgo_favorecido(self, planeta):
        return self.RASGO_FAVORECIDO_POR_AGUA.get(
            planeta.estado_agua_preclima
        )

    def esta_ajustada(self, planeta):
        """Indica si la línea activa coincide con el agua actual."""
        favorecido = self.rasgo_favorecido(planeta)
        return (
            planeta.poblacion_unicelular > 0
            and favorecido is not None
            and planeta.rasgo_linea_unicelular == favorecido
        )

    def linajes_ajustados(self, planeta):
        """Identidades vivas favorecidas, sin repetirlas y en orden de aparición."""
        favorecido = self.rasgo_favorecido(planeta)
        if planeta.poblacion_unicelular == 0 or favorecido is None:
            return []
        ajustados = []
        for linaje, rasgo in zip(
                planeta.linajes_unicelulares_vivos,
                planeta.rasgos_unicelulares_vivos):
            if rasgo == favorecido and linaje not in ajustados:
                ajustados.append(linaje)
        return ajustados

    def elegir_linaje_reproductor(self, planeta):
        """Prefiere un linaje ajustado; los empates conservan el observado."""
        vivos = planeta.linajes_unicelulares_vivos
        if planeta.poblacion_unicelular == 0 or not vivos:
            return None
        observado = planeta.linaje_observado_id
        ajustados = self.linajes_ajustados(planeta)
        if observado in ajustados:
            return observado
        if ajustados:
            # Desempate estable: primera unidad ajustada en la lista viva.
            return ajustados[0]
        if observado in vivos:
            return observado
        return vivos[-1]

    def elegir(self, planeta, anterior, variante):
        favorecido = self.rasgo_favorecido(planeta)
        if variante == favorecido and anterior != favorecido:
            planeta.variantes_biologicas_favorecidas += 1
            return variante

        planeta.variantes_biologicas_descartadas += 1
        return anterior
