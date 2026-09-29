import json
import random
import tempfile
import unittest

from abiogenesis.replication_model import ModeloReplicacionPrebiotica
from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class ReplicacionTests(unittest.TestCase):
    def planeta(self, **cambios):
        datos = dict(
            nombre="Copia", masa_tierra=1, semieje_mayor_au=1,
            alcanzo_protocelula=True, protocelula_viable=True,
            tipo_protocelula="protocelula_criogenica",
            mecanismo_polimerizacion_prebiotica="ciclos_de_congelacion",
            estado_agua_preclima="hielo",
            alcanzo_precursores_complejos=True,
            alcanzo_polimerizacion_prebiotica=True,
            alcanzo_red_quimica_primitiva=True,
            alcanzo_compartimentalizacion_prebiotica=True,
        )
        datos.update(cambios)
        return Planet(**datos)

    def test_tres_rutas_y_determinismo(self):
        rutas = (
            ("protocelula_criogenica", "ciclos_de_congelacion", "hielo", False, "copia_en_hielo"),
            ("protocelula_geoquimica", "superficies_geoquimicas", "liquida", True, "copia_en_poros_minerales"),
            ("protocelula_mixta", "frio_y_geoquimica", "hielo", True, "copia_mixta"),
        )
        modelo = ModeloReplicacionPrebiotica()
        for tipo, polimerizacion, agua, geo, ruta in rutas:
            with self.subTest(tipo=tipo):
                p = self.planeta(tipo_protocelula=tipo,
                                 mecanismo_polimerizacion_prebiotica=polimerizacion,
                                 estado_agua_preclima=agua,
                                 ruta_geoquimica_prebiotica=geo)
                azar = random.getstate()
                modelo.evaluar(p)
                self.assertTrue(p.replicacion_prebiotica_activa)
                self.assertTrue(p.alcanzo_replicacion_prebiotica)
                self.assertEqual(p.mecanismo_replicacion_prebiotica, ruta)
                primera = p.a_dict()
                modelo.evaluar(p)
                self.assertEqual(primera, p.a_dict())
                self.assertEqual(azar, random.getstate())

    def test_viabilidad_sola_no_basta(self):
        cambios = (
            {"protocelula_viable": False},
            {"alcanzo_protocelula": False},
            {"alcanzo_precursores_complejos": False},
            {"alcanzo_polimerizacion_prebiotica": False},
            {"alcanzo_red_quimica_primitiva": False},
            {"alcanzo_compartimentalizacion_prebiotica": False},
            {"mecanismo_polimerizacion_prebiotica": "superficies_geoquimicas"},
            {"estado_agua_preclima": "liquida"},
        )
        for cambio in cambios:
            with self.subTest(cambio=cambio):
                p = self.planeta(**cambio)
                ModeloReplicacionPrebiotica().evaluar(p)
                self.assertFalse(p.replicacion_prebiotica_activa)
                self.assertFalse(p.alcanzo_replicacion_prebiotica)
                self.assertIsNone(p.mecanismo_replicacion_prebiotica)

    def test_perdida_recuperacion_conserva_historia(self):
        p = self.planeta()
        modelo = ModeloReplicacionPrebiotica()
        modelo.evaluar(p)
        p.protocelula_viable = False
        modelo.evaluar(p)
        self.assertFalse(p.replicacion_prebiotica_activa)
        self.assertTrue(p.alcanzo_replicacion_prebiotica)
        self.assertEqual(p.mecanismo_replicacion_prebiotica, "copia_en_hielo")
        p.protocelula_viable = True
        modelo.evaluar(p)
        self.assertTrue(p.replicacion_prebiotica_activa)

    def test_anomalia_puede_sostener_sin_permitir_copia(self):
        p = self.planeta(regimen_mundo="extraordinario",
                         tipo_regla_extraordinaria="anomalia_fisica",
                         estado_agua_preclima="liquida")
        # El modelo de viabilidad pudo aceptar confinamiento anómalo.
        self.assertTrue(p.protocelula_viable)
        ModeloReplicacionPrebiotica().evaluar(p)
        self.assertFalse(p.replicacion_prebiotica_activa)

    def test_guardado_y_continuacion(self):
        u = Universe(seed=23)
        u.planetas = [self.planeta()]
        u.actualizar_replicacion_prebiotica()
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            ruta = gestor.guardar(u, "nuevo")
            cargado = gestor.cargar("nuevo")
            self.assertEqual(u.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            datos = json.loads(ruta.read_text())
            for campo in ("replicacion_prebiotica_activa",
                          "alcanzo_replicacion_prebiotica",
                          "mecanismo_replicacion_prebiotica"):
                del datos["planetas"][0][campo]
            ruta.write_text(json.dumps(datos))
            antiguo = gestor.cargar("nuevo")
            self.assertFalse(antiguo.planetas[0].alcanzo_replicacion_prebiotica)
            self.assertFalse(antiguo.planetas[0].replicacion_prebiotica_activa)
            self.assertIsNone(antiguo.planetas[0].mecanismo_replicacion_prebiotica)
            antiguo.actualizar_replicacion_prebiotica()
            self.assertEqual(u.planetas[0].a_dict(), antiguo.planetas[0].a_dict())
            for universo in (u, cargado):
                universo.actualizar(1)
            self.assertEqual([p.a_dict() for p in u.planetas],
                             [p.a_dict() for p in cargado.planetas])
            self.assertEqual(u.random.getstate(), cargado.random.getstate())


if __name__ == "__main__":
    unittest.main()
