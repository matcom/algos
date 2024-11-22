# DP

## Zombies

En una ciudad infestada de zombis, los pocos supervivientes están intentando escapar. La ciudad está representada por un conjunto de intersecciones conectadas por calles, y cada camino tiene una longitud.

Lázaro, uno de los supervivientes propone buscar el camino más corto en un mapa que encontró tirado por ahí. Cuando el grupo está a punto de partir, Jose se levanta y dice: "Tengo una idea mejor. En lugar de ir por el camino más corto, busquemos uno de los más largos, de al menos tamaño $k$. Así sorprenderemos a los zombies, nunca dejes que sepan tu próximo movimiento".

El grupo de brillantes supervivientes comenzó a aplaudir asombrado, mientras que lázaro se quedaba frío pensando "¿de cuando acá los zombies pueden razonar?"

Ayude al grupo encontrando, dado un mapa de intersecciones y calles, si existe un camino simple de tamaño al menos $k$.

(PD: De más está decir que todo el grupo murió entre terribles sufrimientos).

### Statement

Given a graph and an integer $$ k $$, does there exist a simple path of length at least $$ k $$?

### Solution

Reduces from: Hamiltonian Path
Reduction Idea: Transform the Hamiltonian path problem into the longest path problem by setting $$ k $$ to the number of vertices minus one, ensuring that the existence of a Hamiltonian path corresponds to a long path.
