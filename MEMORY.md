# Memoria de trabajo — Travel Stuff

Lee este registro junto con `FASES.md` antes de cada bloque. Agrega una entrada
al terminar cada cambio: fecha, archivos, decisión, pruebas, estado de Git y
siguiente paso. Conserva las entradas anteriores; Git sigue siendo la fuente
para conocer exactamente qué quedó confirmado en un commit.

## Estado actual — 2026-09-30

- `change_ui` quedó publicada en GitHub con el commit `b023b31`. Se recreó
  `fase-3` desde ese commit y se actualizó `origin/fase-3`; incluye estructura,
  exploración, eventos y calendario.
- La base simbólica de evolución biológica del paso 4 quedó validada para el
  cierre de `fase-2`. Consultar Git para el commit publicado; las entradas
  anteriores conservan el historial de trabajo local previo al cierre.
- La base simbólica del paso 5, metabolismo y biosfera, quedó validada en
  `fase-3`. Incluye consumo de orgánicos, productores fotosintéticos,
  proyección atmosférica separada, descomponedores y ciclo orgánico. Consultar
  Git para el commit y la publicación de la rama; la fase siguiente aún no
  comenzó.
- Al iniciar cada fase se explica su alcance; al terminarla se revisa,
  confirma y sube su rama. La instrucción permanente está en `AGENTS.md`.

## 2026-09-30 — Revisión integral y cierre técnico de Fase 3

- La revisión detectó que un salto largo podía omitir reciclaje de un linaje
  descomponedor transitorio. `biology/inheritance_variation_model.py` ahora
  procesa con `biology/material_cycle_model.py` cada intervalo de reproducción
  reconstruido, con sus linajes sobrevivientes y la muerte de ese intervalo.
  `universe/universe.py` conserva el cierre de muertes pendientes al extinguirse
  toda la población. `tests/test_material_cycle.py` fija el caso de regresión;
  `tests/test_unicellular_competition.py` reconoce los dos campos materiales
  que cambian con una muerte. `tests/test_phase3_integration.py` prueba juntas
  herencia, fotosíntesis, atmósfera y ciclo material con guardado/carga.
- Pasaron 109 pruebas automáticas, compilación y `git diff --check`. En una
  auditoría adicional, 200 semillas controladas con entorno constante dieron
  el mismo estado con pasos de 1 y 20 millones; el balance material se
  conservó en las 200. El universo real con semilla `374852300` avanzó del
  año 0 al 3 000 millones: pasos de 20 millones hasta 2 760 millones,
  1 millón hasta 2 820 millones y de nuevo 20 millones. Protocélulas en
  2 760 millones, primera vida y metabolismo en 2 763 millones y especies
  coexistentes en 2 769 millones. El resultado final tuvo 1849 planetas,
  cinco especies extintas, 26 restos pendientes y cero productores o
  descomponedores. Esta semilla no ejercitó esas capacidades; el caso
  combinado controlado sí. Guardar/cargar y avanzar otro millón conservó los
  estados.
- `FASES.md` marca terminada la base simbólica del paso 5. Queda publicar el
  commit de cierre en `fase-3`; la siguiente fase corresponde a vida compleja
  del paso 6 y todavía no se inicia.

## 2026-09-30 — Reservas de restos y nutrientes reciclados

- `biology/material_cycle_model.py` da una unidad simbólica de restos por
  muerte nueva. Descomponedores activos transfieren los restos disponibles a
  nutrientes; la ruta existente de consumo de orgánicos aprovecha esa reserva.
  Se guardan las reservas, muertes ya contabilizadas y totales históricos.
  Un guardado antiguo inicia sin reservas y no recrea muertes pasadas.
  `biology/decomposition_model.py` reconoce restos guardados además de
  muertes del paso como material para activar su enlace. No cambia población,
  física normal, clima ni atmósfera.
- `planets/planet.py` persiste los cinco campos de este ciclo;
  `universe/universe.py` lo evalúa después del rol descomponedor;
  `ui/simulation_ui.py` muestra restos, nutrientes y total aprovechado en
  Biosfera. `biology/README.md`, `ui/README.md` y `FASES.md` describen el
  alcance. `tests/run_universe_from_zero.py` informa ambos stocks y totales.
- `tests/test_material_cycle.py` comprueba balance, falta de un eslabón,
  reciclaje posterior, consumo, reevaluación, pasos temporales, guardado/carga
  y partida antigua. `tests/test_simulation_dashboard.py` comprueba la línea
  visible. Pasaron 107 pruebas automáticas, compilación y `git diff --check`.
  La corrida natural completa con
  semilla `374852300` avanzó del año 0 a 3 000 millones: pasos de 20 millones
  hasta 2 760 millones, 1 millón hasta 2 820 millones y luego 20 millones.
  Protocélulas en 2 760 millones, primera vida en 2 763 millones y especies
  coexistentes en 2 769 millones. Al final había 1849 planetas, cinco
  especies extintas, 26 unidades de restos pendientes y cero recicladas:
  esta semilla no produjo descomponedores. Guardar/cargar y avanzar otro
  millón mantuvo estados iguales. Las pruebas controladas sí recorrieron
  restos → nutrientes → consumo.
- `fase-3` continúa local sin commit ni push. Siguiente trabajo: revisión
  integral del paso 5 y cierre de la fase si no quedan fallos.

## 2026-09-30 — Capacidad descomponedora y restos recientes

- `biology/decomposition_model.py` decide una capacidad descomponedora por
  variante con azar local y una probabilidad de diseño, solo en un entorno
  con orgánicos. En `biology/inheritance_variation_model.py`, copias y
  variantes hijas del progenitor capaz la conservan. `planets/planet.py`
  persiste los linajes capaces, el hito histórico y las unidades actualmente
  activas; los guardados antiguos comienzan vacíos.
- `universe/universe.py` calcula las muertes de cada actualización, evalúa
  descomposición después del metabolismo y registra el hito planetario.
  Muertes viejas no se convierten en restos siempre disponibles. La señal
  activa es cualitativa: no hay reserva de nutrientes ni retroalimentación
  de crecimiento o atmósfera. `ui/simulation_ui.py` muestra el enlace en
  Biosfera. `tests/run_universe_from_zero.py`, `biology/README.md`,
  `ui/README.md` y `FASES.md` explican la regla y sus límites.
- `tests/test_decomposition.py` cubre ausencia de capacidad, adaptación,
  herencia, cese, extinción, equivalencia de pasos y guardado antiguo/nuevo;
  `tests/test_simulation_dashboard.py` cubre el texto de la vista. Al revisar
  se corrigió una duplicación del sufijo «con reciclaje» al evaluar dos veces
  el mismo paso. Pasaron 103 pruebas automáticas, compilación y
  `git diff --check`.
- Corrida real con semilla `374852300`, año 0 a 3 000 millones: pasos de
  20 millones hasta 2 760 millones, 1 millón hasta 2 820 millones y luego
  20 millones. Protocélulas en 2 760 millones, primera vida y metabolismo
  en 2 763 millones, coexistencia en 2 769 millones. A 3 000 millones había
  1849 planetas, cinco especies extintas y cero linajes con capacidad
  descomponedora; la semilla no ejercitó el nuevo enlace. Las pruebas
  controladas sí lo activaron. Guardar/cargar y continuar otro millón
  conservó todos los estados.
- `fase-3` sigue local, sin commit ni push. Siguiente bloque: una relación
  material pequeña entre restos, reciclaje y consumo, y después revisión
  integral de la fase.

## 2026-09-30 — Proyección atmosférica de productores

- `biology/atmospheric_impact_model.py` calcula después del metabolismo una
  proyección actual de CO₂ y aporte de O₂ solo con productores activos. Cada
  unidad transforma simbólicamente 1 % del CO₂ físico, con tope conjunto de
  5 %. Son parámetros de diseño; el resultado no se acumula por actualización
  y vuelve a la base física cuando cesa la producción. El modelo no modifica
  `presion_co2_preclima_bar`, clima, habitabilidad o población.
- `universe/universe.py` lo ejecuta tras contar productores. `planets/planet.py`
  guarda ambos valores y usa `None` para partidas antiguas hasta recalcular.
  `ui/simulation_ui.py` enseña la comparación en Biosfera.
  `tests/test_atmospheric_impact.py` comprueba tope, ausencia de productores,
  conservación de la física y guardado antiguo/nuevo;
  `tests/test_photosynthetic_producers.py` comprueba igualdad de pasos también
  con estos campos. `tests/test_simulation_dashboard.py` comprueba la vista.
  `tests/run_universe_from_zero.py`, `biology/README.md`, `ui/README.md` y
  `FASES.md` reflejan el nuevo bloque.
- Pasaron 97 pruebas automáticas y compilación. Corrida natural con semilla
  `374852300`, año 0 a 3 000 millones: pasos de 20 millones hasta 2 760
  millones, 1 millón hasta 2 820 millones y después 20 millones. Protocélulas
  en 2 760 millones, primera vida y metabolismo en 2 763 millones y especies
  coexistentes en 2 769 millones. A 3 000 millones había 1849 planetas,
  cinco especies extintas, cero productores y cero atmósferas con aporte
  biológico. La semilla no activó fotosíntesis; las pruebas controladas sí
  verifican la proyección. Guardar/cargar y continuar otro millón conservó
  los estados. Rama `fase-3` sin commit ni push mientras sigue abierta.
- Siguiente bloque: rol de descomponedores y primeras relaciones ecológicas
  entre productores, consumidores y reciclaje, todavía simbólicas.

## 2026-09-30 — Productores fotosintéticos simbólicos

- `biology/metabolism_model.py` reconoce luz, agua líquida y CO₂ como entorno
  apto, y una adaptación de diseño puede surgir en una variante biológica.
  `biology/inheritance_variation_model.py` conserva esa capacidad en copias y
  variantes hijas del linaje capaz. Se corrigió durante la revisión una
  consulta al identificador de la hija en vez del progenitor; una prueba nueva
  comprueba la herencia en una variante aunque no adquiera la capacidad de
  nuevo. El azar se decide por nacimiento y no consume el del universo.
- `planets/planet.py` persiste el conjunto de linajes capaces, productores
  activos e hito histórico; un guardado anterior comienza con valores vacíos.
  `universe/universe.py` registra el primer hito como evento planetario.
  `ui/simulation_ui.py` muestra productores y vínculos simbólicos en Biosfera.
  `biology/README.md`, `ui/README.md` y `FASES.md` explican el alcance.
  `tests/run_universe_from_zero.py` informa fotosíntesis histórica y
  productores activos; `tests/test_photosynthetic_producers.py` y
  `tests/test_simulation_dashboard.py` comprueban condiciones, herencia,
  persistencia, determinismo y pantalla.
- Pasaron 94 pruebas automáticas, compilación y `git diff --check`.
  Corrida natural con semilla `374852300`, año 0 a 3 000 millones: pasos de
  20 millones hasta 2 760 millones, 1 millón hasta 2 820 millones y luego
  20 millones. Primera vida y metabolismo en 2 763 millones; coexistencia
  de especies en 2 769 millones. A 3 000 millones había 1849 planetas,
  cinco especies extintas, cero fotosíntesis histórica y cero productores
  activos. Es un resultado válido para esta semilla; las pruebas controladas
  sí activan y desactivan la ruta. Guardar/cargar y continuar otro millón
  conservó los estados.
- Rama `fase-3`, trabajo local sin commit ni push mientras la fase continúa.
  Siguiente bloque: efecto biológico acotado sobre la atmósfera, manteniendo
  separadas las condiciones físicas de la contribución de la vida.

## 2026-09-30 — Primera energía metabólica y base ecológica microbiana

- `biology/metabolism_model.py` consulta luz, ruta geoquímica y orgánicos
  ambientales actuales. La primera población con vida activa y orgánicos
  recibe la ruta simbólica `consumo_organicos`; sin vida no se crea ruta. Luz
  y geoquímica son potenciales y no fuerzan fotosíntesis o quimiosíntesis.
  La base ecológica observada es el vínculo entre orgánicos y microbios,
  todavía sin red trófica ni efecto sobre reproducción o atmósfera.
- `planets/planet.py` persiste fuentes, ruta y estado actuales, además del
  primer año histórico de metabolismo; guardados anteriores usan valores
  vacíos y se recalculan al actualizar. `universe/universe.py` evalúa después
  de la población unicelular y registra el primer hito como evento planetario.
- `ui/simulation_ui.py` muestra la ruta breve en la ficha planetaria y abre
  con `M` una ficha Biosfera con fuentes, ruta y vínculo ecológico.
  `biology/README.md`, `ui/README.md` y `FASES.md` explican alcance y límites.
- `tests/test_metabolism.py` cubre ausencia de vida, disponibilidad sin rutas
  inventadas, cese y persistencia histórica, guardado/carga y compatibilidad;
  `tests/test_simulation_dashboard.py` revisa navegación y datos de Biosfera.
  `tests/run_universe_from_zero.py` comprueba el hito y su evento en un universo
  natural. 88 pruebas automáticas aprobadas.
- Corrida real con semilla `374852300`: año 0 a 3 000 millones; pasos de
  20 millones hasta 2 760 millones, 1 millón hasta 2 820 millones y de nuevo
  20 millones. Protocélulas en 2 760 millones; primera vida, metabolismo y
  base ecológica en 2 763 millones; tres especies coexistentes en 2 769
  millones. A 3 000 millones había 1849 planetas, un metabolismo histórico,
  ninguna base ecológica activa y cinco especies extintas. Guardar/cargar y
  avanzar otro millón conservó los estados planetarios y el historial.
- El push ordinario de `change_ui` falló por DNS; con acceso autorizado se
  publicaron tanto `change_ui` como `fase-3`. Próximo bloque: rutas energéticas
  nuevas que requieran adaptación biológica y primeros roles de productores.

## 2026-09-30 — Rama `change_ui`

- Por petición del usuario, los cambios locales de preparación estructural,
  navegación, eventos y calendario se guardan juntos en `change_ui`, creada
  desde `fase-3`. Tras subirla, se vuelve a `fase-3` sin integrarla todavía;
  allí quedan pendientes tanto esta integración como el metabolismo.
- No se añadieron reglas de civilización: sus nombres de meses y siglos
  requerirán un estado persistente y una vista propia en una etapa posterior.
- La validación del código para este commit es la de las dos entradas
  siguientes: 83 pruebas automáticas y universo natural desde año 0 hasta
  3 000 millones con continuidad de guardado/carga. No se modificó el motor
  después de esas comprobaciones.

## 2026-09-30 — Eventos por ámbito y calendario local de observación

- Rama `fase-3`, cambios locales sin commit ni push: la fase de metabolismo y
  biosfera sigue abierta. Se mantiene íntegro el reordenamiento de carpetas
  y la navegación de la entrada anterior.
- `universe/events.py` añade ámbito y entidad opcionales a cada evento. Los
  eventos de guardados antiguos se interpretan como universales; guardar y
  cargar conserva los campos nuevos. `universe/universe.py` registra el inicio
  de un universo nuevo con su semilla, y después la formación
  de sistemas y planetas, nacimiento/evolución/remanente de estrellas (incluso
  cuando una estrella queda fuera del modelo), y primeros hitos planetarios
  (atmósfera secundaria, etapas de química prebiótica, protocélulas,
  replicación, vida y extinción local). No altera la física ni el azar.
- `planets/planet.py` guarda año de formación y duración orbital calculada al
  formarse. `planets/local_calendar.py` deriva la fecha visible del único
  reloj universal. Usa la aproximación kepleriana para el año orbital, doce
  divisiones iguales para meses y días estándar de 24 horas; no hay rotación
  ni calendario cultural. Los guardados previos intentan reconstruir datos
  disponibles para la pantalla y marcan la fecha como aproximada.
- `ui/simulation_ui.py` quita las indicaciones repetidas de Enter/E del
  contenido. `V` abre eventos universales o del objeto seleccionado; las
  fichas muestran recientes donde caben. Entrar a planeta ahora fija x1,
  igual al x1 universal (un año universal por segundo), y presenta año, mes,
  día, hora, minuto y segundo locales, junto al año universal del encabezado.
  `universe/world_time.py` hace visible la etiqueta x1. En
  `universe/simulation.py` el límite por refresco pasó a 0.1 s: antes cortaba
  cada intervalo de pantalla de 0.05 s a 0.02 s, y x1 avanzaba más lento de
  lo anunciado. `ui/README.md` y `FASES.md` explican los límites de esta
  observación.
- `tests/test_simulation_dashboard.py` cubre navegación de eventos, ámbitos,
  persistencia, compatibilidad de eventos anteriores, año orbital de 1000
  días, reloj compartido y x1 medido con veinte refrescos de 0.05 s. La
  prueba de pantalla previa falló al seguir
  esperando 1000 años/s y la nota de galaxias en la fila anterior; se ajustó
  a los requisitos nuevos. `tests/run_universe_from_zero.py` exige eventos
  por los tres ámbitos, hitos de protocélulas/vida, periodos planetarios y
  continuidad del historial tras guardar/cargar.
- Validación: 83 pruebas automáticas aprobadas; corrida real con semilla
  `374852300` desde 0 hasta 3 000 000 000, pasos de 20 millones hasta
  2 760 millones, 1 millón hasta 2 820 millones y de nuevo 20 millones.
  Protocélulas a 2 760 millones, vida a 2 763 millones, tres especies
  coexistentes a 2 769 millones; al final 1849 planetas y 5 especies
  extintas. Eventos: 956 de sistema, 1099 de estrella y 1878 de planeta.
  Guardar/cargar y continuar conservaron estados y eventos. Falta una
  revisión manual de legibilidad en una terminal real con muchos eventos.
- Siguiente bloque de `fase-3`: fuentes de energía y metabolismo simbólico.

## 2026-09-30 — Preparación de la estructura y exploración antes de metabolismo

- Rama `fase-3`; trabajo local sin commit ni push porque la fase sigue abierta.
  La raíz conserva `main.py` y `game.py` como entradas, además de los
  documentos. El motor, tiempo, eventos, cosmología, simulación y guardado
  están en `universe/`; estrellas, sistemas, remanentes, modelos y track Hassan
  están en `stars/`. La configuración de pantalla pasó a `ui/config.py`.
  Se actualizaron imports de juego, modelos, interfaz y pruebas, y las rutas
  de los datos estelares. El formato JSON y las reglas físicas no cambiaron.
- `ui/simulation_ui.py` sustituyó las cinco vistas por una ruta: Universo →
  catálogo de sistemas o estrellas → ficha del sistema → catálogo de sus
  planetas → ficha planetaria. Cada catálogo muestra la lista completa por
  páginas, datos relevantes y filtro de nombre con `/`. `Esc` retrocede,
  `Enter` abre, `S` guarda y `+/-` modifica velocidad. No hay galaxias
  simuladas, así que la pantalla lo dice sin inventarlas. `ui/README.md`
  explica la navegación para el usuario.
- `universe/world_time.py` añadió velocidades planetarias hasta 10 000
  años/s conservando los índices antiguos 0–3 para partidas guardadas. Al
  entrar en una ficha planetaria se usan 1 000 años/s y al salir se recupera
  la escala e índice anteriores. Una partida guardada dentro del planeta abre
  el explorador en Universo y vuelve a la escala universal. El tiempo sigue
  siendo del universo entero.
- `tests/test_simulation_dashboard.py` cubre inicio en Universo, navegación,
  búsqueda, lista larga, estrellas, datos relevantes, velocidad local,
  preservación del azar y guardado/carga. El catálogo vacío muestra una
  explicación propia. 80 pruebas automáticas aprobadas; el modelo estelar
  híbrido se pudo crear tras mover el track. Se inició y cerró el juego real
  en una terminal de 100×30, entrando al universo y al catálogo sin excepción.
- Se repitió el escenario real desde año 0, semilla 374852300, con pasos de
  20 millones hasta 2 760 millones, 1 millón hasta 2 820 millones y de nuevo
  20 millones hasta 3 000 millones. Conservó el resultado de Fase 2:
  protocélulas en 2 760 millones, vida en 2 763 millones y coexistencia de
  tres especies en 2 769 millones; guardar/cargar y continuar coincidieron.
  La navegación con un universo poblado merece inspección manual de
  usabilidad, aunque la ruta se cubrió con pruebas de pantalla simulada.
- Próximo bloque de `fase-3`: fuentes de energía y metabolismo simbólico.

## 2026-09-30 — Revisión integral y cierre de Fase 2

- La primera corrida desde cero había creado `Universe` sin el modelo estelar
  híbrido. No reproducía «Iniciar simulación» del juego y por eso llegó a
  cero entornos prebióticos. No era evidencia de un fallo de química o vida.
- `game.py` expone `crear_modelo_estelar` para compartir exactamente la misma
  configuración entre el juego y `tests/run_universe_from_zero.py`. El
  escenario cierra el modelo al terminar, carga con ese mismo modelo y compara
  los planetas después de continuar. Ahora falla si no aparecen protocélulas,
  primera vida, especies coexistentes y extinción histórica.
- Corrida real: semilla `374852300`, año 0 a 3 000 000 000, pasos de 20 millones
  hasta 2 760 millones, de 1 millón hasta 2 820 millones y otra vez de 20
  millones. Protocélulas en 2 760 millones; primera vida en 2 763 millones;
  coexistencia de tres especies y siete unidades en 2 769 millones. En 2 780
  millones había ocho unidades, dos especies vivas y dos extintas. En 2 800
  millones ya no había vida activa y cinco especies quedaron extintas; el
  historial persistió hasta 3 000 millones. Guardar/cargar y avanzar otro
  millón de años produjo planetas iguales.
- `tests/test_simulation_dashboard.py` también comprueba la vista 5 después
  de la extinción. `biology/README.md` aclara la diferencia entre la corrida
  incompleta y la del juego. `FASES.md` marca la revisión integral hecha y
  describe el alcance de `fase-3`. `AGENTS.md` guarda el ciclo de ramas,
  explicación inicial y commit/push de cierre que pidió el usuario.
- Validación final: 80 pruebas automáticas aprobadas, compilación de módulos
  y `git diff --check` sin errores; corrida real terminada con hitos biológicos
  y continuidad de guardado/carga. No se cambió la física normal ni la regla
  de aparición de vida. Próximo trabajo: fuentes de energía y metabolismo
  simbólico del paso 5, desde la rama `fase-3`.

## 2026-09-30 — Diversificación y corrida desde cero

- `AGENTS.md`: exige empezar cada validación con un universo real en el año 0,
  registrar semilla, pasos, hitos y límites, y decir si hace falta prueba
  manual. El informe al usuario incluye cambios, errores, concepto, pruebas,
  pendientes de fase y siguiente paso; si pregunta algo, la respuesta va arriba.
- `biology/species_model.py`: consultas puras de abundancia por especie y de
  especie progenitora e hijas directas. Derivan datos del parentesco ya
  persistido; la extinción de una progenitora no borra la relación. No cambian
  las reglas de reproducción, física ni azar.
- `ui/simulation_ui.py`: vista 5 «Especies» muestra totales, coexistencia,
  abundancia del mundo observado y su rama. La vista 4 «Vida» permanece.
  `tests/test_simulation_dashboard.py` comprueba las cinco vistas en 72×24 y
  que dibujar no altere el planeta.
- `tests/test_unicellular_diversification.py`: prueba parentesco, abundancia,
  coexistencia representada, extinción, consultas sin mutación y guardado/carga.
  `tests/run_universe_from_zero.py`: corrida reproducible desde cero y
  comprobación de año, resumen y planetas tras guardar/cargar.
- `biology/README.md` explica el seguimiento y sus límites. `FASES.md` marca
  diversificación hecha; falta la revisión integral de cierre.
- Validación: 80 pruebas con `unittest discover` pasaron; `git diff --check`
  sin errores. La primera ejecución de pruebas detectó una expectativa de la
  vista 4 después de activar la 5; se corrigió la secuencia de esa prueba.
  Corrida real: semilla 374852300, año 0 a 5 400 000 000; pasos de 20 millones
  hasta 2 760 millones, de 1 millón hasta 2 820 millones, luego 20 millones.
  Llegó a 1 884 estrellas activas y 5 250 planetas; no registró entornos
  prebióticos, orgánicos, protocélulas ni vida. Guardado/carga reprodujo el
  estado final. Esto **no** ejercitó diversificación natural; las pruebas
  controladas sí cubrieron tres especies coexistentes y parentesco. El cero
  contrasta con una corrida anterior descrita en `biology/README.md`; la
  revisión integral debe aclarar si la diferencia se debe a pasos temporales
  o a otra condición antes de cerrar Fase 2.
- Rama `fase-2`; sin commit ni push por instrucción del usuario.

## 2026-09-29 — Criterio operativo de especies unicelulares

- `biology/species_model.py`: clasifica por parentesco. La fundadora inicia
  especie; la primera variación de la rama la conserva y la segunda inicia
  otra. El umbral 2 es diseño, no ciencia medida. Rasgos iguales no fusionan
  especies; hermanos no suman sus variaciones. Consultas de vivas, registradas
  y extintas mediante conjuntos, sin modificar la biología.
- `planets/planet.py`: persiste especie y distancia por linaje; conserva las
  asignaciones conocidas. Al construir/cargar, completa las que falten con
  el parentesco histórico disponible. Linajes sin ascendencia conocida reciben
  especies provisionales propias. No se inventan registros históricos ausentes.
- `biology/inheritance_variation_model.py` clasifica fundadoras y variantes
  nuevas en el momento de registrarlas. `universe.py` expone el modelo a la UI.
- `ui/simulation_ui.py`: vista 4 muestra especies vivas, extintas y registradas
  del universo, y especie del linaje observado. Los identificadores son locales
  por planeta; las consultas no alteran la simulación ni borran extintos.
- `tests/test_unicellular_species.py`: ocho pruebas de criterio, herencia real,
  extinción de la última unidad, refundación, copias, compatibilidad,
  guardado/carga y pasos temporales. `tests/test_simulation_dashboard.py`:
  totales por planeta, extinción y visualización en terminal mínima.
- `biology/README.md` y `FASES.md`: explican límites y marcan el paso de
  especies hecho. Quedan el seguimiento de diversificación y la revisión
  integral; la ramificación básica ya resulta del criterio implementado.
- Validación: 77 pruebas aprobadas con
  `.venv/bin/python -m unittest discover -s tests -v`, sin fallos en la
  ejecución. Pendientes la revisión manual y la corrida completa de cierre.
  Rama `fase-2`, sin commit ni push nuevos.

## 2026-09-29 — Parentesco persistente de linajes

- `planets/planet.py`: nuevo diccionario histórico por identificador, con
  progenitor, rasgo y origen. Guarda claves de texto en JSON y recupera enteros
  al cargar; copia los registros para no compartir diccionarios mutables.
  Estados anteriores reciben registros de origen desconocido solo para los
  linajes vivos conocidos, sin inventar antepasados ni extintos.
- `biology/inheritance_variation_model.py`: registra fundadoras sin progenitor
  y variantes con el linaje realmente seleccionado para reproducir. No crea
  entradas por nacimientos sin variación ni borra historia con las extinciones.
- `ui/simulation_ui.py`: vista 4 muestra linajes registrados y origen del
  observado (identificador del progenitor, fundador o desconocido). Compacta
  la fila a «Rasgo», «Linaje», «Origen» y «Variaciones»; este último sigue
  siendo el contador histórico. No se añadió una vista de árbol completa.
- `tests/test_unicellular_ancestry.py`: siete pruebas de parentesco,
  selección del progenitor, no duplicación, extinción/reinicio, guardar/cargar,
  pasos temporales, compatibilidad y copias independientes. Se ajustaron las
  comprobaciones de pantalla en `tests/test_simulation_dashboard.py`.
- `biology/README.md` explica diccionarios e historial. `FASES.md` registra
  el avance y el alcance del cierre: especies, diversificación y revisión
  integral. Son bloques principales, no una estimación exacta de turnos.
- Validación: 68 pruebas aprobadas con
  `.venv/bin/python -m unittest discover -s tests -v`. No se detectaron fallos
  en esa ejecución. Falta revisión manual y una corrida completa de un
  universo para el cierre. Rama `fase-2`, sin commit ni push nuevos.

## 2026-09-29 — Selección reproductiva entre linajes vivos

- El usuario confirmó las pruebas de linajes; aún no hizo guardado/carga
  manual. Las pruebas automáticas de este bloque sí incluyen esa continuidad.
- `biology/selection_model.py`: identifica linajes ajustados al agua sin
  duplicar identidades. Antes de reproducir, conserva el observado si está
  ajustado; si solo otros lo están, elige la primera unidad ajustada; sin
  candidatos mantiene el observado vivo. Es una regla simbólica de diseño.
- `biology/inheritance_variation_model.py`: aplica la comparación antes de
  cada nacimiento. La descendencia hereda la identidad elegida y luego puede
  variar. Repetir una evaluación sin nacimientos no repite selección. No se
  cuentan los relevos de linajes existentes como variantes nuevas.
- `ui/simulation_ui.py`: muestra «Linajes ajustados X/Y» para el mundo
  observado, o «sin regla». Se deriva de datos ya guardados; no hay nuevos
  campos persistentes ni cambios al formato de guardado.
- `tests/test_unicellular_competition.py`: siete pruebas de efecto en
  descendencia, empates, ausencia de candidatos, extinción, compatibilidad,
  guardado/carga, pasos distintos con el mismo cambio ambiental y conservación
  de física/azar. `tests/test_simulation_dashboard.py`: verifica el indicador
  en una terminal de 72 columnas y 24 filas y estados sin regla de agua.
- `biology/README.md` y `FASES.md`: documentan la selección reproductiva y
  preparan parentesco de linajes antes de especies/diversificación.
- Validación: 61 pruebas aprobadas con
  `.venv/bin/python -m unittest discover -s tests -v`. No hubo fallos en esta
  ejecución. Falta la revisión manual; no se ejecutó un universo completo en
  este bloque. Rama `fase-2`, sin nuevo commit ni push.

## 2026-09-29 — Revisión y cierre del bloque de linajes

- El usuario confirmó que las pruebas de herencia unicelular pasaron en su
  equipo. Al retomar se encontró el avance local de identidad de linajes
  descrito abajo, todavía pendiente de validación.
- Tres pruebas adicionales reprodujeron fallos: identidad observada ausente
  en poblaciones inicializadas directamente; rasgos distintos agrupados bajo
  un solo identificador al cargar; y reproducción de un linaje ya desaparecido.
- `planets/planet.py`: inicializa identidades provisionales negativas por
  rasgo en estados anteriores sin linajes y asigna la identidad observada.
  Así conserva los grupos actuales sin inventar antepasados ni colisionar
  con futuros números de nacimiento.
- `biology/inheritance_variation_model.py`: procesa nacimientos y retiros
  por intervalo para mantener el orden con pasos distintos. Si desaparece el
  linaje observado, sigue la unidad más reciente que permanece viva, sin
  alterar los contadores de selección por este relevo.
- `tests/test_unicellular_lineages.py`: agrega regresiones para los tres
  fallos y comprueba que un guardado antiguo de una sola unidad conserve su
  identidad provisional al evaluarse. `tests/test_unicellular_inheritance.py`: corrige el ejemplo de
  guardado antiguo para que tampoco contenga listas de unidades/linajes,
  ausentes en ese formato. `tests/test_simulation_dashboard.py`: comprueba
  también linajes cero e identidad vacía después de una extinción.
- `biology/README.md` y `FASES.md`: explican identidades, listas paralelas,
  relevo, compatibilidad y límites. La comparación ambiental entre linajes
  vivos sigue pendiente; este bloque no implementa especies ni genealogía.
- Validación final: 54 pruebas superadas con
  `.venv/bin/python -m unittest discover -s tests -q` y `git diff --check`
  sin errores. No se hizo una corrida
  completa de un universo ni una revisión manual de la terminal en este
  bloque. Sin commit ni push; se conservó el cambio previo de `.gitignore`.

## 2026-09-29 — Identidad de linajes unicelulares

- `planets/planet.py`: guarda un identificador de linaje por unidad simbólica
  y el identificador de la línea observada. Guardados anteriores reciben un
  solo identificador provisional para todas sus unidades, sin inventar
  ramificaciones anteriores.
- `biology/inheritance_variation_model.py`: la fundadora obtiene un
  identificador por número de nacimiento; un nacimiento sin variación hereda
  la identidad observada y una variante inicia un linaje nuevo. Las muertes
  retiran identificadores junto con rasgos; la extinción vacía ambas listas.
- `ui/simulation_ui.py`: vista 4 muestra el número de linajes vivos y el
  identificador de la línea observada. Aún no compara su éxito relativo.
- `tests/test_unicellular_lineages.py` y
  `tests/test_simulation_dashboard.py`: prueban creación, continuidad,
  desaparición, guardado/carga, guardados anteriores, pasos temporales y vista.
- `.gitignore`: se retiró la regla local `tests/`, que ocultaba las pruebas
  nuevas a Git. Se conservó el resto del cambio local del usuario.
- `biology/README.md` y `FASES.md`: documentan el alcance simbólico y dejan
  la comparación entre linajes como siguiente bloque. Validación completa
  pendiente al escribir esta entrada; no hay commit ni push nuevos.

## 2026-09-29 — Coexistencia de rasgos unicelulares

- `planets/planet.py`: guarda una lista de rasgos vivos, uno por unidad
  simbólica. Un guardado anterior sin la lista supone que sus unidades tienen
  el rasgo de la línea observada, o 1 si no lo tiene; no inventa variaciones.
- `biology/inheritance_variation_model.py`: agrega el rasgo de cada nacimiento
  y retira las unidades más antiguas hasta igualar el tamaño de población.
  Una variante descartada de la línea observada todavía puede coexistir.
  La extinción vacía la lista y conserva la historia.
- `ui/simulation_ui.py`: vista 4 presenta número de rasgos activos y reparto
  0/1/2 del mundo observado, siempre como unidades simbólicas.
- `tests/test_unicellular_inheritance.py` y
  `tests/test_simulation_dashboard.py`: cubren coexistencia, extinción,
  guardado anterior, continuidad, pasos temporales y pantalla.
- `biology/README.md` y `FASES.md`: explican el límite: los grupos de rasgos
  aún no son linajes con identidad ni especies. Validación: 46 pruebas
  superadas con `.venv/bin/python -m unittest discover -s tests -v` y
  `git diff --check` sin errores. Queda la revisión manual del usuario.
  Git sigue sin nuevo commit ni push.

## 2026-09-29 — Indicador de ajuste ambiental y formato de respuestas

- `AGENTS.md`: exige responder primero las preguntas del usuario y después
  explicar cambios, errores, lógica, pruebas y siguiente paso en ese orden.
- `biology/selection_model.py`: calcula si el rasgo de la línea con población
  coincide con el favorecido por el agua actual. No añade azar ni cambia la
  física o la supervivencia.
- `universe.py` y `ui/simulation_ui.py`: la vista 4 muestra «ajuste agua
  sí/no» para el mundo observado. El valor se deriva de estados ya guardados,
  así que no se añadió otro campo al archivo de guardado.
- `tests/test_unicellular_selection.py` y
  `tests/test_simulation_dashboard.py`: verifican cambio de agua, cambio de
  rasgo, extinción, carga de estado y pantalla. Validación: 45 pruebas
  superadas con `.venv/bin/python -m unittest discover -s tests -v`.
- `biology/README.md` y `FASES.md`: distinguen este indicador de una capacidad
  real de supervivencia y señalan varios linajes como próximo trabajo.

## 2026-09-29 — Selección biológica inicial

- `biology/selection_model.py`: el agua en hielo favorece el rasgo simbólico
  0 y el agua líquida el 2. Solo una variante mejor que el rasgo anterior
  continúa la línea observada; ninguna regla cambia la física normal.
- `biology/inheritance_variation_model.py`: al aparecer una variante, delega
  la continuidad de la línea al modelo de selección. La variación se cuenta
  aunque la variante no continúe.
- `planets/planet.py`: persiste los contadores históricos de variantes
  favorecidas y descartadas, con cero por defecto en guardados anteriores.
- `ui/simulation_ui.py`: vista 4 muestra los dos contadores y aclara que las
  unidades de población son simbólicas.
- `tests/test_unicellular_selection.py`,
  `tests/test_unicellular_inheritance.py` y
  `tests/test_simulation_dashboard.py`: comprueban la regla por entorno,
  continuidad determinista, guardado/carga y visualización.
- `biology/README.md` y `FASES.md`: describen el alcance y el siguiente
  bloque. Una prueba nueva falló inicialmente por un `NameError` al ubicar
  dos líneas en el método equivocado; se corrigió el test. Validación final:
  44 pruebas superadas con
  `.venv/bin/python -m unittest discover -s tests -v` y
  `git diff --check` sin errores. Una corrida completa con semilla `374852300`
  y pasos de 20 millones de años mostró población 1 al año 2 780 000 000;
  al 2 800 000 000, `co2_excesivo` cortó la viabilidad y la población llegó
  a cero. Sin nacimientos posteriores, variación y selección quedaron en
  cero; es un resultado válido de ese mundo, no un fallo del modelo.

## 2026-09-29 — Herencia y variación unicelulares

- `biology/inheritance_variation_model.py`: sigue un rasgo simbólico de una
  línea de nacimientos. Cada nacimiento hereda el anterior y puede variar
  mediante un generador local identificado por semilla, mundo y número de
  nacimiento. No usa el azar global ni modifica el patrón químico.
- `planets/planet.py` y `universe.py`: persisten los nuevos campos y evalúan
  herencia después de actualizar la población. Los guardados anteriores
  inician sin variaciones retrospectivas.
- `ui/simulation_ui.py`: vista 4 muestra el rasgo actual de la línea y las
  variaciones históricas, incluso si la línea está inactiva.
- `biology/README.md` y `FASES.md`: explican el alcance y señalan la selección
  biológica como siguiente trabajo.
- `tests/test_unicellular_inheritance.py` y
  `tests/test_simulation_dashboard.py`: verifican extinción, mismo resultado
  con pasos distintos, guardado/carga, independencia del azar global y vista.
- Validación: 42 pruebas superadas con
  `.venv/bin/python -m unittest discover -s tests -q`;
  `git diff --check` sin errores. Falta revisión manual en un universo nuevo.

## 2026-09-29 — Supervivencia y reproducción unicelular básica

- `MEMORY.md`: se crea este registro continuo y `AGENTS.md` exige leerlo y
  actualizarlo en cada bloque.
- `biology/unicellular_population_model.py`: registra nacimientos y muertes
  en intervalos simbólicos. Si la vida actual cesa, cuenta la pérdida de toda
  la población. Calcula varios intervalos juntos sin usar azar global.
- `planets/planet.py`: guarda y carga los dos contadores nuevos con valores
  por defecto para guardados anteriores.
- `ui/simulation_ui.py`: la vista 4 muestra los contadores globales y permite
  inspeccionar un mundo aunque su población se haya extinguido.
- `tests/test_unicellular_population.py` y
  `tests/test_simulation_dashboard.py`: verifican continuidad, tamaños de paso,
  guardado/carga y visualización después de una extinción.
- `biology/README.md` y `FASES.md`: explican la regla de diseño y el progreso.
- Validación: 38 pruebas superadas con
  `.venv/bin/python -m unittest discover -s tests -v`; `git diff --check` sin
  errores. Falta revisión manual del usuario en un universo nuevo.

## 2026-09-29 — Corrección de la hoja de ruta

- `FASES.md`: reemplaza la división propuesta en seis fases por los diez pasos
  proporcionados por el usuario y marca lo ya implementado.
- `AGENTS.md`: instruye a consultar la hoja de ruta antes de editar y a no
  hacer commit/push sin petición expresa. Ahora también pide consultar y
  actualizar este registro.
- Solo cambió documentación en ese bloque; se comprobó `git diff --check`.

## 2026-09-29 — Inicio de `fase-2` (commit `c1b024e`)

- `biology/unicellular_population_model.py`, `planets/planet.py`,
  `universe.py` y `ui/simulation_ui.py`: primera población simbólica por
  planeta con vida activa, persistente y visible en la vista 4.
- `tests/test_unicellular_population.py` y documentación: primer conjunto de
  pruebas y explicación. El commit se subió a `origin/fase-2`.

## Cierre de `fase-1` (commit `82b2a8d`)

- Se completaron habitabilidad y química prebiótica hasta protocélulas, la
  ampliación corta de reglas extraordinarias, abiogénesis y el criterio
  operativo de primera vida. El commit se subió a `origin/fase-1`.
- Primera vida es un indicador condicionado por una línea activa; el logro
  histórico permanece aunque la actividad desaparezca.
