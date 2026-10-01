class ModeloCicloOrganico:
    """Balance simbólico de restos, nutrientes y consumo microbiano."""

    def procesar_intervalo(self, planeta, muertes, presas_consumidas=0):
        """Procesa un intervalo biológico con sus linajes sobrevivientes."""
        self._registrar_muertes(planeta, muertes - presas_consumidas)
        planeta.muertes_contabilizadas_ciclo += presas_consumidas
        descomponedores = sum(
            linaje in planeta.linajes_descomponedores
            for linaje in planeta.linajes_unicelulares_vivos
        )
        puede_consumir = (
            planeta.candidato_quimica_prebiotica
            and planeta.alcanzo_organicos_simples
        )
        self._transferir(planeta, descomponedores, puede_consumir)

    def evaluar(self, planeta):
        nuevas_muertes = max(
            0, planeta.muertes_unicelulares - planeta.muertes_contabilizadas_ciclo
        )
        self._registrar_muertes(planeta, nuevas_muertes)
        puede_consumir = (
            planeta.ruta_metabolica_inicial is not None
            and "consumo_organicos" in planeta.ruta_metabolica_inicial
        )
        self._transferir(
            planeta, planeta.unidades_descomponedoras_activas, puede_consumir
        )

    def _registrar_muertes(self, planeta, cantidad):
        planeta.restos_organicos_unidades += cantidad
        planeta.muertes_contabilizadas_ciclo += cantidad

    def _transferir(self, planeta, descomponedores, puede_consumir):
        if planeta.vida_activa and descomponedores > 0:
            recicladas = planeta.restos_organicos_unidades
            planeta.restos_organicos_unidades = 0
            planeta.nutrientes_reciclados_unidades += recicladas
            planeta.total_unidades_recicladas += recicladas

        if planeta.vida_activa and puede_consumir:
            consumidas = planeta.nutrientes_reciclados_unidades
            planeta.nutrientes_reciclados_unidades = 0
            planeta.total_nutrientes_aprovechados += consumidas
