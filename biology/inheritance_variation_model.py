import random

from biology.selection_model import ModeloSeleccionUnicelular
from biology.species_model import ModeloEspeciesUnicelulares
from biology.metabolism_model import ModeloMetabolismoInicial
from biology.decomposition_model import ModeloDescomposicionMicrobiana
from biology.material_cycle_model import ModeloCicloOrganico
from biology.colony_model import ModeloColoniasCelulares
from biology.predation_model import ModeloDepredacion
from biology.evolutionary_radiation_model import ModeloRadiacionesEvolutivas


class ModeloHerenciaVariacionUnicelular:
    """Sigue rasgos e identidades de linaje de las unidades vivas."""

    RASGO_INICIAL = 1
    PROBABILIDAD_VARIACION = 0.25  # Parámetro de diseño, no tasa medida.

    def __init__(self):
        self.seleccion = ModeloSeleccionUnicelular()
        self.especies = ModeloEspeciesUnicelulares()
        self.metabolismo = ModeloMetabolismoInicial()
        self.descomposicion = ModeloDescomposicionMicrobiana()
        self.ciclo_organico = ModeloCicloOrganico()
        self.colonias = ModeloColoniasCelulares()
        self.depredacion = ModeloDepredacion()
        self.radiaciones = ModeloRadiacionesEvolutivas()

    def evaluar(self, planeta, seed):
        nacimientos = planeta.nacimientos_unicelulares
        if planeta.poblacion_unicelular == 0:
            planeta.rasgo_linea_unicelular = None
            planeta.rasgos_unicelulares_vivos = []
            planeta.linajes_unicelulares_vivos = []
            planeta.linaje_observado_id = None
            planeta.nacimientos_biologicos_procesados = nacimientos
            return

        if planeta.rasgo_linea_unicelular is None:
            # La fundadora inicia una línea nueva; no es una mutación.
            planeta.rasgo_linea_unicelular = self.RASGO_INICIAL
            if (planeta.poblacion_unicelular == 1
                    and not planeta.rasgos_unicelulares_vivos):
                planeta.rasgos_unicelulares_vivos = [self.RASGO_INICIAL]
                planeta.linajes_unicelulares_vivos = [nacimientos]
                planeta.linaje_observado_id = nacimientos
                planeta.historial_linajes_unicelulares[nacimientos] = {
                    "progenitor_id": None,
                    "rasgo": self.RASGO_INICIAL,
                    "origen": "fundacion",
                }
                self.especies.clasificar_linaje(planeta, nacimientos)
                planeta.nacimientos_biologicos_procesados = nacimientos
                return

        self._mantener_linea_viva(planeta)
        primero = planeta.nacimientos_biologicos_procesados + 1
        while primero <= nacimientos:
            # Reconstruye cada intervalo del modelo de población: un nacimiento
            # en la fundación o a capacidad; dos mientras crece y hay reemplazo.
            cantidad_viva = len(planeta.rasgos_unicelulares_vivos)
            especies_antes = self.especies.especies_vivas(planeta)
            crece = cantidad_viva < planeta.poblacion_unicelular
            cantidad_nacimientos = 2 if crece and cantidad_viva > 1 else 1
            cantidad_final = cantidad_viva + 1 if crece else cantidad_viva
            fin = min(primero + cantidad_nacimientos, nacimientos + 1)
            for numero in range(primero, fin):
                self._registrar_nacimiento(planeta, seed, numero)

            # La captura sustituye una muerte del recambio normal; no añade
            # muertes ni cambia el tamaño total previsto por la población.
            captura = None
            if cantidad_viva > 1:
                captura = self.depredacion.elegir_captura(
                    planeta, seed, fin - 1, cantidad_viva
                )
            if captura is None:
                planeta.rasgos_unicelulares_vivos = (
                    planeta.rasgos_unicelulares_vivos[-cantidad_final:]
                )
                planeta.linajes_unicelulares_vivos = (
                    planeta.linajes_unicelulares_vivos[-cantidad_final:]
                )
            else:
                self.depredacion.registrar_captura(planeta, captura)
                indice_presa = captura[2]
                del planeta.rasgos_unicelulares_vivos[indice_presa]
                del planeta.linajes_unicelulares_vivos[indice_presa]
            self._mantener_linea_viva(planeta)
            # La ecología sigue cada intervalo reconstruido, incluso cuando
            # varios intervalos se evaluaron en un solo salto temporal.
            muertes_intervalo = 1 if cantidad_viva > 1 else 0
            self.ciclo_organico.procesar_intervalo(
                planeta, muertes_intervalo, 1 if captura is not None else 0
            )
            self.colonias.registrar_intervalo(planeta)
            # Solo una especie nueva que sobreviva al recambio puede completar
            # una ramificación; los saltos largos recorren los mismos intervalos.
            self.radiaciones.registrar_intervalo(planeta, especies_antes)
            primero = fin

        planeta.nacimientos_biologicos_procesados = nacimientos

    def _mantener_linea_viva(self, planeta):
        if planeta.linaje_observado_id not in planeta.linajes_unicelulares_vivos:
            # Si desaparece la línea observada, seguimos la unidad más reciente.
            # No es una comparación ambiental ni cuenta como variante favorecida.
            planeta.linaje_observado_id = planeta.linajes_unicelulares_vivos[-1]
        indice = planeta.linajes_unicelulares_vivos.index(planeta.linaje_observado_id)
        planeta.rasgo_linea_unicelular = planeta.rasgos_unicelulares_vivos[indice]

    def _registrar_nacimiento(self, planeta, seed, numero):
        # Compara los linajes existentes solo cuando hay un nacimiento nuevo.
        planeta.linaje_observado_id = self.seleccion.elegir_linaje_reproductor(planeta)
        indice = planeta.linajes_unicelulares_vivos.index(planeta.linaje_observado_id)
        planeta.rasgo_linea_unicelular = planeta.rasgos_unicelulares_vivos[indice]
        rasgo_nacido = planeta.rasgo_linea_unicelular
        linaje_nacido = planeta.linaje_observado_id
        generador = random.Random(
            f"{seed}:{planeta.sistema_nombre}:{planeta.nombre}:bio:{numero}"
        )
        if generador.random() < self.PROBABILIDAD_VARIACION:
            desplazamiento = 1 + generador.randrange(2)
            anterior = planeta.rasgo_linea_unicelular
            variante = (anterior + desplazamiento) % 3
            rasgo_nacido = variante
            linaje_nacido = numero
            # El progenitor es el elegido para reproducir antes de esta variante.
            planeta.historial_linajes_unicelulares[numero] = {
                "progenitor_id": planeta.linaje_observado_id,
                "rasgo": variante,
                "origen": "variacion",
            }
            capacidad_nueva = self.metabolismo.adquiere_fotosintesis(
                planeta, seed, numero
            )
            hereda_capacidad = (
                planeta.linaje_observado_id in planeta.linajes_fotosinteticos
            )
            if hereda_capacidad or capacidad_nueva:
                planeta.linajes_fotosinteticos.add(numero)
            if capacidad_nueva:
                planeta.alcanzo_fotosintesis = True
            capacidad_descomponedora = self.descomposicion.adquiere_capacidad(
                planeta, seed, numero
            )
            hereda_descomposicion = (
                planeta.linaje_observado_id in planeta.linajes_descomponedores
            )
            if hereda_descomposicion or capacidad_descomponedora:
                planeta.linajes_descomponedores.add(numero)
            if capacidad_descomponedora:
                planeta.alcanzo_capacidad_descomponedora = True
            nueva_cohesion = self.colonias.adquiere_cohesion(
                planeta, seed, numero
            )
            if (planeta.linaje_observado_id in planeta.linajes_cohesivos
                    or nueva_cohesion):
                planeta.linajes_cohesivos.add(numero)
            nueva_depredacion = self.depredacion.adquiere_capacidad(
                planeta, seed, numero
            )
            if (planeta.linaje_observado_id in planeta.linajes_depredadores
                    or nueva_depredacion):
                planeta.linajes_depredadores.add(numero)
            self.especies.clasificar_linaje(planeta, numero)
            planeta.variaciones_unicelulares += 1
            planeta.rasgo_linea_unicelular = self.seleccion.elegir(
                planeta, anterior, variante
            )
            if planeta.rasgo_linea_unicelular == variante:
                planeta.linaje_observado_id = numero
        planeta.rasgos_unicelulares_vivos.append(rasgo_nacido)
        planeta.linajes_unicelulares_vivos.append(linaje_nacido)
