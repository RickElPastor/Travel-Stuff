import json
import tempfile
import unittest

from abiogenesis.inheritance_variation_model import ModeloHerenciaVariacion
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class HerenciaVariacionTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            nombre="Linea", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", alcanzo_protocelula=True,
            replicacion_prebiotica_activa=True,
            alcanzo_replicacion_prebiotica=True,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_copias_heredan_y_algunas_varian(self):
        p = self.planeta()
        modelo = ModeloHerenciaVariacion()
        modelo.evaluar(p, 374852300, 2_760_000_000)
        self.assertEqual(p.copias_heredables, 1)
        self.assertIn(p.patron_copia, (0, 1, 2))
        primera = p.a_dict()
        modelo.evaluar(p, 374852300, 2_760_000_000)
        self.assertEqual(p.a_dict(), primera)
        modelo.evaluar(p, 374852300, 2_780_000_000)
        self.assertEqual(p.copias_heredables, 21)
        self.assertGreater(p.variaciones_prebioticas, 0)
        self.assertLess(p.variaciones_prebioticas, p.copias_heredables)
        self.assertEqual(p.proxima_copia_anio, 2_781_000_000)

    def test_pasos_grandes_y_pequenos_coinciden(self):
        grande = self.planeta()
        pequeno = self.planeta()
        modelo = ModeloHerenciaVariacion()
        modelo.evaluar(grande, 7, 100_000_000)
        modelo.evaluar(grande, 7, 120_000_000)
        for anio in range(100_000_000, 120_000_001, 1_000_000):
            modelo.evaluar(pequeno, 7, anio)
        self.assertEqual(grande.a_dict(), pequeno.a_dict())

    def test_interrupcion_termina_linea_pero_conserva_historia(self):
        p = self.planeta()
        modelo = ModeloHerenciaVariacion()
        modelo.evaluar(p, 17, 10_000_000)
        modelo.evaluar(p, 17, 30_000_000)
        copias = p.copias_heredables
        variaciones = p.variaciones_prebioticas
        p.replicacion_prebiotica_activa = False
        modelo.evaluar(p, 17, 31_000_000)
        self.assertIsNone(p.patron_copia)
        self.assertIsNone(p.proxima_copia_anio)
        self.assertEqual(p.copias_heredables, copias)
        self.assertEqual(p.variaciones_prebioticas, variaciones)
        p.replicacion_prebiotica_activa = True
        modelo.evaluar(p, 17, 100_000_000)
        self.assertEqual(p.copias_heredables, copias + 1)
        self.assertEqual(p.proxima_copia_anio, 101_000_000)

    def test_no_modifica_azar_global_ni_campos_fisicos(self):
        u = Universe(seed=21)
        u.planetas = [self.planeta()]
        antes = u.planetas[0].a_dict()
        azar = u.random.getstate()
        u.time.anio = 50_000_000
        u.actualizar_herencia_variacion()
        self.assertEqual(azar, u.random.getstate())
        nuevos = {"patron_copia", "copias_heredables",
                  "variaciones_prebioticas", "proxima_copia_anio",
                  "copias_linea", "variaciones_linea", "comparaciones_linea"}
        self.assertEqual({k:v for k,v in antes.items() if k not in nuevos},
                         {k:v for k,v in u.planetas[0].a_dict().items() if k not in nuevos})

    def test_guardado_nuevo_antiguo_y_continuacion(self):
        u = Universe(seed=21)
        u.planetas = [self.planeta()]
        u.time.anio = 50_000_000
        u.actualizar_herencia_variacion()
        u.time.anio = 60_000_000
        u.actualizar_herencia_variacion()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(u, "nuevo")
            v = gestor.cargar("nuevo")
            self.assertEqual(u.planetas[0].a_dict(), v.planetas[0].a_dict())
            self.assertEqual(u.random.getstate(), v.random.getstate())
            u.time.anio = v.time.anio = 80_000_000
            u.actualizar_herencia_variacion()
            v.actualizar_herencia_variacion()
            self.assertEqual(u.planetas[0].a_dict(), v.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("patron_copia", "copias_heredables",
                          "variaciones_prebioticas", "proxima_copia_anio"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("nuevo")
            self.assertIsNone(antiguo.planetas[0].patron_copia)
            self.assertEqual(antiguo.planetas[0].copias_heredables, 0)
            self.assertEqual(antiguo.planetas[0].variaciones_prebioticas, 0)
            antiguo.actualizar_herencia_variacion()
            self.assertEqual(antiguo.planetas[0].copias_heredables, 1)


if __name__ == "__main__":
    unittest.main()
