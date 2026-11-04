## 6.  Buscar $x$ en una matriz con filas y columnas ordenadas (C3, C5)

**Algoritmo** (búsqueda "en escalera", desde la esquina superior derecha):

```python
def buscar_matriz(M, x):
    n = len(M)
    i, j = 0, n - 1
    while i < n and j >= 0:
        if M[i][j] == x: return True
        if M[i][j] > x:  j -= 1          # la columna j ya no sirve
        else:            i += 1          # la fila i ya no sirve
    return False
```

**Invariante.** Si $x$ está en $M$, está en la submatriz $M[i..n-1][0..j]$.

- *Inicialización:* $i = 0$, $j = n-1$ es la matriz entera.
- *Mantenimiento.* Si $M[i][j] > x$: la columna $j$ está ordenada, así que $M[r][j] \ge M[i][j] > x$ para todo $r \ge i$; las filas $< i$ ya estaban descartadas; la columna $j$ entera queda descartada y $j$ baja. Si $M[i][j] < x$: la fila $i$ está ordenada, así que $M[i][c] \le M[i][j] < x$ para todo $c \le j$; las columnas $> j$ ya estaban descartadas; la fila $i$ queda descartada e $i$ sube. Si es igual, se devuelve `True`, que es correcto.
- *Conclusión.* Al salir, $i = n$ o $j < 0$: la submatriz es vacía, y por el invariante $x$ no está.

**Potencial.** $\Phi = (n - i) + (j + 1)$. Empieza en $2n$, baja exactamente 1 por vuelta, y el ciclo exige que los dos sumandos sean positivos, así que hay a lo sumo $2n - 1$ vueltas. **A lo sumo $2n - 1$ comparaciones: $O(n)$.**

**Cota mínima por adversario: no se puede en $o(n)$.** Tomamos la matriz
$$M[i][j] = 2(i+j) \quad \text{si } i + j \ne n-1, \qquad x = 2n - 2,$$
y dejamos libres las $n$ celdas de la antidiagonal $i + j = n - 1$. Los vecinos de arriba y de la izquierda de una celda antidiagonal valen $2n-4$, y los de abajo y la derecha valen $2n$. Así que **cada celda antidiagonal puede valer, de forma independiente, $2n-3$, $2n-2 = x$ o $2n-1$**, y la matriz sigue teniendo filas y columnas estrictamente crecientes. Ninguna celda fuera de la antidiagonal vale $x$.

*Modelo 1, comparaciones de $x$ con entradas (el del algoritmo).* El adversario contesta con los valores fijos fuera de la antidiagonal, y a cada celda antidiagonal le contesta "$<$" (vale $2n-3$). Si el algoritmo termina sin haber comparado alguna celda antidiagonal $c$, las dos matrices "$c = 2n-3$" (no contiene $x$) y "$c = x$" (contiene $x$) son consistentes con todas las respuestas y tienen respuestas correctas distintas: el algoritmo se equivoca en una. **Hacen falta al menos $n$ comparaciones.**

*Modelo 2, comparaciones arbitrarias entre entradas y $x$.* El adversario fija una celda antidiagonal solo cuando se compara: contra $x$, la fija en $2n-3$ y contesta "$<$"; dos celdas antidiagonales libres entre sí, fija una en $2n-3$ y la otra en $2n-1$; contra una celda de fuera, contesta sin fijar nada (sus valores son $\le 2n-4$ o $\ge 2n$, fuera del intervalo libre $(2n-4, 2n)$). Cada comparación fija a lo sumo dos celdas, y una celda sin fijar al final deja el mismo dilema. **Al menos $n/2$ comparaciones.**

En los dos modelos es $\Omega(n)$, y con $2n - 1$ del algoritmo el problema cuesta $\Theta(n)$.
