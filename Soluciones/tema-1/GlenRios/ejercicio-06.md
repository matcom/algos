# Problema 6 ★★

**Enunciado.** Una matriz $n \times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en $o(n)$.

## Solución formal

**Algoritmo.** Comenzar en la esquina superior derecha $(0, n-1)$. En cada paso, comparar $x$ con el elemento actual $A[i][j]$:

- Si $A[i][j] = x$, devolver verdadero.
- Si $A[i][j] > x$, entonces $x$ no puede estar en la columna $j$ (pues todos los elementos por debajo son mayores), así que decrementar $j$.
- Si $A[i][j] < x$, entonces $x$ no puede estar en la fila $i$ (pues todos los elementos a la izquierda son menores), así que incrementar $i$.

Si se sale de la matriz, devolver falso. Como $i$ solo aumenta y $j$ solo disminuye, el número total de pasos es a lo sumo $2n$, es decir, $O(n)$ comparaciones.

**Invariante.** En todo momento, si $x$ está en la matriz, entonces $x$ está en la submatriz $A[i..n-1][0..j]$. Es decir, se ha descartado el rectángulo superior derecho (filas $<i$ y columnas $>j$) y el inferior izquierdo (filas $>i$ y columnas $<j$). Más precisamente: $x$ no puede estar en las filas $0..i-1$ ni en las columnas $j+1..n-1$.

*Inicialización:* $i=0$, $j=n-1$. No se ha descartado nada, el invariante se cumple trivialmente.

*Mantenimiento:*
- Si $A[i][j] > x$, como las columnas son crecientes, todos los elementos en la columna $j$ desde la fila $i$ hacia abajo son $\ge A[i][j] > x$. Por tanto, $x$ no puede estar en la columna $j$ ni en ninguna columna a la derecha. Así, decrementamos $j$.
- Si $A[i][j] < x$, como las filas son crecientes, todos los elementos en la fila $i$ desde la columna $j$ hacia la izquierda son $\le A[i][j] < x$. Por tanto, $x$ no puede estar en la fila $i$ ni en ninguna fila por encima. Así, incrementamos $i$.

En ambos casos, el invariante se mantiene.

*Conclusión:* Si el algoritmo sale de la matriz ($i=n$ o $j<0$), entonces no hay ninguna celda posible para $x$, así que $x$ no está. Si encuentra $x$, devuelve verdadero.

**Cota mínima con adversario.** Demostramos que cualquier algoritmo que decida si $x$ está en una matriz $n \times n$ ordenada por filas y columnas necesita $\Omega(n)$ comparaciones en el peor caso.

Consideremos el siguiente adversario. El adversario mantiene un conjunto de celdas candidatas que forman una escalera desde la esquina superior derecha hasta la inferior izquierda. Inicialmente, todas las celdas son candidatas. Cuando el algoritmo compara $x$ con una celda $A[i][j]$, el adversario responde de modo que el número de candidatos se reduzca a lo sumo en 1. Por ejemplo, si la celda está en la frontera de la escalera, el adversario puede responder de forma que solo se elimine esa celda. Como la escalera inicial tiene $2n-1$ celdas, y cada comparación puede eliminar a lo sumo una celda, el algoritmo necesita al menos $n$ comparaciones para reducir la escalera a cero. Por tanto, $\Omega(n)$.

Más formalmente, el adversario puede construir una matriz en la que $x$ no está, y todas las comparaciones que el algoritmo haga den respuestas consistentes con una escalera de tamaño $n$. Como hay $n$ celdas que podrían ser $x$ (una por fila, por ejemplo), el algoritmo no puede distinguir si $x$ está en una de ellas sin mirarlas todas. Así, necesita $\Omega(n)$ comparaciones.

**Conclusión.** El algoritmo es óptimo en el modelo de comparaciones.
