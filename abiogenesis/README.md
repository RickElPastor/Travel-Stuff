# Abiogénesis: hasta la primera vida

La primera etapa representa **copias químicas rudimentarias** dentro de un
sistema protocelular. Es una regla conceptual del simulador. No genera
secuencias, genes, poblaciones ni tasas biológicas de reproducción. Por sí
sola no cumple el criterio operativo de primera vida definido al final.

## Condiciones

Una ruta de copia puede estar activa cuando:

1. El planeta alcanzó protocélulas y conserva viabilidad actual.
2. Tiene registrados precursores complejos, polímeros, red química y
   compartimentalización.
3. El mecanismo histórico de polimerización corresponde al tipo de protocélula.
4. El estado actual del agua y, cuando corresponde, la geoquímica permiten
   usar esa ruta de copia.

| Protocélula | Polimerización | Ruta de copia | Entorno actual |
| --- | --- | --- | --- |
| Criogénica | Ciclos de congelación | Hielo | Hielo |
| Geoquímica | Superficies geoquímicas | Poros minerales | Agua líquida y geoquímica |
| Mixta | Frío y geoquímica | Mixta | Hielo y geoquímica |

Un confinamiento anómalo puede sostener la viabilidad, pero no sustituye el
entorno físico necesario para que se copie el polímero. La energía exótica
puede sostener la viabilidad cuando falta la fuente normal, pero la ruta de
copia todavía necesita su entorno correspondiente. La catálisis arcana no
crea una ruta de copia nueva.

## Qué significan los contadores

`Replicación: hist` cuenta planetas donde el modelo permitió una ruta de copia
al menos una vez. Ese logro no se borra. `activa` cuenta los que cumplen las
condiciones ahora; puede subir o bajar. `activa` nunca debe superar `hist`.
Al cargar un guardado antiguo, ambos empiezan en cero y se calculan al avanzar.
Los nuevos guardados conservan los tres campos: logro, actividad y mecanismo.

Esta regla se evalúa después de la viabilidad, en el mismo paso. Por eso una
protocélula viable puede empezar a copiarse en ese paso si su ruta coincide.
La actividad no espera un plazo inventado en años: la primera copia modelada
puede registrarse en el mismo paso. Después, el módulo de herencia observa
una copia por cada millón de años mientras la ruta siga activa. Ese intervalo
organiza la simulación y no representa una tasa molecular medida. Si las condiciones se pierden, `activa` vuelve
a cero; cuando regresan, significa que el entorno vuelve a permitir la ruta.
No se afirma que sobreviva una protocélula individual durante la interrupción.

## Revisión y prueba en un universo nuevo

Lee [el modelo de replicación](replication_model.py), los tres campos nuevos de
`Planet`, y el orden al final de `Universe.actualizar`. Luego ejecuta:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py
```

Inicia un universo nuevo. Observa `proto`, `Viabilidad` y `Replicación` al
avanzar. Puede haber ceros durante mucho tiempo. Cuando `proto` suba,
`Replicación hist` subirá solo si existe una ruta viable y compatible. Al perder
habitabilidad, `activa` puede volver a cero mientras `hist` conserva su valor.
Guarda con un nombre nuevo, carga y comprueba que los contadores persistan.

Como práctica, explica por qué se comprueba la viabilidad antes de la ruta de
copia y por qué el logro histórico se asigna solo la primera vez. Después
cambia temporalmente una condición en una prueba, observa el fallo y restáurala.

En una reproducción de la semilla 374852300 hasta el año 5 371 654 369,
con pasos de 20 millones de años, se observaron 12 protocélulas históricas,
12 rutas de copia históricas y cero rutas activas al final. La primera ruta
se activó cerca del año 2 760 000 000 y se desactivó cerca del 2 800 000 000.
Son resultados de esa resolución temporal; los años exactos pueden cambiar
con pasos de simulación diferentes.

## Herencia y variación

[El modelo de herencia](inheritance_variation_model.py) sigue una sola línea
simbólica de copias por planeta. `patron_copia` vale 0, 1 o 2: son etiquetas
abstractas, no genes ni moléculas reales. La primera línea empieza en 1.
Cada copia recibe el patrón de la anterior. Con una probabilidad de diseño
del 25 %, la nueva copia recibe una de las otras dos etiquetas. Ese cambio
cuenta como variación. No altera la física ni la viabilidad. El módulo de
selección decide si ese nuevo patrón continúa la línea.

La variación usa una semilla privada formada por la semilla del universo, el
sistema, el planeta y el número de copia. No consume el azar de estrellas ni
planetas. El número de copias, las variaciones, el patrón actual y el próximo
año de observación se guardan, para que cargar y continuar dé el mismo
resultado.

| Campo | Significado |
| --- | --- |
| `patron_copia` | Patrón de la línea actual; `None` si está inactiva |
| `copias_heredables` | Total histórico de copias observadas |
| `variaciones_prebioticas` | Total histórico de copias con patrón diferente |
| `proxima_copia_anio` | Próxima observación programada |

Cuando deja de haber replicación activa, la línea actual termina y su patrón
se limpia. Los totales históricos se conservan. Si la replicación se reactiva,
empieza otra línea en el patrón inicial; no suponemos que sobrevivió una
protocélula durante la interrupción. El contador `herencia` de la interfaz
muestra mundos con al menos una copia; `variación` muestra mundos con al menos
un cambio. Ambos contadores son históricos.

Para entender el método `evaluar`, sigue este orden: comprueba actividad,
inicia una línea cuando falta, procesa las observaciones pendientes y deja
programada la siguiente. En `_copiar`, identifica dónde se copia el patrón
y dónde puede cambiar. Como práctica, explica por qué repetir la evaluación
en el mismo año no añade otra copia.

## Selección

[El modelo de selección](selection_model.py) asigna un patrón favorecido a cada
ruta: 0 para hielo, 1 para la ruta mixta y 2 para poros minerales. Es una
regla de diseño para practicar lógica evolutiva, no una medida química.
Cuando aparece una variante, el modelo compara el patrón anterior y el nuevo.
Si el nuevo es el favorecido y el anterior no lo era, continúa la variante.
En cualquier otro caso continúa el anterior. Los empates conservan el anterior.

`variantes_favorecidas` y `variantes_descartadas` son contadores históricos:
cuentan decisiones, no seres vivos. Su suma coincide con las variaciones
observadas en los universos nuevos. La interfaz muestra `Mundos con selección`
y esos dos totales. Una variante descartada sigue contando como variación,
porque el cambio sí ocurrió, aunque no continuó la línea.

La interfaz ahora tiene tres vistas accesibles con 1, 2 y 3. La primera pone
Abiogénesis en primer plano; Universo resume formación y reglas fantásticas;
Condiciones muestra habitabilidad y química actual. Los eventos y controles
permanecen visibles. En una terminal de 72 × 24 caben los indicadores actuales;
en una más alta hay más espacio para eventos.

Para probar con un universo nuevo, observa que primero suben protocélulas,
viabilidad y replicación. Herencia cuenta mundos con copias, variación mundos
con cambios y selección mundos donde el modelo ya comparó una variante.
Al perder actividad, los totales históricos permanecen. Puedes guardar y
cargar con un nombre nuevo para comprobar la continuidad. Ejecuta también:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

## Primera vida

[El criterio de primera vida](first_life_model.py) se aplica a una línea
**actualmente activa**. Exige una protocélula viable, replicación activa, un
patrón copiable, al menos tres copias de esa misma línea, una variación y una
comparación por selección. Una variante descartada también demuestra que el
modelo comparó dos patrones y conservó el anterior.

La línea tiene tres contadores propios: `copias_linea`, `variaciones_linea` y
`comparaciones_linea`. Se ponen en cero al interrumpirse la replicación, así
que los totales históricos de épocas distintas no pueden producir vida nueva
por accidente. `vida_activa` puede volver a falso cuando cambian las
condiciones. `alcanzo_primera_vida` y `anio_primera_vida` conservan cuándo
se alcanzó el criterio por primera vez. Es una definición **operativa del
simulador**, no una prueba científica de vida extraterrestre.

En la pantalla, `PRIMERA VIDA` muestra activa e histórica. Debajo, `Línea
inactiva` significa que el mundo observado conserva copias históricas pero
no tiene patrón actual; por eso antes aparecía un guion. `Mundos con selección`
cuenta dónde hubo al menos una comparación. `favorecidas 0 · descartadas 33`
indica que, en esas 33 comparaciones, el patrón anterior siguió siendo el
preferido por la regla actual.

Para comprobarlo en un universo nuevo, observa la cadena de indicadores en
la vista 1. Puede pasar de `vida activa 1` a `vida activa 0` sin perder
`vida histórica 1`. Guarda con un nombre nuevo, carga y continúa para revisar
el mismo estado. El próximo trabajo, después de esta entrega, será modelar
poblaciones y evolución biológica. No se incluye aquí.
