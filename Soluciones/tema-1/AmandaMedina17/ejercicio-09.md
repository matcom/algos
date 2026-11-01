**Problema:** Una mezcla "optimizada" de dos listas ordenadas de largo deja de comparar cuando a la primera
lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso.
Sin probarla, decide si es correcta, y construye con el adversario la entrada en la que falla.

## 1. Comparaciones en el peor caso:

En el algoritmo de mezcla $Merge$, para dos listas ordenas de tamaño $n$, el peor caso requiere realizar $2n-1$ comparaciones, que es cuando los elementos de ambas listas se intercalan uno a uno y queda un elemento final en una de ellas.

Ahora para la variante optimizada:

- Condición de parada: el algoritmo deja de comparar exactamente en el momento en que la primera lista le queda un solo elemento sin procesar, y procede a colocar ese elemento al final del resultado.
- Para que la primera lista de tamaño $n$ le quede exactamente 1 elemento, el algoritmo debe coger $n-1$ elementos de dicha lista mediante comparaciones.
- Para maximizar el número de comparaciones antes de alcanzar la condición de parada, el adversario diseña las listas de modo que los elementos de la segunda lista se intercalen alternadamente con los de la primera lista. Así por cada elemento de la primera lista que se procesa hasta $n-1$, se compara y se procesa un elemento de la segunda lista.
- Con esto, se consumen $n-1$ elementos de la primera lista y en el peor caso de entrelazamiento, se habrán comparado $n-1$ o $n$ elementos de la segunda lista. Por tanto, el número total de comparaciones en el peor caso es: $C=(n-1)+(n-1)=2n-2$ o $C=(n-1)+n=2n-1$.

## 2. Análisis de la correctitud:

Un algoritmo de mezcla es correcto si y solo si garantiza que el resultado final es una secuencia ordenada que contiene todos lo elementos de ambas listas de entrada.

La heurística de "dejar de comparar cuando a la primera lista le queda un solo elemento y ponerlo al final" asume una hipótesis falsa: asume que el último elemento de la primera lista es mayor o igual que todos los elementos restantes de la segunda lista. Si esta predicción falla, colocar ese elemento al final rompe inmediatamente la propiedad de ordenación, ya que un elemento menor quedará ubicado después de elementos mayores.

## 3. Construcción de la entrada de fallo con el adversario:

Para demostrar la incorreción del algoritmo, aplicaremos el Método del Adversario.

Definición de las listas del adversario:
Supongamos que el tamaño de las listas $n=2$. Definimos dos listas ordenadas:

- Lista 1: $[1,5]$
- Lista 2: $[2,6]$
  Ambas listas están correctamente ordenadas de forma individual.

Flujo de la ejecución de algoritmo:

1: Estado inicial:

- $[1,5]$ (puntero en el índice 0, valor 1)
- $[2,6]$ (puntero en el índice 0, valor 2)
- Ans = []

2: Primera comparación:

- El algoritmo compara 1 < 2, se agrega el uno a la respuesta y se avanza el puntero en la primera lista
- $[5]$ (puntero en el índice 1, valor 5)
- $[2, 6]$ (puntero en el índice 0, valor 2)
- Ans = $[1]$

3: Activación de la regla de parada:

- Al verificar que cada un solo elemento en la primera lista, el algoritmo deja de comprar inmediatamente. Para finalizar, agrega a la respuesta los elementos restantes en la segunda lista, y luego, agrega el elemento que queda de la primera.
- Ans = $[1, 2, 6, 5]$

Como se puede observar, la lista resultante no está ordenada, ya que $Ans[2] > Ans[3]$.

## Conclusión:

El uso del método del adversario demuestra que la optimización propuesta es incorrecta. Y se puede decir que, ningún atajo que detenga las comparaciones basándose en el tamaño residual de una de las listas puede garantizar la correctitud del orden global, ya que los elementos comparados en la otra lista pueden alterar la relación de precedencia.
