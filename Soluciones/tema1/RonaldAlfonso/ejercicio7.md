## 7.  Mediana de dos arreglos ordenados en $O(\log n)$ (C2, C3, C5)

**Problema (C2 §2: precisar).** $A$ y $B$ ordenados (no decrecientes), de largo $n \ge 1$. Devolver el $n$-ésimo menor de los $2n$ elementos (la mediana inferior), contando repetidos. Con empates basta devolver el valor.

**Idea.** El $n$-ésimo menor es el máximo de algún conjunto formado por los primeros $i$ de $A$ y los primeros $n-i$ de $B$. Hay que encontrar el $i$ correcto, y eso es una búsqueda binaria sobre $i \in \{0, \dots, n\}$. Usamos centinelas $A[-1] = B[-1] = -\infty$ y $A[n] = B[n] = +\infty$.

Definimos el predicado
$$P(i):\quad A[i] \ge B[n-i-1].$$

```python
def mediana(A, B):
    n = len(A)
    lo, hi = 0, n                         # invariante: i* está en [lo, hi]
    while lo < hi:
        m = (lo + hi) // 2                # m < n, así que A[m] y B[n-m-1] existen
        if A[m] >= B[n - m - 1]: hi = m   # P(m)
        else:                    lo = m + 1
    i = lo
    candidatos = ([A[i - 1]] if i > 0 else []) + ([B[n - i - 1]] if i < n else [])
    return max(candidatos)
```

**Correctitud.**

*Lema 1 (monotonía).* Si $P(i)$ vale y $j > i$, vale $P(j)$: $A[j] \ge A[i] \ge B[n-i-1] \ge B[n-j-1]$. Y $P(n)$ vale por el centinela. Así que $P$ es "falso…falso verdadero…verdadero" y existe $i^* = \min\{i : P(i)\}$.

*Lema 2 (búsqueda).* La búsqueda binaria mantiene el invariante "$i^* \in [lo, hi]$": si $P(m)$, por el lema 1 $i^* \le m$; si no, $i^* > m$. Potencial $hi - lo$, que se parte a la mitad como en el ejercicio 2. Al terminar, $lo = i^*$.

*Lema 3 (el corte es correcto).* Sea $L = A[0..i^*-1] \cup B[0..n-i^*-1]$, que tiene $n$ elementos. Todo elemento fuera de $L$ es $\ge$ todo elemento de $L$:

- los de $A$ fuera de $L$ son $\ge A[i^*] \ge B[n - i^* - 1]$ (por $P(i^*)$), que es el mayor de los de $B$ en $L$; y $\ge A[i^*-1]$ por el orden de $A$;
- los de $B$ fuera de $L$ son $\ge B[n-i^*] > A[i^*-1]$ (porque $P(i^*-1)$ es falso, si $i^* > 0$), que es el mayor de los de $A$ en $L$; y $\ge B[n - i^* - 1]$ por el orden de $B$.

Entonces $L$ es un conjunto de los $n$ menores, y el $n$-ésimo menor es $\max(L) = \max(A[i^*-1], B[n-i^*-1])$. Los empates no rompen nada porque todas las desigualdades son $\le$. $\square$

**Costo.** $\lceil \log(n+1) \rceil$ comparaciones en la búsqueda más 1 para el máximo: $O(\log n)$ tiempo, $O(1)$ memoria. La mezcla ingenua hasta la posición $n$ cuesta $\Theta(n)$.

**Cota de información.** Con elementos distintos, la respuesta puede estar en cualquiera de las $2n$ posiciones: $A[k]$ es el $n$-ésimo menor si exactamente $k$ elementos de $A$ y $n-1-k$ de $B$ están por debajo, y eso se puede arreglar para cada $k \in \{0,\dots,n-1\}$; igual para $B[k]$. Como la salida de un algoritmo de comparaciones depende solo de la hoja (C5 §3, lema 2), esas $2n$ entradas van a hojas distintas, y con elementos distintos ninguna comparación responde "$=$": el árbol es binario. Por el lema 1 de C5:
$$\text{peor caso} \ \ge\ \lceil \log(2n) \rceil = \lceil \log n \rceil + 1.$$
El algoritmo usa $\lceil \log (n+1)\rceil + 1$, que coincide con la cota salvo cuando $n$ es potencia de 2, donde sobra una comparación. El algoritmo es óptimo hasta una comparación aditiva.

---