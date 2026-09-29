import json
import random
import tempfile
import unittest

from extraordinary.chemistry_support_model import ModeloApoyoQuimicoExtraordinario
from extraordinary.world_rules_model import ModeloReglasMundo
from chemistry.protocell_viability_model import ModeloViabilidadProtocelular
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class ApoyoExtraordinarioTests(unittest.TestCase):
    def planeta(self, tipo="arcano", **cambios):
        datos = dict(
            candidato_habitable_fase1=True,
            nombre="Prueba", masa_tierra=1, semieje_mayor_au=1,
            regimen_mundo="extraordinario", tipo_regla_extraordinaria=tipo,
            intensidad_extraordinaria=0.6, tiene_ingredientes_prebioticos=True,
            tiene_agua_condensada=True, candidato_quimica_prebiotica=True,
            alcanzo_red_quimica_primitiva=True, alcanzo_protocelula=True,
            temperatura_equilibrio_cero_albedo_k=280,
            etapa_quimica_historica="protocelula",
            tipo_protocelula="protocelula_criogenica", estado_agua_preclima="hielo",
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_tipos_preservan_todos_los_campos_anteriores_y_azar(self):
        campos = {"catalisis_arcana", "confinamiento_anomalo", "energia_quimica_exotica"}
        for tipo, campo in zip(ModeloReglasMundo.TIPOS_EXTRAORDINARIOS,
                               ("catalisis_arcana", "confinamiento_anomalo", "energia_quimica_exotica")):
            with self.subTest(tipo=tipo):
                planeta = self.planeta(tipo)
                antes = planeta.a_dict()
                azar = random.getstate()
                modelo = ModeloApoyoQuimicoExtraordinario()
                modelo.evaluar(planeta)
                despues = planeta.a_dict()
                self.assertEqual(getattr(planeta, campo), 0.6)
                self.assertEqual(sum(despues[c] for c in campos), 0.6)
                for clave in antes.keys() - campos:
                    self.assertEqual(antes[clave], despues[clave], clave)
                modelo.evaluar(planeta)
                self.assertEqual(despues, planeta.a_dict())
                self.assertEqual(azar, random.getstate())

    def test_sin_condiciones_no_hay_apoyo(self):
        for tipo in ModeloReglasMundo.TIPOS_EXTRAORDINARIOS:
            for cambios in ({"regimen_mundo": "normal"},
                            {"tiene_ingredientes_prebioticos": False},
                            {"tiene_agua_condensada": False},
                            {"intensidad_extraordinaria": 0},
                            {"intensidad_extraordinaria": 1.1}):
                planeta = self.planeta(tipo, **cambios)
                ModeloApoyoQuimicoExtraordinario().evaluar(planeta)
                self.assertEqual(planeta.obtener_apoyo_protocelular_extraordinario(), 0)

    def test_anomalia_necesita_red_y_no_crea_protocelula(self):
        planeta = self.planeta("anomalia_fisica", alcanzo_red_quimica_primitiva=False,
                               alcanzo_protocelula=False)
        modelo = ModeloApoyoQuimicoExtraordinario()
        modelo.evaluar(planeta)
        self.assertEqual(planeta.confinamiento_anomalo, 0)
        planeta.alcanzo_red_quimica_primitiva = True
        modelo.evaluar(planeta)
        self.assertEqual(planeta.confinamiento_anomalo, 0.6)
        self.assertFalse(planeta.es_candidato_abiogenesis())
        self.assertEqual(planeta.obtener_apoyo_protocelular_extraordinario(), 0)

    def test_energia_alternativa_y_perdida_de_apoyo_sin_borrar_historia(self):
        planeta = self.planeta("energia_exotica", candidato_quimica_prebiotica=False)
        modelo = ModeloApoyoQuimicoExtraordinario()
        modelo.evaluar(planeta)
        ModeloViabilidadProtocelular().evaluar(planeta)
        self.assertTrue(planeta.es_candidato_abiogenesis())
        self.assertFalse(planeta.ruta_uv_prebiotica)
        self.assertFalse(planeta.ruta_geoquimica_prebiotica)
        planeta.tiene_agua_condensada = False
        modelo.evaluar(planeta)
        ModeloViabilidadProtocelular().evaluar(planeta)
        self.assertEqual(planeta.energia_quimica_exotica, 0)
        self.assertFalse(planeta.es_candidato_abiogenesis())
        self.assertTrue(planeta.alcanzo_protocelula)
        self.assertEqual(planeta.etapa_quimica_historica, "protocelula")

    def test_guardado_antiguo_y_nuevo(self):
        universo = Universe(seed=123)
        universo.planetas = [self.planeta(tipo) for tipo in ModeloReglasMundo.TIPOS_EXTRAORDINARIOS]
        universo.actualizar_apoyos_extraordinarios()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(universo, "prueba")
            cargado = gestor.cargar("prueba")
            self.assertEqual([p.a_dict() for p in universo.planetas],
                             [p.a_dict() for p in cargado.planetas])
            self.assertEqual(universo.random.getstate(), cargado.random.getstate())
            # Simula un v3 previo a estos campos.
            datos = json.loads(ruta.read_text())
            for planeta in datos["planetas"]:
                for campo in ("catalisis_arcana", "confinamiento_anomalo", "energia_quimica_exotica"):
                    del planeta[campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("prueba")
            self.assertTrue(all(p.obtener_apoyo_protocelular_extraordinario() == 0
                                for p in antiguo.planetas))
            antiguo.actualizar_apoyos_extraordinarios()
            self.assertEqual([p.a_dict() for p in universo.planetas],
                             [p.a_dict() for p in antiguo.planetas])
            # La continuación usa el ciclo real de actualización.
            universo.actualizar(1)
            cargado.actualizar(1)
            gestor.guardar(universo, "continuo")
            gestor.guardar(cargado, "reanudado")
            self.assertEqual(json.loads((ruta.parent / "continuo.json").read_text()),
                             json.loads((ruta.parent / "reanudado.json").read_text()))

    def test_misma_semilla_asigna_mismas_reglas(self):
        modelo = ModeloReglasMundo()
        for numero in range(100):
            a = Planet(str(numero), 1, 1)
            b = Planet(str(numero), 1, 1)
            modelo.asignar(a, 123)
            modelo.asignar(b, 123)
            self.assertEqual(a.a_dict(), b.a_dict())


if __name__ == "__main__":
    unittest.main()
