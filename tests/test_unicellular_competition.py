import tempfile
import unittest

from planets.planet import Planet
from save_manager import SaveManager
from universe import Universe


class CompetenciaUnicelularTests(unittest.TestCase):
    def universo(self, agua="liquida"):
        universo = Universe(seed=73)
        universo.planetas = [Planet(
            "Vida", 1, 1, sistema_nombre="Sistema", vida_activa=True,
            estado_agua_preclima=agua, poblacion_unicelular=3,
            nacimientos_unicelulares=20, muertes_unicelulares=17,
            nacimientos_biologicos_procesados=20,
            proximo_crecimiento_unicelular_anio=101_000_000,
            rasgos_unicelulares_vivos=[0, 2, 2],
            linajes_unicelulares_vivos=[11, 7, 5],
            linaje_observado_id=11, rasgo_linea_unicelular=0,
        )]
        return universo

    def avanzar(self, universo, anio):
        universo.time.anio = anio
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()

    def test_compara_identidades_sin_confundir_unidades_con_linajes(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = universo.modelo_seleccion_unicelular
        planeta.linajes_unicelulares_vivos = [11, 7, 7]
        antes = planeta.a_dict()
        self.assertEqual(modelo.linajes_ajustados(planeta), [7])
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 7)
        self.assertEqual(planeta.a_dict(), antes)

    def test_empate_conserva_observado_o_elige_primera_unidad_ajustada(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = universo.modelo_seleccion_unicelular
        self.assertEqual(modelo.linajes_ajustados(planeta), [7, 5])
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 7)
        planeta.linaje_observado_id = 5
        planeta.rasgo_linea_unicelular = 2
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 5)
        planeta.estado_agua_preclima = "hielo"
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 11)

    def test_sin_regla_o_sin_rasgo_ajustado_conserva_un_linaje_vivo(self):
        universo = self.universo()
        planeta = universo.planetas[0]
        modelo = universo.modelo_seleccion_unicelular
        planeta.estado_agua_preclima = None
        self.assertEqual(modelo.linajes_ajustados(planeta), [])
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 11)
        planeta.estado_agua_preclima = "liquida"
        planeta.rasgos_unicelulares_vivos = [0, 1, 1]
        self.assertEqual(modelo.linajes_ajustados(planeta), [])
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 11)
        planeta.linaje_observado_id = 99
        self.assertEqual(modelo.elegir_linaje_reproductor(planeta), 5)

    def test_agua_cambia_descendencia_solo_al_nacer_sin_inventar_variaciones(self):
        universo = self.universo("hielo")
        planeta = universo.planetas[0]
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        azar = universo.random.getstate()
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [7, 5, 11, 11])

        planeta.estado_agua_preclima = "liquida"
        antes = planeta.a_dict()
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.a_dict(), antes)
        self.avanzar(universo, 102_000_000)
        self.assertEqual(planeta.linaje_observado_id, 7)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [5, 11, 11, 7, 7])
        self.assertEqual(planeta.rasgos_unicelulares_vivos[-2:], [2, 2])
        self.assertEqual(universo.random.getstate(), azar)

        campos_actualizados = {
            "poblacion_unicelular", "nacimientos_unicelulares",
            "muertes_unicelulares", "proximo_crecimiento_unicelular_anio",
            "nacimientos_biologicos_procesados", "rasgo_linea_unicelular",
            "rasgos_unicelulares_vivos", "linaje_observado_id",
            "linajes_unicelulares_vivos",
        }
        despues = planeta.a_dict()
        for campo, valor in antes.items():
            if campo not in campos_actualizados:
                self.assertEqual(despues[campo], valor, campo)

    def test_ajuste_no_impide_extincion_ni_resucita_linajes(self):
        universo = self.universo("hielo")
        planeta = universo.planetas[0]
        modelo = universo.modelo_seleccion_unicelular
        self.assertTrue(modelo.esta_ajustada(planeta))
        planeta.vida_activa = False
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.poblacion_unicelular, 0)
        self.assertEqual(modelo.linajes_ajustados(planeta), [])
        self.assertIsNone(modelo.elegir_linaje_reproductor(planeta))
        self.assertEqual(planeta.linajes_unicelulares_vivos, [])

    def test_guardado_y_pasos_distintos_con_cambio_ambiental_compartido(self):
        corto = self.universo("hielo")
        largo = self.universo("hielo")
        for anio in range(101_000_000, 106_000_000, 1_000_000):
            self.avanzar(corto, anio)
        self.avanzar(largo, 105_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(corto, "competencia")
            cargado = gestor.cargar("competencia")
            self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
            for universo in (corto, largo, cargado):
                universo.planetas[0].estado_agua_preclima = "liquida"
            for anio in range(106_000_000, 121_000_000, 1_000_000):
                self.avanzar(corto, anio)
                self.avanzar(cargado, anio)
            self.avanzar(largo, 120_000_000)
        self.assertEqual(corto.planetas[0].a_dict(), cargado.planetas[0].a_dict())
        self.assertEqual(corto.planetas[0].a_dict(), largo.planetas[0].a_dict())
        self.assertEqual(corto.random.getstate(), cargado.random.getstate())

    def test_guardado_anterior_puede_seleccionar_identidad_provisional(self):
        universo = self.universo()
        datos = universo.planetas[0].a_dict()
        del datos["linajes_unicelulares_vivos"]
        del datos["linaje_observado_id"]
        planeta = Planet.desde_dict(datos)
        universo.planetas = [planeta]
        universo.modelo_herencia_unicelular.PROBABILIDAD_VARIACION = 0.0
        self.avanzar(universo, 101_000_000)
        self.assertEqual(planeta.linaje_observado_id, -3)
        self.assertEqual(planeta.linajes_unicelulares_vivos, [-3] * 4)
        self.assertEqual(planeta.variaciones_unicelulares, 0)


if __name__ == "__main__":
    unittest.main()
