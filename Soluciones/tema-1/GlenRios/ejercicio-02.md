# Problema 2 ★

**Enunciado.** Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

## Solución formal

**Algoritmo.** Búsqueda binaria en un arreglo ordenado $A[0..n-1]$ para un valor $x$.

**Invariante.** Antes de cada iteración se cumple:

$$
\text{si } x \text{ está en } A,\ \text{entonces } x \in A[lo:hi].
$$

Inicialmente $lo=0$, $hi=n$, y el invariante se cumple trivialmente. En cada paso se compara $x$ con $A[mid]$, donde $mid = \lfloor (lo+hi)/2 \rfloor$:

- Si $A[mid] = x$, se encontró el elemento.
- Si $A[mid] < x$, entonces $x$ no puede estar en $A[lo:mid]$, por lo que se actualiza $lo = mid+1$.
- Si $A[mid] > x$, entonces $x$ no puede estar en $A[mid:hi]$, por lo que se actualiza $hi = mid$.

En ambos casos el invariante se mantiene. Al terminar, $lo = hi$, el rango es vacío, y por tanto $x$ no está en $A$.

**Potencial.** Se define $\Phi = hi - lo$. Inicialmente $\Phi = n$. En cada iteración, el nuevo intervalo tiene longitud estrictamente menor que la mitad del anterior, de modo que $\Phi$ decrece al menos a la mitad. Como $\Phi$ es un entero no negativo, el ciclo termina. El número de iteraciones es a lo sumo $\lceil \log_2(n+1)\rceil$.

**Cota de información.** Si $x$ no está en $A$, cae en uno de los $n+1$ huecos entre elementos. En el árbol de decisión, para esos casos ninguna comparación puede dar “=”, así que solo se usan las ramas “<” y “>”. Esto forma un árbol binario con $n+1$ hojas. Por el lema del árbol binario, su altura es al menos $\lceil \log_2(n+1)\rceil$. La búsqueda binaria alcanza exactamente esa cota, por lo que es óptima en el modelo de comparaciones.
