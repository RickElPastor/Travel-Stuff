import json
import tempfile
import unittest

from biology.metabolism_model import ModeloMetabolismoInicial
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class MetabolismoInicialTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            irradiancia_media_w_m2=1000,
            ruta_geoquimica_prebiotica=True,
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_fuentes_no_crean_vida_ni_fotosintesis(self):
        planeta = self.planeta()
        modelo = ModeloMetabolismoInicial()
        modelo.evaluar(planeta, 100)
        self.assertEqual(planeta.fuentes_energia_potenciales,
                         ["luz", "geoquimica", "organicos_ambientales"])
        self.assertIsNone(planeta.ruta_metabolica_inicial)
        self.assertEqual(planeta.estado_ecosistema, "sin_vida")
        self.assertFalse(planeta.alcanzo_metabolismo_inicial)

    def test_primera_poblacion_usa_organicos_y_conserva_historia(self):
        planeta = self.planeta(vida_activa=True, poblacion_unicelular=2)
        modelo = ModeloMetabolismoInicial()
        modelo.evaluar(planeta, 100)
        self.assertEqual(planeta.ruta_metabolica_inicial, "consumo_organicos")
        self.assertEqual(planeta.estado_ecosistema,
                         "microbiano_organicos_ambientales")
        self.assertEqual(planeta.anio_metabolismo_inicial, 100)
        modelo.evaluar(planeta, 200)
        self.assertEqual(planeta.anio_metabolismo_inicial, 100)

        planeta.candidato_quimica_prebiotica = False
        modelo.evaluar(planeta, 300)
        self.assertIsNone(planeta.ruta_metabolica_inicial)
        self.assertEqual(planeta.estado_ecosistema, "vida_sin_fuente_modelada")
        self.assertTrue(planeta.alcanzo_metabolismo_inicial)
        planeta.vida_activa = False
        planeta.poblacion_unicelular = 0
        modelo.evaluar(planeta, 400)
        self.assertEqual(planeta.estado_ecosistema, "sin_vida")
        self.assertEqual(planeta.anio_metabolismo_inicial, 100)

    def test_sin_organicos_no_inventa_otra_ruta(self):
        planeta = self.planeta(vida_activa=True, poblacion_unicelular=1,
                              alcanzo_organicos_simples=False)
        ModeloMetabolismoInicial().evaluar(planeta, 100)
        self.assertEqual(planeta.fuentes_energia_potenciales,
                         ["luz", "geoquimica"])
        self.assertIsNone(planeta.ruta_metabolica_inicial)
        self.assertEqual(planeta.estado_ecosistema, "vida_sin_fuente_modelada")

    def test_universo_guarda_carga_y_lee_guardado_anterior(self):
        universo = Universe(seed=7)
        universo.planetas = [self.planeta(vida_activa=True,
                                         poblacion_unicelular=1)]
        universo.time.anio = 1_000
        estado_azar = universo.random.getstate()
        universo.actualizar_metabolismo_inicial()
        self.assertEqual(universo.random.getstate(), estado_azar)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "metabolismo")
            cargado = gestor.cargar("metabolismo")
            self.assertEqual(universo.planetas[0].a_dict(),
                             cargado.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            for campo in ("fuentes_energia_potenciales",
                          "ruta_metabolica_inicial", "estado_ecosistema",
                          "alcanzo_metabolismo_inicial",
                          "anio_metabolismo_inicial"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("metabolismo")
            self.assertIsNone(antiguo.planetas[0].ruta_metabolica_inicial)
            self.assertFalse(antiguo.planetas[0].alcanzo_metabolismo_inicial)
            antiguo.actualizar_metabolismo_inicial()
            self.assertEqual(antiguo.planetas[0].ruta_metabolica_inicial,
                             "consumo_organicos")


if __name__ == "__main__":
    unittest.main()
