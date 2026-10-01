import json
import tempfile
import unittest

from biology.initial_communication_model import ModeloComunicacionInicial
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class ComunicacionInicialTests(unittest.TestCase):
    def universo(self):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Mundo", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima="liquida",
            candidato_quimica_prebiotica=True,
            alcanzo_organicos_simples=True,
            poblacion_unicelular=6,
            linajes_unicelulares_vivos=[1, 1, 2, 2, 3, 3],
            clasificacion_especies_unicelulares={
                1: {"especie_id": 1, "distancia": 0},
                2: {"especie_id": 1, "distancia": 1},
                3: {"especie_id": 2, "distancia": 0},
            },
            fuentes_energia_potenciales=["organicos_ambientales"],
            linajes_cohesivos={1, 2, 3},
            linajes_fotosinteticos={1}, unidades_productoras_activas=2,
            linajes_descomponedores={3}, unidades_descomponedoras_activas=2,
            restos_organicos_unidades=1,
            recursos_recordados_por_linaje={
                1: ["luz"], 2: ["luz"], 3: ["restos"]
            },
        )]
        return universo

    def test_senal_actual_tiene_emisor_receptor_y_recurso(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloComunicacionInicial()
        antes = planeta.a_dict()
        azar_antes = universo.random.getstate()
        self.assertEqual(modelo.senales_actuales(planeta), [{
            "especie": 1, "origen": 1, "destino": 2, "recurso": "luz"
        }])
        self.assertEqual(planeta.a_dict(), antes)
        universo.actualizar_comunicacion_inicial()
        self.assertEqual(planeta.especies_con_senal_recurso, {1})
        for _ in range(5):
            universo.actualizar_comunicacion_inicial()
        self.assertEqual(planeta.especies_con_senal_recurso, {1})
        self.assertEqual(universo.random.getstate(), azar_antes)

        planeta.unidades_productoras_activas = 0
        self.assertEqual(modelo.senales_actuales(planeta), [])
        self.assertEqual(planeta.especies_con_senal_recurso, {1})

    def test_no_hay_senal_sin_memoria_colonia_o_recurso_disponible(self):
        planeta = self.universo().planetas[0]
        modelo = ModeloComunicacionInicial()
        planeta.recursos_recordados_por_linaje[1].clear()
        self.assertEqual(modelo.senales_actuales(planeta), [])
        planeta.recursos_recordados_por_linaje[1] = ["luz"]
        planeta.linajes_unicelulares_vivos.remove(2)
        planeta.poblacion_unicelular -= 1
        self.assertEqual(modelo.senales_actuales(planeta), [])
        planeta.linajes_unicelulares_vivos.append(2)
        planeta.poblacion_unicelular += 1
        planeta.estado_agua_preclima = "hielo"
        self.assertEqual(modelo.senales_actuales(planeta), [])

    def test_restos_reciclados_no_son_un_aviso_actual(self):
        planeta = self.universo().planetas[0]
        planeta.linajes_descomponedores = {1}
        planeta.unidades_descomponedoras_activas = 2
        planeta.linajes_fotosinteticos.clear()
        planeta.unidades_productoras_activas = 0
        planeta.recursos_recordados_por_linaje[1] = ["restos"]
        modelo = ModeloComunicacionInicial()
        self.assertEqual(modelo.senales_actuales(planeta)[0]["recurso"], "restos")
        planeta.restos_organicos_unidades = 0
        self.assertEqual(modelo.senales_actuales(planeta), [])

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        universo.actualizar_comunicacion_inicial()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "comunicacion")
            cargado = gestor.cargar("comunicacion")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            self.assertEqual(
                ModeloComunicacionInicial().senales_actuales(cargado.planetas[0]),
                ModeloComunicacionInicial().senales_actuales(universo.planetas[0])
            )
            for version in (universo, cargado):
                version.planetas[0].unidades_productoras_activas = 0
                version.actualizar_comunicacion_inicial()
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["especies_con_senal_recurso"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("comunicacion")
            self.assertEqual(anterior.planetas[0].especies_con_senal_recurso,
                             set())
            anterior.actualizar_comunicacion_inicial()
            self.assertEqual(anterior.planetas[0].especies_con_senal_recurso,
                             {1})


if __name__ == "__main__":
    unittest.main()
