## Problema

El problema de la mochila entera (*Knapsack 0/1*) se resuelve mediante programación dinámica en un tiempo de $\mathcal{O}(n \cdot W)$, donde $n$ es la cantidad de objetos y $W$ es la capacidad máxima de la mochila.

Midiendo el tamaño de la entrada en **bits** (tal como se establece en la sección 8 de la Conferencia 1):

1. Determine si dicho algoritmo es polinomial.
2. Explique en qué se asemeja al algoritmo de primalidad por división.

---

## Solución

### 1. ¿Es polinomial el algoritmo de la mochila?

**No, el algoritmo de programación dinámica no es polinomial en el tamaño de la entrada.**

#### Análisis Formal en Bits

En la teoría de complejidad computacional, el tamaño de una entrada se mide estrictamente por la **cantidad de bits** necesarios para representarla en memoria.

* Si la capacidad de la mochila es un número entero $W$, este valor requiere $b = \log_2 W$ bits para ser escrito en binario. Por lo tanto, el valor numérico de la capacidad expresado en función de su tamaño en bits es exponencial:

$$W = 2^b$$


* Sustituyendo esto en la complejidad temporal del algoritmo de programación dinámica ($\mathcal{O}(n \cdot W)$), obtenemos:

$$\mathcal{O}(n \cdot 2^b)$$



Como la complejidad temporal crece de forma **exponencial** respecto al tamaño de la entrada en bits ($b$), el algoritmo **no es polinomial**.

#### Definición de Pseudopolinomialidad

Cuando el tiempo de ejecución de un algoritmo es polinomial con respecto al *valor numérico* de los números de la entrada, pero exponencial con respecto a su *longitud en bits*, se clasifica como **pseudopolinomial**. El algoritmo de la mochila con su tabla de dimensiones $n \times W$ es el ejemplo clásico por excelencia de esta categoría.

---

### 2. Similitud con la Primalidad por División

El algoritmo de la mochila guarda un **paralelismo conceptual profundo** con el algoritmo de primalidad por división analizado en la Conferencia 1:

* **Dependencia del valor frente a los bits:** En la primalidad por división, para comprobar si un número $N$ es primo, se realizan divisiones hasta $\sqrt{N}$. Si medimos el tamaño de $N$ en bits ($b = \log_2 N$), el número de operaciones es $\mathcal{O}(\sqrt{N}) = \mathcal{O}(2^{b/2})$, lo cual es exponencial en la cantidad de bits. De forma análoga, en la mochila el costo es $\mathcal{O}(n \cdot W) = \mathcal{O}(n \cdot 2^b)$, que también depende exponencialmente del tamaño en bits de la capacidad $W$.
* **Engaño de la escala numérica:** Ambos algoritmos parecen "rápidos" y eficientes cuando los parámetros de entrada ($N$ o $W$) son números pequeños en su valor decimal (por ejemplo, $W = 100$). Sin embargo, en criptografía o en instancias grandes donde $W$ o $N$ alcanzan tamaños de 1024 bits ($2^{1024}$), los requerimientos temporales superan la edad del universo, demostrando que ambos son ineficientes cuando se analizan rigurosamente bajo la métrica del tamaño real de la entrada en bits.