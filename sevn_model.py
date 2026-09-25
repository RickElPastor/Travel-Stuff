from pathlib import Path

from stellar_model import (
    EstadoEstelar,
    ModeloEvolutivoEstelar,
)


class ModeloSEVN(ModeloEvolutivoEstelar):
    nombre = "SEVN híbrido"

    ETAPAS_BSE = {
        0: "secuencia_principal_baja_masa",
        1: "secuencia_principal",
        2: "brecha_hertzsprung",
        3: "rama_gigante",
        4: "quema_helio_nucleo",
        5: "agb_temprana",
        6: "agb_pulsos_termicos",
        7: "helio_secuencia_principal",
        8: "helio_brecha_hertzsprung",
        9: "helio_rama_gigante",
        10: "enana_blanca_helio",
        11: "enana_blanca_carbono_oxigeno",
        12: "enana_blanca_oxigeno_neon",
        13: "estrella_de_neutrones",
        14: "agujero_negro",
        15: "remanente_sin_masa",
    }

    REMANENTES_BSE = {
        10: "enana_blanca_helio",
        11: "enana_blanca_carbono_oxigeno",
        12: "enana_blanca_oxigeno_neon",
        13: "estrella_de_neutrones",
        14: "agujero_negro",
    }

    PROPIEDADES = [
        "Worldtime",
        "Mass",
        "Radius",
        "Luminosity",
        "Temperature",
        "MHE",
        "MCO",
        "Phase",
        "PhaseBSE",
        "RemnantType",
    ]

    def __init__(
        self,
        modelo_supernova="rapid",
        ruta_parsec=None,
        ruta_mist_v25=None,
    ):
        from sevnpy.sevn import (
            SEVNmanager,
            Star as SEVNStar,
        )

        self._SEVNmanager = SEVNmanager
        self._SEVNStar = SEVNStar

        self.modelo_supernova = modelo_supernova

        if ruta_parsec is None:
            ruta_parsec = (
                Path.home()
                / "Documents"
                / "sevn"
                / "tables"
                / "SEVNtracks_parsec_ov05_AGB"
            )

        if ruta_mist_v25 is None:
            ruta_mist_v25 = (
                Path.home()
                / "Documents"
                / "sevn_external_tables"
                / ("SEVNtracks_MISTV2.5_" "a0.0_AGBnotpedantic")
            )

        self.configuraciones = {
            "parsec": {
                "ruta": Path(ruta_parsec),
                "parametros": {},
            },
            "mist_v25": {
                "ruta": Path(ruta_mist_v25),
                "parametros": {
                    "tabuse_rhe": False,
                    "tabuse_rco": False,
                },
            },
        }

        self.rangos = {}

        self._trayectorias = {}

        self._modelo_activo = None
        self._sesion_abierta = False

        self._validar_rutas()
        self._leer_rangos()

    def _validar_rutas(self):
        for nombre, configuracion in self.configuraciones.items():
            ruta = configuracion["ruta"]

            if not ruta.exists():
                raise FileNotFoundError(
                    f"No se encontraron las " f"tablas {nombre}: {ruta}"
                )

    def _leer_rangos(self):
        for nombre in self.configuraciones:
            self._activar_tablas(nombre)

            info = self._SEVNmanager.tables_info()

            self.rangos[nombre] = {
                "masa_minima": float(info["min_zams"]),
                "masa_maxima": float(info["max_zams"]),
                "z_minima": float(info["min_z"]),
                "z_maxima": float(info["max_z"]),
            }

        self.cerrar()

    def _activar_tablas(
        self,
        nombre,
    ):
        if self._sesion_abierta and self._modelo_activo == nombre:
            return

        if self._sesion_abierta:
            self._SEVNmanager.close()

            self._sesion_abierta = False
            self._modelo_activo = None

        configuracion = self.configuraciones[nombre]

        parametros = {"tables": str(configuracion["ruta"])}

        parametros.update(configuracion["parametros"])

        self._SEVNmanager.init(parametros)

        self._modelo_activo = nombre
        self._sesion_abierta = True

    def cerrar(self):
        if not self._sesion_abierta:
            return

        self._SEVNmanager.close()

        self._sesion_abierta = False
        self._modelo_activo = None

    def _esta_en_rango(
        self,
        nombre,
        masa_inicial,
        metalicidad_z,
    ):
        rango = self.rangos[nombre]

        return (
            rango["masa_minima"] <= masa_inicial <= rango["masa_maxima"]
            and rango["z_minima"] <= metalicidad_z <= rango["z_maxima"]
        )

    def seleccionar_modelo(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        if metalicidad_z == 0:
            return None

        # PARSEC sigue siendo nuestro
        # modelo principal siempre que
        # pueda representar la estrella.
        if self._esta_en_rango(
            "parsec",
            masa_inicial,
            metalicidad_z,
        ):
            return "parsec"

        # MIST v2.5 rellena especialmente
        # el hueco de baja masa.
        if self._esta_en_rango(
            "mist_v25",
            masa_inicial,
            metalicidad_z,
        ):
            return "mist_v25"

        return None

    def admite_estrella(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        return (
            self.seleccionar_modelo(
                masa_inicial,
                metalicidad_z,
            )
            is not None
        )

    def motivo_no_admitida(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        if metalicidad_z == 0:
            return "los modelos SEVN activos " "no contienen Z=0 exacta"

        masa_minima = min(rango["masa_minima"] for rango in self.rangos.values())

        masa_maxima = max(rango["masa_maxima"] for rango in self.rangos.values())

        if masa_inicial < masa_minima:
            return "masa menor que " f"{masa_minima:.3f} Msol"

        if masa_inicial > masa_maxima:
            return "masa mayor que " f"{masa_maxima:.3f} Msol"

        return (
            "la combinación de masa y "
            "metalicidad está fuera del "
            "dominio de las tablas activas"
        )

    def obtener_estado(
        self,
        masa_inicial,
        metalicidad_z,
        edad,
    ):
        if edad < 0:
            raise ValueError("La edad estelar no puede " "ser negativa.")

        modelo = self.seleccionar_modelo(
            masa_inicial,
            metalicidad_z,
        )

        if modelo is None:
            raise ValueError(
                self.motivo_no_admitida(
                    masa_inicial,
                    metalicidad_z,
                )
            )

        trayectoria = self._obtener_trayectoria(
            modelo,
            masa_inicial,
            metalicidad_z,
        )

        edad_myr = edad / 1_000_000

        indice = trayectoria["Worldtime"].searchsorted(
            edad_myr,
            side="right",
        ) - 1

        if indice < 0:
            indice = 0

        fila = trayectoria.iloc[indice]

        fase_bse = int(round(float(fila["PhaseBSE"])))

        etapa = self.ETAPAS_BSE.get(
            fase_bse,
            (f"fase_bse_" f"{fase_bse}"),
        )

        tipo_remanente = self.REMANENTES_BSE.get(fase_bse)

        viva = fase_bse <= 9

        masa_actual = float(fila["Mass"])

        if tipo_remanente is None:
            masa_remanente = None

        else:
            masa_remanente = masa_actual

        return EstadoEstelar(
            masa_actual=masa_actual,
            etapa=etapa,
            viva=viva,
            edad_modelo_anios=(float(fila["Worldtime"]) * 1_000_000),
            temperatura_efectiva=float(fila["Temperature"]),
            luminosidad=float(fila["Luminosity"]),
            radio=float(fila["Radius"]),
            masa_nucleo_helio=float(fila["MHE"]),
            masa_nucleo_carbono_oxigeno=float(fila["MCO"]),
            tipo_espectral=None,
            tipo_remanente=(tipo_remanente),
            masa_remanente=(masa_remanente),
        )

    def _obtener_trayectoria(
        self,
        modelo,
        masa_inicial,
        metalicidad_z,
    ):
        clave = (
            modelo,
            float(masa_inicial),
            float(metalicidad_z),
            self.modelo_supernova,
        )

        if clave in self._trayectorias:
            return self._trayectorias[clave]

        self._activar_tablas(modelo)

        estrella = self._SEVNStar(
            Mzams=masa_inicial,
            Z=metalicidad_z,
            tini="zams",
            snmodel=(self.modelo_supernova),
        )

        estrella.evolve()

        trayectoria = estrella.getp(self.PROPIEDADES)

        self._trayectorias[clave] = trayectoria

        return trayectoria

    def obtener_rangos(self):
        return {nombre: dict(rango) for nombre, rango in self.rangos.items()}
