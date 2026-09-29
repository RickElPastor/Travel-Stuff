import json
import tempfile
import unittest

from abiogenesis.selection_model import ModeloSeleccionPrebiotica
from abiogenesis.inheritance_variation_model import ModeloHerenciaVariacion
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class SeleccionTests(unittest.TestCase):
    def planeta(self, ruta="copia_en_hielo", **cambios):
        datos = dict(
            nombre="Selección", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", replicacion_prebiotica_activa=True,
            mecanismo_replicacion_prebiotica=ruta,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_un_patron_favorecido_por_cada_entorno(self):
        modelo = ModeloSeleccionPrebiotica()
        for ruta, favorecido in modelo.PATRON_FAVORECIDO.items():
            with self.subTest(ruta=ruta):
                anterior = (favorecido + 1) % 3
                p = self.planeta(ruta)
                self.assertEqual(modelo.elegir(p, anterior, favorecido), favorecido)
                self.assertEqual(p.variantes_favorecidas, 1)
                self.assertEqual(modelo.elegir(p, favorecido, anterior), favorecido)
                self.assertEqual(p.variantes_descartadas, 1)

    def test_empate_conserva_anterior_y_no_modifica_fisica(self):
        p = self.planeta()
        antes = p.a_dict()
        self.assertEqual(ModeloSeleccionPrebiotica().elegir(p, 1, 2), 1)
        self.assertEqual(p.variantes_descartadas, 1)
        for clave in antes.keys() - {"variantes_descartadas", "comparaciones_linea"}:
            self.assertEqual(antes[clave], p.a_dict()[clave])

    def test_variacion_es_distinta_de_variante_favorecida(self):
        p = self.planeta()
        modelo = ModeloHerenciaVariacion()
        modelo.evaluar(p, 374852300, 0)
        modelo.evaluar(p, 374852300, 30_000_000)
        self.assertGreater(p.variaciones_prebioticas, 0)
        self.assertEqual(p.variaciones_prebioticas,
                         p.variantes_favorecidas + p.variantes_descartadas)
        self.assertLessEqual(p.variantes_favorecidas, 1)
        self.assertEqual(p.patron_copia, 0)

    def test_guardado_antiguo_nuevo_y_continuacion(self):
        u = Universe(seed=374852300)
        u.planetas = [self.planeta()]
        u.time.anio = 0
        u.actualizar_herencia_variacion()
        u.time.anio = 30_000_000
        u.actualizar_herencia_variacion()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(u, "seleccion")
            cargado = gestor.cargar("seleccion")
            self.assertEqual(u.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            for universo in (u, cargado):
                universo.time.anio = 60_000_000
                universo.actualizar_herencia_variacion()
            self.assertEqual(u.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            self.assertEqual(u.random.getstate(), cargado.random.getstate())
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["variantes_favorecidas"]
            del datos["planetas"][0]["variantes_descartadas"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("seleccion")
            self.assertEqual(antiguo.planetas[0].variantes_favorecidas, 0)
            self.assertEqual(antiguo.planetas[0].variantes_descartadas, 0)


if __name__ == "__main__":
    unittest.main()
