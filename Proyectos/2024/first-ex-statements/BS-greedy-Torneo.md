# DP

## Torneo

Tan pronto como comienza el toreno de programación competitiva, tu experimentado equipo de $3$ personas se da cuenta inmediatamente de que este presenta $a$ problemas fáciles, $b$ problemas medianos, y $c$ problemas difíciles. Resolver un problema les tomará a cualquiera de ustedes $2$, $3$ o $4$ unidades de tiempo, dependiendo de si el problema es fácil, mediano o difícil. Independientemente de la dificultad del problema, la última unidad de tiempo gastada en resolverlo debe gastarse utilizando la computadora compartida.

Tu equipo organiza sus esfuerzos de manera que cada uno de ustedes comienza (y termina) resolviendo problemas en unidades de tiempo enteras. Cualquier problema dado solo puede ser resuelto por un concursante; requiere una cantidad continua de tiempo (que depende de la dificultad del problema). Ninguno de los $3$ puede resolver más de un problema a la vez, pero pueden comenzar a resolver un nuevo problema inmediatamente después de terminar uno. De manera similar, la computadora compartida no puede ser utilizada por más de uno de ustedes al mismo tiempo, pero cualquiera de ustedes puede comenzar a usar la computadora (para completar el problema que se está resolviendo actualmente) inmediatamente después de que alguien más deje de usarla.

Dado que el concurso dura $l$ unidades de tiempo, encuentra el número máximo de problemas que tu equipo puede resolver. Además, encuentra una forma de resolver el número máximo de problemas.

### Statement

Dado un concurso que dura $l$ unidades de tiempo, un equipo de $3$ personas debe resolver $a$ problemas fáciles, $b$ problemas medianos, y $c$ problemas difíciles. Resolver un problema fácil toma $2$ unidades de tiempo, uno mediano toma $3$ unidades de tiempo, y uno difícil toma $4$ unidades de tiempo. Todos los problemas deben ser finalizados utilizando una computadora compartida en la última unidad de tiempo dedicada a ese problema.

Cada miembro del equipo puede resolver problemas en unidades de tiempo enteras, y ningún miembro puede resolver más de un problema a la vez. La computadora compartida solo puede ser utilizada por un miembro del equipo a la vez, pero cualquier miembro puede comenzar a usarla inmediatamente después de que otro miembro la deje de usar.

El objetivo es encontrar el número máximo de problemas que el equipo puede resolver en $l$ unidades de tiempo, y una manera de resolver dicho número máximo de problemas.

### Solution

Para comenzar, determinamos si es posible resolver $a$ problemas fáciles, $b$ problemas medianos y $c$ problemas difíciles en un concurso que dura $l$ unidades de tiempo. Una vez que somos capaces de hacer esto, es fácil encontrar el número óptimo de problemas que se pueden resolver; lo haremos en la sección "Solución completa" más abajo.

Vamos a (no, que lo hagan ellos) demostrar que es posible resolver $a$ problemas fáciles, $b$ problemas medianos y $c$ problemas difíciles si y solo si se cumplen las siguientes dos restricciones:

1. $l \geq a + b + c +$
   $$
   \begin{cases}
   0 & \text{si } a = b = c = 0 \\
   1 & \text{si } a \geq 1 \\
   2 & \text{si } a = 0 \text{ y al menos uno de } b \text{ y } c \geq 1 \\
   \end{cases}
   $$

2. $3l \geq 2a + 3b + 4c +$
   $$
   \begin{cases}
   0 & \text{si } a = b = c = 0 \\
   3 & \text{si } a, b, c \geq 1 \\
   4 & \text{si al menos uno de } a, b, c \text{ es } 0 \text{ pero al menos uno de } a \text{ o } b \geq 1 \\
   6 & \text{si } a = b = 0 \text{ y } c \geq 1 \\
   \end{cases}
   $$

Regresemos ahora a la tarea original, que nos requiere determinar el número máximo de problemas $n$ que se pueden resolver en el tiempo $l$. Para hacerlo, realizamos una búsqueda binaria sobre $n$ en el intervalo $[0, a + b + c]$. Para un valor candidato dado de $n$, decidimos de manera greedy los tipos de problemas a resolver: primero hasta $a$ problemas fáciles, luego hasta $b$ problemas medianos, y finalmente hasta $c$ problemas difíciles, hasta que alcancemos el número total deseado de problemas $n$ (obviamente, no hay ventaja en planear resolver un problema mientras se omite uno estrictamente más fácil). Gracias a las secciones anteriores, Somos capaces de determinar en $O(1)$ tiempo si es posible resolver los $n$ problemas elegidos. Una vez que se encuentra el valor óptimo de $n$, podemos imprimir una estrategia explícita en $O(n)$ tiempo. En general, la complejidad de esta solución es $O(\log(a + b + c) + n)$.

Para determinar si es posible resolver los $n$ problemas elegidos, también podemos construir de manera greedy una estrategia óptima y verificar si toma como máximo $l$ unidades de tiempo. Dicha solución no se basa explícitamente en verificar las restricciones (1) y (2).
