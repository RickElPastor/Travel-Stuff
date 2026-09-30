import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class IntegracionBiosferaTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida", irradiancia_media_w_m2=1000,
            presion_co2_preclima_bar=0.2,
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )]
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.metabolismo.PROBABILIDAD_ADAPTACION_FOTOSINTETICA = 1.0
        herencia.descomposicion.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 1.0
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        muertes = universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion(muertes)
        universo.actualizar_ciclo_organico()
        universo.actualizar_atmosfera_biologica()

    def test_capacidades_atmosfera_reciclaje_y_continuidad(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.avanzar(universo, 100_000_000)
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        planeta = corto.planetas[0]
        self.assertEqual(planeta.a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(planeta.presion_co2_preclima_bar, 0.2)
        self.assertGreater(planeta.unidades_productoras_activas, 0)
        self.assertGreater(planeta.aporte_o2_biologico_bar, 0)
        self.assertGreater(planeta.total_unidades_recicladas, 0)
        self.assertEqual(planeta.total_unidades_recicladas,
                         planeta.total_nutrientes_aprovechados)

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(corto, "biosfera")
            cargado = gestor.cargar("biosfera")
        self.assertEqual(planeta.a_dict(), cargado.planetas[0].a_dict())
        herencia = cargado.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1.0
        herencia.metabolismo.PROBABILIDAD_ADAPTACION_FOTOSINTETICA = 1.0
        herencia.descomposicion.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 1.0
        self.avanzar(corto, 111_000_000)
        self.avanzar(cargado, 111_000_000)
        self.assertEqual(corto.planetas[0].a_dict(),
                         cargado.planetas[0].a_dict())


if __name__ == "__main__":
    unittest.main()
