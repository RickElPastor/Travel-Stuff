import curses
import time

from save_manager import SaveManager

from ui.console_utils import centrar, escribir_seguro, linea_horizontal

from ui.save_game_menu import SaveGameMenu


class SimulationUI:
    REFRESCO_SEGUNDOS = 0.01

    def __init__(self, simulation):
        self.simulation = simulation

        self.universe = simulation.universe

        self.scroll_eventos = 0

        self.save_manager = SaveManager()

        self.save_game_menu = SaveGameMenu()

    def ejecutar(self, stdscr):
        stdscr.nodelay(True)
        stdscr.keypad(True)

        try:
            curses.curs_set(0)

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

    def _procesar_mouse(self):
        try:
            evento_mouse = curses.getmouse()

        except curses.error:
            return

        estado = evento_mouse[4]

        if estado & curses.BUTTON4_PRESSED:
            self._subir_eventos()

        elif estado & curses.BUTTON5_PRESSED:
            self._bajar_eventos()

    def _subir_eventos(self):
        eventos = self.universe.event_manager.obtener_eventos()

        max_scroll = max(0, len(eventos) - 1)

        self.scroll_eventos = min(self.scroll_eventos + 1, max_scroll)

    def _bajar_eventos(self):
        self.scroll_eventos = max(0, self.scroll_eventos - 1)

    def _guardar(self, stdscr):
        stdscr.nodelay(False)

        nombre = self.save_game_menu.guardar_partida(stdscr, self.save_manager)

        if nombre:
            self.save_manager.guardar(self.universe, nombre)

        self.simulation.reiniciar_reloj()

        stdscr.nodelay(True)

    def _dibujar(self, stdscr):
        stdscr.erase()

        alto, ancho = stdscr.getmaxyx()

        if alto < 24 or ancho < 72:
            centrar(stdscr, 2, "TRAVEL STUFF")

            centrar(stdscr, 4, ("La terminal es " "demasiado pequeña."))

            centrar(stdscr, 5, ("Usa al menos " "72 columnas x 24 filas."))

            stdscr.refresh()
            return

        fila = 0

        fila = self._dibujar_cabecera(stdscr, fila)

        fila = self._dibujar_universo(stdscr, fila)

        fila = self._dibujar_estrellas(stdscr, fila)

        fila = self._dibujar_remanentes(stdscr, fila)

        self._dibujar_eventos(stdscr, fila, alto)

        controles = (
            "ESC Menu | " "S Guardar | " "UP/DOWN Velocidad | " "PgUp/PgDn Eventos"
        )

        linea_horizontal(stdscr, alto - 2)

        escribir_seguro(stdscr, alto - 1, 0, controles)

        stdscr.refresh()

    def _dibujar_cabecera(self, stdscr, fila):
        centrar(stdscr, fila, (".       *        .        " "+        ."))

        fila += 1

        centrar(
            stdscr,
            fila,
            ("*       TRAVEL STUFF - " "SIMULACION       *"),
            curses.A_BOLD,
        )

        fila += 1

        centrar(stdscr, fila, (".    +       .        " "*        ."))

        fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_universo(
        self,
        stdscr,
        fila,
    ):
        escribir_seguro(
            stdscr,
            fila,
            0,
            "UNIVERSO",
            curses.A_BOLD,
        )

        fila += 1

        edad = self._numero_entero(self.universe.time.anio)

        velocidad = self.universe.time.obtener_descripcion_velocidad()

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                f"Semilla: "
                f"{self.universe.seed}"
                "  |  "
                f"Edad: {edad} años"
                "  |  "
                f"Velocidad: {velocidad}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Estrellas activas: "
                f"{len(self.universe.estrellas)}"
                "  |  "
                "Remanentes: "
                f"{len(self.universe.remanentes)}"
            ),
        )

        fila += 1

        sistemas_simples = 0
        sistemas_binarios = 0
        sistemas_triples = 0
        sistemas_multiples = 0

        for sistema in self.universe.sistemas_estelares:
            tipo = sistema.obtener_tipo()

            if tipo == "simple":
                sistemas_simples += 1

            elif tipo == "binario":
                sistemas_binarios += 1

            elif tipo == "triple":
                sistemas_triples += 1

            elif tipo == "multiple":
                sistemas_multiples += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Sistemas: "
                f"{len(self.universe.sistemas_estelares)}"
                "  |  "
                f"Simples: {sistemas_simples}"
                "  |  "
                f"Binarios: {sistemas_binarios}"
                "  |  "
                "Triples+: "
                f"{sistemas_triples + sistemas_multiples}"
            ),
        )

        fila += 1

        discos_truncados = sum(
            1
            for disco in self.universe.discos_protoplanetarios
            if disco.truncado_por_companera
        )

        cantidad_embriones = sum(
            disco.obtener_cantidad_embriones()
            for disco in self.universe.discos_protoplanetarios
        )

        cantidad_protoplanetas = sum(
            disco.obtener_cantidad_protoplanetas()
            for disco in self.universe.discos_protoplanetarios
        )

        cantidad_planetas = len(self.universe.planetas)

        candidatos_gas = sum(
            1 for planeta in self.universe.planetas if planeta.candidato_captura_gas
        )

        candidatos_con_gas = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.candidato_captura_gas and planeta.gas_disponible_al_formarse)
        )

        # Todos los planetas que capturaron
        # cualquier cantidad de gas.
        planetas_con_gas = sum(
            1 for planeta in self.universe.planetas if planeta.masa_gas_tierra > 0
        )

        candidatos_runaway = sum(
            1 for planeta in self.universe.planetas if planeta.candidato_runaway
        )

        gigantes_runaway = sum(
            1 for planeta in self.universe.planetas if planeta.entro_runaway
        )

        # Estados finales de formación.
        planetas_solidos = sum(
            1 for planeta in self.universe.planetas if planeta.masa_gas_tierra == 0
        )

        planetas_con_envoltura = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.masa_gas_tierra > 0 and not planeta.entro_runaway)
        )

        masa_gas_runaway = sum(
            planeta.masa_gas_runaway_tierra for planeta in self.universe.planetas
        )

        masa_gas_planetas = sum(
            planeta.masa_gas_tierra for planeta in self.universe.planetas
        )

        masa_total_planetas = sum(
            planeta.masa_solida_tierra for planeta in self.universe.planetas
        )

        masa_total_embriones = sum(
            disco.obtener_masa_embriones_tierra()
            for disco in self.universe.discos_protoplanetarios
        )

        masa_total_protoplanetas = sum(
            disco.obtener_masa_protoplanetas_tierra()
            for disco in self.universe.discos_protoplanetarios
        )

        planeta_mas_masivo = max(
            self.universe.planetas,
            key=lambda planeta: planeta.masa_tierra,
            default=None,
        )

        planeta_irradiado = next(
            (
                planeta
                for planeta in self.universe.planetas
                if (planeta.flujo_estelar_tierra is not None)
            ),
            None,
        )

        planetas_en_hz = sum(
            1
            for planeta in self.universe.planetas
            if planeta.en_zona_habitable_radiativa
        )

        candidatos_terrestres_hz = sum(
            1 for planeta in self.universe.planetas if planeta.candidato_terrestre_hz
        )

        candidatos_con_retencion = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.candidato_terrestre_hz and planeta.retencion_atmosferica_aprox)
        )

        candidatos_geologicamente_activos = sum(
            1
            for planeta in self.universe.planetas
            if (
                planeta.candidato_terrestre_hz
                and planeta.retencion_atmosferica_aprox
                and planeta.geologicamente_activo
            )
        )

        candidatos_con_agua_inicial = sum(
            1
            for planeta in self.universe.planetas
            if (
                planeta.candidato_terrestre_hz
                and planeta.retencion_atmosferica_aprox
                and planeta.masa_agua_inicial_tierra is not None
                and planeta.masa_agua_inicial_tierra > 0
            )
        )

        candidatos_con_agua_condensada = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.candidato_terrestre_hz and planeta.tiene_agua_condensada)
        )

        candidatos_con_atmosfera = sum(
            1
            for planeta in self.universe.planetas
            if planeta.tiene_atmosfera_secundaria
        )

        candidatos_habitables_fase1 = sum(
            1 for planeta in self.universe.planetas if planeta.candidato_habitable_fase1
        )

        candidatos_temperados = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.estado_habitabilidad_fase1 == "candidato_temperado")
        )

        candidatos_glaciados = sum(
            1
            for planeta in self.universe.planetas
            if (planeta.estado_habitabilidad_fase1 == "candidato_glaciado")
        )

        planeta_atmosfera_ejemplo = next(
            (
                planeta
                for planeta in self.universe.planetas
                if planeta.tiene_atmosfera_secundaria
            ),
            None,
        )

        planeta_agua_ejemplo = next(
            (
                planeta
                for planeta in self.universe.planetas
                if (planeta.presion_atmosferica_preclima_bar is not None)
            ),
            None,
        )

        candidatos_prebioticos = sum(
            1
            for planeta in self.universe.planetas
            if planeta.candidato_quimica_prebiotica
        )

        rutas_uv = sum(
            1 for planeta in self.universe.planetas if planeta.ruta_uv_prebiotica
        )

        rutas_geoquimicas = sum(
            1
            for planeta in self.universe.planetas
            if planeta.ruta_geoquimica_prebiotica
        )

        mundos_prebioticos_historicos = sum(
            1 for planeta in self.universe.planetas if planeta.tuvo_entorno_prebiotico
        )

        mundos_uv_historicos = sum(
            1 for planeta in self.universe.planetas if planeta.tuvo_ruta_uv_prebiotica
        )

        mundos_geoquimicos_historicos = sum(
            1
            for planeta in self.universe.planetas
            if planeta.tuvo_ruta_geoquimica_prebiotica
        )

        mundos_con_organicos_simples = sum(
            1 for planeta in self.universe.planetas if planeta.alcanzo_organicos_simples
        )

        organicos_ruta_uv = sum(
            1
            for planeta in self.universe.planetas
            if planeta.ruta_organicos_simples == "uv"
        )

        organicos_ruta_geoquimica = sum(
            1
            for planeta in self.universe.planetas
            if planeta.ruta_organicos_simples == "geoquimica"
        )

        organicos_ruta_mixta = sum(
            1
            for planeta in self.universe.planetas
            if planeta.ruta_organicos_simples == "uv_y_geoquimica"
        )

        mundos_con_concentracion_prebiotica = sum(
            1
            for planeta in self.universe.planetas
            if planeta.alcanzo_concentracion_prebiotica
        )

        mundos_con_precursores_complejos = sum(
            1
            for planeta in self.universe.planetas
            if planeta.alcanzo_precursores_complejos
        )

        mundos_con_polimerizacion = sum(
            1
            for planeta in self.universe.planetas
            if planeta.alcanzo_polimerizacion_prebiotica
        )

        concentracion_por_hielo = sum(
            1
            for planeta in self.universe.planetas
            if planeta.mecanismo_concentracion_prebiotica == "concentracion_por_hielo"
        )

        concentracion_geoquimica = sum(
            1
            for planeta in self.universe.planetas
            if planeta.mecanismo_concentracion_prebiotica == "gradientes_geoquimicos"
        )

        concentracion_mixta = sum(
            1
            for planeta in self.universe.planetas
            if planeta.mecanismo_concentracion_prebiotica == "hielo_y_geoquimica"
        )

        mundos_normales = sum(
            1 for planeta in self.universe.planetas if planeta.regimen_mundo == "normal"
        )

        mundos_extraordinarios = sum(
            1
            for planeta in self.universe.planetas
            if planeta.regimen_mundo == "extraordinario"
        )

        mundos_arcanos = sum(
            1
            for planeta in self.universe.planetas
            if planeta.tipo_regla_extraordinaria == "arcano"
        )

        mundos_anomalos = sum(
            1
            for planeta in self.universe.planetas
            if planeta.tipo_regla_extraordinaria == "anomalia_fisica"
        )

        mundos_energia_exotica = sum(
            1
            for planeta in self.universe.planetas
            if planeta.tipo_regla_extraordinaria == "energia_exotica"
        )

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Discos de formación: "
                f"{len(self.universe.discos_protoplanetarios)}"
                "  |  "
                "Truncados por binaria: "
                f"{discos_truncados}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            ("Embriones planetarios: " f"{cantidad_embriones}"),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            ("Protoplanetas: " f"{cantidad_protoplanetas}"),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Planetas: "
                f"{cantidad_planetas}"
                " | "
                f"Candidatos gas: {candidatos_gas}"
                " | "
                f"A tiempo: {candidatos_con_gas}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Envolturas totales: "
                f"{planetas_con_gas}"
                " | "
                "Runaway candidatos: "
                f"{candidatos_runaway}"
                " | "
                "Gas capturado: "
                f"{masa_gas_planetas:.3f} Mt"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Runaway realizado: "
                f"{gigantes_runaway}"
                " | "
                "Gas runaway: "
                f"{masa_gas_runaway:.3f} Mt"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Estados planetarios: "
                f"solidos={planetas_solidos}"
                " | "
                f"envoltura={planetas_con_envoltura}"
                " | "
                f"gigantes={gigantes_runaway}"
            ),
        )

        fila += 1

        if planeta_mas_masivo is not None:
            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Planeta mas masivo: "
                    f"M={planeta_mas_masivo.masa_tierra:.2f} Mt"
                    " | "
                    f"R={planeta_mas_masivo.radio_tierra:.2f} Rt"
                    " | "
                    f"rho={planeta_mas_masivo.densidad_g_cm3:.2f} g/cm3"
                    " | "
                    f"g={planeta_mas_masivo.gravedad_superficial_ms2:.1f} m/s2"
                ),
            )

        else:
            escribir_seguro(
                stdscr,
                fila,
                0,
                "Todavia no hay planetas.",
            )

        fila += 1

        if planeta_irradiado is not None:
            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Irradiacion ejemplo: "
                    f"S={planeta_irradiado.flujo_estelar_tierra:.3f} S-Tierra"
                    " | "
                    f"F={planeta_irradiado.irradiancia_media_w_m2:.1f} W/m2"
                    " | "
                    "Teq0="
                    f"{planeta_irradiado.temperatura_equilibrio_cero_albedo_k:.1f} K"
                ),
            )

        else:
            escribir_seguro(
                stdscr,
                fila,
                0,
                ("Irradiacion ejemplo: " "sin estrella anfitriona activa"),
            )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Habitabilidad: "
                f"HZ={planetas_en_hz}"
                " | "
                f"Ter={candidatos_terrestres_hz}"
                " | "
                f"Ret={candidatos_con_retencion}"
                " | "
                f"Hab={candidatos_habitables_fase1}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Planeta activo: "
                f"Geo={candidatos_geologicamente_activos}"
                " | "
                f"Atm={candidatos_con_atmosfera}"
                " | "
                f"H2Ocond={candidatos_con_agua_condensada}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Prebiotica: "
                f"hist={mundos_prebioticos_historicos}"
                " | "
                f"org={mundos_con_organicos_simples}"
                " | "
                f"conc={mundos_con_concentracion_prebiotica}"
                " | "
                f"comp={mundos_con_precursores_complejos}"
                " | "
                f"polim={mundos_con_polimerizacion}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Mundos: "
                f"normal={mundos_normales}"
                " | "
                f"extra={mundos_extraordinarios}"
                " | "
                f"arc={mundos_arcanos}"
                " | "
                f"anom={mundos_anomalos}"
                " | "
                f"exo={mundos_energia_exotica}"
            ),
        )

        fila += 1

        escribir_seguro(
            stdscr,
            fila,
            0,
            (
                "Masa formación: "
                f"E={masa_total_embriones:.3f} Mt"
                " | "
                f"P={masa_total_protoplanetas:.3f} Mt"
                " | "
                f"planetas={masa_total_planetas:.3f} Mt"
            ),
        )

        fila += 1

        disco_ejemplo = next(
            iter(self.universe.discos_protoplanetarios),
            None,
        )

        if disco_ejemplo is not None:
            masa_polvo = self._valor(
                disco_ejemplo.masa_polvo_tierra,
                "Mt",
                2,
            )

            radio_caracteristico = self._valor(
                disco_ejemplo.radio_caracteristico_au,
                "AU",
                2,
            )

            linea_hielo = self._valor(
                disco_ejemplo.linea_hielo_au,
                "AU",
                2,
            )

            masa_interior = self._valor(
                disco_ejemplo.obtener_masa_polvo_interior_linea_hielo(),
                "Mt",
                2,
            )

            masa_exterior = self._valor(
                disco_ejemplo.obtener_masa_polvo_exterior_linea_hielo(),
                "Mt",
                2,
            )

            cantidad_embriones_disco = disco_ejemplo.obtener_cantidad_embriones()

            masa_embriones = self._valor(
                disco_ejemplo.obtener_masa_embriones_tierra(),
                "Mt",
                3,
            )

            masa_planetesimales = self._valor(
                disco_ejemplo.masa_planetesimales_tierra,
                "Mt",
                3,
            )

            masa_gas = self._valor(
                disco_ejemplo.masa_gas_referencia_tierra,
                "Mt",
                1,
            )

            vida_gas = self._valor(
                disco_ejemplo.vida_gas_myr,
                "Myr",
                2,
            )

            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Disco ejemplo: "
                    f"polvo={masa_polvo} | "
                    f"Rc={radio_caracteristico} | "
                    f"hielo={linea_hielo}"
                ),
            )

            fila += 1

            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Sólidos: "
                    f"interior={masa_interior} | "
                    f"exterior={masa_exterior}"
                ),
            )

            fila += 1

            escribir_seguro(
                stdscr,
                fila,
                0,
                ("Gas de referencia: " f"{masa_gas}" " | " f"vida={vida_gas}"),
            )

            fila += 1

            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Formación: "
                    f"embriones={cantidad_embriones_disco}"
                    " | "
                    f"masa embriones={masa_embriones}"
                    " | "
                    f"planetesimales={masa_planetesimales}"
                ),
            )

            fila += 1

        sistema_binario = next(
            (
                sistema
                for sistema in self.universe.sistemas_estelares
                if sistema.obtener_tipo() == "binario"
            ),
            None,
        )

        if sistema_binario is not None:
            periodo = self._valor(
                sistema_binario.periodo_orbital_dias,
                "d",
                1,
            )

            semieje = self._valor(
                sistema_binario.semieje_mayor_au,
                "AU",
                3,
            )

            excentricidad = self._valor(
                sistema_binario.excentricidad,
                "",
                3,
            )

            periastro = self._valor(
                sistema_binario.obtener_periastro_au(),
                "AU",
                3,
            )

            apoastro = self._valor(
                sistema_binario.obtener_apoastro_au(),
                "AU",
                3,
            )

            escribir_seguro(
                stdscr,
                fila,
                0,
                (
                    "Órbita binaria: "
                    f"P={periodo}"
                    " | "
                    f"a={semieje}"
                    " | "
                    f"e={excentricidad}"
                ),
            )

            fila += 1

            escribir_seguro(
                stdscr,
                fila,
                0,
                ("Distancias: " f"periastro={periastro}" " | " f"apoastro={apoastro}"),
            )

            fila += 1

        linea_horizontal(
            stdscr,
            fila,
        )

        return fila + 1

    def _dibujar_estrellas(self, stdscr, fila):
        escribir_seguro(stdscr, fila, 0, "ESTRELLAS", curses.A_BOLD)

        fila += 1

        if not self.universe.estrellas:
            escribir_seguro(stdscr, fila, 2, "No hay estrellas activas.")

            fila += 1

        else:
            for estrella in self.universe.estrellas[:4]:
                temperatura = self._valor(estrella.temperatura_efectiva, "K", 0)

                masa = self._valor(estrella.masa_actual, "Msol", 3)

                escribir_seguro(
                    stdscr,
                    fila,
                    2,
                    (
                        f"* {estrella.nombre} | "
                        f"{estrella.obtener_etapa_visible()} | "
                        f"{masa} | "
                        f"{temperatura}"
                    ),
                )

                fila += 1

            restantes = len(self.universe.estrellas) - 4

            if restantes > 0:
                escribir_seguro(
                    stdscr, fila, 4, (f"... y {restantes} " "estrellas mas.")
                )

                fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_remanentes(self, stdscr, fila):
        escribir_seguro(stdscr, fila, 0, "REMANENTES", curses.A_BOLD)

        fila += 1

        if not self.universe.remanentes:
            escribir_seguro(stdscr, fila, 2, ("No hay remanentes " "estelares."))

            fila += 1

        else:
            for remanente in self.universe.remanentes[-3:]:
                escribir_seguro(
                    stdscr,
                    fila,
                    2,
                    (
                        f"+ {remanente.nombre} | "
                        f"{remanente.obtener_tipo_visible()} | "
                        f"{remanente.masa:.3f} "
                        "Msol"
                    ),
                )

                fila += 1

        linea_horizontal(stdscr, fila)

        return fila + 1

    def _dibujar_eventos(self, stdscr, fila, alto):
        escribir_seguro(stdscr, fila, 0, "EVENTOS", curses.A_BOLD)

        fila += 1

        espacio = max(1, alto - fila - 3)

        eventos = self.universe.event_manager.obtener_eventos()

        fin = max(0, len(eventos) - self.scroll_eventos)

        inicio = max(0, fin - espacio)

        visibles = eventos[inicio:fin]

        if not visibles:
            escribir_seguro(stdscr, fila, 2, "Todavia no hay eventos.")

            return

        for evento in visibles:
            escribir_seguro(stdscr, fila, 2, f"- {evento}")

            fila += 1

    def _numero_entero(self, valor):
        return f"{valor:,.0f}".replace(",", " ")

    def _valor(self, valor, unidad="", decimales=2):
        if valor is None:
            return "sin datos"

        texto = f"{valor:.{decimales}f}"

        if unidad:
            texto += f" {unidad}"

        return texto
