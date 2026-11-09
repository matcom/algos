# Ejercicio 11: la mochila y el tamaño en bits

> La mochila entera se resuelve con programación dinámica en O(nW), donde W es la capacidad. Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

## El algoritmo

La programación dinámica llena una tabla de (n + 1) filas por (W + 1) columnas. La casilla (i, w) guarda el mejor valor usando los primeros i objetos con capacidad w. Cada casilla se calcula en O(1) mirando la fila anterior.

## Tamaño de la entrada

En la entrada hay n objetos, cada uno con un peso y un valor, y la capacidad W de la mochila.

W es un número, y no ocupa lo que vale sino los bits que hacen falta para escribirlo: ⌊log₂ W⌋ + 1 ≈ log₂ W bits. Llamo b a esa cantidad, así que W ≈ 2^b.

El tamaño total de la entrada es al menos n + log₂ W bits, porque cada objeto ocupa al menos un bit, más los bits de W.

## Costo en función de los bits

El algoritmo llena n·(W + 1) casillas. En función de b, eso es n·(2^b + 1). El costo es **Θ(n·2^b)**:

- **O:** la tabla no tiene más casillas que esas, y cada una cuesta O(1).
- **Ω:** el algoritmo llena todas las casillas, así que hace al menos ese trabajo.

El algoritmo es **pseudopolinomial**: es polinomial en el *valor* de W, pero exponencial en la cantidad de *bits* de W. Agregar un solo bit a W (que casi no cambia el tamaño de la entrada) duplica el número de columnas de la tabla, y con eso el trabajo.

## El parecido con la primalidad por división

Los dos algoritmos hacen un trabajo proporcional al **valor** de un número de la entrada, no a su tamaño.

En la primalidad, el algoritmo prueba √n divisores, pero para escribir n se necesitan log₂ n = b bits. Entonces en realidad son √(2^b) = 2^(b/2) divisiones, que también es exponencial. En la mochila pasa lo mismo con W: n·W parece un polinomio, pero en bits es n·2^b.

## Cuándo sí es polinomial

Si W está acotado por algo polinomial en n, por ejemplo W ≤ 100·n (porque los pesos son números pequeños), entonces n·W ≤ 100·n², o sea O(n²). Como el tamaño de la entrada es al menos n, eso es polinomial en el tamaño. Es un caso en que limitar la entrada da un mejor tiempo: la exponencialidad solo aparece cuando W puede ser enorme comparado con n.

## Experimentos

`ej11_mochila.py` implementa la tabla, la compara con la fuerza bruta (probar los 2^n subconjuntos) en 500 instancias pequeñas sin fallos, y después fija n = 20 y le va agregando bits a W:

```
 bits de W          W     casillas    tiempo
        10      1,023       20,480    0.002s
        11      2,047       40,960    0.005s
        12      4,095       81,920    0.011s
        13      8,191      163,840    0.026s
        14     16,383      327,680    0.057s
        15     32,767      655,360    0.122s
        16     65,535    1,310,720    0.342s
        17    131,071    2,621,440    0.531s
        18    262,143    5,242,880    1.124s
```

Cada bit más en W duplica las casillas y, aproximadamente, el tiempo: la entrada crece en un bit y el trabajo se multiplica por 2. Es el comportamiento de un algoritmo exponencial en el tamaño de la entrada.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación y los casos de prueba, y como tutor (pistas y corrección de mi redacción). El análisis es mío.*
