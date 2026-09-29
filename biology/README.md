# Vida unicelular: primer paso de Fase 2

[`ModeloPoblacionUnicelular`](unicellular_population_model.py) observa el
indicador `vida_activa` calculado al final de la abiogénesis. Cuando aparece,
funda una población de **una unidad simbólica**. Mientras siga activa, añade
una unidad por cada millón de años transcurridos, hasta un máximo inicial de
ocho. Estos números organizan el juego: no cuentan células ni representan una
tasa biológica medida. Tampoco modelamos todavía especies, recursos o
competencia.

Si `vida_activa` se pierde, la población actual llega a cero y el crecimiento
programado se limpia. Si aparece de nuevo, comienza una población nueva. El
registro histórico `alcanzo_primera_vida` permanece. La evaluación se ejecuta
después de la primera vida y no altera habitabilidad, química ni la línea de
copias de Fase 1.

El tamaño y el próximo año de crecimiento se guardan con el planeta. Un
guardado anterior carece de esos campos y carga tamaño cero; al avanzar, puede
fundar una población si todavía hay vida activa. Repetir la evaluación en el
mismo año no duplica el crecimiento. En la vista **4 Vida** se observan mundos
con población activa, suma de unidades y un mundo destacado.

Para revisar el cambio, mira primero el `if not planeta.vida_activa` y luego
la fundación y el cálculo de `intervalos`. Prueba con un universo nuevo y,
cuando aparezca primera vida, cambia a la vista 4. Guarda y carga mientras
haya una población para comprobar que conserva su tamaño. Los ceros anteriores
a la primera vida son esperados. La prueba automática específica es:

```sh
.venv/bin/python -m unittest tests.test_unicellular_population -v
```
