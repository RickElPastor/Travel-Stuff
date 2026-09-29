# Viabilidad protocelular: primer paso hacia abiogénesis

`alcanzo_protocelula` registra un logro histórico que no se borra.
`protocelula_viable` indica si las condiciones actuales permiten mantener
sistemas de ese tipo. No representa una población ni la supervivencia de una
protocélula individual. Tampoco declara vida.

Es una regla conceptual de diseño, sin probabilidades ni umbrales científicos
nuevos. Exige un tipo conocido, habitabilidad actual de Fase 1, ingredientes,
agua condensada, energía y confinamiento compatible.

| Tipo histórico | Confinamiento normal requerido ahora |
| --- | --- |
| criogénica | Agua en estado de hielo |
| geoquímica | Agua líquida y ruta geoquímica activa |
| mixta | Hielo y ruta geoquímica activa |

Estas condiciones conservan los entornos usados por los modelos anteriores.
La energía normal se toma de `candidato_quimica_prebiotica`.

## Qué pueden hacer los apoyos

- Energía exótica: suplir energía normal, pero no ingredientes ni confinamiento.
- Confinamiento anómalo: suplir confinamiento normal, pero no agua ni energía.
- Catálisis arcana: sigue registrada como apoyo; por sí sola no elimina ningún
  requisito de viabilidad. No modelamos aún velocidades de reacción.

Los apoyos se recalculan antes de evaluar viabilidad. Sus condiciones originales
siguen aplicándose. Ninguno evita la exigencia de habitabilidad normal actual.
`protocelula_viable_normal` conserva el resultado sin apoyos y
`protocelula_viable` contiene el resultado final. Ambos pueden ser verdaderos:
la fila de interfaz cuenta como `extra` solo los casos que necesitan apoyos.

`estado_viabilidad_protocelular` explica el primer requisito incumplido, según
el orden del modelo, o indica `viable_normal` / `viable_extraordinaria`.
La ausencia de habitabilidad se informa antes que los ingredientes porque el
modelo prebiótico deja esos indicadores en falso cuando un mundo no es habitable.

## Tiempo y guardado

En cada paso se ejecutan química normal, apoyos y viabilidad, en ese orden.
Perder condiciones desactiva la viabilidad; recuperarlas puede reactivarla.
Esto significa que el entorno vuelve a permitir sistemas protocelulares, no
que una protocélula destruida haya resucitado. No hay memoria de poblaciones.

Los tres campos se guardan y cargan. Un guardado antiguo usa `False`, `False`
y `no_evaluado`; se actualizan al avanzar. La interfaz muestra `pendiente`
para los mundos con protocélulas históricas aún sin evaluar.
`es_candidato_abiogenesis()` consulta el resultado de viabilidad; por eso debe
usarse después de esa evaluación o al cargar un guardado ya evaluado.

## Cómo revisar y probar

1. Lee `ModeloViabilidadProtocelular.evaluar`: cada retorno explica un requisito.
2. Revisa `_tiene_confinamiento_normal` y las alternativas con `or`.
3. Revisa los tres campos en Planet: constructor, `a_dict` y `desde_dict`.
4. En Universe, comprueba el orden al final de `actualizar`.

Desde la carpeta del repositorio:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python main.py
```

Inicia un universo nuevo y observa `proto` y `Viabilidad` mientras avanza.
`proto=0` implica viabilidad cero. Si `normal` sube y luego baja, el mundo
conserva `proto` pero dejó de cumplir alguna condición actual. Guarda con un
nombre nuevo y vuelve a cargar para comprobar que ambos estados persisten.

La semilla 374852300 se reprodujo hasta el año 5 371 654 369 con pasos de
20 millones de años: 12 mundos alcanzaron protocélulas y la viabilidad normal
terminó en cero. Antes de esa fecha hubo varios periodos con mundos viables.
Los momentos exactos pueden variar si la simulación usa pasos distintos.

Las pruebas cubren rutas normales, apoyos, pérdida y recuperación, conservación
del historial, ausencia de consumo aleatorio, persistencia y guardados antiguos.
Como ejercicio, explica por qué `proto=16` puede coexistir con cero viables.

La etapa siguiente, replicación prebiótica, se implementa en
`abiogenesis/replication_model.py`. Aún faltan herencia, variación y selección
para establecer el criterio de primera vida.
