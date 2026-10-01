import json
import tempfile
import unittest

from biology.initial_culture_model import ModeloCulturaInicial
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class CulturaInicialTests(unittest.TestCase):
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
            linajes_fotosinteticos={1}, unidades_productoras_activas=2,
            recursos_recordados_por_linaje={1: ["luz"], 2: ["luz"]},
        )]
        return universo

    def test_aviso_de_ida_no_basta_y_dos_avisos_crean_practica(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloCulturaInicial()
        azar_antes = universo.random.getstate()
        self.assertEqual(modelo.practicas_actuales(planeta), {})
        universo.actualizar_cultura_inicial()
        self.assertEqual(planeta.rutas_culturales_por_especie, {})

        planeta.linajes_fotosinteticos.add(2)
        planeta.unidades_productoras_activas = 4
        antes = planeta.a_dict()
        self.assertEqual(modelo.practicas_actuales(planeta), {1: ["luz"]})
        self.assertEqual(planeta.a_dict(), antes)
        universo.actualizar_cultura_inicial()
        self.assertEqual(planeta.rutas_culturales_por_especie, {1: ["luz"]})
        for _ in range(5):
            universo.actualizar_cultura_inicial()
        self.assertEqual(planeta.rutas_culturales_por_especie, {1: ["luz"]})
        self.assertEqual(universo.random.getstate(), azar_antes)

        planeta.unidades_productoras_activas = 0
        self.assertEqual(modelo.practicas_actuales(planeta), {})
        self.assertEqual(planeta.rutas_culturales_por_especie, {1: ["luz"]})
        planeta.unidades_productoras_activas = 4
        self.assertEqual(modelo.practicas_actuales(planeta), {1: ["luz"]})

    def test_mismo_recurso_y_misma_especie_son_necesarios(self):
        planeta = self.universo().planetas[0]
        modelo = ModeloCulturaInicial()
        planeta.linajes_fotosinteticos.add(2)
        planeta.unidades_productoras_activas = 4
        planeta.recursos_recordados_por_linaje[2] = ["restos"]
        self.assertEqual(modelo.practicas_actuales(planeta), {})
        planeta.recursos_recordados_por_linaje[2] = ["luz"]
        planeta.clasificacion_especies_unicelulares[2]["especie_id"] = 2
        self.assertEqual(modelo.practicas_actuales(planeta), {})
        planeta.clasificacion_especies_unicelulares[2]["especie_id"] = 1
        planeta.linajes_unicelulares_vivos.remove(2)
        planeta.poblacion_unicelular -= 1
        self.assertEqual(modelo.practicas_actuales(planeta), {})

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.linajes_fotosinteticos.add(2)
        planeta.unidades_productoras_activas = 4
        universo.actualizar_cultura_inicial()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "cultura")
            cargado = gestor.cargar("cultura")
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())
            for version in (universo, cargado):
                version.planetas[0].unidades_productoras_activas = 0
                version.actualizar_cultura_inicial()
            self.assertEqual(cargado.planetas[0].a_dict(), planeta.a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["rutas_culturales_por_especie"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("cultura")
            self.assertEqual(anterior.planetas[0].rutas_culturales_por_especie,
                             {})
            anterior.actualizar_cultura_inicial()
            self.assertEqual(anterior.planetas[0].rutas_culturales_por_especie,
                             {1: ["luz"]})


if __name__ == "__main__":
    unittest.main()
