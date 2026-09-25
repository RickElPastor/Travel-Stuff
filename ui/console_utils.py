import curses


def escribir_seguro(stdscr, y, x, texto, atributo=0):
    alto, ancho = stdscr.getmaxyx()

    if y < 0 or y >= alto:
        return

    if x < 0 or x >= ancho:
        return

    espacio = ancho - x - 1

    if espacio <= 0:
        return

    try:
        stdscr.addnstr(y, x, str(texto), espacio, atributo)

    except curses.error:
        pass


def linea_horizontal(stdscr, y, caracter="-"):
    _, ancho = stdscr.getmaxyx()

    escribir_seguro(stdscr, y, 0, caracter * max(1, ancho - 1))


def centrar(stdscr, y, texto, atributo=0):
    _, ancho = stdscr.getmaxyx()

    x = max(0, (ancho - len(texto)) // 2)

    escribir_seguro(stdscr, y, x, texto, atributo)
