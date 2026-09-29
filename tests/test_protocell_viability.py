import json
import random
import tempfile
import unittest

from chemistry.protocell_viability_model import ModeloViabilidadProtocelular
from extraordinary.chemistry_support_model import ModeloApoyoQuimicoExtraordinario
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class ViabilidadTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            candidato_habitable_fase1=True,
            nombre="Viabilidad", masa_tierra=1, semieje_mayor_au=1,
            regimen_mundo="normal", alcanzo_protocelula=True,
            tipo_protocelula="protocelula_criogenica",
            etapa_quimica_historica="protocelula",
            tiene_ingredientes_prebioticos=True, tiene_agua_condensada=True,
            estado_agua_preclima="hielo", candidato_quimica_prebiotica=True,
            alcanzo_red_quimica_primitiva=True,
        )
        datos.update(cambios)
        return Planet(**datos)

    def evaluar(self, planeta):
        ModeloApoyoQuimicoExtraordinario().evaluar(planeta)
        ModeloViabilidadProtocelular().evaluar(planeta)

    def test_tres_rutas_normales(self):
        for tipo, agua, geo in (
            ("protocelula_criogenica", "hielo", False),
            ("protocelula_geoquimica", "liquida", True),
            ("protocelula_mixta", "hielo", True),
        ):
            with self.subTest(tipo=tipo):
                p = self.planeta(tipo_protocelula=tipo, estado_agua_preclima=agua,
                                  ruta_geoquimica_prebiotica=geo)
                self.evaluar(p)
                self.assertTrue(p.protocelula_viable_normal)
                self.assertTrue(p.es_candidato_abiogenesis())
                self.assertEqual(p.estado_viabilidad_protocelular, "viable_normal")

    def test_motivos_y_no_crear_logros(self):
        for cambios, motivo in (
            ({"alcanzo_protocelula": False}, "sin_protocelula"),
            ({"tipo_protocelula": None}, "tipo_no_modelado"),
            ({"candidato_habitable_fase1": False}, "sin_habitabilidad_actual"),
            ({"tiene_ingredientes_prebioticos": False}, "sin_ingredientes"),
            ({"tiene_agua_condensada": False}, "sin_agua_condensada"),
            ({"candidato_quimica_prebiotica": False}, "sin_energia"),
            ({"estado_agua_preclima": "liquida"}, "sin_confinamiento"),
            ({"tipo_protocelula": "protocelula_mixta"}, "sin_confinamiento"),
            ({"tipo_protocelula": "protocelula_geoquimica",
              "estado_agua_preclima": "liquida"}, "sin_confinamiento"),
        ):
            with self.subTest(cambios=cambios):
                p = self.planeta(**cambios)
                self.evaluar(p)
                self.assertFalse(p.protocelula_viable_normal)
                self.assertFalse(p.es_candidato_abiogenesis())
                self.assertEqual(p.estado_viabilidad_protocelular, motivo)
                self.assertEqual(p.alcanzo_protocelula, cambios.get("alcanzo_protocelula", True))

    def test_energia_exotica_no_sustituye_agua_ni_confinamiento(self):
        p = self.planeta(regimen_mundo="extraordinario",
                          tipo_regla_extraordinaria="energia_exotica",
                          intensidad_extraordinaria=0.5, candidato_quimica_prebiotica=False)
        self.evaluar(p)
        self.assertTrue(p.protocelula_viable)
        self.assertFalse(p.protocelula_viable_normal)
        self.assertEqual(p.estado_viabilidad_protocelular, "viable_extraordinaria")
        p.estado_agua_preclima = "liquida"
        self.evaluar(p)
        self.assertEqual(p.estado_viabilidad_protocelular, "sin_confinamiento")
        p.tiene_agua_condensada = False
        self.evaluar(p)
        self.assertEqual(p.estado_viabilidad_protocelular, "sin_agua_condensada")

    def test_anomalia_suple_confinamiento_y_arcano_no(self):
        for tipo, esperado in (("anomalia_fisica", True), ("arcano", False)):
            p = self.planeta(regimen_mundo="extraordinario",
                              tipo_regla_extraordinaria=tipo, intensidad_extraordinaria=0.5,
                              estado_agua_preclima="liquida")
            self.evaluar(p)
            self.assertEqual(p.protocelula_viable, esperado)
            self.assertFalse(p.protocelula_viable_normal)
            p.candidato_quimica_prebiotica = False
            self.evaluar(p)
            self.assertFalse(p.protocelula_viable)

    def test_perdida_recuperacion_historia_y_determinismo(self):
        p = self.planeta()
        modelo = ModeloViabilidadProtocelular()
        antes = p.a_dict()
        azar = random.getstate()
        modelo.evaluar(p)
        primera = p.a_dict()
        modelo.evaluar(p)
        self.assertEqual(primera, p.a_dict())
        campos = {"protocelula_viable", "protocelula_viable_normal", "estado_viabilidad_protocelular"}
        self.assertEqual({k:v for k,v in antes.items() if k not in campos},
                         {k:v for k,v in p.a_dict().items() if k not in campos})
        p.tiene_agua_condensada = False
        modelo.evaluar(p)
        self.assertFalse(p.es_candidato_abiogenesis())
        self.assertTrue(p.alcanzo_protocelula)
        p.tiene_agua_condensada = True
        modelo.evaluar(p)
        self.assertEqual(primera, p.a_dict())
        self.assertEqual(azar, random.getstate())

    def test_guardado_antiguo_nuevo_y_continuacion(self):
        u = Universe(seed=123)
        u.planetas = [self.planeta()]
        u.actualizar_apoyos_extraordinarios()
        u.actualizar_viabilidad_protocelular()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(u, "prueba")
            v = gestor.cargar("prueba")
            self.assertTrue(v.planetas[0].es_candidato_abiogenesis())
            self.assertEqual(u.planetas[0].a_dict(), v.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("protocelula_viable", "protocelula_viable_normal", "estado_viabilidad_protocelular"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("prueba")
            self.assertFalse(antiguo.planetas[0].es_candidato_abiogenesis())
            self.assertEqual(antiguo.planetas[0].estado_viabilidad_protocelular, "no_evaluado")
            antiguo.actualizar_viabilidad_protocelular()
            self.assertEqual(u.planetas[0].a_dict(), antiguo.planetas[0].a_dict())
            for universo in (u, v, antiguo):
                universo.actualizar(1)
            gestor.guardar(u, "u")
            gestor.guardar(v, "v")
            gestor.guardar(antiguo, "antiguo")
            for nombre in ("v", "antiguo"):
                self.assertEqual(json.loads((ruta.parent / "u.json").read_text()),
                                 json.loads((ruta.parent / f"{nombre}.json").read_text()))
            self.assertNotEqual(u.planetas[0].estado_viabilidad_protocelular, "no_evaluado")


if __name__ == "__main__":
    unittest.main()
