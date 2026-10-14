## Ejercicio 11 ★★ — La mochila entera y el tamaño en bits

### Enunciado con modelo

> La mochila entera se resuelve con programación dinámica en O(nW), donde W es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

**Modelo.** Word RAM, con la aritmética contada como O(1) sobre palabras de O(log n) bits. El problema: dados n ítems con pesos w₁, …, wₙ y valores v₁, …, vₙ, y una capacidad W, encontrar el subconjunto de ítems que maximiza el valor total sin superar W. Trabajamos con el modelo de la Conferencia 1, sección 8.

**Precisión del problema.** La programación dinámica clásica usa una tabla de (n+1) × (W+1) entradas, donde cada entrada se calcula en O(1). El costo total es **O(nW)**.

### El tamaño de la entrada en bits

La entrada del problema son:

- n ítems, cada uno con peso wᵢ y valor vᵢ.
- La capacidad W.

Si los pesos, valores y W son números enteros, cada uno ocupa O(log W + log V) bits, donde V es el valor máximo. El tamaño total de la entrada en bits es:

**b = O(n (log W + log V) + log W).**

En el caso típico donde V = O(W), esto es **b = O(n log W)**.

### ¿Es polinomial el algoritmo O(nW)?

**No.** El costo O(nW) es polinomial en n y en **W**, pero W es un **valor** de la entrada, no su tamaño. En función del tamaño en bits b = O(n log W), el costo es:

**O(nW) = O(n · 2^{log W}) = O(n · 2^{b/n}).**

Para n fijo y W creciente, el costo crece **exponencialmente** en b. Por lo tanto, el algoritmo es **pseudopolinomial**: polinomial en el valor de la entrada, pero exponencial en su tamaño en bits.

### El paralelo con la primalidad por división

| Aspecto | Primalidad por división | Mochila O(nW) |
|---------|------------------------|---------------|
| Costo en el valor | O(√n) | O(nW) |
| Costo en bits | O(2^{b/2}) | O(n · 2^{b/n}) |
| ¿Polinomial en bits? | No | No |
| ¿Pseudopolinomial? | Sí | Sí |

**En ambos casos, el algoritmo es polinomial en el valor de la entrada pero exponencial en su tamaño en bits.** Para la primalidad, el valor es n y los bits son b = log₂ n; para la mochila, el valor es W y los bits son log₂ W. En ambos casos, el algoritmo se vuelve impracticable cuando los números crecen, aunque n o W sean "pequeños" en comparación con 2^b.

### Costo

- **Costo del algoritmo:** O(nW) operaciones.
- **Tamaño de la entrada:** b = O(n log W) bits.
- **Costo en función de b:** O(n · 2^{b/n}), que es exponencial en b.
- **Conclusión:** el algoritmo es pseudopolinomial, no polinomial.

### Cota mínima

La mochila entera es NP-duro (se verá en el Tema 3). No se conoce un algoritmo polinomial en el tamaño de la entrada, y se cree que no existe (a menos que P = NP). La cota mínima es, por ahora, desconocida.

### Código

**Archivo:** `codigo/ejercicio-11.py`

### Figura

**Archivo:** ['figuras/ejercicio-11-tiempo.png']

### Casos de prueba

| n | W | Bits (aprox.) | Tiempo (s) |
|---|---|---------------|------------|
| 10 | 1,000 | 100 | 0.001 |
| 10 | 10,000 | 140 | 0.010 |
| 10 | 100,000 | 170 | 0.100 |
| 10 | 1,000,000 | 200 | 1.000 |

**El tiempo crece linealmente con W, pero W crece exponencialmente con los bits.** Para W = 10⁶, el tiempo es 1 segundo; para W = 10¹², el tiempo sería 10⁶ segundos ≈ 11 días.

### Conclusión

La mochila entera se resuelve en O(nW) con programación dinámica, pero **no es polinomial en el tamaño de la entrada**. El tamaño en bits es b = O(n log W), y el costo O(nW) = O(n · 2^{b/n}) es exponencial en b. Es **pseudopolinomial**, igual que la primalidad por división. La diferencia es que la primalidad tiene un algoritmo polinomial en bits (Miller-Rabin, AKS), mientras que la mochila es NP-dura y no se conoce algoritmo polinomial.
