import json
import tempfile
import unittest

from biology.species_model import ModeloEspeciesUnicelulares
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class EspeciesUnicelularesTests(unittest.TestCase):
    def planeta_con_parentesco(self):
        return Planet(
            "Vida", 1, 1, vida_activa=True, poblacion_unicelular=3,
            nacimientos_unicelulares=6, muertes_unicelulares=3,
            nacimientos_biologicos_procesados=6,
            linajes_unicelulares_vivos=[2, 3, 6],
            rasgos_unicelulares_vivos=[0, 1, 1],
            linaje_observado_id=2, rasgo_linea_unicelular=0,
            historial_linajes_unicelulares={
                # El orden del diccionario no determina el parentesco.
                6: {"progenitor_id": 5, "rasgo": 1, "origen": "variacion"},
                4: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
                3: {"progenitor_id": 2, "rasgo": 1, "origen": "variacion"},
                1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
                5: {"progenitor_id": 3, "rasgo": 0, "origen": "variacion"},
                2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
            },
        )

    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Vida", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="hielo",
        )]
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()

    def test_especie_depende_de_rama_no_de_rasgo_ni_total_de_variaciones(self):
        planeta = self.planeta_con_parentesco()
        self.assertEqual(planeta.clasificacion_especies_unicelulares, {
            1: {"especie_id": 1, "distancia": 0},
            2: {"especie_id": 1, "distancia": 1},
            3: {"especie_id": 3, "distancia": 0},
            4: {"especie_id": 1, "distancia": 1},
            5: {"especie_id": 3, "distancia": 1},
            6: {"especie_id": 6, "distancia": 0},
        })
        # 1, 3 y 6 comparten rasgo, pero son raíces de especies diferentes.
        modelo = ModeloEspeciesUnicelulares()
        self.assertEqual(modelo.especies_registradas(planeta), {1, 3, 6})
        self.assertEqual(modelo.especies_vivas(planeta), {1, 3, 6})

    def test_sin_parentesco_no_fusiona_linajes_por_compartir_rasgo(self):
        planeta = Planet(
            "Antiguo", 1, 1, poblacion_unicelular=2,
            linajes_unicelulares_vivos=[7, 9], rasgos_unicelulares_vivos=[0, 0],
        )
        self.assertEqual(ModeloEspeciesUnicelulares().especies_vivas(planeta), {7, 9})
        self.assertEqual(planeta.historial_linajes_unicelulares[7]["origen"],
                         "desconocido")

    def test_clasificar_y_consultar_no_alteran_biologia_ni_fisica(self):
        planeta = self.planeta_con_parentesco()
        planeta.clasificacion_especies_unicelulares = {}
        antes = planeta.a_dict()
        modelo = ModeloEspeciesUnicelulares()
        modelo.completar_clasificacion(planeta)
        despues = planeta.a_dict()
        for campo, valor in antes.items():
            if campo != "clasificacion_especies_unicelulares":
                self.assertEqual(despues[campo], valor, campo)
        modelo.completar_clasificacion(planeta)
        modelo.especies_vivas(planeta)
        modelo.especies_extintas(planeta)
        self.assertEqual(planeta.a_dict(), despues)

    def test_nacimientos_reales_registran_especies_y_no_duplican_sin_variacion(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        azar = universo.random.getstate()
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.clasificacion_especies_unicelulares[2]["especie_id"], 1)
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.clasificacion_especies_unicelulares[3]["especie_id"], 3)
        clasificacion = planeta.a_dict()["clasificacion_especies_unicelulares"]
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        self.avanzar(universo, 110_000_000)
        self.assertEqual(planeta.a_dict()["clasificacion_especies_unicelulares"],
                         clasificacion)
        self.assertEqual(universo.random.getstate(), azar)

    def test_extincion_depende_de_ultima_unidad_y_refundacion_tiene_otra_especie(self):
        planeta = self.planeta_con_parentesco()
        modelo = ModeloEspeciesUnicelulares()
        # La especie 1 sigue viva a través del linaje 2 aunque su fundador murió.
        self.assertIn(1, modelo.especies_vivas(planeta))
        planeta.linajes_unicelulares_vivos = [3, 6]
        planeta.rasgos_unicelulares_vivos = [1, 1]
        planeta.poblacion_unicelular = 2
        self.assertEqual(modelo.especies_extintas(planeta), {1})

        universo = self.universo()
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        planeta.vida_activa = False
        self.avanzar(universo, 102_000_000)
        self.assertEqual(modelo.especies_vivas(planeta), set())
        self.assertEqual(modelo.especies_extintas(planeta), {1})
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "extintas")
            universo = gestor.cargar("extintas")
        planeta = universo.planetas[0]
        planeta.vida_activa = True
        self.avanzar(universo, 103_000_000)
        self.assertEqual(modelo.especies_vivas(planeta), {3})
        self.assertEqual(modelo.especies_extintas(planeta), {1})

    def test_guardado_continuacion_y_pasos_temporales_conservan_clasificacion(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.avanzar(universo, 100_000_000)
        self.avanzar(corto, 105_000_000)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(corto, "especies")
            cargado = gestor.cargar("especies")
            cargado.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
            self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            for anio in range(106_000_000, 121_000_000, 1_000_000):
                self.avanzar(corto, anio)
                self.avanzar(cargado, anio)
            self.avanzar(largo, 120_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())

    def test_guardado_anterior_usa_solo_parentesco_disponible(self):
        universo = Universe(seed=73)
        universo.planetas = [self.planeta_con_parentesco()]
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "anterior")
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["clasificacion_especies_unicelulares"]
            ruta.write_text(json.dumps(datos))
            cargado = gestor.cargar("anterior")
            self.assertEqual(universo.planetas[0].a_dict(), cargado.planetas[0].a_dict())

            del datos["planetas"][0]["historial_linajes_unicelulares"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("anterior").planetas[0]
        modelo = ModeloEspeciesUnicelulares()
        self.assertEqual(modelo.especies_registradas(antiguo), {2, 3, 6})
        self.assertEqual(modelo.especies_extintas(antiguo), set())

    def test_asignaciones_persistidas_no_se_recalculan_ni_comparten_copias(self):
        planeta = self.planeta_con_parentesco()
        antes = planeta.a_dict()
        modelo = ModeloEspeciesUnicelulares()
        modelo.VARIACIONES_PARA_NUEVA_ESPECIE = 1
        modelo.completar_clasificacion(planeta)
        self.assertEqual(planeta.a_dict(), antes)
        copia = Planet.desde_dict(antes)
        antes["clasificacion_especies_unicelulares"]["2"]["especie_id"] = 999
        self.assertEqual(planeta.clasificacion_especies_unicelulares[2]["especie_id"], 1)
        self.assertEqual(copia.clasificacion_especies_unicelulares[2]["especie_id"], 1)


if __name__ == "__main__":
    unittest.main()
