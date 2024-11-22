# Grafos

## Distancia de árboles

Un árbol se define como un grafo no dirigido y conectado con $n$ vértices y $n-1$ aristas. La distancia entre dos vértices en un árbol es igual al número de aristas en el camino simple único entre ellos.

Se te dan dos enteros $x$ y $y$. Construye un árbol con las siguientes propiedades:

- El número de pares de vértices con una distancia par entre ellos es igual a $x$.
- El número de pares de vértices con una distancia impar entre ellos es igual a $y$.

Por par de vértices, nos referimos a un par ordenado de dos vértices (posiblemente, el mismo o diferente).

### Statement

Se te dan dos enteros $x$ y $y$. Tu tarea es construir un árbol con las siguientes propiedades:

- El número de pares de vértices con una distancia par entre ellos es igual a $x$.
- El número de pares de vértices con una distancia impar entre ellos es igual a $y$.

Por par de vértices, nos referimos a un par ordenado de dos vértices (posiblemente, el mismo o diferente).

### Solution

La primera observación básica que podemos hacer es que la suma de $x$ y $y$ debe ser un cuadrado perfecto.

### ¿Por qué?

Dado que cada vértice forma un par con todos los demás vértices de un árbol, incluido él mismo, para cualquier árbol de $N$ vértices, el número total de pares ordenados de vértices será $N^2$.

Como la suma de $x$ y $y$ representa el número total de pares ordenados de vértices, que es un cuadrado perfecto, entonces $x + y$ debe ser un cuadrado perfecto.

Ahora, queda por determinar si es posible tener un árbol que tenga $x$ pares de vértices con una distancia par entre ellos y $y$ pares de vértices con una distancia impar entre ellos.

Está claro que cualquier vértice del árbol puede estar en un nivel par o en un nivel impar. La raíz del árbol está en el nivel par ($0$-basado en la indexación). Averigüemos cuántos pares de vértices tienen una distancia impar entre ellos.

Teorema:

Cualquier par de vértices $(x, y)$ tiene una distancia impar entre ellos si los vértices $x$ y $y$ están en niveles de paridad opuesta.

Demostración:

Supongamos que el vértice $x$ está en un nivel par y el vértice $y$ en un nivel impar. La distancia entre dos nodos se puede obtener en términos del ancestro común más bajo (LCA). A continuación se muestra la fórmula para calcularlo:

$$
dis(x, y) = dis(root, x) + dis(root, y) - 2 \times dis(root, lca)
$$

Dado que $x$ está en un nivel par, $dis(root, x)$ es par, mientras que $y$ está en un nivel impar, por lo que $dis(root, y)$ es impar. Por lo tanto, podemos ver:

$$
dis(x, y) = \text{Par} + \text{Impar} - \text{Par}
$$

Eso significa que si los vértices están en niveles de paridad opuesta, entonces la distancia entre ellos es impar.

Ahora calculemos cuántos pares de vértices tienen una distancia impar entre ellos. Para distancias impares, cada vértice que está en un nivel impar formará un par con cada vértice que esté en un nivel par y viceversa.

Supongamos que $[e_1, e_2, e_3, \dots, e_i]$ y $[o_1, o_2, o_3, \dots, o_j]$ son los vértices que están en niveles pares e impares, respectivamente. Ahora, para cada vértice que está en un nivel par, formará un par con cada vértice que está en un nivel impar y viceversa. Por lo tanto:

$$
\text{Pares impares} = (e_1 \times o_1 + e_1 \times o_2 + \dots + e_1 \times o_j + \dots + e_i \times o_1 + \dots + e_i \times o_j)
$$

$$
\text{Pares impares} = (e_1 + e_2 + e_3 + \dots + e_i) \times (o_1 + o_2 + o_3 + \dots + o_j)
$$

$$
\text{Pares impares} = E \times O
$$

donde $E$ y $O$ representan el número de nodos que están en niveles pares e impares, respectivamente.

Dado que estamos buscando los pares ordenados de dos, el número de pares anteriores se duplicará. Es decir, si $(x, y)$ es un par que tiene una distancia impar entre ellos, entonces $(y, x)$ también tendrá una distancia impar entre ellos. Por lo tanto:

$$
\text{Pares impares} = 2 \times E \times O
$$

Eso significa que solo nos importa el número de vértices que están en niveles pares e impares. La raíz es el único nodo que está en el nivel $0$, y si queremos más nodos en un nivel par, debe existir al menos un vértice en un nivel impar. Ahora podemos verificar cada posibilidad y encontrar si existe tal disposición de vértices que satisfaga $x$ y $y$ del problema. Si es así, podemos construir el árbol.

COMPLEJIDAD TEMPORAL:
$O(\sqrt{X+Y})$
