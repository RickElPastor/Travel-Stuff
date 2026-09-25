from bisect import bisect_right
import csv
import json
import math
from pathlib import Path

from stellar_model import (
    EstadoEstelar,
    ModeloEvolutivoEstelar,
)


class ModeloHassanPopIII(ModeloEvolutivoEstelar):
    nombre = "Hassan Pop III MESA ratesfix"

    MASA_REFERENCIA = 50.0
    Z_REFERENCIA = 0.0

    COLUMNAS_INTERPOLABLES = [
        "star_age",
        "star_mass",
        "log_L",
        "Teff",
        "radius",
        "he_core_mass",
        "co_core_mass",
        "fe_core_mass",
    ]

    def __init__(
        self,
        ruta_csv=None,
        ruta_hitos=None,
    ):
        carpeta_datos = Path(__file__).parent / "data" / "stellar_tracks" / "popiii"

        if ruta_csv is None:
            ruta_csv = carpeta_datos / "hassan_50_omega020.csv"

        if ruta_hitos is None:
            ruta_hitos = carpeta_datos / "hassan_50_omega020_milestones.json"

        self.ruta_csv = Path(ruta_csv)
        self.ruta_hitos = Path(ruta_hitos)

        self._validar_archivos()

        self._filas = self._leer_csv()

        self._edades = [fila["star_age"] for fila in self._filas]

        self._validar_edades()

        self._edades_hitos = self._leer_edades_hitos()

    def _validar_archivos(self):
        if not self.ruta_csv.exists():
            raise FileNotFoundError(f"No existe el track Hassan: " f"{self.ruta_csv}")

        if not self.ruta_hitos.exists():
            raise FileNotFoundError(
                f"No existe el archivo de hitos: " f"{self.ruta_hitos}"
            )

    def _leer_csv(self):
        filas = []

        with open(
            self.ruta_csv,
            "r",
            encoding="utf-8",
        ) as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                fila_convertida = {}

                for clave, valor in fila.items():
                    if clave == "model_number":
                        fila_convertida[clave] = int(valor)
                    else:
                        fila_convertida[clave] = float(valor)

                filas.append(fila_convertida)

        if not filas:
            raise ValueError("El track Hassan está vacío.")

        return filas

    def _validar_edades(self):
        for indice in range(
            1,
            len(self._edades),
        ):
            if self._edades[indice] < self._edades[indice - 1]:
                raise ValueError("Las edades del track Hassan " "no están ordenadas.")

    def _leer_edades_hitos(self):
        with open(
            self.ruta_hitos,
            "r",
            encoding="utf-8",
        ) as archivo:
            datos = json.load(archivo)

        hitos = datos["milestones"]

        return {
            nombre: float(informacion["star_age"])
            for nombre, informacion in hitos.items()
        }

    def admite_estrella(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        masa_correcta = math.isclose(
            float(masa_inicial),
            self.MASA_REFERENCIA,
            rel_tol=0.0,
            abs_tol=1e-9,
        )

        z_correcta = float(metalicidad_z) == self.Z_REFERENCIA

        return masa_correcta and z_correcta

    def motivo_no_admitida(
        self,
        masa_inicial,
        metalicidad_z,
    ):
        if float(metalicidad_z) != 0.0:
            return "Hassan Pop III solo representa " "Z=0 exacta"

        if not math.isclose(
            float(masa_inicial),
            self.MASA_REFERENCIA,
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            return "por ahora solo existe un track " "Hassan validado de 50 Msol"

        return "estrella admitida"

    def obtener_estado(
        self,
        masa_inicial,
        metalicidad_z,
        edad,
    ):
        if edad < 0:
            raise ValueError("La edad estelar no puede " "ser negativa.")

        if not self.admite_estrella(
            masa_inicial,
            metalicidad_z,
        ):
            raise ValueError(
                self.motivo_no_admitida(
                    masa_inicial,
                    metalicidad_z,
                )
            )

        edad_colapso = self._edades_hitos["core_collapse"]

        if edad >= edad_colapso:
            fila = self._filas[-1]

            etapa = "colapso_nucleo"
            viva = False
            edad_modelo = edad_colapso

        else:
            fila = self._interpolar(edad)

            etapa = self._obtener_etapa(edad)
            viva = True
            edad_modelo = max(
                edad,
                self._edades[0],
            )

        luminosidad = 10 ** fila["log_L"]

        return EstadoEstelar(
            masa_actual=fila["star_mass"],
            etapa=etapa,
            viva=viva,
            edad_modelo_anios=edad_modelo,
            temperatura_efectiva=fila["Teff"],
            luminosidad=luminosidad,
            radio=fila["radius"],
            masa_nucleo_helio=(fila["he_core_mass"]),
            masa_nucleo_carbono_oxigeno=(fila["co_core_mass"]),
            tipo_espectral=None,
            # Hassan termina en colapso.
            # El remanente se añadirá después
            # desde el modelo de explosión.
            tipo_remanente=None,
            masa_remanente=None,
        )

    def _interpolar(self, edad):
        if edad <= self._edades[0]:
            return dict(self._filas[0])

        if edad >= self._edades[-1]:
            return dict(self._filas[-1])

        indice_derecho = bisect_right(
            self._edades,
            edad,
        )

        fila_a = self._filas[indice_derecho - 1]

        fila_b = self._filas[indice_derecho]

        edad_a = fila_a["star_age"]
        edad_b = fila_b["star_age"]

        if edad_b == edad_a:
            return dict(fila_b)

        fraccion = (edad - edad_a) / (edad_b - edad_a)

        resultado = dict(fila_a)

        for columna in self.COLUMNAS_INTERPOLABLES:
            valor_a = fila_a[columna]
            valor_b = fila_b[columna]

            resultado[columna] = valor_a + (valor_b - valor_a) * fraccion

        resultado["star_age"] = edad

        return resultado

    def _obtener_etapa(self, edad):
        hitos = self._edades_hitos

        if edad < hitos["zams"]:
            return "pre_zams"

        if edad < hitos["iams"]:
            return "secuencia_principal"

        if edad < hitos["end_core_h"]:
            return "secuencia_principal_tardia"

        if edad < hitos["end_core_he"]:
            return "quema_helio_nucleo"

        if edad < hitos["end_core_c"]:
            return "quema_carbono_nucleo"

        if edad < hitos["core_collapse"]:
            return "quemado_avanzado"

        return "colapso_nucleo"

    def obtener_hitos(self):
        return dict(self._edades_hitos)
