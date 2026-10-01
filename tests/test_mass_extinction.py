import json
import tempfile
import unittest

from biology.mass_extinction_model import ModeloExtincionesMasivas
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class ExtincionesMasivasTests(unittest.TestCase):
    def universo(self, cantidad_especies=2):
        universo = Universe(seed=73)
        linajes = list(range(1, cantidad_especies + 1))
        planeta = Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            poblacion_unicelular=cantidad_especies,
            rasgo_linea_unicelular=1,
            rasgos_unicelulares_vivos=[1] * cantidad_especies,
            linajes_unicelulares_vivos=linajes,
            linaje_observado_id=1,
            clasificacion_especies_unicelulares={
                numero: {"especie_id": numero, "distancia": 0}
                for numero in linajes
            },
        )
        universo.planetas = [planeta]
        return universo

    def test_perdida_ambiental_de_dos_especies_registra_un_solo_evento(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        universo.time.anio = 1
        universo.actualizar(1)
        self.assertFalse(planeta.vida_activa)
        self.assertEqual(planeta.poblacion_unicelular, 0)
        self.assertEqual(planeta.muertes_unicelulares, 2)
        self.assertEqual(planeta.extinciones_masivas_locales, 1)
        self.assertEqual(planeta.anio_ultima_extincion_masiva, 1)
        self.assertEqual(planeta.especies_ultima_extincion_masiva, [1, 2])
        eventos = [e for e in universo.event_manager.obtener_eventos()
                   if "Extinción" in e.tipo]
        self.assertEqual([e.tipo for e in eventos], ["Extinción masiva local"])
        self.assertIn("2 especies (1, 2)", eventos[0].mensaje)
        self.assertIn("liquida → sin dato", eventos[0].mensaje)

        universo.time.anio = 2
        universo.actualizar(1)
        self.assertEqual(planeta.extinciones_masivas_locales, 1)
        self.assertEqual(len([e for e in universo.event_manager.obtener_eventos()
                              if "Extinción" in e.tipo]), 1)

    def test_una_especie_solo_produce_extincion_local(self):
        universo = self.universo(cantidad_especies=1)
        universo.time.anio = 1
        universo.actualizar(1)
        planeta = universo.planetas[0]
        self.assertEqual(planeta.extinciones_masivas_locales, 0)
        self.assertEqual(planeta.especies_ultima_extincion_masiva, [])
        eventos = [e for e in universo.event_manager.obtener_eventos()
                   if "Extinción" in e.tipo]
        self.assertEqual([e.tipo for e in eventos], ["Extinción local"])

    def test_una_nueva_caida_puede_registrarse_sin_recontar_la_anterior(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloExtincionesMasivas()
        planeta.vida_activa = False
        planeta.poblacion_unicelular = 0
        self.assertEqual(modelo.registrar(planeta, {1, 2}, 10), [1, 2])
        self.assertEqual(modelo.registrar(planeta, {1, 2}, 10), [])
        self.assertEqual(planeta.extinciones_masivas_locales, 1)

        planeta.clasificacion_especies_unicelulares.update({
            3: {"especie_id": 3, "distancia": 0},
            4: {"especie_id": 4, "distancia": 0},
        })
        self.assertEqual(modelo.registrar(planeta, {3, 4}, 20), [3, 4])
        self.assertEqual(planeta.extinciones_masivas_locales, 2)
        self.assertEqual(planeta.especies_ultima_extincion_masiva, [3, 4])

    def test_guardar_cargar_y_partida_anterior(self):
        universo = self.universo()
        universo.time.anio = 1
        universo.actualizar(1)
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "extinciones")
            cargado = gestor.cargar("extinciones")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            for version in (universo, cargado):
                version.time.anio = 2
                version.actualizar(1)
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            self.assertEqual(cargado.planetas[0].extinciones_masivas_locales, 1)

            datos = json.loads(ruta.read_text())
            for campo in ("extinciones_masivas_locales",
                          "anio_ultima_extincion_masiva",
                          "especies_ultima_extincion_masiva"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("extinciones").planetas[0]
            self.assertEqual(antiguo.extinciones_masivas_locales, 0)
            self.assertIsNone(antiguo.anio_ultima_extincion_masiva)
            self.assertEqual(antiguo.especies_ultima_extincion_masiva, [])


if __name__ == "__main__":
    unittest.main()
