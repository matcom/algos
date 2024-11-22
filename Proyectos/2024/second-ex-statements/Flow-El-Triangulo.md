# Grafos

## El triángulo

Javier estaba un día practicando con su instrumento favorito: El triángulo. El  
triángulo es un instrumento musical tan espectacular que sus notas se escriben  
como números enteros. Este día Javier se propuso componer una canción de  
una forma bastante peculiar. Tomó $n$ enteros (notas) aleatorios y los escribió  
en una lista $a$. Una melodía válida es una subsecuencia de $a$ en la que todos sus  
números adyacentes cumplen que:  

- Se diferencian en $1$.  
- Son congruentes módulo $7$.  

La canción de Javier debe contener exactamente $4$ melodías que cumplan con  
lo anterior y además no se intercepten entre sí. Ayude a Javier encontrando una  
canción que maximice las notas usadas.

### Statement

Dado un conjunto de $n$ elementos, se deben tomar cuatro subsecuencias no vacías y no intersectantes de manera que la suma de sus longitudes sea máxima.

Una subsecuencia es una secuencia que se puede derivar de otra eliminando algunos elementos sin cambiar el orden de los elementos restantes.

Una subsecuencia es válida cuando cada dos elementos adyacentes o bien difieren en 1, o son congruentes módulo 7.

Debes escribir un programa que calcule la suma máxima de longitudes de dichas cuatro subsecuencias no vacías y no intersectantes que cumplan con las condiciones dadas.

### Solution

Construyamos un grafo dirigido donde los vértices representan elementos y una arista dirigida va del vértice $i$ al vértice $j$ si y solo si $i < j$ y $a_i$ y $a_j$ pueden ser consecutivos en una secuencia válida. Ahora debemos encontrar cuatro caminos más largos y disjuntos en este grafo.

Este problema se puede resolver utilizando algoritmos de flujo de costo mínimo $k$. Construimos una red donde cada vértice del grafo se divide en dos (denotemos los vértices que obtenemos al dividir un vértice $i$ como $v_{i,1}$ y $v_{i,2}$). Luego, cada arista dirigida se transforma en una arista dirigida desde el vértice $v_{i,2}$ hasta el vértice $v_{j,1}$ en la red, la capacidad de esta arista es 1 y el costo es 0. También añadimos aristas dirigidas desde la fuente a cada vértice $v_{i,1}$ y desde cada vértice $v_{i,2}$ al sumidero (tienen las mismas características: capacidad es 1, costo es 0). Para cada $i$, añadimos una arista dirigida entre $v_{i,1}$ y $v_{i,2}$; estas aristas representan el uso de un elemento en una secuencia, por lo que sus capacidades también son igual a 1, y sus costos son $-1$. La respuesta al problema es igual al valor absoluto del costo mínimo de un flujo de 4 en esta red.

El problema es que la red es realmente grande. Por lo tanto, debemos usar algún algoritmo avanzado de costo mínimo.

La solución modelo usa el algoritmo de Dijkstra con potenciales de Johnson para encontrar caminos aumentantes de costo mínimo. Asignamos un número $p(v)$ a cada vértice $v$ de la red (estos números se llaman potenciales). Luego modificamos los costos de las aristas: si alguna arista tenía costo $c_{i,j}$, ahora su costo es $c'_{i,j} = c_{i,j} + p(i) - p(j)$. Es fácil demostrar que si algún camino entre los vértices $v$ y $u$ era el más corto sin modificar los costos con potenciales, entonces después de modificarlos seguirá siendo el más corto. Entonces, en lugar de buscar un camino aumentante en la red original, podemos buscarlo en una red con aristas modificadas. ¿Por qué? Porque siempre es posible establecer todos los potenciales de manera que todos los costos de las aristas sean no negativos (y podremos usar Dijkstra para encontrar el camino más corto de la fuente al sumidero).

Antes de buscar el primer camino aumentante, calculamos los potenciales recursivamente: $p(source) = 0$, $p(v) = \min{p(u) + c_{u,v}}$ (verificamos todos los $u$ tales que hay una arista en la red). La red es acíclica antes de empujar el flujo, por lo que siempre hay una manera de calcular estos potenciales con programación dinámica. Luego, cada vez que queremos encontrar un camino aumentante, ejecutamos el algoritmo de Dijkstra en la red modificada, empujamos flujo a través del camino que encontramos y modificamos los potenciales: el nuevo potencial de cada vértice $v$ se convierte en $p'(v) = p(v) + d(v)$, donde $d(v)$ es la distancia entre la fuente y el vértice $v$ en la red modificada (y encontramos esta distancia con Dijkstra). Cuando hemos encontrado cuatro caminos aumentantes, hemos terminado y es hora de evaluar el costo del flujo.
