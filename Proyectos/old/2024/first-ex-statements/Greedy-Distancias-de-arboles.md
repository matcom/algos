# Greedy

## Distancia de Árboles

Un árbol se define como un grafo conectado y no dirigido con $n$ vértices y $n - 1$ aristas. La distancia entre dos vértices en un árbol es igual al número de aristas en el camino simple único entre ellos.

Te dan dos enteros $x$ y $y$. Construye un árbol con las siguientes propiedades:

- El número de pares de vértices con una distancia par entre ellos es igual a $x$.
- El número de pares de vértices con una distancia impar entre ellos es igual a $y$.

Por un par de vértices, nos referimos a un par ordenado de dos vértices (posiblemente, el mismo o diferente).

### Statement

Te dan dos enteros $x$ y $y$. Tu tarea es construir un árbol con las siguientes propiedades:

- El número de pares de vértices con una distancia par entre ellos es igual a $x$.
- El número de pares de vértices con una distancia impar entre ellos es igual a $y$.

Por un par de vértices, nos referimos a un par ordenado de dos (posiblemente, el mismo o diferente) vértices.

### Solution

La primera observación básica que podemos hacer es que la suma de $x$ y $y$ debe ser un cuadrado perfecto.

¿Por qué?
Dado que cada vértice forma un par con cada otro vértice de un árbol, incluido él mismo, para cualquier árbol de $N$ vértices, el número total de pares ordenados de vértices será $N^2$.

Como la suma de $x$ y $y$ representa el número total de pares ordenados de vértices, esto debe ser un cuadrado perfecto. Por lo tanto, $x + y$ debe ser un cuadrado perfecto.

Ahora, debemos encontrar si es posible tener un árbol que tenga $x$ pares de vértices con una distancia par entre ellos y $y$ pares de vértices con una distancia impar entre ellos.

Está bastante claro que cualquier vértice del árbol puede estar en un nivel par o en un nivel impar. La raíz del árbol está en el nivel par ($0$ - indexado de manera base $0$). Veamos cuántos pares de vértices tienen una distancia impar entre ellos.

Teorema:
Cualquier par de vértices $(x, y)$ tiene una distancia impar entre ellos si los vértices $x$ y $y$ provienen de niveles de paridad opuesta.

Prueba
Supongamos que el vértice $x$ está en un nivel par y el vértice $y$ en un nivel impar. La distancia entre dos nodos se puede obtener en términos del menor ancestro común (lca). A continuación se muestra la fórmula para la misma:

$$
dis(x, y) = dis(root, x) + dis(root, y) - 2 \times dis(root, lca)
$$

Dado que $x$ está en un nivel par, $dis(root, x)$ es par, mientras que $y$ está en un nivel impar, por lo que $dis(root, y)$ es impar. Por lo tanto, podemos ver que:

$$
dis(x, y) = Par + Impar - Par
$$

Esto significa que si los vértices están en niveles de paridad opuesta, la distancia entre ellos es impar.

Cálculo de los pares de vértices con una distancia impar
Para las distancias impares, cada vértice en un nivel impar formará un par con cada vértice en un nivel par, y viceversa.

Supongamos que $[e_1, e_2, e_3, \dots, e_i]$ son los vértices en niveles pares, y $[o_1, o_2, o_3, \dots, o_j]$ son los vértices en niveles impares. Ahora, para cada vértice en un nivel par, formará un par con cada vértice en un nivel impar, y viceversa. Por lo tanto:

$$
Odd \ pairs' = (e_1 \times o_1 + e_1 \times o_2 + \dots + e_1 \times o_j + \dots + e_i \times o_1 + \dots + e_i \times o_j)
$$

$$
Odd \ pairs' = (e_1 + e_2 + e_3 + \dots + e_i) \times (o_1 + o_2 + o_3 + \dots + o_j)
$$

$$
Odd \ pairs' = E \times O
$$

Donde $E$ y $O$ representan el número de nodos en niveles pares e impares, respectivamente.

Dado que estamos considerando pares ordenados, el número de estos pares se duplicará. Si $(x, y)$ es un par con una distancia impar entre ellos, entonces $(y, x)$ también tendrá una distancia impar. Por lo tanto:

$$
Odd \ pairs = 2 \times E \times O
$$

Esto significa que solo nos importa el número de vértices en niveles pares e impares. La raíz es el único nodo en el nivel $0$, y si queremos más nodos en un nivel par, debe existir al menos un vértice en un nivel impar. Ahora podemos verificar todas las posibilidades y encontrar si existe una disposición de vértices que satisfaga $x$ y $y$ según el problema. Si es así, podemos construir y mostrar el árbol.

COMPLEJIDAD TEMPORAL:
$O(\sqrt{X + Y})$
