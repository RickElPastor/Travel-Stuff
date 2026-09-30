import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class ProductoresFotosinteticosTests(unittest.TestCase):
    def universo(self, **cambios):
        universo = Universe(seed=73)
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida", irradiancia_media_w_m2=1000,
            presion_co2_preclima_bar=0.1,
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )
        datos.update(cambios)
        universo.planetas = [Planet(**datos)]
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_atmosfera_biologica()

    def forzar_adaptacion(self, universo):
        modelo = universo.modelo_herencia_unicelular
        modelo.PROBABILIDAD_VARIACION = 1.0
        modelo.metabolismo.PROBABILIDAD_ADAPTACION_FOTOSINTETICA = 1.0

    def test_luz_agua_y_carbono_no_crean_productores_por_si_solos(self):
        universo = self.universo()
        self.avanzar(universo, 100_000_000)
        planeta = universo.planetas[0]
        self.assertIn("luz", planeta.fuentes_energia_potenciales)
        self.assertEqual(planeta.unidades_productoras_activas, 0)
        self.assertFalse(planeta.alcanzo_fotosintesis)
        self.assertEqual(planeta.ruta_metabolica_inicial, "consumo_organicos")

    def test_variante_adquiere_capacidad_y_sus_copias_la_heredan(self):
        universo = self.universo()
        self.forzar_adaptacion(universo)
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertIn(2, planeta.linajes_fotosinteticos)
        self.assertEqual(planeta.unidades_productoras_activas, 1)
        self.assertTrue(planeta.alcanzo_fotosintesis)
        self.assertEqual(planeta.ruta_metabolica_inicial,
                         "consumo_organicos_y_fotosintesis")
        self.assertEqual(planeta.estado_ecosistema,
                         "microbiano_productor_y_consumidor")

        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        planeta.linaje_observado_id = 2
        planeta.rasgo_linea_unicelular = planeta.rasgos_unicelulares_vivos[-1]
        self.avanzar(universo, 102_000_000)
        self.assertGreater(planeta.unidades_productoras_activas, 1)
        self.assertEqual(planeta.linajes_fotosinteticos, {2})

        planeta.irradiancia_media_w_m2 = None
        universo.actualizar_metabolismo_inicial()
        self.assertEqual(planeta.unidades_productoras_activas, 0)
        self.assertEqual(planeta.ruta_metabolica_inicial, "consumo_organicos")
        self.assertTrue(planeta.alcanzo_fotosintesis)
        planeta.irradiancia_media_w_m2 = 1000
        universo.actualizar_metabolismo_inicial()
        self.assertGreater(planeta.unidades_productoras_activas, 1)

    def test_sin_agua_liquida_o_carbono_no_aparece_adaptacion(self):
        for cambios in ({"estado_agua_preclima": "hielo"},
                        {"presion_co2_preclima_bar": None}):
            with self.subTest(cambios=cambios):
                universo = self.universo(**cambios)
                self.forzar_adaptacion(universo)
                self.avanzar(universo, 100_000_000)
                self.avanzar(universo, 101_000_000)
                planeta = universo.planetas[0]
                self.assertGreater(planeta.variaciones_unicelulares, 0)
                self.assertEqual(planeta.linajes_fotosinteticos, set())
                self.assertEqual(planeta.unidades_productoras_activas, 0)

    def test_variante_hereda_capacidad_de_su_progenitor(self):
        universo = self.universo()
        self.forzar_adaptacion(universo)
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertIn(2, planeta.linajes_fotosinteticos)

        # Aislamos la unidad adaptada para conocer con certeza el progenitor.
        planeta.poblacion_unicelular = 1
        planeta.linajes_unicelulares_vivos = [2]
        planeta.rasgos_unicelulares_vivos = [
            planeta.historial_linajes_unicelulares[2]["rasgo"]
        ]
        planeta.linaje_observado_id = 2
        metabolismo = universo.modelo_herencia_unicelular.metabolismo
        metabolismo.PROBABILIDAD_ADAPTACION_FOTOSINTETICA = 0
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[3]["progenitor_id"], 2)
        self.assertIn(3, planeta.linajes_fotosinteticos)
        self.assertTrue(planeta.alcanzo_fotosintesis)

    def test_pasos_y_guardado_conservan_capacidad_sin_retroactividad(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.forzar_adaptacion(universo)
            self.avanzar(universo, 100_000_000)
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), largo.random.getstate())

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(corto, "productores")
            cargado = gestor.cargar("productores")
            self.assertEqual(corto.planetas[0].a_dict(),
                             cargado.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("linajes_fotosinteticos",
                          "unidades_productoras_activas", "alcanzo_fotosintesis"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("productores").planetas[0]
            self.assertEqual(antiguo.linajes_fotosinteticos, set())
            self.assertEqual(antiguo.unidades_productoras_activas, 0)
            self.assertFalse(antiguo.alcanzo_fotosintesis)


if __name__ == "__main__":
    unittest.main()
