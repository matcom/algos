# Solución ejercicio 4

Sea t el número de unos finales del contador => los unos consecutivos que empiezan en el LSB

1. Avanza a la izquierda en la cinta cambiando cada 1 por 0: t pasos
2. En el primer 0 escribe 1 => 1 paso
3. Vuelve al LSB en a lo sumo t pasos

Costo real: c <= 2*t + 2

Analicemos su potencial:
------------------------

k = número de unos en el contador

- k >= 0 siempre y k0 = 0 porque empieza desde 0.
- Un incremento convierte t unos en ceros y un cero en uno, por ende Δk = 1 - t

Definimos ĉ = c + 2Δk => ĉ <= (2*t + 2) + 2(1 - t) = 4

Por lo tanto poder afirmar que:

Σ c = Σ ĉ - 2(k_m - k0) <= 4k - 2*k_m <= 4m

porque k_m >= k0. Por ende, m incrementos desde 0 cuestan O(m) pasos en total.

Un solo incremento puede costar O(log m):

- Cota superior: Tras m incrementos, el contador vale a lo sumo m y tiene ⌊log2(m)⌋ + 1 bits, así que t <= ⌊log2(m)⌋ + 1 y c <= 2 * log2 m +4.

- Cota inferior: el incremento lleva el contador de 2^k - 1 a 2^k cuesta 2k + 1 pasos: k para poner ceros, 1 para escribir el uno y k para volver. Con m = 2^k => O(logm)

Por lo tanto el peor incremento cuesta Θ(log m), pero el potencial muestra que la deuda de unos que paga ese incremento digamos "caro" se acumuló en incrementos "baratos" anteriores

El coste medio por incremento es O(1), con garantía de peor caso sobre la secuencia , y podemos decir que m incrementos cuestan Θ(m): la cota inferior es m pasos porque cada incremento da al menos 1.