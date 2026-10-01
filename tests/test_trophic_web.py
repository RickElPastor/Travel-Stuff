import tempfile
import unittest

from biology.trophic_web_model import ModeloRedTrofica
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class RedTroficaTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        planeta = Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            poblacion_unicelular=3,
            linajes_unicelulares_vivos=[1, 2, 3],
            clasificacion_especies_unicelulares={
                numero: {"especie_id": numero, "distancia": 0}
                for numero in (1, 2, 3)
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_fotosinteticos={1}, unidades_productoras_activas=1,
            linajes_descomponedores={2}, unidades_descomponedoras_activas=1,
            linajes_depredadores={3},
        )
        universo.planetas = [planeta]
        return universo

    def test_recursos_y_presas_forman_relaciones_dirigidas(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloRedTrofica()
        antes = planeta.a_dict()
        azar_antes = universo.random.getstate()
        self.assertEqual(modelo.enlaces(planeta), [
            {"tipo": "recurso", "origen": "luz", "destino": 1, "unidades": 1},
            {"tipo": "recurso", "origen": "organicos", "destino": 1,
             "unidades": 1},
            {"tipo": "recurso", "origen": "organicos", "destino": 2,
             "unidades": 1},
            {"tipo": "recurso", "origen": "organicos", "destino": 3,
             "unidades": 1},
            {"tipo": "recurso", "origen": "restos", "destino": 2,
             "unidades": 1},
            {"tipo": "presa_posible", "origen": 1, "destino": 3,
             "unidades": 1},
            {"tipo": "presa_posible", "origen": 2, "destino": 3,
             "unidades": 1},
        ])
        self.assertEqual(modelo.resumen(planeta), {
            "especies": 3, "recursos": 5, "presas_posibles": 2,
        })
        self.assertEqual(planeta.a_dict(), antes)
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_relacion_potencial_desaparece_al_perder_la_presa(self):
        planeta = self.universo().planetas[0]
        modelo = ModeloRedTrofica()
        planeta.linajes_unicelulares_vivos = [3]
        planeta.poblacion_unicelular = 1
        self.assertFalse(any(e["tipo"] == "presa_posible"
                             for e in modelo.enlaces(planeta)))
        planeta.vida_activa = False
        planeta.capturas_depredacion = 1
        planeta.ultima_especie_predadora_id = 3
        planeta.ultima_especie_presa_id = 1
        self.assertEqual(modelo.enlaces(planeta), [])

    def test_dos_depredadores_pueden_tener_enlaces_opuestos_sin_autoconsumo(self):
        planeta = self.universo().planetas[0]
        planeta.linajes_depredadores = {1, 2}
        enlaces = ModeloRedTrofica().enlaces(planeta)
        pares = {(e["origen"], e["destino"]) for e in enlaces
                 if e["tipo"] == "presa_posible"}
        self.assertIn((1, 2), pares)
        self.assertIn((2, 1), pares)
        self.assertTrue(all(presa != depredador for presa, depredador in pares))

    def test_guardar_y_cargar_reconstruye_la_misma_red(self):
        universo = self.universo()
        modelo = ModeloRedTrofica()
        esperados = modelo.enlaces(universo.planetas[0])
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "red")
            cargado = gestor.cargar("red")
        self.assertEqual(modelo.enlaces(cargado.planetas[0]), esperados)
        self.assertEqual(cargado.planetas[0].a_dict(), universo.planetas[0].a_dict())


if __name__ == "__main__":
    unittest.main()
