## Ejercicio 1 ★ — Una computadora mil veces más rápida

### Enunciado

> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)? Estima los dos factores. (C1)

**Modelo.** Word RAM, con la aritmética contada como O(1) sobre palabras de O(log n) bits. Medimos el número de operaciones como función del tamaño de la entrada n. Suponemos que la computadora hace una cantidad fija de operaciones por segundo y que el presupuesto es de una hora. El "tamaño de entrada que se resuelve" es el mayor n tal que el costo del algoritmo sobre esa entrada no supera el presupuesto.

### Planteamiento

Sea C el presupuesto de operaciones en una hora. En la computadora actual, C = 3600 · 10⁹ operaciones (una computadora que hace 10⁹ operaciones por segundo). En la computadora mil veces más rápida, el presupuesto es C' = 1000 · C = 3.6 · 10¹⁵ operaciones.

Buscamos el factor de crecimiento del tamaño de entrada:

- Para un algoritmo Θ(n²): sea n₀ el mayor n con n₀² ≤ C. Sea n₁ el mayor n con n₁² ≤ C'. Entonces n₁² / n₀² = C' / C = 1000, así que n₁/n₀ = √1000 ≈ 31.62.
- Para un algoritmo Θ(n log n): sea n₀ el mayor n con n₀ log₂ n₀ ≤ C. Sea n₁ el mayor n con n₁ log₂ n₁ ≤ C'. Entonces n₁ log₂ n₁ / (n₀ log₂ n₀) = 1000. Para n grande, log₂ n₁ ≈ log₂ n₀ + log₂(n₁/n₀), y podemos despejar el factor.

### Cálculo detallado

**Caso Θ(n²).**

El factor es exactamente √1000:

n₁ / n₀ = √(C'/C) = √1000 ≈ **31.62**.

Esto significa que si la computadora actual resuelve n₀ = 60,000 en una hora (porque 60,000² = 3.6 · 10⁹), la computadora mil veces más rápida resuelve n₁ ≈ 60,000 · 31.62 ≈ **1,897,000** en una hora. Verificación: (1.897 · 10⁶)² ≈ 3.6 · 10¹², que es 1000 veces 3.6 · 10⁹. 

**Caso Θ(n log n).**

Queremos el factor f = n₁/n₀ tal que:

(n₁ log₂ n₁) / (n₀ log₂ n₀) = 1000.

Escribimos n₁ = f · n₀ y tomamos logaritmos para despejar f. Para n₀ grande, log₂ n₁ = log₂ n₀ + log₂ f. Entonces:

f · (log₂ n₀ + log₂ f) / log₂ n₀ = 1000
f · (1 + log₂ f / log₂ n₀) = 1000.

Si n₀ es muy grande, el término log₂ f / log₂ n₀ es pequeño comparado con 1, y f ≈ 1000. Pero para valores realistas de n₀ (digamos n₀ = 10⁸, log₂ n₀ ≈ 26.6), el término no es despreciable. Resolvamos numéricamente.

**Ejemplo numérico.** Tomemos C = 3.6 · 10⁹ operaciones (computadora actual, 10⁹ ops/seg, una hora) y C' = 3.6 · 10¹² operaciones (mil veces más rápida).

Para Θ(n log₂ n), buscamos el mayor n con n log₂ n ≤ C.

- Actual: n₀ = 10⁸ → 10⁸ · log₂(10⁸) = 10⁸ · 26.575 ≈ 2.66 · 10⁹ ≤ 3.6 · 10⁹. n₀ = 1.2 · 10⁸ → 1.2 · 10⁸ · 27.84 ≈ 3.34 · 10⁹ ≤ 3.6 · 10⁹. n₀ ≈ 1.28 · 10⁸ → 1.28 · 10⁸ · 27.93 ≈ 3.58 · 10⁹. Así que **n₀ ≈ 1.28 · 10⁸**.
- Mil veces más rápida: n₁ = 10¹¹ → 10¹¹ · log₂(10¹¹) = 10¹¹ · 36.54 ≈ 3.65 · 10¹² ≈ C'. n₁ ≈ 9.85 · 10¹⁰ → 9.85 · 10¹⁰ · 36.52 ≈ 3.60 · 10¹². Así que **n₁ ≈ 9.85 · 10¹⁰**.

El factor es n₁/n₀ ≈ 9.85 · 10¹⁰ / 1.28 · 10⁸ ≈ **770**.

**Interpretación.** Para Θ(n log n), el factor es cercano a 1000 pero algo menor, porque el logaritmo también crece. Para n₀ muy grande, el factor tiende a 1000; para n₀ pequeño, el factor es menor. La fórmula aproximada es:

n₁ / n₀ ≈ 1000 / (1 + log₂(1000) / log₂ n₀) = 1000 / (1 + 9.97 / log₂ n₀).

Para n₀ = 10⁸ (log₂ n₀ ≈ 26.6): factor ≈ 1000 / (1 + 0.375) ≈ **727**. El cálculo numérico dio 770, del mismo orden. La diferencia viene de que la aproximación log₂ n₁ ≈ log₂ n₀ + log₂ f no es exacta.

### Código

El programa que calcula los factores de crecimiento está en
[`codigos/ejercicio-01.py`](codigos/ejercicio-01.py).

### Resumen de los dos factores

| Costo | Factor de crecimiento |
|-------|----------------------|
| Θ(n²) | √1000 ≈ **31.6** |
| Θ(n log n) | ≈ **770** (para n₀ ≈ 10⁸); tiende a 1000 cuando n₀ → ∞ |

### Comentario 

La lección de la sección 7 de la Conferencia 1 es que **una computadora más rápida beneficia mucho a los algoritmos lineales y casi nada a los exponenciales**. Aquí vemos el caso intermedio: un algoritmo Θ(n²) solo gana un factor √1000 ≈ 31.6 en tamaño de entrada, mientras que uno Θ(n log n) gana casi 1000. La diferencia entre n² y n log n es enorme en la práctica, y por eso vale la pena buscar el algoritmo asintóticamente mejor aunque las constantes sean peores.

**Cota mínima.** No aplica: este ejercicio no pide una cota mínima, sino una estimación del factor de crecimiento.

**Conclusión.** Mil veces más potencia de cómputo compra un factor ≈ 31.6 en tamaño para Θ(n²) y un factor ≈ 770 para Θ(n log n). El algoritmo lineal (o casi lineal) es el que más se beneficia del hardware.
