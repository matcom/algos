# Ejercicio 07: mediana de dos arreglos ordenados

## Enunciado

Mediana de dos arreglos ordenados de largo `n`: el `n`-ésimo menor de los `2n` elementos. Diseña un algoritmo `O(log n)`, demuestra su correctitud y da la cota de información.

## Convenciones

- **Entrada:** `A[1..n]` y `B[1..n]`, ordenados de menor a mayor, con `n >= 1` y todos los valores distintos. (Si hubiera repetidos, se desempata poniendo los de `B` antes que los de `A` cuando son iguales: eso es lo que hace `<` en `P`. El valor devuelto es el mismo con cualquier desempate. Con repetidos, "los `n` menores" son los de ese orden y la salida como valor no cambia.)
- **Salida:** el `n`-ésimo menor de los `2n` elementos. Si se piensa en el modelo de abajo, la salida es una posición: `A[k]` o `B[k]`.
- **Modelo:** comparaciones. Los valores solo se conocen por preguntas `A[i] < B[j]`. Comparar dos elementos del mismo arreglo no aporta nada: su respuesta ya se sabe. Todo el cálculo con índices es gratis.
- **Costo:** el número de comparaciones `A[i] < B[j]` (y el `max` final, que es una comparación más). Cada una cuenta 1, con el resultado que tenga.
- **Centinelas:** `A[0] = B[0] = -∞` y `A[n+1] = B[n+1] = +∞`. Solo se usan en las definiciones; el algoritmo nunca los lee ni los compara.
- **Alcance de la cota:** la cota de información vale solo en este modelo.

## Idea

Sea `S` el conjunto de los `n` menores de los `2n` elementos. Como `A` y `B` están ordenados, `S` es un prefijo de `A` más un prefijo de `B`: `S = A[1..i] ∪ B[1..n-i]`. Hay una sola incógnita, `i ∈ [0, n]`. Una vez conocida, la mediana es el mayor elemento de `S`, es decir `max(A[i], B[n-i])`.

Para saber si un `i` es el correcto, no hace falta mirar todo: basta ver el borde entre lo que entra y lo que queda fuera. Defino

```
P(i) = A[i] < B[n - i + 1]      // 1 <= i <= n
P(0) = verdadero,  P(n+1) = falso
```

`P(i)` dice que lo último que tomamos de `A` es menor que lo primero que dejamos de `B`. Si `i` crece, `A[i]` crece y `B[n-i+1]` decrece, así que `P` es verdadero hasta cierto punto y falso después. Buscamos el último `i` verdadero, y eso es una búsqueda binaria.

## Algoritmo

```
mediana(A, B):                      // A[1..n], B[1..n] ordenados
    lo = 0
    hi = n
    while lo < hi:
        i = ⌈(lo + hi) / 2⌉          // lo < i <= hi, luego 1 <= i <= n
        if A[i] < B[n - i + 1]:      // 1 comparación: P(i)
            lo = i
        else:
            hi = i - 1
    // aquí lo = hi
    i = lo
    if i == 0:
        return B[n]
    if i == n:
        return A[n]
    return max(A[i], B[n - i])       // 1 comparación
```

(En el script los arreglos son de base 0, así que `A[i]` aquí es `A[i-1]` allá.)

## Invariante

Sea `i*` el mayor `i ∈ [0, n]` con `P(i)`. Existe porque `P(0)` es verdadero.

**Lema 1 (monotonía).** Si `P(i)` y `0 <= i' <= i`, entonces `P(i')`. Por tanto, para `0 <= i <= n + 1`: `P(i)` si y solo si `i <= i*`.

*Demostración.* Con `i' = 0` es la convención. Con `1 <= i' <= i <= n`:

`A[i'] <= A[i] < B[n-i+1] <= B[n-i'+1]`

porque `A` está ordenado, vale `P(i)`, y `n - i + 1 <= n - i' + 1` con `B` ordenado. Entonces `A[i'] < B[n-i'+1]`. ∎

**Invariante.** Cada vez que se evalúa la guarda del `while`:

`0 <= lo <= hi <= n`, y `lo <= i* <= hi`.

Por el Lema 1, esto equivale a `P(lo)` y no `P(hi + 1)`, que es la forma que se usa abajo.

**Inicialización.** Con `lo = 0` y `hi = n`: `0 <= 0 <= n <= n`, `P(0)` es verdadero y `P(n+1)` es falso por convención.

**Mantenimiento.** La guarda es `lo < hi`. Con `i = ⌈(lo + hi)/2⌉` se cumple `lo < i <= hi`, así que `1 <= i <= n` y `B[n-i+1]` existe. El `if` pregunta justo `P(i)`.

- **Caso `P(i)`:** se hace `lo = i`. El nuevo `P(lo)` es verdadero por el `if`. Se mantiene `no P(hi+1)` por hipótesis, y `lo = i <= hi` por la elección de `i`.
- **Caso `no P(i)`:** se hace `hi = i - 1`. El nuevo `no P(hi+1)` es `no P(i)`, verdadero por el `if`. Se mantiene `P(lo)` por hipótesis, y `lo <= i - 1 = hi` porque `i > lo`. ∎

**Corolario (a la salida).** Al salir, `lo >= hi`; con el invariante, `lo = hi`. Como `lo <= i* <= hi`, resulta `lo = i*`.

**Terminación (potencial).** `Φ = hi - lo` es un entero `>= 0` por el invariante, y baja en cada vuelta: con `P(i)`, `hi - i < hi - lo` porque `i > lo`; con `no P(i)`, `(i - 1) - lo < hi - lo` porque `i <= hi`. Como no puede bajar para siempre, el ciclo termina.

## Correctitud

**Lema 2.** Con `i = i*`, el conjunto `S = A[1..i] ∪ B[1..n-i]` (que tiene `n` elementos) es exactamente el conjunto de los `n` menores.

*Demostración.* Basta ver que todo elemento de `S` es menor que todo elemento de fuera, `A[i+1..n] ∪ B[n-i+1..n]`. Hay cuatro pares:

- **`A` de `S` contra `A` de fuera:** por `A` ordenado.
- **`B` de `S` contra `B` de fuera:** por `B` ordenado.
- **`A` de `S` contra `B` de fuera:** si `i >= 1`, `P(i)` da `A[i] < B[n-i+1]`, y como `A[i]` es el mayor del prefijo y `B[n-i+1]` el menor del resto, vale para todos. Si `i = 0` no hay elementos de `A` en `S`.
- **`B` de `S` contra `A` de fuera:** si `i + 1 <= n`, por el Lema 1 `no P(i+1)`, es decir `no (A[i+1] < B[n-i])`, y con valores distintos, `B[n-i] < A[i+1]`; vale para todos por el mismo argumento. Si `i = n` no hay `A` fuera. ∎

**Postcondición.** El `n`-ésimo menor es el mayor de los `n` menores, o sea el máximo de `S`. Como cada prefijo está ordenado, su máximo es el último elemento:

- Si `i = 0`, `S = B[1..n]` y el máximo es `B[n]`.
- Si `i = n`, `S = A[1..n]` y el máximo es `A[n]`.
- Si `1 <= i <= n - 1`, ambos prefijos son no vacíos y el máximo es `max(A[i], B[n-i])`.

El algoritmo devuelve exactamente eso, con `i = i*` por el corolario del invariante. Con la terminación, queda demostrada la correctitud total. ∎

## Complejidad

**Vueltas.** Sea `s = hi - lo + 1` el número de candidatos. Al principio `s = n + 1`. Con `lo < hi`, `i - lo = ⌊s/2⌋`, así que:

- **`P(i)`:** `lo = i`, y `s' = hi - i + 1 = s - ⌊s/2⌋ = ⌈s/2⌉`.
- **`no P(i)`:** `hi = i - 1`, y `s' = i - lo = ⌊s/2⌋`.

En ambos casos `s' <= ⌈s/2⌉`. Después de `k` vueltas `s <= ⌈(n+1)/2^k⌉`, y el ciclo termina cuando `s = 1`. Entonces hay a lo sumo `⌈log₂(n+1)⌉` vueltas, y cada una hace una comparación.

**Total:** a lo sumo `⌈log₂(n+1)⌉ + 1` comparaciones (la `+1` es el `max` final, que no hace falta si `i = 0` o `i = n`), que es **`O(log n)`**. El tiempo es `O(log n)` y la memoria extra es `O(1)`: `lo`, `hi`, `i`. Comparar con `Θ(n)` de mezclar los dos arreglos.

## Casos de prueba

| Caso | A | B | i | mediana | comparaciones |
|---|---|---|---|---|---|
| n = 1, A < B | [1] | [2] | 1 | 1 | 1 |
| n = 1, B < A | [2] | [1] | 0 | 1 | 1 |
| n = 2, A < B | [1, 2] | [3, 4] | 2 | 2 | 2 |
| n = 2, B < A | [3, 4] | [1, 2] | 0 | 2 | 1 |
| n = 2, intercaladas | [1, 3] | [2, 4] | 1 | 2 | 3 |
| n = 3, intercaladas | [1, 3, 5] | [2, 4, 6] | 2 | 3 | 3 |
| n = 4, mediana en A | [1, 2, 3, 10] | [4, 5, 6, 7] | 3 | 4 | 4 |
| n = 5, mediana en B | [1, 2, 3, 4, 20] | [5, 6, 7, 8, 9] | 4 | 5 | 4 |
| n = 6, mezcla | [2, 4, 6, 8, 10, 12] | [1, 3, 5, 7, 9, 11] | 3 | 6 | 4 |
| n = 7, A grande | [11, 12, 13, 14, 15, 16, 17] | [1, 2, 3, 4, 5, 6, 7] | 0 | 7 | 3 |

Traza sobre `A = [1, 3, 5, 7, 9, 11, 13]`, `B = [2, 4, 6, 8, 10, 12, 14]`:

| [lo, hi] | i | comparación | ¿cierto? |
|---|---|---|---|
| [0, 7] | 4 | A[4]=7 < B[4]=8 | sí |
| [4, 7] | 6 | A[6]=11 < B[2]=4 | no |
| [4, 5] | 5 | A[5]=9 < B[3]=6 | no |
| [4, 4] | — | fin: i* = 4 | — |

Los 4 elementos de `A` y los 3 de `B` que forman `S` son `1, 3, 5, 7` y `2, 4, 6`. La mediana es `max(A[4], B[3]) = max(7, 6) = 7`, que es el 7.º menor de 14.

Búsqueda exhaustiva¹ (todas las intercalaciones):

| n | entradas | peor caso observado | ⌈log₂(n+1)⌉ + 1 | ⌈log₂ 2n⌉ |
|---|---|---|---|---|
| 1 | 2 | 1 | 2 | 1 |
| 2 | 6 | 3 | 3 | 2 |
| 3 | 20 | 3 | 3 | 3 |
| 4 | 70 | 4 | 4 | 3 |
| 5 | 252 | 4 | 4 | 4 |
| 6 | 924 | 4 | 4 | 4 |
| 7 | 3432 | 4 | 4 | 4 |
| 8 | 12870 | 5 | 5 | 4 |
| 9 | 48620 | 5 | 5 | 5 |

## Cota de información

**Teorema.** Todo algoritmo de comparaciones que encuentre el `n`-ésimo menor de dos arreglos ordenados de largo `n`, con valores distintos, hace en el peor caso al menos `⌈log₂ 2n⌉ = ⌈log₂ n⌉ + 1` comparaciones.

*Demostración.* El algoritmo es un árbol de decisión: cada nodo interno es una comparación `A[i] < B[j]` con dos ramas (los valores son distintos), y el costo en el peor caso es la altura. Las comparaciones dentro de un mismo arreglo no ramifican, así que no cambian ni las hojas ni la altura. Dos pasos:

1. **La salida depende solo de la hoja.** El algoritmo solo ve las respuestas, así que su salida es una posición (`A[k]` o `B[k]`), y dos entradas que reciben las mismas respuestas llegan a la misma hoja y dan la misma salida.
2. **Las `2n` posiciones pueden ser la mediana, así que hay al menos `2n` hojas.** Para que `A[k]` sea el `n`-ésimo menor tomamos la intercalación (patrón de orden creciente, `A` y `B` marcan de qué arreglo viene cada elemento)

   `A^{k-1} B^{n-k} A A^{n-k} B^{k}`

   Los primeros `n - 1` lugares tienen `k - 1` elementos de `A` y `n - k` de `B`, el lugar `n` es el `k`-ésimo de `A`, y en total hay `n` de cada uno. Para `B[k]` se intercambian las letras. Entonces las `2n` salidas ocurren, cada una necesita su hoja, y el árbol tiene al menos `2n` hojas.

Un árbol binario de altura `h` tiene a lo sumo `2^h` hojas (se prueba por inducción sobre `h`), así que `2^h >= 2n` y `h >= ⌈log₂ 2n⌉`. ∎

**Comparación con el algoritmo.** El algoritmo hace a lo sumo `⌈log₂(n+1)⌉ + 1` comparaciones y la cota es `⌈log₂ n⌉ + 1`. Coinciden salvo cuando `n` es potencia de 2 (con `n >= 2`), y ahí el algoritmo hace una más. Por tanto `Θ(log n)` es óptimo en este modelo, con una brecha de a lo sumo 1.

**Qué tan buena es la cota.** Por minimax sobre todos los algoritmos de comparaciones¹, el óptimo exacto para `n = 1..5` es `1, 2, 3, 3, 4`, igual a `⌈log₂ 2n⌉`: en esos tamaños la cota de información es exacta. No afirmo que lo sea para todo `n`.

¹ **Verificación en código** (`verificar_ejercicio_07.py`, Python 3, sin dependencias, generado por un LLM a partir del pseudocódigo):

- Casos de prueba fijos y la traza: coinciden con las tablas de arriba.
- **Invariante y potencial ejecutables:** una versión instrumentada comprueba `0 <= lo <= hi <= n`, `P(lo)`, `no P(hi+1)`, que `hi - lo` baja en cada vuelta, y que `S` es el conjunto de los `n` menores. Pasó en todas las intercalaciones para `n <= 9`.
- **Búsqueda exhaustiva** (`n = 1..9`, hasta 48 620 entradas): la salida es siempre `sorted(A + B)[n-1]` y las comparaciones nunca superan `⌈log₂(n+1)⌉ + 1`.
- **Pruebas aleatorias** contra `sorted` con `n = 10, 100, 1000, 20000` (12 300 entradas, con casos extremos `A < B` y `B < A`): 0 errores.
- **Cota de información:** el número de salidas distintas es exactamente `2n` para `n = 1..9`, y el patrón de intercalación de arriba hace de `A[k]` la mediana para todo `k`.
- **Óptimo exacto** por minimax sobre todos los árboles de decisión de comparaciones `A[i] < B[j]` para `n = 1..5`: `1, 2, 3, 3, 4`. Nuestro algoritmo hace `1, 3, 3, 4, 4` en el peor caso.
