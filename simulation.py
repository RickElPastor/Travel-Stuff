import curses
import time

from save_manager import SaveManager
from ui.save_game_menu import SaveGameMenu

class Simulation:
    def __init__(self, universe):
        self.universe = universe
        self.ultimo_tick = time.time()
        self.indice_velocidad = 1
        self.scroll_eventos = 0
        self.save_manager = SaveManager()
        self.save_game_menu = SaveGameMenu()

    def actualizar_tiempo(self):
        ahora = time.time()
        transcurrido = ahora - self.ultimo_tick
        self.ultimo_tick = ahora

        año_inicial = self.universe.time.anio

        ticks = self.universe.time.avanzar(transcurrido)

        for i in range(ticks):
            año = año_inicial + i + 1

            self.universe.event_manager.actualizar(año)

    #PENDIENTE: Restraso de ESC
    def ejecutar(self, stdscr):
        stdscr.nodelay(True)

        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        while True:
            tecla = stdscr.getch()

            eventos = self.universe.event_manager.obtener_eventos()
            max_scroll = max(0, len(eventos) - 5)
            
            inicio = max(0, len(eventos) - 5 - self.scroll_eventos)
            fin = len(eventos) - self.scroll_eventos

            eventos_visibles = eventos[inicio:fin]

            if tecla == curses.KEY_MOUSE:
                evento_mouse = curses.getmouse()

                if evento_mouse[4] == curses.BUTTON5_PRESSED:
                    if self.scroll_eventos < max_scroll:
                        self.scroll_eventos += 1

                elif evento_mouse[4] == curses.BUTTON4_PRESSED:
                    if self.scroll_eventos > 0:
                        self.scroll_eventos -= 1

            if tecla == 27:
                stdscr.nodelay(False)
                break

            self.actualizar_tiempo()

            time.sleep(0.1)

            stdscr.clear()

            stdscr.addstr("TRAVEL STUFF\n\n")
            stdscr.addstr("SIMULACION\n\n")

            stdscr.addstr(f"Semilla: {self.universe.seed}\n")
            stdscr.addstr(f"Edad universo: {self.universe.time.anio}\n")
            stdscr.addstr(f"Velocidad x{self.universe.time.velocidad}\n\n")

            stdscr.addstr("EVENTOS RECIENTES\n")

            for evento in eventos_visibles:
                stdscr.addstr(f"- {evento}\n")

            stdscr.addstr("\nPresione ESC para volver al menú")

            stdscr.refresh()

            if tecla == curses.KEY_UP:
                self.indice_velocidad = (
                    self.indice_velocidad + 1
                ) % len(self.universe.time.velocidades)

            elif tecla == curses.KEY_DOWN:
                self.indice_velocidad = (
                    self.indice_velocidad - 1
                ) % len(self.universe.time.velocidades)

            elif tecla in (ord("s"), ord("S")):
                stdscr.nodelay(False)

                nombre = self.save_game_menu.guardar_partida(
                    stdscr,
                    self.save_manager
                )

                self.save_manager.guardar(
                    self.universe,
                    nombre
                )

                self.ultimo_tick = time.time()
                stdscr.nodelay(True)

            self.universe.time.velocidad = (
                self.universe.time.velocidades[self.indice_velocidad]
            )
