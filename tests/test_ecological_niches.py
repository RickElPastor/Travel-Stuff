import tempfile
import unittest

from biology.niche_model import ModeloNichosEcologicos
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class NichosEcologicosTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        planeta = Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            poblacion_unicelular=4,
            linajes_unicelulares_vivos=[1, 1, 2, 3],
            clasificacion_especies_unicelulares={
                numero: {"especie_id": numero, "distancia": 0}
                for numero in (1, 2, 3)
            },
            linajes_fotosinteticos={1}, linajes_descomponedores={2},
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            irradiancia_media_w_m2=1000,
            presion_co2_preclima_bar=0.1,
            restos_organicos_unidades=2,
        )
        universo.planetas = [planeta]
        return universo

    def actualizar_recursos(self, universo):
        planeta = universo.planetas[0]
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion({planeta: 0})

    def test_recursos_se_asignan_a_especies_y_pueden_solaparse(self):
        universo = self.universo()
        self.actualizar_recursos(universo)
        planeta = universo.planetas[0]
        modelo = ModeloNichosEcologicos()
        antes = planeta.a_dict()
        self.assertEqual(modelo.ocupacion_por_especie(planeta), {
            1: {"unidades": 2, "organicos": 2, "luz": 2, "restos": 0,
                "presas": 0},
            2: {"unidades": 1, "organicos": 1, "luz": 0, "restos": 1,
                "presas": 0},
            3: {"unidades": 1, "organicos": 1, "luz": 0, "restos": 0,
                "presas": 0},
        })
        self.assertEqual(modelo.resumen(planeta), {
            "organicos": 3, "luz": 1, "restos": 1, "presas": 0,
            "sin_recurso": 0,
        })
        self.assertEqual(planeta.a_dict(), antes)
        self.assertEqual(universo.random.getstate(), Universe(seed=73).random.getstate())

    def test_recurso_desaparece_sin_borrar_especie_ni_inventar_extincion(self):
        universo = self.universo()
        self.actualizar_recursos(universo)
        planeta = universo.planetas[0]
        planeta.estado_agua_preclima = "hielo"
        planeta.candidato_quimica_prebiotica = False
        planeta.restos_organicos_unidades = 0
        self.actualizar_recursos(universo)
        modelo = ModeloNichosEcologicos()
        self.assertEqual(modelo.resumen(planeta), {
            "organicos": 0, "luz": 0, "restos": 0, "presas": 0,
            "sin_recurso": 3,
        })
        self.assertEqual(planeta.poblacion_unicelular, 4)
        self.assertEqual(len(universo.modelo_especies_unicelulares.especies_vivas(planeta)), 3)
        planeta.vida_activa = False
        self.assertEqual(modelo.ocupacion_por_especie(planeta), {})

    def test_guardar_cargar_reconstruye_la_misma_ocupacion(self):
        universo = self.universo()
        self.actualizar_recursos(universo)
        modelo = ModeloNichosEcologicos()
        esperado = modelo.ocupacion_por_especie(universo.planetas[0])
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "nichos")
            cargado = gestor.cargar("nichos")
        self.assertEqual(modelo.ocupacion_por_especie(cargado.planetas[0]), esperado)
        self.assertEqual(cargado.planetas[0].a_dict(), universo.planetas[0].a_dict())


if __name__ == "__main__":
    unittest.main()
