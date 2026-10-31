# Ejercicio 14: máximo de un arreglo unimodal

## Enunciado

Escoge un problema que no hayamos visto, recorre el ciclo completo (problema, algoritmo, correctitud, costo, cota mínima) y consigue que el algoritmo y la cota mínima coincidan.

**Problema escogido: máximo de un arreglo unimodal.** Dado un arreglo que crece y luego decrece, encontrar la posición de su máximo.

## Convenciones

- **Entrada:** `A[1..n]` con `n >= 1` y todos los valores distintos, tal que existe `p ∈ [1, n]` con `A[1] < A[2] < ... < A[p] > A[p+1] > ... > A[n]`. El arreglo puede ser solo creciente (`p = n`) o solo decreciente (`p = 1`). Ese `p` es único: es la posición del máximo.
- **Salida:** `p`.
- **Modelo:** comparaciones. Los valores solo se conocen por preguntas `A[i] < A[j]`, con cualquier par `i != j`. Todo el cómputo con índices y respuestas es gratis.
- **Costo:** el número de comparaciones. Cada una cuenta 1, con el resultado que tenga. Como los valores son distintos, cada pregunta tiene exactamente dos respuestas.
- **Por qué "valores distintos":** la hipótesis es esencial. Si se permitieran repetidos, por ejemplo `[0, 0, 1, 0, 0]`, un adversario que responde "iguales" a todo descarta como mucho dos candidatos por comparación (los dos que se comparan), y hacen falta al menos `⌊n/2⌋` comparaciones: el costo pasa a `Ω(n)` y la búsqueda binaria deja de servir.
- **Alcance de la cota:** la cota inferior vale en este modelo (comparaciones entre elementos), no para algoritmos que usen los valores de otra forma.

## Algoritmo

```
pico(A):                            // A[1..n] unimodal, valores distintos
    lo = 1
    hi = n
    while lo < hi:
        m = ⌊(lo + hi) / 2⌋         // lo <= m < hi, luego m + 1 <= hi
        if A[m] < A[m + 1]:         // 1 comparación: ¿sube?
            lo = m + 1              // el pico está a la derecha de m
        else:
            hi = m                  // el pico está en [lo, m]
    return lo
```

(En el script los arreglos son de base 0, así que `A[m]` aquí es `A[m-1]` allá.)

## Invariante

Dos hechos sobre los datos, que usa todo lo demás. Para `1 <= m < n`:

- **H1.** Si `m < p`, entonces `A[m] < A[m+1]`: ambos están en la parte creciente `A[1..p]`.
- **H2.** Si `m >= p`, entonces `A[m] > A[m+1]`: ambos están en la parte decreciente `A[p..n]`.

Como los valores son distintos, `A[m] < A[m+1]` o `A[m] > A[m+1]`, y por H1 y H2:

> `A[m] < A[m+1]` si y solo si `m < p`.

**Invariante.** Cada vez que se evalúa la guarda del `while`:

`1 <= lo <= hi <= n` y `lo <= p <= hi`.

**Inicialización.** Con `lo = 1` y `hi = n`: `1 <= 1 <= n <= n` y `p ∈ [1, n]` por la definición de `p`.

**Mantenimiento.** Entramos con `lo < hi`, así que `lo <= m < hi` y `A[m+1]` existe.

- **Caso `A[m] < A[m+1]`.** Por la equivalencia, `m < p`, es decir `p >= m + 1`. El nuevo `lo = m + 1` cumple `lo <= p` por esto, y `lo <= hi` porque `m < hi`. Lo recién descartado, `[lo, m]`, no contiene a `p`, y eso se justifica con las propiedades de los datos (H1). El resto, `p <= hi` y `hi <= n`, se mantiene por hipótesis.
- **Caso `A[m] > A[m+1]`.** (Es el único otro, por valores distintos.) Por la equivalencia, `m >= p`. El nuevo `hi = m` cumple `p <= hi` por esto, y `lo <= hi` porque `m >= lo`. Lo recién descartado, `[m+1, hi]`, no contiene a `p` (H2). El resto se mantiene por hipótesis. ∎

**Corolario (a la salida).** Al salir, `lo >= hi`; con el invariante, `lo = hi`. Como `lo <= p <= hi`, resulta `p = lo`.

**Terminación (potencial).** `Φ = hi - lo` es un entero `>= 0` por el invariante, y baja en cada vuelta:

- con `lo = m + 1`: `hi - (m + 1) < hi - lo`, porque `m >= lo`;
- con `hi = m`: `m - lo < hi - lo`, porque `m < hi`.

Un entero no negativo no puede bajar para siempre, así que el ciclo termina.

## Correctitud

Corolario y terminación juntos dan la correctitud total: para toda entrada válida el algoritmo termina y devuelve `p`. ∎

## Complejidad

**Vueltas.** Sea `s = hi - lo + 1` el número de candidatos. Al principio `s = n`. Como `m - lo + 1 = ⌊(hi - lo)/2⌋ + 1 = ⌈s/2⌉`:

- si `hi = m`, quedan `⌈s/2⌉` candidatos;
- si `lo = m + 1`, quedan `⌊s/2⌋`.

En ambos casos `s' <= ⌈s/2⌉`. Por inducción, después de `k` comparaciones `s <= ⌈n / 2^k⌉`, porque `⌈⌈n / 2^{k-1}⌉ / 2⌉ = ⌈n / 2^k⌉`. El ciclo termina cuando `s = 1`, y eso pasa en cuanto `2^k >= n`.

**Total: a lo sumo `⌈log₂ n⌉` comparaciones**, una por vuelta. El tiempo es `O(log n)` y la memoria extra es `O(1)`: `lo`, `hi`, `m`. Como la sección siguiente demuestra que ningún algoritmo puede hacer menos de `⌈log₂ n⌉`, en el peor caso este hace exactamente `⌈log₂ n⌉`.

## Casos de prueba

| Caso | A | pico (base 1) | comparaciones | ⌈log₂ n⌉ |
|---|---|---|---|---|
| n = 1 | [7] | 1 | 0 | 0 |
| n = 2, sube | [1, 2] | 2 | 1 | 1 |
| n = 2, baja | [2, 1] | 1 | 1 | 1 |
| n = 3, pico al medio | [3, 9, 8] | 2 | 2 | 2 |
| solo creciente | [1, 2, 3, 4, 5] | 5 | 2 | 3 |
| solo decreciente | [5, 4, 3, 2, 1] | 1 | 3 | 3 |
| n = 7, pico en 4 | [2, 5, 9, 14, 11, 7, 3] | 4 | 3 | 3 |
| n = 8, pico en 4 | [1, 3, 5, 7, 6, 4, 2, 0] | 4 | 3 | 3 |
| n = 8, pico en 8 | [1, 2, 3, 4, 5, 6, 7, 8] | 8 | 3 | 3 |
| n = 10, pico en 3 | [1, 9, 20, 15, 14, 12, 8, 5, 3, 2] | 3 | 3 | 4 |

Traza sobre `A = [2, 5, 9, 14, 11, 7, 3]`:

| [lo, hi] | m | comparación | resultado |
|---|---|---|---|
| [1, 7] | 4 | A[4]=14 < A[5]=11 | no → hi = m |
| [1, 4] | 2 | A[2]=5 < A[3]=9 | sí → lo = m + 1 |
| [3, 4] | 3 | A[3]=9 < A[4]=14 | sí → lo = m + 1 |
| [4, 4] | — | fin: p = 4 | — |

Peor caso por búsqueda exhaustiva¹ (todos los órdenes unimodales posibles):

| n | entradas | peor caso observado | ⌈log₂ n⌉ |
|---|---|---|---|
| 1 | 1 | 0 | 0 |
| 2 | 2 | 1 | 1 |
| 3 | 4 | 2 | 2 |
| 4 | 8 | 2 | 2 |
| 5 | 16 | 3 | 3 |
| 6 | 32 | 3 | 3 |
| 7 | 64 | 3 | 3 |
| 8 | 128 | 3 | 3 |
| 9 | 256 | 4 | 4 |
| 10 | 512 | 4 | 4 |
| 11 | 1024 | 4 | 4 |
| 12 | 2048 | 4 | 4 |
| 13 | 4096 | 4 | 4 |
| 14 | 8192 | 4 | 4 |
| 15 | 16384 | 4 | 4 |
| 16 | 32768 | 4 | 4 |

## Cota inferior (información)

**Lema.** Un árbol binario de altura `h` tiene a lo sumo `2^h` hojas.

*Demostración.* Por inducción sobre `h`. Con `h = 0` es una sola hoja, `1 = 2^0`. Con `h > 0`, la raíz tiene a lo sumo dos subárboles de altura `<= h - 1`, con a lo sumo `2^{h-1}` hojas cada uno, y juntos `2 · 2^{h-1} = 2^h`. ∎

**Teorema.** Todo algoritmo de comparaciones que encuentre el máximo de un arreglo unimodal de `n` valores distintos hace, en el peor caso, al menos `⌈log₂ n⌉` comparaciones.

*Demostración.* El algoritmo es un árbol de decisión: cada nodo interno es una comparación `A[i] < A[j]` con dos ramas (los valores son distintos), cada hoja es una salida, y el costo en el peor caso es la altura. Da igual qué pares compare: solo se cuentan hojas. Dos pasos:

1. **La salida depende solo de la hoja.** El algoritmo nunca ve los valores, solo las respuestas, así que su salida es una posición, y dos entradas que reciben las mismas respuestas llegan a la misma hoja y dan la misma salida.
2. **Hay `n` entradas que necesitan salidas distintas.** Para cada `p ∈ [1, n]` sea `I_p` la entrada con `I_p[i] = i` si `i <= p` y `I_p[i] = -i` si `i > p`. Es unimodal con valores distintos: la parte `1, ..., p` crece, `I_p[p] = p > -(p+1) = I_p[p+1]`, y `-(p+1) > -(p+2) > ... > -n` decrece. Su pico es `p`. Si `I_p` e `I_q` con `p != q` llegaran a la misma hoja, el algoritmo daría la misma salida para las dos, y estaría mal en una.

Entonces el árbol tiene al menos `n` hojas. Por el lema, `n <= 2^h`, es decir `h >= ⌈log₂ n⌉`. ∎

**Coincidencia.** El algoritmo hace a lo sumo `⌈log₂ n⌉` comparaciones y todo algoritmo necesita al menos `⌈log₂ n⌉`. Entonces el costo exacto del problema en el peor caso es **`⌈log₂ n⌉`**, para todo `n >= 1`, y el algoritmo es óptimo. Por minimax sobre todos los algoritmos de comparaciones¹, el óptimo exacto para `n = 1..8` es `0, 1, 2, 2, 3, 3, 3, 3`.

¹ **Verificación en código** (`verificar_ejercicio_14.py`, Python 3, sin dependencias, generado con un LLLM a partir del pseudocódigo):

- Casos de prueba fijos y la traza: coinciden con las tablas de arriba.
- **Invariante y potencial ejecutables:** una versión instrumentada comprueba `1 <= lo <= hi <= n`, `lo <= p <= hi`, que `A[m] < A[m+1]` si y solo si `m < p`, y que `hi - lo` baja en cada vuelta. Pasó en todos los órdenes unimodales para `n <= 12`.
- **Búsqueda exhaustiva** (`n = 1..16`, hasta 32 768 entradas): la salida es siempre la posición del máximo y el peor caso es exactamente `⌈log₂ n⌉`.
- **Pruebas aleatorias** con valores reales distintos, `n = 10, 1000, 100000` (8300 arreglos): 0 errores, y el peor caso observado es `⌈log₂ n⌉` (4, 10 y 17).
- **Cota de información:** para `n = 1..40` las `n` entradas `I_p` son unimodales con pico en `p` y producen `n` secuencias de respuestas distintas, es decir `n` hojas distintas.
- **Óptimo exacto** por minimax sobre todos los algoritmos de comparaciones de cualquier par (`n = 1..8`): `0, 1, 2, 2, 3, 3, 3, 3`, igual a `⌈log₂ n⌉`.
- **Valores repetidos:** sobre los arreglos 0/1 no estrictamente unimodales (`n = 2..10`) el algoritmo falla en algunos (por ejemplo, 16 de 56 para `n = 10`). En la familia del adversario (ceros y un solo 1, con respuestas `<`, `=`, `>`), el óptimo exacto es `⌊n/2⌋` para `n = 1..8`, lo que sostiene el `Ω(n)` de Convenciones.
