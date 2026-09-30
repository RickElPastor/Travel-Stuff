# Instrucciones de Travel Stuff

Antes de modificar este repositorio, lee `FASES.md` y `MEMORY.md`, inspecciona
el estado de Git y revisa los módulos relacionados con la tarea. `FASES.md`
contiene la secuencia de diez pasos proporcionada por el usuario; `MEMORY.md`
registra los cambios y decisiones recientes. Consulta ambos en cada bloque.
Al terminar, añade a `MEMORY.md` los archivos cambiados, el motivo, las
pruebas y el siguiente paso; actualiza `FASES.md` si cambia el progreso.

Trabaja con cambios pequeños, claros, deterministas y persistentes. No rehagas
sistemas terminados ni confundas reglas de diseño con datos científicos.

## Inicio y cierre de cada fase

Al comenzar una fase, explica al usuario su objetivo, los bloques previstos y
qué queda fuera de su alcance según `FASES.md`. Crea y cambia a una rama
`fase-N` desde el cierre confirmado de la fase anterior antes de escribir
código de la nueva fase; súbela a `origin` para que exista en GitHub. No crees
un proyecto nuevo.

Al terminar una fase, realiza primero la revisión integral y resuelve los
fallos encontrados. Actualiza `FASES.md` y `MEMORY.md`, ejecuta las pruebas
apropiadas y solo cuando el cierre sea real haz commit y push de la rama de
esa fase. Esta petición del usuario autoriza commit y push al cierre de cada
fase, sin tener que pedir permiso otra vez. No hagas commits intermedios ni
subas una fase incompleta salvo instrucción posterior del usuario. Comunica
el commit, la rama y el resultado del push.

## Validación obligatoria de cada bloque

Además de las pruebas específicas y de la suite apropiada, crea un universo
nuevo en el año 0 y avánzalo mediante `Universe.actualizar` hasta un horizonte
que permita observar los sistemas modificados. Usa una semilla y pasos de
tiempo explícitos y reproducibles. No sustituyas esta corrida por un planeta
preparado artificialmente ni por pruebas que comienzan en un año avanzado.
Documenta semilla, años inicial/final, tamaño de paso, hitos observados,
resultado final y cualquier límite (por ejemplo, que esa semilla no produjo
vida suficiente para ejercitar una regla). Si el universo natural no ejercita
un caso, complétalo con pruebas controladas sin presentarlas como la corrida
desde cero. Si la corrida falla, informa el error y corrígelo antes de cerrar
el bloque; no llames exitosa a una corrida parcial. Prefiere el escenario
reproducible de `tests/run_universe_from_zero.py` cuando esté disponible.

## Cómo explicar cada entrega al usuario

Si el usuario hace una pregunta, empieza la respuesta final con **Respuesta**
y contéstala directamente antes de hablar de cambios. Después presenta,
siempre en este orden y con palabras claras:

1. **Cambios realizados:** archivos, clase o método, qué se cambió y por qué.
2. **Errores:** qué falló durante el trabajo, cómo se corrigió y qué sigue
   pendiente. Si no hubo errores, dilo sin inventar problemas.
3. **Qué debo entender:** explica la lógica importante y las construcciones
   nuevas de Python con un ejemplo breve cuando ayude.
4. **Pruebas realizadas y qué debo probar:** resultados de pruebas automáticas
   y de la corrida real desde año 0, con semilla, pasos, hitos y resultado.
   Di explícitamente si hace falta una prueba manual del usuario o si ya quedó
   suficientemente validado por ti. Cuando sí haga falta, da pasos concretos
   para revisar un universo nuevo y guardar/cargar; explica resultados válidos.
5. **Qué falta para terminar la fase:** enumera el trabajo pendiente según
   `FASES.md`, incluso cuando la fase ya esté lista para cierre.
6. **Qué sigue:** siguiente bloque pequeño y su relación con lo pendiente.

No llames «probado» a algo que solo se revisó visualmente o al leer código.
Distingue pruebas automáticas, corrida desde cero y revisión manual pendiente.
Explica qué ocurrió en la corrida real, no solo que terminó sin errores.
