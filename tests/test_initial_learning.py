import json
import tempfile
import unittest

from biology.initial_learning_model import ModeloAprendizajeInicial
from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class AprendizajeInicialTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=3,
            linajes_unicelulares_vivos=[1, 1, 2],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 2, "distancia": 0},
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1},
            linajes_fotosinteticos={1}, unidades_productoras_activas=2,
            linajes_depredadores={1},
        )]
        return universo

    def test_recuerda_rutas_extra_y_prioriza_una_conocida_disponible(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloAprendizajeInicial()
        candidatos = ModeloPrecursoresInteligencia()
        self.assertIsNone(modelo.preferencia_actual(
            planeta, 1, candidatos.candidatas(planeta)[1]["recursos"]
        ))
        azar_antes = universo.random.getstate()
        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_especie,
                         {1: ["luz", "presas"]})
        self.assertEqual(modelo.preferencia_actual(
            planeta, 1, candidatos.candidatas(planeta)[1]["recursos"]
        ), "luz")

        planeta.linajes_fotosinteticos.clear()
        planeta.unidades_productoras_activas = 0
        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(modelo.preferencia_actual(
            planeta, 1, candidatos.candidatas(planeta)[1]["recursos"]
        ), "presas")

        planeta.linajes_depredadores.clear()
        planeta.linajes_descomponedores = {1}
        planeta.unidades_descomponedoras_activas = 2
        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_especie,
                         {1: ["luz", "presas", "restos"]})
        self.assertEqual(modelo.preferencia_actual(
            planeta, 1, candidatos.candidatas(planeta)[1]["recursos"]
        ), "restos")
        planeta.linajes_fotosinteticos = {1}
        planeta.unidades_productoras_activas = 2
        self.assertEqual(modelo.preferencia_actual(
            planeta, 1, candidatos.candidatas(planeta)[1]["recursos"]
        ), "luz")
        for _ in range(5):
            universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_especie,
                         {1: ["luz", "presas", "restos"]})
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_sin_candidatura_no_aprende_pero_conserva_historia(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        universo.actualizar_aprendizaje_inicial()
        planeta.estado_agua_preclima = "hielo"
        planeta.linajes_fotosinteticos.clear()
        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_especie,
                         {1: ["luz", "presas"]})
        self.assertEqual(ModeloPrecursoresInteligencia().candidatas(planeta), {})

    def test_guardado_carga_pasos_y_partida_antigua(self):
        corto, largo = self.universo(), self.universo()
        for _ in range(10):
            corto.actualizar_aprendizaje_inicial()
        largo.actualizar_aprendizaje_inicial()
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(corto, "memoria")
            cargado = gestor.cargar("memoria")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())
            for version in (corto, cargado):
                version.actualizar_aprendizaje_inicial()
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["recursos_recordados_por_especie"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("memoria")
            self.assertEqual(antiguo.planetas[0].recursos_recordados_por_especie,
                             {})
            antiguo.actualizar_aprendizaje_inicial()
            self.assertEqual(antiguo.planetas[0].recursos_recordados_por_especie,
                             {1: ["luz", "presas"]})


if __name__ == "__main__":
    unittest.main()
