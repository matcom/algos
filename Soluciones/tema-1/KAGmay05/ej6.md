## Problema 6

Una matriz $M$ de $n \times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en $o(n)$.

### Respuesta

Que las filas y las columnas estén ordenadas significa que, para todo $i, j$:

$$M[i][j] \le M[i][j+1] \qquad \text{y} \qquad M[i][j] \le M[i+1][j]$$

Es decir, los valores crecen hacia la derecha y hacia abajo.

#### Algoritmo 

Se empieza en la esquina superior derecha, $M[0][n-1]$. Esa casilla es la mayor de su fila y la menor de su columna, así que al compararla con $x$ siempre se puede descartar una fila o una columna completa:

- Si $M[i][j] > x$: todo lo que está debajo en la columna $j$ es todavía mayor, así que se descarta la columna $j$ y se avanza a la izquierda.
- Si $M[i][j] < x$: todo lo que está a la izquierda en la fila $i$ es todavía menor, así que se descarta la fila $i$ y se baja.

```python
def buscar(M, x):
    n = len(M)
    i, j = 0, n - 1          
    while i < n and j >= 0:
        if M[i][j] == x:
            return True
        elif M[i][j] > x:
            j -= 1           
        else:
            i += 1           
    return False
```


### Invariante: 

Al inicio de cada vuelta, si $x$ está en $M$, entonces está en la submatriz $M[i..n-1][0..j]$ (las filas de $i$ hacia abajo y las columnas de $j$ hacia la izquierda).



- Inicio: $i = 0$ y $j = n-1$, así que la submatriz es toda $M$. 
- Mantenimiento: supongamos que se cumple y que $M[i][j] \ne x$.
  - Si $M[i][j] > x$: como la columna $j$ es creciente, para todo $k \ge i$ se tiene $M[k][j] \ge M[i][j] > x$. Ninguna casilla de la columna $j$ dentro de la submatriz es $x$, así que $x$ (si está) está en $M[i..n-1][0..j-1]$. Después de j -= 1 el invariante se cumple.
  - Si $M[i][j] < x$: como la fila $i$ es creciente, para todo $l \le j$ se tiene $M[i][l] \le M[i][j] < x$. Ninguna casilla de la fila $i$ dentro de la submatriz es $x$, así que $x$ (si está) está en $M[i+1..n-1][0..j]$. Después de i += 1 el invariante se cumple.
- Terminación: el ciclo acaba de una de dos formas:
  - Encuentra $M[i][j] = x$ y devuelve True, que es correcto.
  - Sale porque $i = n$ o $j = -1$. En ese caso la submatriz $M[i..n-1][0..j]$ está vacía y, por el invariante, $x$ no está en $M$. Devolver False es correcto.

#### Potencial y número de comparaciones

El potencial es el número de filas más el número de columnas que le quedan a la submatriz.

- Al principio vale 2n.
- Dentro del ciclo $i \le n-1$ y $j \ge 0$, así que el potencial es mayor igual que 2.
- Cada vuelta que no encuentra $x$ hace i += 1 o j -= 1, así que el potencial baja exactamente en $1$.

Al inicio de cada vuelta el potencial toma un valor distinto de $2n, 2n-1, \dots, 2$, por lo que el ciclo da como mucho $2n - 1$ vueltas, o sea que termina el algoritmo. En cada vuelta se compara $x$ con una sola casilla, con resultado $<$, $=$ o $>$, así que el algoritmo hace como mucho $2n - 1$ comparaciones: $O(n)$.

#### Cota inferior por adversario

Modelo: el algoritmo solo obtiene información de $M$ comparando $x$ con alguna casilla $M[i][j]$, y la respuesta es $<$, $=$ o $>$. En el peor caso, cualquier algoritmo correcto necesita al menos $n$ comparaciones, así que no puede existir uno con $o(n)$.

Nos fijamos en la antidiagonal: las $n$ casillas con $i + j = n - 1$, o sea $M[0][n-1], M[1][n-2], \dots, M[n-1][0]$.

El adversario no fija la matriz de antemano, sino que contesta cada comparación así:

$$x \text{ vs } M[i][j] \;\longrightarrow\; \begin{cases} M[i][j] < x & \text{si } i + j \le n-1 \\ M[i][j] > x & \text{si } i + j \ge n \end{cases}$$

Nunca contesta "$=$".

Las respuestas son consistentes con una matriz que no contiene $x$:

$$M^-[i][j] = x + 2(i + j) - 2n + 1$$

Cada paso a la derecha o hacia abajo suma $2$, así que $M^-$ tiene filas y columnas (estrictamente) crecientes. Si $i + j \le n-1$, entonces $M^-[i][j] \le x - 1 < x$; si $i + j \ge n$, entonces $M^-[i][j] \ge x + 1 > x$. Así que $M^-$ da exactamente las respuestas del adversario, y no contiene $x$ porque todos sus valores difieren de $x$ en un número impar.

Ejemplo con $n = 4$ y $x = 0$:

|            | col 0  | col 1  | col 2  | col 3  |
|------------|--------|--------|--------|--------|
| fila 0 | −7     | −5     | −3     | −1 |
| fila 1 | −5     | −3     | −1 | 1      |
| fila 2 | −3     | −1 | 1      | 3      |
| fila 3 | −1 | 1      | 3      | 5      |

Y también con una que sí lo contiene. Supongamos que el algoritmo termina sin haber comparado $x$ con alguna casilla de la antidiagonal, digamos $(k,\, n-1-k)$. Sea $M^+$ igual a $M^-$ salvo en esa casilla, donde ponemos $M^+[k][n-1-k] = x$.

- $M^+$ sigue ordenada: en $M^-$ esa casilla valía $x - 1$. Sus vecinas de arriba y de la izquierda están en $i + j = n-2$ y valen $x - 3 < x$; sus vecinas de abajo y de la derecha están en $i + j = n$ y valen $x + 1 > x$.
- $M^+$ da las mismas respuestas que $M^-$ en todas las casillas comparadas, porque solo difieren en una casilla que nunca se comparó.

El algoritmo ve exactamente las mismas respuestas con $M^-$ que con $M^+$, así que da la misma salida en las dos. Pero en $M^-$ la respuesta correcta es "no está" y en $M^+$ es "sí está": se equivoca en una de ellas.

Contra este adversario, todo algoritmo correcto tiene que comparar $x$ con las $n$ casillas de la antidiagonal, así que hace al menos $n$ comparaciones en el peor caso. Si un algoritmo usara $f(n) = o(n)$ comparaciones, para $n$ suficientemente grande tendríamos $f(n) < n$ y quedaría alguna casilla de la antidiagonal sin comparar, lo cual es una contradicción. Por lo tanto el problema necesita $\Omega(n)$ comparaciones y la búsqueda en escalera es asintóticamente óptima.

El mismo adversario obliga también a comparar las $n - 1$ casillas con $i + j = n$: en $M^-$ valen $x + 1$, sus vecinas de arriba y de la izquierda valen $x - 1$ y las de abajo y de la derecha valen $x + 3$, así que cualquiera de ellas se puede cambiar por $x$ sin romper el orden. Eso da al menos $n + (n-1) = 2n - 1$ comparaciones, que es exactamente lo que hace el algoritmo en el peor caso: la búsqueda en escalera es óptima incluso en la constante.

Si además se permitiera comparar dos casillas entre sí, el adversario contesta según $M^-$. Cambiar una casilla que no participó en ninguna comparación no altera ninguna respuesta, y cada comparación toca como mucho dos casillas, así que harían falta al menos $n/2$ comparaciones. Sigue siendo $\Omega(n)$.
