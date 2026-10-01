import json
import tempfile
import unittest

from biology.early_technology_model import ModeloTecnologiaTemprana
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class TecnologiaTempranaTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=4,
            linajes_unicelulares_vivos=[1, 1, 2, 2],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 1, "distancia": 1},
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1, 2},
            linajes_fotosinteticos={1, 2}, unidades_productoras_activas=4,
            linajes_descomponedores={1, 2},
            unidades_descomponedoras_activas=4,
            restos_organicos_unidades=1,
            recursos_recordados_por_linaje={
                1: ["luz", "restos"], 2: ["luz", "restos"]
            },
        )]
        return universo

    def preparar_soporte_y_codigos(self, universo):
        universo.actualizar_herramientas_iniciales()
        universo.actualizar_lenguaje_inicial()

    def test_tecnica_requiere_repetir_soporte_despues_de_escasez(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloTecnologiaTemprana()
        azar_antes = universo.random.getstate()
        self.preparar_soporte_y_codigos(universo)
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_con_tecnica_soporte, set())
        self.assertEqual(planeta.especies_soporte_con_escasez, set())
        for _ in range(5):
            universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_con_tecnica_soporte, set())

        planeta.restos_organicos_unidades = 0
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_soporte_con_escasez, {1})
        self.assertEqual(planeta.especies_con_tecnica_soporte, set())
        planeta.restos_organicos_unidades = 1
        antes = planeta.a_dict()
        self.assertEqual(modelo.tecnicas_actuales(planeta), {})
        self.assertEqual(planeta.a_dict(), antes)
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_con_tecnica_soporte, {1})
        self.assertEqual(modelo.tecnicas_actuales(planeta), {
            1: {"linajes": [1, 2], "codigo": "C2"}
        })
        self.assertEqual(universo.random.getstate(), azar_antes)

        planeta.restos_organicos_unidades = 0
        self.assertEqual(modelo.tecnicas_actuales(planeta), {})
        self.assertEqual(planeta.especies_con_tecnica_soporte, {1})
        planeta.restos_organicos_unidades = 1
        self.assertEqual(len(modelo.tecnicas_actuales(planeta)), 1)

    def test_sin_codigos_o_soporte_previo_no_basta_escasez(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.restos_organicos_unidades = 0
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_soporte_con_escasez, set())

        planeta.restos_organicos_unidades = 1
        universo.actualizar_herramientas_iniciales()
        planeta.restos_organicos_unidades = 0
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_soporte_con_escasez, set())
        planeta.restos_organicos_unidades = 1
        universo.actualizar_lenguaje_inicial()
        universo.actualizar_tecnologia_temprana()
        self.assertEqual(planeta.especies_con_tecnica_soporte, set())

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        self.preparar_soporte_y_codigos(universo)
        planeta.restos_organicos_unidades = 0
        universo.actualizar_tecnologia_temprana()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "tecnologia")
            cargado = gestor.cargar("tecnologia")
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
            for version in (universo, cargado):
                version.planetas[0].restos_organicos_unidades = 1
                version.actualizar_tecnologia_temprana()
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
            self.assertEqual(planeta.especies_con_tecnica_soporte, {1})

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["especies_con_tecnica_soporte"]
            del datos["planetas"][0]["especies_soporte_con_escasez"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("tecnologia")
            self.assertEqual(anterior.planetas[0].especies_con_tecnica_soporte,
                             set())
            self.assertEqual(anterior.planetas[0].especies_soporte_con_escasez,
                             set())
            anterior.planetas[0].restos_organicos_unidades = 1
            anterior.actualizar_tecnologia_temprana()
            self.assertEqual(anterior.planetas[0].especies_con_tecnica_soporte,
                             set())


if __name__ == "__main__":
    unittest.main()
