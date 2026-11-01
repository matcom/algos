**Problema:** En un splay tree que empieza como un camino de nodos se accede a las claves en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? 

Un árbol Splay que comienza estructurado como un camino lineal de $n$ nodos, es decir, una estructura degenerada equivalente a una lista enlazada, donde cada nodo tiene a lo sumo un hijo, ordenados secuencialmente de la clave 1 a la clave $n$. Se accede a las $n$ claves del árbol en un orden estrictamente creciente $(1, 2, ..., n)$.

## Acotación del costo con el Lema de Acceso
1. Función de Potencial y Rangos
En el análisis amortizado de árboles Splay mediante el método de potencial, la función de potencial del árbol $\Phi(T)$ se define como la suma de los rangos de todos sus nodos:
$$\Phi(T) = \sum_{x \in T} r(x)$$

Donde el rango $r(x)$ de un nodo $x$ se define logarítmicamente en función del tamaño de su subárbol $s(x)$ (el número de descendientes de $x$, incluyéndose a sí mismo): $r(x) = log_2s(x)$

El Lema de Acceso establece que el costo amortizado $\hat{c}$ de realizar la operación $splay(x)$ sobre un nodo $x$ está acotado superiormente por:
$$\hat{c} \le 3 \left( r(\text{root}) - r(x) \right) + 1 = 3 \log_2 \left( \frac{s(\text{root})}{s(x)} \right) + 1$$
Como el tamaño del subárbol de la raíz es siempre $s(root) = n$, el costo amortizado de acceder a cualquier nodo $x$ que tenga un subárbol de tamaño $s(x)$ es: $$\hat{c}(x) = \mathcal{O}\left( \log_2 \left( \frac{n}{s(x)} \right) \right)$$

## Sumatoria del costo total para el acceso secuencial (1, 2, ..., n)
Si aplicamos el Lema de Acceso de forma general para cada acceso $i$ en la secuencia $1, 2, ..., n$, el costo amortizado acumulado se obtiene de los costos individuales:
$$\text{Costo Amortizado Total} = \sum_{i=1}^{n} \left( 3 \log_2 \left( \frac{n}{s(i)} \right) + 1 \right)$$

En el peor escenario estructural considerado por el lema (donde el tamaño del subárbol s(i) para cada elemento al momento de su acceso es acotado de manera conservadora), al sumar los términos logarítmicos $log_2(n/i)$:
$$\sum_{i=1}^{n} \log_2 \left( \frac{n}{i} \right) = \sum_{i=1}^{n} (\log_2 n - \log_2 i) = n \log_2 n - \log_2(n!)$$

Utilizando la aproximación de Stirling para el factorial ($\log_2(n!) = \Theta(n \log_2 n)$):
$$\text{Costo Total Acotado por el Lema de Acceso} = \mathcal{O}(n \log n)$$

## Análisis
El teorema de Acceso Secuencial demuestra rigurosamente que el costo real total de acceder a las $n$ claves en orden secuencial $(1, 2, ..., n)$ en un árbol Splay es $O(n)$, independientemente de la forma inicial del árbol (incluso si parte como el peor camino lineal posible).

**Intuición de porqué es lineal:**
A medida que realizan los primeros accesos en orden $(1,2,...)$, las operaciones de splay reestructuran el árbol de manera tan agresiva y eficiente que colapsan el camino lineal, transformándolo en un árbol equilibrado. Los accesos subsiguientes encuentran los nodos a una profundidad sumamente baja, amortizando de forma extraordinariael costo de los primeros accesos.

## ¿Es ajustada la cota?
No, la cota obtenida mediante el lema de acceso no es ajustada para esta caso en particular.
Comparación de los resultados:
1. Cota obtenida por el lema de acceso: $O(nlogn)$
2. Costo real por el teorema de acceso secuencial: $O(n)$