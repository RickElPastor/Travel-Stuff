import json
import tempfile
import unittest

from biology.initial_language_model import ModeloLenguajeInicial
from planets.planet import Planet
from universe.save_manager import SaveManager
from universe.universe import Universe


class LenguajeInicialTests(unittest.TestCase):
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

    def test_dos_rutas_crean_codigos_estables_y_una_no(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = ModeloLenguajeInicial()
        azar_antes = universo.random.getstate()
        antes = planeta.a_dict()
        self.assertEqual(modelo.repertorios_actuales(planeta), {})
        self.assertEqual(planeta.a_dict(), antes)
        universo.actualizar_cultura_inicial()
        universo.actualizar_lenguaje_inicial()
        self.assertEqual(planeta.codigos_senal_por_especie,
                         {1: {"luz": "C1", "restos": "C2"}})
        self.assertEqual(modelo.repertorios_actuales(planeta),
                         {1: {"luz": "C1", "restos": "C2"}})
        for _ in range(5):
            universo.actualizar_lenguaje_inicial()
        self.assertEqual(planeta.codigos_senal_por_especie,
                         {1: {"luz": "C1", "restos": "C2"}})
        self.assertEqual(universo.random.getstate(), azar_antes)

        planeta.restos_organicos_unidades = 0
        self.assertEqual(modelo.repertorios_actuales(planeta), {})
        self.assertEqual(planeta.codigos_senal_por_especie,
                         {1: {"luz": "C1", "restos": "C2"}})
        planeta.restos_organicos_unidades = 1
        self.assertEqual(len(modelo.repertorios_actuales(planeta)), 1)

    def test_ruta_nueva_recibe_codigo_siguiente_sin_cambiar_anteriores(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        universo.actualizar_lenguaje_inicial()
        planeta.poblacion_unicelular = 5
        planeta.linajes_unicelulares_vivos.append(3)
        planeta.clasificacion_especies_unicelulares[3] = {
            "especie_id": 2, "distancia": 0
        }
        planeta.linajes_depredadores = {1, 2}
        planeta.recursos_recordados_por_linaje[1].append("presas")
        planeta.recursos_recordados_por_linaje[2].append("presas")
        universo.actualizar_lenguaje_inicial()
        self.assertEqual(planeta.codigos_senal_por_especie, {
            1: {"luz": "C1", "restos": "C2", "presas": "C3"}
        })

    def test_una_practica_o_aviso_unilateral_no_forma_repertorio(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        planeta.linajes_descomponedores = {1}
        planeta.unidades_descomponedoras_activas = 2
        universo.actualizar_lenguaje_inicial()
        self.assertEqual(planeta.codigos_senal_por_especie, {})
        planeta.linajes_descomponedores.add(2)
        planeta.unidades_descomponedoras_activas = 4
        planeta.recursos_recordados_por_linaje[2] = ["luz"]
        universo.actualizar_lenguaje_inicial()
        self.assertEqual(planeta.codigos_senal_por_especie, {})

    def test_guardado_carga_y_partida_anterior(self):
        universo = self.universo()
        universo.actualizar_lenguaje_inicial()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "lenguaje")
            cargado = gestor.cargar("lenguaje")
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())
            for version in (universo, cargado):
                version.planetas[0].restos_organicos_unidades = 0
                version.actualizar_lenguaje_inicial()
            self.assertEqual(cargado.planetas[0].a_dict(),
                             universo.planetas[0].a_dict())

            datos = json.loads(ruta.read_text())
            del datos["planetas"][0]["codigos_senal_por_especie"]
            ruta.write_text(json.dumps(datos))
            anterior = gestor.cargar("lenguaje")
            self.assertEqual(anterior.planetas[0].codigos_senal_por_especie, {})
            anterior.actualizar_lenguaje_inicial()
            self.assertEqual(anterior.planetas[0].codigos_senal_por_especie,
                             {1: {"luz": "C1", "restos": "C2"}})


if __name__ == "__main__":
    unittest.main()
