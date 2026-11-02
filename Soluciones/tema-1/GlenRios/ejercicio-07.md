# Problema 7 ★★★

**Enunciado.** Mediana de dos arreglos ordenados de largo $n$: el $n$-ésimo menor de los $2n$ elementos. Diseña un algoritmo $O(\log n)$, demuestra su correctitud y da la cota de información.

## Solución formal

**Algoritmo.** Tenemos $A[0..n-1]$ y $B[0..n-1]$ ordenados. Buscamos el $n$-ésimo menor de los $2n$ elementos. Hacemos búsqueda binaria sobre un índice de partición $i$ en $A$, con $0 \le i \le n$. Definimos $j = n - i$. La partición divide los elementos en dos mitades:
- Izquierda $L(i) = A[0..i-1] \cup B[0..j-1]$, con exactamente $n$ elementos.
- Derecha $R(i) = A[i..n-1] \cup B[j..n-1]$, con los otros $n$.

Usamos las convenciones $A[-1] = B[-1] = -\infty$ y $A[n] = B[n] = +\infty$.

El algoritmo busca un $i$ que cumpla las condiciones de frontera:
$$
A[i-1] \le B[j] \quad \text{y} \quad B[j-1] \le A[i].
$$
Si encuentra un $i$ así, devuelve $\max(A[i-1], B[j-1])$.

La búsqueda binaria funciona así: con $lo=0$ y $hi=n$, mientras $lo \le hi$, tomamos $mid = \lfloor (lo+hi)/2 \rfloor$ y $j = n - mid$.
- Si $A[mid-1] > B[j]$, el índice $mid$ es muy grande, así que hacemos $hi = mid - 1$.
- Si $B[j-1] > A[mid]$, el índice $mid$ es muy pequeño, así que hacemos $lo = mid + 1$.
- Si no falla ninguna, $mid$ es válido y devolvemos $\max(A[mid-1], B[j-1])$.

## Correctitud

Para demostrar que el algoritmo funciona, usamos un **invariante del bucle**: en todo momento, el intervalo $[lo, hi]$ contiene al menos un índice $i$ que cumple las condiciones de frontera.

**Inicialización.** Antes de la primera iteración, $[lo, hi] = [0, n]$. Sabemos que la mediana real induce una partición válida: si mezclamos $A$ y $B$ en un solo arreglo ordenado $M$ de $2n$ elementos, los primeros $n$ elementos forman la mitad izquierda. Sea $a$ la cantidad de elementos de $A$ en esa mitad izquierda. Tomando $i = a$ y $j = n - a$, la partición corresponde exactamente a la mitad izquierda de $M$. Por definición de $M$, todos los elementos de la izquierda son $\le$ que los de la derecha, así que se cumplen $A[a-1] \le B[j]$ y $B[j-1] \le A[a]$. Por tanto, $i = a$ es válido y está en $[0, n]$. El invariante se cumple.

**Mantenimiento.** Supongamos que $[lo, hi]$ contiene un índice válido y veamos qué pasa en cada caso.

- *Si $A[mid-1] > B[j]$.* Afirmamos que ningún índice $k \ge mid$ puede ser válido. En efecto, para $k \ge mid$, como $A$ está ordenado, $A[k-1] \ge A[mid-1]$. Y como $B$ está ordenado y $n-k \le n-mid = j$, se tiene $B[n-k] \le B[j]$. Juntando las desigualdades: $A[k-1] \ge A[mid-1] > B[j] \ge B[n-k]$. Es decir, $A[k-1] > B[n-k]$, que es la negación de la primera condición de frontera. Así que todo $k \ge mid$ falla. El índice válido tiene que estar estrictamente a la izquierda de $mid$, o sea en $[lo, mid-1]$. El algoritmo asigna $hi = mid - 1$, y el invariante se mantiene.

- *Si $B[j-1] > A[mid]$.* Análogamente, ningún $k \le mid$ puede ser válido. Para $k \le mid$, $B[n-k-1] \ge B[n-mid-1] = B[j-1]$ (porque $n-k-1 \ge n-mid-1$ y $B$ está ordenado). Y $A[mid] \ge A[k]$ (porque $mid \ge k$). Juntando: $B[n-k-1] \ge B[j-1] > A[mid] \ge A[k]$. Es decir, $B[n-k-1] > A[k]$, la negación de la segunda condición. El índice válido está en $[mid+1, hi]$. El algoritmo asigna $lo = mid + 1$, y el invariante se mantiene.

- *Si no falla ninguna.* $mid$ cumple ambas condiciones, así que es válido y el algoritmo devuelve la respuesta. El invariante se cumple trivialmente porque ya terminó.

**Terminación.** En cada iteración, o bien el algoritmo devuelve un índice válido, o bien el intervalo $[lo, hi]$ se reduce estrictamente (a $[lo, mid-1]$ o a $[mid+1, hi]$). Como el intervalo es finito, eventualmente se alcanza un $mid$ válido. Además, por el invariante, el intervalo nunca se vacía sin encontrar un índice válido. El número de iteraciones es a lo sumo $\lceil \log_2(n+1) \rceil$.

**El valor devuelto es el correcto.** Falta ver que si $i$ es válido, entonces $\max(A[i-1], B[j-1])$ es el $n$-ésimo menor. Como $i$ es válido, se cumplen $A[i-1] \le B[j]$ y $B[j-1] \le A[i]$. Veamos que todo elemento de la izquierda $L(i)$ es $\le$ que todo elemento de la derecha $R(i)$:
- Dentro de $A$: $A[0..i-1] \le A[i..n-1]$ porque $A$ está ordenado.
- Dentro de $B$: $B[0..j-1] \le B[j..n-1]$ porque $B$ está ordenado.
- Cruce $A$ izquierda con $B$ derecha: $A[i-1] \le B[j]$, y como $A[0..i-1] \le A[i-1]$ y $B[j] \le B[j..n-1]$, se tiene $A[0..i-1] \le B[j..n-1]$.
- Cruce $B$ izquierda con $A$ derecha: $B[j-1] \le A[i]$, y como $B[0..j-1] \le B[j-1]$ y $A[i] \le A[i..n-1]$, se tiene $B[0..j-1] \le A[i..n-1]$.

Por tanto, $L(i)$ contiene exactamente los $n$ elementos más pequeños del total, y el mayor de $L(i)$ es el $n$-ésimo menor. Ese mayor es $\max(A[i-1], B[j-1])$ (con las convenciones de $-\infty$ si algún índice es negativo). Esto completa la demostración.

## Cota de información

El $n$-ésimo menor de $2n$ elementos puede ser cualquiera de los $2n$ elementos. Un árbol de decisión que distinga entre $2n$ posibles respuestas debe tener al menos $2n$ hojas, por lo que su altura es al menos $\lceil \log_2(2n) \rceil = \Omega(\log n)$. El algoritmo logra $O(\log n)$, así que es óptimo en el modelo de comparaciones.

**Conclusión.** El algoritmo es correcto y óptimo en el modelo de comparaciones.