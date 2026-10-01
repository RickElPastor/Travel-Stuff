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
| 5. Metabolismos y biosfera | Fuentes de energía, rutas metabólicas, posible fotosíntesis, efectos sobre la atmósfera, productores, consumidores, descomponedores y ecosistemas. | Base simbólica terminada y validada en `fase-3` |
| 6. Vida compleja | Multicelularidad, nichos, depredación, redes tróficas, extinciones masivas y radiaciones evolutivas, sin fecha obligatoria. | Base simbólica terminada y validada en `fase-4`; organismos complejos con tejidos quedan para más adelante |
| 7. Inteligencia | Inteligencia no garantizada, herramientas, aprendizaje social, comunicación, cultura, lenguaje y tecnología inicial. | Base simbólica terminada y validada en `fase-5`; inteligencia avanzada queda para etapas posteriores |
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

La rama `change_ui`, incorporada al recrear `fase-3`, prepara eventos universales y eventos
filtrados de sistemas, estrellas y planetas. El reloj universal sigue siendo
único; la vista planetaria entra en x1 y deriva una fecha numérica local del
periodo orbital al formarse cada planeta. Meses y días son convenciones de
visualización provisionales, no cultura ni rotación planetaria simulada.
Los calendarios que una civilización pudiera crear pertenecen a pasos
posteriores. Esta mejora de observación tampoco cuenta como metabolismo.

Primer bloque de metabolismo: las condiciones actuales distinguen luz,
geoquímica y orgánicos ambientales como fuentes potenciales. Una población
con primera vida y orgánicos disponibles recibe por ahora una ruta simbólica
de consumo. Esto permite mostrar una **base ecológica microbiana**: vínculo
entre compuestos del ambiente y la población. No asigna fotosíntesis ni
quimiosíntesis a partir de la mera presencia de luz o energía geoquímica.
Tampoco cambia aún crecimiento, extinción o atmósfera, ni constituye una red
trófica completa. Es una regla inicial de diseño, no una tasa medida.

Segundo bloque: una variante de un linaje vivo puede adquirir una capacidad
fotosintética simbólica si en ese nacimiento hay luz, agua líquida y CO₂. La
decisión usa un parámetro de diseño y azar local por nacimiento; descendientes
del linaje capaz la heredan. La ruta solo está activa mientras convivan esos
recursos y unidades capaces. La vista Biosfera distingue productores activos,
consumidores de orgánicos ambientales y la historia de la capacidad. Esto no
produce todavía materia orgánica, no aumenta población y no cambia atmósfera.
Un planeta iluminado sin variante capaz continúa sin fotosíntesis.

Tercer bloque: los productores activos generan una **proyección atmosférica
biológica actual** separada del CO₂ físico calculado antes de la vida. La
regla simbólica transforma un 1 % de ese CO₂ por unidad productora, con un
límite total del 5 %, y muestra un aporte equivalente de O₂ en bar. Son
parámetros de diseño, no una tasa real ni una acumulación geológica. Cuando
cesa la producción, la proyección vuelve al valor físico; guardar/cargar
conserva ambos valores. Todavía no retroalimenta clima, habitabilidad,
reproducción ni evolución, y no modela sumideros de oxígeno.

Cuarto bloque: una variante puede adquirir y transmitir capacidad
descomponedora en un entorno con orgánicos. El enlace ecológico de restos de
unidades muertas a descomponedores se muestra solo cuando hay muertes nuevas
en el paso y linajes capaces vivos. Las muertes históricas no quedan como
recurso actual perpetuo. La relación es cualitativa: todavía no hay reserva
de nutrientes, consumo de esa reserva ni beneficio para productores o
consumidores. No afecta los cálculos físicos, el clima o la población.

Quinto bloque: cada muerte nueva añade una unidad simbólica de restos. Los
descomponedores activos transforman los restos disponibles en nutrientes; la
ruta que consume orgánicos puede aprovecharlos. Las reservas y los totales
históricos se guardan. Una partida anterior no crea restos por muertes pasadas
al cargarse. Esta regla de diseño no mide materia real ni cambia todavía
crecimiento, extinción, clima o atmósfera. Un paso largo no reconstruye los
cambios ambientales intermedios, igual que otras reglas biológicas actuales.

### Cierre de la base de Fase 3

- [x] Fuentes potenciales y consumo inicial de orgánicos ambientales.
- [x] Capacidad fotosintética heredable y productores condicionados al entorno.
- [x] Proyección atmosférica biológica separada de la física normal.
- [x] Capacidad descomponedora heredable y ciclo de restos y nutrientes.
- [x] Revisión integral: 109 pruebas, caso combinado de las tres capas,
  guardado/carga, pantalla y universo nuevo desde el año 0.

La revisión encontró que procesar todos los restos al final de un salto largo
omitía descomponedores que habían aparecido y desaparecido dentro de él. Ahora
el ciclo sigue cada intervalo biológico reconstruido. En 200 semillas
controladas con entorno fijo, los estados finales coincidieron con pasos
cortos y largos. Un cambio ambiental no observado dentro de un salto sigue
fuera de la resolución temporal del simulador. La base de Fase 3 queda
terminada; aún no incluye crecimiento dependiente de nutrientes, depósitos
geoquímicos realistas ni vida compleja. El paso 6 empieza en `fase-4`, después
de publicar el cierre de `fase-3`.

Explicar primero al usuario el alcance y trabajar por bloques pequeños:
fuentes de energía y metabolismo simbólico; rutas metabólicas como posible
fotosíntesis si las condiciones lo permiten; efectos biológicos sobre la
atmósfera; roles de productores, consumidores y descomponedores; y primeras
relaciones de ecosistema. Mantener el surgimiento contingente, el determinismo,
la persistencia y la física normal. La multicelularidad, los nichos, la
depredación y las redes tróficas corresponden al paso 6, no a esta base.

### Inicio de Fase 4 — Vida compleja

La rama `fase-4` nace del cierre de `fase-3`. El primer bloque modela
**colonias celulares simples**, una etapa inicial y simbólica de
multicelularidad. Una variante puede adquirir cohesión en un entorno con vida,
agua líquida y orgánicos; sus descendientes heredan esa capacidad. Dos unidades
vivas del mismo linaje cohesivo forman una colonia simbólica. El número actual
depende de las unidades y del entorno; el hito histórico permanece aunque la
colonia se disuelva o la vida se extinga. La probabilidad de adquirir cohesión
es un parámetro de diseño, no una tasa observada. Cada nacimiento usa azar local
para preservar el determinismo. El estado se guarda y los archivos anteriores
empiezan sin esa capacidad ni colonias inventadas.

La colonia todavía no tiene tejidos, órganos, reproducción propia ni ventajas
ecológicas. No consume unidades, altera el crecimiento ni cambia la física, el
clima o la atmósfera.

El segundo bloque consulta **nichos de recursos por especie viva**. Cuenta
unidades capaces de aprovechar orgánicos ambientales, luz o restos según las
rutas activas ya calculadas. Una especie puede ocupar varios nichos y otra
quedar sin recurso modelado; esto último no provoca automáticamente su muerte.
No son hábitats espaciales ni especializaciones nuevas. Es una consulta del
estado actual, sin azar ni campos nuevos: el guardado conserva los datos de
origen y al cargar se reconstruye la misma ocupación. La vista Biosfera resume
cuántas especies ocupan cada recurso; los conteos pueden solaparse. En ese
bloque no se añadieron competencia ni depredación.

El tercer bloque añade una **primera depredación simbólica**. Una variante con
vida y al menos dos unidades puede adquirir capacidad depredadora; sus hijas
la heredan. Si hay unidades de otra especie viva en el mismo planeta, un
encuentro puede elegir una de ellas como presa. Los parámetros de adquisición
y encuentro (`0.0625` y `0.5`) son elecciones de diseño, no tasas medidas.
El encuentro se decide con azar local ligado a la semilla y al nacimiento del
intervalo. La captura determina cuál unidad muere en el recambio que ya
existía: cambia la composición de especies, pero no añade una muerte ni
aumenta la población. La presa consumida no se duplica como resto orgánico.
El número acumulado y la última relación depredador-presa se guardan. Los
guardados anteriores empiezan sin depredadores ni capturas.

El nicho de presas señala capacidad y presencia de otra especie; no garantiza
una captura en cada intervalo. Todavía no hay ventaja reproductiva por comer
ni competencia explícita por recursos.

El cuarto bloque construye una **red trófica actual** a partir de los nichos
vivos: luz, orgánicos y restos apuntan a las especies que los aprovechan;
una especie presa apunta a otra capaz de depredarla. El sentido de la flecha
es «fuente de energía o presa → consumidor». Los enlaces de presas son
**posibilidades**, no capturas realizadas. La red no inventa interacciones,
no altera población ni recursos y no añade campos de guardado; al cargar se
reconstruye desde capacidades y especies persistidas. La vista `R` desde
Biosfera permite recorrer todos los enlaces de un planeta, incluso cuando no
caben en una sola pantalla. Un planeta sin vida puede tener una red vacía.

El quinto bloque reconoce una **extinción masiva local** cuando un planeta
pasa de vida activa a inactiva y pierde al menos dos especies que estaban
vivas al comenzar la actualización. El umbral de dos es operativo y de diseño,
no una definición paleontológica. Se guardan el número de episodios, el año y
las especies del último episodio. El evento sustituye a la extinción local
genérica para no duplicarlo y, si cambió el estado del agua, muestra ambos
valores como observación, sin declarar que ese cambio fue la causa única.
No añade una catástrofe ni muertes: usa la pérdida de viabilidad ya calculada
por el simulador. Tampoco implica que se extinguió la vida de todo el universo.
Un salto temporal solo observa las condiciones en sus extremos; no puede
reconstruir episodios que nacieron y terminaron dentro del salto. Los guardados
anteriores empiezan sin episodios retrospectivos.

El sexto bloque reconoce una **radiación evolutiva simbólica** cuando aparece
una nueva especie y coexiste con otra especie hija directa del mismo ancestro.
Los nacimientos de las dos especies deben distar como máximo 12 nacimientos
biológicos; la ventana es un parámetro de diseño para expresar cercanía en
la historia de reproducción, no una tasa real en años. Se cuenta una vez por
especie ancestral, aun si esta ya se extinguió. La detección ocurre después
del recambio de cada intervalo biológico, por lo que un salto temporal largo
no oculta una coexistencia que luego termine. No se cuentan dos especies
distintas sin parentesco conocido ni la mera coexistencia de progenitora e
hija. La lista de ancestros y la última pareja se guardan; un guardado antiguo
comienza sin radiaciones retrospectivas. El evento se fecha al final del paso
que la observó, igual que otros hitos planetarios.

El nombre no implica adaptación comprobada a nichos diferentes ni una
recuperación obligatoria después de una extinción masiva. Esta primera regla
solo reconoce ramificación y cercanía de nacimientos; no añade especies,
ventajas reproductivas, azar, consumo de recursos ni cambios físicos.

### Cierre de la base de Fase 4

- [x] Colonias celulares simples y capacidad de cohesión heredable.
- [x] Nichos de recursos por especie viva.
- [x] Depredación simbólica entre especies sin muertes adicionales.
- [x] Red trófica actual de recursos y presas posibles.
- [x] Extinciones masivas locales observadas.
- [x] Radiaciones evolutivas por ramificación real de especies.
- [x] Revisión integral: caso controlado que une los seis sistemas, pasos
  cortos/largos, guardado/carga, extinción, pantalla y universo desde el año 0.

La base simbólica de Fase 4 queda terminada. La red trófica no calcula flujo
de energía, cantidades consumidas ni fuerza de competencia. Las colonias no
tienen tejidos ni órganos; «radiación» no demuestra adaptación a nichos.
Tampoco hay inteligencia o civilizaciones, que pertenecen a pasos posteriores.
La revisión integral no amplía estas reglas más allá de lo comprobado.

### Inicio de Fase 5 — Inteligencia no garantizada

La rama `fase-5` parte del cierre de `fase-4`. Esta fase avanzará por bloques:
condiciones precursoras, aprendizaje y memoria, posible transmisión social,
herramientas, comunicación, cultura y lenguaje inicial, y tecnología temprana.
Cada capacidad deberá depender de especies vivas y condiciones comprobables;
ninguna se asignará por una fecha fija. Asentamientos, gobiernos, territorios y
civilizaciones corresponden al paso 8 y quedan fuera de esta fase.

El primer bloque es una **consulta de candidatas**, no una declaración de
inteligencia. Requiere al menos una colonia celular actual de un mismo linaje
y acceso actual a dos recursos modelados en la especie. Dos es un umbral de
diseño para preparar el siguiente modelo, no una medida científica de mente.
Una especie puede tener varios nichos sin ser candidata, o formar colonia con
un solo recurso sin serlo. Se usan los linajes, especies, colonias y nichos ya
persistidos; la consulta no añade azar, campos de guardado, eventos, nacimientos,
muertes ni cambios físicos. Al cargar se reconstruye el mismo resultado.
La vista `I` desde Biosfera enumera las candidatas y explica que todavía no
hay inteligencia demostrada. Cero candidatas es un resultado normal.

El segundo bloque añade una **memoria simbólica de rutas adicionales**. Al
observar una especie candidata, registra por primera vez las rutas de luz,
restos o presas posibles que estaban disponibles; los orgánicos no se anotan
porque ya son requisito ambiental de la colonia. La prioridad actual es la
primera ruta recordada que sigue disponible. Si deja de estarlo, puede
priorizar otra conocida y recuperar la anterior cuando vuelva. Cada especie
guarda su propia lista en orden de descubrimiento. Sin candidatura no añade
recuerdos; la memoria histórica no se borra al extinguirse la especie. Los
guardados anteriores comienzan vacíos y pueden aprender en actualizaciones
futuras. La regla no se hereda entre especies ni cambia consumo, reproducción,
supervivencia, clima o física: es una primera preferencia observable, no
inteligencia avanzada ni ventaja adaptativa comprobada.

La observación ocurre al final de cada actualización del entorno. Con un
entorno estable, repetir pasos no duplica recuerdos; un salto largo puede
omitir una ruta que apareció y desapareció entre sus extremos, límite temporal
del simulador que no se presenta como una observación precisa.

El tercer bloque distingue el resumen histórico por especie de la **memoria
de cada linaje con colonia**. Un linaje registra directamente una ruta extra
solo si tiene la capacidad correspondiente y su especie es candidata. Cuando
dos linajes de la misma especie tienen colonias activas, uno puede compartir
una ruta que recuerda con el otro. Se cuenta cada ruta nueva recibida una sola
vez; no cruza especies, no concede la capacidad biológica de usar esa ruta y
no altera recursos, población ni física. Los guardados anteriores empiezan
sin memorias por linaje ni transmisiones inventadas; la lista histórica por
especie sigue disponible y los linajes pueden registrar recursos en futuras
actualizaciones. El intercambio se observa al final de cada actualización;
los encuentros transitorios dentro de saltos largos pueden quedar fuera.

El cuarto bloque reconoce un **ensayo simbólico de soporte orgánico externo**:
una especie candidata tiene una colonia actual cuyo linaje recuerda la ruta de
restos, y el planeta tiene restos pendientes o reciclados durante la
actualización observada. En ese estado, el modelo señala un posible uso como
apoyo; guarda por especie que el ensayo ocurrió alguna vez, aunque desaparezca
el material o la colonia. Una ruta recordada por otro linaje sin colonia no
basta. La observación no consume restos, fabrica un objeto, asigna órganos ni
mejora alimentación o supervivencia. Tampoco representa herramientas animales
o tecnología. Es una regla de diseño para iniciar la conducta de uso externo,
no una afirmación científica sobre organismos unicelulares. Se guarda cuánto
material se encontró en el intervalo, aunque el ciclo orgánico lo haya
reciclado después; saltos largos aún pueden omitir otras oportunidades breves.
Los guardados antiguos empiezan sin esta observación ni el hito.

El quinto bloque añade una **señal inicial de recurso** distinta del recuerdo
compartido. Dos linajes vivos de la misma especie candidata deben mantener
colonias. El emisor recuerda una ruta que puede usar biológicamente y está
disponible ahora; el receptor es otro linaje con colonia de esa especie. La
consulta muestra emisor, receptor y recurso. La señal deja de estar activa si
falta la ruta, la capacidad o alguna colonia. Por especie se guarda solo el
hito de haber tenido una señal, sin contar repetidamente el mismo aviso por
cada paso temporal. Para restos se exige material pendiente u observado y
reciclado en el intervalo, no solo una capacidad descomponedora marcada.

La regla representa un aviso temporal de oportunidad, mientras la transmisión
social conserva memoria histórica. El aviso no otorga capacidades ni cambia
consumo, población, ambiente o física. No simula sonido, gestos, vocabulario,
significado complejo ni lenguaje. Como otras consultas de esta fase, observa
el estado al final de la actualización; un aviso transitorio dentro de un
salto largo puede no registrarse. Guardados anteriores empiezan sin el hito.

El sexto bloque reconoce una **práctica compartida incipiente** cuando dos
linajes de una misma especie candidata, ambos con colonias, emiten avisos
recíprocos sobre la misma ruta de recurso disponible. Un aviso en un solo
sentido, o dos avisos sobre rutas distintas, no bastan. Se guarda por especie
la ruta que alguna vez cumplió el criterio; repetir la observación no añade
copias. La práctica está activa solo mientras los dos avisos siguen siendo
posibles. La historia persiste si desaparece la ruta o la especie se extingue.

Es una convención operacional muy pequeña, no una cultura antropológica:
no hay normas, tradiciones elaboradas, lenguaje, símbolos compartidos ni
ventajas ecológicas nuevas. Requiere las capacidades y memorias actuales de
ambos linajes; un recuerdo social sin capacidad biológica no inventa un aviso
de vuelta. La regla no altera evolución, recursos ni física. Los guardados
anteriores comienzan sin prácticas inventadas. Como el resto de esta etapa,
solo observa el final de cada actualización y puede omitir episodios breves
dentro de saltos largos.

El séptimo bloque modela un **repertorio de códigos inicial**: una especie debe
mantener prácticas recíprocas actuales sobre al menos dos rutas de recurso
distintas. Entonces asigna etiquetas abstractas `C1`, `C2` y siguientes a las
rutas en el orden del primer reconocimiento, propias de esa especie. Una sola
práctica no basta; una tercera ruta recibe el siguiente código sin cambiar los
anteriores. El repertorio histórico se guarda y permanece aunque la especie
se extinga o el recurso desaparezca. Se considera activo solo si al menos dos
rutas ya codificadas mantienen prácticas actuales. Los guardados anteriores
comienzan sin códigos inventados y pueden adquirirlos al continuar.

Los códigos son identificadores internos del simulador para distinguir
referentes, no sonidos, palabras pronunciadas, gramática ni demostración de
lenguaje humano. Dos rutas es un umbral de diseño. No altera comunicación,
consumo, población ni física; observa solo el final de cada actualización, por
lo que un salto largo puede omitir una combinación pasajera.

El octavo bloque reconoce una **técnica temprana de soporte recuperado**. La
especie debe haber observado el uso de soporte orgánico y contar con un
repertorio histórico que codifique `restos`. Si sigue viva, con colonia que
recuerda esa ruta, y después se observa una actualización sin material, el
planeta guarda la escasez. Solo cuando reaparecen restos y al menos dos
linajes con colonias pueden usar soporte mientras está activo el código de
`restos`, se registra el método compartido. Repetir actualizaciones con el
material siempre presente no crea la técnica. La historia persiste al cesar
la actividad; los guardados anteriores no inventan escasez ni técnicas.

La técnica es una regla de diseño para reconocer recuperación de un
procedimiento, no una tecnología manufacturera. No prepara ni almacena
objetos, no consume restos ni mejora la supervivencia. Las transiciones solo
se observan al final de las actualizaciones; un salto largo que oculte una
escasez transitoria no la registrará. La física normal y el ciclo orgánico
siguen calculándose sin modificaciones.

### Cierre de Fase 5

- [x] Candidatas por colonias y recursos, memoria de rutas y transmisión social.
- [x] Ensayo de soporte, señales recíprocas y práctica compartida.
- [x] Códigos iniciales y técnica de soporte recuperado tras escasez.
- [x] Revisión integral: el material reciclado durante un intervalo puede
  observarse sin alterar el balance orgánico; pruebas controladas de la cadena
  completa, guardado/carga, compatibilidad y universo nuevo desde el año 0.

La base simbólica de Fase 5 queda terminada. Son umbrales de diseño para
conductas precursoras; no hay inteligencia humana, lenguaje hablado,
organismos macroscópicos ni civilizaciones. El paso 8 comienza en `fase-6`.

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
