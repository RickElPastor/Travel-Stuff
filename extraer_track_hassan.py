from pathlib import Path
import csv
import json


HISTORY_PATH = (
    Path.home()
    / "Documents"
    / "popiii_models"
    / "hassan_mesa"
    / "run_50_omega020_ratesfix"
    / "LOGS"
    / "history.data"
)

OUTPUT_DIR = Path(__file__).parent / "data" / "stellar_tracks" / "popiii"

CSV_PATH = OUTPUT_DIR / "hassan_50_omega020.csv"
JSON_PATH = OUTPUT_DIR / "hassan_50_omega020_milestones.json"


COLUMNAS_GUARDADAS = [
    "model_number",
    "star_age",
    "star_mass",
    "log_L",
    "Teff",
    "radius",
    "log_R",
    "log_center_T",
    "log_center_Rho",
    "center_h1",
    "center_he4",
    "center_c12",
    "center_o16",
    "surface_h1",
    "surface_he4",
    "he_core_mass",
    "co_core_mass",
    "fe_core_mass",
    "surf_avg_v_div_v_crit",
]


def leer_history(path):
    with open(path, "r", encoding="utf-8") as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    indice_columnas = None

    for indice, linea in enumerate(lineas):
        if linea.startswith("model_number"):
            indice_columnas = indice
            break

    if indice_columnas is None:
        raise ValueError("No encontré las columnas de MESA.")

    columnas = lineas[indice_columnas].split()

    modelos = {}
    filas_validas = 0

    for linea in lineas[indice_columnas + 1 :]:
        valores = linea.split()

        if len(valores) != len(columnas):
            continue

        fila = dict(zip(columnas, valores))

        numero_modelo = int(fila["model_number"])

        # Si MESA reinició desde un modelo anterior,
        # conservamos la aparición más reciente.
        modelos[numero_modelo] = fila

        filas_validas += 1

    modelos_ordenados = [modelos[numero] for numero in sorted(modelos)]

    return modelos_ordenados, filas_validas


def numero(fila, columna):
    return float(fila[columna].replace("D", "E"))


def buscar_modelo(modelos, numero_buscado):
    for fila in modelos:
        if int(fila["model_number"]) == numero_buscado:
            return fila

    raise ValueError(f"No encontré el modelo {numero_buscado}.")


def buscar_primero(modelos, condicion, modelo_minimo=0):
    for fila in modelos:
        modelo = int(fila["model_number"])

        if modelo < modelo_minimo:
            continue

        if condicion(fila):
            return fila

    raise ValueError("No encontré una etapa que cumpla el criterio.")


def detectar_etapas(modelos):
    # Estos cinco puntos fueron obtenidos directamente
    # de las corridas por etapas de Hassan que validamos.
    pre_zams = buscar_modelo(modelos, 73)
    zams = buscar_modelo(modelos, 121)
    iams = buscar_modelo(modelos, 180)
    fin_h = buscar_modelo(modelos, 274)
    fin_he = buscar_modelo(modelos, 816)

    # Desde fin de He usamos la rama ratesfix.
    # El final de C se define físicamente por:
    # Xc(C12) <= 1e-3.
    fin_c = buscar_primero(
        modelos,
        lambda fila: numero(fila, "center_c12") <= 1e-3,
        modelo_minimo=817,
    )

    # La última fila es el modelo que alcanzó
    # el criterio de colapso.
    colapso = modelos[-1]

    return {
        "pre_zams": pre_zams,
        "zams": zams,
        "iams": iams,
        "end_core_h": fin_h,
        "end_core_he": fin_he,
        "end_core_c": fin_c,
        "core_collapse": colapso,
    }


def simplificar_fila(fila):
    resultado = {}

    for columna in COLUMNAS_GUARDADAS:
        if columna == "model_number":
            resultado[columna] = int(fila[columna])
        else:
            resultado[columna] = numero(fila, columna)

    return resultado


def guardar_csv(modelos):
    with open(
        CSV_PATH,
        "w",
        newline="",
        encoding="utf-8",
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=COLUMNAS_GUARDADAS,
        )

        escritor.writeheader()

        for fila in modelos:
            escritor.writerow(simplificar_fila(fila))


def guardar_etapas(etapas):
    datos = {
        "source": "Hassan et al. Population III MESA",
        "mesa_version": "r24.08.1-ratesfix",
        "initial_mass_msun": 50.0,
        "metallicity": 0.0,
        "new_omega_div_omega_crit": 0.20,
        "milestones": {
            nombre: simplificar_fila(fila) for nombre, fila in etapas.items()
        },
    }

    with open(
        JSON_PATH,
        "w",
        encoding="utf-8",
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
        )


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    modelos, filas_validas = leer_history(HISTORY_PATH)

    etapas = detectar_etapas(modelos)

    guardar_csv(modelos)
    guardar_etapas(etapas)

    print()
    print("===== TRACK POP III =====")
    print(f"Filas leídas:    {filas_validas}")
    print(f"Modelos únicos:  {len(modelos)}")
    print(f"Duplicados:      " f"{filas_validas - len(modelos)}")

    print()
    print("===== ETAPAS =====")

    for nombre, fila in etapas.items():
        modelo = int(fila["model_number"])
        edad = numero(fila, "star_age")

        print(f"{nombre:15} " f"modelo={modelo:4} " f"edad={edad:,.2f} años")

    print()
    print(f"CSV:  {CSV_PATH}")
    print(f"JSON: {JSON_PATH}")


if __name__ == "__main__":
    main()
