# Grafos

## Gato y Ratón

Un juego en un grafo no dirigido es jugado por dos jugadores, Ratón y Gato, que alternan turnos.

El grafo se da de la siguiente manera: `graph[a]` es una lista de todos los nodos `b` tales que `ab` es una arista del grafo.

El ratón comienza en el nodo 1 y juega primero, el gato comienza en el nodo 2 y juega segundo, y hay un agujero en el nodo 0.

Durante el turno de cada jugador, deben viajar a lo largo de una arista del grafo que conecta con el nodo en el que se encuentran. Por ejemplo, si el ratón está en el nodo 1, debe viajar a cualquier nodo en `graph[1]`.

Además, no se permite que el gato viaje al agujero (nodo 0).

El juego puede terminar de tres maneras:

1. Si alguna vez el gato ocupa el mismo nodo que el ratón, el gato gana.
2. Si alguna vez el ratón llega al agujero, el ratón gana.
3. Si alguna vez se repite una posición (es decir, los jugadores están en la misma posición que en un turno anterior, y es el turno del mismo jugador para moverse), el juego termina en empate.

Dado un grafo, y suponiendo que ambos jugadores juegan de manera óptima, devuelve:

- 1 si el ratón gana el juego,
- 2 si el gato gana el juego, o
- 0 si el juego termina en empate.

### Statement

Suficientemente explicado arriba

### Solution

Este problema es una combinación de grafos y un juego secuencial. Dos jugadores con información perfecta juegan de manera óptima uno contra el otro en pasos finitos, ya que el juego termina en empate una vez que se repite un estado anterior.

A partir de la descripción del empate, es sencillo extraer la definición de un estado:

- Posición del gato
- Posición del ratón
- Si el siguiente movimiento es del gato o del ratón

Estos conceptos recuerdan a la programación dinámica.

Denotemos el resultado del juego con una función `game(next_mover, i, j)`, donde $i$ es la posición del gato, $j$ es la posición del ratón, y `next_mover` puede ser el gato o el ratón. Por ejemplo, el valor `game(mouse, 3, 4)` es el resultado final del juego cuando el gato está en el nodo 3, el ratón está en el nodo 4, y es el turno del ratón para moverse. El resultado puede ser `CAT` (el gato gana), `MOUSE` (el ratón gana) o `DRAW` (empate).

Es sencillo obtener una definición recursiva.

El problema parece tener subestructuras óptimas y problemas superpuestos, que son propiedades deseables. Algunas otras soluciones incluso ignoran los problemas superpuestos y realizan un DFS recursivo, esperando que el algoritmo eventualmente termine.

¿Por qué las soluciones DFS y DP son incorrectas?

Algunas soluciones de DFS y DP no notan que los subproblemas pueden estar "entrelazados". Es decir, no son independientes. Según la definición anterior, `game(cat, i, j)` depende de `game(mouse, v, j)` donde $v$ es adyacente a $i$. A su vez, `game(mouse, v, j)` podría depender también de `game(cat, v, u)` donde $u$ es adyacente a $j$, lo que puede depender de `game(mouse, i, u)` y eventualmente depender de `game(cat, i, j)` ¡en sí mismo!

Otros intentan sortear este problema marcando el estado inicial antes de resolver otros subproblemas para romper el ciclo. Sin embargo, en realidad están resolviendo un subproblema completamente diferente, ya que el conjunto de estados disponibles se reduce. (Ver la siguiente sección "Intento ingenuo de arreglar DP").

La dificultad radica en que puede existir tal dependencia circular, porque en un grafo no dirigido donde la adyacencia es conmutativa, los subproblemas no son independientes. Resolver uno de los subproblemas requerirá resolver otro, que a su vez requiere resolver el problema inicial.

Intuición:

Si los subproblemas dependen entre sí, ¿cómo sería posible resolverlos? Después de todo, estamos en un ciclo interminable para evaluar el resultado de `game(cat/mouse, i, j)`.

Intento ingenuo de arreglar DP:

Es factible definir otro estado para evitar este problema. No se nos permite alcanzar un estado anterior por segunda vez, entonces ¿por qué no agregar otro parámetro que indique los estados disponibles en ese momento (o, de manera equivalente, los estados visitados previamente)? De esta manera, el subproblema se puede definir como `game(cat/mouse, i, j, conjunto de estados disponibles)`.

Desafortunadamente, esta única modificación aumentaría el número de estados a una escala prohibitivamente grande. En el problema original, denotemos el conjunto (y su cardinalidad) de nodos por $V$ y de aristas por $E$. Entonces, hay $V \times V \times 2$ estados en total (aunque no todos son legales, ya que el gato no puede alcanzar el agujero y el ratón no necesita moverse más desde el agujero). Después de incluir el parámetro adicional, hay $2^{(V^2 \times 2)}$ combinaciones posibles, como máximo $2^{5000}$ en nuestro problema.

BFS, Volviendo a la fórmula recursiva:

Observamos que la condición en nuestra definición recursiva es codiciosa: a veces podemos determinar el resultado de un subproblema incluso si solo conocemos una parte de sus subproblemas dependientes; es decir, si existe un $v$ que satisface `game(mouse, v, j) == 2`, podemos decir que `game(cat, i, j) = 2` (simétrico para el ratón).

Esto explica por qué aún podemos resolver algunos de los subproblemas a pesar de la existencia de interdependencia. Tenga en cuenta que ya conocemos ciertos estados en los que sabemos el resultado, a saber:

- **Gana el ratón:** `game(cat, i, 0)`, $i \neq 0$, en el cual el ratón acaba de llegar al agujero mientras el gato está en otro lugar.
- **Gana el gato:** `game(cat/mouse, i, i)`, $i \neq 0$, en el cual el ratón y el gato se encuentran fuera del agujero, y por lo tanto el ratón es atrapado.

Entonces, a partir de los estados conocidos, podemos obtener algunos resultados para otros subproblemas, que podrían incluir nuestro objetivo `game(mouse, 2, 1)`. En caso de que no logremos determinar el valor, lo consideramos un empate (`DRAW`): ninguno de los jugadores puede lograr un mejor resultado que un empate. A menos que el oponente pueda forzar una victoria, un jugador siempre puede elegir el estado "seguro" hasta un empate.

Intuición:

Nuestra idea debería estar clara ahora: a partir de los estados conocidos, intentamos deducir el resultado de otros subproblemas (sub-juegos) lo mejor posible. Si podemos determinar el resultado de `game(mouse, 2, 1)`, todo va bien. Si no, habrá un empate.

BFS puede realizar bien esta tarea. Ponemos esos estados iniciales en una cola, examinamos los posibles cambios en los resultados de otros subproblemas, y añadimos los subproblemas activados en la cola. Para rastrear los estados de los nodos adyacentes, necesitamos mantener una tabla para registrar el número de subproblemas "coloreados" por un cierto resultado.

Relajación de Bellman-Ford:

Pero, ¿por qué molestarse con la complejidad de mantener tal tabla? El código debe transmitir la idea del programador de manera clara y concisa, y en muchas situaciones, la simplicidad del código supera la eficiencia. BFS es genial, pero es excesivo para el problema.

Pensemos en este problema de una manera más directa. Queremos expandir el conjunto de subproblemas determinables tanto como sea posible. Para ver si hay algún otro subproblema que se pueda determinar pero aún no descubierto, simplemente examinamos todo el conjunto de estados. Si no encontramos ningún subproblema determinable además de los conocidos, decimos que el conjunto ha convergido y, por lo tanto, el algoritmo termina. Si algún subproblema se determina (es decir, se "relaja"), entonces examinaremos todos los estados nuevamente en la siguiente ronda.

Este procedimiento está garantizado para terminar después de $O(V^2)$ iteraciones. La prueba es similar al algoritmo de Bellman-Ford. Cualquier camino más corto es simple, lo que implica que no puede haber vértices duplicados en el camino más corto. Puede haber como máximo $V$ vértices en un camino más corto, por lo que si cada escaneo incrementa el camino en uno, necesitamos $|V| - 1$ iteraciones en el peor de los casos.

Del mismo modo, expandimos nuestro conjunto de estados determinables al menos en uno por iteración. Una vez que un estado (o el juego correspondiente) se determina, es decir, se convierte de estado `DRAW` a otro, no se puede revertir. Por lo tanto, necesitamos como máximo $V^2 \times 2$ iteraciones.

Análisis de tiempo

Cada iteración examina una vez cada estado en todo el conjunto, así como sus estados adyacentes. Cada arista se examina $O(V)$ veces (hay $O(V)$ estados incidentes para una arista), por lo tanto, el tiempo de cómputo es $O(V^2 + VE)$ en total. Suponiendo que el grafo está conectado ($V = O(E)$), la complejidad de tiempo es $O(VE)$ por iteración.

COMPLEJIDAD TEMPORAL:
O(n^3)
