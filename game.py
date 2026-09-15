import curses

from ui.menu import Menu
from universe import Universe
from simulation import Simulation
from save_manager import SaveManager
from ui.save_menu import SaveMenu


class Game:
    def __init__(self):
        self.menu = Menu()
        self.universe = None
        self.save_manager = SaveManager()
        self.save_menu = SaveMenu()

    def ejecutar(self, stdscr):
        while True:
            universo_existe = self.universe is not None

            seleccion = self.menu.mostrar(stdscr, universo_existe)

            if universo_existe:
                if seleccion == 0:
                    self.universe = Universe()
                    simulation = Simulation(self.universe)
                    simulation.ejecutar(stdscr)
                elif seleccion == 1:
                    simulation = Simulation(self.universe)
                    simulation.ejecutar(stdscr)
                elif seleccion == 3:
                    partidas = self.save_manager.listar_guardados()

                    if partidas:
                        partida = self.save_menu.mostrar(stdscr, partidas)

                        if partida is not None:
                            self.universe = self.save_manager.cargar(partida)

                            simulation = Simulation(self.universe)
                            simulation.ejecutar(stdscr)
                elif seleccion == 4:
                    break

            else:
                if seleccion == 0:
                    self.universe = Universe()
                    simulation = Simulation(self.universe)
                    simulation.ejecutar(stdscr)
                elif seleccion == 2:
                    partidas = self.save_manager.listar_guardados()

                    if partidas:
                        partida = self.save_menu.mostrar(stdscr, partidas)

                        if partida is not None:
                            self.universe = self.save_manager.cargar(partida)

                            simulation = Simulation(self.universe)
                            simulation.ejecutar(stdscr)
                elif seleccion == 3:
                    break
    
    def run(self):
        curses.wrapper(self.ejecutar)
