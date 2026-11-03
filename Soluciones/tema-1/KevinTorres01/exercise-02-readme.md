# Ejercicio 2 — Búsqueda Binaria: Invariante, Potencial y Cota

**Diseño y Análisis de Algoritmos · Tema 1 · Curso 2026**

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima. (C3, C5)

---

## 1. Descripción del algoritmo

Dado un arreglo ordenado $A$ de tamaño $n$ y un valor $x$, el algoritmo de búsqueda binaria mantiene dos índices, `low` y `high`, que delimitan el subarreglo donde aún es posible encontrar a $x$. En cada iteración:
1. Se calcula el punto medio `mid = (low + high) / 2`.
2. Si `A[mid] == x`, se devuelve `mid` (encontrado).
3. Si `A[mid] < x`, se descarta la mitad izquierda actualizando `low = mid + 1`.
4. Si `A[mid] > x`, se descarta la mitad derecha actualizando `high = mid - 1`.

Si el ciclo termina (`low > high`), se concluye que $x$ no está en el arreglo.

## 2. Correctitud total

La correctitud total se compone de correctitud parcial (demostrada con el invariante) más terminación (demostrada con el potencial).

### 2.1 Correctitud parcial (Invariante)

**Invariante:** *Al inicio de cada iteración, si $x$ está en el arreglo, entonces está en el subarreglo $A[\text{low} \ldots \text{high}]$. Además, todos los elementos a la izquierda de `low` son estrictamente menores que $x$, y todos los elementos a la derecha de `high` son estrictamente mayores que $x$.*

- **Inicialización:** Antes de la primera iteración, `low = 0` y `high = n - 1`. El subarreglo es el arreglo completo, por lo que si $x$ está, está en ese rango. No hay elementos fuera del rango, por lo que las condiciones sobre los extremos se cumplen trivialmente.
- **Mantenimiento:** Supongamos que el invariante se cumple.
  - Si `A[mid] < x`: Como el arreglo está ordenado, todos los elementos en $A[\text{low} \ldots \text{mid}]$ son menores o iguales a `A[mid]`, y por lo tanto estrictamente menores que $x$. Al hacer `low = mid + 1`, descartamos esa parte con seguridad. La nueva porción $A[\text{low} \ldots \text{high}]$ sigue conteniendo a $x$ si estaba en el rango anterior.
  - Si `A[mid] > x`: Simétricamente, todos los elementos en $A[\text{mid} \ldots \text{high}]$ son estrictamente mayores que $x$. Al hacer `high = mid - 1`, los descartamos con seguridad, preservando el invariante.
- **Conclusión:** Si el ciclo termina porque `low > high`, el subarreglo $A[\text{low} \ldots \text{high}]$ está vacío. Por el invariante, si $x$ estuviera en el arreglo, debería estar en ese subarreglo vacío, lo cual es una contradicción. Por lo tanto, $x$ no está en el arreglo. Si el algoritmo termina antes (encontrando `A[mid] == x`), devuelve la posición correcta.

### 2.2 Terminación (Potencial)

Para demostrar que el ciclo termina, definimos el potencial como el tamaño del espacio de búsqueda:
$$
\Phi = \text{high} - \text{low} + 1
$$
(Con la convención de que si `low > high`, $\Phi = 0$).

- **Propiedad básica:** $\Phi \ge 0$ siempre, porque el tamaño de un intervalo no puede ser negativo.
- **Decrecimiento estricto:** En cada iteración, si no se encuentra $x$, el algoritmo actualiza `low` o `high`. Como `mid` es estrictamente menor que `high` (cuando el tamaño es mayor que 1), el nuevo tamaño del intervalo será menor que el anterior. Es decir, $\Phi$ disminuye estrictamente en cada iteración.
- **Conclusión:** Al ser $\Phi$ un entero no negativo que decrece estrictamente en cada paso, el ciclo debe terminar después de un número finito de iteraciones (a lo sumo $O(\log n)$, ya que el intervalo se divide a la mitad).

## 3. Cota mínima de información ($\Omega(\log n)$)

El modelo es el de árboles de decisión, donde cada nodo interno representa una comparación y las hojas representan las posibles salidas del algoritmo.

1. **Posibles respuestas:** Para un arreglo de tamaño $n$, el elemento $x$ puede estar en cualquiera de las $n$ posiciones. Además, si $x$ no está en el arreglo, hay $n + 1$ "huecos" donde podría insertarse (antes del primer elemento, entre cada par, y después del último). Por lo tanto, el número total de respuestas posibles es:
   $$
   n + (n + 1) = 2n + 1
   $$
2. **Altura del árbol:** Un árbol binario con $L$ hojas tiene una altura mínima de $\lceil \log_2 L \rceil$. Sustituyendo $L = 2n + 1$, la cantidad mínima de comparaciones en el peor caso es:
   $$
   \lceil \log_2(2n + 1) \rceil
   $$
3. **Conclusión:** Cualquier algoritmo basado en comparaciones requiere $\Omega(\log(2n + 1)) = \Omega(\log n)$ comparaciones. La búsqueda binaria realiza un número de comparaciones de este orden, por lo que es asintóticamente óptima.