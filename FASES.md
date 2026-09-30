# Hoja de ruta de Travel Stuff

Este documento sigue el plan entregado por el creador del proyecto. Debe
consultarse antes de cada bloque de desarrollo y actualizarse cuando cambie el
estado real del código. Sustituye la división anterior en seis fases: el plan
original enumera **diez pasos de trabajo**, además de ideas para mucho más
adelante. Esos pasos no implican diez ramas de Git.

## Objetivo y reglas permanentes

Travel Stuff simula un universo, vida e historia **emergente**. Construimos
reglas, condiciones, eventos y consecuencias; no escribimos una cronología
predeterminada ni forzamos la aparición de vida o civilizaciones. Un universo
sin vida es un resultado válido.

- Continuar el proyecto existente sin rehacer sistemas que funcionan.
- Mantener módulos con responsabilidades claras y `main.py` como entrada.
- Mantener la interfaz principalmente en terminal; no añadir GUI ni Pygame
  todavía. Separar datos en vistas cuando falte espacio.
- Conservar el determinismo: misma semilla y estado deben dar la misma
  historia. Guardar/cargar y cambiar el tamaño de los pasos temporales no
  deben alterar resultados solo por el número de actualizaciones.
- Etiquetar por separado datos observacionales, modelos publicados,
  aproximaciones, parámetros de diseño, límites computacionales y ficción.
  No presentar parámetros elegidos como probabilidades científicas medidas.
- Calcular siempre la física normal; las reglas extraordinarias son una capa
  adicional y no borran sus resultados.
- Persistir cada estado nuevo y probar continuidad y compatibilidad razonable
  con guardados anteriores. No cambiar la versión del guardado sin necesidad.
- Trabajar en cambios pequeños, explicables y verificables. Al cerrar cada
  fase validada, hacer commit y push; al iniciar la siguiente, explicar su
  alcance y crear/cambiar a su rama `fase-N` en GitHub. No cerrar una fase con
  fallos pendientes.

## Estado de ramas y sistemas existentes

`fase-1` cerró la base del simulador: motor, tiempo, semilla, eventos,
guardado/carga, astronomía, formación planetaria, habitabilidad y química
prebiótica hasta protocélulas. También cerró la ampliación corta de reglas
extraordinarias, abiogénesis y el criterio operativo de primera vida.

`fase-2` cierra la base de evolución biológica. Tiene una población unicelular **simbólica**
por planeta con vida activa: tamaño actual, nacimientos y muertes por
intervalo, extinción si cesa la vida activa, un rasgo heredable y variable
de una línea observada, y varios rasgos y linajes simbólicos que pueden
coexistir entre unidades vivas. Una primera regla de selección biológica
según el agua actual compara los linajes vivos antes de cada nacimiento y
decide el origen de la descendencia. También evalúa las variantes nuevas;
la pantalla muestra el ajuste de la línea y cuántos linajes están ajustados.
Los estados de los que dependen persisten. Es un inicio del paso 4, no un
sistema completo de evolución biológica. Las unidades de población no
equivalen a células contadas; los linajes tienen identidad persistente y
competencia reproductiva básica e historial de progenitores que permanece
tras la extinción. Las especies simbólicas se clasifican por parentesco y
dos variaciones encadenadas por rama; su identidad persiste y su extinción
se reconoce al perder la última unidad. El umbral es una regla de diseño,
no una definición científica. Aún no hay competencia por recursos.
Si desaparece el linaje observado,
se sigue otro que permanece vivo; su identidad persiste al guardar y cargar.
La selección prebiótica de `abiogenesis/` es otra capa.

## Secuencia original de diez pasos

| Paso | Trabajo previsto | Estado actual |
| --- | --- | --- |
| 1. Reglas extraordinarias, ampliación corta | Arcano, anomalía física y energía exótica pueden apoyar química/protocélulas sin sustituir la física normal. La fantasía profunda queda para después. | Hecho en `fase-1` |
| 2. Abiogénesis | Separar protocélula de vida; replicación, herencia, variación y selección prebióticas sin probabilidad científica inventada. | Hecho en `fase-1` |
| 3. Primera vida | Criterio operativo para reconocer una línea viva simple, sin asumir que toda protocélula lo logra. | Hecho en `fase-1` |
| 4. Evolución biológica | Reproducción, herencia, mutación, selección, adaptación, linajes, especies, extinción y diversificación. La vida puede permanecer microbiana. | Base simbólica terminada en `fase-2`; modelos biológicos más profundos quedan para etapas posteriores |
| 5. Metabolismos y biosfera | Fuentes de energía, rutas metabólicas, posible fotosíntesis, efectos sobre la atmósfera, productores, consumidores, descomponedores y ecosistemas. | Siguiente: `fase-3` |
| 6. Vida compleja | Multicelularidad, nichos, depredación, redes tróficas, extinciones masivas y radiaciones evolutivas, sin fecha obligatoria. | Pendiente |
| 7. Inteligencia | Inteligencia no garantizada, herramientas, aprendizaje social, comunicación, cultura, lenguaje y tecnología inicial. | Pendiente |
| 8. Civilizaciones | Asentamientos, culturas, territorios, gobiernos, recursos, comercio y tecnologías. Ninguna civilización es obligatoria. | Pendiente |
| 9. Historia dinámica | Guerras, alianzas, migraciones, revoluciones, descubrimientos, catástrofes y otros eventos emergentes; nunca una cronología fija. | Pendiente |
| 10. Religiones | Creencias, cultos, mitologías, conversiones, divisiones y desapariciones según condiciones e historia, sin fecha obligatoria. | Pendiente |

### Trabajo inmediato en el paso 4

El seguimiento de diversificación deriva del historial la especie progenitora
y las hijas directas, cuenta unidades vivas por especie y detecta coexistencia
de dos o más especies por planeta. La vista 5 lo presenta. No fuerza que varias
especies sobrevivan ni convierte la primera vida en garantía de crecimiento.
La revisión integral probó un universo nuevo con el mismo modelo estelar que el
juego: desde el año 0 hasta 3 000 millones, con primera vida, coexistencia,
extinción y continuidad de guardado/carga. Las pruebas de pantalla cubren la
terminal mínima; el siguiente bloque pertenece al paso 5.

### Cierre de la base de Fase 2

El alcance actual de `fase-2` es la base simbólica de evolución biológica
del paso 4. No incluye todavía metabolismos, biosfera ni vida compleja.

- [x] Población, reproducción, mortalidad y extinción total.
- [x] Herencia, variación y selección reproductiva según el entorno.
- [x] Identidad, coexistencia y parentesco persistente de linajes.
- [x] Criterio operativo de especies, identidad y seguimiento de su extinción.
- [x] Diversificación: seguimiento de ramificación, abundancia y coexistencia.
- [x] Revisión integral: universo nuevo desde cero, guardar/cargar,
  continuación determinista y pantalla automatizada.

La base de Fase 2 queda terminada. El paso 5 de la hoja de ruta comienza en
`fase-3`; el simulador todavía no representa metabolismos o ecosistemas.

### Inicio de Fase 3 — Metabolismos y biosfera

Antes de agregar metabolismo, se ordenaron los módulos del universo y de
estrellas y se cambió la interfaz a una exploración por catálogos de sistemas,
estrellas y planetas. Todavía no existe un modelo de galaxias; la navegación
parte del universo directamente a los sistemas o las estrellas. Esta
preparación de estructura e interfaz no cuenta como metabolismo implementado.

La rama `change_ui`, creada desde `fase-3`, prepara eventos universales y eventos
filtrados de sistemas, estrellas y planetas. El reloj universal sigue siendo
único; la vista planetaria entra en x1 y deriva una fecha numérica local del
periodo orbital al formarse cada planeta. Meses y días son convenciones de
visualización provisionales, no cultura ni rotación planetaria simulada.
Los calendarios que una civilización pudiera crear pertenecen a pasos
posteriores. Esta mejora de observación tampoco cuenta como metabolismo y
queda pendiente integrarla en `fase-3` cuando se retome ese trabajo.

Explicar primero al usuario el alcance y trabajar por bloques pequeños:
fuentes de energía y metabolismo simbólico; rutas metabólicas como posible
fotosíntesis si las condiciones lo permiten; efectos biológicos sobre la
atmósfera; roles de productores, consumidores y descomponedores; y primeras
relaciones de ecosistema. Mantener el surgimiento contingente, el determinismo,
la persistencia y la física normal. No añadir aún multicelularidad, nichos
profundos, depredación ni vida compleja: eso corresponde al paso 6.

## Horizontes posteriores, todavía sin paso inmediato

- **Dios real/usuario:** podría existir dentro de la ficción y ser conocido,
  interpretado o ignorado por sus habitantes.
- **Fantasía profunda:** magia, criaturas, vampirismo con rutas diversas,
  artefactos y magitecnología, solo en mundos donde surjan causas y reglas.
  Deben coexistir mundos normales, fantásticos, anómalos y de ciencia ficción.
- **Personajes y familias:** vidas individuales, relaciones, descendencia,
  árboles familiares e historia personal después de civilizaciones e historia.
- **Tecnología:** desarrollo no lineal; las sociedades pueden avanzar,
  estancarse, retroceder, colapsar o combinar magia y tecnología.
- **Viajes temporales y realidades alternativas:** mucho más adelante, después
  de consolidar una única línea temporal.
- **Juego:** eventual modo de persona normal y modo dios. Por ahora se
  construye el cerebro de la simulación, no gameplay profundo.

## Forma de revisar cada bloque

Al terminar un cambio, explicar **qué archivos cambiaron y por qué**, dónde
revisar las clases y métodos, qué lógica de Python conviene entender, qué
probar y qué resultado esperar. Cerrar indicando el siguiente bloque y lo que
falta para completar el paso actual. El usuario está aprendiendo Python:
preferir código simple que pueda explicar línea por línea.
