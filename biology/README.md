# Vida unicelular: primer paso de Fase 2

[`ModeloPoblacionUnicelular`](unicellular_population_model.py) observa el
indicador `vida_activa` calculado al final de la abiogénesis. Cuando aparece,
funda una población de **una unidad simbólica** y registra un nacimiento. Cada
millón de años con vida activa aplica esta regla de diseño:

1. Si hay al menos dos unidades, una muere.
2. Un nacimiento reemplaza esa pérdida.
3. Si la población aún no alcanzó ocho unidades, otro nacimiento la hace crecer
   en una unidad. Cuando solo hay una unidad, no muere ninguna y nace otra.

Al llegar a ocho, la población permanece en ocho, pero sigue habiendo un
nacimiento y una muerte en cada intervalo. Los números organizan el juego: no
cuentan células ni representan tasas biológicas medidas. Todavía no se modelan
competencia por recursos. Las especies simbólicas y la selección entre
linajes para dejar descendencia se explican al final de este documento.

Si `vida_activa` se pierde, todas las unidades actuales se registran como
muertes, la población llega a cero y el crecimiento programado se limpia. Si
aparece de nuevo, comienza una población nueva. Los contadores históricos de
nacimientos y muertes, y `alcanzo_primera_vida`, permanecen. La evaluación se
ejecuta después de la primera vida y no altera habitabilidad, química ni la
línea de copias de Fase 1.

El tamaño, los nacimientos, las muertes y el próximo año de crecimiento se
guardan con el planeta. Un guardado anterior carece de esos campos y carga
ceros; al avanzar, puede fundar una población si todavía hay vida activa.
Repetir la evaluación en el mismo año no duplica el crecimiento. El modelo
calcula juntos los intervalos pendientes, para dar el mismo resultado con
pasos cortos o largos mientras la vida siga activa. En la vista **4 Vida** se
observan mundos activos, unidades actuales y nacimientos/muertes históricos,
incluso después de una extinción.

Para revisar el cambio, mira primero el `if not planeta.vida_activa` y luego
la fundación y el cálculo de `intervalos`. Prueba con un universo nuevo y,
cuando aparezca primera vida, cambia a la vista 4. Guarda y carga mientras
haya una población para comprobar que conserva tamaño y contadores. Si se
extingue, espera tamaño cero y muertes acumuladas; la primera vida histórica
debe seguir registrada. Los ceros anteriores a la primera vida son esperados.
La prueba automática específica es:

```sh
.venv/bin/python -m unittest tests.test_unicellular_population -v
```

## Herencia y variación biológicas

[`ModeloHerenciaVariacionUnicelular`](inheritance_variation_model.py) sigue
**una línea observada** dentro de la población. Su rasgo vale 0, 1 o 2: son
etiquetas abstractas, no genes reales. La fundadora comienza con 1. Cada
nacimiento posterior hereda el rasgo del linaje elegido entre los vivos por
su ajuste al agua actual. Una probabilidad
del 25 % elegida para el simulador puede cambiarlo a una de las otras dos
etiquetas. Cuando eso ocurre, el módulo de selección decide cuál de los dos
rasgos continúa **la línea observada**. No afirmamos que sea el rasgo
dominante de toda la población.

La decisión de variar usa un generador local ligado a la semilla del universo,
el sistema, el planeta y el número histórico de nacimiento. No consume el azar
global del universo y un mismo nacimiento da el mismo resultado aunque el
tiempo avance en bloques distintos. `nacimientos_biologicos_procesados` evita
repetir nacimientos al evaluar otra vez o tras cargar. El rasgo actual se
limpia al extinguirse la población; `variaciones_unicelulares` conserva el
total histórico. Una nueva fundadora reinicia el rasgo en 1.

Los tres campos se guardan con el planeta. En guardados anteriores, el rasgo
empieza sin asignar, las variaciones en cero y los nacimientos antiguos se
consideran procesados: no inventamos mutaciones retrospectivas. La vista
**4 Vida** muestra el rasgo de la línea y las variaciones históricas. Si la
vida activa dura poco, un cero en variaciones es un resultado válido.

Para entender el código, sigue el orden de `evaluar`: extinción, fundadora y
nacimientos nuevos. Comprueba después que la semilla de cada nacimiento incluye
su número y que el patrón químico `patron_copia` nunca se modifica aquí. La
prueba específica es:

```sh
.venv/bin/python -m unittest tests.test_unicellular_inheritance -v
```

## Selección biológica inicial

[`ModeloSeleccionUnicelular`](selection_model.py) compara el rasgo anterior
con una variante cuando ocurre un nacimiento con variación. El agua actual del
planeta determina una preferencia de **diseño**: en hielo se favorece la
etiqueta 0; en agua líquida, la 2. Una variante continúa la línea observada
solo si coincide con la etiqueta favorecida y la anterior no. Los empates, las
variantes no favorecidas y los estados de agua sin regla conservan el rasgo
anterior. No se modifican el agua, la habitabilidad, la química ni el tamaño
de la población.

`variantes_biologicas_favorecidas` cuenta las variantes que pasaron a la línea
observada; `variantes_biologicas_descartadas` cuenta las que no pasaron. Una
variante descartada **sí** cuenta como variación, pero «descartada» no significa
que haya muerto una unidad de población. Los contadores son históricos y
persisten al extinguirse la población. En un universo nuevo, la suma de ambos
coincide con `variaciones_unicelulares`.

La selección no añade azar: recibe las variantes ya creadas por el modelo de
herencia. Con agua constante, evaluar los mismos nacimientos en pasos largos o
cortos da el mismo resultado. Si el agua cambia entre observaciones, un paso
muy grande no puede reconstruir todos los estados intermedios: esa es una
limitación de la resolución temporal actual, no una tasa científica. La vista
**4 Vida** muestra variantes favorecidas y descartadas del mundo observado.

Para revisar, lee `elegir` y luego el lugar donde `evaluar` lo llama cuando
aparece una variación. Prueba en un universo nuevo; es válido que ambos
contadores permanezcan en cero si no hubo suficientes nacimientos. La prueba
específica es:

```sh
.venv/bin/python -m unittest tests.test_unicellular_selection -v
```

En una corrida completa con semilla `374852300` y pasos de 20 millones de
años, se observó primera vida y población 1 cerca del año 2 780 000 000.
En la siguiente observación, cerca del 2 800 000 000, el estado de
habitabilidad pasó a `co2_excesivo`, la protocélula dejó de ser viable y la
población llegó a cero. Variación y selección biológicas permanecieron en
cero porque no hubo otro nacimiento durante la vida activa observada. Ese
resultado es válido para esa semilla y resolución temporal; no es un objetivo
numérico para todos los universos.

## Ajuste al agua actual

`esta_ajustada` en [el modelo de selección](selection_model.py) compara el
rasgo de la línea activa con el favorecido por el agua **actual**. Devuelve
`True` solo si hay población, el agua tiene una regla definida y ambos rasgos
coinciden. Si el agua cambia, puede pasar a `False` sin que haya una mutación;
una variante favorecida posterior puede devolverlo a `True`. La vista **4
Vida** muestra «ajuste agua sí/no» para el mundo observado.

Es un primer indicador de adaptación, no una nueva capacidad de supervivencia
ni una medida científica. No se guarda otro campo: el valor se vuelve a
calcular a partir de población, rasgo y agua, que ya se guardan. Así no puede
quedar desactualizado después de cargar o de un cambio ambiental. Para probar
el cambio de estado sin esperar un universo raro, ejecuta:

```sh
.venv/bin/python -m unittest tests.test_unicellular_selection -v
```

## Rasgos que coexisten en la población

`rasgos_unicelulares_vivos` guarda un rasgo 0, 1 o 2 por cada **unidad
simbólica** viva. La fundadora empieza con `[1]`; cada nacimiento añade el
rasgo heredado o su variante. Una variante «descartada» por la selección de
la línea observada todavía puede aparecer entre las unidades vivas: esa
selección decide qué rasgo sigue la línea observada, no mata a la variante.
Cuando hay muertes, salen las unidades más antiguas y quedan los últimos
nacimientos. Al extinguirse la población, la lista se vacía; los contadores
históricos permanecen.

La lista se guarda con el planeta. Si un guardado anterior no la contiene,
las unidades existentes se inicializan con el rasgo de su línea observada;
si tampoco existe ese rasgo, con 1. Es una suposición de compatibilidad, no
una reconstrucción de diversidad pasada. En la vista **4 Vida**, la fila
«Rasgos vivos» muestra cuántos grupos de rasgos hay y cuántas unidades tienen
cada etiqueta en el mundo observado. Por ejemplo, `0:1 1:0 2:2` significa
una unidad con rasgo 0 y dos con rasgo 2. Un grupo de rasgos puede contener
varios linajes: compartir una etiqueta no significa tener la misma identidad.

Para entenderlo, sigue la lista desde la fundadora, un nacimiento con
variación y la extinción. Después prueba guardar/cargar un mundo con varios
rasgos visibles; los tres conteos deben conservarse. La prueba específica es:

```sh
.venv/bin/python -m unittest tests.test_unicellular_inheritance -v
```

## Identidad de los linajes unicelulares

`linajes_unicelulares_vivos` acompaña a la lista de rasgos: cada posición
pertenece a la misma unidad en ambas listas. La fundadora recibe como
identificador su número histórico de nacimiento. Un nacimiento sin variación
hereda el identificador observado; una variante recibe uno nuevo, aunque la
selección no la elija para continuar la línea observada. Son identificadores
locales de cada planeta. Un linaje puede compartir rasgo con otro. La especie
es una clasificación distinta que puede agrupar varios linajes; se explica
al final junto con el registro de parentesco.

Por ejemplo, rasgos `[1, 0, 0]` y linajes `[1, 2, 2]` describen tres unidades
vivas: una del linaje 1 y dos del linaje 2. `linaje_observado_id` indica cuál
seguimos para los próximos nacimientos. Al completar cada intervalo se
retiran las unidades más antiguas; si desaparece el linaje observado, seguimos
la unidad más reciente que permanece viva. Este relevo no incrementa
«favorecidas» ni «descartadas»: solo mantiene una fuente viva de descendencia.
También puede cambiar el indicador de ajuste al agua.

El modelo de herencia reconstruye los intervalos pendientes usando la regla
del modelo de población: un nacimiento si había una unidad o ya se alcanzó la
capacidad; dos cuando hay reemplazo y crecimiento. Así aplica los relevos en
el mismo orden con pasos cortos o largos, mientras el entorno se mantenga.
En Python, el `while` recorre esos intervalos y el `for` sus nacimientos;
`_registrar_nacimiento` y `_mantener_linea_viva` separan las dos tareas.

Las identidades se guardan con el planeta. La extinción total vacía las dos
listas y deja la identidad observada en `None`. Una nueva fundadora utiliza
otro número de nacimiento; no recupera el identificador de una línea extinta.
Un guardado anterior sin identidades recibe grupos provisionales por rasgo:
`-1` para el rasgo 0, `-2` para el 1 y `-3` para el 2. El signo negativo indica
que desconocemos su historia previa y evita colisiones con nuevos linajes.

La vista **4 Vida** añade «linajes» al número de grupos vivos y muestra el
identificador observado junto a «Rasgo» y «Origen». Prueba un universo nuevo y,
si aparece vida, observa que una variante puede aumentar los linajes vivos;
también pueden disminuir cuando desaparecen sus últimas unidades. Guarda y
carga en pausa para comparar los mismos valores. Es válido que se mantenga un
solo linaje o que la vida no dure lo suficiente para ramificarse. Para probar
los casos de forma controlada:

```sh
.venv/bin/python -m unittest tests.test_unicellular_lineages -v
```

## Selección entre linajes vivos

Antes de cada nacimiento nuevo, `elegir_linaje_reproductor` compara los
linajes vivos. Reutiliza la regla simbólica existente: hielo favorece el
rasgo 0 y agua líquida favorece el 2. Es una regla de diseño, no una medida
biológica. Decide el origen de la descendencia así:

1. Si el linaje observado está ajustado, lo conserva, incluso si otros
   también lo están.
2. Si solo otros linajes están ajustados, elige el de la primera unidad
   ajustada en la lista viva. El orden de las listas se conserva al guardar.
3. Si ninguno está ajustado, o no hay regla para ese estado del agua,
   continúa el observado. Si este ya desapareció, sigue una unidad viva.

El nacimiento hereda el rasgo y la identidad elegidos, y después puede variar
con la regla de mutación existente. Por ejemplo, con dos linajes de rasgos
0 y 2, un cambio de hielo a agua líquida puede pasar la descendencia al de
rasgo 2. No necesita aparecer una mutación nueva para que ocurra ese relevo.
Por eso no incrementa los contadores de variantes favorecidas/descartadas:
esos siguen contando únicamente la evaluación de variantes nuevas.

Los linajes no elegidos continúan vivos hasta perder sus unidades por las
reglas de mortalidad. El total de nacimientos, muertes y la capacidad siguen
dependiendo del modelo de población. Estar ajustado no evita la extinción
cuando desaparece la vida activa. Esta es una competencia reproductiva
inicial; aún no simula recursos ni nichos. La clasificación de especies
registra los grupos resultantes sin cambiar esa regla reproductiva.

En Python, `zip` recorre juntos identificadores y rasgos de las dos listas;
`linajes_ajustados` agrega cada identidad solo una vez, aunque tenga varias
unidades. La elección conserva un orden estable y no consume azar global.
Solo se aplica al procesar un nacimiento pendiente: repetir una evaluación
sin nacimientos no cambia la identidad ni inventa historia. Con el mismo
entorno en los mismos intervalos, pasos cortos/largos y guardar/cargar dan
el mismo estado. Un salto que omita un cambio ambiental no puede reconstruirlo.

La vista **4 Vida** añade «Linajes ajustados X/Y» al mundo observado: X es
el número de linajes vivos favorecidos por el agua y Y todos los linajes vivos.
«Sin regla» significa que no hay una preferencia definida para ese estado
del agua. El indicador se calcula con datos ya persistidos; no añade campos
al guardado ni realiza selección al dibujar. Puede cambiar al cambiar el agua
antes de que nazca otra unidad; la descendencia cambiará en el próximo
nacimiento. Para probar casos controlados, incluidos cambio de agua y carga:

```sh
.venv/bin/python -m unittest tests.test_unicellular_competition -v
```

## Parentesco e historia de los linajes

`historial_linajes_unicelulares` es un diccionario: cada identificador de
linaje apunta a otro diccionario con su `progenitor_id`, su `rasgo` y su
`origen`. Una fundadora tiene origen `fundacion` y progenitor `None`. Cuando
un nacimiento varía, se guarda un registro con origen `variacion` y el
identificador del linaje elegido para reproducirse, antes de evaluar si esa
variante continúa la línea observada. Una variante descartada por la selección
también conserva su parentesco.

Por ejemplo, si el linaje 7 deja un descendiente con variación en el nacimiento
12, se registra el linaje 12 con progenitor 7. Los nacimientos sin variación
siguen perteneciendo al linaje existente y no añaden registros. Cada variante
añade una entrada histórica; la memoria y el guardado crecen con los linajes
creados, no con todos los nacimientos. El registro incluye relaciones y rasgos,
pero todavía no fechas. La clasificación de especies se guarda por separado.

Al extinguirse unidades o toda la población, las listas de vivos cambian y el
historial permanece. Una fundadora posterior inicia otra raíz sin progenitor;
no hereda un padre extinto. Guardar y cargar conserva también los linajes
extintos. JSON escribe las claves del diccionario como texto y `Planet` las
convierte otra vez a enteros al cargar. Las copias de los registros evitan que
modificar un diccionario exportado cambie el planeta original.

Un guardado anterior sin historial registra solo los linajes vivos conocidos
con origen `desconocido` y progenitor `None`. No se reconstruyen antepasados
ni linajes extintos que ese archivo nunca guardó. `setdefault` añade estos
registros únicamente si faltan y conserva cualquier parentesco ya conocido.
Los descendientes nuevos de estos linajes sí tendrán un progenitor registrado.

La vista **4 Vida** muestra «linajes registrados», incluyendo los extintos
conocidos, y el origen del linaje observado: un número identifica su progenitor,
«fundador» indica una raíz conocida y «desconocido» indica historia ausente en
un guardado anterior. «Variaciones» sigue siendo el contador histórico.
Si la población se extingue, el origen observado pasa a «—», pero la cantidad
de registros permanece. Para comprobar parentesco, extinción y persistencia:

```sh
.venv/bin/python -m unittest tests.test_unicellular_ancestry -v
```

## Especies unicelulares simbólicas

[`ModeloEspeciesUnicelulares`](species_model.py) aplica un criterio operativo
de diseño, **no una definición científica ni una prueba de aislamiento
reproductivo**. Una especie agrupa linajes según su parentesco:

1. Una fundadora inicia una especie con su propio identificador de linaje.
2. La primera variación en una rama pertenece a la especie de su progenitor.
3. La segunda variación encadenada desde el inicio de esa especie inicia otra
   especie. La cuenta de esa nueva rama vuelve a cero.

`VARIACIONES_PARA_NUEVA_ESPECIE = 2` es un parámetro elegido para esta primera
versión. Se cuentan cambios a lo largo de cada rama, no todas las variaciones
del planeta ni los nacimientos sin variación. Si 1 origina 2 y 2 origina 3,
los linajes 1 y 2 pertenecen a la especie 1, y el 3 inicia la especie 3. Otro
hijo directo del linaje 1 seguirá en la especie 1. Aunque el linaje 3 vuelva
al rasgo de su abuelo, su especie no se fusiona con la anterior.

`clasificacion_especies_unicelulares` guarda por linaje `especie_id` y
`distancia` (variaciones desde la raíz de su especie). Las identidades son
locales de cada planeta. El modelo solo clasifica un linaje cuando falta su
registro; no renumera identidades ya guardadas. Al nacer una variante se
clasifica inmediatamente, aunque la selección no la favorezca. No cambian
el tamaño de población, los rasgos, la reproducción ni el azar global.

Los métodos de consulta usan conjuntos (`set`) para contar una especie una
sola vez aunque tenga varios linajes o unidades. Una especie está viva si al
menos una unidad pertenece a ella, aunque su linaje fundador ya haya muerto.
Las extintas son las registradas que no están vivas: la diferencia entre ambos
conjuntos. No se borra su clasificación al extinguirse. Una nueva fundadora
tras una extinción total recibe otra especie y no resucita la anterior.

El campo nuevo se guarda con el planeta. Al cargar partidas que no lo tienen,
se aplica el criterio al parentesco histórico disponible, en orden de nacimiento.
Si falta el parentesco de un linaje, se le asigna una especie provisional propia;
no se fusionan linajes desconocidos solo por compartir rasgo ni se inventan
extintos que no constan en el historial. Las clasificaciones guardadas se
conservan. Es una clasificación retrospectiva del registro disponible, no
una reconstrucción de hechos biológicos ausentes.

En **4 Vida**, «Especies vivas», «Especies extintas» y «Especies reg.» son
totales del universo (cada planeta tiene sus propias identidades). El campo
«Especie» junto a selección pertenece al linaje observado; «—» indica que no
hay uno activo. Los tres totales cumplen registradas = vivas + extintas.
Una especie inicial y ninguna extinta son resultados válidos, igual que cero
especies si nunca apareció población. Para probar clasificación y persistencia:

```sh
.venv/bin/python -m unittest tests.test_unicellular_species -v
```

## Seguimiento de diversificación

[`ModeloEspeciesUnicelulares`](species_model.py) también permite consultar la
abundancia viva por especie y la relación entre especies progenitoras e hijas.
La especie nueva toma como progenitora la especie del linaje del que nació su
fundador. Por ejemplo, si el linaje 3 inicia una especie a partir del linaje 2
de la especie 1, la especie 3 es hija directa de la 1. La relación sigue en el
historial si la especie 1 se extingue. Una especie fundadora o de origen
desconocido no tiene progenitora conocida.

La abundancia cuenta **unidades simbólicas vivas**, no linajes ni células
reales: `[2, 3, 3]` puede significar una unidad de una especie y dos de otra.
Dos o más especies con al menos una unidad cada una indican coexistencia en
ese planeta. Los identificadores son locales: `especie 3` en dos planetas no
es necesariamente la misma especie. Son consultas de los datos ya guardados;
no añaden azar ni modifican la población o la física.

La vista **5 Especies** resume vivas, extintas, registradas y mundos con
coexistencia. Para el mundo observado presenta abundancia por especie y la
rama de la especie observada. Un cero es normal si el universo aún no formó
vida o si las especies no coexistieron. No se modelan recursos o nichos.

Para comprobar casos concretos y la vista en una terminal mínima:

```sh
.venv/bin/python -m unittest tests.test_unicellular_diversification tests.test_simulation_dashboard -v
```

Para iniciar **un universo real desde el año 0** con el mismo modelo estelar
híbrido que usa `Game`, avanzar con semilla y pasos conocidos hasta
3 000 millones de años y comprobar guardado/carga y continuación:

```sh
.venv/bin/python -m tests.run_universe_from_zero
```

Otras semillas pueden no mantener vida suficiente para generar varias especies.
Las pruebas controladas cubren parentesco y coexistencia sin confundir un
planeta preparado con uno emergente.

En la revisión de cierre de Fase 2, el escenario con el **modelo estelar
híbrido del juego** y semilla `374852300` alcanzó protocélulas en el año
2 760 000 000, primera vida en 2 763 000 000 y tres especies vivas coexistiendo
en 2 769 000 000. En 2 800 000 000 ya no había población activa y las cinco
especies registradas estaban extintas; al llegar a 3 000 000 000 seguía el
historial. Guardar, cargar y continuar produjo estados iguales. La corrida
anterior que había dado cero hasta 5 400 millones de años había omitido el
modelo estelar al construir `Universe`; por eso no representaba la ruta de
«Iniciar simulación». Los años observados dependen de la resolución temporal:
un paso largo puede omitir condiciones transitorias que detectan pasos cortos.
