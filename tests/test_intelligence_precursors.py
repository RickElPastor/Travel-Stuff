import tempfile
import unittest

from biology.intelligence_precursor_model import ModeloPrecursoresInteligencia
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class PrecursoresInteligenciaTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=5,
            linajes_unicelulares_vivos=[1, 1, 2, 2, 3],
            clasificacion_especies_unicelulares={
                numero: {"especie_id": numero, "distancia": 0}
                for numero in (1, 2, 3)
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1, 2},
            linajes_fotosinteticos={1, 3}, unidades_productoras_activas=3,
            linajes_descomponedores={2}, unidades_descomponedoras_activas=2,
            linajes_depredadores={2},
        )]
        return universo

    def test_candidatas_exigen_colonia_y_dos_recursos_sin_mutar_estado(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloPrecursoresInteligencia()
        antes = planeta.a_dict()
        azar_antes = universo.random.getstate()
        self.assertEqual(modelo.candidatas(planeta), {
            1: {"colonias": 1, "recursos": ["organicos", "luz"]},
            2: {"colonias": 1,
                "recursos": ["organicos", "restos", "presas"]},
        })
        self.assertEqual(planeta.a_dict(), antes)
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_una_colonia_sin_segundo_recurso_no_es_candidata(self):
        planeta = self.universo().planetas[0]
        planeta.linajes_fotosinteticos = set()
        planeta.unidades_productoras_activas = 0
        self.assertNotIn(1, ModeloPrecursoresInteligencia().candidatas(planeta))
        planeta.linajes_cohesivos.discard(2)
        self.assertEqual(ModeloPrecursoresInteligencia().candidatas(planeta), {})
        planeta.estado_agua_preclima = "hielo"
        self.assertEqual(ModeloPrecursoresInteligencia().candidatas(planeta), {})

    def test_dos_linajes_cohesivos_de_una_especie_no_forman_colonia(self):
        planeta = self.universo().planetas[0]
        planeta.linajes_unicelulares_vivos = [1, 2]
        planeta.poblacion_unicelular = 2
        planeta.clasificacion_especies_unicelulares[2]["especie_id"] = 1
        self.assertEqual(ModeloPrecursoresInteligencia().candidatas(planeta), {})

    def test_guardar_y_cargar_reconstruyen_la_consulta(self):
        universo = self.universo()
        modelo = ModeloPrecursoresInteligencia()
        esperado = modelo.candidatas(universo.planetas[0])
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "precursores")
            cargado = gestor.cargar("precursores")
        self.assertEqual(modelo.candidatas(cargado.planetas[0]), esperado)
        self.assertEqual(cargado.planetas[0].a_dict(),
                         universo.planetas[0].a_dict())


if __name__ == "__main__":
    unittest.main()
