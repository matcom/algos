# Grafos

## El Viaje

Kenny y Jesús quieren hacer un viaje por carretera de La Habana a Guantánamo.  
**Objetivo**: Fiesta.  
**Obstáculo**: Precio de la gasolina. Incluyendo el punto de salida (La Habana) y de destino (Guantánamo), hay un total de $n$ puntos a los que es posible visitar, unidos por $m$ carreteras cuyos costos de gasolina se conocen.  
Los compañeros comienzan entonces a planificar su viaje.

Luego de pensar por unas horas, Kenny va entusiasmado hacia Jesús y le entrega una hoja. En esta hoja se encontraban $q$ tuplas de la forma $(u, v, l)$ y le explica que a partir de ahora considerarían como útiles sólo a los caminos entre los puntos $u$ y $v$ cuyo costo de gasolina fuera menor o igual a $l$, para $u$, $v$, $l$ de alguna de las $q$ tuplas.

Jesús lo miró por un momento y le dijo: *Gracias*. La verdad esta información no era del todo útil para su viaje. Pero para no desperdiciar las horas de trabajo de Kenny, se dispuso a buscar lo que definió como carreteras útiles. Una carretera útil es aquella que pertenece a algún camino útil.  
Ayude a Kenny y Jesús encontrando el número total de carreteras útiles.

PD: Cuando le contaron del plan a Sheyla, esta se preguntó extrañada por qué Kenny y Jesús  
no habían simplemente buscado el camino de costo mínimo entre La Habana y Guantánamo.  
Hay que estudiar más discreta.

### Statement

Se te da un grafo no dirigido y ponderado con $n$ vértices, junto con $q$ tríos $(u, v, l)$, donde en cada trío $u$ y $v$ son vértices y $l$ es un entero positivo. Una arista $e$ se llama útil si existe al menos un trío $(u, v, l)$ y un camino (no necesariamente simple) con las siguientes propiedades:

- $u$ y $v$ son los extremos de este camino,
- $e$ es una de las aristas de este camino,
- La suma de los pesos de todas las aristas en este camino no excede $l$.

Imprime el número de aristas útiles en este grafo.

### Solution

Encuentra todas las distancias entre los vértices usando el algoritmo de Floyd con complejidad $O(n^3)$. Considera todos los tríos con un punto final fijo, digamos $v$. Vamos a encontrar todas las aristas útiles correspondientes a dichos tríos.

Una arista $(a, b, w)$ es útil si existe un trío $(v, u_i, l_i)$ tal que:

$$ \text{dist}(v, a) + w + \text{dist}(b, u_i) \leq l_i \quad \text{equivalente a} \quad -l_i + \text{dist}(u_i, b) \leq -w - \text{dist}(v, a). $$

Observa que el lado derecho de la desigualdad depende solo del vértice fijo $v$ y de la propia arista, por lo que vamos a minimizar el lado izquierdo sobre todos los posibles tríos. Esto se puede hacer usando el algoritmo de Dijkstra en $O(n^2)$ si inicializamos la distancia a todos los $u_i$ con $-l_i$.

Una vez que hemos realizado esto para todos los vértices $v$, solo queda verificar para cada arista si ha sido marcada como útil para algún vértice $v$.
