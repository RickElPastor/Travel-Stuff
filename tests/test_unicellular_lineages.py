import json
import tempfile
import unittest

from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class LinajesUnicelularesTests(unittest.TestCase):
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

    def test_poblacion_inicial_tiene_identidad_heredable(self):
        universo = self.universo()
        universo.planetas = [Planet(
            "Vida", 1, 1, vida_activa=True,
            poblacion_unicelular=2, rasgo_linea_unicelular=1,
            nacimientos_unicelulares=2, nacimientos_biologicos_procesados=2,
            proximo_crecimiento_unicelular_anio=101_000_000,
        )]
        planeta = universo.planetas[0]
        self.assertIsNotNone(planeta.linaje_observado_id)
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        self.avanzar(universo, 101_000_000)
        self.assertNotIn(None, planeta.linajes_unicelulares_vivos)

    def test_linea_observada_permanece_viva_con_muchas_variaciones(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
            self.avanzar(universo, 100_000_000)

        for anio in range(101_000_000, 121_000_000, 1_000_000):
            self.avanzar(corto, anio)
            planeta = corto.planetas[0]
            self.assertIn(planeta.linaje_observado_id,
                          planeta.linajes_unicelulares_vivos)
            indice = planeta.linajes_unicelulares_vivos.index(
                planeta.linaje_observado_id
            )
            self.assertEqual(planeta.rasgo_linea_unicelular,
                             planeta.rasgos_unicelulares_vivos[indice])
        self.avanzar(largo, 120_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())

    def test_guardado_sin_linajes_separa_rasgos_sin_inventar_antepasados(self):
        datos = Planet(
            "Vida", 1, 1, poblacion_unicelular=3,
            rasgo_linea_unicelular=0, rasgos_unicelulares_vivos=[1, 0, 0],
            nacimientos_unicelulares=7, nacimientos_biologicos_procesados=7,
        ).a_dict()
        del datos["linajes_unicelulares_vivos"]
        del datos["linaje_observado_id"]
        planeta = Planet.desde_dict(datos)
        ids = planeta.linajes_unicelulares_vivos
        self.assertNotEqual(ids[0], ids[1])
        self.assertEqual(ids[1], ids[2])
        self.assertEqual(planeta.linaje_observado_id, ids[1])
        self.assertTrue(all(linaje < 0 for linaje in ids))

    def test_guardado_antiguo_de_una_unidad_conserva_identidad_provisional(self):
        universo = self.universo()
        universo.planetas = [Planet.desde_dict({
            "nombre": "Vida", "masa_tierra": 1, "semieje_mayor_au": 1,
            "vida_activa": True, "poblacion_unicelular": 1,
            "nacimientos_unicelulares": 1,
        })]
        planeta = universo.planetas[0]
        identidad = planeta.linaje_observado_id
        self.assertLess(identidad, 0)
        universo.actualizar_herencia_unicelular()
        self.assertEqual(planeta.linaje_observado_id, identidad)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [identidad])
        self.assertEqual(planeta.variaciones_unicelulares, 0)

    def test_variante_crea_linaje_y_extincion_no_reutiliza_identidad(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        planeta = universo.planetas[0]

        self.avanzar(universo, 100_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [1])
        self.assertEqual(planeta.linaje_observado_id, 1)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1, 0])
        self.assertEqual(planeta.linajes_unicelulares_vivos, [1, 2])
        self.assertEqual(planeta.linaje_observado_id, 2)

        planeta.vida_activa = False
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [])
        self.assertIsNone(planeta.linaje_observado_id)
        planeta.vida_activa = True
        self.avanzar(universo, 103_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [3])
        self.assertEqual(planeta.linaje_observado_id, 3)

    def test_variante_no_elegida_conserva_identidad_propia(self):
        universo = self.universo("liquida")
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0
        planeta = universo.planetas[0]

        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [1, 2])
        self.assertEqual(planeta.linaje_observado_id, 1)
        self.assertEqual(planeta.variantes_biologicas_descartadas, 1)

        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        self.avanzar(universo, 120_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [1] * 8)
        self.assertEqual(planeta.linaje_observado_id, 1)

    def test_continuidad_guardado_y_pasos_distintos(self):
        corto = self.universo()
        largo = self.universo()
        self.avanzar(corto, 100_000_000)
        self.avanzar(largo, 100_000_000)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            self.avanzar(corto, 105_000_000)
            gestor.guardar(corto, "linajes")
            cargado = gestor.cargar("linajes")
            for anio in range(106_000_000, 121_000_000, 1_000_000):
                self.avanzar(corto, anio)
                self.avanzar(cargado, anio)
            self.avanzar(largo, 120_000_000)

        self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(
            len(corto.planetas[0].linajes_unicelulares_vivos),
            corto.planetas[0].poblacion_unicelular,
        )

    def test_guardado_anterior_asigna_identidades_provisionales(self):
        universo = self.universo()
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 103_000_000)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "anterior")
            datos = json.loads(ruta.read_text())
            planeta_guardado = datos["planetas"][0]
            del planeta_guardado["linajes_unicelulares_vivos"]
            del planeta_guardado["linaje_observado_id"]
            ruta.write_text(json.dumps(datos))
            cargado = gestor.cargar("anterior")

        planeta = cargado.planetas[0]
        self.assertEqual(planeta.linajes_unicelulares_vivos,
                         [-(rasgo + 1) for rasgo in planeta.rasgos_unicelulares_vivos])
        self.assertEqual(planeta.linaje_observado_id,
                         -(planeta.rasgo_linea_unicelular + 1))
        self.assertEqual(planeta.variaciones_unicelulares,
                         universo.planetas[0].variaciones_unicelulares)
        self.avanzar(cargado, 104_000_000)
        self.assertEqual(len(planeta.linajes_unicelulares_vivos),
                         planeta.poblacion_unicelular)


if __name__ == "__main__":
    unittest.main()
