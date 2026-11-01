Aquí tienes la respuesta completa al **Ejercicio 11** del resumen del Tema 1, aplicando el concepto de medición en bits de la Conferencia 1.

***

# Ejercicio 11: La mochila entera y el tamaño en bits

**Enunciado:** La mochila entera se resuelve con programación dinámica en \(O(n W)\), donde \(W\) es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

**Modelo:** Modelo RAM (word RAM) y medición de tamaño de entrada en bits.

---

## 1. Midiendo el tamaño de la entrada en bits

En el problema de la mochila entera (0/1 Knapsack), la entrada consta de:
*   \(n\) ítems, cada uno con un peso \(w_i\) y un valor \(v_i\).
*   Una capacidad máxima \(W\).

Para analizar la complejidad correctamente, debemos medir el tamaño de la entrada en **bits** (como aprendimos en la Sección 8 de la C1).
*   El número de ítems \(n\) se representa con \(\approx \log_2 n\) bits.
*   Los pesos y valores de los ítems ocupan una cantidad de bits proporcional a sus magnitudes.
*   **El dato clave:** La capacidad \(W\) es un número. Para escribirlo en binario se necesitan \(b = \lfloor \log_2 W \rfloor + 1\) bits. Es decir, el tamaño en bits de \(W\) es \(b = \Theta(\log W)\).

Por lo tanto, el tamaño total de la entrada en bits es aproximadamente \(N_{bits} = \Theta(n \log W)\) (asumiendo que los pesos y valores no son desproporcionadamente más grandes que \(W\)).

---

## 2. ¿Es polinomial el algoritmo \(O(n W)\)?

**No, no es un algoritmo polinomial en función del tamaño de la entrada.**

Analicemos la función de costo \(T(n, W) = O(n W)\).
Si expresamos \(W\) en función de su tamaño en bits \(b\):
\[
W = 2^b
\]

Sustituyendo esto en el costo del algoritmo:
\[
T(n, b) = O(n \cdot 2^b)
\]

Como \(b\) es parte del tamaño de la entrada, la función \(2^b\) crece **exponencialmente** con respecto al tamaño en bits de la capacidad. Por lo tanto, el algoritmo es **exponencial** en el tamaño de la entrada.

*(Nota: A los algoritmos cuyo tiempo de ejecución es polinomial en el **valor numérico** de la entrada, pero exponencial en su **tamaño en bits**, se les llama **pseudopolinomiales**. Este es el caso de la mochila).*

---

## 3. ¿En qué se parece a la primalidad por división?

El algoritmo de prueba de primalidad por división (que probaba todos los divisores hasta \(\sqrt{n}\)) y el algoritmo de la mochila por programación dinámica \(O(n W)\) comparten una característica fundamental: **ambos son pseudopolinomiales**.

*   **Primalidad por división:**
    *   Entrada: Un número \(n\).
    *   Tamaño en bits: \(b = \Theta(\log n)\).
    *   Costo: \(O(\sqrt{n}) = O(\sqrt{2^b}) = O(2^{b/2})\).
    *   **Conclusión:** Es exponencial en el tamaño de la entrada (los bits).

*   **Mochila entera:**
    *   Entrada: Ítems y una capacidad \(W\).
    *   Tamaño en bits: Incluye \(b_W = \Theta(\log W)\).
    *   Costo: \(O(n W) = O(n \cdot 2^{b_W})\).
    *   **Conclusión:** Es exponencial en el tamaño en bits de \(W\).

**El parecido:** Ambos algoritmos parecen "rápidos" si los analizamos pensando en los números como valores (probar hasta \(\sqrt{n}\) o llenar una tabla hasta \(W\)), pero son inviables para entradas grandes porque el número de bits necesarios para representar esos valores crece logarítmicamente. Un incremento de 1 bit en la entrada **duplica** el trabajo del algoritmo en ambos casos. 

**Diferencia clave:** A la mochila se le conoce como fuertemente NP-completa (o débilmente NP-completa), y tiene un algoritmo pseudopolinomial. El problema de primalidad, aunque el algoritmo de división sea pseudopolinomial, resultó tener algoritmos polinomiales verdaderos (como Miller-Rabin o AKS) en función de los bits. Para la mochila, no se conoce (ni se cree que exista, a menos que P=NP) un algoritmo polinomial en el número de bits.