import random


class ModeloDescomposicionMicrobiana:
    """Reconoce linajes capaces de aprovechar restos de unidades muertas."""

    PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 0.125  # Regla de diseño.

    def adquiere_capacidad(self, planeta, seed, nacimiento):
        if not (planeta.candidato_quimica_prebiotica
                and planeta.alcanzo_organicos_simples):
            return False
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:descomp:{nacimiento}"
        )
        return generador.random() < self.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA

    def evaluar(self, planeta, muertes_recientes):
        sufijo = "_con_reciclaje"
        if planeta.estado_ecosistema.endswith(sufijo):
            planeta.estado_ecosistema = planeta.estado_ecosistema[:-len(sufijo)]
        planeta.unidades_descomponedoras_activas = 0
        hay_restos = (muertes_recientes > 0
                      or planeta.restos_organicos_unidades > 0)
        if (not planeta.vida_activa or not hay_restos
                or planeta.poblacion_unicelular <= 0):
            return
        planeta.unidades_descomponedoras_activas = sum(
            linaje in planeta.linajes_descomponedores
            for linaje in planeta.linajes_unicelulares_vivos
        )
        if planeta.unidades_descomponedoras_activas:
            planeta.estado_ecosistema += sufijo
