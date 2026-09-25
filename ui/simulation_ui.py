import curses
import time

from save_manager import SaveManager

from ui.console_utils import centrar, escribir_seguro, linea_horizontal

from ui.save_game_menu import SaveGameMenu


class SimulationUI:
    REFRESCO_SEGUNDOS = 0.01

    def __init__(self, simulation):
        self.simulation = simulation

        self.universe = simulation.universe

        self.scroll_eventos = 0

        self.save_manager = SaveManager()

        self.save_game_menu = SaveGameMenu()

    def ejecutar(self, stdscr):
        stdscr.nodelay(True)
        stdscr.keypad(True)

        try:
            curses.curs_set(0)

        except curses.error:
            pass

        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        while True:
            tecla = stdscr.getch()

            if tecla == 27:
                stdscr.nodelay(False)
                return

            self._procesar_tecla(stdscr, tecla)

            self.simulation.actualizar()

            self._dibujar(stdscr)

            time.sleep(self.REFRESCO_SEGUNDOS)

    def _procesar_tecla(self, stdscr, tecla):
        if tecla == curses.KEY_UP:
            self.simulation.subir_velocidad()

        elif tecla == curses.KEY_DOWN:
            self.simulation.bajar_velocidad()

        elif tecla == curses.KEY_PPAGE:
            self._subir_eventos()

        elif tecla == curses.KEY_NPAGE:
            self._bajar_eventos()

        elif tecla == curses.KEY_MOUSE:
            self._procesar_mouse()

        elif tecla in (ord("s"), ord("S")):
            self._guardar(stdscr)

    def _procesar_mouse(self):
        try:
            evento_mouse = curses.getmouse()

        except curses.error:
            return

        estado = evento_mouse[4]

        if estado & curses.BUTTON4_PRESSED:
            self._subir_eventos()

        elif estado & curses.BUTTON5_PRESSED:
            self._bajar_eventos()

    def _subir_eventos(self):
        eventos = self.universe.event_manager.obtener_eventos()

        max_scroll = max(0, len(eventos) - 1)

        self.scroll_eventos = min(self.scroll_eventos + 1, max_scroll)

    def _bajar_eventos(self):
        self.scroll_eventos = max(0, self.scroll_eventos - 1)

    def _guardar(self, stdscr):
        stdscr.nodelay(False)

        nombre = self.save_game_menu.guardar_partida(stdscr, self.save_manager)

        if nombre:
            self.save_manager.guardar(self.universe, nombre)

        self.simulation.reiniciar_reloj()

        stdscr.nodelay(True)

    def _dibujar(self, stdscr):
        stdscr.erase()

        alto, ancho = stdscr.getmaxyx()

        if alto < 24 or ancho < 72:
            centrar(stdscr, 2, "TRAVEL STUFF")

            centrar(stdscr, 4, ("La terminal es " "demasiado pequeña."))

            centrar(stdscr, 5, ("Usa al menos " "72 columnas x 24 filas."))

            stdscr.refresh()
            return

        fila = 0

        fila = self._dibujar_cabecera(stdscr, fila)

        fila = self._dibujar_universo(stdscr, fila)

        fila = self._dibujar_estrellas(stdscr, fila)

        fila = self._dibujar_remanentes(stdscr, fila)

        self._dibujar_eventos(stdscr, fila, alto)

        controles = (
            "ESC Menu | " "S Guardar | " "UP/DOWN Velocidad | " "PgUp/PgDn Eventos"
        )

        linea_horizontal(stdscr, alto - 2)

        escribir_seguro(stdscr, alto - 1, 0, controles)

        stdscr.refresh()

    def _dibujar_cabecera(self, stdscr, fila):
        centrar(stdscr, fila, (".       *        .        " "+        ."))

        fila += 1

        centrar(
            stdscr,
            fila,
            ("*       TRAVEL STUFF - " "SIMULACION       *"),
            curses.A_BOLD,
        )

        fila += 1

        centrar(stdscr, fila, (".    +       .        " "*        ."))

        fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_universo(self, stdscr, fila):
        escribir_seguro(stdscr, fila, 0, "UNIVERSO", curses.A_BOLD)

        fila += 1

        edad = self._numero_entero(self.universe.time.anio)

        velocidad = self.universe.time.obtener_descripcion_velocidad()

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                f"Semilla: "
                f"{self.universe.seed}  |  "
                f"Edad: {edad} años  |  "
                f"Velocidad: {velocidad}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Estrellas activas: "
                f"{len(self.universe.estrellas)}"
                "  |  "
                "Remanentes: "
                f"{len(self.universe.remanentes)}"
            ),
        )

        fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_estrellas(self, stdscr, fila):
        escribir_seguro(stdscr, fila, 0, "ESTRELLAS", curses.A_BOLD)

        fila += 1

        if not self.universe.estrellas:
            escribir_seguro(stdscr, fila, 2, "No hay estrellas activas.")

            fila += 1

        else:
            for estrella in self.universe.estrellas[:4]:
                temperatura = self._valor(estrella.temperatura_efectiva, "K", 0)

                masa = self._valor(estrella.masa_actual, "Msol", 3)

                escribir_seguro(
                    stdscr,
                    fila,
                    2,
                    (
                        f"* {estrella.nombre} | "
                        f"{estrella.obtener_etapa_visible()} | "
                        f"{masa} | "
                        f"{temperatura}"
                    ),
                )

                fila += 1

            restantes = len(self.universe.estrellas) - 4

            if restantes > 0:
                escribir_seguro(
                    stdscr, fila, 4, (f"... y {restantes} " "estrellas mas.")
                )

                fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_remanentes(self, stdscr, fila):
        escribir_seguro(stdscr, fila, 0, "REMANENTES", curses.A_BOLD)

        fila += 1

        if not self.universe.remanentes:
            escribir_seguro(stdscr, fila, 2, ("No hay remanentes " "estelares."))

            fila += 1

        else:
            for remanente in self.universe.remanentes[-3:]:
                escribir_seguro(
                    stdscr,
                    fila,
                    2,
                    (
                        f"+ {remanente.nombre} | "
                        f"{remanente.obtener_tipo_visible()} | "
                        f"{remanente.masa:.3f} "
                        "Msol"
                    ),
                )

                fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_eventos(self, stdscr, fila, alto):
        escribir_seguro(stdscr, fila, 0, "EVENTOS", curses.A_BOLD)

        fila += 1

        espacio = max(1, alto - fila - 3)

        eventos = self.universe.event_manager.obtener_eventos()

        fin = max(0, len(eventos) - self.scroll_eventos)

        inicio = max(0, fin - espacio)

        visibles = eventos[inicio:fin]

        if not visibles:
            escribir_seguro(stdscr, fila, 2, "Todavia no hay eventos.")

            return

        for evento in visibles:
            escribir_seguro(stdscr, fila, 2, f"- {evento}")

            fila += 1

    def _numero_entero(self, valor):
        return f"{valor:,.0f}".replace(",", " ")

    def _valor(self, valor, unidad="", decimales=2):
        if valor is None:
            return "sin datos"

        texto = f"{valor:.{decimales}f}"

        if unidad:
            texto += f" {unidad}"

        return texto
