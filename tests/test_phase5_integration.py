import json
import tempfile
import unittest

from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class IntegracionFase5Tests(unittest.TestCase):
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
            ruta_metabolica_inicial="consumo_organicos",
            linajes_cohesivos={1, 2},
            linajes_fotosinteticos={1, 2}, unidades_productoras_activas=4,
            linajes_descomponedores={1, 2},
            unidades_descomponedoras_activas=4,
            restos_organicos_unidades=1,
        )]
        return universo

    def observar_intervalo(self, universo):
        planeta = universo.planetas[0]
        recicladas_antes = {planeta: planeta.total_unidades_recicladas}
        universo.actualizar_ciclo_organico()
        universo.actualizar_restos_observados(recicladas_antes)
        universo.actualizar_aprendizaje_inicial()
        universo.actualizar_transmision_social()
        universo.actualizar_herramientas_iniciales()
        universo.actualizar_comunicacion_inicial()
        universo.actualizar_cultura_inicial()
        universo.actualizar_lenguaje_inicial()
        universo.actualizar_tecnologia_temprana()

    def test_material_reciclado_permite_ruta_y_recuperacion(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        azar_antes = universo.random.getstate()
        self.observar_intervalo(universo)
        self.assertEqual(planeta.restos_organicos_unidades, 0)
        self.assertEqual(planeta.restos_observados_intervalo, 1)
        self.assertEqual(planeta.especies_con_soporte_organico, {1})
        self.assertEqual(planeta.especies_con_senal_recurso, {1})
        self.assertEqual(planeta.rutas_culturales_por_especie[1],
                         ["luz", "restos"])
        self.assertEqual(planeta.codigos_senal_por_especie[1],
                         {"luz": "C1", "restos": "C2"})
        self.assertEqual(planeta.especies_con_tecnica_soporte, set())

        self.observar_intervalo(universo)
        self.assertEqual(planeta.restos_observados_intervalo, 0)
        self.assertEqual(planeta.especies_soporte_con_escasez, {1})
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "fase5")
            cargado = gestor.cargar("fase5")
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
            for version in (universo, cargado):
                version.planetas[0].restos_organicos_unidades = 1
                self.observar_intervalo(version)
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())

        self.assertEqual(planeta.especies_con_tecnica_soporte, {1})
        self.assertEqual(planeta.restos_organicos_unidades, 0)
        self.assertEqual(planeta.restos_observados_intervalo, 1)
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_guardado_anterior_inicia_sin_observacion_inventada(self):
        universo = self.universo()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "anterior")
            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["restos_observados_intervalo"]
            ruta.write_text(json.dumps(datos))
            cargado = gestor.cargar("anterior")
        self.assertEqual(cargado.planetas[0].restos_observados_intervalo, 0)


if __name__ == "__main__":
    unittest.main()
