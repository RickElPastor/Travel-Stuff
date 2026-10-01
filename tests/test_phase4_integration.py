import tempfile
import unittest

from biology.niche_model import ModeloNichosEcologicos
from biology.trophic_web_model import ModeloRedTrofica
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class IntegracionFase4Tests(unittest.TestCase):
    def crear_universo(self):
        universo = Universe(seed=1)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )]
        herencia = universo.modelo_herencia_unicelular
        herencia.colonias.PROBABILIDAD_COHESION = 1
        herencia.depredacion.PROBABILIDAD_CAPACIDAD = 1
        herencia.depredacion.PROBABILIDAD_ENCUENTRO = 1
        return universo

    def avanzar_biologia(self, universo, anio):
        universo.time.anio = anio
        muertes = universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion(muertes)
        universo.actualizar_ciclo_organico()
        universo.actualizar_colonias_celulares()

    def test_ecosistema_completo_pasos_guardado_y_extincion(self):
        corto, largo = self.crear_universo(), self.crear_universo()
        for universo in (corto, largo):
            self.avanzar_biologia(universo, 100_000_000)
        for anio in range(101_000_000, 114_000_000, 1_000_000):
            self.avanzar_biologia(corto, anio)
        self.avanzar_biologia(largo, 113_000_000)
        planeta = corto.planetas[0]
        self.assertEqual(planeta.a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), largo.random.getstate())

        self.assertEqual(planeta.poblacion_unicelular, 8)
        self.assertEqual(planeta.colonias_multicelulares_activas, 2)
        self.assertTrue(planeta.alcanzo_colonia_multicelular)
        self.assertEqual(planeta.capturas_depredacion, 6)
        self.assertEqual(planeta.ancestros_con_radiacion, {1})
        self.assertEqual(ModeloNichosEcologicos().resumen(planeta), {
            "organicos": 3, "luz": 0, "restos": 1,
            "presas": 3, "sin_recurso": 0,
        })
        self.assertEqual(ModeloRedTrofica().resumen(planeta), {
            "especies": 3, "recursos": 4, "presas_posibles": 6,
        })

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(corto, "fase4")
            cargado = gestor.cargar("fase4")
        self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
        self.assertEqual(ModeloRedTrofica().enlaces(cargado.planetas[0]),
                         ModeloRedTrofica().enlaces(planeta))

        for universo in (corto, largo, cargado):
            universo.time.anio = 114_000_000
            universo.actualizar(1_000_000)
        self.assertEqual(corto.planetas[0].a_dict(),
                         largo.planetas[0].a_dict())
        self.assertEqual(corto.planetas[0].a_dict(),
                         cargado.planetas[0].a_dict())
        self.assertFalse(planeta.vida_activa)
        self.assertEqual(planeta.poblacion_unicelular, 0)
        self.assertEqual(planeta.colonias_multicelulares_activas, 0)
        self.assertEqual(planeta.extinciones_masivas_locales, 1)
        self.assertEqual(len(planeta.especies_ultima_extincion_masiva), 3)
        self.assertEqual(planeta.ancestros_con_radiacion, {1})
        self.assertEqual(ModeloRedTrofica().enlaces(planeta), [])
        self.assertEqual([e.tipo for e in corto.event_manager.obtener_eventos()
                          if "Extinción" in e.tipo], ["Extinción masiva local"])


if __name__ == "__main__":
    unittest.main()
