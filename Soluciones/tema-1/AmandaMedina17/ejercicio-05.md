**Problema:** Detección de ciclos en una lista enlazada con dos punteros $A$ y $B$ que avanzan a velocidades $1$ y $2$ respectivamente (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

## 1. Correctitud mediante Invariante
Para demostrar que los punteros se encuentran si y solo si existe un ciclo, formulamos el siguiente invariante de ciclo:
* Si la lista tiene un ciclo de longitud $L$, en cada iteración en la que los punteros se encuentran dentro del ciclo, la distancia desde el puntero $A$ al puntero $B$ disminuye en cada paso hasta llegar a 0. Si noy hay ciclo el puntero $B$ avanzará hasta el final de la lista sin colisionar con el puntero $A$.

**Demostración**
* Caso donde no hay ciclos: EL puntero más rápido se desplaza estrictamente hacia adelante sobre una linea finita. Como no hay bucles y avanza más rápido, llegará inevitablemente a un apuntador $None$, por lo que se concluye que no hay ciclos.
* Caso donde hay ciclos: Cuando los dos punteros ingresan al ciclo, el puntero $B$ se encuentra a cierta distancia del puntero $A$. En cada iteración, el puntero $A$ avanza un paso y el $B$ avanza 2, lo que significa que en cada iteración la distancia entre ellos se acorta en 1 nodo. Esto quiere decir que ambos están obligados a encontrarse en a lo sumo $L$ iteraciones (longitud del ciclo).

## 2. Terminación del Potencial:
Definimos una función de potencial  $\Phi$ que mide el progreso hacia el fin de la ejecución:
* Si la lista no tiene ciclo,  $\Phi$ representa el número de enlaces que le falta al nodo B para alcanzar el $None$.
* Si la lista tiene un ciclo,  $\Phi$ representa la cantidad de nodos que faltan desde la posición del puntero $B$ hasta el puntero $A$ a lo largo del ciclo.
Este potencial cumple que es no negativo durante toda la ejecución. Además, cumple el decrecimiento estricto ya que, en las listas acíclicas el puntero $B$ se acerca estrictamente al final en cada paso, reduciendo  $\Phi$, y en las listas con ciclos, cada iteración reduce la distancia entre los dos punteros en una unidad, por lo que  $\Phi$ disminuye estrictamente hasta alcanzar a 0. Luego, como  $\Phi$ es una cantidad entera no negativa que decrece estrictamente en cada iteración del bucle, el algoritmo termina siempre.

## 3. Analisis de costo:
* Si no hay ciclos, el puntero más rápido recorre la lista en $O(N)$.
* Si hay un ciclo de longitud $L$, y digamos que antes de ese ciclo hay una linea de nodos de longitud $M$, es decir $(N = L + M)$, el puntero $A$ ingresa al ciclo en $M$ pasos y es alcanzado por $B$ en a la sumo $L$ pasos dentro del ciclo. Por tanto, el tiempo en el peor caso en $O(N)$.
* Como el algoritmo solo usa dos variable de referencia $(A y B)$ por lo que la memoria requerida es $O(1)$.