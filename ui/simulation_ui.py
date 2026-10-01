import curses
import time
import textwrap

from biology.niche_model import ModeloNichosEcologicos
from biology.trophic_web_model import ModeloRedTrofica
from planets.local_calendar import fecha_local, periodo_orbital_dias
from universe.events import Event
from universe.save_manager import SaveManager
from ui.console_utils import centrar, escribir_seguro
from ui.save_game_menu import SaveGameMenu


class SimulationUI:
    REFRESCO_SEGUNDOS = 0.05

    def __init__(self, simulation):
        self.simulation = simulation
        self.universe = simulation.universe
        if self.universe.time.escala == "planeta":
            # La ubicación no se guarda: al reabrir empezamos en Universo.
            self.universe.time.establecer_escala("universo")
            self.universe.time.indice_velocidad = 1
        self.ruta = [{"tipo": "universo"}]
        self.velocidad_previa = None
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

        while True:
            if self._procesar_tecla(stdscr, stdscr.getch()):
                stdscr.nodelay(False)
                return
            self.simulation.actualizar()
            self._dibujar(stdscr)
            time.sleep(self.REFRESCO_SEGUNDOS)

    def _actual(self):
        return self.ruta[-1]

    def _abrir(self, tipo, objeto=None):
        pagina = {"tipo": tipo, "objeto": objeto}
        if tipo in ("estrellas", "sistemas", "planetas", "eventos"):
            pagina.update(filtro="", indice=0)
        elif tipo == "red_trofica":
            pagina["indice"] = 0
        self.ruta.append(pagina)
        if tipo == "planeta":
            tiempo = self.universe.time
            self.velocidad_previa = (tiempo.escala, tiempo.indice_velocidad)
            tiempo.establecer_escala("planeta")
            tiempo.indice_velocidad = 1  # x1 equivale al x1 universal.

    def _volver(self):
        if len(self.ruta) == 1:
            return True
        if self._actual()["tipo"] == "planeta":
            escala, indice = self.velocidad_previa
            tiempo = self.universe.time
            tiempo.establecer_escala(escala)
            tiempo.indice_velocidad = indice
            self.velocidad_previa = None
        self.ruta.pop()
        return False

    def _procesar_tecla(self, stdscr, tecla):
        if tecla == 27:
            return self._volver()
        if tecla in (ord("+"), ord("=")):
            self.simulation.subir_velocidad()
            return False
        if tecla == ord("-"):
            self.simulation.bajar_velocidad()
            return False
        if tecla in (ord("s"), ord("S")):
            self._guardar(stdscr)
            return False

        pagina = self._actual()
        tipo = pagina["tipo"]
        if tecla in (ord("v"), ord("V")) and tipo in (
            "universo", "estrella", "sistema", "planeta", "biosfera",
            "red_trofica",
        ):
            if tipo == "universo":
                contexto = None
            else:
                ambito = "planeta" if tipo in ("biosfera", "red_trofica") else tipo
                contexto = (ambito, self._nombre(pagina["objeto"]))
            self._abrir("eventos", contexto)
            return False
        if tipo == "red_trofica":
            enlaces = ModeloRedTrofica().enlaces(pagina["objeto"])
            visibles = max(1, stdscr.getmaxyx()[0] - 14)
            ultimo = max(0, len(enlaces) - visibles)
            if tecla == curses.KEY_UP:
                pagina["indice"] = max(0, pagina["indice"] - 1)
            elif tecla == curses.KEY_DOWN:
                pagina["indice"] = min(ultimo, pagina["indice"] + 1)
            elif tecla == curses.KEY_PPAGE:
                pagina["indice"] = max(0, pagina["indice"] - visibles)
            elif tecla == curses.KEY_NPAGE:
                pagina["indice"] = min(ultimo, pagina["indice"] + visibles)
            return False
        if tipo in ("estrellas", "sistemas", "planetas", "eventos"):
            items = self._items(pagina)
            pagina["indice"] = max(0, min(pagina["indice"], len(items) - 1))
            salto = max(1, stdscr.getmaxyx()[0] - 14)
            if tecla == curses.KEY_UP:
                pagina["indice"] = max(0, pagina["indice"] - 1)
            elif tecla == curses.KEY_DOWN:
                pagina["indice"] = min(len(items) - 1, pagina["indice"] + 1)
            elif tecla == curses.KEY_PPAGE:
                pagina["indice"] = max(0, pagina["indice"] - salto)
            elif tecla == curses.KEY_NPAGE:
                pagina["indice"] = min(len(items) - 1, pagina["indice"] + salto)
            elif tecla in (ord("/"), ord("f"), ord("F")):
                self._buscar(stdscr)
            elif tecla in (curses.KEY_ENTER, 10, 13) and items:
                elegido = items[pagina["indice"]]
                siguiente = {"estrellas": "estrella", "sistemas": "sistema",
                             "planetas": "planeta", "eventos": "evento"}[tipo]
                self._abrir(siguiente, elegido)
            return False

        if tipo == "universo":
            if tecla in (curses.KEY_ENTER, 10, 13):
                self._abrir("sistemas")
            elif tecla in (ord("e"), ord("E")):
                self._abrir("estrellas")
        elif tipo == "estrella" and tecla in (curses.KEY_ENTER, 10, 13):
            sistema = self._sistema_de_estrella(pagina["objeto"])
            if sistema is not None:
                self._abrir("sistema", sistema)
        elif tipo == "sistema":
            if tecla in (curses.KEY_ENTER, 10, 13, ord("p"), ord("P")):
                self._abrir("planetas", pagina["objeto"])
            elif tecla in (ord("e"), ord("E")):
                self._abrir("estrellas", pagina["objeto"])
        elif tipo == "planeta" and tecla in (ord("m"), ord("M")):
            self._abrir("biosfera", pagina["objeto"])
        elif tipo == "biosfera" and tecla in (ord("r"), ord("R")):
            self._abrir("red_trofica", pagina["objeto"])
        return False

    def _buscar(self, stdscr):
        pagina = self._actual()
        anterior = pagina["filtro"]
        texto = anterior
        stdscr.nodelay(False)
        try:
            while True:
                pagina["filtro"] = texto
                pagina["indice"] = 0
                self._dibujar(stdscr)
                alto, _ = stdscr.getmaxyx()
                self._texto(stdscr, alto - 3,
                            "Buscar: " + texto + "_  ·  Enter aplicar · Esc cancelar")
                stdscr.refresh()
                tecla = stdscr.getch()
                if tecla in (curses.KEY_ENTER, 10, 13):
                    break
                if tecla == 27:
                    pagina["filtro"] = anterior
                    break
                if tecla in (curses.KEY_BACKSPACE, 127, 8):
                    texto = texto[:-1]
                elif 32 <= tecla <= 126 and len(texto) < 40:
                    texto += chr(tecla)
        finally:
            stdscr.nodelay(True)
            self.simulation.reiniciar_reloj()

    def _guardar(self, stdscr):
        stdscr.nodelay(False)
        try:
            nombre = self.save_game_menu.guardar_partida(stdscr, self.save_manager)
            if nombre:
                self.save_manager.guardar(self.universe, nombre)
        finally:
            self.simulation.reiniciar_reloj()
            stdscr.nodelay(True)

    def _items(self, pagina):
        tipo = pagina["tipo"]
        if tipo == "eventos":
            contexto = pagina["objeto"]
            if contexto is None:
                items = list(self.universe.event_manager.obtener_eventos())
            else:
                items = self.universe.event_manager.obtener_por_entidad(*contexto)
            items.reverse()
        elif tipo == "estrellas":
            sistema = pagina["objeto"]
            if sistema is None:
                nombres = {nombre for s in self.universe.sistemas_estelares
                           for nombre in s.nombres_estrellas}
                nombres.update(e.nombre for e in self.universe.estrellas)
                nombres.update(r.nombre_origen for r in self.universe.remanentes)
            else:
                nombres = set(sistema.nombres_estrellas)
            items = sorted(nombres)
        elif tipo == "sistemas":
            items = sorted(self.universe.sistemas_estelares,
                           key=lambda s: s.nombre)
        else:
            sistema = pagina["objeto"]
            items = sorted((p for p in self.universe.planetas
                            if p.sistema_nombre == sistema.nombre),
                           key=lambda p: p.nombre)
        filtro = pagina["filtro"].casefold()
        return [item for item in items if filtro in self._nombre(item).casefold()]

    def _nombre(self, item):
        if isinstance(item, Event):
            return str(item)
        return item if isinstance(item, str) else item.nombre

    def _sistema_de_estrella(self, nombre):
        return next((s for s in self.universe.sistemas_estelares
                     if nombre in s.nombres_estrellas), None)

    def _estrella_activa(self, nombre):
        return next((e for e in self.universe.estrellas if e.nombre == nombre), None)

    def _remanente(self, nombre):
        return next((r for r in self.universe.remanentes
                     if r.nombre_origen == nombre), None)

    def _color(self, numero):
        try:
            return curses.color_pair(numero) if curses.has_colors() else 0
        except curses.error:
            return 0

    def _texto(self, stdscr, fila, texto, atributo=0):
        escribir_seguro(stdscr, fila, 2, texto, atributo)

    def _separador(self, stdscr, fila):
        _, ancho = stdscr.getmaxyx()
        escribir_seguro(stdscr, fila, 0, "─" * (ancho - 1), self._color(1))

    def _dibujar(self, stdscr):
        stdscr.erase()
        alto, ancho = stdscr.getmaxyx()
        if alto < 24 or ancho < 72:
            centrar(stdscr, 2, "TRAVEL STUFF")
            centrar(stdscr, 4, "Amplía la terminal a 72 columnas x 24 filas.")
            stdscr.refresh()
            return
        pagina = self._actual()
        tipo = pagina["tipo"]
        self._separador(stdscr, 0)
        self._texto(stdscr, 1, "TRAVEL STUFF  /  EXPLORADOR DEL UNIVERSO",
                    curses.A_BOLD | self._color(1))
        anio = f"{self.universe.time.anio:,}".replace(",", " ")
        self._texto(stdscr, 2, f"Año {anio} · Semilla {self.universe.seed} · "
                    f"{self.universe.time.obtener_descripcion_velocidad()}")
        self._texto(stdscr, 4, "  ›  ".join(
            "Red trófica" if p["tipo"] == "red_trofica" else
            self._nombre(p["objeto"]) if p.get("objeto") is not None
            and p["tipo"] not in ("estrellas", "planetas", "eventos")
            else p["tipo"].capitalize() for p in self.ruta))
        self._separador(stdscr, 5)
        if tipo == "universo":
            self._dibujar_universo(stdscr)
        elif tipo in ("estrellas", "sistemas", "planetas", "eventos"):
            self._dibujar_lista(stdscr, pagina)
        elif tipo == "estrella":
            self._dibujar_estrella(stdscr, pagina["objeto"])
        elif tipo == "sistema":
            self._dibujar_sistema(stdscr, pagina["objeto"])
        elif tipo == "evento":
            self._dibujar_evento(stdscr, pagina["objeto"])
        elif tipo == "biosfera":
            self._dibujar_biosfera(stdscr, pagina["objeto"])
        elif tipo == "red_trofica":
            self._dibujar_red_trofica(stdscr, pagina, alto)
        else:
            self._dibujar_planeta(stdscr, pagina["objeto"])
        self._separador(stdscr, alto - 2)
        controles = ("Enter Sistemas · E Estrellas · V Eventos · S Guardar · +/- · Esc Menú"
                     if tipo == "universo" else
                     "↑↓/PgUp/PgDn Mover · / Buscar · Enter Abrir · Esc Volver"
                     if tipo in ("estrellas", "sistemas", "planetas", "eventos") else
                     "M Biosfera · V Eventos · S Guardar · +/- Tiempo · Esc Volver"
                     if tipo == "planeta" else
                     "R Red trófica · V Eventos · S Guardar · Esc Volver"
                     if tipo == "biosfera" else
                     "↑↓/PgUp/PgDn · V Eventos · S Guardar · Esc Volver"
                     if tipo == "red_trofica" else
                     "Enter Sistema · V Eventos · S Guardar · +/- · Esc Volver"
                     if tipo == "estrella" else
                     "Enter Planetas · E Estrellas · V Eventos · S Guardar · Esc"
                     if tipo == "sistema" else
                     "S Guardar · +/- Tiempo · Esc Volver")
        self._texto(stdscr, alto - 1, controles)
        stdscr.refresh()

    def _dibujar_universo(self, stdscr):
        u = self.universe
        self._texto(stdscr, 6, "UNIVERSO  ·  resumen", curses.A_BOLD)
        self._texto(stdscr, 8, f"Sistemas {len(u.sistemas_estelares)} · "
                    f"Estrellas activas {len(u.estrellas)} · Remanentes {len(u.remanentes)}")
        self._texto(stdscr, 9, f"Planetas formados {len(u.planetas)}")
        self._texto(stdscr, 11, f"Mundos con vida ahora {sum(p.vida_activa for p in u.planetas)}"
                    f" · con vida histórica {sum(p.alcanzo_primera_vida for p in u.planetas)}")
        self._texto(stdscr, 12, f"Mundos con protocélulas históricas "
                    f"{sum(p.alcanzo_protocelula for p in u.planetas)}")
        self._texto(stdscr, 13, "Extinciones masivas locales "
                    f"{sum(p.extinciones_masivas_locales for p in u.planetas)}"
                    " · Radiaciones "
                    f"{sum(len(p.ancestros_con_radiacion) for p in u.planetas)}")
        self._texto(stdscr, 14, "EVENTOS RECIENTES", curses.A_BOLD)
        recientes = u.event_manager.obtener_recientes(4)
        if not recientes:
            self._texto(stdscr, 15, "Aún no hay eventos registrados.")
        for fila, evento in enumerate(reversed(recientes), start=15):
            self._texto(stdscr, fila, str(evento))
        self._texto(stdscr, 20, "Las galaxias aún no están modeladas.")

    def _resumen_item(self, tipo, item):
        if tipo == "eventos":
            return str(item)
        if tipo == "sistemas":
            return (f"{item.nombre} · estrellas {len(item.nombres_estrellas)}"
                    f" · planetas {len(item.nombres_planetas)}")
        if tipo == "planetas":
            vida = "vida" if item.vida_activa else "sin vida activa"
            return f"{item.nombre} · {item.masa_tierra:.2f} M⊕ · {vida}"
        estrella = self._estrella_activa(item)
        if estrella is not None:
            return f"{item} · activa · {estrella.etapa.replace('_', ' ')}"
        remanente = self._remanente(item)
        if remanente is not None:
            return f"{item} · remanente {remanente.tipo.replace('_', ' ')}"
        return f"{item} · sin estado estelar actual"

    def _dibujar_lista(self, stdscr, pagina):
        tipo = pagina["tipo"]
        items = self._items(pagina)
        pagina["indice"] = max(0, min(pagina["indice"], len(items) - 1))
        alto, _ = stdscr.getmaxyx()
        visibles = alto - 14
        inicio = max(0, pagina["indice"] - visibles + 1)
        inicio = min(inicio, max(0, len(items) - visibles))
        titulo = "HISTORIAL DE EVENTOS" if tipo == "eventos" else f"CATÁLOGO DE {tipo.upper()}"
        self._texto(stdscr, 6, titulo, curses.A_BOLD)
        self._texto(stdscr, 7, f"Filtro: {pagina['filtro'] or 'todos'}")
        self._texto(stdscr, 8, f"Resultados {len(items)} · "
                    f"selección {pagina['indice'] + 1 if items else 0}")
        self._separador(stdscr, 9)
        if not items:
            mensaje = ("Sin resultados. Borra el filtro con /."
                       if pagina["filtro"] else
                       "Aún no hay eventos en esta vista." if tipo == "eventos" else
                       f"Aún no hay {tipo} registrados.")
            self._texto(stdscr, 11, mensaje)
        for fila, item in enumerate(items[inicio:inicio + visibles], start=10):
            indice = inicio + fila - 10
            marca = "›" if indice == pagina["indice"] else " "
            self._texto(stdscr, fila, f"{marca} {self._resumen_item(tipo, item)}",
                        curses.A_REVERSE if indice == pagina["indice"] else 0)
        if items:
            self._texto(stdscr, alto - 4,
                        f"Mostrando {inicio + 1}-{min(inicio + visibles, len(items))}"
                        f" de {len(items)}")

    def _dibujar_estrella(self, stdscr, nombre):
        self._texto(stdscr, 6, "ESTRELLA  ·  ficha", curses.A_BOLD)
        self._texto(stdscr, 8, nombre)
        sistema = self._sistema_de_estrella(nombre)
        self._texto(stdscr, 9, f"Sistema: {sistema.nombre if sistema else 'desconocido'}")
        estrella = self._estrella_activa(nombre)
        remanente = self._remanente(nombre)
        if estrella is not None:
            self._texto(stdscr, 11, f"Estado: {estrella.etapa.replace('_', ' ')}")
            self._texto(stdscr, 12, f"Masa actual: {estrella.masa_actual:.2f} M☉")
            if estrella.temperatura_efectiva is not None:
                self._texto(stdscr, 13,
                            f"Temperatura efectiva: {estrella.temperatura_efectiva:.0f} K")
        elif remanente is not None:
            self._texto(stdscr, 11, f"Remanente: {remanente.tipo.replace('_', ' ')}")
            self._texto(stdscr, 12, f"Masa: {remanente.masa:.2f} M☉")
        else:
            self._texto(stdscr, 11, "Sin estado estelar actual modelado.")
        recientes = self.universe.event_manager.obtener_por_entidad("estrella", nombre)
        self._texto(stdscr, 15, "EVENTOS RECIENTES", curses.A_BOLD)
        if not recientes:
            self._texto(stdscr, 16, "Aún no hay eventos de esta estrella.")
        for fila, evento in enumerate(reversed(recientes[-3:]), start=16):
            self._texto(stdscr, fila, str(evento))

    def _dibujar_sistema(self, stdscr, sistema):
        self._texto(stdscr, 6, "SISTEMA ESTELAR  ·  ficha", curses.A_BOLD)
        self._texto(stdscr, 8, sistema.nombre)
        self._texto(stdscr, 9, f"Formación: año {sistema.anio_formacion:,}".replace(",", " "))
        self._texto(stdscr, 11, f"Tipo: {sistema.obtener_tipo()} · "
                    f"estrellas {len(sistema.nombres_estrellas)}")
        self._texto(stdscr, 12, f"Planetas registrados: {len(sistema.nombres_planetas)}")
        self._texto(stdscr, 13, "Estrella principal: " +
                    (sistema.nombre_estrella_primaria or "sin dato"))
        recientes = self.universe.event_manager.obtener_por_entidad(
            "sistema", sistema.nombre
        )
        self._texto(stdscr, 16, "EVENTOS RECIENTES", curses.A_BOLD)
        for fila, evento in enumerate(reversed(recientes[-3:]), start=17):
            self._texto(stdscr, fila, str(evento))

    def _dibujar_evento(self, stdscr, evento):
        self._texto(stdscr, 6, "EVENTO  ·  detalle", curses.A_BOLD)
        self._texto(stdscr, 8, evento.tipo)
        self._texto(stdscr, 9, f"Año universal {evento.anio:,}".replace(",", " "))
        self._texto(stdscr, 10, f"Ámbito: {evento.ambito}"
                    + (f" · {evento.entidad}" if evento.entidad else ""))
        _, ancho = stdscr.getmaxyx()
        for fila, linea in enumerate(textwrap.wrap(evento.mensaje, ancho - 5), start=12):
            if fila >= stdscr.getmaxyx()[0] - 3:
                break
            self._texto(stdscr, fila, linea)

    def _dibujar_planeta(self, stdscr, planeta):
        u = self.universe
        especies = u.modelo_especies_unicelulares
        self._texto(stdscr, 6, "PLANETA  ·  observación", curses.A_BOLD)
        self._texto(stdscr, 7, planeta.nombre)
        self._texto(stdscr, 8, f"Sistema: {planeta.sistema_nombre or 'sin dato'}")
        self._texto(stdscr, 9, f"Masa {planeta.masa_tierra:.2f} M⊕ · "
                    f"órbita {planeta.semieje_mayor_au:.2f} AU")
        self._texto(stdscr, 10, "Regla: " + planeta.regimen_mundo.replace("_", " "))
        ruta = planeta.ruta_metabolica_inicial or "sin ruta"
        self._texto(stdscr, 11, "Metabolismo: " + ruta.replace("_", " "))
        self._texto(stdscr, 12, "CONDICIONES ACTUALES", curses.A_BOLD)
        self._texto(stdscr, 13, "Habitabilidad: " +
                    planeta.estado_habitabilidad_fase1.replace("_", " "))
        self._texto(stdscr, 14, "Agua: " + (planeta.estado_agua_preclima or "sin dato"))
        self._texto(stdscr, 15, "Química: " +
                    planeta.estado_quimica_prebiotica.replace("_", " "))
        self._texto(stdscr, 16, f"Protocélulas: {'viables' if planeta.protocelula_viable else 'no viables'}"
                    f" · logro histórico {'sí' if planeta.alcanzo_protocelula else 'no'}")
        self._texto(stdscr, 17, f"Vida: {'activa' if planeta.vida_activa else 'inactiva'}"
                    f" · población {planeta.poblacion_unicelular}")
        self._texto(stdscr, 18, f"Especies vivas {len(especies.especies_vivas(planeta))}"
                    f" · extintas {len(especies.especies_extintas(planeta))}"
                    f" · ext. masivas {planeta.extinciones_masivas_locales}"
                    f" · radiaciones {len(planeta.ancestros_con_radiacion)}")
        anio_formacion = planeta.anio_formacion
        duracion = planeta.periodo_orbital_dias
        aproximada = False
        if anio_formacion is None or duracion is None:
            # Los guardados antiguos no tenían calendario; reconstruimos
            # una fecha aproximada sin cambiar el archivo ni la simulación.
            aproximada = True
            estrella = self._estrella_activa(planeta.estrella_anfitriona)
            disco = next((d for d in u.discos_protoplanetarios
                          if d.estrella_nombre == planeta.estrella_anfitriona), None)
            sistema = u.buscar_sistema_estelar(planeta.sistema_nombre)
            if anio_formacion is None:
                anio_formacion = (estrella.anio_nacimiento if estrella else
                                   sistema.anio_formacion if sistema else None)
            if duracion is None:
                masa = (disco.masa_estelar_msol if disco else
                        estrella.masa_inicial if estrella else None)
                duracion = periodo_orbital_dias(planeta.semieje_mayor_au, masa)
        fecha = fecha_local(planeta, u.time, anio_formacion, duracion)
        if fecha is None:
            self._texto(stdscr, 20, "Fecha local: faltan datos orbitales o de formación.")
        else:
            anio, mes, dia, hora, minuto, segundo = fecha
            marca = " aprox." if aproximada else ""
            self._texto(stdscr, 19, f"Año orbital{marca}: {duracion:.2f} días estándar")
            self._texto(stdscr, 20, f"Año {anio:,} · mes {mes} · día {dia}".replace(",", " "))
            self._texto(stdscr, 21, f"Hora {hora:02d}:{minuto:02d}:{segundo:02d}"
                        " · meses = 1/12 del año orbital")

    def _dibujar_biosfera(self, stdscr, planeta):
        self._texto(stdscr, 6, "BIOSFERA  ·  inicio microbiano", curses.A_BOLD)
        nichos = ModeloNichosEcologicos().resumen(planeta)
        self._texto(stdscr, 7,
                    f"Nichos: org {nichos['organicos']} · luz {nichos['luz']}"
                    f" · restos {nichos['restos']} · presas {nichos['presas']}"
                    f" · sin ruta {nichos['sin_recurso']}")
        self._texto(stdscr, 8, planeta.nombre)
        self._texto(stdscr, 9, f"Vida: {'activa' if planeta.vida_activa else 'inactiva'}"
                    f" · población {planeta.poblacion_unicelular}")
        self._texto(stdscr, 10, "Ciclo: restos "
                    f"{planeta.restos_organicos_unidades} · nutrientes "
                    f"{planeta.nutrientes_reciclados_unidades} · usados "
                    f"{planeta.total_nutrientes_aprovechados}")
        fuentes = ", ".join(planeta.fuentes_energia_potenciales) or "ninguna modelada"
        self._texto(stdscr, 11, "Fuentes ambientales: " + fuentes.replace("_", " "))
        self._texto(stdscr, 12,
                    f"Colonias simples: {planeta.colonias_multicelulares_activas}"
                    f" · linajes cohesivos {len(planeta.linajes_cohesivos)}"
                    f" · históricas "
                    f"{'sí' if planeta.alcanzo_colonia_multicelular else 'no'}")
        ruta = planeta.ruta_metabolica_inicial or "ninguna"
        self._texto(stdscr, 13, "Ruta metabólica: " + ruta.replace("_", " "))
        self._texto(stdscr, 14, "Estado: " + planeta.estado_ecosistema.replace("_", " "))
        self._texto(stdscr, 15, f"Productores fotosintéticos: "
                    f"{planeta.unidades_productoras_activas}"
                    f" · históricos {'sí' if planeta.alcanzo_fotosintesis else 'no'}")
        if planeta.unidades_productoras_activas and "organicos_ambientales" in (
                planeta.fuentes_energia_potenciales):
            self._texto(stdscr, 16, "Luz → productores · orgánicos → consumidores")
        elif planeta.unidades_productoras_activas:
            self._texto(stdscr, 16, "Enlace: luz → productores microbianos")
        elif planeta.ruta_metabolica_inicial == "consumo_organicos":
            self._texto(stdscr, 16, "Enlace: orgánicos ambientales → microbios")
        else:
            self._texto(stdscr, 16, "Aún no hay un enlace ecológico modelado.")
        self._texto(stdscr, 17,
                    f"Restos → descomponedores: "
                    f"{planeta.unidades_descomponedoras_activas} activos"
                    f" · capacidad histórica "
                    f"{'sí' if planeta.alcanzo_capacidad_descomponedora else 'no'}")
        self._texto(stdscr, 18, "ATMÓSFERA · proyección biológica", curses.A_BOLD)
        co2_fisico = planeta.presion_co2_preclima_bar
        co2_vida = planeta.presion_co2_con_vida_bar
        if co2_fisico is None or co2_vida is None:
            self._texto(stdscr, 19, "CO₂: sin datos atmosféricos")
        else:
            self._texto(stdscr, 19,
                        f"CO₂ físico {co2_fisico:.3g} → con vida {co2_vida:.3g} bar")
        oxigeno = planeta.aporte_o2_biologico_bar
        if oxigeno is None:
            self._texto(stdscr, 20, "Aporte de O₂: sin datos")
        else:
            self._texto(stdscr, 20, f"Aporte de O₂: {oxigeno:.3g} bar (diseño)")
        ultima = ("ninguna" if planeta.ultima_especie_presa_id is None else
                  f"especie {planeta.ultima_especie_predadora_id} → "
                  f"especie {planeta.ultima_especie_presa_id}")
        self._texto(stdscr, 21,
                    f"Capturas: {planeta.capturas_depredacion} · última: {ultima}")

    def _dibujar_red_trofica(self, stdscr, pagina, alto):
        planeta = pagina["objeto"]
        modelo = ModeloRedTrofica()
        enlaces = modelo.enlaces(planeta)
        resumen = modelo.resumen(planeta)
        self._texto(stdscr, 6, "RED TRÓFICA  ·  relaciones actuales", curses.A_BOLD)
        self._texto(stdscr, 7, planeta.nombre)
        self._texto(stdscr, 8,
                    f"Especies {resumen['especies']} · recursos "
                    f"{resumen['recursos']} · presas posibles "
                    f"{resumen['presas_posibles']}")
        self._texto(stdscr, 9, "Flecha: fuente de energía o presa → consumidor")
        self._separador(stdscr, 10)
        visibles = max(1, alto - 14)
        inicio = min(pagina["indice"], max(0, len(enlaces) - visibles))
        pagina["indice"] = inicio
        nombres = {"luz": "Luz", "organicos": "Orgánicos", "restos": "Restos"}
        if not enlaces:
            self._texto(stdscr, 12, "Sin relaciones tróficas actuales.")
        for fila, enlace in enumerate(enlaces[inicio:inicio + visibles], start=11):
            if enlace["tipo"] == "recurso":
                descripcion = (f"{nombres[enlace['origen']]} → especie "
                               f"{enlace['destino']} · {enlace['unidades']} unidades")
            else:
                descripcion = (f"Especie {enlace['origen']} → especie "
                               f"{enlace['destino']} · captura posible")
            self._texto(stdscr, fila, descripcion)
        self._texto(stdscr, alto - 3,
                    f"Mostrando {inicio + 1 if enlaces else 0}-"
                    f"{min(inicio + visibles, len(enlaces))} de {len(enlaces)}"
                    " · posible no significa realizada")
