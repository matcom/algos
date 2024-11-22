# DP

## MEX Subsecuencia

Daniel tiene un array
$a_1, a_2, \dots, a_N$. Necesita encontrar el número de formas de dividir el array en subarrays contiguos tal que:

- Cada elemento de la secuencia $a$ pertenezca exactamente a uno de los subarrays.
- Existe un número entero $m$ tal que el MEX de cada subarray sea igual a $m$. El MEX de una secuencia es el menor número entero no negativo que no aparece en dicha secuencia.

Ayuda a Daniel con esta tarea.

### Statement

Te dan un arreglo de $N$ enteros como $A_1, A_2, A_3, \dots, A_N$. Tu tarea es encontrar el número de formas de dividir el arreglo en subarreglos contiguos tales que:

1. Cada elemento del arreglo dado $A$ pertenezca exactamente a uno de los subarreglos.
2. Existe un entero $m$, tal que el $MEX$ de cada subarreglo es igual a $m$.

El $MEX$ de una secuencia es el menor entero no negativo que no aparece en la secuencia.

### Solution

EXPLICACIÓN RÁPIDA:
Podemos notar que el MEX($m$) es siempre único a lo largo de todo el proceso y es igual al MEX del array dado.

Cualquier subarray de este array es válido solamente cuando el MEX de ese subarray es igual al MEX del array dado.

Podemos usar un enfoque de programación dinámica para encontrar el número de formas de dividir el array en subarrays contiguos de manera que el MEX de cada subarray sea $m$.

El estado de DP se representa como $(x)$, representando el número de formas de dividir un array de longitud $x$, tal que el MEX de cada subarray sea $m$.

El estado de DP se calcula en orden de $1$ a $N$, y el número de formas se calcula en consecuencia.

Finalmente, se debe imprimir el número de formas para la secuencia de longitud $N$.

EXPLICACIÓN:
Se nos da un array de $N$ enteros como $A_1, A_2, A_3, \dots, A_N$. Nuestra tarea es encontrar el número de formas de dividir el array en subarrays contiguos de manera que el MEX de cada subarray sea el mismo, es decir, $m$.

La primera observación que podemos hacer es que el MEX es siempre único a lo largo de todo el proceso y es igual al MEX del array dado.

Prueba:
Ahora, pasemos a la programación dinámica.

Definamos nuestro DP como $(y)$, que se define de la siguiente manera:

DP$(y)$ se define como el número de formas de dividir un array de longitud $y$ en subarrays contiguos de manera que el MEX de cada subarray sea el mismo y sea igual a $m$. Ahora nuestro objetivo es encontrar los subarrays cuyo MEX sea igual a $m$, lo cual se puede hacer encontrando subarrays donde estén presentes todos los enteros menores que $m$.

Establecemos, $DP[0] = 1$.

Ahora, encontraremos el subarray de longitud mínima tal que este subarray contenga todos los enteros menores que $m$. Por lo tanto, el MEX de este subarray es $m$. Supongamos que tenemos dicho subarray, llamado $S$.

$A_1, A_2, \dots, A_x, A_{x+1}, A_{x+2}, \dots, A_y$

$S = [A_{x+1}, A_{x+2}, \dots, A_y]$

Aquí, $S$ es el subarray cuyo MEX es igual a $m$. Esto significa que si dividimos el array antes de $x$, entonces el MEX seguirá siendo $m$. Por lo tanto, podemos dividir el array de la siguiente manera:

$[A_1][A_2, A_3, \dots, A_y]$

$[A_1, A_2][A_3, \dots, A_Y]$

$\dots$

$[A_1, A_2, \dots, A_x][A_{x+1}, A_{x+2}, \dots, A_y]$

Dado que estamos seguros de que el último subarray tendrá un MEX igual a $m$, y ya hemos calculado el número de formas de dividir un array de longitud menor a $x$ tal que el MEX sea $m$, la expresión matemática para el DP será:

$DP[y] = \sum_{i=0}^{x} DP[i]$

Donde $DP[i]$ se define como el número de formas de dividir un array de longitud $i$ tal que el MEX sea $m$.

Podemos usar la suma de prefijos para precomputar la suma de todos los $DP[i]$ para longitudes menores a $x$, cuando llegamos a la longitud $x$ del array dado.

Nuestra respuesta será el número de formas de dividir un array de longitud $N$ en subarrays contiguos tal que el MEX de cada subarray sea $m$. Esto estará representado por $DP[N]$.

COMPLEJIDAD TEMPORAL:
$O(N)$ por caso de prueba.

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

### Statement 2

Dado un arreglo binario $A$, encuentra la secuencia buena más larga $x_1, x_2, \dots, x_k$ tal que satisface:

$1 \leq x_1 < x_2 < \dots < x_k \leq N + 1$

$A[x_i : x_j - 1]$ contiene un número igual de ceros y unos para cada $i < j$.

### Solution 2

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
