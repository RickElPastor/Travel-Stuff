import json
import tempfile
import unittest

from biology.unicellular_population_model import ModeloPoblacionUnicelular
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class PoblacionUnicelularTests(unittest.TestCase):
    def test_fundacion_crecimiento_y_perdida(self):
        planeta = Planet("Vida", 1, 1, vida_activa=True)
        modelo = ModeloPoblacionUnicelular()

        modelo.evaluar(planeta, 100_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 1)
        modelo.evaluar(planeta, 100_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 1)
        modelo.evaluar(planeta, 103_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 4)
        modelo.evaluar(planeta, 120_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 8)

        planeta.vida_activa = False
        modelo.evaluar(planeta, 121_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 0)
        self.assertIsNone(planeta.proximo_crecimiento_unicelular_anio)
        planeta.vida_activa = True
        modelo.evaluar(planeta, 122_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 1)

    def test_guardado_carga_y_continuacion(self):
        original = Universe(seed=7)
        original.planetas = [Planet("Vida", 1, 1, vida_activa=True)]
        original.time.anio = 100_000_000
        original.actualizar_poblacion_unicelular()

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(original, "vida_fase_2")
            cargado = gestor.cargar("vida_fase_2")
            for universo in (original, cargado):
                universo.time.anio = 104_000_000
                universo.actualizar_poblacion_unicelular()
            self.assertEqual(original.planetas[0].a_dict(),
                             cargado.planetas[0].a_dict())
            self.assertEqual(original.random.getstate(), cargado.random.getstate())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["poblacion_unicelular"]
            del datos["planetas"][0]["proximo_crecimiento_unicelular_anio"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("vida_fase_2")
            self.assertEqual(antiguo.planetas[0].poblacion_unicelular, 0)
            antiguo.actualizar_poblacion_unicelular()
            self.assertEqual(antiguo.planetas[0].poblacion_unicelular, 1)


if __name__ == "__main__":
    unittest.main()
