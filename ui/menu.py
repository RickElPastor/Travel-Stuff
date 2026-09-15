import curses

from config import TITULO, SUBTITULO


class Menu:
    def mostrar(self, stdscr, universo_existe):
        opciones = [
            "Iniciar simulación",
            "Configurar universo",
            "Cargar universo",
            "Salir",
        ]

        if universo_existe:
            opciones.insert(1, "Continuar universo")

        seleccion = 0

        while True:
            stdscr.clear()

            stdscr.addstr("╔══════════════════════════════════╗\n")
            stdscr.addstr(f"║          {TITULO}            ║\n")
            stdscr.addstr(f"║      {SUBTITULO}     ║\n")
            stdscr.addstr("╚══════════════════════════════════╝\n\n")

            for indice, opcion in enumerate(opciones):
                if indice == seleccion:
                    stdscr.addstr(f"> {opcion}\n")
                else:
                    stdscr.addstr(f"  {opcion}\n")

            stdscr.refresh()

            tecla = stdscr.getch()

            if tecla == curses.KEY_UP:
                seleccion = (seleccion - 1) % len(opciones)

            elif tecla == curses.KEY_DOWN:
                seleccion = (seleccion + 1) % len(opciones)

            elif tecla == 10:
                return seleccion
