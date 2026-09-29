# Apoyo extraordinario a la química

Esta ampliación define apoyos actuales de ficción y prepara la entrada a
abiogénesis. Los índices van de 0 a 1 y usan la intensidad ya asignada al planeta.
No son tasas científicas ni multiplicadores de velocidad. Por ahora no aceleran
las etapas químicas ni crean nuevas protocélulas.

| Regla | Apoyo | Condiciones adicionales |
| --- | --- | --- |
| arcano | catalisis_arcana | Entorno químico normal activo |
| anomalia_fisica | confinamiento_anomalo | Entorno químico activo y red química histórica |
| energia_exotica | energia_quimica_exotica | Puede aportar energía sin UV ni geoquímica |

Todos requieren mundo extraordinario, intensidad mayor que cero y no superior
a uno, ingredientes prebióticos y agua condensada. Los ingredientes se evalúan
previamente mediante el modelo normal, que exige habitabilidad de Fase 1.
La capa extraordinaria no sustituye ese requisito.

## Orden y persistencia

1. Universe calcula física, habitabilidad y química habituales.
2. ModeloApoyoQuimicoExtraordinario.evaluar recalcula los tres apoyos.
3. Planet guarda y carga esos tres valores junto con el resto de sus datos.

No hay nuevas llamadas aleatorias. Cada evaluación borra únicamente los apoyos
actuales antes de recalcularlos. Si desaparece el agua o los ingredientes, el
apoyo desaparece; los logros históricos se conservan.

Los guardados antiguos cargan los apoyos en cero. Se calculan al siguiente paso
de simulación. Los nuevos conservan los valores incluso antes de reanudar.
No se necesita cambiar la versión del guardado.

## Preparación de abiogénesis

Planet.es_candidato_abiogenesis consulta ahora la viabilidad actual, evaluada
por ModeloViabilidadProtocelular después de los apoyos extraordinarios.
Consulta [las reglas de viabilidad](../chemistry/VIABILIDAD.md).
Ser candidato todavía no significa estar vivo: faltan replicación, herencia,
variación y selección.

Planet.obtener_apoyo_protocelular_extraordinario devuelve el apoyo disponible
cuando existe un logro protocelular. Tampoco representa supervivencia medida.
La interfaz muestra apoyo_proto en Mundos y cand_abio en Viabilidad.

## Revisión y práctica

Desde la carpeta Travel Stuff:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py
```

Carga prebio_dieseis, comprueba que proto sigue en 16 y avanza la simulación.
Guarda con un nombre nuevo y vuelve a cargar: los datos deben conservarse.
No esperes apoyos positivos en todos los mundos extraordinarios: tienen requisitos.

Para entender el código, revisa evaluar y explica sus retornos tempranos.
Después revisa ModeloViabilidadProtocelular y explica por qué usa `and` para
combinar requisitos y `or` para aceptar fuentes de energía alternativas. Como ejercicio,
cambia temporalmente una expectativa de las pruebas, observa el fallo y restáurala.

Validación realizada: seis pruebas automatizadas y carga del guardado real
prebio_dieseis (4096 planetas, 16 protocélulas). Se guardó una copia temporal,
se volvió a cargar y se comparó un paso con/sin la capa extraordinaria: todos
los campos anteriores y el estado aleatorio coincidieron. En esa comprobación
hubo cero apoyos protocelulares y cero candidatos actuales a abiogénesis.
