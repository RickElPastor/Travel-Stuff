"""Corrida reproducible del simulador real desde el año cero."""

import tempfile

from game import crear_modelo_estelar
from save_manager import SaveManager
from universe import Universe


SEMILLA = 374852300
CAMBIO_DE_PASO = 2_760_000_000
FIN_PASO_CORTO = 2_820_000_000
ANIO_FINAL = 3_000_000_000
PASO_INICIAL = 20_000_000
PASO_DE_VIDA = 1_000_000


def resumen(universo):
    planetas = universo.planetas
    especies = universo.modelo_especies_unicelulares
    vivas = sum(len(especies.especies_vivas(p)) for p in planetas)
    registradas = sum(len(especies.especies_registradas(p)) for p in planetas)
    return {
        "estrellas": len(universo.estrellas),
        "planetas": len(planetas),
        "entornos_prebioticos_historicos": sum(
            p.tuvo_entorno_prebiotico for p in planetas
        ),
        "organicos_historicos": sum(p.alcanzo_organicos_simples for p in planetas),
        "concentracion_historica": sum(
            p.alcanzo_concentracion_prebiotica for p in planetas
        ),
        "compartimentos_historicos": sum(
            p.alcanzo_compartimentalizacion_prebiotica for p in planetas
        ),
        "protocelulas_historicas": sum(p.alcanzo_protocelula for p in planetas),
        "primera_vida_historica": sum(p.alcanzo_primera_vida for p in planetas),
        "mundos_con_vida_activa": sum(p.vida_activa for p in planetas),
        "unidades_vivas": sum(p.poblacion_unicelular for p in planetas),
        "especies_vivas": vivas,
        "especies_extintas": registradas - vivas,
        "mundos_con_especies_coexistentes": sum(
            len(especies.especies_vivas(p)) >= 2 for p in planetas
        ),
    }


def ejecutar_con_modelo(modelo_estelar):
    universo = Universe(seed=SEMILLA, modelo_estelar=modelo_estelar)
    assert universo.time.anio == 0
    print(f"Semilla {SEMILLA}; inicio año 0; final {ANIO_FINAL:,}", flush=True)
    print(f"Pasos {PASO_INICIAL:,} hasta {CAMBIO_DE_PASO:,}; "
          f"{PASO_DE_VIDA:,} hasta {FIN_PASO_CORTO:,}; "
          f"después {PASO_INICIAL:,}", flush=True)
    hitos = (1_000_000_000, 2_000_000_000, 2_600_000_000,
             CAMBIO_DE_PASO, 2_780_000_000, 2_800_000_000,
             FIN_PASO_CORTO, ANIO_FINAL)
    primeros = set()
    while universo.time.anio < ANIO_FINAL:
        paso = (PASO_DE_VIDA if CAMBIO_DE_PASO <= universo.time.anio
                < FIN_PASO_CORTO else PASO_INICIAL)
        universo.time.anio += paso
        universo.actualizar(paso)
        datos = resumen(universo)
        for nombre, clave in (
            ("protocélulas", "protocelulas_historicas"),
            ("primera vida", "primera_vida_historica"),
            ("especies coexistentes", "mundos_con_especies_coexistentes"),
        ):
            if datos[clave] and nombre not in primeros:
                print(f"Primer hito {nombre}: año {universo.time.anio:,}; "
                      f"{datos}", flush=True)
                primeros.add(nombre)
        if universo.time.anio in hitos:
            print(f"Año {universo.time.anio:,}: {datos}", flush=True)

    for nombre in ("protocélulas", "primera vida", "especies coexistentes"):
        assert nombre in primeros, f"No apareció el hito esperado: {nombre}"
    assert datos["especies_extintas"] > 0

    with tempfile.TemporaryDirectory() as carpeta:
        gestor = SaveManager(carpeta)
        gestor.guardar(universo, "desde_cero")
        cargado = gestor.cargar("desde_cero", modelo_estelar=modelo_estelar)
    assert cargado.time.anio == universo.time.anio
    assert resumen(cargado) == resumen(universo)
    assert [p.a_dict() for p in cargado.planetas] == [
        p.a_dict() for p in universo.planetas
    ]
    print("Guardado/carga: año, resumen y estados planetarios iguales.", flush=True)
    for version in (universo, cargado):
        version.time.anio += PASO_DE_VIDA
        version.actualizar(PASO_DE_VIDA)
    assert resumen(cargado) == resumen(universo)
    assert [p.a_dict() for p in cargado.planetas] == [
        p.a_dict() for p in universo.planetas
    ]
    print("Continuación tras cargar: estados iguales.", flush=True)
    print("Corrida completa sin errores.", flush=True)
    return datos


def ejecutar():
    modelo_estelar = crear_modelo_estelar()
    try:
        return ejecutar_con_modelo(modelo_estelar)
    finally:
        modelo_estelar.cerrar()


if __name__ == "__main__":
    ejecutar()
