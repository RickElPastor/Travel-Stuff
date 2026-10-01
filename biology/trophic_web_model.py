from biology.niche_model import ModeloNichosEcologicos


class ModeloRedTrofica:
    """Relaciones alimentarias actuales, derivadas de especies y nichos vivos."""

    RECURSOS = ("luz", "organicos", "restos")

    def enlaces(self, planeta):
        ocupacion = ModeloNichosEcologicos().ocupacion_por_especie(planeta)
        relaciones = []
        for recurso in self.RECURSOS:
            for especie in sorted(ocupacion):
                unidades = ocupacion[especie][recurso]
                if unidades > 0:
                    relaciones.append({
                        "tipo": "recurso",
                        "origen": recurso,
                        "destino": especie,
                        "unidades": unidades,
                    })

        for depredador in sorted(ocupacion):
            unidades = ocupacion[depredador]["presas"]
            if unidades == 0:
                continue
            for presa in sorted(ocupacion):
                if presa != depredador:
                    relaciones.append({
                        "tipo": "presa_posible",
                        "origen": presa,
                        "destino": depredador,
                        "unidades": unidades,
                    })
        return relaciones

    def resumen(self, planeta):
        relaciones = self.enlaces(planeta)
        return {
            "especies": len(ModeloNichosEcologicos().ocupacion_por_especie(planeta)),
            "recursos": sum(r["tipo"] == "recurso" for r in relaciones),
            "presas_posibles": sum(r["tipo"] == "presa_posible" for r in relaciones),
        }
