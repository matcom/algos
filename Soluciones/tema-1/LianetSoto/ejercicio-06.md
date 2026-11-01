# Ejercicio 6 — Buscar en una matriz con filas y columnas ordenadas

> ★★ Una matriz n × n tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor x en O(n) comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en o(n). (C3, C5)

---

## 1. El problema y su especificación

**Problema.** Dada una matriz `A` de `n × n` enteros, con la propiedad de que cada fila está ordenada de forma no decreciente de izquierda a derecha y cada columna está ordenada de forma no decreciente de arriba a abajo, decidir si un valor `x` aparece en `A`.

**Modelo.** Comparaciones entre `x` y elementos de `A`. Cada comparación devuelve uno de tres signos: `<`, `=`, `>`. Contamos el número de comparaciones en el peor caso.

**Especificación (contrato).**

- **Precondición.** `A` es una matriz `n × n` de enteros tal que:
  - para todo `i` y todo `j < n-1`: `A[i][j] ≤ A[i][j+1]` (filas ordenadas),
  - para todo `j` y todo `i < n-1`: `A[i][j] ≤ A[i+1][j]` (columnas ordenadas).
- **Postcondición.** El valor devuelto `r` cumple:
  - `r = True` y existe `(i, j)` con `A[i][j] = x`, o
  - `r = False` y no existe `(i, j)` con `A[i][j] = x`.

**Ejemplo de matriz válida (n = 5):**

```text
      j=0   j=1   j=2   j=3   j=4
    +-----+-----+-----+-----+-----+
i=0 |  1  |  4  |  7  | 11  | 15  |
    +-----+-----+-----+-----+-----+
i=1 |  2  |  5  |  8  | 12  | 19  |
    +-----+-----+-----+-----+-----+
i=2 |  3  |  6  |  9  | 16  | 22  |
    +-----+-----+-----+-----+-----+
i=3 | 10  | 13  | 14  | 17  | 24  |
    +-----+-----+-----+-----+-----+
i=4 | 18  | 21  | 23  | 26  | 30  |
    +-----+-----+-----+-----+-----+
```


---

## 2. Primeras ideas y por qué no alcanzan

| Estrategia | Tiempo | Problema |
|---|---|---|
| Recorrer las `n²` celdas | `Θ(n²)` | Demasiado lento para matrices grandes. |
| Búsqueda binaria en cada fila | `O(n log n)` | No usa la propiedad de las columnas, y `n log n` es `ω(n)`. |
| **Desde la esquina superior derecha** | **`O(n)`** | **La solución que vamos a construir.** |

La idea clave es que la esquina **superior derecha** tiene una propiedad especial: es el **máximo de su fila** y el **mínimo de su columna**. Si comparamos `x` con `A[0][n-1]`:

- Si `x = A[0][n-1]`, ya está.
- Si `x < A[0][n-1]`, entonces `x` no puede estar en la **columna** `n-1` (porque todos los elementos de esa columna son `≥ A[0][n-1] > x`). Podemos **descartar la columna** `n-1` y movernos a la izquierda.
- Si `x > A[0][n-1]`, entonces `x` no puede estar en la **fila** `0` (porque todos los elementos de esa fila son `≤ A[0][n-1] < x`). Podemos **descartar la fila** `0` y movernos hacia abajo.

En cada paso descartamos **una fila o una columna completa**. Como hay `n` filas y `n` columnas, después de a lo sumo `2n − 1` pasos no queda nada por descartar, y la respuesta es `False` (o encontramos `x` antes).

---

## 3. El algoritmo

```python
def buscar_en_matriz(A, x):
    """Devuelve True si x está en A, False si no.
       A es n×n con filas y columnas ordenadas de forma no decreciente."""
    n = len(A)
    if n == 0:
        return False
    i, j = 0, n - 1          # empezamos en la esquina superior derecha
    while i < n and j >= 0:
        if A[i][j] == x:
            return True
        elif A[i][j] > x:
            j -= 1           # descartamos la columna j
        else:
            i += 1           # descartamos la fila i
    return False
```


### 3.1. Traza sobre el ejemplo

Buscamos `x = 16` en la matriz de la sección 1.

```text
inicio: i=0, j=4, A[0][4]=15
```

| Paso | `i` | `j` | `A[i][j]` | Comparación | Acción | Celdas descartadas |
|---:|---:|---:|---:|---|---|---|
| 1 | 0 | 4 | 15 | `15 < 16` | `i = 1` | fila 0 |
| 2 | 1 | 4 | 19 | `19 > 16` | `j = 3` | columna 4 |
| 3 | 1 | 3 | 12 | `12 < 16` | `i = 2` | fila 1 |
| 4 | 2 | 3 | 16 | `16 == 16` | **encontrado** | — |

**4 comparaciones**, y `x = 16` está en `A[2][3]`. ✔

Buscamos `x = 20` (no está):

| Paso | `i` | `j` | `A[i][j]` | Comparación | Acción | Celdas descartadas |
|---:|---:|---:|---:|---|---|---|
| 1 | 0 | 4 | 15 | `15 < 20` | `i = 1` | fila 0 |
| 2 | 1 | 4 | 19 | `19 < 20` | `i = 2` | fila 1 |
| 3 | 2 | 4 | 22 | `22 > 20` | `j = 3` | columna 4 |
| 4 | 2 | 3 | 16 | `16 < 20` | `i = 3` | fila 2 |
| 5 | 3 | 3 | 17 | `17 < 20` | `i = 4` | fila 3 |
| 6 | 4 | 3 | 26 | `26 > 20` | `j = 2` | columna 3 |
| 7 | 4 | 2 | 23 | `23 > 20` | `j = 1` | columna 2 |
| 8 | 4 | 1 | 21 | `21 > 20` | `j = 0` | columna 1 |
| 9 | 4 | 0 | 18 | `18 < 20` | `i = 5` | fila 4 |
| 10 | 5 | 0 | — | `i == n` | **False** | — |

**9 comparaciones** (`2n − 1 = 9`), y `x = 20` no está. ✔

### 3.2. El camino sobre la matriz

El algoritmo recorre un camino que **baja y va a la izquierda**. Nunca sube ni va a la derecha.

```text
      j=0   j=1   j=2   j=3   j=4
    +-----+-----+-----+-----+-----+
i=0 |  1  |  4  |  7  | 11  | 15  |  ← inicio (0,4)
    +-----+-----+-----+-----+-----+
i=1 |  2  |  5  |  8  | 12  | 19  |  ← paso 2 (1,4), paso 3 (1,3)
    +-----+-----+-----+-----+-----+
i=2 |  3  |  6  |  9  | 16  | 22  |  ← paso 4 (2,3) ¡encontrado!
    +-----+-----+-----+-----+-----+
i=3 | 10  | 13  | 14  | 17  | 24  |
    +-----+-----+-----+-----+-----+
i=4 | 18  | 21  | 23  | 26  | 30  |
    +-----+-----+-----+-----+-----+
```

Para `x = 16`, el camino es `(0,4) → (1,4) → (1,3) → (2,3)`. En cada paso, o bajamos (descartamos una fila) o vamos a la izquierda (descartamos una columna). El número de pasos es a lo sumo `n + n − 1 = 2n − 1`.

---

## 4. Correctitud parcial: el invariante

### 4.1. Enunciado del invariante

> **Invariante `I(i, j)`.** Si `x` está en `A`, entonces `x` está en la submatriz `A[i..n-1][0..j]`, es decir, en las filas `i` a `n-1` y las columnas `0` a `j`.

Dicho de otra forma: **todo lo que está por encima de la fila `i` o a la derecha de la columna `j` ya fue descartado**, y `x` no puede estar ahí.

### 4.2. Inicialización

Antes de la primera vuelta, `i = 0` y `j = n-1`. La submatriz `A[0..n-1][0..n-1]` es la matriz entera. Si `x` está en `A`, trivialmente está en la matriz entera. ✔

### 4.3. Mantenimiento

Supongamos `I(i, j)` y que `i < n`, `j >= 0`. Sea `v = A[i][j]`. Hay tres casos:

**Caso 1: `v == x`.** El algoritmo devuelve `True`, y la postcondición se cumple en el acto. ✔

**Caso 2: `v > x`.** Como la columna `j` está ordenada de arriba a abajo, para todo `k ≥ i` se tiene `A[k][j] ≥ A[i][j] = v > x`. Así que **ningún elemento de la columna `j` en las filas `i..n-1` puede ser `x`**. El algoritmo hace `j = j - 1`, y la nueva submatriz `A[i..n-1][0..j-1]` contiene a `x` si la vieja lo contenía, porque la única parte que quitamos es la columna `j`, que ya descartamos. ✔

**Caso 3: `v < x`.** Como la fila `i` está ordenada de izquierda a derecha, para todo `k ≤ j` se tiene `A[i][k] ≤ A[i][j] = v < x`. Así que **ningún elemento de la fila `i` en las columnas `0..j` puede ser `x`**. El algoritmo hace `i = i + 1`, y la nueva submatriz `A[i+1..n-1][0..j]` contiene a `x` si la vieja lo contenía, porque la única parte que quitamos es la fila `i`, que ya descartamos. ✔

En los tres casos, el invariante se mantiene.

### 4.4. Conclusión

Cuando el bucle termina, `i == n` o `j < 0`. La submatriz `A[i..n-1][0..j]` es vacía (no tiene filas si `i == n`, o no tiene columnas si `j < 0`). Por el invariante, si `x` estuviera en `A`, estaría en esa submatriz vacía, lo cual es imposible. Por tanto, `x` no está en `A`, y devolver `False` es correcto. ✔

**Conclusión de la correctitud parcial:** si el algoritmo termina, la salida es correcta.

---

## 5. Terminación: el potencial

### 5.1. Enunciado del potencial

> **Potencial `Φ(i, j) = (n - i) + (j + 1)`.**

Es el número de filas que quedan por descartar (`n - i`) más el número de columnas que quedan por descartar (`j + 1`).

**Propiedades.**

- `Φ ≥ 0` siempre, porque `i ≤ n` y `j ≥ -1` en todo momento.
- Antes de la primera vuelta, `Φ = n + n = 2n`.
- Cada vuelta que no devuelve reduce `Φ` **estrictamente** en 1.

### 5.2. Por qué baja

- Si `v > x`, el algoritmo hace `j = j - 1`. El nuevo potencial es `(n - i) + ((j-1) + 1) = (n - i) + j = Φ - 1`. ✔
- Si `v < x`, el algoritmo hace `i = i + 1`. El nuevo potencial es `(n - (i+1)) + (j + 1) = (n - i - 1) + (j + 1) = Φ - 1`. ✔

En ambos casos, `Φ` baja exactamente en 1. Como `Φ` es un entero no negativo que baja en cada vuelta, el ciclo termina. Además, el número de vueltas es a lo sumo `Φ₀ = 2n`, así que el algoritmo hace **a lo sumo `2n` comparaciones** (en realidad `2n − 1`, porque cuando `Φ = 1` y no encuentra `x`, la siguiente vuelta hace `i = n` o `j = -1` y termina; la comparación de esa última vuelta es la número `2n − 1`).

**Conclusión de la terminación:** el algoritmo termina para toda entrada que cumpla la precondición. ✔

**Correctitud total:** correctitud parcial (sección 4) + terminación (sección 5). ✔

---

## 6. Costo

**Tiempo.** Cada vuelta hace **una comparación** y **una** operación de avance (`i += 1` o `j -= 1`). El número de vueltas es a lo sumo `2n - 1`, porque cada vuelta descarta al menos una fila o una columna, y hay `n` filas y `n` columnas. Por tanto:

```text
T(n) = O(n) comparaciones
```

**Memoria.** Dos índices `i` y `j`: `O(1)` memoria extra.

**Comparación con las alternativas.**

| Algoritmo | Comparaciones en el peor caso | Memoria |
|---|---|---|
| Fuerza bruta (recorrer todo) | `n²` | `O(1)` |
| Búsqueda binaria en cada fila | `n · ⌈log₂ n⌉` | `O(1)` |
| **Esquina superior derecha** | **`2n − 1`** | **`O(1)`** |

Para `n = 1000`:

- Fuerza bruta: `1 000 000` comparaciones.
- Búsqueda binaria por fila: `10 000` comparaciones.
- **Esquina superior derecha: `1 999` comparaciones.**

La diferencia es de tres órdenes de magnitud frente a la fuerza bruta, y de un factor `log n` frente a la búsqueda binaria por fila.

---

## 7. Cota mínima: `Ω(n)` con un adversario

### 7.1. El teorema

**Teorema.** Cualquier algoritmo de comparaciones que decida si `x` está en una matriz `n × n` con filas y columnas ordenadas necesita, en el peor caso, al menos `n` comparaciones.


### 7.2. La estrategia del adversario

Trabajamos con el caso particular `x = 1`. Para cada `k ∈ {0, …, n−1}`, definimos la matriz `N_k`:

```text
            ⎧ 0   si  i + j < k
N_k[i][j] = ⎨ 1   si  i + j = k
            ⎩ 2   si  i + j > k
```


Cada `N_k` tiene filas y columnas no decrecientes, y el valor 1 aparece exactamente en la anti-diagonal `i+j = k`. También definimos `M_k` como la misma matriz pero con 2 en toda la anti-diagonal `i+j = k` (es decir, `M_k` no contiene ningún 1). Ambas son válidas.

```text
            ⎧ 0   si  i + j < k
M_k[i][j] = ⎨ 2   si  i + j ≥ k
            ⎩ 
```

El adversario mantiene un conjunto `K ⊆ {0, …, n−1}` de anti-diagonales posibles, inicialmente `K = {0, …, n−1}`. Cuando el algoritmo consulta la celda `(i, j)`, el adversario responde de la siguiente manera:

    - Si i+j < min(K): responde 0. Esta respuesta es consistente con todas las matrices para k ∈ K.
    
    - Si i+j > max(K): responde 2. Consistente con todas las matrices para k ∈ K.

    - Si i+j ∈ K (es decir, i+j = k para algún k ∈ K): responde 0 y actualiza el conjunto eliminando todas las anti-diagonales menores o iguales a k. Es decir, K = { k' ∈ K | k' > k }.

**¿Por qué esta respuesta es consistente?** Si el adversario responde 0 en la celda `(i, j)` donde `i+j = k`, la respuesta `0` es consistente con cualquier matriz `N_{k'}` o `M_{k'}` tal que `i+j < k'` (porque en esas matrices, los valores por debajo de la anti-diagonal `k'` son `0`). Por tanto, el verdadero `k'` debe ser estrictamente mayor que `k`. Las opciones `k' ≤ k` quedan descartadas y se eliminan de `K`.

Cada vez que el algoritmo consulta una celda con `i+j ∈ K`, el tamaño del conjunto K disminuye en al menos 1. Las consultas con `i+j < min(K)` o `i+j > max(K)` no eliminan ningún elemento de `K`.

### 7.3. Por qué fuerza n comparaciones

Si el algoritmo hiciera `q < n` comparaciones y terminara, como `K` empezó con `n` elementos y cada comparación elimina a lo sumo un elemento de `K`, quedaría al menos un `k* ∈ K` que no fue eliminado.

Ese `k*` no fue consultado en su anti-diagonal: si el algoritmo hubiera consultado alguna celda con `i+j = k*`, el adversario habría actualizado `K` y habría eliminado `k*` (junto con todos los menores). Por tanto, para todas las celdas consultadas por el algoritmo, `i+j ≠ k*`.

Ahora consideramos las dos matrices `N_{k*}` y `M_{k*}`. Para toda celda consultada `(i, j)`:

    Si i+j < k*, tanto N_{k*} como M_{k*} valen 0, que es lo que respondió el adversario (porque k* ∈ K y i+j < min(K) ≤ k*).

    Si i+j > k*, tanto N_{k*} como M_{k*} valen 2, que es lo que respondió el adversario (porque i+j > max(K) ≥ k*).

    La celda con i+j = k* no fue consultada.

Por tanto, el algoritmo recibe exactamente las mismas respuestas sobre `N_{k*}` y sobre `M_{k*}`, y devuelve la misma salida en ambos casos. Pero la salida correcta es distinta: en `N_{k*}` el valor 1 está presente (en la anti-diagonal `k*`), y en `M_{k*}` no está. Así que el algoritmo se equivoca en al menos una de las dos matrices. Contradicción.

Por tanto, cualquier algoritmo correcto necesita al menos n comparaciones. ∎

### 7.4. La cota es ajustada en orden de magnitud

El algoritmo de la sección 3 hace a lo sumo `2n − 1` comparaciones. La cota inferior demuestra que cualquier algoritmo correcto necesita al menos n comparaciones. Por tanto:
```text
Ω(n) ≤ costo del problema ≤ O(n).
```

El algoritmo de la esquina superior derecha es óptimo en orden de magnitud: no se puede resolver en `o(n)` comparaciones. La constante exacta no importa para este ejercicio.

---

## 8. Verificación experimental

### 8.1. Comparación contra fuerza bruta

```python
import random

def buscar_fuerza_bruta(A, x):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] == x:
                return True
    return False


def matriz_ordenada(n, rng):
    """Genera una matriz n×n con filas y columnas no decrecientes."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                A[i][j] = rng.randint(0, 5)
            elif i == 0:
                A[i][j] = A[i][j-1] + rng.randint(0, 5)
            elif j == 0:
                A[i][j] = A[i-1][j] + rng.randint(0, 5)
            else:
                A[i][j] = max(A[i-1][j], A[i][j-1]) + rng.randint(0, 5)
    return A


rng = random.Random(2026)
casos = 0
for _ in range(2000):
    n = rng.randint(1, 12)
    A = matriz_ordenada(n, rng)
    # probamos todos los valores en un rango amplio
    for x in range(-2, 100):
        assert buscar_en_matriz(A, x) == buscar_fuerza_bruta(A, x), \
            f"Fallo con n={n}, x={x}, A={A}"
        casos += 1

print(f"{casos} consultas comparadas con fuerza bruta: sin fallos")
```

```text
204000 consultas comparadas con fuerza bruta: sin fallos
```

### 8.2. Conteo de comparaciones

Instrumentamos el algoritmo para contar comparaciones y verificamos que nunca pasa de `2n − 1`.

```python
def buscar_contando(A, x):
    n = len(A)
    i, j = 0, n - 1
    comparaciones = 0
    while i < n and j >= 0:
        comparaciones += 1
        if A[i][j] == x:
            return True, comparaciones
        elif A[i][j] > x:
            j -= 1
        else:
            i += 1
    return False, comparaciones


rng = random.Random(7)
peor = {}
for _ in range(3000):
    n = rng.randint(1, 20)
    A = matriz_ordenada(n, rng)
    for x in range(-2, 200):
        _, c = buscar_contando(A, x)
        peor[n] = max(peor.get(n, 0), c)

print(f"{'n':>3} {'peor medido':>12} {'2n-1':>6} {'coincide':>10}")
for n in sorted(peor):
    print(f"{n:>3} {peor[n]:>12} {2*n-1:>6} {str(peor[n] <= 2*n-1):>10}")
```

```text
  n  peor medido   2n-1  coincide
  1            1      1      True
  2            3      3      True
  3            5      5      True
  4            7      7      True
  5            9      9      True
  6           11     11      True
  7           13     13      True
  8           15     15      True
  9           17     17      True
 10           19     19      True
 11           21     21      True
 12           23     23      True
 13           25     25      True
 14           27     27      True
 15           29     29      True
 16           31     31      True
 17           33     33      True
 18           35     35      True
 19           37     37      True
 20           39     39      True
```

El peor caso medido coincide exactamente con `2n − 1` para todo `n`. La cota `O(n)` es ajustada en la constante 2.

### 8.3. La matriz que fuerza `2n − 1` comparaciones

Busquemos `x = 22` (que no está en la matriz):


```text
      j=0   j=1   j=2   j=3   j=4
    +-----+-----+-----+-----+-----+
i=0 |  1  | 10  | 20  | 30  | 40  |
    +-----+-----+-----+-----+-----+
i=1 |  5  | 15  | 25  | 35  | 45  |
    +-----+-----+-----+-----+-----+
i=2 |  9  | 19  | 29  | 39  | 49  |
    +-----+-----+-----+-----+-----+
i=3 | 13  | 23  | 33  | 43  | 53  |
    +-----+-----+-----+-----+-----+
i=4 | 17  | 27  | 37  | 47  | 57  |
    +-----+-----+-----+-----+-----+
```

Traza del algoritmo:

| Paso | `i` | `j` | `A[i][j]` | Acción |
|---:|---:|---:|---:|---|
| 1 | 0 | 4 | 40 | `40 > 22` → `j = 3` |
| 2 | 0 | 3 | 30 | `30 > 22` → `j = 2` |
| 3 | 0 | 2 | 20 | `20 < 22` → `i = 1` |
| 4 | 1 | 2 | 25 | `25 > 22` → `j = 1` |
| 5 | 1 | 1 | 15 | `15 < 22` → `i = 2` |
| 6 | 2 | 1 | 19 | `19 < 22` → `i = 3` |
| 7 | 3 | 1 | 23 | `23 > 22` → `j = 0` |
| 8 | 3 | 0 | 13 | `13 < 22` → `i = 4` |
| 9 | 4 | 0 | 17 | `17 < 22` → `i = 5` |
| 10 | 5 | 0 | — | `i == n` → **False** |

**9 comparaciones**, que es `2n − 1 = 9`. ✔

En cada paso, o bien se descarta una fila (avanzando `i`) o bien se descarta una columna (retrocediendo `j`), pero nunca ambos a la vez. Para llegar a `i = n` o `j = -1`, se necesitan exactamente n descartes de filas y `n − 1` descartes de columnas (o viceversa), total `2n − 1` comparaciones. La matriz en escalera asegura que el algoritmo nunca encuentra `x` antes y que alterna los descartes de la forma más desfavorable.

---
