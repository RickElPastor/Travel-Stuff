import json
import tempfile
import unittest

from biology.niche_model import ModeloNichosEcologicos
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class DepredacionTests(unittest.TestCase):
    def universo(self, **cambios):
        universo = Universe(seed=73)
        datos = dict(
            nombre="Mundo", masa_tierra=1, semieje_mayor_au=1,
            sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=3,
            proximo_crecimiento_unicelular_anio=101_000_000,
            nacimientos_unicelulares=3,
            nacimientos_biologicos_procesados=3,
            rasgo_linea_unicelular=1,
            rasgos_unicelulares_vivos=[1, 1, 2],
            linajes_unicelulares_vivos=[1, 1, 2],
            linaje_observado_id=1,
            historial_linajes_unicelulares={
                1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
                2: {"progenitor_id": 1, "rasgo": 2, "origen": "variacion"},
            },
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 2, "distancia": 0},
            },
            linajes_depredadores={1},
        )
        datos.update(cambios)
        universo.planetas = [Planet(**datos)]
        universo.time.anio = 100_000_000
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0
        universo.modelo_herencia_unicelular.depredacion.PROBABILIDAD_ENCUENTRO = 1
        universo.actualizar_metabolismo_inicial()
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        muertes = universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion(muertes)
        universo.actualizar_ciclo_organico()
        universo.actualizar_colonias_celulares()

    def test_captura_cambia_presa_pero_no_total_de_muertes(self):
        con = self.universo()
        sin = self.universo(linajes_depredadores=set())
        self.assertEqual(ModeloNichosEcologicos().resumen(con.planetas[0])["presas"], 1)
        self.avanzar(con, 101_000_000)
        self.avanzar(sin, 101_000_000)
        depredado = con.planetas[0]
        control = sin.planetas[0]
        self.assertEqual(depredado.poblacion_unicelular, control.poblacion_unicelular)
        self.assertEqual(depredado.muertes_unicelulares, control.muertes_unicelulares)
        self.assertEqual(depredado.capturas_depredacion, 1)
        self.assertEqual((depredado.ultima_especie_predadora_id,
                          depredado.ultima_especie_presa_id), (1, 2))
        self.assertLess(depredado.linajes_unicelulares_vivos.count(2),
                        control.linajes_unicelulares_vivos.count(2))
        self.assertGreater(depredado.linajes_unicelulares_vivos.count(1),
                           control.linajes_unicelulares_vivos.count(1))
        self.assertEqual(depredado.restos_organicos_unidades, 0)
        self.assertEqual(control.restos_organicos_unidades, 1)
        self.assertEqual(depredado.muertes_contabilizadas_ciclo, 1)
        self.assertEqual(ModeloNichosEcologicos().resumen(depredado)["presas"], 1)

    def test_sin_otra_especie_no_hay_presa(self):
        universo = self.universo(
            rasgos_unicelulares_vivos=[1, 2, 2],
            linajes_unicelulares_vivos=[1, 2, 2],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 1, "distancia": 1},
            },
        )
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertEqual(planeta.capturas_depredacion, 0)
        self.assertEqual(planeta.restos_organicos_unidades, 1)
        self.assertEqual(ModeloNichosEcologicos().resumen(planeta)["presas"], 0)

    def test_nicho_de_presas_no_garantiza_encuentro(self):
        universo = self.universo()
        universo.modelo_herencia_unicelular.depredacion.PROBABILIDAD_ENCUENTRO = 0
        self.assertEqual(ModeloNichosEcologicos().resumen(universo.planetas[0])["presas"], 1)
        self.avanzar(universo, 101_000_000)
        planeta = universo.planetas[0]
        self.assertEqual(planeta.capturas_depredacion, 0)
        self.assertEqual(planeta.restos_organicos_unidades, 1)

    def test_capacidad_requiere_vida_y_mas_de_una_unidad(self):
        universo = self.universo()
        modelo = universo.modelo_herencia_unicelular.depredacion
        modelo.PROBABILIDAD_CAPACIDAD = 1
        planeta = universo.planetas[0]
        planeta.vida_activa = False
        self.assertFalse(modelo.adquiere_capacidad(planeta, 73, 4))
        planeta.vida_activa = True
        planeta.poblacion_unicelular = 1
        self.assertFalse(modelo.adquiere_capacidad(planeta, 73, 4))

    def test_variante_hija_hereda_capacidad(self):
        universo = Universe(seed=73)
        planeta = Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
        )
        universo.planetas = [planeta]
        herencia = universo.modelo_herencia_unicelular
        herencia.PROBABILIDAD_VARIACION = 1
        herencia.depredacion.PROBABILIDAD_CAPACIDAD = 1
        self.avanzar(universo, 100_000_000)
        self.avanzar(universo, 101_000_000)
        self.assertIn(2, planeta.linajes_depredadores)
        planeta.poblacion_unicelular = 1
        planeta.linajes_unicelulares_vivos = [2]
        planeta.rasgos_unicelulares_vivos = [
            planeta.historial_linajes_unicelulares[2]["rasgo"]
        ]
        planeta.linaje_observado_id = 2
        herencia.depredacion.PROBABILIDAD_CAPACIDAD = 0
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.historial_linajes_unicelulares[3]["progenitor_id"], 2)
        self.assertIn(3, planeta.linajes_depredadores)

    def test_pasos_guardado_y_partida_antigua(self):
        corto = self.universo()
        largo = self.universo()
        for anio in range(101_000_000, 111_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 110_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), largo.random.getstate())

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(corto, "depredacion")
            cargado = gestor.cargar("depredacion")
            self.assertEqual(cargado.planetas[0].a_dict(), corto.planetas[0].a_dict())
            for universo in (corto, cargado):
                universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0
                universo.modelo_herencia_unicelular.depredacion.PROBABILIDAD_ENCUENTRO = 1
                self.avanzar(universo, 111_000_000)
            self.assertEqual(cargado.planetas[0].a_dict(), corto.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            for campo in ("linajes_depredadores", "capturas_depredacion",
                          "ultima_especie_predadora_id", "ultima_especie_presa_id"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("depredacion").planetas[0]
            self.assertEqual(antiguo.linajes_depredadores, set())
            self.assertEqual(antiguo.capturas_depredacion, 0)
            self.assertIsNone(antiguo.ultima_especie_presa_id)


if __name__ == "__main__":
    unittest.main()
