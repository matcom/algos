# DP

## Subsecuencia Buena

Supongamos que tienes un array binario $B$ de longitud $N$. Una secuencia $x_1, x_2, \dots, x_k$ se llama buena con respecto a $B$ si satisface las siguientes condiciones:

- $1 \leq x_1 < x_2 < \dots < x_k \leq N + 1$
- Para cada par $(i, j)$ tal que $1 \leq i < j \leq k$, el subarray $B[x_i : x_j - 1]$ contiene $(j - i)$ unos más que ceros. Es decir, si $B[x_i : x_j - 1]$ contiene $c_1$ unos y $c_0$ ceros, entonces se debe cumplir que $c_1 - c_0 = j - i$.

Aquí, $B[L : R]$ denota el subarray que consiste en los elementos $[B_L, B_{L + 1}, B_{L + 2}, \dots, B_R]$. Nota que, en particular, una secuencia de tamaño $1$ siempre es buena.

Por ejemplo, supongamos que $B = [0, 1, 1, 0, 1, 1]$. Entonces:

- La secuencia $[1, 4, 7]$ es una secuencia buena. Los subarrays que necesitan ser revisados son $B[1 : 3]$, $B[1 : 6]$ y $B[4 : 6]$, que todos cumplen con la condición.
- La secuencia $[1, 5]$ no es buena, porque $B[1 : 4] = [0, 1, 1, 0]$ contiene un número igual de ceros y unos (cuando debería contener un $1$ extra).

Alice le dio a Bob un array binario $A$ de tamaño $N$ y le pidió que encontrara la secuencia más larga que sea buena con respecto a $A$. Ayuda a Bob a encontrar una de estas secuencias.

Si existen múltiples secuencias más largas posibles, puedes imprimir cualquiera de ellas.

### Statement

Dado un arreglo binario $A$, encuentra la secuencia buena más larga $x_1, x_2, \dots, x_k$ tal que satisface:

$1 \leq x_1 < x_2 < \dots < x_k \leq N + 1$

$A[x_i : x_j - 1]$ contiene un número igual de ceros y unos para cada $i < j$.

### Solution

Primero, note que es suficiente asegurar que $A[x_i : x_{i+1} - 1]$ (es decir, el subarreglo entre elementos consecutivos) satisfaga la condición, es decir, contiene un uno extra.

Prueba
Esto no es difícil de ver. El subarreglo $A[x_i : x_j - 1]$ se puede pensar como la concatenación de $A[x_i : x_{i+1} - 1], A[x_{i+1} : x_{i+2} - 1], \dots, A[x_{j-1}, x_j - 1]$. Note que hay $j - i$ subarreglos de este tipo.

Si cada uno de estos contiene un uno extra, por supuesto, todos juntos tendrán exactamente $j - i$ unos extra.

Ahora, usemos un pequeño truco: reemplace cada $0$ en el arreglo con $-1$. Llamemos al arreglo obtenido de esta manera $B$. Por ejemplo, si $A = [0, 1, 1, 0, 1]$, entonces $B = [-1, 1, 1, -1, 1]$.

Observe que "A[L:R] contiene un uno extra" se traduce a "B[L:R] tiene una suma de $1$" en el nuevo arreglo, lo cual es mucho más fácil de manejar.

Dado que estamos tratando con sumas de subarreglos, es natural pensar en sumas prefixadas. Entonces, sea $P_i = B_1 + B_2 + \dots + B_i$ (con $P_0 = 0$) denotando el arreglo de sumas prefixadas de $B$.

Ahora, para que $B[L:R]$ tenga una suma de $1$, debemos tener $P_R - P_{L-1} = 1$, o $P_R = P_{L-1} + 1$.

Aplicando esto a la definición de una secuencia buena, vemos que debemos tener $P_{x_{i+1} - 1} = P_{x_i - 1} + 1$ para cada $1 \leq i < k$. En otras palabras, necesitamos elegir una secuencia de índices cuyas sumas prefixadas sean $k, k + 1, k + 2, \dots$ para algún valor de $k$.

La secuencia buena más larga, por lo tanto, corresponde a la secuencia más larga de sumas prefixadas de esta forma.

Esto se puede calcular usando programación dinámica.

Sea $dp_i$ la longitud de la secuencia más larga de sumas prefixadas que termina en la posición $i$ y que satisface la condición anterior. Las transiciones para un índice dado son fáciles de calcular en $O(N)$. Simplemente tenemos $dp_i = 1 + \max(dp_j)$ en todos los $j < i$ tales que $P_j + 1 = P_i$.

Sin embargo, hacer esta computación $O(N)$ para cada índice es demasiado lento, necesitamos acelerarlo un poco. Esto se puede hacer observando que solo nos importan aquellos índices cuyos valores $P_j$ sean iguales a $P_i - 1$; de hecho, solo nos importa el valor máximo de $dp_j$ entre estos índices.

Así que, mantengamos otro arreglo $mx$, donde $mx[x]$ es el valor más grande de $dp_i$ en todos los índices $i$ tales que $P_i = x$. Inicialmente, lo inicializamos a todos ceros.

Luego, para cada $i$ desde $0$ hasta $N$,

$dp_i = 1 + mx[P_i]$

$mx[P_i] = \max(dp_i, mx[P_i])$

El elemento máximo de $dp$ es la respuesta final.

Reconstituir una secuencia válida no es difícil, cuando se realiza el $dp$, se mantiene un enlace al elemento anterior en la secuencia, luego se siguen estos en reversa al final.

COMPLEJIDAD TEMPORAL:

$O(N)$ por caso de prueba.
