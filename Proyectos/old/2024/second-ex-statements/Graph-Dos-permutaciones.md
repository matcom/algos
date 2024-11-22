# Grafos

## Dos permutaciones

Rodrigo es el maestro de una academia de magia y debe organizar y clasificar sus ingredientes mágicos. Son tan mágicos que, consumidos de la forma adecuada, te permiten ver criaturas fantásticas y luces de colores, dejando poca resaca (Rodrigo no los consume pues es un maestro sano). Tiene dos estantes mágicos, uno llamado "a" y otro llamado "b", ambos con $n$ frascos de pociones, cada uno etiquetado con un número del 1 al $n$. Cada frasco está en un lugar aleatorio en los estantes, pero el número en cada frasco es único en cada estante.

Tu tarea es ayudar a Rodrigo a organizar ambos estantes en el orden correcto, de modo que los números en los frascos estén en orden ascendente de izquierda a derecha en ambos estantes. Sin embargo, estos estantes mágicos sólo se pueden mover siguiendo unas reglas:

1. Puedes elegir cualquier número $i$ entre 1 y $n$;
2. Encuentra el frasco en el estante "a" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$;
3. Luego, encuentra el frasco en el estante "b" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$.

Tu objetivo es organizar ambos estantes con el menor número de movimientos posible, asegurándote de que todos los frascos en ambos estantes estén en el orden correcto al finalizar la tarea.

### Statement

Se te dan dos permutaciones $a$ y $b$, ambas de tamaño $n$. Una permutación de tamaño $n$ es un arreglo de $n$ elementos, donde cada entero de $1$ a $n$ aparece exactamente una vez. Los elementos en cada permutación están indexados de $1$ a $n$.

Puedes realizar la siguiente operación cualquier número de veces:

1. Elige un entero $i$ de $1$ a $n$;
2. Sea $x$ el entero tal que $a_x = i$. Intercambia $a_i$ con $a_x$;
3. Sea $y$ el entero tal que $b_y = i$. Intercambia $b_i$ con $b_y$.

Tu objetivo es ordenar ambas permutaciones en orden ascendente (es decir, que se cumplan las condiciones $a_1 < a_2 < \cdots < a_n$ y $b_1 < b_2 < \cdots < b_n$) utilizando el número mínimo de operaciones. Ten en cuenta que ambas permutaciones deben estar ordenadas después de realizar la secuencia de operaciones que hayas elegido.

### Solution

La solución a este problema utiliza la descomposición cíclica de permutaciones. Una descomposición cíclica de una permutación se formula de la siguiente manera: tratas una permutación como un grafo dirigido sobre $n$ vértices, donde cada vértice $i$ tiene un arco saliente $i \rightarrow p_i$. Este grafo consta de varios ciclos, y las propiedades de este grafo pueden ser útiles al resolver problemas basados en permutaciones.

Primero, ¿cómo se ve la descomposición cíclica de una permutación ordenada? Cada vértice pertenece a su propio ciclo formado por un bucle que va desde ese vértice hacia sí mismo. Intentaremos llevar las descomposiciones cíclicas de las permutaciones dadas a esta forma.

¿Qué hace una operación con el entero $i$ en la descomposición cíclica de la permutación? Si $i$ está en su propio ciclo separado, la operación no hace nada ($p_i = i$, por lo que intercambiamos un elemento consigo mismo).

De lo contrario, supongamos que $x$ es el elemento antes de $i$ en el mismo ciclo ($p_x = i$), y $y$ es el elemento después de $i$ en el mismo ciclo ($p_i = y$). Nota que este puede ser el mismo elemento. Cuando aplicamos una operación sobre $i$, intercambiamos $p_x$ con $p_i$, por lo que después de la operación, $p_i = i$, y $p_x = y$. Así que, $i$ sale del ciclo y forma su propio ciclo separado, y $y$ se convierte en el siguiente vértice en el ciclo después de $x$. Por lo tanto, al usar la operación, excluimos el vértice $i$ del ciclo.

Supongamos que queremos ordenar una permutación. Entonces, cada ciclo de longitud $\geq 2$ debe ser descompuesto: para un ciclo de longitud $c$, necesitamos excluir $c-1$ vértices de él para descomponerlo. El vértice que no tocamos puede ser cualquier vértice del ciclo, y todos los demás vértices del ciclo serán extraídos usando una operación dirigida a ellos. Es fácil ver ahora que si queremos ordenar una permutación, no necesitamos aplicar la misma operación dos veces, y el orden de las operaciones no importa.

Entonces, ¿qué pasa con ordenar dos permutaciones en paralelo? Cambiemos un poco el problema: en lugar de calcular el número mínimo de operaciones, intentaremos maximizar el número de enteros $i$ que no tocamos con las operaciones. Entonces, un entero $i$ puede quedar intacto si es el único vértice intacto en sus ciclos en ambas permutaciones... ¿Ves a dónde va esto?

Supongamos que queremos dejar el vértice $i$ intacto. Esto significa que en sus ciclos en ambas permutaciones, todos los demás vértices deben ser extraídos con una operación. Entonces, si dos ciclos de diferentes permutaciones tienen un vértice en común, podemos dejar este vértice intacto, siempre y cuando no haya otros vértices intactos en ambos ciclos. Construyamos un grafo bipartito, donde cada vértice en la parte izquierda representa un ciclo en la primera permutación, y cada vértice en la parte derecha representa un ciclo en la segunda permutación. Trataremos cada entero $i$ como una arista entre dos vértices respectivos en el grafo bipartito. Si la arista correspondiente a $i$ es "usada" ($i$ se deja intacto), no podemos "usar" ninguna arista incidente al mismo vértice en la parte izquierda o derecha. Entonces, maximizar el número de números intactos es en realidad lo mismo que encontrar el emparejamiento máximo en este grafo bipartito.

Después de encontrar el emparejamiento máximo, restaurar la respuesta real es fácil. Recuerda que las aristas saturadas por el emparejamiento corresponden a los enteros que no tocamos con nuestras operaciones, el orden de las operaciones no importa, y cada entero debe ser utilizado en una operación solo una vez. Por lo tanto, la respuesta real es el conjunto de todos los enteros sin aquellos que corresponden a las aristas del emparejamiento.

Esta solución se ejecuta en $O(n^2)$ incluso con una implementación directa del emparejamiento bipartito, ya que el grafo bipartito tiene como máximo $O(n)$ vértices y $O(n)$ aristas.

COMPLEJIDAD TEMPORAL:
$O(n^2)$
