# Ejercicio 11

### El problema 
> La mochila entera se resuelve con programación dinámica en $\Theta(n \cdot W)$, donde $W$ es la capacidad. Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

---

### Medición del tamaño de la entrada en bits

Siguiendo la teoría de la **Conferencia 1 (Sección 8)**, la complejidad de un algoritmo no se mide en función del *valor* de los parámetros numéricos de entrada, sino del **tamaño de la entrada medido en bits**, pues esto representa el espacio real que ocupa en memoria y lo que la máquina RAM debe procesar.

Dada una instancia del problema de la mochila con $n$ objetos (cada uno con peso $w_i$ y valor $v_i$) y una capacidad máxima $W$:

* Para representar la capacidad $W$ en binario se requieren:
  $$b_W = \lfloor \log_2 W \rfloor + 1 = \Theta(\log W) \text{ bits}$$
* Para representar la cantidad de objetos $n$ y las listas de pesos y valores en binario se requieren:
  $$b_{objetos} = \Theta(n) + \sum_{i=1}^n \left( \Theta(\log w_i) + \Theta(\log v_i) \right) \text{ bits}$$

Por lo tanto, la longitud total de la entrada en bits $L$ es la suma de sus componentes:
$$L = b_W + b_{objetos} = \Omega(n + \log W)$$

De aquí despejamos la capacidad $W$ en función del número de bits $b_W$ necesarios para codificarla:
$$W = \Theta(2^{b_W})$$

---

### Análisis de complejidad y polinomialidad

El algoritmo clásico de programación dinámica llena una tabla de dimensiones $(n + 1) \times (W + 1)$, realizando un número total de operaciones de:
$$T(n, W) = \Theta(n \cdot W)$$

Sustituyendo $W$ en función del tamaño real de su representación en bits ($b_W$):
$$T(n, b_W) = \Theta(n \cdot 2^{b_W})$$

Expresado en función de la longitud total de la entrada en bits $L$:
$$T(L) = \Omega(n \cdot 2^{\Omega(L)})$$

#### ¿Es polinomial este algoritmo?
**No, el algoritmo NO es polinomial.** Es **exponencial en el tamaño de la entrada** ($L$). 

Formalmente, como su costo es polinomial con respecto al *valor numérico* de una de sus entradas ($W$), pero exponencial respecto al *número de bits* necesarios para representarla ($\log W$), el algoritmo se clasifica como **pseudopolinomial** (tal como define la Conferencia 1 en la Sección 8).

---

### Semejanza con la primalidad por división

La relación entre el algoritmo de programación dinámica para la mochila y el algoritmo de división tentativa para verificar si un número $N$ es primo (`es_primo(N)`) es directa y conceptualmente idéntica:

1. **Confusión entre valor de entrada y tamaño en bits:**
   * **Primalidad:** Probar divisores hasta $\sqrt{N}$ toma $O(\sqrt{N})$ divisiones. Aunque $\sqrt{N}$ crece más despacio que $N$, el tamaño de la entrada es $b = \log_2 N$ bits. En función de $b$, el costo es $O(2^{b/2})$, lo que lo hace exponencial en la cantidad de bits.
   * **Mochila:** Llenar la tabla toma $\Theta(n \cdot W)$ operaciones. Aunque $W$ es un simple valor entero, requiere $b_W = \log_2 W$ bits. En función de $b_W$, el costo es $\Theta(n \cdot 2^{b_W})$, exponencial en la cantidad de bits.

2. **Efecto de agregar un solo bit a la entrada:**
   * En la **primalidad**, al agregar 1 bit al número $N$ (lo que aproximadamente duplica su valor), el número de divisiones necesarias se multiplica por $\approx \sqrt{2} \approx 1.41$.
   * En la **mochila**, al agregar 1 bit a la capacidad $W$ en binario (lo que duplica el valor de $W$), el tamaño de la tabla y la cantidad de operaciones del algoritmo se **duplican exactamente** ($\Theta(n \cdot 2W)$).

En conclusión, ambos algoritmos son **pseudopolinomiales**: parecen rápidos y eficientes cuando se evalúan con valores numéricos pequeños, pero se vuelven computacionalmente inviables cuando el tamaño binario de la entrada (el número de bits) crece.