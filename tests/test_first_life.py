import json
import tempfile
import unittest

from abiogenesis.first_life_model import ModeloPrimeraVida
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class PrimeraVidaTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            nombre="Primera", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", protocelula_viable=True,
            replicacion_prebiotica_activa=True,
            mecanismo_replicacion_prebiotica="copia_en_hielo",
            patron_copia=1, copias_linea=3,
            variaciones_linea=1, comparaciones_linea=1,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_requisitos_de_una_misma_linea(self):
        modelo = ModeloPrimeraVida()
        for cambio in (
            {"protocelula_viable": False},
            {"replicacion_prebiotica_activa": False},
            {"patron_copia": None},
            {"copias_linea": 2},
            {"variaciones_linea": 0},
            {"comparaciones_linea": 0},
            # Los totales históricos no sustituyen a la línea actual.
            {"copias_linea": 1, "copias_heredables": 41,
             "variaciones_prebioticas": 33, "variantes_descartadas": 33},
        ):
            with self.subTest(cambio=cambio):
                p = self.planeta(**cambio)
                modelo.evaluar(p, 100)
                self.assertFalse(p.vida_activa)
                self.assertFalse(p.alcanzo_primera_vida)
                self.assertIsNone(p.anio_primera_vida)

    def test_primera_vida_persiste_pero_puede_dejar_de_estar_activa(self):
        p = self.planeta(variantes_descartadas=1)
        modelo = ModeloPrimeraVida()
        modelo.evaluar(p, 2_780_000_000)
        self.assertTrue(p.vida_activa)
        self.assertTrue(p.alcanzo_primera_vida)
        self.assertEqual(p.anio_primera_vida, 2_780_000_000)
        p.replicacion_prebiotica_activa = False
        modelo.evaluar(p, 2_800_000_000)
        self.assertFalse(p.vida_activa)
        self.assertTrue(p.alcanzo_primera_vida)
        self.assertEqual(p.anio_primera_vida, 2_780_000_000)
        p.replicacion_prebiotica_activa = True
        modelo.evaluar(p, 2_820_000_000)
        self.assertTrue(p.vida_activa)
        self.assertEqual(p.anio_primera_vida, 2_780_000_000)

    def test_integracion_con_copias_y_reinicio_de_linea(self):
        u = Universe(seed=374852300)
        p = self.planeta(copias_linea=0, variaciones_linea=0,
                         comparaciones_linea=0, patron_copia=None)
        u.planetas = [p]
        u.time.anio = 2_760_000_000
        u.actualizar_herencia_variacion()
        u.actualizar_primera_vida()
        self.assertFalse(p.vida_activa)
        u.time.anio = 2_780_000_000
        u.actualizar_herencia_variacion()
        u.actualizar_primera_vida()
        self.assertGreater(p.variaciones_linea, 0)
        self.assertEqual(p.variaciones_linea, p.comparaciones_linea)
        self.assertTrue(p.alcanzo_primera_vida)
        p.replicacion_prebiotica_activa = False
        u.time.anio = 2_800_000_000
        u.actualizar_herencia_variacion()
        u.actualizar_primera_vida()
        self.assertEqual(p.copias_linea, 0)
        self.assertEqual(p.variaciones_linea, 0)
        self.assertFalse(p.vida_activa)
        self.assertTrue(p.alcanzo_primera_vida)
        p.replicacion_prebiotica_activa = True
        u.time.anio = 2_820_000_000
        u.actualizar_herencia_variacion()
        u.actualizar_primera_vida()
        self.assertEqual(p.copias_linea, 1)
        self.assertFalse(p.vida_activa)

    def test_guardado_y_reanudacion_igual(self):
        u = Universe(seed=374852300)
        p = self.planeta()
        u.planetas = [p]
        u.time.anio = 2_780_000_000
        u.actualizar_primera_vida()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(u, "vida")
            cargado = gestor.cargar("vida")
            self.assertEqual(u.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            for universo in (u, cargado):
                universo.time.anio = 2_781_000_000
                universo.actualizar_herencia_variacion()
                universo.actualizar_primera_vida()
            self.assertEqual(u.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            self.assertEqual(u.random.getstate(), cargado.random.getstate())
            datos = json.loads(ruta.read_text())
            for campo in ("copias_linea", "variaciones_linea",
                          "comparaciones_linea", "vida_activa",
                          "alcanzo_primera_vida", "anio_primera_vida"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("vida")
            self.assertFalse(antiguo.planetas[0].alcanzo_primera_vida)
            self.assertIsNone(antiguo.planetas[0].anio_primera_vida)
            self.assertEqual(antiguo.planetas[0].copias_linea, 0)


if __name__ == "__main__":
    unittest.main()
