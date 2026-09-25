import curses

from ui.console_utils import (
    centrar,
    escribir_seguro,
    linea_horizontal,
)


class SaveMenu:
    def mostrar(
        self,
        stdscr,
        partidas,
    ):
        partidas = sorted(partidas)

        seleccion = 0

        stdscr.keypad(True)

        try:
            curses.curs_set(0)

        except curses.error:
            pass

        while True:
            stdscr.erase()

            alto, ancho = stdscr.getmaxyx()

            centrar(
                stdscr,
                1,
                ".        *        .        +        .",
            )

            centrar(
                stdscr,
                2,
                "PARTIDAS GUARDADAS",
                curses.A_BOLD,
            )

            linea_horizontal(
                stdscr,
                4,
            )

            if not partidas:
                centrar(
                    stdscr,
                    7,
                    "No hay universos guardados.",
                )

                escribir_seguro(
                    stdscr,
                    alto - 2,
                    2,
                    "ESC Volver",
                )

                stdscr.refresh()

                if stdscr.getch() == 27:
                    return None

                continue

            filas_disponibles = max(
                1,
                alto - 10,
            )

            inicio = max(
                0,
                min(
                    seleccion - filas_disponibles + 1,
                    len(partidas) - filas_disponibles,
                ),
            )

            fin = min(
                len(partidas),
                inicio + filas_disponibles,
            )

            fila = 6

            for indice in range(
                inicio,
                fin,
            ):
                partida = partidas[indice]

                if indice == seleccion:
                    texto = f"> {partida}"
                    atributo = curses.A_REVERSE

                else:
                    texto = f"  {partida}"
                    atributo = 0

                escribir_seguro(
                    stdscr,
                    fila,
                    max(
                        2,
                        (ancho - len(texto)) // 2,
                    ),
                    texto,
                    atributo,
                )

                fila += 1

            escribir_seguro(
                stdscr,
                alto - 3,
                2,
                (f"Guardado " f"{seleccion + 1} " f"de {len(partidas)}"),
            )

            linea_horizontal(
                stdscr,
                alto - 2,
            )

            escribir_seguro(
                stdscr,
                alto - 1,
                2,
                ("ESC Volver   " "↑ ↓ Seleccionar   " "ENTER Cargar"),
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
                    len(partidas) - 1,
                    seleccion + 1,
                )

            elif tecla in (
                curses.KEY_ENTER,
                10,
                13,
            ):
                return partidas[seleccion]

            elif tecla == 27:
                return None
