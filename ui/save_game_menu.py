import curses

from ui.console_utils import (
    centrar,
    escribir_seguro,
    linea_horizontal,
)


class SaveGameMenu:
    MAX_NOMBRE = 40

    CARACTERES_INVALIDOS = '<>:"/\\|?*'

    def mostrar(
        self,
        stdscr,
        mensaje=None,
    ):
        nombre = ""

        stdscr.keypad(True)

        try:
            curses.curs_set(1)

        except curses.error:
            pass

        while True:
            stdscr.erase()

            alto, _ = stdscr.getmaxyx()

            centrar(
                stdscr,
                1,
                ".        *        .        +        .",
            )

            centrar(
                stdscr,
                2,
                "GUARDAR UNIVERSO",
                curses.A_BOLD,
            )

            linea_horizontal(
                stdscr,
                4,
            )

            escribir_seguro(
                stdscr,
                6,
                2,
                "Nombre de la partida:",
            )

            escribir_seguro(
                stdscr,
                8,
                2,
                f"> {nombre}_",
            )

            if mensaje:
                escribir_seguro(
                    stdscr,
                    10,
                    2,
                    mensaje,
                    curses.A_BOLD,
                )

            linea_horizontal(
                stdscr,
                alto - 2,
            )

            escribir_seguro(
                stdscr,
                alto - 1,
                2,
                "ENTER Guardar   ESC Cancelar",
            )

            stdscr.refresh()

            tecla = stdscr.getch()

            if tecla == 27:
                self._ocultar_cursor()
                return None

            if tecla in (
                curses.KEY_ENTER,
                10,
                13,
            ):
                self._ocultar_cursor()

                return nombre.strip()

            if tecla in (
                curses.KEY_BACKSPACE,
                127,
                8,
            ):
                nombre = nombre[:-1]

                continue

            if 32 <= tecla <= 126:
                caracter = chr(tecla)

                if len(nombre) < self.MAX_NOMBRE:
                    nombre += caracter

    def confirmar_sobrescritura(
        self,
        stdscr,
        nombre,
    ):
        opciones = [
            "Sí",
            "No",
        ]

        seleccion = 1

        self._ocultar_cursor()

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
                "PARTIDA YA EXISTE",
                curses.A_BOLD,
            )

            linea_horizontal(
                stdscr,
                4,
            )

            escribir_seguro(
                stdscr,
                6,
                2,
                (f"La partida " f"'{nombre}' ya existe."),
            )

            escribir_seguro(
                stdscr,
                7,
                2,
                "¿Quieres sobrescribirla?",
            )

            fila = 10

            for indice, opcion in enumerate(opciones):
                if indice == seleccion:
                    texto = f"> {opcion}"
                    atributo = curses.A_REVERSE

                else:
                    texto = f"  {opcion}"
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

            linea_horizontal(
                stdscr,
                alto - 2,
            )

            escribir_seguro(
                stdscr,
                alto - 1,
                2,
                ("↑ ↓ Seleccionar   " "ENTER Confirmar   " "ESC Cancelar"),
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
                return seleccion == 0

            elif tecla == 27:
                return None

    def guardar_partida(
        self,
        stdscr,
        save_manager,
    ):
        mensaje = None

        while True:
            nombre = self.mostrar(
                stdscr,
                mensaje=mensaje,
            )

            if nombre is None:
                return None

            valido, mensaje = self._validar_nombre(nombre)

            if not valido:
                continue

            if save_manager.existe_guardado(nombre):
                sobrescribir = self.confirmar_sobrescritura(
                    stdscr,
                    nombre,
                )

                if sobrescribir is None:
                    return None

                if not sobrescribir:
                    mensaje = None
                    continue

            return nombre

    def _validar_nombre(
        self,
        nombre,
    ):
        if not nombre:
            return (
                False,
                "El nombre no puede estar vacío.",
            )

        if nombre in (
            ".",
            "..",
        ):
            return (
                False,
                "Ese nombre no es válido.",
            )

        if any(caracter in self.CARACTERES_INVALIDOS for caracter in nombre):
            return (
                False,
                ("No uses estos caracteres: " f"{self.CARACTERES_INVALIDOS}"),
            )

        return True, None

    def _ocultar_cursor(self):
        try:
            curses.curs_set(0)

        except curses.error:
            pass
