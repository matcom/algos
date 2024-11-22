# DP

## Minecraft

En el juego de MineCraft una de las principales distracciones es la construccion, los mejores jugadores logran hacer monumentos imponentes que sorprenden a todos. Actualmente se esta llevando a cabo un torneo de construcción en el juego, donde la tarea es hacer un muro. Un muro es, como sabemos, una ilera de columnas de bloques de piedra, todos de la misma altura. En MineCraft, para llevar a cabo esta tarea hay 3 movimientos válidos:

- sacar un bloque de piedra del inventario y aumentar la altura de la columna en cuestion en 1 de altura
- destruir un bloque de piedra de una columna y disminuir la altura de la columna en cuestion en 1 de altura
- mover un bloque de piedra de una columna a otra, aumentando la altura de la 2da columna y disminuyendo la de la 1ra en 1 de altura cada una.

Se sabe que hacer cada movimiento consume c, d y m de energia respectivamente, y que en los inventarios de los jugadores hay suficienues bloques de piedra siempre. Los jugadores comienzan a jugar con un muro a medio hacer aleatorio, osea, se les da una cantidad n de columnas de bloques de piedra en ilera, de disímiles tamaños y el ganador del torneo será el que construya un muro de largo n utilizando la menor cantidad de energia, no se permite crear columnas nuevas ni dejar huecos de antiguas columnas en el muro porsupuesto.

Elabore una estrategia que asegure que para cualquier muro inicial a medio hacer con que comience, usted logrará hacer el muro pedido utilizando la menor cantidad de energia posible.

### Statement

Dado que la pared consiste en $N$ pilares de ladrillos, donde la altura del $i$-ésimo pilar es inicialmente igual a $h_i$, y todas las alturas de los $N$ pilares deben ser iguales después de la restauración:

Se permiten las siguientes operaciones:

- Colocar un ladrillo en la parte superior de un pilar, con un costo de $A$.
- Quitar un ladrillo de la parte superior de un pilar no vacío, con un costo de $R$.
- Mover un ladrillo de la parte superior de un pilar no vacío a la parte superior de otro pilar, con un costo de $M$.

No puedes crear pilares adicionales ni ignorar algunos de los pilares preexistentes, incluso si su altura se reduce a 0.

Determina el costo total mínimo para hacer que todos los pilares tengan la misma altura.

### Solution

Primero, hagamos $M = \min(M, A + R)$ — esto es cierto ya que podemos emular el movimiento agregando y removiendo. Después de eso, nunca será rentable agregar y remover en una misma solución, ya que siempre podemos mover en su lugar.

Supongamos que hemos fijado $H$ — la altura resultante para todos los pilares. ¿Cómo podemos calcular el costo mínimo para un valor dado de $H$? Algunos pilares tienen como máximo $H$ ladrillos, denotemos el número total de ladrillos faltantes en estos pilares como $P$. Otros pilares tienen como mínimo $H$ ladrillos, denotemos el número total de ladrillos extra en estos pilares como $Q$. Si $P \geq Q$, entonces nos faltan $(P - Q)$ ladrillos en total, por lo que debemos realizar $(P - Q)$ adiciones. No habrá más adiciones o remociones, y tenemos que hacer al menos $Q$ movimientos ya que de alguna manera debemos deshacernos de los ladrillos extra de aquellos pilares que inicialmente tienen más de $H$ ladrillos. Está claro que $Q$ movimientos son suficientes. Por lo tanto, el costo total será $C = A(P - Q) + MQ$. De manera similar, si $Q \geq P$, entonces el costo total será $C = R(Q - P) + MP$.

Supongamos ahora que $P \geq Q$. Tenemos exactamente $X$ pilares con como máximo $H$ ladrillos y exactamente $N - X$ pilares con estrictamente más de $H$ ladrillos. Intentemos incrementar $H$ en 1 y ver cómo cambiará el costo total. $P' = P + X$, $Q' = Q - (N - X) = Q - N + X$. $C' = A(P' - Q') + MQ' = A(P + X - Q + N - X) + M(Q - N + X) = A(P - Q) + MQ + AN - M(N - X)$. Podemos ver que el costo total ha cambiado en $AN - M(N - X)$. Mientras $X$ sea constante, el cambio de costo será constante. ¿Cuáles son los momentos en los que $X$ cambia? Cuando $H$ es igual a la altura inicial de algún pilar. Por lo tanto, el costo como función de $H$ es lineal por tramos con puntos de ruptura correspondientes a las alturas iniciales.

Hay un matiz — hemos asumido $P \geq Q$. Lo mismo será cierto para $P \leq Q$, pero puede haber puntos de ruptura adicionales cuando cambiamos entre estos dos estados. Este cambio ocurrirá solo una vez para $H ≈ \sum h_i / N$ (la igualdad aproximada aquí significa que este punto puede no ser entero, por lo que deberíamos agregar tanto $\lfloor \sum h_i / N \rfloor$ como $\lceil \sum h_i / N \rceil$ como puntos de ruptura).

Los mínimos de la función lineal por tramos están en los puntos de ruptura, por lo que basta con calcular el costo en los puntos de ruptura (las alturas iniciales y $H ≈ \sum h_i / N$) y elegir el mínimo de ellos.

Para calcular el costo para un valor dado de $H$ rápidamente, podemos ordenar las alturas iniciales y calcular las sumas prefixadas de las alturas. Luego, utilizando búsqueda binaria, podemos determinar qué pilares tienen altura menor que $H$ y mayor que $H$, y luego calcular $P$ y $Q$ usando las sumas prefixadas. Podemos usar dos punteros en lugar de búsquedas binarias, pero esto no mejorará la complejidad total, que es $O(N \log N)$ debido a la ordenación (y búsquedas binarias si las estamos usando).

COMPLEJIDAD TEMPORAL:
$O(N \log N)$
