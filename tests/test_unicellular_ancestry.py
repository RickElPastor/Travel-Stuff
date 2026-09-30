import json
import tempfile
import unittest

from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class ParentescoUnicelularTests(unittest.TestCase):
    def universo(self, agua="hielo"):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Vida", 1, 1, sistema_nombre="Sistema",
            vida_activa=True, estado_agua_preclima=agua,
        )]
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()

    def test_registra_fundadora_y_variante_aunque_no_sea_favorecida(self):
        universo = self.universo("liquida")
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        planeta = universo.planetas[0]
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares, {
            1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
            2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
        })
        self.assertEqual(planeta.linaje_observado_id, 1)
        self.assertEqual(planeta.variantes_biologicas_descartadas, 1)
        antes = planeta.a_dict()
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.a_dict(), antes)

    def test_progenitor_es_el_linaje_elegido_antes_de_variar(self):
        universo = self.universo()
        universo.planetas = [Planet(
            "Vida", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="hielo", poblacion_unicelular=2,
            nacimientos_unicelulares=2, nacimientos_biologicos_procesados=2,
            proximo_crecimiento_unicelular_anio=101_000_000,
            rasgos_unicelulares_vivos=[1, 0], linajes_unicelulares_vivos=[1, 2],
            linaje_observado_id=1, rasgo_linea_unicelular=1,
        )]
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        self.avanzar(universo, 101_000_000)
        historia = universo.planetas[0].historial_linajes_unicelulares
        self.assertEqual(historia[3]["progenitor_id"], 2)
        self.assertEqual(historia[4]["progenitor_id"], 2)
        self.assertEqual(historia[2]["origen"], "desconocido")

    def test_nacimientos_sin_variacion_no_duplican_linajes(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        azar = universo.random.getstate()
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 120_000_000)
        planeta = universo.planetas[0]
        self.assertGreater(planeta.nacimientos_unicelulares, 1)
        self.assertEqual(list(planeta.historial_linajes_unicelulares), [1])
        self.assertEqual(universo.random.getstate(), azar)

    def test_extincion_conserva_historia_y_nueva_fundadora_no_hereda_padre(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        planeta = universo.planetas[0]
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        historia = planeta.a_dict()["historial_linajes_unicelulares"]
        planeta.vida_activa = False
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [])
        self.assertEqual(planeta.a_dict()["historial_linajes_unicelulares"], historia)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "extincion")
            universo = gestor.cargar("extincion")
        planeta = universo.planetas[0]
        self.assertEqual(planeta.a_dict()["historial_linajes_unicelulares"], historia)
        planeta.vida_activa = True
        self.avanzar(universo, 103_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[3], {
            "progenitor_id": None, "rasgo": 1, "origen": "fundacion",
        })
        self.assertEqual(planeta.historial_linajes_unicelulares[2]["progenitor_id"], 1)

    def test_guardado_continuacion_y_pasos_conservan_todo_el_parentesco(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.avanzar(universo, 100_000_000)
        self.avanzar(corto, 105_000_000)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(corto, "parentesco")
            cargado = gestor.cargar("parentesco")
            self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            for anio in range(106_000_000, 121_000_000, 1_000_000):
                self.avanzar(corto, anio)
                self.avanzar(cargado, anio)
            self.avanzar(largo, 120_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        planeta = corto.planetas[0]
        self.assertEqual(len(planeta.historial_linajes_unicelulares),
                         1 + planeta.variaciones_unicelulares)
        for linaje, registro in planeta.historial_linajes_unicelulares.items():
            padre = registro["progenitor_id"]
            if padre is not None:
                self.assertIn(padre, planeta.historial_linajes_unicelulares)
                self.assertLess(padre, linaje)

    def test_guardado_anterior_no_inventa_parentesco_ni_linajes_extintos(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 110_000_000)
        vivos = set(universo.planetas[0].linajes_unicelulares_vivos)
        self.assertGreater(len(universo.planetas[0].historial_linajes_unicelulares),
                           len(vivos))
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "anterior")
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["historial_linajes_unicelulares"]
            ruta.write_text(json.dumps(datos))
            cargado = gestor.cargar("anterior")
        planeta = cargado.planetas[0]
        self.assertEqual(set(planeta.historial_linajes_unicelulares), vivos)
        for registro in planeta.historial_linajes_unicelulares.values():
            self.assertIsNone(registro["progenitor_id"])
            self.assertEqual(registro["origen"], "desconocido")
        cargado.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        padre = cargado.modelo_seleccion_unicelular.elegir_linaje_reproductor(planeta)
        nuevo = planeta.nacimientos_unicelulares + 1
        self.avanzar(cargado, 111_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[nuevo]["progenitor_id"],
                         padre)

    def test_copias_del_historial_no_comparten_diccionarios_mutables(self):
        universo = self.universo()
        self.avanzar(universo, 100_000_000)
        planeta = universo.planetas[0]
        datos = planeta.a_dict()
        copia = Planet.desde_dict(datos)
        datos["historial_linajes_unicelulares"]["1"]["rasgo"] = 2
        self.assertEqual(planeta.historial_linajes_unicelulares[1]["rasgo"], 1)
        self.assertEqual(copia.historial_linajes_unicelulares[1]["rasgo"], 1)


if __name__ == "__main__":
    unittest.main()
