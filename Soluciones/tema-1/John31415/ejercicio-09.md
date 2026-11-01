## Problema

Dada una variante "optimizada" del algoritmo clásico de mezcla (*merge*) de dos listas ordenadas de longitud $n$, la cual se detiene anticipadamente y deja de realizar comparaciones en el momento exacto en que a la primera lista le resta un único elemento, colocándolo directamente al final de la mezcla:

1. Determine el número de comparaciones realizadas en el peor caso.
2. Decida formalmente su correctitud apoyándose en los resultados teóricos de cota inferior para la mezcla de listas.
3. Construya explícitamente una entrada de contraejemplo mediante el **método del adversario** para demostrar el fallo del algoritmo.

---

## Solución

### 1. Cantidad de Comparaciones en el Peor Caso

En el algoritmo estándar de mezcla de dos listas ordenadas de tamaño $n$, cada comparación entre las cabezas de ambas listas permite ubicar un elemento en su posición definitiva, requiriendo un total de $2n - 1$ comparaciones en el peor caso (cuando la última comparación ocurre al restar un único elemento en cada lista).

En la variante propuesta, el proceso de comparación se interrumpe prematuramente tan pronto como a la primera lista $A$ le queda un único elemento ($a_n$), pasando a vaciar el resto de la segunda lista $B$ sin comparaciones y añadiendo $a_n$ al final.

Para maximizar el número de comparaciones antes de activar esta condición de parada:

* Se deben extraer mediante comparaciones los primeros $n - 1$ elementos de la primera lista $A$.
* Durante dicho proceso, el algoritmo no debe consumir elementos de la segunda lista $B$.
* Una vez que a la primera lista le resta un único elemento, se requieren otras $n - 1$ comparaciones para incorporar los $n - 1$ elementos iniciales de la segunda lista $B$ (el último elemento restante se acopla directamente por la regla de parada).

Por consiguiente, el número máximo de comparaciones ejecutadas en el peor caso es:


$$\text{Comparaciones} = (n - 1) + (n - 1) = 2n - 2$$

Este peor caso se materializa, por ejemplo, cuando todos los elementos de la primera lista son estrictamente menores que todos los elementos de la segunda lista, obligando al algoritmo a consumir casi toda la primera lista antes de detenerse.

---

### 2. Análisis de Correctitud (Basado en Cota Inferior)

El algoritmo **no es correcto** para todas las instancias posibles.

#### Justificación Teórica

De acuerdo con la teoría de árboles de decisión y los resultados formales de cota inferior para la mezcla (específicamente la teoría de mezclas óptimas), cualquier algoritmo basado en comparaciones que mezcle correctamente dos listas ordenadas de longitud $n$ requiere demostrar un número mínimo de **$2n - 1$ comparaciones** en el peor caso absoluto para distinguir entre las $\binom{2n}{n}$ configuraciones posibles de orden relativo.

Dado que la variante propuesta ejecuta como máximo $2n - 2$ comparaciones, viola la cota inferior teórica necesaria para garantizar un resultado correcto en todas las entradas. Al omitir al menos una comparación crucial, el algoritmo carece de la información suficiente sobre las relaciones de orden entre los elementos restantes, lo que inevitablemente conduce a fallos estructurales en ciertos escenarios construidos por un adversario.

---

### 3. Construcción de la Entrada Fallida mediante el Adversario

Para evidenciar la incorrección del algoritmo, consideremos el caso base con listas de tamaño $n = 2$:

* Primera lista: $A = [a_1, a_2]$
* Segunda lista: $B = [b_1, b_2]$

#### Estrategia del Adversario durante la Ejecución

1. **Primera comparación:** El algoritmo compara el elemento cabeza $a_1$ con $b_1$. El adversario responde de manera consistente:

$$a_1 < b_1$$



Por lo tanto, $a_1$ es extraído e incorporado a la salida. En este instante, a la primera lista $A$ le queda únicamente el elemento $a_2$.
2. **Activación de la Condición de Parada:** Al cumplirse la condición de que a la primera lista le resta un solo elemento ($a_2$), el algoritmo **suspende las comparaciones**, vacía los elementos restantes de $B$ colocándolos en la salida, y añade $a_2$ incondicionalmente al final.
3. El algoritmo concluye habiendo realizado **una única comparación** ($2n - 2 = 2(2) - 2 = 2$ es el peor caso teórico de esta variante, pero en esta traza específica se detiene antes).

#### Asignación de Valores Concretos

El adversario asigna valores reales que cumplen estrictamente con la respuesta dada ($a_1 < b_1$) pero contradicen la suposición implícita del algoritmo:


$$A = [1, 2], \quad B = [5, 6]$$

#### Traza de Ejecución sobre el Contraejemplo:

1. Se compara $1$ (de $A$) con $5$ (de $B$). Como $1 < 5$, el elemento $1$ se coloca en la salida.
2. A la primera lista $A$ le queda únicamente el elemento $2$.
3. Se activa la regla de parada anticipada: el algoritmo deja de comparar y vuelca los elementos restantes de $B$ ($[5, 6]$) de forma directa, añadiendo el $2$ remanente al final.
4. **Salida producida por el algoritmo:**

$$\text{Salida} = [1, 5, 6, 2]$$



#### Contraste con el Resultado Correcto

La mezcla ordenada real y correcta de los conjuntos debería ser:


$$\text{Salida Correcta} = [1, 2, 5, 6]$$

#### Conclusión del Adversario

El algoritmo falla porque la única comparación realizada ($1 < 5$) no otorga información sobre la posición relativa del elemento $2$ respecto a los elementos grandes de $B$ ($5$ y $6$). Al asumir de forma arbitraria que el último elemento de la primera lista debe ubicarse al final, la variante pasa por alto que $2$ es menor que $5$ y $6$, demostrando formalmente su incorrección.