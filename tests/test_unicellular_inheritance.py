import json
import tempfile
import unittest

from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class HerenciaUnicelularTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Vida", 1, 1, sistema_nombre="Sistema",
            vida_activa=True, patron_copia=2, estado_agua_preclima="hielo",
        )]
        return universo

    def avanzar_biologia(self, universo, anio):
        universo.time.anio = anio
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()

    def test_fundadora_herencia_variacion_y_extincion(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = universo.modelo_herencia_unicelular
        modelo.PROBABILIDAD_VARIACION = 1.0
        azar_inicial = universo.random.getstate()

        self.avanzar_biologia(universo, 100_000_000)
        self.assertEqual(planeta.rasgo_linea_unicelular, 1)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1])
        self.assertEqual(planeta.variaciones_unicelulares, 0)
        self.avanzar_biologia(universo, 101_000_000)
        self.assertNotEqual(planeta.rasgo_linea_unicelular, 1)
        self.assertEqual(planeta.variaciones_unicelulares, 1)
        self.assertEqual(planeta.variantes_biologicas_favorecidas, 1)
        self.assertEqual(planeta.variantes_biologicas_descartadas, 0)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1, 0])
        self.assertEqual(planeta.nacimientos_biologicos_procesados, 2)
        self.assertEqual(planeta.patron_copia, 2)
        self.assertEqual(universo.random.getstate(), azar_inicial)
        estado = planeta.a_dict()
        self.avanzar_biologia(universo, 101_000_000)
        self.assertEqual(planeta.a_dict(), estado)

        planeta.vida_activa = False
        self.avanzar_biologia(universo, 102_000_000)
        self.assertIsNone(planeta.rasgo_linea_unicelular)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [])
        self.assertEqual(planeta.variaciones_unicelulares, 1)
        planeta.vida_activa = True
        self.avanzar_biologia(universo, 103_000_000)
        self.assertEqual(planeta.rasgo_linea_unicelular, 1)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1])
        self.assertEqual(planeta.variaciones_unicelulares, 1)

    def test_sin_variacion_el_rasgo_se_hereda(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        self.avanzar_biologia(universo, 100_000_000)
        self.avanzar_biologia(universo, 110_000_000)
        planeta = universo.planetas[0]
        self.assertGreater(planeta.nacimientos_unicelulares, 1)
        self.assertEqual(planeta.rasgo_linea_unicelular, 1)
        self.assertEqual(planeta.variaciones_unicelulares, 0)
        self.assertEqual(planeta.variantes_biologicas_favorecidas, 0)
        self.assertEqual(planeta.variantes_biologicas_descartadas, 0)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1] * 8)

    def test_variante_descartada_de_la_linea_sigue_en_la_poblacion(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.estado_agua_preclima = "liquida"
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 1.0

        self.avanzar_biologia(universo, 100_000_000)
        self.avanzar_biologia(universo, 101_000_000)

        self.assertEqual(planeta.rasgo_linea_unicelular, 1)
        self.assertEqual(planeta.rasgos_unicelulares_vivos, [1, 0])
        self.assertEqual(planeta.variantes_biologicas_descartadas, 1)
        self.assertEqual(planeta.poblacion_unicelular,
                         len(planeta.rasgos_unicelulares_vivos))

    def test_misma_semilla_y_distinto_tamano_de_paso(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.avanzar_biologia(universo, 100_000_000)

        for anio in range(101_000_000, 121_000_000, 1_000_000):
            self.avanzar_biologia(corto, anio)
        self.avanzar_biologia(largo, 120_000_000)

        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), largo.random.getstate())
        self.assertGreater(corto.planetas[0].variaciones_unicelulares, 0)
        self.assertEqual(len(corto.planetas[0].rasgos_unicelulares_vivos), 8)
        self.assertEqual(
            corto.planetas[0].variaciones_unicelulares,
            corto.planetas[0].variantes_biologicas_favorecidas
            + corto.planetas[0].variantes_biologicas_descartadas,
        )

    def test_guardado_y_campos_ausentes_en_guardado_anterior(self):
        original = self.universo()
        self.avanzar_biologia(original, 100_000_000)
        self.avanzar_biologia(original, 103_000_000)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(original, "herencia")
            cargado = gestor.cargar("herencia")
            for universo in (original, cargado):
                self.avanzar_biologia(universo, 105_000_000)
            self.assertEqual(original.planetas[0].a_dict(),
                             cargado.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["rasgos_unicelulares_vivos"]
            ruta.write_text(json.dumps(datos))
            sin_grupos = gestor.cargar("herencia").planetas[0]
            self.assertEqual(
                sin_grupos.rasgos_unicelulares_vivos,
                [sin_grupos.rasgo_linea_unicelular] * sin_grupos.poblacion_unicelular,
            )

            for campo in ("rasgo_linea_unicelular",
                          "variaciones_unicelulares",
                          "nacimientos_biologicos_procesados",
                          "variantes_biologicas_favorecidas",
                          "variantes_biologicas_descartadas"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("herencia")
            planeta = antiguo.planetas[0]
            self.assertIsNone(planeta.rasgo_linea_unicelular)
            self.assertEqual(planeta.rasgos_unicelulares_vivos,
                             [1] * planeta.poblacion_unicelular)
            self.assertEqual(planeta.variaciones_unicelulares, 0)
            self.assertEqual(planeta.variantes_biologicas_favorecidas, 0)
            self.assertEqual(planeta.variantes_biologicas_descartadas, 0)
            self.assertEqual(planeta.nacimientos_biologicos_procesados,
                             planeta.nacimientos_unicelulares)
            self.avanzar_biologia(antiguo, 105_000_000)
            self.assertIn(planeta.rasgo_linea_unicelular, (0, 1, 2))
            self.assertEqual(planeta.nacimientos_biologicos_procesados,
                             planeta.nacimientos_unicelulares)

    def test_guardado_con_variaciones_previas_no_selecciona_hacia_atras(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.poblacion_unicelular = 3
        planeta.nacimientos_unicelulares = 7
        planeta.nacimientos_biologicos_procesados = 7
        planeta.rasgo_linea_unicelular = 0
        planeta.variaciones_unicelulares = 2

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "anterior")
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["variantes_biologicas_favorecidas"]
            del datos["planetas"][0]["variantes_biologicas_descartadas"]
            # Este formato anterior tampoco conocía unidades ni linajes vivos.
            del datos["planetas"][0]["rasgos_unicelulares_vivos"]
            del datos["planetas"][0]["linajes_unicelulares_vivos"]
            del datos["planetas"][0]["linaje_observado_id"]
            ruta.write_text(json.dumps(datos))
            cargado = gestor.cargar("anterior")
            cargado.actualizar_herencia_unicelular()
            p = cargado.planetas[0]
            self.assertEqual(p.rasgo_linea_unicelular, 0)
            self.assertEqual(p.variaciones_unicelulares, 2)
            self.assertEqual(p.variantes_biologicas_favorecidas, 0)
            self.assertEqual(p.variantes_biologicas_descartadas, 0)


if __name__ == "__main__":
    unittest.main()
