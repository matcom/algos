## 2.  Búsqueda binaria: invariante, potencial y cota de información (C3, C5)

```python
def busqueda_binaria(A, x):          # precondición: A ordenado crecientemente
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if x == A[m]:  return ("está", m)
        if x <  A[m]:  hi = m
        else:          lo = m + 1
    return ("hueco", lo)
```

**Invariante** (versión reforzada, que además justifica la salida "hueco"):
$$I:\quad A[j] < x \text{ para todo } j < lo, \qquad A[j] > x \text{ para todo } j \ge hi.$$
En particular, si $x$ está en $A$, está en $A[lo:hi]$.

- *Inicialización.* $lo = 0$, $hi = n$: las dos afirmaciones son vacías.
- *Mantenimiento.* Si $x < A[m]$, como $A$ está ordenado, $A[j] \ge A[m] > x$ para todo $j \ge m$, y la asignación $hi = m$ conserva la segunda parte. Si $x > A[m]$, simétricamente $A[j] \le A[m] < x$ para $j \le m$, y $lo = m+1$ conserva la primera. Si $x = A[m]$ se devuelve $m$, que es correcto.
- *Conclusión.* Si el ciclo termina sin devolver, $lo = hi$, y por $I$ todo elemento a la izquierda de $lo$ es menor que $x$ y todo elemento desde $lo$ es mayor: $x$ no está y cae en el hueco $lo$.

**Potencial.** $\Phi = hi - lo$, entero y $\ge 0$ dentro del ciclo. Con $s = hi - lo$ y $m = lo + \lfloor s/2\rfloor$, el intervalo nuevo tiene tamaño $\lfloor s/2 \rfloor$ (si $hi=m$) o $s - \lfloor s/2\rfloor - 1 \le \lfloor s/2\rfloor$ (si $lo = m+1$). Así que $\Phi$ baja estrictamente (termina) y además se parte al menos a la mitad: después de $k$ vueltas, $\Phi \le \lfloor n/2^k \rfloor$. El ciclo da a lo sumo $\lfloor \log n\rfloor + 1 = \lceil \log(n+1)\rceil$ vueltas, una comparación (de tres salidas) cada una.

**Cota de información (C5 §3, lema 4).** Si $x$ no está, cae en uno de los $n+1$ huecos; dos valores en huecos distintos tienen que llegar a hojas distintas, y en esas ramas ninguna comparación responde "$=$", así que esa parte del árbol es binaria. Por el lema 1, cualquier algoritmo de comparaciones hace al menos $\lceil \log(n+1)\rceil$ comparaciones en el peor caso. La búsqueda binaria hace exactamente eso: es óptima, sin constante de diferencia.

---