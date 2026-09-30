import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class CicloOrganicoTests(unittest.TestCase):
    def universo(self, seed=73, **cambios):
        universo = Universe(seed=seed)
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", vida_activa=True,
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            linajes_descomponedores={1},
            presion_co2_preclima_bar=0.3,
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

    def test_muerte_pasa_por_restos_reciclaje_y_consumo(self):
        universo = self.universo()
        for anio in (100_000_000, 101_000_000, 102_000_000):
            self.avanzar(universo, anio)
        planeta = universo.planetas[0]
        self.assertEqual(planeta.muertes_unicelulares, 1)
        self.assertEqual(planeta.total_unidades_recicladas, 1)
        self.assertEqual(planeta.total_nutrientes_aprovechados, 1)
        self.assertEqual(planeta.restos_organicos_unidades, 0)
        self.assertEqual(planeta.nutrientes_reciclados_unidades, 0)
        self.assertEqual(
            planeta.muertes_unicelulares,
            planeta.restos_organicos_unidades
            + planeta.nutrientes_reciclados_unidades
            + planeta.total_nutrientes_aprovechados,
        )
        self.assertEqual(planeta.presion_co2_preclima_bar, 0.3)
        universo.actualizar_ciclo_organico()
        self.assertEqual(planeta.total_unidades_recicladas, 1)
        self.assertEqual(planeta.total_nutrientes_aprovechados, 1)

    def test_restos_y_nutrientes_esperan_si_falta_un_eslabon(self):
        universo = self.universo(linajes_descomponedores=set(),
                                 candidato_quimica_prebiotica=False)
        for anio in (100_000_000, 101_000_000, 102_000_000):
            self.avanzar(universo, anio)
        planeta = universo.planetas[0]
        self.assertEqual(planeta.restos_organicos_unidades, 1)
        self.assertEqual(planeta.total_unidades_recicladas, 0)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "restos")
            cargado = gestor.cargar("restos")
        self.assertEqual(cargado.planetas[0].restos_organicos_unidades, 1)

        planeta.linajes_descomponedores = set(planeta.linajes_unicelulares_vivos)
        universo.actualizar_descomposicion({planeta: 0})
        universo.actualizar_ciclo_organico()
        self.assertEqual(planeta.restos_organicos_unidades, 0)
        self.assertEqual(planeta.nutrientes_reciclados_unidades, 1)
        self.assertEqual(planeta.total_nutrientes_aprovechados, 0)

        planeta.candidato_quimica_prebiotica = True
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_ciclo_organico()
        self.assertEqual(planeta.nutrientes_reciclados_unidades, 0)
        self.assertEqual(planeta.total_nutrientes_aprovechados, 1)

    def test_pasos_guardado_y_guardado_anterior(self):
        corto = self.universo()
        largo = self.universo()
        for universo in (corto, largo):
            self.avanzar(universo, 100_000_000)
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), largo.random.getstate())

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(corto, "ciclo")
            cargado = gestor.cargar("ciclo")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())
            self.avanzar(corto, 111_000_000)
            self.avanzar(cargado, 111_000_000)
            self.assertEqual(cargado.planetas[0].a_dict(),
                             corto.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            for campo in ("restos_organicos_unidades",
                          "nutrientes_reciclados_unidades",
                          "muertes_contabilizadas_ciclo",
                          "total_unidades_recicladas",
                          "total_nutrientes_aprovechados"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("ciclo").planetas[0]
            self.assertEqual(antiguo.restos_organicos_unidades, 0)
            self.assertEqual(antiguo.muertes_contabilizadas_ciclo,
                             antiguo.muertes_unicelulares)

    def test_adaptacion_y_ciclo_coinciden_con_pasos_distintos(self):
        corto = self.universo(linajes_descomponedores=set())
        largo = self.universo(linajes_descomponedores=set())
        for universo in (corto, largo):
            herencia = universo.modelo_herencia_unicelular
            herencia.PROBABILIDAD_VARIACION = 1
            herencia.descomposicion.PROBABILIDAD_ADAPTACION_DESCOMPONEDORA = 1
            self.avanzar(universo, 100_000_000)
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertGreater(corto.planetas[0].total_nutrientes_aprovechados, 0)

    def test_linaje_descomponedor_transitorio_no_depende_del_paso(self):
        corto = self.universo(seed=1, linajes_descomponedores=set())
        largo = self.universo(seed=1, linajes_descomponedores=set())
        self.avanzar(corto, 100_000_000)
        self.avanzar(largo, 100_000_000)
        for anio in range(101_000_000, 121_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 120_000_000)
        self.assertGreater(corto.planetas[0].total_unidades_recicladas, 0)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())


if __name__ == "__main__":
    unittest.main()
