import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class ColoniasCelularesTests(unittest.TestCase):
    def universo(self, **cambios):
        universo = Universe(seed=73)
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )
        datos.update(cambios)
        universo.planetas = [Planet(**datos)]
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        muertes = universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion(muertes)
        universo.actualizar_ciclo_organico()
        universo.actualizar_colonias_celulares()

    def test_dos_linajes_distintos_no_forman_una_colonia(self):
        universo = self.universo(
            poblacion_unicelular=2,
            linajes_unicelulares_vivos=[1, 2],
            linajes_cohesivos={1, 2},
        )
        planeta = universo.planetas[0]
        universo.actualizar_colonias_celulares()
        self.assertEqual(planeta.colonias_multicelulares_activas, 0)
        planeta.linajes_unicelulares_vivos = [1, 1]
        universo.actualizar_colonias_celulares()
        self.assertEqual(planeta.colonias_multicelulares_activas, 1)
        planeta.estado_agua_preclima = "hielo"
        universo.actualizar_colonias_celulares()
        self.assertEqual(planeta.colonias_multicelulares_activas, 0)
        self.assertTrue(planeta.alcanzo_colonia_multicelular)

    def test_variante_adquiere_cohesion_y_copias_forman_colonia(self):
        universo = self.universo()
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.colonias.PROBABILIDAD_COHESION = 1.0
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertIn(2, planeta.linajes_cohesivos)
        self.assertEqual(planeta.colonias_multicelulares_activas, 0)

        herencia.PROBABILIDAD_VARIACION = 0.0
        planeta.linaje_observado_id = 2
        self.avanzar(universo, 102_000_000)
        self.assertGreater(planeta.colonias_multicelulares_activas, 0)
        self.assertTrue(planeta.alcanzo_colonia_multicelular)
        planeta.vida_activa = False
        self.avanzar(universo, 103_000_000)
        self.assertEqual(planeta.colonias_multicelulares_activas, 0)
        self.assertTrue(planeta.alcanzo_colonia_multicelular)

    def test_entorno_sin_organicos_no_asigna_cohesion(self):
        universo = self.universo(candidato_quimica_prebiotica=False)
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.colonias.PROBABILIDAD_COHESION = 1.0
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(universo.planetas[0].linajes_cohesivos, set())

    def test_variante_hija_hereda_cohesion_sin_adquirirla_de_nuevo(self):
        universo = self.universo()
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.colonias.PROBABILIDAD_COHESION = 1.0
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertIn(2, planeta.linajes_cohesivos)

        # Dejar solo la variante permite identificar sin ambigüedad la madre.
        planeta.poblacion_unicelular = 1
        planeta.linajes_unicelulares_vivos = [2]
        planeta.rasgos_unicelulares_vivos = [
            planeta.historial_linajes_unicelulares[2]["rasgo"]
        ]
        planeta.linaje_observado_id = 2
        herencia.colonias.PROBABILIDAD_COHESION = 0.0
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[3]["progenitor_id"], 2)
        self.assertIn(3, planeta.linajes_cohesivos)

    def test_pasos_y_guardados_conservan_estado(self):
        corto = self.universo(linajes_cohesivos={1})
        largo = self.universo(linajes_cohesivos={1})
        for universo in (corto, largo):
            universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0
            self.avanzar(universo, 100_000_000)
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertTrue(corto.planetas[0].alcanzo_colonia_multicelular)
        self.assertEqual(corto.random.getstate(), largo.random.getstate())

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(corto, "colonias")
            cargado = gestor.cargar("colonias")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("linajes_cohesivos",
                          "colonias_multicelulares_activas",
                          "alcanzo_colonia_multicelular"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("colonias").planetas[0]
            self.assertEqual(antiguo.linajes_cohesivos, set())
            self.assertEqual(antiguo.colonias_multicelulares_activas, 0)
            self.assertFalse(antiguo.alcanzo_colonia_multicelular)


if __name__ == "__main__":
    unittest.main()
