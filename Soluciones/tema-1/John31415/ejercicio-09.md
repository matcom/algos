## Problema

Dada una variante "optimizada" del algoritmo clásico de mezcla (*merge*) de dos listas ordenadas de longitud $n$, la cual se detiene anticipadamente y deja de realizar comparaciones en el momento exacto en que a la primera lista le resta un único elemento, colocándolo directamente al final de la mezcla:

1. Determine el número de comparaciones realizadas en el peor caso.
2. Decida formalmente su correctitud apoyándose en los resultados teóricos de cota inferior para la mezcla de listas.
3. Construya explícitamente una entrada de contraejemplo mediante el método del adversario para demostrar el fallo del algoritmo.

---

## Solución

### 1. Cantidad de Comparaciones en el Peor Caso

En el algoritmo estándar de mezcla de dos listas ordenadas de tamaño $n$, cada comparación entre las cabezas de ambas listas permite ubicar un elemento en su posición definitiva, requiriendo un total de $2n - 1$ comparaciones en el peor caso (cuando la última comparación ocurre al restar un único elemento en cada lista).

En la variante propuesta, el proceso de comparación se interrumpe prematuramente tan pronto como a la primera lista $A$ le queda un único elemento ($a_n$), pasando a vaciar el resto de la segunda lista $B$ sin comparaciones y añadiendo $a_n$ al final.

Para maximizar el número de comparaciones antes de activar esta condición de parada:

* Se deben consumir mediante comparaciones los primeros $n-1$ elementos de la primera lista $A$.
* Durante dicho proceso también se deben consumir mediante comparaciones tantos elementos de la segunda lista $B$ como sea posible, sin que esta se agote antes de activar la condición de parada.
* Como máximo pueden consumirse $n-1$ elementos de $B$, por lo que el máximo se alcanza cuando se consumen $n-1$ elementos de cada lista antes de que a $A$ le quede un único elemento.

Por consiguiente, el número máximo de comparaciones ejecutadas en el peor caso es:


$$\text{Comparaciones} = (n - 1) + (n - 1) = 2n - 2$$

Este peor caso se alcanza, por ejemplo, cuando el orden de los primeros $2n - 2$ elementos de la mezcla es:


$$b_1 < a_1 < b_2 < a_2 < \dots < b_{n-1} < a_{n-1}$$

De esta manera, se consumen $n-1$ elementos de cada lista y se activa la condición de parada. Los dos elementos restantes se incorporan sin comparación.

---

### 2. Análisis de Correctitud (Basado en Cota Inferior)

El algoritmo no es correcto para todas las instancias posibles.

#### Justificación Teórica

De acuerdo con los resultados teóricos de cota inferior para la mezcla de listas ordenadas, cualquier algoritmo basado en comparaciones que mezcle correctamente dos listas ordenadas de longitud $n$ requiere al menos $2n - 1$ comparaciones en el peor caso.

Esta cota se puede justificar considerando una instancia cuya mezcla ordenada intercale completamente los elementos de ambas listas:


$$a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n$$

En esta disposición existen exactamente $2n - 1$ pares de elementos consecutivos que pertenecen a listas diferentes.

Un algoritmo correcto debe determinar el orden relativo de cada uno de estos pares. Ninguno puede inferirse mediante transitividad a partir de comparaciones con otros elementos, porque no existe ningún elemento intermedio entre sus integrantes. Si alguno de estos pares no se compara directamente, el adversario puede invertir su orden relativo sin alterar el orden interno de ninguna de las dos listas ni los resultados de las demás comparaciones.

Por tanto, cualquier algoritmo correcto necesita realizar al menos:


$$2n - 1$$


comparaciones en el peor caso.

La variante propuesta ejecuta como máximo $2n - 2$ comparaciones, por lo que no alcanza la cota inferior necesaria para garantizar una mezcla correcta en todas las entradas. Esto demuestra que el algoritmo es incorrecto.

---

### 3. Construcción de la Entrada Fallida mediante el Adversario

Para evidenciar la incorrección del algoritmo, consideremos el caso base con listas de tamaño $n = 2$:

* Primera lista: $A = [a_1, a_2]$
* Segunda lista: $B = [b_1, b_2]$

#### Estrategia del Adversario durante la Ejecución

1. **Primera comparación:**
El algoritmo compara los elementos cabeza $a_1$ y $b_1$. El adversario responde de manera consistente:

$$b_1 < a_1$$



Por lo tanto, $b_1$ es extraído e incorporado a la salida.
2. **Segunda comparación:**
El algoritmo compara ahora $a_1$ con $b_2$. El adversario responde:

$$a_1 < b_2$$



Por lo tanto, $a_1$ es extraído e incorporado a la salida. En este instante, a la primera lista $A$ le queda únicamente el elemento $a_2$.
3. **Activación de la Condición de Parada:**
Al cumplirse la condición de que a la primera lista le resta un solo elemento ($a_2$), el algoritmo suspende las comparaciones, vacía los elementos restantes de $B$ colocándolos en la salida y añade $a_2$ incondicionalmente al final.
4. El algoritmo concluye habiendo realizado dos comparaciones, que corresponden al peor caso para $n = 2$:

$$2n - 2 = 2(2) - 2 = 2$$



#### Asignación de Valores Concretos

El adversario asigna valores reales que cumplen estrictamente con las respuestas dadas ($b_1 < a_1$ y $a_1 < b_2$), pero contradicen la suposición implícita del algoritmo sobre la posición del elemento restante de $A$:


$$A = [2, 4], \qquad B = [1, 5]$$

Las comparaciones realizadas son compatibles también con otra entrada, por ejemplo $A = [2, 6]$ y $B = [1, 5]$. En esta segunda entrada, el elemento restante de $B$ sí es menor que el de $A$. Por tanto, las comparaciones realizadas no permiten determinar el orden relativo de los dos elementos restantes.

#### Traza de Ejecución sobre el Contraejemplo

1. Se compara $2$ (de $A$) con $1$ (de $B$). Como $1 < 2$, el elemento $1$ se coloca en la salida.
2. Se compara $2$ (de $A$) con $5$ (de $B$). Como $2 < 5$, el elemento $2$ se coloca en la salida.
3. A la primera lista $A$ le queda únicamente el elemento $4$.
4. Se activa la regla de parada anticipada: el algoritmo deja de comparar y vuelca los elementos restantes de $B$ ($[5]$) de forma directa, añadiendo el $4$ remanente al final.
5. Salida producida por el algoritmo:

$$\text{Salida} = [1, 2, 5, 4]$$



#### Contraste con el Resultado Correcto

La mezcla ordenada real y correcta de las listas debería ser:


$$\text{Salida Correcta} = [1, 2, 4, 5]$$

#### Conclusión del Adversario

El algoritmo falla porque las comparaciones realizadas ($1 < 2$ y $2 < 5$) no proporcionan información sobre la posición relativa del elemento restante $4$ respecto al elemento restante $5$. Ambas posibilidades son compatibles con las respuestas obtenidas.

Al asumir de forma arbitraria que el último elemento de la primera lista debe ubicarse después de todos los elementos restantes de la segunda lista, la variante pasa por alto que $4 < 5$, demostrando formalmente su incorrección.