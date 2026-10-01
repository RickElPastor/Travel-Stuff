import json
import tempfile
import unittest

from biology.initial_tool_model import ModeloHerramientasIniciales
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class HerramientasInicialesTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=2,
            linajes_unicelulares_vivos=[1, 1],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1},
            linajes_fotosinteticos={1}, unidades_productoras_activas=2,
            restos_organicos_unidades=1,
            recursos_recordados_por_linaje={1: ["restos"]},
        )]
        return universo

    def test_ensayo_requiere_colonia_memoria_y_material_actual(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloHerramientasIniciales()
        estado_antes = planeta.a_dict()
        azar_antes = universo.random.getstate()
        self.assertEqual(modelo.usos_actuales(planeta), {1: [1]})
        self.assertEqual(planeta.a_dict(), estado_antes)
        universo.actualizar_herramientas_iniciales()
        self.assertEqual(planeta.especies_con_soporte_organico, {1})
        for _ in range(5):
            universo.actualizar_herramientas_iniciales()
        self.assertEqual(planeta.especies_con_soporte_organico, {1})
        self.assertEqual(universo.random.getstate(), azar_antes)

        planeta.restos_organicos_unidades = 0
        self.assertEqual(modelo.usos_actuales(planeta), {})
        self.assertEqual(planeta.especies_con_soporte_organico, {1})
        planeta.restos_organicos_unidades = 1
        planeta.recursos_recordados_por_linaje[1].clear()
        self.assertEqual(modelo.usos_actuales(planeta), {})
        planeta.recursos_recordados_por_linaje[1] = ["restos"]
        planeta.linajes_unicelulares_vivos.pop()
        planeta.poblacion_unicelular = 1
        self.assertEqual(modelo.usos_actuales(planeta), {})

    def test_no_basta_con_memoria_de_otra_especie_o_sin_vida(self):
        planeta = self.universo().planetas[0]
        modelo = ModeloHerramientasIniciales()
        planeta.recursos_recordados_por_linaje = {2: ["restos"]}
        self.assertEqual(modelo.usos_actuales(planeta), {})
        planeta.recursos_recordados_por_linaje = {1: ["restos"]}
        planeta.vida_activa = False
        self.assertEqual(modelo.usos_actuales(planeta), {})

    def test_recuerdo_compartido_permite_ensayo_sin_nueva_capacidad(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.linajes_unicelulares_vivos = [1, 1, 2, 2]
        planeta.poblacion_unicelular = 4
        planeta.clasificacion_especies_unicelulares[2] = {
            "especie_id": 1, "distancia": 1
        }
        planeta.linajes_cohesivos.add(2)
        planeta.linajes_fotosinteticos.clear()
        planeta.unidades_productoras_activas = 0
        planeta.linajes_descomponedores = {1}
        planeta.unidades_descomponedoras_activas = 2
        planeta.recursos_recordados_por_linaje = {}

        universo.actualizar_aprendizaje_inicial()
        self.assertEqual(planeta.recursos_recordados_por_linaje,
                         {1: ["restos"], 2: []})
        universo.actualizar_transmision_social()
        self.assertEqual(planeta.recursos_recordados_por_linaje[2], ["restos"])
        self.assertNotIn(2, planeta.linajes_descomponedores)
        self.assertEqual(ModeloHerramientasIniciales().usos_actuales(planeta),
                         {1: [1, 2]})

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        universo.actualizar_herramientas_iniciales()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "herramientas")
            cargado = gestor.cargar("herramientas")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            for version in (universo, cargado):
                version.planetas[0].restos_organicos_unidades = 0
                version.actualizar_herramientas_iniciales()
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["especies_con_soporte_organico"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("herramientas")
            self.assertEqual(anterior.planetas[0].especies_con_soporte_organico,
                             set())
            anterior.actualizar_herramientas_iniciales()
            self.assertEqual(anterior.planetas[0].especies_con_soporte_organico,
                             {1})


if __name__ == "__main__":
    unittest.main()
