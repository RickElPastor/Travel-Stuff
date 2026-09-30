import unittest

from biology.selection_model import ModeloSeleccionUnicelular
from planets.planet import Planet


class SeleccionUnicelularTests(unittest.TestCase):
    def test_ajuste_cambia_con_el_agua_y_con_la_linea(self):
        modelo = ModeloSeleccionUnicelular()
        planeta = Planet(
            "Vida", 1, 1, poblacion_unicelular=3,
            rasgo_linea_unicelular=0, estado_agua_preclima="hielo",
        )
        self.assertTrue(modelo.esta_ajustada(planeta))

        planeta.estado_agua_preclima = "liquida"
        self.assertFalse(modelo.esta_ajustada(planeta))
        planeta.rasgo_linea_unicelular = modelo.elegir(planeta, 0, 2)
        self.assertTrue(modelo.esta_ajustada(planeta))

        copia = Planet.desde_dict(planeta.a_dict())
        self.assertEqual(modelo.esta_ajustada(copia),
                         modelo.esta_ajustada(planeta))
        planeta.poblacion_unicelular = 0
        self.assertFalse(modelo.esta_ajustada(planeta))
        planeta.estado_agua_preclima = None
        planeta.poblacion_unicelular = 1
        self.assertFalse(modelo.esta_ajustada(planeta))

    def test_el_rasgo_favorecido_depende_del_agua_actual(self):
        modelo = ModeloSeleccionUnicelular()
        casos = (
            ("hielo", 1, 0, 0, 1),
            ("hielo", 0, 2, 0, 0),
            ("liquida", 1, 2, 2, 1),
            ("liquida", 0, 2, 2, 1),
            ("liquida", 2, 0, 2, 0),
            (None, 1, 0, 1, 0),
        )
        for agua, anterior, variante, esperado, favorecidas in casos:
            with self.subTest(agua=agua, anterior=anterior, variante=variante):
                planeta = Planet("Vida", 1, 1, estado_agua_preclima=agua)
                resultado = modelo.elegir(planeta, anterior, variante)
                self.assertEqual(resultado, esperado)
                self.assertEqual(planeta.variantes_biologicas_favorecidas,
                                 favorecidas)
                self.assertEqual(planeta.variantes_biologicas_descartadas,
                                 1 - favorecidas)
                self.assertEqual(planeta.estado_agua_preclima, agua)
                self.assertFalse(planeta.candidato_habitable_fase1)


if __name__ == "__main__":
    unittest.main()
