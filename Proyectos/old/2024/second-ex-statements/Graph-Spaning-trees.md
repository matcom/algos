# Grafos

## Ciudades

El país de Berland tiene inicialmente $N$ ciudades aisladas, donde la $i$-ésima ciudad tiene una significancia de $A_i$. El Presidente de Berland quiere conectar todas las ciudades. Él puede construir una carretera bidireccional de longitud $L$ $(L > 0)$ desde la ciudad $X$ a la ciudad $Y$ si $(A_X \& A_Y \& L) = L$, donde $ \& $ representa el operador AND bit a bit.

¿Cuál es la longitud total mínima de las carreteras que tiene que construir para conectar todas las ciudades en Berland? Imprime $-1$ si es imposible.

Nota:

Se dice que la ciudad $X$ y la ciudad $Y$ están conectadas si existe una secuencia de ciudades $C_1, C_2, \dots, C_K$ $(K \geq 1)$ tal que $C_1 = X$, $C_K = Y$, y existe una carretera desde $C_i$ a $C_{i+1}$ $(1 \leq i < K)$. Todas las ciudades en Berland se dicen conectadas cuando cada par de ciudades en Berland está conectado.

### Statement

Dado $N$ vértices donde el $i$-ésimo tiene un valor $A_i$, puedes dibujar una arista entre $u$ y $v$ de longitud $L$ si $L$ es una submáscara tanto de $A_u$ como de $A_v$.

Encuentra el costo mínimo para conectar todas las ciudades, o indica si es imposible hacerlo.

### Solution

Por el momento, supongamos que podemos conectar todos los $N$ vértices. Hagamos un par de observaciones:

1. El grafo final va a ser un árbol.
2. Cualquier arista $L$ en el grafo final tendrá una longitud que es una potencia de $2$, es decir, $L = 2^k$ para algún $k \geq 0$.

Demostración:

El primer punto debería ser obvio: si tenemos un ciclo, podemos eliminar alguna arista de él para obtener un costo estrictamente menor mientras preservamos la conectividad.

El segundo punto tampoco es difícil de ver: si una longitud contiene más de un bit activado, eliminar cualquier bit activado en ella aún la mantendrá como una arista válida, pero reducirá el costo.

Esto nos da inmediatamente una solución, aunque lenta:
Considera el (multi)grafo $G$ en $N$ vértices, donde para cada $(u, v, k)$ hay una arista entre $u$ y $v$ de longitud $2^k$ si $u$ y $v$ tienen ambos el $k$-ésimo bit activado.
Nuestra respuesta no es más que el peso del árbol de expansión mínima (MST) de este grafo.

Sin embargo, este grafo puede tener hasta $30 \cdot N^2$ aristas, y calcularlas todas es obviamente imposible, por lo que necesitamos hacerlo mejor.

Para optimizar esto, veamos cómo funcionaría el algoritmo de Kruskal para el MST en este grafo:

- Primero, considerará todas las aristas con peso $2^0$.
- Luego, considerará todas las aristas con peso $2^1$.
- Luego, considerará todas las aristas con peso $2^2$.
- Y así sucesivamente...

¿Qué tiene de especial esto?

Sea $x_1 < x_2 < \dots < x_m$ todos los vértices con el $k$-ésimo bit activado. Entonces, las aristas con peso $2^k$ son exactamente todos los pares de estos $m$ vértices.

Ahora, supongamos que encontramos $x_1, \dots, x_m$ para un $k$ fijo.
No necesitamos considerar todos los pares de estos $m$ vértices: simplemente necesitamos mantener suficientes aristas para conectarlos todos. La forma más sencilla de hacer esto es considerar solo las aristas $(x_1, x_2), (x_2, x_3), \dots, (x_{m-1}, x_m)$.

Observa que hacer esto reduce inmediatamente el número de aristas a $< N$ por bit, para un total de $< 30 \cdot N$ aristas en total. Esto es lo suficientemente pequeño como para que podamos ejecutar un algoritmo de MST en estas aristas directamente y obtener la respuesta.

Nota:
Si el grafo final que obtenemos no está conectado, la respuesta es $-1$, ya que no hay forma de conectarlo.

COMPLEJIDAD TEMPORAL:
O(n^3)
