import curses


class SaveGameMenu:
    def mostrar(self, stdscr):
        stdscr.clear()

        stdscr.addstr("╔══════════════════════════════════╗\n")
        stdscr.addstr("║        GUARDAR UNIVERSO          ║\n")
        stdscr.addstr("╚══════════════════════════════════╝\n\n")

        stdscr.addstr("Nombre de la partida:\n")
        stdscr.addstr("> ")

        stdscr.refresh()

        curses.echo()
        nombre = stdscr.getstr().decode("utf-8")
        curses.noecho()

        return nombre

    def confirmar_sobrescritura(self, stdscr, nombre):
        seleccion = 0
        opciones = ["Sí", "No"]

        while True:
            stdscr.clear()

            stdscr.addstr("╔══════════════════════════════════╗\n")
            stdscr.addstr("║       PARTIDA YA EXISTE          ║\n")
            stdscr.addstr("╚══════════════════════════════════╝\n\n")

            stdscr.addstr(f"La partida '{nombre}' ya existe.\n")
            stdscr.addstr("¿Quieres sobrescribirla?\n\n")

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
                return seleccion == 0

            elif tecla == 27:
                return False

    def guardar_partida(self, stdscr, save_manager):
        while True:
            nombre = self.mostrar(stdscr)

            if save_manager.existe_guardado(nombre):
                sobrescribir = self.confirmar_sobrescritura(stdscr, nombre)

                if not sobrescribir:
                    continue

            return nombre



