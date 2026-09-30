import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class DescomposicionTests(unittest.TestCase):
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

    def forzar_adaptacion(self, universo):
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.descomposicion.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 1.0

    def test_restos_solos_no_crean_descomponedores(self):
        universo = self.universo()
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.avanzar(universo, 102_000_000)
        planeta = universo.planetas[0]
        self.assertGreater(planeta.muertes_unicelulares, 0)
        self.assertEqual(planeta.unidades_descomponedoras_activas, 0)
        self.assertFalse(planeta.alcanzo_capacidad_descomponedora)

    def test_capacidad_y_restos_recientes_activan_reciclaje(self):
        universo = self.universo()
        self.forzar_adaptacion(universo)
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertIn(2, planeta.linajes_descomponedores)
        self.assertEqual(planeta.unidades_descomponedoras_activas, 0)
        self.avanzar(universo, 102_000_000)
        self.assertGreater(planeta.unidades_descomponedoras_activas, 0)
        self.assertIn("con_reciclaje", planeta.estado_ecosistema)
        universo.actualizar_descomposicion({planeta: 1})
        self.assertEqual(planeta.estado_ecosistema.count("con_reciclaje"), 1)
        universo.actualizar_descomposicion({planeta: 0})
        self.assertEqual(planeta.unidades_descomponedoras_activas, 0)
        self.assertNotIn("con_reciclaje", planeta.estado_ecosistema)
        self.assertTrue(planeta.alcanzo_capacidad_descomponedora)
        planeta.vida_activa = False
        planeta.poblacion_unicelular = 0
        universo.actualizar_descomposicion({planeta: 5})
        self.assertEqual(planeta.unidades_descomponedoras_activas, 0)
        self.assertTrue(planeta.alcanzo_capacidad_descomponedora)

    def test_variante_hereda_sin_adquirir_de_nuevo(self):
        universo = self.universo()
        self.forzar_adaptacion(universo)
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        planeta.poblacion_unicelular = 1
        planeta.linajes_unicelulares_vivos = [2]
        planeta.rasgos_unicelulares_vivos = [
            planeta.historial_linajes_unicelulares[2]["rasgo"]
        ]
        planeta.linaje_observado_id = 2
        descomposicion = universo.modelo_herencia_unicelular.descomposicion
        descomposicion.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 0
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[3]["progenitor_id"], 2)
        self.assertIn(3, planeta.linajes_descomponedores)

    def test_sin_organicos_no_aparece_capacidad(self):
        universo = self.universo(candidato_quimica_prebiotica=False)
        self.forzar_adaptacion(universo)
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertEqual(universo.planetas[0].linajes_descomponedores, set())

    def test_pasos_guardado_y_partida_anterior(self):
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
            ruta = gestor.guardar(corto, "descomponedores")
            cargado = gestor.cargar("descomponedores")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("linajes_descomponedores",
                          "unidades_descomponedoras_activas",
                          "alcanzo_capacidad_descomponedora"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("descomponedores").planetas[0]
            self.assertEqual(antiguo.linajes_descomponedores, set())
            self.assertEqual(antiguo.unidades_descomponedoras_activas, 0)
            self.assertFalse(antiguo.alcanzo_capacidad_descomponedora)


if __name__ == "__main__":
    unittest.main()
