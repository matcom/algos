# Problema 5 ★★

**Enunciado.** Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2. Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

## Solución formal

**Algoritmo.** Se usan dos punteros, `slow` y `fast`, que inicialmente apuntan a la cabeza de la lista. En cada iteración, `slow` avanza un nodo y `fast` avanza dos. Si en algún momento `slow == fast`, hay ciclo. Si `fast` llega a `None` o `fast.next` es `None`, no hay ciclo.

**Invariante.** Si hay un ciclo, una vez que `slow` entra al ciclo, `fast` ya está dentro. Sea $\lambda$ la longitud del ciclo. En cada iteración, `slow` avanza 1 y `fast` avanza 2, de modo que `fast` gana 1 posición a `slow` a lo largo del ciclo. Por tanto, la distancia (en pasos) de `fast` a `slow` a lo largo del ciclo disminuye en 1 módulo $\lambda$. Eventualmente la distancia es 0 y se encuentran.

**Terminación.**

- Si no hay ciclo, `fast` llega a `None` en a lo sumo $n/2$ iteraciones.
- Si hay ciclo, sea $\mu$ la longitud de la cola antes del ciclo. Tras $\mu$ iteraciones, `slow` entra al ciclo. En ese momento, `fast` está en alguna posición del ciclo. La distancia entre ambos es a lo sumo $\lambda-1$. Como esa distancia disminuye en 1 en cada iteración, en a lo sumo $\lambda$ iteraciones más se encuentran. Total: $O(\mu + \lambda) = O(n)$.

**Potencial.** Se puede tomar $\Phi$ como la distancia (en el sentido de avance) de `fast` a `slow` dentro del ciclo. Es un entero no negativo que decrece en 1 en cada iteración mientras ambos están en el ciclo. Cuando $\Phi = 0$, se cumple `slow == fast`.

**Costo.** Tiempo $O(n)$, espacio $O(1)$.
