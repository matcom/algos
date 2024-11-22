# Grafos

## PCC

Han pasado 20 años desde que Lázaro se graduó de Ciencias de la Computación  
(haciendo una muy buena tesis) y las vueltas de la vida lo llevaron a convertirse  
en el presidente del Partido Comunista de Cuba. Una de sus muchas responsabilidades  
consiste en visitar zonas remotas. En esta ocasión debe visitar una  
ciudad campestre de Pinar del Río.

También han pasado 20 años desde que Marié consiguió su título en MATCOM.  
Tras años de viaje por las grandes metrópolis del mundo, en algún punto  
decidió que prefería vivir una vida tranquila, aislada de la urbanización, en una  
tranquila ciudad de Pinar del Río. Las vueltas de la vida quisieron que precisamente  
Marié fuera la única universitaria habitando la ciudad que Lázaro se  
dispone a visitar.

Los habitantes de la zona entraron en pánico ante la visita de una figura tan  
importante y decidieron reparar las calles de la ciudad por las que transitaría  
Lázaro. El problema está en que nadie sabía qué ruta tomaría el presidente y  
decidieron pedirle ayuda a Marié.

La ciudad tiene $n$ puntos importantes, unidos entre sí por calles cuyos  
tamaños se conoce. Se sabe que Lázaro comenzará en alguno de esos puntos  
($s$) y terminará el viaje en otro ($t$). Los ciudadanos quieren saber, para  
cada par $s$, $t$, cuántas calles participan en algún camino de distancia mínima  
entre $s$ y $t$.

### Statement

Dado un país con n ciudades y m caminos. Cada camino conecta un par de ciudades distintas y es bidireccional. Entre cualquier par de ciudades, como máximo hay un camino. Para cada camino, se conoce su longitud.

Sabemos que el Presidente pronto viajará desde la ciudad s hasta la ciudad t y elegirá uno de los caminos más cortos de s a t, pero no se sabe cuál camino escogerá.

se desea reparar los caminos en las posibles rutas del Presidente.

Para todos los pares distintos s, t (s < t), encuentra el número de caminos que están en al menos un camino más corto entre s y t.

### Solution

Necesitamos contar la cantidad de aristas en todos los caminos más cortos entre cada par de vértices. Hagamos algo más sencillo primero: en lugar de contar todas las aristas, contaremos solo aquellas que tienen el vértice de destino en su lado. Por ejemplo, estas son las aristas que pertenecen a los caminos más cortos desde 4 a 2 que están conectadas al vértice 2:

Denotemos este número de la siguiente manera: inEdgessource, v — número de aristas que llegan al vértice v en algún camino más corto desde el vértice fuente al vértice v. En el ejemplo dado, inEdges4, 2 = 3. También denotemos el conjunto Ssource, dest — es el conjunto de los vértices que pertenecen a al menos un camino más corto desde source a dest. Por ejemplo, S4, 2 = {1, 2, 3, 4}. Con estas dos variables se puede ver que la respuesta para los vértices source y dest será:

$Edges(s,d) = \sum_{v \in S_{s,d}} InEdges(s,v)$

En otras palabras, la respuesta para los vértices s y d será igual a la suma de inEdgess, v para todos los vértices v que pertenecen a algún camino más corto de s a d. Entonces, lo único que queda es calcular estos S y inEdges. Ambos se pueden calcular fácilmente si se tienen las distancias mínimas entre todos los pares de vértices. Y estas distancias se pueden calcular utilizando el algoritmo de Floyd-Warshall. Por lo tanto, la solución completa es:

1. Calcular las distancias mínimas entre todos los pares de vértices utilizando el algoritmo de Floyd-Warshall.

2. Contar inEdges. Simplemente itera sobre todos los vértices fuente y todas las aristas. Para cada arista, verifica si alguno de sus extremos pertenece a algún camino más corto desde la fuente.

3. Calcular la respuesta. Utiliza tres ciclos para iterar sobre los vértices: fuente, destino y mid. Los primeros dos vértices son aquellos para los cuales estamos calculando la respuesta. El tercer vértice es el vértice que debería pertenecer a algún camino más corto (básicamente estamos verificando si v pertenece a Ssource, dest). Si mid pertenece a algún camino más corto de source a dest, entonces sumamos inEdgessource, mid a la respuesta.

Cada paso tiene una complejidad de O(n^3).

COMPLEJIDAD TEMPORAL:
O(n^3)
