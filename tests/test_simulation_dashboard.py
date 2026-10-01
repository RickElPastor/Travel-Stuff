import curses
import tempfile
import unittest

from planets.planet import Planet
from planets.local_calendar import fecha_local, periodo_orbital_dias
from stars.star import Star
from stars.systems.stellar_system import SistemaEstelar
from universe.save_manager import SaveManager
from universe.events import Event
from universe.simulation import Simulation
from universe.universe import Universe
from universe.world_time import Time
from ui.simulation_ui import SimulationUI


class PantallaFalsa:
    def __init__(self, alto=24, ancho=72, teclas=None):
        self.alto = alto
        self.ancho = ancho
        self.teclas = list(teclas or [])
        self.erase()

    def getmaxyx(self):
        return self.alto, self.ancho

    def erase(self):
        self.filas = [[" "] * self.ancho for _ in range(self.alto)]

    def addnstr(self, y, x, valor, limite, atributo=0):
        for indice, letra in enumerate(str(valor)[:limite]):
            if x + indice < self.ancho:
                self.filas[y][x + indice] = letra

    def refresh(self):
        pass

    def nodelay(self, valor):
        self.sin_espera = valor

    def getch(self):
        return self.teclas.pop(0)

    def linea(self, numero):
        return "".join(self.filas[numero]).rstrip()


class ExploradorTests(unittest.TestCase):
    def crear_universo(self):
        universo = Universe(seed=73)
        alfa = SistemaEstelar("Sistema Alfa", 100, estrellas=["Alfa"],
                              estrella_primaria="Alfa")
        beta = SistemaEstelar("Sistema Beta", 200, estrellas=["Beta"],
                              estrella_primaria="Beta")
        universo.sistemas_estelares = [alfa, beta]
        universo.estrellas = [Star("Alfa", 1, 0.01)]
        planeta = Planet(
            "Mundo Beta", 1.5, 1.2, sistema_nombre="Sistema Beta",
            estrella_anfitriona="Beta", estado_agua_preclima="liquida",
            estado_habitabilidad_fase1="candidato_temperado",
            alcanzo_protocelula=True, vida_activa=True,
            poblacion_unicelular=1, rasgos_unicelulares_vivos=[1],
            linajes_unicelulares_vivos=[1], linaje_observado_id=1,
        )
        universo.planetas = [planeta]
        beta.agregar_planeta(planeta)
        return universo

    def test_empieza_en_universo_y_las_teclas_antiguas_no_cambian_vista(self):
        universo = self.crear_universo()
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("EXPLORADOR DEL UNIVERSO", pantalla.linea(1))
        self.assertIn("Sistemas 2", pantalla.linea(8))
        self.assertIn("Planetas formados 1", pantalla.linea(9))
        self.assertIn("Las galaxias aún no están modeladas", pantalla.linea(20))
        interfaz._procesar_tecla(pantalla, ord("5"))
        self.assertEqual(interfaz._actual()["tipo"], "universo")
        self.assertIn("Esc Menú", pantalla.linea(23))
        self.assertTrue(interfaz._procesar_tecla(pantalla, 27))

    def test_buscar_sistema_planeta_y_restaurar_velocidad_al_volver(self):
        universo = self.crear_universo()
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        antes = universo.planetas[0].a_dict()
        azar_antes = universo.random.getstate()

        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("Resultados 2", pantalla.linea(8))
        self.assertIn("Sistema Alfa", pantalla.linea(10))
        self.assertIn("Sistema Beta", pantalla.linea(11))
        pantalla.teclas = [ord(letra) for letra in "Beta"] + [10]
        interfaz._procesar_tecla(pantalla, ord("/"))
        interfaz._dibujar(pantalla)
        self.assertIn("Resultados 1", pantalla.linea(8))
        self.assertIn("Sistema Beta", pantalla.linea(10))

        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("SISTEMA ESTELAR", pantalla.linea(6))
        self.assertIn("Planetas registrados: 1", pantalla.linea(12))
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("CATÁLOGO DE PLANETAS", pantalla.linea(6))
        self.assertIn("Mundo Beta", pantalla.linea(10))
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("PLANETA", pantalla.linea(6))
        self.assertIn("Masa 1.50", pantalla.linea(9))
        self.assertIn("Vida: activa · población 1", pantalla.linea(17))
        self.assertEqual(universo.time.escala, "planeta")
        self.assertEqual(universo.time.obtener_velocidad_actual(), 1)
        interfaz._procesar_tecla(pantalla, ord("+"))
        self.assertEqual(universo.time.obtener_velocidad_actual(), 2)
        self.assertEqual(universo.planetas[0].a_dict(), antes)
        self.assertEqual(universo.random.getstate(), azar_antes)
        self.assertFalse(interfaz._procesar_tecla(pantalla, 27))
        self.assertEqual(universo.time.escala, "universo")
        self.assertEqual(universo.time.obtener_velocidad_actual(), 1)
        self.assertEqual(interfaz._actual()["tipo"], "planetas")

    def test_estrellas_incluye_nombres_historicos_y_abre_su_sistema(self):
        interfaz = SimulationUI(Simulation(self.crear_universo()))
        pantalla = PantallaFalsa()
        interfaz._procesar_tecla(pantalla, ord("e"))
        interfaz._dibujar(pantalla)
        self.assertIn("Resultados 2", pantalla.linea(8))
        self.assertIn("Alfa · activa", pantalla.linea(10))
        self.assertIn("Beta · sin estado estelar actual", pantalla.linea(11))
        interfaz._procesar_tecla(pantalla, curses.KEY_DOWN)
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("Beta", pantalla.linea(8))
        self.assertIn("Sistema Beta", pantalla.linea(9))
        interfaz._procesar_tecla(pantalla, 10)
        self.assertEqual(interfaz._actual()["objeto"].nombre, "Sistema Beta")

    def test_lista_larga_pagina_y_filtro_sin_resultados(self):
        universo = self.crear_universo()
        universo.sistemas_estelares += [
            SistemaEstelar(f"Sistema {n:02d}", 0) for n in range(30)
        ]
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._procesar_tecla(pantalla, curses.KEY_NPAGE)
        interfaz._dibujar(pantalla)
        self.assertIn("Resultados 32", pantalla.linea(8))
        self.assertIn("selección 11", pantalla.linea(8))
        pantalla.teclas = [ord(letra) for letra in "No existe"] + [10]
        interfaz._procesar_tecla(pantalla, ord("/"))
        interfaz._dibujar(pantalla)
        self.assertIn("Resultados 0", pantalla.linea(8))
        self.assertIn("Sin resultados", pantalla.linea(11))

    def test_catalogo_vacio_explicado_sin_filtro(self):
        interfaz = SimulationUI(Simulation(Universe(seed=1)))
        pantalla = PantallaFalsa()
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("Aún no hay sistemas registrados", pantalla.linea(11))

    def test_escala_planeta_persiste_al_guardar_y_cargar(self):
        universo = self.crear_universo()
        interfaz = SimulationUI(Simulation(universo))
        interfaz._abrir("planeta", universo.planetas[0])
        interfaz._procesar_tecla(PantallaFalsa(), ord("+"))
        with tempfile.TemporaryDirectory() as carpeta:
            gestor = SaveManager(carpeta)
            gestor.guardar(universo, "tiempo")
            cargado = gestor.cargar("tiempo")
        self.assertEqual(cargado.time.escala, "planeta")
        self.assertEqual(cargado.time.obtener_velocidad_actual(), 2)
        self.assertEqual(cargado.planetas[0].a_dict(), universo.planetas[0].a_dict())
        nueva_interfaz = SimulationUI(Simulation(cargado))
        self.assertEqual(nueva_interfaz._actual()["tipo"], "universo")
        self.assertEqual(cargado.time.escala, "universo")
        self.assertEqual(cargado.time.obtener_velocidad_actual(), 1)

    def test_tiempo_planeta_no_avanza_millones_en_un_refresco(self):
        tiempo = Time()
        tiempo.establecer_escala("planeta")
        tiempo.indice_velocidad = 3
        self.assertEqual(tiempo.obtener_velocidad_actual(), 3)
        tiempo.indice_velocidad = len(tiempo.velocidades_planeta) - 1
        self.assertEqual(tiempo.obtener_velocidad_actual(), 10_000)
        self.assertEqual(tiempo.avanzar(0.02), 200)
        self.assertEqual(tiempo.anio, 200)

    def test_fecha_local_usa_el_mismo_reloj_y_orbita_del_planeta(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.anio_formacion = 0
        planeta.periodo_orbital_dias = 1_000
        interfaz = SimulationUI(Simulation(universo))
        interfaz._abrir("planeta", planeta)
        self.assertEqual(universo.time.obtener_velocidad_actual(), 1)
        self.assertEqual(fecha_local(planeta, universo.time), (0, 1, 1, 0, 0, 0))
        universo.time.avanzar(0.5)
        self.assertEqual(universo.time.anio, 0)
        self.assertGreater(fecha_local(planeta, universo.time)[2], 1)
        universo.time.anio = 2
        self.assertEqual(fecha_local(planeta, universo.time)[0], 0)
        universo.time.anio = 3
        self.assertEqual(fecha_local(planeta, universo.time)[0], 1)
        self.assertAlmostEqual(periodo_orbital_dias(1, 1), 365.2425)
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("Año orbital: 1000.00", pantalla.linea(19))
        self.assertIn("Año 1", pantalla.linea(20))
        self.assertIn("Hora", pantalla.linea(21))
        self.assertIn("x1", universo.time.obtener_descripcion_velocidad())

    def test_x1_universo_y_planeta_avanzan_al_mismo_ritmo_real(self):
        universo = Universe(seed=7)
        reloj = [0.0]
        simulacion = Simulation(universo, reloj=lambda: reloj[0])
        for _ in range(20):
            reloj[0] += 0.05
            simulacion.actualizar()
        self.assertEqual(universo.time.anio, 1)
        universo.time.establecer_escala("planeta")
        for _ in range(20):
            reloj[0] += 0.05
            simulacion.actualizar()
        self.assertEqual(universo.time.anio, 2)

    def test_biosfera_muestra_fuente_ruta_y_ecosistema(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.candidato_quimica_prebiotica = True
        planeta.alcanzo_organicos_simples = True
        universo.actualizar_metabolismo_inicial()
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._abrir("planeta", planeta)
        interfaz._dibujar(pantalla)
        self.assertIn("Metabolismo: consumo organicos", pantalla.linea(11))
        self.assertIn("M Biosfera", pantalla.linea(23))
        interfaz._procesar_tecla(pantalla, ord("m"))
        interfaz._dibujar(pantalla)
        self.assertIn("BIOSFERA", pantalla.linea(6))
        self.assertIn("organicos ambientales", pantalla.linea(11))
        self.assertIn("consumo organicos", pantalla.linea(13))
        self.assertIn("microbiano organicos ambientales", pantalla.linea(14))
        interfaz._procesar_tecla(pantalla, 27)
        self.assertEqual(interfaz._actual()["tipo"], "planeta")
        self.assertEqual(universo.time.escala, "planeta")

    def test_biosfera_muestra_productores_del_linaje_activo(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.irradiancia_media_w_m2 = 1000
        planeta.presion_co2_preclima_bar = 0.1
        planeta.candidato_quimica_prebiotica = True
        planeta.alcanzo_organicos_simples = True
        planeta.linajes_fotosinteticos = {1}
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_atmosfera_biologica()
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(pantalla, ord("m"))
        interfaz._dibujar(pantalla)
        self.assertIn("productor y consumidor", pantalla.linea(14))
        self.assertIn("Productores fotosintéticos: 1", pantalla.linea(15))
        self.assertIn("Luz → productores", pantalla.linea(16))
        self.assertIn("CO₂ físico 0.1 → con vida 0.099 bar", pantalla.linea(19))
        self.assertIn("Aporte de O₂: 0.001 bar", pantalla.linea(20))
        interfaz._procesar_tecla(pantalla, ord("v"))
        self.assertEqual(interfaz._actual()["tipo"], "eventos")

    def test_biosfera_muestra_reciclaje_con_restos_recientes(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.candidato_quimica_prebiotica = True
        planeta.alcanzo_organicos_simples = True
        planeta.linajes_descomponedores = {1}
        planeta.alcanzo_capacidad_descomponedora = True
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion({planeta: 1})
        planeta.restos_organicos_unidades = 2
        planeta.nutrientes_reciclados_unidades = 1
        planeta.total_nutrientes_aprovechados = 3
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(pantalla, ord("m"))
        interfaz._dibujar(pantalla)
        self.assertIn("con reciclaje", pantalla.linea(14))
        self.assertIn("descomponedores: 1 activos", pantalla.linea(17))
        self.assertIn("restos 2 · nutrientes 1 · usados 3", pantalla.linea(10))

    def test_biosfera_muestra_colonias_activas_e_historicas(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.poblacion_unicelular = 2
        planeta.linajes_unicelulares_vivos = [1, 1]
        planeta.linajes_cohesivos = {1}
        planeta.candidato_quimica_prebiotica = True
        planeta.alcanzo_organicos_simples = True
        universo.actualizar_colonias_celulares()
        interfaz = SimulationUI(Simulation(universo))
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(PantallaFalsa(), ord("m"))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("Colonias simples: 1", pantalla.linea(12))
        self.assertIn("históricas sí", pantalla.linea(12))
        planeta.vida_activa = False
        universo.actualizar_colonias_celulares()
        interfaz._dibujar(pantalla)
        self.assertIn("Colonias simples: 0", pantalla.linea(12))
        self.assertIn("históricas sí", pantalla.linea(12))

    def test_biosfera_resume_nichos_de_especies_vivas(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.candidato_quimica_prebiotica = True
        planeta.alcanzo_organicos_simples = True
        planeta.irradiancia_media_w_m2 = 1000
        planeta.presion_co2_preclima_bar = 0.1
        planeta.linajes_fotosinteticos = {1}
        planeta.linajes_descomponedores = {1}
        planeta.restos_organicos_unidades = 1
        universo.actualizar_metabolismo_inicial()
        universo.actualizar_descomposicion({planeta: 0})
        interfaz = SimulationUI(Simulation(universo))
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(PantallaFalsa(), ord("m"))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("org 1 · luz 1 · restos 1 · presas 0 · sin ruta 0",
                      pantalla.linea(7))

    def test_biosfera_muestra_presas_y_ultima_captura(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.poblacion_unicelular = 2
        planeta.linajes_unicelulares_vivos = [1, 2]
        planeta.clasificacion_especies_unicelulares[2] = {
            "especie_id": 2, "distancia": 0,
        }
        planeta.linajes_depredadores = {1}
        planeta.capturas_depredacion = 1
        planeta.ultima_especie_predadora_id = 1
        planeta.ultima_especie_presa_id = 2
        interfaz = SimulationUI(Simulation(universo))
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(PantallaFalsa(), ord("m"))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("presas 1", pantalla.linea(7))
        self.assertIn("Capturas: 1 · última: especie 1 → especie 2",
                      pantalla.linea(21))

    def test_red_trofica_se_abre_y_recorre_todas_las_relaciones(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.poblacion_unicelular = 5
        planeta.linajes_unicelulares_vivos = [1, 2, 3, 4, 5]
        planeta.clasificacion_especies_unicelulares = {
            numero: {"especie_id": numero, "distancia": 0}
            for numero in range(1, 6)
        }
        planeta.fuentes_energia_potenciales = ["organicos_ambientales"]
        planeta.linajes_depredadores = {1, 2}
        estado_antes = planeta.a_dict()
        azar_antes = universo.random.getstate()
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._abrir("planeta", planeta)
        interfaz._procesar_tecla(pantalla, ord("m"))
        interfaz._dibujar(pantalla)
        self.assertIn("R Red trófica", pantalla.linea(23))
        interfaz._procesar_tecla(pantalla, ord("r"))
        interfaz._dibujar(pantalla)
        self.assertIn("RED TRÓFICA", pantalla.linea(6))
        self.assertIn("recursos 5 · presas posibles 8", pantalla.linea(8))
        self.assertIn("Orgánicos → especie 1", pantalla.linea(11))
        self.assertIn("Mostrando 1-10 de 13", pantalla.linea(21))
        interfaz._procesar_tecla(pantalla, curses.KEY_NPAGE)
        interfaz._dibujar(pantalla)
        self.assertIn("Mostrando 4-13 de 13", pantalla.linea(21))
        self.assertIn("Especie 5 → especie 2 · captura posible", pantalla.linea(20))
        interfaz._procesar_tecla(pantalla, 27)
        self.assertEqual(interfaz._actual()["tipo"], "biosfera")
        interfaz._procesar_tecla(pantalla, 27)
        self.assertEqual(universo.time.escala, "planeta")
        self.assertEqual(planeta.a_dict(), estado_antes)
        self.assertEqual(universo.random.getstate(), azar_antes)

    def test_red_trofica_vacia_explica_ausencia_de_vida(self):
        universo = self.crear_universo()
        universo.planetas[0].vida_activa = False
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._abrir("planeta", universo.planetas[0])
        interfaz._procesar_tecla(pantalla, ord("m"))
        interfaz._procesar_tecla(pantalla, ord("r"))
        interfaz._dibujar(pantalla)
        self.assertIn("Sin relaciones tróficas actuales", pantalla.linea(12))

    def test_universo_y_planeta_muestran_extinciones_masivas_locales(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.extinciones_masivas_locales = 2
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("Extinciones masivas locales 2", pantalla.linea(13))
        interfaz._abrir("planeta", planeta)
        interfaz._dibujar(pantalla)
        self.assertIn("ext. masivas 2", pantalla.linea(18))

    def test_universo_y_planeta_muestran_radiaciones_evolutivas(self):
        universo = self.crear_universo()
        planeta = universo.planetas[0]
        planeta.ancestros_con_radiacion = {1, 9}
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("Radiaciones 2", pantalla.linea(13))
        interfaz._abrir("planeta", planeta)
        interfaz._dibujar(pantalla)
        self.assertIn("radiaciones 2", pantalla.linea(18))

    def test_eventos_filtrados_y_guardados(self):
        universo = self.crear_universo()
        gestor = universo.event_manager
        gestor.agregar_evento("Origen", 100, "Surgió Alfa.", "estrella", "Alfa")
        gestor.agregar_evento("Origen", 200, "Surgió Mundo Beta.",
                             "planeta", "Mundo Beta")
        interfaz = SimulationUI(Simulation(universo))
        pantalla = PantallaFalsa()
        interfaz._dibujar(pantalla)
        self.assertIn("Surgió Mundo Beta", pantalla.linea(15))
        self.assertNotIn("Enter: buscar", pantalla.linea(15))
        interfaz._procesar_tecla(pantalla, ord("v"))
        self.assertEqual(len(interfaz._items(interfaz._actual())), 3)
        interfaz._procesar_tecla(pantalla, 27)
        interfaz._abrir("estrella", "Alfa")
        interfaz._procesar_tecla(pantalla, ord("v"))
        self.assertEqual(len(interfaz._items(interfaz._actual())), 1)
        interfaz._procesar_tecla(pantalla, 27)
        interfaz._procesar_tecla(pantalla, 27)
        interfaz._abrir("planeta", universo.planetas[0])
        interfaz._procesar_tecla(pantalla, ord("v"))
        self.assertEqual(len(interfaz._items(interfaz._actual())), 1)
        interfaz._procesar_tecla(pantalla, 10)
        interfaz._dibujar(pantalla)
        self.assertIn("Surgió Mundo Beta", pantalla.linea(12))
        with tempfile.TemporaryDirectory() as carpeta:
            archivos = SaveManager(carpeta)
            archivos.guardar(universo, "eventos")
            cargado = archivos.cargar("eventos")
        self.assertEqual([e.a_dict() for e in cargado.event_manager.eventos],
                         [e.a_dict() for e in gestor.eventos])
        antiguo = Event.desde_dict({"tipo": "antiguo", "anio": 1,
                                   "mensaje": "Evento sin ámbito."})
        self.assertEqual(antiguo.ambito, "universo")
        self.assertIsNone(antiguo.entidad)


if __name__ == "__main__":
    unittest.main()
