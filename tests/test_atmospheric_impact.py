import json
import tempfile
import unittest

from biology.atmospheric_impact_model import ModeloAporteAtmosfericoBiologico
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class AporteAtmosfericoBiologicoTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            presion_co2_preclima_bar=2.0,
            presion_atmosferica_preclima_bar=3.0,
            vida_activa=True,
            unidades_productoras_activas=3,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_aporte_acotado_preserva_atmosfera_fisica(self):
        planeta = self.planeta()
        modelo = ModeloAporteAtmosfericoBiologico()
        modelo.evaluar(planeta)
        self.assertAlmostEqual(planeta.presion_co2_con_vida_bar, 1.94)
        self.assertAlmostEqual(planeta.aporte_o2_biologico_bar, 0.06)
        self.assertEqual(planeta.presion_co2_preclima_bar, 2.0)
        self.assertEqual(planeta.presion_atmosferica_preclima_bar, 3.0)

        planeta.unidades_productoras_activas = 100
        modelo.evaluar(planeta)
        self.assertAlmostEqual(planeta.presion_co2_con_vida_bar, 1.9)
        self.assertAlmostEqual(planeta.aporte_o2_biologico_bar, 0.1)
        modelo.evaluar(planeta)
        self.assertAlmostEqual(planeta.aporte_o2_biologico_bar, 0.1)

    def test_cese_de_productores_no_duplica_aporte(self):
        planeta = self.planeta()
        modelo = ModeloAporteAtmosfericoBiologico()
        modelo.evaluar(planeta)
        planeta.unidades_productoras_activas = 0
        modelo.evaluar(planeta)
        self.assertEqual(planeta.presion_co2_con_vida_bar, 2.0)
        self.assertEqual(planeta.aporte_o2_biologico_bar, 0.0)
        planeta.unidades_productoras_activas = 3
        planeta.vida_activa = False
        modelo.evaluar(planeta)
        self.assertEqual(planeta.aporte_o2_biologico_bar, 0.0)
        planeta.presion_co2_preclima_bar = None
        modelo.evaluar(planeta)
        self.assertIsNone(planeta.presion_co2_con_vida_bar)
        self.assertIsNone(planeta.aporte_o2_biologico_bar)

    def test_guardado_carga_y_campos_antiguos(self):
        universo = Universe(seed=73)
        universo.planetas = [self.planeta()]
        azar = universo.random.getstate()
        universo.actualizar_atmosfera_biologica()
        self.assertEqual(universo.random.getstate(), azar)

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "atmosfera")
            cargado = gestor.cargar("atmosfera")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["presion_co2_con_vida_bar"]
            del datos["planetas"][0]["aporte_o2_biologico_bar"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("atmosfera")
            self.assertIsNone(antiguo.planetas[0].presion_co2_con_vida_bar)
            self.assertIsNone(antiguo.planetas[0].aporte_o2_biologico_bar)
            antiguo.actualizar_atmosfera_biologica()
            self.assertAlmostEqual(antiguo.planetas[0].aporte_o2_biologico_bar,
                                   0.06)


if __name__ == "__main__":
    unittest.main()
