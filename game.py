import curses

from hybrid_stellar_model import ModeloEstelarHibrido
from popiii_hassan_model import ModeloHassanPopIII
from save_manager import SaveManager
from sevn_model import ModeloSEVN
from simulation import Simulation
from ui.info_screen import InfoScreen
from ui.menu import Menu
from ui.save_menu import SaveMenu
from ui.simulation_ui import SimulationUI
from universe import Universe


class Game:
    def __init__(self):
        self.menu = Menu()

        self.save_manager = SaveManager()
        self.save_menu = SaveMenu()
        self.info_screen = InfoScreen()

        self.universe = None

        modelo_popiii = ModeloHassanPopIII()

        modelo_sevn = ModeloSEVN(
            modelo_supernova="rapid",
        )

        self.modelo_estelar = ModeloEstelarHibrido(
            modelo_popiii=modelo_popiii,
            modelo_sevn=modelo_sevn,
        )

    def ejecutar(
        self,
        stdscr,
    ):
        while True:
            accion = self.menu.mostrar(
                stdscr,
                universo_existe=(self.universe is not None),
            )

            if accion == "Iniciar simulación":
                self._iniciar_nuevo_universo(stdscr)

            elif accion == "Continuar universo":
                self._continuar_universo(stdscr)

            elif accion == "Configurar universo":
                self._mostrar_configuracion(stdscr)

            elif accion == "Cargar universo":
                self._cargar_universo(stdscr)

            elif accion == "Salir":
                return

    def _iniciar_nuevo_universo(
        self,
        stdscr,
    ):
        self.universe = Universe(
            modelo_estelar=(self.modelo_estelar),
        )

        self._abrir_simulacion(stdscr)

    def _continuar_universo(
        self,
        stdscr,
    ):
        if self.universe is None:
            self.info_screen.mostrar(
                stdscr,
                "SIN UNIVERSO ACTIVO",
                [
                    "No hay un universo en memoria.",
                    "Inicia o carga uno primero.",
                ],
            )

            return

        self._abrir_simulacion(stdscr)

    def _cargar_universo(
        self,
        stdscr,
    ):
        partidas = self.save_manager.listar_guardados()

        if not partidas:
            self.info_screen.mostrar(
                stdscr,
                "PARTIDAS GUARDADAS",
                [
                    "No hay universos guardados.",
                ],
            )

            return

        partida = self.save_menu.mostrar(
            stdscr,
            partidas,
        )

        if partida is None:
            return

        try:
            universo = self.save_manager.cargar(
                partida,
                modelo_estelar=(self.modelo_estelar),
            )

        except (
            OSError,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            self.info_screen.mostrar(
                stdscr,
                "NO SE PUDO CARGAR",
                [
                    f"Archivo: {partida}",
                    "",
                    str(error),
                ],
            )

            return

        self.universe = universo

        self._abrir_simulacion(stdscr)

    def _mostrar_configuracion(
        self,
        stdscr,
    ):
        self.info_screen.mostrar(
            stdscr,
            "CONFIGURAR UNIVERSO",
            [
                ("Formación estelar " "cosmológica activa."),
                "",
                ("Evolución estelar: " "SEVN híbrido."),
                "",
                ("Modelo principal: " "PARSEC."),
                ("Baja masa: " "MIST v2.5."),
                ("MIST: modelos " "no rotantes, " "[alpha/Fe]=0.0."),
                "",
                ("Población III Z=0: " "pendiente."),
                ("Masas menores al " "dominio MIST: " "pendientes."),
                "",
                ("No se extrapolan " "estrellas fuera del " "dominio científico."),
            ],
        )

    def _abrir_simulacion(
        self,
        stdscr,
    ):
        if self.universe is None:
            return

        simulacion = Simulation(self.universe)

        interfaz = SimulationUI(simulacion)

        interfaz.ejecutar(stdscr)

    def run(self):
        try:
            curses.wrapper(self.ejecutar)

        finally:
            self.modelo_estelar.cerrar()
