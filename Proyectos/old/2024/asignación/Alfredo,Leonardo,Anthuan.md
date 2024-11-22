# Problemas

## MEX Subsecuencia

Alfredo tiene un array
$a_1, a_2, \dots, a_N$. Necesita encontrar el número de formas de dividir el array en subarrays contiguos tal que:

- Cada elemento de la secuencia $a$ pertenezca exactamente a uno de los subarrays.
- Existe un número entero $m$ tal que el MEX de cada subarray sea igual a $m$. El MEX de una secuencia es el menor número entero no negativo que no aparece en dicha secuencia.

Ayuda a Alfredo con esta tarea.

## Magia

Rodrigo es el maestro de una academia de magia y debe organizar y clasificar sus ingredientes mágicos. Son tan mágicos que, consumidos de la forma adecuada, te permiten ver criaturas fantásticas y luces de colores, dejando poca resaca (Rodrigo no los consume pues es un maestro sano). Tiene dos estantes mágicos, uno llamado "a" y otro llamado "b", ambos con $n$ frascos de pociones, cada uno etiquetado con un número del 1 al $n$. Cada frasco está en un lugar aleatorio en los estantes, pero el número en cada frasco es único en cada estante.

Tu tarea es ayudar a Rodrigo a organizar ambos estantes en el orden correcto, de modo que los números en los frascos estén en orden ascendente de izquierda a derecha en ambos estantes. Sin embargo, estos estantes mágicos sólo se pueden mover siguiendo unas reglas:

1. Puedes elegir cualquier número $i$ entre 1 y $n$;
2. Encuentra el frasco en el estante "a" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$;
3. Luego, encuentra el frasco en el estante "b" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$.

Tu objetivo es organizar ambos estantes con el menor número de movimientos posible, asegurándote de que todos los frascos en ambos estantes estén en el orden correcto al finalizar la tarea.

## Tesoro pirata

En una isla desierta, un grupo de piratas ha trazado un mapa lleno de senderos secretos. Cada sendero tiene un tesoro escondido en alguna parte de su trayecto. Los piratas de la tripulación del infame capitán Jack Amarow quieren esconderse en las intersecciones de los senderos para vigilar sus tesoros. En una intersección se pueden cruzar dos senderos o más. Todas las intersecciones tienen unas palmeras a las que los piratas se pueden encaramar. Mientras más alta la palmera, más difícil es subirse y por tanto más costo tiene.

Tu misión es ayudar a los piratas a encontrar el conjunto mínimo de intersecciones donde deben esconderse para poder vigilar todos los senderos que llevan a sus tesoros y que el costo de subirse en las palmas sea mínimo.
