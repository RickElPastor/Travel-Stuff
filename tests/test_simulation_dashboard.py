import unittest

from planets.planet import Planet
from simulation import Simulation
from ui.simulation_ui import SimulationUI
from universe import Universe


class PantallaFalsa:
    def __init__(self, alto, ancho):
        self.alto = alto
        self.ancho = ancho
        self.erase()

    def getmaxyx(self):
        return self.alto, self.ancho

    def erase(self):
        self.filas = [[" "] * self.ancho for _ in range(self.alto)]

    def addnstr(self, y, x, valor, limite, atributo=0):
        for indice, letra in enumerate(str(valor)[:limite]):
            if x + indice < self.ancho:
                self.filas[y][x + indice] = letra

    def refresh(self):
        pass

    def linea(self, numero):
        return "".join(self.filas[numero]).rstrip()


class PanelTests(unittest.TestCase):
    def test_tres_vistas_y_controles_en_terminal_minima(self):
        universo = Universe(seed=374852300)
        universo.time.anio = 2_780_000_000
        planeta = Planet(
            "Planeta-Prueba", 1, 1,
            alcanzo_protocelula=True, protocelula_viable=True,
            replicacion_prebiotica_activa=True,
            alcanzo_replicacion_prebiotica=True,
            copias_heredables=21, variaciones_prebioticas=3,
            variantes_favorecidas=1, variantes_descartadas=2,
            patron_copia=0,
        )
        universo.planetas = [planeta]
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa(24, 72)
        antes = planeta.a_dict()

        interfaz._dibujar(pantalla)
        self.assertIn("TRAVEL STUFF", pantalla.linea(1))
        self.assertIn("Protocélulas 1", pantalla.linea(9))
        self.assertIn("Mundos con selección 1", pantalla.linea(15))
        self.assertIn("PRIMERA VIDA", pantalla.linea(16))
        self.assertIn("Línea activa", pantalla.linea(17))
        self.assertIn("EVENTOS RECIENTES", pantalla.linea(19))
        self.assertIn("Esc Menú", pantalla.linea(23))

        interfaz._procesar_tecla(pantalla, ord("2"))
        interfaz._dibujar(pantalla)
        self.assertIn("ESTRUCTURA DEL UNIVERSO", pantalla.linea(6))
        self.assertIn("Planetas 1", pantalla.linea(12))
        interfaz._procesar_tecla(pantalla, ord("3"))
        interfaz._dibujar(pantalla)
        self.assertIn("HABITABILIDAD", pantalla.linea(6))
        self.assertIn("Candidatos químicos", pantalla.linea(12))
        self.assertEqual(antes, planeta.a_dict())

    def test_linea_inactiva_y_primera_vida_historica_se_explican(self):
        universo = Universe(seed=1)
        universo.planetas = [Planet(
            "Planeta-Prueba", 1, 1,
            alcanzo_protocelula=True, copias_heredables=41,
            alcanzo_primera_vida=True, anio_primera_vida=100,
        )]
        pantalla = PantallaFalsa(24, 72)
        SimulationUI(Simulation(universo))._dibujar(pantalla)
        self.assertIn("activa 0", pantalla.linea(16))
        self.assertIn("histórica 1", pantalla.linea(16))
        self.assertIn("Línea inactiva", pantalla.linea(17))
        self.assertIn("41 copias históricas", pantalla.linea(17))

    def test_eventos_no_tapan_los_controles_y_se_desplazan(self):
        universo = Universe(seed=1)
        universo.event_manager.eventos = [f"Evento {n}" for n in range(12)]
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa(24, 72)
        interfaz._dibujar(pantalla)
        self.assertIn("Evento 11", pantalla.linea(21))
        interfaz._subir_eventos()
        interfaz._dibujar(pantalla)
        self.assertIn("Evento 10", pantalla.linea(21))
        self.assertIn("Esc Menú", pantalla.linea(23))

    def test_terminal_alta_reserva_mas_espacio_para_eventos(self):
        interfaz = SimulationUI(Simulation(Universe(seed=1)))
        pantalla = PantallaFalsa(30, 100)
        interfaz._dibujar(pantalla)
        self.assertIn("EVENTOS RECIENTES", pantalla.linea(19))
        self.assertIn("Esc Menú", pantalla.linea(29))
        self.assertTrue(pantalla.linea(28).startswith("─"))


if __name__ == "__main__":
    unittest.main()
