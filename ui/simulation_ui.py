import curses
import time

from save_manager import SaveManager
from ui.console_utils import centrar, escribir_seguro
from ui.save_game_menu import SaveGameMenu


class SimulationUI:
    REFRESCO_SEGUNDOS = 0.01
    VISTAS = ("Abiogénesis", "Universo", "Condiciones", "Vida")

    def __init__(self, simulation):
        self.simulation = simulation
        self.universe = simulation.universe
        self.scroll_eventos = 0
        self.vista = 0
        self.save_manager = SaveManager()
        self.save_game_menu = SaveGameMenu()

    def ejecutar(self, stdscr):
        stdscr.nodelay(True)
        stdscr.keypad(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        try:
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_CYAN, -1)
                curses.init_pair(2, curses.COLOR_GREEN, -1)
                curses.init_pair(3, curses.COLOR_YELLOW, -1)
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
        elif tecla in (ord("1"), ord("2"), ord("3"), ord("4")):
            self.vista = tecla - ord("1")

    def _procesar_mouse(self):
        try:
            estado = curses.getmouse()[4]
        except curses.error:
            return
        if estado & curses.BUTTON4_PRESSED:
            self._subir_eventos()
        elif estado & curses.BUTTON5_PRESSED:
            self._bajar_eventos()

    def _subir_eventos(self):
        eventos = self.universe.event_manager.obtener_eventos()
        self.scroll_eventos = min(self.scroll_eventos + 1, max(0, len(eventos) - 1))

    def _bajar_eventos(self):
        self.scroll_eventos = max(0, self.scroll_eventos - 1)

    def _guardar(self, stdscr):
        stdscr.nodelay(False)
        nombre = self.save_game_menu.guardar_partida(stdscr, self.save_manager)
        if nombre:
            self.save_manager.guardar(self.universe, nombre)
        self.simulation.reiniciar_reloj()
        stdscr.nodelay(True)

    def _color(self, numero):
        try:
            return curses.color_pair(numero) if curses.has_colors() else 0
        except curses.error:
            return 0

    def _separador(self, stdscr, fila):
        _, ancho = stdscr.getmaxyx()
        escribir_seguro(stdscr, fila, 0, "─" * (ancho - 1), self._color(1))

    def _texto(self, stdscr, fila, texto, atributo=0):
        escribir_seguro(stdscr, fila, 2, texto, atributo)

    def _dibujar(self, stdscr):
        stdscr.erase()
        alto, ancho = stdscr.getmaxyx()
        if alto < 24 or ancho < 72:
            centrar(stdscr, 2, "TRAVEL STUFF")
            centrar(stdscr, 4, "Amplía la terminal a 72 columnas x 24 filas.")
            stdscr.refresh()
            return

        self._separador(stdscr, 0)
        self._texto(stdscr, 1, "TRAVEL STUFF  /  SIMULADOR DE UNIVERSOS",
                    curses.A_BOLD | self._color(1))
        edad = f"{self.universe.time.anio:,}".replace(",", " ")
        self._texto(
            stdscr, 2,
            f"Año {edad}   ·   Semilla {self.universe.seed}   ·   "
            f"{self.universe.time.obtener_descripcion_velocidad()}",
        )
        self._separador(stdscr, 3)
        x = 2
        for indice, nombre in enumerate(self.VISTAS):
            etiqueta = f" {indice + 1} {nombre} "
            atributo = (curses.A_BOLD | self._color(1)) if indice == self.vista else 0
            escribir_seguro(stdscr, 4, x, etiqueta, atributo)
            x += len(etiqueta) + 2
        self._separador(stdscr, 5)

        if self.vista == 0:
            self._dibujar_abiogenesis(stdscr)
        elif self.vista == 1:
            self._dibujar_universo(stdscr)
        elif self.vista == 2:
            self._dibujar_condiciones(stdscr)
        else:
            self._dibujar_vida(stdscr)

        self._dibujar_eventos(stdscr, alto)
        self._separador(stdscr, alto - 2)
        self._texto(
            stdscr, alto - 1,
            "1-4 Vistas · ↑↓ Vel. · S Guardar · PgUp/PgDn Eventos · Esc Menú",
        )
        stdscr.refresh()

    def _encabezado(self, stdscr, fila, texto):
        self._texto(stdscr, fila, texto, curses.A_BOLD | self._color(1))

    def _dibujar_abiogenesis(self, stdscr):
        conteos = {
            "entorno": 0, "organicos": 0, "concentracion": 0,
            "precursores": 0, "polimeros": 0, "redes": 0,
            "compartimentos": 0, "protocelulas": 0,
            "normal": 0, "extra": 0, "rep_hist": 0, "rep_activa": 0,
            "herencia": 0, "variacion": 0, "seleccion": 0,
            "favorecidas": 0, "descartadas": 0,
            "vida_activa": 0, "vida_historica": 0,
        }
        foco = None
        for planeta in self.universe.planetas:
            conteos["entorno"] += bool(planeta.tuvo_entorno_prebiotico)
            conteos["organicos"] += bool(planeta.alcanzo_organicos_simples)
            conteos["concentracion"] += bool(planeta.alcanzo_concentracion_prebiotica)
            conteos["precursores"] += bool(planeta.alcanzo_precursores_complejos)
            conteos["polimeros"] += bool(planeta.alcanzo_polimerizacion_prebiotica)
            conteos["redes"] += bool(planeta.alcanzo_red_quimica_primitiva)
            conteos["compartimentos"] += bool(planeta.alcanzo_compartimentalizacion_prebiotica)
            conteos["protocelulas"] += bool(planeta.alcanzo_protocelula)
            conteos["normal"] += bool(planeta.protocelula_viable_normal)
            conteos["extra"] += bool(
                planeta.protocelula_viable and not planeta.protocelula_viable_normal
            )
            conteos["rep_hist"] += bool(planeta.alcanzo_replicacion_prebiotica)
            conteos["rep_activa"] += bool(planeta.replicacion_prebiotica_activa)
            conteos["herencia"] += planeta.copias_heredables > 0
            conteos["variacion"] += planeta.variaciones_prebioticas > 0
            conteos["seleccion"] += (
                planeta.variantes_favorecidas + planeta.variantes_descartadas > 0
            )
            conteos["favorecidas"] += planeta.variantes_favorecidas
            conteos["descartadas"] += planeta.variantes_descartadas
            conteos["vida_activa"] += bool(planeta.vida_activa)
            conteos["vida_historica"] += bool(planeta.alcanzo_primera_vida)
            if planeta.alcanzo_protocelula and (
                foco is None
                or (planeta.vida_activa,
                    planeta.replicacion_prebiotica_activa,
                    planeta.copias_heredables)
                > (foco.vida_activa,
                   foco.replicacion_prebiotica_activa,
                   foco.copias_heredables)
            ):
                foco = planeta

        c = conteos
        self._encabezado(stdscr, 6, "01  QUÍMICA PREBIÓTICA  ·  logros históricos")
        self._texto(stdscr, 7, f"Entorno {c['entorno']}   →   Orgánicos {c['organicos']}"
                    f"   →   Concentración {c['concentracion']}")
        self._texto(stdscr, 8, f"Precursores {c['precursores']}   →   "
                    f"Polímeros {c['polimeros']}   →   Redes {c['redes']}")
        self._texto(stdscr, 9, f"Compartimentos {c['compartimentos']}   →   "
                    f"Protocélulas {c['protocelulas']}")
        self._encabezado(stdscr, 11, "02  ABIOGÉNESIS  ·  condiciones actuales e historia")
        self._texto(stdscr, 12, f"Viabilidad ahora   normal {c['normal']}   "
                    f"extraordinaria {c['extra']}", self._color(2))
        self._texto(stdscr, 13, f"Replicación        activa {c['rep_activa']}   "
                    f"histórica {c['rep_hist']}")
        self._texto(stdscr, 14, f"Mundos con herencia {c['herencia']}   ·   "
                    f"con variación {c['variacion']}")
        self._texto(stdscr, 15, f"Mundos con selección {c['seleccion']}   ·   "
                    f"favorecidas {c['favorecidas']}   descartadas {c['descartadas']}")
        self._texto(stdscr, 16,
                    f"PRIMERA VIDA   activa {c['vida_activa']}   "
                    f"histórica {c['vida_historica']}",
                    curses.A_BOLD | self._color(2))
        if foco is None:
            self._texto(stdscr, 17, "Línea actual: aún sin protocélulas.",
                        self._color(3))
        elif foco.patron_copia is None:
            self._texto(stdscr, 17,
                        f"Línea inactiva · {foco.copias_heredables} copias "
                        f"históricas · {foco.nombre}", self._color(3))
        else:
            self._texto(stdscr, 17,
                        f"Línea activa · patrón {foco.patron_copia} · "
                        f"{foco.copias_linea} copias · {foco.nombre}",
                        self._color(3))

    def _dibujar_universo(self, stdscr):
        sistemas = self.universe.sistemas_estelares
        discos = self.universe.discos_protoplanetarios
        planetas = self.universe.planetas
        tipos = {"normal": 0, "arcano": 0, "anomalia_fisica": 0,
                 "energia_exotica": 0}
        gigantes = 0
        for planeta in planetas:
            if planeta.regimen_mundo == "normal":
                tipos["normal"] += 1
            elif planeta.tipo_regla_extraordinaria in tipos:
                tipos[planeta.tipo_regla_extraordinaria] += 1
            gigantes += bool(planeta.entro_runaway)

        self._encabezado(stdscr, 6, "01  ESTRUCTURA DEL UNIVERSO")
        self._texto(stdscr, 7, f"Estrellas activas {len(self.universe.estrellas)}   "
                    f"Remanentes {len(self.universe.remanentes)}")
        self._texto(stdscr, 8, f"Sistemas estelares {len(sistemas)}   "
                    f"Discos {len(discos)}")
        self._encabezado(stdscr, 10, "02  FORMACIÓN PLANETARIA")
        self._texto(stdscr, 11, f"Embriones {sum(d.obtener_cantidad_embriones() for d in discos)}"
                    f"   Protoplanetas {sum(d.obtener_cantidad_protoplanetas() for d in discos)}")
        self._texto(stdscr, 12, f"Planetas {len(planetas)}   Gigantes runaway {gigantes}")
        self._encabezado(stdscr, 14, "03  REGLAS DE LOS MUNDOS")
        self._texto(stdscr, 15, f"Normales {tipos['normal']}   "
                    f"Extraordinarios {sum(tipos.values()) - tipos['normal']}")
        self._texto(stdscr, 16, f"Arcanos {tipos['arcano']}   "
                    f"Anomalías {tipos['anomalia_fisica']}   "
                    f"Energía exótica {tipos['energia_exotica']}")

    def _dibujar_condiciones(self, stdscr):
        planetas = self.universe.planetas
        hz = ter = ret = atm = agua = hab = quim = 0
        temperados = glaciados = 0
        for p in planetas:
            hz += bool(p.en_zona_habitable_radiativa)
            ter += bool(p.candidato_terrestre_hz)
            ret += bool(p.retencion_atmosferica_aprox)
            atm += bool(p.tiene_atmosfera_secundaria)
            agua += bool(p.tiene_agua_condensada)
            hab += bool(p.candidato_habitable_fase1)
            quim += bool(p.candidato_quimica_prebiotica)
            temperados += p.estado_habitabilidad_fase1 == "candidato_temperado"
            glaciados += p.estado_habitabilidad_fase1 == "candidato_glaciado"

        self._encabezado(stdscr, 6, "01  HABITABILIDAD  ·  condiciones actuales")
        self._texto(stdscr, 7, f"Zona habitable {hz}   →   Terrestres {ter}"
                    f"   →   Retención {ret}")
        self._texto(stdscr, 8, f"Atmósfera secundaria {atm}   Agua condensada {agua}")
        self._texto(stdscr, 9, f"Habitables ahora {hab}   "
                    f"(templados {temperados}, glaciados {glaciados})",
                    self._color(2))
        self._encabezado(stdscr, 11, "02  ENTORNO QUÍMICO ACTUAL")
        self._texto(stdscr, 12, f"Candidatos químicos {quim}")
        self._texto(stdscr, 13, "Los logros históricos se muestran en Abiogénesis.")
        self._texto(stdscr, 15, "Una condición puede desaparecer al cambiar la estrella")
        self._texto(stdscr, 16, "o la atmósfera; los logros históricos permanecen.")

    def _dibujar_vida(self, stdscr):
        planetas = self.universe.planetas
        activos = [p for p in planetas if p.poblacion_unicelular > 0]
        historicos = sum(bool(p.alcanzo_primera_vida) for p in planetas)
        unidades = sum(p.poblacion_unicelular for p in activos)

        self._encabezado(stdscr, 6, "01  VIDA UNICELULAR  ·  fase 2")
        self._texto(stdscr, 8, f"Mundos con población activa {len(activos)}")
        self._texto(stdscr, 9, f"Unidades simbólicas en total {unidades}",
                    self._color(2))
        self._texto(stdscr, 10, f"Mundos que alcanzaron primera vida {historicos}")
        self._encabezado(stdscr, 12, "02  MUNDO OBSERVADO")
        if activos:
            foco = max(activos, key=lambda p: p.poblacion_unicelular)
            capacidad = self.universe.modelo_poblacion_unicelular.CAPACIDAD_INICIAL
            self._texto(stdscr, 13, foco.nombre)
            self._texto(stdscr, 14,
                        f"Población actual {foco.poblacion_unicelular} "
                        f"de {capacidad} unidades")
            self._texto(stdscr, 15, f"Patrón heredable {foco.patron_copia}")
        else:
            self._texto(stdscr, 13, "Aún no hay población activa.")
        self._texto(stdscr, 17, "Las unidades son una escala del modelo, no individuos.",
                    self._color(3))

    def _dibujar_eventos(self, stdscr, alto):
        fila = 18
        self._separador(stdscr, fila)
        self._encabezado(stdscr, fila + 1, "EVENTOS RECIENTES  ·  PgUp/PgDn")
        eventos = self.universe.event_manager.obtener_eventos()
        espacio = alto - fila - 4
        fin = max(0, len(eventos) - self.scroll_eventos)
        visibles = eventos[max(0, fin - espacio):fin]
        if not visibles:
            self._texto(stdscr, fila + 2, "Aún no hay eventos.")
        else:
            for desplazamiento, evento in enumerate(visibles):
                self._texto(stdscr, fila + 2 + desplazamiento, f"• {evento}")
