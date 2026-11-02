
---
 **Resumen** Empieza en la esquina superior derecha y compara con $x$. Si la entrada es demasiado grande, descarta su columna. Si es demasiado pequeña, descarta su fila. Esto toma como máximo $2n-1$ comparaciones. Para la cota inferior, un adversario esconde $x$ en una de las $n$ celdas de la anti-diagonal, y cualquier algoritmo debe inspeccionarlas todas, así que se necesitan al menos $n$ comparaciones.

---

## 1. Enunciado formal


**Entrada:** un entero $n \ge 1$, una matriz $M$ de $n\times n$ (indexada desde $0$) con

$$
M_{i,j} < M_{i,j+1}
\quad\text{y}\quad
M_{i,j} < M_{i+1,j}
$$

siempre que ambos lados existan, y un valor $x$.

**Salida:** `True` si y solo si existen $i,j$ con $M_{i,j}=x$; en caso contrario, `False`.

**Modelo de costo:** una comparación es una prueba de tres vías de una entrada contra $x$ (menor, igual o mayor). El algoritmo de abajo también funciona si las filas y columnas son únicamente no decrecientes.

---

## 2. Algoritmo

```python
def search(M, n, x):
    i = 0
    j = n - 1
    while i < n and j >= 0:
        v = M[i][j]
        if v == x:
            return True
        if v > x:
            j = j - 1
        else:
            i = i + 1
    return False
```

---

## 3. Correctitud


Definimos la **región activa** $R(i,j)$ como las filas $i,\dots,n-1$ y las columnas $0,\dots,j$ de $M$.

**Invariante (I):** al comienzo de cada iteración, si $x$ aparece en $M$, entonces $x$ aparece en $R(i,j)$.

- **Inicialización.** $i=0$, $j=n-1$, así que $R$ es toda la matriz y (I) se cumple trivialmente.

- **Mantenimiento.** Supongamos que (I) se cumple y que la condición del bucle $i<n$ y $j\ge 0$ se cumple, así que $(i,j)$ está en $R$. Sea $v=M_{i,j}$.
  - Si $v=x$, devolvemos `True`, lo cual es correcto.
  - Si $v>x$: toda entrada $M_{k,j}$ con $k\ge i$ satisface

    $$
    M_{k,j} \ge v > x,
    $$

    porque las columnas están ordenadas. Así que $x$ no aparece en la parte de la columna $j$ dentro de $R$. Si $x$ aparece en $M$, aparece en $R(i,j-1)$, y (I) se cumple después de $j=j-1$.
  - Si $v<x$: toda entrada $M_{i,k}$ con $k\le j$ satisface

    $$
    M_{i,k} \le v < x,
    $$

    porque las filas están ordenadas. Así que $x$ no aparece en la parte de la fila $i$ dentro de $R$. Si $x$ aparece en $M$, aparece en $R(i+1,j)$, y (I) se cumple después de $i=i+1$.

- **Terminación (parada).** Sean

  $$
  r=n-i
  \quad\text{y}\quad
  c=j+1
  $$

  el número de filas y columnas de $R$. Cada iteración que no devuelve disminuye $r+c$ exactamente en $1$. El bucle se ejecuta solo mientras $r\ge 1$ y $c\ge 1$, y $r+c$ empieza en $2n$. Así que el bucle no puede ejecutarse indefinidamente y se ejecuta como máximo $2n-1$ veces: la última iteración comienza con $r+c\ge 2$ y deja $r+c\ge 1$.

- **Conclusión.** Si el bucle sale mediante `return True`, se encontró una entrada igual a $x$. En caso contrario, sale con $i=n$ o $j<0$, así que $R$ está vacía. Por (I), si $x$ apareciera en $M$, aparecería en la $R$ vacía, lo cual es imposible. Así que $x$ no está en $M$ y `False` es correcto. $\blacksquare$

---

## 4. Complejidad



Cada iteración realiza una comparación de tres vías, y hay como máximo $2n-1$ iteraciones. Así que el algoritmo usa como máximo

$$
2n-1 = O(n)
$$

comparaciones, y el tiempo total también es $O(n)$, ya que todo el demás trabajo por iteración es $O(1)$.

---

## 5. Cota inferior: $\Omega(n)$, mediante un adversario


Fijamos $x=0$ y la **matriz base**

$$
B_{i,j} = 2\bigl(i+j-(n-1)\bigr).
$$

- $B$ tiene filas y columnas estrictamente crecientes.
- $B_{i,j}=0$ exactamente en la **anti-diagonal**

  $$
  D=\{(i,n-1-i):0\le i<n\},
  $$

  que tiene $n$ celdas.
- Las celdas con $i+j<n-1$ tienen valores $\le -2$, y las celdas con $i+j>n-1$ tienen valores $\ge 2$.

**Hecho clave.** Reemplaza cualquier subconjunto de las celdas de $D$ por el valor $0$ o $1$ (la base ya tiene $0$ allí). La matriz sigue siendo válida. Cualquier vecino de una celda de $D$ está fuera de $D$ (su $i+j$ es $n$ o $n-2$), así que tiene $\pm 2$, y los valores $0$ y $1$ quedan ambos estrictamente entre los vecinos. Además, dos celdas de $D$ cualesquiera no comparten fila ni columna, así que dos celdas cambiadas cualesquiera no se restringen entre sí.

**Adversario.** Responde cada comparación como sigue:

- Para una celda fuera de $D$, responde según $B$ (la respuesta es “menor” o “mayor” que $x$, nunca “igual”).
- Para una celda de $D$, responde “mayor que $x$” (su valor es $1$).

**Argumento.** Supongamos que un algoritmo se detiene tras consultar menos de $n$ celdas de $D$. Entonces alguna celda $c$ de $D$ no ha sido consultada. Considera dos matrices:

- $M_1$: toda celda de $D$ tiene valor $1$. No contiene ningún $0$, así que $x$ está ausente.
- $M_2$: idéntica a $M_1$ excepto que $c$ tiene valor $0$. Es válida por el hecho clave y contiene $x$.

Ambas son consistentes con todas las respuestas que dio el adversario, así que el algoritmo ve la misma transcripción en ambas y produce la misma respuesta, que es incorrecta para una de ellas. Por lo tanto, todo algoritmo correcto debe consultar las $n$ celdas de $D$ en alguna entrada, así que usa al menos

$$
n
$$

comparaciones en el peor caso, lo cual es $\Omega(n)$ y, en particular, no es $o(n)$. $\blacksquare$

**Conclusión:** el peor caso está entre $n$ y $2n-1$ comparaciones, así que el algoritmo es óptimo salvo un factor constante, y $\Theta(n)$ es la cota ajustada.

