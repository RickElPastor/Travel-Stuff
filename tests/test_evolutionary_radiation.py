import json
import tempfile
import unittest
from unittest.mock import patch

from biology.evolutionary_radiation_model import ModeloRadiacionesEvolutivas
from biology.inheritance_variation_model import ModeloHerenciaVariacionUnicelular
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class RadiacionesEvolutivasTests(unittest.TestCase):
    def planeta_con_hijas(self, segunda=5, misma_madre=True):
        padre_segunda = 1 if misma_madre else 9
        historial = {
            1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
            2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
            3: {"progenitor_id": 2, "rasgo": 1, "origen": "variacion"},
            segunda - 1: {
                "progenitor_id": padre_segunda, "rasgo": 0,
                "origen": "variacion",
            },
            segunda: {
                "progenitor_id": segunda - 1, "rasgo": 1,
                "origen": "variacion",
            },
        }
        if not misma_madre:
            historial[9] = {
                "progenitor_id": None, "rasgo": 1, "origen": "fundacion"
            }
        clasificacion = {
            1: {"especie_id": 1, "distancia": 0},
            2: {"especie_id": 1, "distancia": 1},
            3: {"especie_id": 3, "distancia": 0},
            segunda - 1: {"especie_id": padre_segunda, "distancia": 1},
            segunda: {"especie_id": segunda, "distancia": 0},
        }
        if not misma_madre:
            clasificacion[9] = {"especie_id": 9, "distancia": 0}
        return Planet(
            "Rama", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            poblacion_unicelular=3, rasgo_linea_unicelular=1,
            rasgos_unicelulares_vivos=[1, 1, 1],
            linajes_unicelulares_vivos=[1, 3, segunda],
            linaje_observado_id=1,
            historial_linajes_unicelulares=historial,
            clasificacion_especies_unicelulares=clasificacion,
        )

    def test_dos_hijas_vivas_y_cercanas_registran_una_radiacion(self):
        planeta = self.planeta_con_hijas()
        modelo = ModeloRadiacionesEvolutivas()
        self.assertEqual(modelo.registrar_intervalo(planeta, {1, 3}),
                         [(1, [3, 5])])
        self.assertEqual(planeta.ancestros_con_radiacion, {1})
        self.assertEqual(planeta.especies_ultima_radiacion, [3, 5])
        self.assertEqual(modelo.registrar_intervalo(planeta, {1, 3}), [])

    def test_sin_rama_nueva_hermana_o_ventana_no_hay_radiacion(self):
        modelo = ModeloRadiacionesEvolutivas()
        antigua = self.planeta_con_hijas()
        self.assertEqual(modelo.registrar_intervalo(antigua, {1, 3, 5}), [])
        lejana = self.planeta_con_hijas(segunda=20)
        self.assertEqual(modelo.registrar_intervalo(lejana, {1, 3}), [])
        otra_madre = self.planeta_con_hijas(segunda=11, misma_madre=False)
        self.assertEqual(modelo.registrar_intervalo(otra_madre, {1, 3, 9}), [])
        extinguida = self.planeta_con_hijas()
        extinguida.linajes_unicelulares_vivos = [1, 5]
        extinguida.rasgos_unicelulares_vivos = [1, 1]
        extinguida.poblacion_unicelular = 2
        self.assertEqual(modelo.registrar_intervalo(extinguida, {1, 3}), [])

    def test_nacimientos_reales_detectan_radiacion_en_pasos_distintos(self):
        def nuevo_planeta():
            return Planet(
                "Rama", 1, 1, sistema_nombre="Sistema", vida_activa=True,
                poblacion_unicelular=8, nacimientos_unicelulares=60,
                nacimientos_biologicos_procesados=1,
                rasgo_linea_unicelular=1,
                rasgos_unicelulares_vivos=[1],
                linajes_unicelulares_vivos=[1], linaje_observado_id=1,
                historial_linajes_unicelulares={
                    1: {"progenitor_id": None, "rasgo": 1,
                        "origen": "fundacion"},
                },
                clasificacion_especies_unicelulares={
                    1: {"especie_id": 1, "distancia": 0},
                },
            )

        largo, cortos = nuevo_planeta(), nuevo_planeta()
        modelo = ModeloHerenciaVariacionUnicelular()
        modelo.evaluar(largo, 31)
        cortos.nacimientos_unicelulares = 30
        modelo.evaluar(cortos, 31)
        cortos.nacimientos_unicelulares = 60
        modelo.evaluar(cortos, 31)
        self.assertEqual(largo.ancestros_con_radiacion, {1})
        self.assertEqual(largo.especies_ultima_radiacion, [13, 16])
        self.assertEqual(largo.a_dict(), cortos.a_dict())

    def test_evento_guardado_y_partida_antigua(self):
        universo = Universe(seed=73)
        planeta = Planet("Rama", 1, 1, sistema_nombre="Sistema")
        universo.planetas = [planeta]

        def registrar():
            planeta.ancestros_con_radiacion.add(1)
            planeta.especies_ultima_radiacion = [3, 5]

        with patch.object(universo, "actualizar_herencia_unicelular",
                          side_effect=registrar):
            universo.time.anio = 1
            universo.actualizar(1)
        eventos = [e for e in universo.event_manager.obtener_eventos()
                   if e.tipo == "Radiación evolutiva"]
        self.assertEqual(len(eventos), 1)
        self.assertIn("3 y 5", eventos[0].mensaje)
        universo.time.anio = 2
        universo.actualizar(1)
        self.assertEqual(sum(e.tipo == "Radiación evolutiva"
                             for e in universo.event_manager.obtener_eventos()), 1)

        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "radiaciones")
            cargado = gestor.cargar("radiaciones")
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
            for version in (universo, cargado):
                version.time.anio = 3
                version.actualizar(1)
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["ancestros_con_radiacion"]
            del datos["planetas"][0]["especies_ultima_radiacion"]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("radiaciones").planetas[0]
            self.assertEqual(antiguo.ancestros_con_radiacion, set())
            self.assertEqual(antiguo.especies_ultima_radiacion, [])


if __name__ == "__main__":
    unittest.main()
