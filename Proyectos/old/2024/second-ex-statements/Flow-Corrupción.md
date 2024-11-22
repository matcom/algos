# Grafos

## Corrupción

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

Se tiene un grafo simple (es decir, un grafo sin lazos ni múltiples aristas) que consta de $n$ vértices y $m$ aristas.

El peso del $i$-ésimo vértice es $a_i$.

El peso de la $i$-ésima arista es $w_i$.

Un subgrafo de un grafo es un conjunto de vértices del grafo y un conjunto de aristas del grafo. El conjunto de aristas debe cumplir la condición de que ambos extremos de cada arista del conjunto deben pertenecer al conjunto de vértices elegido.

El peso de un subgrafo es la suma de los pesos de sus aristas, menos la suma de los pesos de sus vértices. Necesitas encontrar el peso máximo de un subgrafo del grafo dado. El grafo dado no contiene lazos ni múltiples aristas.

### Solution

Este problema se puede reducir a uno de los problemas de flujo más conocidos: "Proyectos e Instrumentos". En este problema, tenemos un conjunto de proyectos que podemos realizar, cada uno con su costo, y un conjunto de instrumentos (cada uno también con un costo). Cada proyecto depende de algunos instrumentos, y cada instrumento se puede usar un número ilimitado de veces. Debemos elegir un subconjunto de proyectos y un subconjunto de instrumentos de manera que, si se elige un proyecto, también se eligen todos los instrumentos de los que depende dicho proyecto, y debemos maximizar la diferencia entre la suma de los costos de los proyectos elegidos y la suma de los costos de los instrumentos elegidos.

El problema sobre proyectos e instrumentos se puede resolver con la siguiente red de flujo:

- Para cada proyecto, se crea un vértice y se agrega una arista dirigida desde la fuente a este vértice con capacidad igual al costo de este proyecto.
- Para cada instrumento, se crea un vértice y se agrega una arista dirigida desde este vértice al sumidero con capacidad igual al costo de este instrumento.
- Para cada proyecto, se crean aristas con capacidad infinita desde el vértice que denota este proyecto a todos los vértices que representan los instrumentos requeridos para este proyecto.

Analicemos un corte $(S, T)$ entre la fuente y el sumidero en este grafo, y construyamos una solución basada en este corte de la siguiente manera: si un vértice de proyecto pertenece a $S$, entonces tomamos este proyecto; si un vértice de instrumento pertenece a $S$, entonces tomamos este instrumento; todos los demás proyectos e instrumentos se descartan. Si una arista entre algún proyecto y algún instrumento es cortada, entonces significa que la respuesta es incorrecta (intentamos tomar un proyecto que requiere algún instrumento que no tomamos), y el valor del corte es infinito. De lo contrario, el valor del corte es igual al costo total de los instrumentos tomados y los proyectos descartados, y necesitamos minimizarlo. Por lo tanto, el corte mínimo en esta red denota la mejor respuesta.

Reducir el problema dado a este problema es sencillo: las aristas del grafo dado son "proyectos", y los vértices del grafo dado son "instrumentos".

En cuanto a la implementación, cualquier algoritmo de flujo que utilice escalado de capacidad debería ser suficiente.

COMPLEJIDAD TEMPORAL:
$O(n^2m)$
