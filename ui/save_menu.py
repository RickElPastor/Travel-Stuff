import curses

class SaveMenu:
    def mostrar(self, stdscr, partidas):
        seleccion = 0

        while True:
            stdscr.clear()

            stdscr.addstr("╔══════════════════════════════════╗\n")
            stdscr.addstr("║       PARTIDAS GUARDADAS         ║\n")
            stdscr.addstr("╚══════════════════════════════════╝\n\n")

            for indice, partida in enumerate(partidas):
                if indice == seleccion:
                    stdscr.addstr(f"> {partida}\n")
                else:
                    stdscr.addstr(f"  {partida}\n")

            stdscr.addstr("\n↑ ↓ Seleccionar\n")
            stdscr.addstr("Enter Cargar\n")
            stdscr.addstr("ESC Volver")

            stdscr.refresh()

            tecla = stdscr.getch()

            if tecla == curses.KEY_UP:
                seleccion = (seleccion - 1) % len(partidas)
            elif tecla == curses.KEY_DOWN:
                seleccion = (seleccion + 1) % len(partidas)
            elif tecla == 10:
                return partidas[seleccion]
            elif tecla == 27:
                return None
