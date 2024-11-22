# Problemas

## Zombies

En una ciudad infestada de zombis, los pocos supervivientes están intentando escapar. La ciudad está representada por un conjunto de intersecciones conectadas por calles, y cada camino tiene una longitud.

Roger, uno de los supervivientes propone buscar el camino más corto en un mapa que encontró tirado por ahí. Cuando el grupo está a punto de partir, Jan se levanta y dice: "Tengo una idea mejor. En lugar de ir por el camino más corto, busquemos uno de los más largos, de al menos tamaño $k$. Así sorprenderemos a los zombies, nunca dejes que sepan tu próximo movimiento".

El grupo de brillantes supervivientes comenzó a aplaudir asombrado, mientras que Roger se quedaba frío pensando "¿de cuando acá los zombies pueden razonar?"

Ayude al grupo encontrando, dado un mapa de intersecciones y calles, si existe un camino simple de tamaño al menos $k$.

(PD: De más está decir que todo el grupo murió entre terribles sufrimientos).

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

## Sufijo Balanceado

Te dan una cadena $S$ de longitud $N$ y un número entero $K$.

Sea $C$ el conjunto de todos los caracteres en $S$. La cadena $S$ se llama buena si, para cada sufijo de $S$:

La diferencia entre las frecuencias de cualquier par de caracteres en $C$ no excede $K$.
En particular, si el conjunto $C$ tiene un solo elemento, la cadena $S$ es buena.

Encuentra si existe una reordenación de $S$ que sea buena.
Si existen múltiples reordenaciones de este tipo, imprime la reordenación lexicográficamente más pequeña.
Si no existe tal reordenación, imprime $-1$ en su lugar.

Nota que un sufijo de una cadena se obtiene eliminando algunos (posiblemente cero) caracteres desde el principio de la cadena. Por ejemplo, los sufijos de $S = abca$ son $\\{a, ca, bca, abca\\}$.
