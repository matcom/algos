## Problema 2

Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

### Respuesta

En el algoritmo de búsqueda binaria:
```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if A[mid] == x:
            return mid
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

- Invariante: si $x$ está en $A$, entonces está en entre $A[lo]$ y  $A[hi]$.

- Potencial: La cantidad de posiciones que quedan por revisar. Es un entero $\ge 0$, y en cada vuelta que no encuentra $x$ pasa de $m$ a como mucho $\lfloor m/2 \rfloor$: se descarta $A[mid]$ y una de las dos mitades. Empieza valiendo $n$, así que después de $k$ vueltas $\Phi \le n/2^k$, y el ciclo da como mucho $\lfloor \log_2 n \rfloor + 1$ vueltas. Es decir, $O(\log n)$ comparaciones.

- Cota de información: cualquier algoritmo que busque comparando $x$ con elementos de $A$ se puede ver como un árbol de decisión. Cada nodo es una comparación de $x$ con algún $A[i]$: si sale $<$ se baja a la izquierda, si sale $>$ a la derecha, y si sale $=$ se termina. Las comparaciones en el peor caso son la altura $h$ del árbol.

  Para poder responder en qué posición está, el algoritmo tuvo que comparar $x$ con $A[i]$, así que el árbol necesita al menos $n$ nodos, uno por posición. Un árbol binario de altura $h$ tiene como mucho $2^h - 1$ nodos, por lo tanto:

  $$2^h - 1 \ge n \;\Rightarrow\; h \ge \lceil \log_2 (n+1) \rceil$$

  Hay $n+1$ respuestas posibles (las posiciones $0, \dots, n-1$ o "no está"), y cada comparación aporta como mucho 1 bit, así que hacen falta al menos $\log_2(n+1)$ comparaciones.

  Por el potencial, la búsqueda binaria hace en el peor caso $\lfloor \log_2 n \rfloor + 1 = \lceil \log_2 (n+1) \rceil$ comparaciones, que es exactamente la cota. Por eso es óptima: ningún algoritmo basado en comparaciones puede usar menos en el peor caso.
