import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class TransmisionSocialTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=6,
            linajes_unicelulares_vivos=[1, 1, 2, 2, 3, 3],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 1, "distancia": 1},
                3: {"especie_id": 2, "distancia": 0},
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1, 2, 3},
            linajes_fotosinteticos={1}, unidades_productoras_activas=2,
            linajes_descomponedores={3}, unidades_descomponedoras_activas=2,
        )]
        return universo

    def test_solo_se_comparte_entre_colonias_de_la_misma_especie(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        azar_antes = universo.random.getstate()
        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_linaje,
                         {1: ["luz"], 2: [], 3: ["restos"]})
        self.assertEqual(planeta.transmisiones_sociales, 0)

        universo.actualizar_transmision_social()
        self.assertEqual(planeta.recursos_recordados_por_linaje,
                         {1: ["luz"], 2: ["luz"], 3: ["restos"]})
        self.assertEqual(planeta.transmisiones_sociales, 1)
        for _ in range(5):
            universo.actualizar_transmision_social()
        self.assertEqual(planeta.transmisiones_sociales, 1)
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_requiere_dos_colonias_vivas_y_candidatura_actual(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        universo.actualizar_aprendizaje_inicial()
        planeta.linajes_unicelulares_vivos.remove(2)
        planeta.poblacion_unicelular -= 1
        universo.actualizar_transmision_social()
        self.assertEqual(planeta.transmisiones_sociales, 0)
        self.assertEqual(planeta.recursos_recordados_por_linaje[2], [])

        planeta.linajes_unicelulares_vivos.append(2)
        planeta.poblacion_unicelular += 1
        planeta.estado_agua_preclima = "hielo"
        universo.actualizar_transmision_social()
        self.assertEqual(planeta.transmisiones_sociales, 0)
        planeta.estado_agua_preclima = "liquida"
        universo.actualizar_transmision_social()
        self.assertEqual(planeta.transmisiones_sociales, 1)

    def test_recurso_de_linaje_sin_colonia_no_se_transmite(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.linajes_fotosinteticos = {3}
        planeta.linajes_descomponedores.clear()
        planeta.unidades_descomponedoras_activas = 0
        planeta.clasificacion_especies_unicelulares[3]["especie_id"] = 1
        planeta.linajes_unicelulares_vivos.remove(3)
        planeta.poblacion_unicelular -= 1
        universo.actualizar_aprendizaje_inicial()
        universo.actualizar_transmision_social()
        self.assertEqual(planeta.recursos_recordados_por_especie, {1: ["luz"]})
        self.assertEqual(planeta.recursos_recordados_por_linaje,
                         {1: [], 2: []})
        self.assertEqual(planeta.transmisiones_sociales, 0)

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        universo.actualizar_aprendizaje_inicial()
        universo.actualizar_transmision_social()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "social")
            cargado = gestor.cargar("social")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            for version in (universo, cargado):
                version.actualizar_aprendizaje_inicial()
                version.actualizar_transmision_social()
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["recursos_recordados_por_linaje"]
            del datos["planetas"][0]["transmisiones_sociales"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("social")
            self.assertEqual(anterior.planetas[0].recursos_recordados_por_linaje,
                             {})
            self.assertEqual(anterior.planetas[0].transmisiones_sociales, 0)
            anterior.actualizar_aprendizaje_inicial()
            anterior.actualizar_transmision_social()
            self.assertEqual(anterior.planetas[0].transmisiones_sociales, 1)


if __name__ == "__main__":
    unittest.main()
