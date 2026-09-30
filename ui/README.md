# Explorador del universo

La simulación abre en **Universo**. `Enter` muestra el catálogo de todos los
sistemas estelares registrados; `E` muestra las estrellas activas y remanentes.
El proyecto todavía no modela galaxias, así que no se presenta una lista
inventada de ellas.

En un catálogo, `↑/↓` mueve la selección, `PgUp/PgDn` recorre páginas y `/`
filtra por parte del nombre. La lista indica cuántos resultados hay, la
posición seleccionada y los datos necesarios para decidir qué abrir. `Enter`
abre la ficha seleccionada y `Esc` vuelve. Desde una estrella se puede abrir
su sistema si la relación sigue registrada. Desde un sistema, `Enter` o `P`
abren **sus** planetas y `E` abre **sus** estrellas. Cada ficha planetaria
resume masa, órbita, habitabilidad, agua, química y vida.

Desde un planeta, `M` abre **Biosfera**. Muestra fuentes ambientales
potenciales, la primera ruta metabólica simbólica si existe y el estado
ecológico microbiano. La luz y la geoquímica no crean rutas biológicas por sí
solas. Una variante capaz puede abrir la ruta fotosintética cuando también hay
agua líquida y CO₂; se muestran sus unidades productoras activas y el hito
histórico. Debajo aparece una proyección del CO₂ con vida y del aporte de O₂
actual, separados del CO₂ físico. No modifica todavía el clima ni la
habitabilidad. Si un linaje descomponedor vivo coincide con muertes del paso,
la vista enseña el enlace de restos a descomponedores. La línea **Ciclo**
muestra unidades simbólicas
de restos y nutrientes pendientes, más el total histórico aprovechado por
microbios consumidores. `Esc`
vuelve al planeta sin cambiar la velocidad ni el reloj compartido.

`V` abre el historial de eventos desde Universo, una estrella, un sistema o
un planeta. El resumen universal muestra los últimos eventos; las fichas de
estrella y sistema muestran sus eventos recientes. El historial universal
incluye todos los ámbitos, mientras que una ficha filtra su propio objeto.
Los eventos nuevos registran formación de sistemas, estrellas y planetas,
evolución estelar, los pasos de química prebiótica, protocélulas, primera vida
y extinción local. Un nacimiento estelar fuera del modelo también conserva su
evento. El año de un hito planetario corresponde al final del paso en que se
observó; no indica un instante más preciso. Los guardados antiguos conservan
sus eventos globales sin
inventar ámbitos que no tenían.

`S` guarda desde cualquier pantalla. `+/-` cambia la velocidad. Al entrar en
un planeta, empieza en **x1 = un año universal por segundo**, exactamente
igual que el x1 de Universo. La escala planetaria ofrece de 0 a 10 000 años
universales por segundo;
al salir recupera la velocidad y escala anteriores. El tiempo sigue siendo
el del universo completo: observar un planeta no congela los demás mundos.
La ficha conserva el año universal en el encabezado y debajo muestra una
fecha local derivada de ese mismo reloj. El año local usa una aproximación
kepleriana del periodo orbital al formarse el planeta; cada día mostrado es
una unidad estándar de 24 horas, porque todavía no hay rotación modelada.
Los doce meses son divisiones numéricas iguales del año orbital, no meses
astronómicos ni un calendario creado por una civilización. Un año orbital de
1000 días estándar tarda esos 1000 días en incrementar el año local. Los
guardados anteriores reconstruyen una fecha aproximada solo para la pantalla
cuando disponen de masa estelar y año de formación del sistema.
La ubicación del explorador no se guarda; un universo cargado vuelve a abrir
en el resumen del universo y recupera la escala universal. El archivo de
guardado conserva los datos, el año y la escala que tenía al guardarse; abrir
la interfaz cambia la escala si el guardado se hizo dentro de un planeta.

La pantalla necesita al menos 72 columnas y 24 filas. Los catálogos muestran
una página a la vez para mantener legibles miles de sistemas o planetas.
