## Problema

Dada una matriz cuadrada $M$ de dimensiones $n \times n$ cuyas filas y columnas se encuentran ordenadas de forma estrictamente creciente, diseñe un algoritmo que determine la existencia de un valor objetivo $x$ en un costo temporal de $\mathcal{O}(n)$ comparaciones.

1. Enuncie y demuestre la correctitud del algoritmo utilizando un invariante de ciclo.
2. Demuestre formalmente mediante el método del adversario que no es posible resolver el problema en un número de comparaciones de orden estrictamente menor a $n$ ($o(n)$).

---

## Solución

### 1. Algoritmo en $\mathcal{O}(n)$ Comparaciones

Para buscar $x$ de manera eficiente, aprovechamos la propiedad de monotonía bidimensional iniciando la exploración en la esquina superior derecha de la matriz (fila $\text{row} = 0$, columna $\text{col} = n - 1$):

1. Comparamos el valor actual $M[\text{row}][\text{col}]$ con el objetivo $x$:
* Si $M[\text{row}][\text{col}] == x$: El elemento ha sido encontrado; retornamos `True`.
* Si $M[\text{row}][\text{col}] > x$: Dado que las columnas están ordenadas crecientemente de arriba hacia abajo, todos los elementos situados debajo en esa misma columna son estrictamente mayores que $x$. Por consiguiente, $x$ no puede encontrarse en la columna actual. Descartamos toda la columna decrementando el índice: $\text{col} = \text{col} - 1$.
* Si $M[\text{row}][\text{col}] < x$: Dado que las filas están ordenadas crecientemente de izquierda a derecha, todos los elementos situados a la izquierda en esa misma fila son estrictamente menores que $x$. Por consiguiente, $x$ no puede encontrarse en la fila actual. Descartamos toda la fila incrementando el índice: $\text{row} = \text{row} + 1$.


2. Repetimos el proceso hasta hallar $x$ o hasta que los índices salgan de los límites válidos de la matriz.

#### Análisis de Costo Temporal

En cada iteración del ciclo, el algoritmo decrementa la columna o incrementa la fila. Como la columna puede decrecer como máximo $n$ veces y la fila puede incrementarse como máximo $n$ veces, el número máximo de iteraciones es $2n - 1$. Cada iteración realiza una única comparación, lo que garantiza una complejidad de $\mathcal{O}(n)$ comparaciones en el peor de los casos.

---

### 2. Demostración de Correctitud con un Invariante

#### Declaración del Invariante ($I$)

Si el elemento objetivo $x$ se encuentra contenido en la matriz $M$, entonces necesariamente pertenece a la submatriz rectangular activa delimitada por las filas desde $\text{row}$ hasta $n-1$ y las columnas desde $0$ hasta $\text{col}$.

Formalmente:


$$x \in M \implies x \in M[\text{row} \dots n-1][0 \dots \text{col}]$$

#### Demostración en Tres Fases

1. **Inicialización:**
Antes de la primera iteración, $\text{row} = 0$ y $\text{col} = n - 1$. La submatriz activa abarca la totalidad de la matriz $M[0 \dots n-1][0 \dots n-1]$. Si $x$ está presente en la matriz, trivialmente pertenece a este rango completo. El invariante se cumple inicialmente.
2. **Mantenimiento:**
Asumimos que el invariante es válido al inicio de una iteración arbitraria y evaluamos el elemento en $M[\text{row}][\text{col}]$:
* Caso $M[\text{row}][\text{col}] == x$: El algoritmo retorna `True` correctamente.
* Caso $M[\text{row}][\text{col}] > x$: Por el ordenamiento creciente vertical, todos los elementos situados debajo de la celda actual en la columna $\text{col}$ son estrictamente mayores que $x$. Por tanto, ningún elemento de esa columna dentro de la submatriz activa puede ser igual a $x$. Actualizar $\text{col} = \text{col} - 1$ descarta dicha columna entera sin omitir ningún candidato válido. Si $x$ existía en la matriz original, sigue estando confinado en la nueva submatriz activa. El invariante se preserva.
* Caso $M[\text{row}][\text{col}] < x$: Por el ordenamiento creciente horizontal, todos los elementos situados a la izquierda de la celda actual en la fila $\text{row}$ son estrictamente menores que $x$. Por tanto, ningún elemento de esa fila dentro de la submatriz activa puede ser igual a $x$. Actualizar $\text{row} = \text{row} + 1$ descarta dicha fila entera de manera segura. El invariante se preserva para el nuevo intervalo activo.


3. **Conclusión:**
El ciclo concluye cuando $\text{row} \geq n$ o $\text{col} < 0$, momento en el cual la submatriz activa se ha reducido a un conjunto vacío ($\emptyset$). Por el invariante, si $x$ estuviera en la matriz, debería pertenecer a un conjunto vacío, lo cual es lógicamente imposible. Por lo tanto, se concluye que $x \notin M$ y se retorna `False` correctamente.

---

### 3. Demostración de Cota Inferior con el Método del Adversario ($\Omega(n)$)

Queremos demostrar que ningún algoritmo basado en comparaciones entre los elementos de la matriz y el valor objetivo puede decidir si $x$ está en la matriz realizando menos de $n$ comparaciones en el peor de los casos.

#### Estrategia del Adversario

Construiremos una familia de matrices que cumplen las restricciones del problema y que son indistinguibles para cualquier algoritmo que no inspeccione determinadas posiciones.

1. **Construcción de la matriz negativa:**
Utilizamos índices desde $0$ hasta $n-1$ y fijamos $x = 2n-1$. Construimos una matriz $M_0$ definida por:

$$M_0[i][j] = \begin{cases} 2(i+j), & \text{si } i+j \neq n-1, \\ 2n-2, & \text{si } i+j = n-1. \end{cases}$$



Esta matriz está estrictamente ordenada por filas y columnas. En efecto, los valores aumentan estrictamente al avanzar horizontal o verticalmente, incluso al atravesar la diagonal secundaria. Además, ningún elemento es igual a $x$, por lo que la respuesta correcta para esta matriz es `False`.
2. **Construcción de las matrices positivas:**
Para cada índice $r$, con $0 \leq r < n$, construimos una matriz $M_r$ idéntica a $M_0$, excepto en la posición de la diagonal secundaria $(r, n-1-r)$, donde establecemos:

$$M_r[r][n-1-r] = 2n-1 = x$$



Todas estas matrices siguen estando estrictamente ordenadas por filas y columnas, puesto que el valor modificado continúa siendo estrictamente mayor que su vecino superior e izquierdo y estrictamente menor que su vecino inferior y derecho, cuando estos existen.
Cada matriz $M_r$ contiene exactamente una aparición de $x$, por lo que la respuesta correcta es `True`.
3. **Argumento de indistinguibilidad:**
Supongamos, por contradicción, que existe un algoritmo correcto que resuelve el problema utilizando menos de $n$ comparaciones en el peor caso.
Ejecutamos dicho algoritmo sobre $M_0$. Como existen $n$ posiciones en la diagonal secundaria y el algoritmo realiza menos de $n$ comparaciones, necesariamente habrá al menos una posición $(r, n-1-r)$ de dicha diagonal que no habrá sido consultada.
Consideremos ahora la matriz $M_r$. Esta matriz difiere de $M_0$ únicamente en la posición $(r, n-1-r)$ que no fue consultada. Por tanto, todas las comparaciones realizadas por el algoritmo producen exactamente los mismos resultados en ambas matrices.
4. **Contradicción:**
Como las ejecuciones son indistinguibles, el algoritmo debe producir la misma respuesta para ambas matrices. Sin embargo:
* Para $M_0$, la respuesta correcta es `False`.
* Para $M_r$, la respuesta correcta es `True`.


Por tanto, el algoritmo necesariamente se equivoca en al menos una de las dos entradas, contradiciendo la hipótesis de que es correcto.

#### Conclusión del Adversario

Para garantizar una respuesta correcta, el algoritmo debe inspeccionar las $n$ posiciones de la diagonal secundaria en el peor caso. Por consiguiente, cualquier algoritmo basado en comparaciones entre los elementos de la matriz y el objetivo requiere al menos $n$ comparaciones en el peor caso:


$$T(n) \in \Omega(n)$$

Como el algoritmo presentado en la primera sección realiza $\mathcal{O}(n)$ comparaciones, se concluye que la complejidad óptima del problema es:


$$\boxed{T(n) \in \Theta(n)}$$