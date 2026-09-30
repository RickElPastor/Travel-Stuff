"""Corrida reproducible del simulador real desde el año cero."""

import tempfile

from game import crear_modelo_estelar
from universe.save_manager import SaveManager
from universe.universe import Universe


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
        "metabolismos_historicos": sum(
            p.alcanzo_metabolismo_inicial for p in planetas
        ),
        "fotosintesis_historicas": sum(
            p.alcanzo_fotosintesis for p in planetas
        ),
        "productores_activos": sum(
            p.unidades_productoras_activas for p in planetas
        ),
        "capacidad_descomponedora_historica": sum(
            p.alcanzo_capacidad_descomponedora for p in planetas
        ),
        "descomponedores_activos": sum(
            p.unidades_descomponedoras_activas for p in planetas
        ),
        "restos_pendientes": sum(p.restos_organicos_unidades for p in planetas),
        "nutrientes_pendientes": sum(
            p.nutrientes_reciclados_unidades for p in planetas
        ),
        "material_reciclado": sum(p.total_unidades_recicladas for p in planetas),
        "nutrientes_aprovechados": sum(
            p.total_nutrientes_aprovechados for p in planetas
        ),
        "atmosferas_con_aporte_biologico": sum(
            p.aporte_o2_biologico_bar is not None
            and p.aporte_o2_biologico_bar > 0
            for p in planetas
        ),
        "bases_ecologicas_activas": sum(
            p.estado_ecosistema == "microbiano_organicos_ambientales"
            for p in planetas
        ),
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
            ("metabolismo inicial", "metabolismos_historicos"),
            ("fotosíntesis", "fotosintesis_historicas"),
            ("capacidad descomponedora", "capacidad_descomponedora_historica"),
            ("base ecológica", "bases_ecologicas_activas"),
            ("especies coexistentes", "mundos_con_especies_coexistentes"),
        ):
            if datos[clave] and nombre not in primeros:
                print(f"Primer hito {nombre}: año {universo.time.anio:,}; "
                      f"{datos}", flush=True)
                primeros.add(nombre)
        if universo.time.anio in hitos:
            print(f"Año {universo.time.anio:,}: {datos}", flush=True)

    for nombre in ("protocélulas", "primera vida", "metabolismo inicial",
                   "base ecológica", "especies coexistentes"):
        assert nombre in primeros, f"No apareció el hito esperado: {nombre}"
    assert datos["especies_extintas"] > 0
    eventos = universo.event_manager.obtener_eventos()
    conteos = {
        tipo: sum(evento.ambito == tipo for evento in eventos)
        for tipo in ("sistema", "estrella", "planeta")
    }
    assert all(conteos.values()), f"Faltan eventos por ámbito: {conteos}"
    assert any(e.tipo == "Protocélulas" for e in eventos)
    assert any(e.tipo == "Primera vida" for e in eventos)
    assert any(e.tipo == "Metabolismo inicial" for e in eventos)
    assert all(p.anio_formacion is not None and p.periodo_orbital_dias > 0
               for p in universo.planetas)
    print(f"Eventos por ámbito: {conteos}; protocélulas y primera vida registrados.",
          flush=True)

    with tempfile.TemporaryDirectory() as carpeta:
        gestor = SaveManager(carpeta)
        gestor.guardar(universo, "desde_cero")
        cargado = gestor.cargar("desde_cero", modelo_estelar=modelo_estelar)
    assert cargado.time.anio == universo.time.anio
    assert resumen(cargado) == resumen(universo)
    assert [p.a_dict() for p in cargado.planetas] == [
        p.a_dict() for p in universo.planetas
    ]
    assert [e.a_dict() for e in cargado.event_manager.eventos] == [
        e.a_dict() for e in eventos
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
