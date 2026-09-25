import curses

from config import SUBTITULO, TITULO
from ui.console_utils import (
    centrar,
    escribir_seguro,
    linea_horizontal,
)


class Menu:
    def mostrar(
        self,
        stdscr,
        universo_existe,
    ):
        opciones = [
            "Iniciar simulación",
            "Configurar universo",
            "Cargar universo",
            "Salir",
        ]

        if universo_existe:
            opciones.insert(
                1,
                "Continuar universo",
            )

        seleccion = 0

        stdscr.keypad(True)

        try:
            curses.curs_set(0)

        except curses.error:
            pass

        while True:
            stdscr.erase()

            alto, ancho = stdscr.getmaxyx()

            if alto < 16 or ancho < 50:
                centrar(
                    stdscr,
                    2,
                    TITULO,
                    curses.A_BOLD,
                )

                centrar(
                    stdscr,
                    4,
                    "Amplía la ventana de la terminal para continuar.",
                )

                stdscr.refresh()
                stdscr.getch()

                continue

            centrar(
                stdscr,
                1,
                ".        *        .        +        .",
            )

            centrar(
                stdscr,
                2,
                TITULO,
                curses.A_BOLD,
            )

            centrar(
                stdscr,
                3,
                SUBTITULO,
            )

            centrar(
                stdscr,
                4,
                "*        .        *        .        +",
            )

            linea_horizontal(
                stdscr,
                6,
            )

            fila = 8

            for indice, opcion in enumerate(opciones):
                if indice == seleccion:
                    texto = f"> {opcion}"
                    atributo = curses.A_REVERSE

                else:
                    texto = f"  {opcion}"
                    atributo = 0

                x = max(
                    2,
                    (ancho - len(texto)) // 2,
                )

                escribir_seguro(
                    stdscr,
                    fila,
                    x,
                    texto,
                    atributo,
                )

                fila += 1

            escribir_seguro(
                stdscr,
                alto - 2,
                2,
                "↑ ↓ Mover   ENTER Seleccionar",
            )

            stdscr.refresh()

            tecla = stdscr.getch()

            if tecla == curses.KEY_UP:
                seleccion = max(
                    0,
                    seleccion - 1,
                )

            elif tecla == curses.KEY_DOWN:
                seleccion = min(
                    len(opciones) - 1,
                    seleccion + 1,
                )

            elif tecla in (
                curses.KEY_ENTER,
                10,
                13,
            ):
                return opciones[seleccion]
