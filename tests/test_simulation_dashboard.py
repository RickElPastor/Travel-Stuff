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
    def test_cinco_vistas_y_controles_en_terminal_minima(self):
        universo = Universe(seed=374852300)
        universo.time.anio = 2_780_000_000
        planeta = Planet(
            "Planeta-Prueba", 1, 1,
            alcanzo_protocelula=True, protocelula_viable=True,
            replicacion_prebiotica_activa=True,
            alcanzo_replicacion_prebiotica=True,
            copias_heredables=21, variaciones_prebioticas=3,
            variantes_favorecidas=1, variantes_descartadas=2,
            patron_copia=0, vida_activa=True,
            alcanzo_primera_vida=True, poblacion_unicelular=3,
            nacimientos_unicelulares=7, muertes_unicelulares=4,
            rasgo_linea_unicelular=2, variaciones_unicelulares=3,
            variantes_biologicas_favorecidas=1,
            variantes_biologicas_descartadas=2,
            rasgos_unicelulares_vivos=[0, 2, 2],
            linajes_unicelulares_vivos=[1, 2, 2],
            linaje_observado_id=2,
            historial_linajes_unicelulares={
                1: {"progenitor_id": None, "rasgo": 0, "origen": "fundacion"},
                2: {"progenitor_id": 1, "rasgo": 2, "origen": "variacion"},
            },
            estado_agua_preclima="liquida",
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
        interfaz._procesar_tecla(pantalla, ord("4"))
        interfaz._dibujar(pantalla)
        self.assertIn("VIDA UNICELULAR", pantalla.linea(6))
        self.assertIn("Rasgos vivos 2 · linajes 2 · 0:1 1:0 2:2",
                      pantalla.linea(7))
        self.assertIn("Mundos con población activa 1", pantalla.linea(8))
        self.assertIn("Especies vivas 1", pantalla.linea(8))
        self.assertIn("Especies extintas 0", pantalla.linea(9))
        self.assertIn("Especies reg. 1", pantalla.linea(10))
        self.assertIn("Unidades simbólicas en total 3", pantalla.linea(9))
        self.assertIn("Historial: nacimientos 7   muertes 4", pantalla.linea(11))
        self.assertIn("Población actual 3 de 8 unidades", pantalla.linea(14))
        self.assertIn("ajuste agua sí", pantalla.linea(14))
        self.assertIn("Nacimientos 7   Muertes 4", pantalla.linea(15))
        self.assertIn("Linajes ajustados 1/2", pantalla.linea(15))
        self.assertIn("linajes registrados 2", pantalla.linea(12))
        self.assertIn("Rasgo 2 · Linaje 2 · Origen 1", pantalla.linea(16))
        self.assertIn("Variaciones 3", pantalla.linea(16))
        self.assertIn("Selección: favorecidas 1   descartadas 2",
                      pantalla.linea(17))
        self.assertIn("Especie 1", pantalla.linea(17))
        interfaz._procesar_tecla(pantalla, ord("5"))
        interfaz._dibujar(pantalla)
        self.assertIn("DIVERSIFICACIÓN", pantalla.linea(6))
        self.assertIn("Especies vivas 1", pantalla.linea(7))
        self.assertIn("Mundos con dos o más especies vivas 0", pantalla.linea(8))
        self.assertIn("Unidades por especie: 1:3", pantalla.linea(15))
        self.assertIn("1-5 Vistas", pantalla.linea(23))
        self.assertEqual(antes, planeta.a_dict())

        planeta.estado_agua_preclima = None
        interfaz.vista = 3
        interfaz._dibujar(pantalla)
        self.assertIn("Linajes ajustados sin regla", pantalla.linea(15))

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

    def test_vida_muestra_historial_tras_extincion(self):
        universo = Universe(seed=1)
        universo.planetas = [Planet(
            "Planeta-Prueba", 1, 1,
            alcanzo_primera_vida=True,
            nacimientos_unicelulares=7,
            muertes_unicelulares=7,
            variaciones_unicelulares=3,
            variantes_biologicas_favorecidas=1,
            variantes_biologicas_descartadas=2,
        )]
        interfaz = SimulationUI(Simulation(universo))
        interfaz.vista = 3
        pantalla = PantallaFalsa(24, 72)
        interfaz._dibujar(pantalla)
        self.assertIn("Mundos con población activa 0", pantalla.linea(8))
        self.assertIn("linajes 0", pantalla.linea(7))
        self.assertIn("Linajes ajustados sin regla", pantalla.linea(15))
        self.assertIn("Historial: nacimientos 7   muertes 7",
                      pantalla.linea(11))
        self.assertIn("Planeta-Prueba", pantalla.linea(13))
        self.assertIn("Población actual 0", pantalla.linea(14))
        self.assertIn("ajuste agua no", pantalla.linea(14))
        self.assertIn("Rasgo inactivo", pantalla.linea(16))
        self.assertIn("Linaje — · Origen —", pantalla.linea(16))
        self.assertIn("Variaciones 3", pantalla.linea(16))
        self.assertIn("Selección: favorecidas 1   descartadas 2",
                      pantalla.linea(17))

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

    def test_especies_se_cuentan_por_planeta_y_conservan_extintas(self):
        universo = Universe(seed=73)
        historia = {
            1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
            2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
            3: {"progenitor_id": 2, "rasgo": 1, "origen": "variacion"},
        }
        universo.planetas = [Planet(
            nombre, 1, 1, vida_activa=True, poblacion_unicelular=1,
            nacimientos_unicelulares=3, muertes_unicelulares=2,
            linajes_unicelulares_vivos=[3], rasgos_unicelulares_vivos=[1],
            rasgo_linea_unicelular=1, linaje_observado_id=3,
            historial_linajes_unicelulares=historia,
        ) for nombre in ("Uno", "Dos")]
        interfaz = SimulationUI(Simulation(universo))
        interfaz.vista = 3
        pantalla = PantallaFalsa(24, 72)
        interfaz._dibujar(pantalla)
        self.assertIn("Especies vivas 2", pantalla.linea(8))
        self.assertIn("Especies extintas 2", pantalla.linea(9))
        self.assertIn("Especies reg. 4", pantalla.linea(10))
        self.assertIn("Especie 3", pantalla.linea(17))
        for planeta in universo.planetas:
            planeta.vida_activa = False
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        interfaz._dibujar(pantalla)
        self.assertIn("Especies vivas 0", pantalla.linea(8))
        self.assertIn("Especies extintas 4", pantalla.linea(9))
        self.assertIn("Especie —", pantalla.linea(17))

    def test_diversificacion_muestra_coexistencia_y_rama(self):
        universo = Universe(seed=73)
        planeta = Planet(
            "Diverso", 1, 1, vida_activa=True, poblacion_unicelular=5,
            linajes_unicelulares_vivos=[2, 3, 3, 4, 5],
            rasgos_unicelulares_vivos=[0, 1, 1, 0, 2],
            linaje_observado_id=5, rasgo_linea_unicelular=2,
            historial_linajes_unicelulares={
                1: {"progenitor_id": None, "rasgo": 1, "origen": "fundacion"},
                2: {"progenitor_id": 1, "rasgo": 0, "origen": "variacion"},
                3: {"progenitor_id": 2, "rasgo": 1, "origen": "variacion"},
                4: {"progenitor_id": 3, "rasgo": 0, "origen": "variacion"},
                5: {"progenitor_id": 4, "rasgo": 2, "origen": "variacion"},
            },
        )
        universo.planetas = [planeta]
        interfaz = SimulationUI(Simulation(universo))
        interfaz.vista = 4
        pantalla = PantallaFalsa(24, 72)
        antes = planeta.a_dict()
        interfaz._dibujar(pantalla)
        self.assertIn("Especies vivas 3 · extintas 0", pantalla.linea(7))
        self.assertIn("Mundos con dos o más especies vivas 1", pantalla.linea(8))
        self.assertIn("Unidades por especie: 1:1  3:3  5:1", pantalla.linea(15))
        self.assertIn("Especie observada 5 · origen 3 · hijas 0", pantalla.linea(17))
        self.assertEqual(planeta.a_dict(), antes)

        planeta.vida_activa = False
        universo.actualizar_poblacion_unicelular()
        universo.actualizar_herencia_unicelular()
        interfaz._dibujar(pantalla)
        self.assertIn("Especies vivas 0 · extintas 3", pantalla.linea(7))
        self.assertIn("Sin unidades vivas; la historia permanece.",
                      pantalla.linea(15))
        self.assertIn("Rama observada: ninguna activa.", pantalla.linea(17))

    def test_terminal_alta_reserva_mas_espacio_para_eventos(self):
        interfaz = SimulationUI(Simulation(Universe(seed=1)))
        pantalla = PantallaFalsa(30, 100)
        interfaz._dibujar(pantalla)
        self.assertIn("EVENTOS RECIENTES", pantalla.linea(19))
        self.assertIn("Esc Menú", pantalla.linea(29))
        self.assertTrue(pantalla.linea(28).startswith("─"))


if __name__ == "__main__":
    unittest.main()
