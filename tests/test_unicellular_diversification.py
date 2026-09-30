import tempfile
import unittest

from biology.species_model import ModeloEspeciesUnicelulares
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class DiversificacionTests(unittest.TestCase):
    def crear_planeta(self):
        return Planet(
            "Diverso", 1, 1, vida_activa=True, poblacion_unicelular=5,
            linajes_unicelulares_vivos=[2, 3, 3, 4, 5],
            rasgos_unicelulares_vivos=[0, 1, 1, 0, 2],
            linaje_observado_id=5, rasgo_linea_unicelular=2,
            historial_linajes_unicelulares={
                1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
                2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
                3: {"progenitor_id": 2, "rasgo": 1, "origen": "variacion"},
                4: {"progenitor_id": 3, "rasgo": 0, "origen": "variacion"},
                5: {"progenitor_id": 4, "rasgo": 2, "origen": "variacion"},
            },
        )

    def test_abundancia_parentesco_y_consultas_no_modifican_el_planeta(self):
        planeta = self.crear_planeta()
        antes = planeta.a_dict()
        modelo = ModeloEspeciesUnicelulares()
        self.assertEqual(modelo.abundancia_por_especie(planeta),
                         {1: 1, 3: 3, 5: 1})
        self.assertEqual(modelo.especies_vivas(planeta), {1, 3, 5})
        self.assertIsNone(modelo.especie_progenitora(planeta, 1))
        self.assertEqual(modelo.especie_progenitora(planeta, 3), 1)
        self.assertEqual(modelo.especie_progenitora(planeta, 5), 3)
        self.assertEqual(modelo.especies_hijas(planeta, 1), [3])
        self.assertEqual(modelo.especies_hijas(planeta, 3), [5])
        self.assertEqual(modelo.especies_hijas(planeta, 5), [])
        self.assertEqual(planeta.a_dict(), antes)

    def test_extincion_conserva_parentesco_y_guardado(self):
        planeta = self.crear_planeta()
        planeta.linajes_unicelulares_vivos = [3, 4, 5]
        planeta.rasgos_unicelulares_vivos = [1, 0, 2]
        planeta.poblacion_unicelular = 3
        modelo = ModeloEspeciesUnicelulares()
        self.assertEqual(modelo.especies_extintas(planeta), {1})
        self.assertEqual(modelo.especie_progenitora(planeta, 3), 1)

        universo = Universe(seed=73)
        universo.planetas = [planeta]
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "diversificacion")
            cargado = gestor.cargar("diversificacion")
        self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
        self.assertEqual(modelo.abundancia_por_especie(cargado.planetas[0]),
                         {3: 2, 5: 1})
        self.assertEqual(modelo.especies_hijas(cargado.planetas[0], 1), [3])

        planeta.linajes_unicelulares_vivos = []
        planeta.rasgos_unicelulares_vivos = []
        planeta.poblacion_unicelular = 0
        self.assertEqual(modelo.abundancia_por_especie(planeta), {})
        self.assertEqual(modelo.especies_extintas(planeta), {1, 3, 5})


if __name__ == "__main__":
    unittest.main()
