class ModeloSeleccionPrebiotica:
    """Compara una variante con su copia anterior en un entorno dado.

    Este modelo sigue una sola línea, no poblaciones ni competencia real.
    El patrón mejor adaptado se conserva; los empates conservan el anterior.
    """

    PATRON_FAVORECIDO = {
        "copia_en_hielo": 0,
        "copia_mixta": 1,
        "copia_en_poros_minerales": 2,
    }

    def elegir(self, planeta, anterior, variante):
        favorecido = self.PATRON_FAVORECIDO.get(
            planeta.mecanismo_replicacion_prebiotica
        )
        if favorecido is None or anterior == variante:
            return anterior

        planeta.comparaciones_linea += 1
        if variante == favorecido and anterior != favorecido:
            planeta.variantes_favorecidas += 1
            return variante

        # Si no hay ventaja demostrada por esta regla, continúa el anterior.
        planeta.variantes_descartadas += 1
        return anterior
