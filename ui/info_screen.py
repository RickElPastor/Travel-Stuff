import curses

from ui.console_utils import (
    centrar,
    escribir_seguro,
    linea_horizontal,
)


class InfoScreen:
    def mostrar(
        self,
        stdscr,
        titulo,
        lineas,
    ):
        stdscr.erase()
        stdscr.keypad(True)

        try:
            curses.curs_set(0)

        except curses.error:
            pass

        alto, _ = stdscr.getmaxyx()

        centrar(
            stdscr,
            1,
            ".        *        .        +        .",
        )

        centrar(
            stdscr,
            2,
            titulo,
            curses.A_BOLD,
        )

        linea_horizontal(
            stdscr,
            4,
        )

        fila = 6

        for linea in lineas:
            if fila >= alto - 3:
                break

            escribir_seguro(
                stdscr,
                fila,
                2,
                linea,
            )

            fila += 1

        linea_horizontal(
            stdscr,
            alto - 3,
        )

        escribir_seguro(
            stdscr,
            alto - 2,
            2,
            "ENTER o ESC para volver",
        )

        stdscr.refresh()

        while True:
            tecla = stdscr.getch()

            if tecla in (
                27,
                curses.KEY_ENTER,
                10,
                13,
            ):
                return
