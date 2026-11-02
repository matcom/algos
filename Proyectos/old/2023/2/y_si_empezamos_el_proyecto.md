
¿Y si empezamos el proyecto?

Daimís y Abraham se juntaron una tarde para hacer su proyecto de DAA.
Tenían que hacerlo, tenían que empezar a trabajar, ellos lo sabían, pero
la verdad es que no tenían ganas. Luego de 45 minutos de decir en bucle:
\"en 5 min arrancamos\", Abraham tuvo una epifanía (lastimosamente no
relacionada con DAA). Inventó un juego que el denominó como
espectacular.

El juego consistía en lo siguiente: Recortó $2n$ cuadraditos de papel y
los separó en dos grupos $a$ y $b$ de tamaño $n$. Luego tomó cada grupo
y en cada papel escribió un número distinto entre 1 y $n$. Luego los
desordenó y los colocó aleatoria mente en dos filas sin mezclar los
papeles de cada grupo. De esta forma, consiguió dos permutaciones con
los números entre 1 y $n$. Sobre estos dos grupos se puede realizar la
siguiente operación tantas veces como sea necesario:

-   Escoger un entero $i$ entre 1 y $n$

-   sea x el entero tal que $a_i = x$, intercambia $a_i$ con $a_x$.

-   sea y el entero tal que $b_i = y$, intercambia $b_i$ con $b_x$.

El objetivo del juego es ordenar las dos filas de papeles de forma
ascendente, con la menor cantidad de operaciones posible.

Luego de entender las reglas, a Daimís le pareció un juego
extremadamente aburrido, pero por consideración a Abraham, le dijo lo
siguiente: \"Mira, buscamos un algoritmo para el juego y luego empezamos
con DAA\".
