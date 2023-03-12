

¿Jenga?

A Marcos le compraron un Jenga por navidad. Jenga es un juego que
consiste en armar una torre con palitos, para luego ir retirándolos uno
a uno hasta que la torre se desmorone. Marcos no sabe esto. De hecho
Marcos no tiene ni idea de qué hacer con el reguero de palitos que tiene
sobre la mesa. Como todo un programador, decide utilizar los palitos
para un juego que, según él, es más divertido que Jenga, fueran cuales
fueran sus reglas.

Primero coloca algunos palitos de manera que se formen $n$ columnas.
Cada columna $i$ tiene inicialmente tamaño $h_i$. Entonces se pueden
realizar tres acciones distintas, con distintos costos que se definen al
inicio del juego:

-   Coloca un palito sobre una columna aumentando en 1 su tamaño (costo
    $C$)

-   Eliminar el palito más arriba de una columna disminuyendo en 1 su
    tamaño (costo $E$)

-   Mover el palito más arriba de una columna a la posición más arriba
    de otra columna ($M$)

El objetivo del juego es lograr que todas las columnas tengan la misma
altura, utilizando acciones que sumen el menor costo posible. Encuentre
un algoritmo que reciba una lista de tamaño $n$ con las $h_i$ alturas
iniciales junto con los enteros $C$, $E$ y $M$ de los distintos costos y
calcule el costo de la secuecncia de acciones más eficiente.