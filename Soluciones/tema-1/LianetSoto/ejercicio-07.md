# Ejercicio 7 — Mediana de dos arreglos ordenados

> ★★★ Mediana de dos arreglos ordenados de largo n: el n-ésimo menor de los 2n elementos. Diseña un algoritmo O(log n), demuestra su correctitud y da la cota de información. (C2, C3, C5)

---

## 1. El problema y su especificación

**Problema** (mediana de dos arreglos ordenados). Dados dos arreglos `A` y `B`, ambos de tamaño `n` y ordenados de forma no decreciente, encontrar el n-ésimo menor de los `2n` elementos combinados. Es decir, si ordenamos los `2n` elementos, el que ocupa la posición n (1-indexado).

**Especificación (contrato).**

- **Precondición**. `A` y `B` son arreglos de tamaño `n ≥ 1`, ordenados de forma no decreciente.

- **Postcondición**. El valor devuelto `m` cumple, considerando `S = A ∪ B` como multiconjunto:
    ```text 
    |{x ∈ S : x < m}| < n  y |{x ∈ S : x ≤ m}| ≥ n
    ```

    Equivalentemente, `m = select_n(A ∪ B)`, el n-ésimo menor de S.


**Modelo**. Comparaciones entre elementos de A y B. Contamos el número de comparaciones en el peor caso.

**Ejemplo.**

```text
A = [1, 3, 8, 9]
B = [2, 4, 7, 10]

Combinados y ordenados: [1, 2, 3, 4, 7, 8, 9, 10]. El 4º menor es 4. La respuesta es 4.
```

## 2. La idea: partición con binaria

Queremos dividir los `2n` elementos en dos mitades de tamaño `n` cada una: una mitad izquierda (los `n` menores) y una mitad derecha (los `n` mayores). La mediana será el máximo de la mitad izquierda.

Como `A` y `B` están ordenados, cualquier mitad izquierda válida se puede describir tomando:

    i elementos de A (los primeros i), y

    j = n − i elementos de B (los primeros j).

La mitad izquierda es `A[0..i-1] ∪ B[0..j-1]`, y la mitad derecha es `A[i..n-1] ∪ B[j..n-1]`.

Para que esta partición sea válida, se deben cumplir dos condiciones:

    Todo elemento de la izquierda es ≤ todo elemento de la derecha. Como cada arreglo ya está ordenado, basta comprobar las fronteras:

        A[i-1] ≤ B[j] (el mayor de la izquierda de A ≤ el menor de la derecha de B).

        B[j-1] ≤ A[i] (el mayor de la izquierda de B ≤ el menor de la derecha de A).

    La mediana es max(A[i-1], B[j-1]), porque es el mayor de la mitad izquierda.

La clave está en que la condición `A[i-1] ≤ B[j]` se puede buscar con búsqueda binaria sobre `i`. Si `A[i-1] > B[j]`, entonces `i` es demasiado grande (hemos tomado demasiados elementos de `A` y muy pocos de `B`), así que hay que reducir `i`. Si `B[j-1] > A[i]`, entonces `i` es demasiado pequeño, así que hay que aumentar `i`.

## 3. El algoritmo
```python
def mediana_dos_arreglos(A, B):
    """
    A y B son listas ordenadas de tamaño n >= 1.
    Devuelve el n-ésimo menor de los 2n elementos combinados.
    """
    n = len(A)
    # Buscamos i en [0, n] tal que:
    #   i elementos de A en la izquierda, j = n - i elementos de B en la izquierda
    #   A[i-1] <= B[j]  y  B[j-1] <= A[i]
    # Usamos -infinito y +infinito para los casos límite.
    INF = float('inf')
    lo, hi = 0, n

    while lo <= hi:
        i = (lo + hi) // 2
        j = n - i

        # Valores en las fronteras (con centinelas)
        A_izq = A[i - 1] if i > 0 else -INF
        A_der = A[i] if i < n else INF
        B_izq = B[j - 1] if j > 0 else -INF
        B_der = B[j] if j < n else INF

        if A_izq <= B_der and B_izq <= A_der:
            # Partición válida: la mediana es el máximo de la izquierda
            return max(A_izq, B_izq)
        elif A_izq > B_der:
            # i es demasiado grande: reducir i
            hi = i - 1
        else:
            # B_izq > A_der: i es demasiado pequeño: aumentar i
            lo = i + 1

    raise ValueError("Entrada inválida")
```

**Detalles importantes.**

    Los centinelas -INF y INF evitan tener que tratar los casos i = 0, i = n, j = 0 y j = n por separado. Son valores simbólicos que no se comparan con nada real.

    El bucle busca i en el rango [0, n]. En cada iteración, o encontramos la partición válida, o descartamos la mitad del rango.

    La mediana es max(A_izq, B_izq), no un promedio, porque buscamos el n-ésimo menor de 2n elementos (no la mediana en el sentido de promedio de los dos centrales).

## 4. Traza sobre el ejemplo
```text
A = [1, 3, 8, 9]
B = [2, 4, 7, 10]
n = 4
```

| Iteración | `lo` | `hi` | `i` | `j` | `A_izq` | `A_der` | `B_izq` | `B_der` | ¿Partición válida? |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 0 | 4 | 2 | 2 | 3 | 8 | 4 | 7 | **Sí**: `3 ≤ 7` y `4 ≤ 8`. Mediana = `max(3, 4) = 4`. |

La primera partición (`i = 2`, `j = 2`) ya es válida, porque `A[1] = 3 ≤ B[2] = 7` y `B[1] = 4 ≤ A[2] = 8`. La mediana es max(3, 4) = 4. ✔

Otro ejemplo (con más iteraciones).
```text
A = [1, 2, 3, 4]
B = [5, 6, 7, 8]
n = 4
```

| Iteración | `lo` | `hi` | `i` | `j` | `A_izq` | `A_der` | `B_izq` | `B_der` | Acción |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 0 | 4 | 2 | 2 | 2 | 3 | 6 | 7 | `B_izq (6) > A_der (3)` → `lo = 3` |
| 2 | 3 | 4 | 3 | 1 | 3 | 4 | 5 | 6 | `B_izq (5) > A_der (4)` → `lo = 4` |
| 3 | 4 | 4 | 4 | 0 | 4 | INF | -INF | 5 | `A_izq (4) ≤ B_der (5)` y `B_izq (-INF) ≤ A_der (INF)` → válida. Mediana = `max(4, -INF) = 4` |

La respuesta es 4. ✔

## 5. Correctitud
### 5.1. Invariante

**Invariante**. En cada iteración, si existe una partición válida, entonces el valor de `i` que la produce está en el intervalo `[lo, hi]`.

**Inicialización**. `lo = 0`, `hi = n`. El rango completo contiene la solución. ✔

**Mantenimiento**. Supongamos que la solución está en `[lo, hi]`. Calculamos `i = (lo + hi) // 2` y `j = n - i`.

    Si A[i-1] > B[j], entonces i es demasiado grande: la solución debe tener un i menor. Por tanto, la solución está en [lo, i-1], y hacemos hi = i - 1.

    Si B[j-1] > A[i], entonces i es demasiado pequeño: la solución debe tener un i mayor. Por tanto, la solución está en [i+1, hi], y hacemos lo = i + 1.

    Si ninguna de las dos condiciones se cumple, hemos encontrado la partición válida y devolvemos la mediana.

En los dos primeros casos, el nuevo intervalo sigue conteniendo la solución. ✔

**Terminación**. El rango `[lo, hi]` tiene tamaño `hi - lo + 1`. En cada iteración que no devuelve, el nuevo rango tiene tamaño estrictamente menor. Como el tamaño es un entero no negativo que decrece, el bucle termina. Además, el rango nunca se vacía sin encontrar la solución: por el lema de existencia (abajo), siempre hay una partición válida, y el invariante garantiza que el rango la contiene hasta que se devuelve. ✔

### 5.2. Lema de existencia de la partición válida

**Lema**. Existe `i ∈ [0, n]` tal que, con `j = n - i,`
```text
A[i−1] ≤ B[j]  y  B[j−1] ≤ A[i],
```

donde usamos los centinelas `A[-1] = B[-1] = -∞` y `A[n] = B[n] = +∞`.

**Demostración**. Definimos
```text
f(i)=A[i−1]−B[n−i]
```

para `i = 0, 1, …, n`. La función `f` es no decreciente en `i`: cuando `i` aumenta en 1, `A[i-1]` no decrece (los arreglos están ordenados) y `B[n-i]` no crece (porque el índice `n-i` disminuye y B está ordenado). Por tanto, `f(i)` no decrece.

Además `f(0) = A[-1] - B[n] = -∞ < 0`.

**Caso 1**: `f(n) ≤ 0`. Entonces `i = n` es una partición válida:

    A[n-1] ≤ B[0] porque f(n) = A[n-1] - B[0] ≤ 0.

    B[-1] = -∞ ≤ A[n] = +∞.

**Caso 2**: `f(n) > 0`. Sea `i*` el menor índice con `f(i*) > 0`. Como `f(0) < 0`, se tiene `i* ≥ 1`. Por minimalidad, `f(i*-1) ≤ 0`. Es decir:
```text
A[i∗−2]≤B[n−i∗+1]yB[n−i∗]≤A[i∗−1].
```

Tomando `i = i^* - 1` y `j = n - i = n - i^* + 1`:

    A[i-1] = A[i^*-2] ≤ B[n-i^*+1] = B[j].

    B[j-1] = B[n-i^*] ≤ A[i^*-1] = A[i].

Luego `i = i^* - 1` es una partición válida. ∎

Este lema es exactamente lo que el algoritmo de búsqueda binaria necesita: garantiza que hay una solución en `[0, n]`, y por tanto que el bucle no termina sin devolver.

### 5.3. La partición válida da la mediana

**Lema**. Si `i y j = n - i` satisfacen `A[i-1] ≤ B[j]` y `B[j-1] ≤ A[i]`, entonces `max(A[i-1], B[j-1])` es el n-ésimo menor de `A ∪ B`.

**Demostración**. La mitad izquierda `L = A[0..i-1] ∪ B[0..j-1]` tiene exactamente `i + j = n` elementos. Por las condiciones de frontera, todo elemento de `L` es menor o igual que todo elemento de la mitad derecha `R = A[i..n-1] ∪ B[j..n-1]`:

    A[i-1] ≤ B[j] cubre la frontera entre A izquierda y B derecha.

    B[j-1] ≤ A[i] cubre la frontera entre B izquierda y A derecha.

    Dentro de cada arreglo, la ordenación ya garantiza el resto.

Por tanto, `L` contiene exactamente los n elementos más pequeños de `A ∪ B`. El mayor de ellos es `max(A[i-1], B[j-1])`, que es el n-ésimo menor. ∎

**Corolario (correctitud del algoritmo).** El algoritmo devuelve `max(A_izq, B_izq)` cuando encuentra una partición válida. Por el lema 5.3, ese valor es el n-ésimo menor. Por el lema 5.2, la partición válida existe. Por el invariante 5.1, el algoritmo la encuentra. Por tanto, el algoritmo es correcto. ∎

## 6. Complejidad

**Tiempo**. En cada iteración, el rango `[lo, hi]` se reduce a la mitad (o se encuentra la solución). El tamaño inicial del rango es `n + 1`. Por tanto, el número de iteraciones es `O(log n)`. Cada iteración hace `O(1)` comparaciones. Total: `O(log n)` comparaciones.

**Memoria**. `O(1)` adicional (solo variables auxiliares).

## 7. Cota inferior de información

**Teorema.** Cualquier algoritmo de comparaciones que resuelva el problema de la mediana de dos arreglos ordenados de tamaño n necesita Ω(log n) comparaciones en el peor caso.

**Demostración.** Restringimos el análisis a entradas con todos los valores distintos, de modo que cada comparación entre dos elementos de `A ∪ B` tiene exactamente dos resultados posibles (< o >). Así, el árbol de decisión correspondiente es binario.

Para cada `k ∈ {1, …, 2n}`, definimos el conjunto ordenado:
```text

S_k = {k − n + 1, k − n + 2, …, k − 1, k, k + 1, …, k + n}
```

`S_k` tiene exactamente `2n` elementos distintos, y su n-ésimo menor es `k`: hay exactamente `n − 1` elementos menores que `k` y `n` elementos mayores que `k`.

Definimos:
```text

A_k = [k − n + 1, …, k]
B_k = [k + 1, …, k + n]
```
Ambos tienen tamaño `n` y están ordenados. Además, el n-ésimo menor de `A_k ∪ B_k` es exactamente `k`.

Para `k = 1, …, 2n`, los valores `k` son todos distintos. Por tanto, las `2n` instancias (`A_k, B_k`) requieren `2n` salidas distintas. Como el árbol de decisión es binario, debe tener al menos `2n` hojas.

Un árbol binario de altura `h` tiene a lo sumo `2^h` hojas. Luego:
```text

2^h ≥ 2n  ⇒  h ≥ ⌈log₂(2n)⌉ = Ω(log n)
```
La altura del árbol es el número de comparaciones en el peor caso. Por tanto, cualquier algoritmo de comparaciones necesita `Ω(log n)` comparaciones en el peor caso. ∎

**Observación.** El algoritmo de la sección 3 usa `O(log n)` comparaciones, así que es óptimo asintóticamente en el modelo de comparaciones. No se afirma que use exactamente `⌈log₂(2n)⌉` comparaciones; de hecho, para esta implementación el peor caso es `2⌊log₂(n+1)⌋ + 3` comparaciones, que sigue siendo `Θ(log n)`.

## 8. Verificación experimental
### 8.1. Correctitud contra fuerza bruta
```python
import random
import itertools

def mediana_fuerza_bruta(A, B):
    combinados = sorted(A + B)
    return combinados[len(A) - 1]  # n-ésimo menor (índice n-1 en 0-indexado)

random.seed(2026)
fallos = 0
for _ in range(5000):
    n = random.randint(1, 20)
    A = sorted(random.sample(range(100), n))
    B = sorted(random.sample(range(100), n))
    m1 = mediana_dos_arreglos(A, B)
    m2 = mediana_fuerza_bruta(A, B)
    if m1 != m2:
        fallos += 1
        print(f"Fallo con A={A}, B={B}: {m1} != {m2}")
print(f"5000 instancias, fallos: {fallos}")
```

```text
5000 instancias, fallos: 0
```

### 8.2. Conteo de comparaciones

El código `mediana_contando` cuenta las comparaciones reales, incluyendo las que involucran a los centinelas `-INF` e `INF`.

Para esta implementación concreta, el peor caso se alcanza cuando todos los elementos de `A` son menores que todos los de `B` (por ejemplo, `A = [0, ..., n-1]`, `B = [n, ..., 2n-1]`). En ese caso:

    Para cada i < n, la primera comparación A_izq <= B_der es verdadera, y la segunda B_izq <= A_der es falsa. Cada iteración no válida cuesta 2 comparaciones.

    La última iteración, en i = n, es válida y cuesta 3 comparaciones.

    La búsqueda binaria sobre [0, n] tarda en llegar a i = n exactamente ⌊log₂(n+1)⌋ + 1 iteraciones en el peor caso.

Por tanto, el número exacto de comparaciones en el peor caso para este código es:
```text

2⌊log₂(n+1)⌋ + 3
```
Verificación constructiva:
```python

import math

def mediana_contando(A, B):
    """Devuelve (mediana, número real de comparaciones)."""
    n = len(A)
    INF = float('inf')
    lo, hi = 0, n
    comps = 0

    while lo <= hi:
        i = (lo + hi) // 2
        j = n - i

        A_izq = A[i - 1] if i > 0 else -INF
        A_der = A[i] if i < n else INF
        B_izq = B[j - 1] if j > 0 else -INF
        B_der = B[j] if j < n else INF

        comps += 1
        if A_izq <= B_der:
            comps += 1
            if B_izq <= A_der:
                comps += 1
                return max(A_izq, B_izq), comps
            else:
                lo = i + 1
        else:
            hi = i - 1

    raise ValueError("Entrada inválida")

def peor_formula(n):
    return 2 * math.floor(math.log2(n + 1)) + 3

print(f"{'n':>5} {'peor caso exacto':>17} {'2⌊log₂(n+1)⌋+3':>16} {'⌈log₂(2n)⌉':>12}")
for n in [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 32]:
    # Construimos la entrada que alcanza el peor caso
    A = list(range(n))
    B = list(range(n, 2 * n))
    _, c = mediana_contando(A, B)
    formula = peor_formula(n)
    cota_info = math.ceil(math.log2(2 * n)) if n > 0 else 0
    print(f"{n:>5} {c:>17} {formula:>16} {cota_info:>12}")
```
Salida esperada:
```text
    n   peor caso exacto   2⌊log₂(n+1)⌋+3   ⌈log₂(2n)⌉
    1                 5                 5            1
    2                 5                 5            2
    3                 7                 7            3
    4                 7                 7            3
    5                 7                 7            4
    6                 7                 7            4
    7                 9                 9            4
    8                 9                 9            4
   15                11                11            5
   16                11                11            5
   31                13                13            6
   32                13                13            6
```
**Lectura.** El algoritmo usa Θ(log n) comparaciones, y la cota inferior Ω(log n) se cumple. La diferencia con ⌈log₂(2n)⌉ es una constante multiplicativa y aditiva; no cambia la optimalidad asintótica. Las comparaciones con -INF e INF se cuentan como comparaciones reales; si se quisieran excluir, habría que modificar el código para no consultar los centinelas, pero eso complicaría la implementación sin cambiar la cota asintótica.

### 8.3. Casos límite
```python
# n = 1: el único caso donde el corte puede ser i = 0 o i = n
assert mediana_dos_arreglos([1], [2]) == 1
assert mediana_dos_arreglos([2], [1]) == 1

# Todos los elementos de A son menores que los de B:
# el corte válido es i = n, j = 0
assert mediana_dos_arreglos([1, 2, 3], [4, 5, 6]) == 3

# Todos los elementos de B son menores que los de A:
# el corte válido es i = 0, j = n
assert mediana_dos_arreglos([4, 5, 6], [1, 2, 3]) == 3

# Elementos intercalados: el corte válido está en el medio
assert mediana_dos_arreglos([1, 3, 5], [2, 4, 6]) == 3

# Con elementos repetidos: la postcondición debe seguir caracterizando
# al n-ésimo menor aunque haya empates
assert mediana_dos_arreglos([1, 2, 2], [2, 2, 3]) == 2

print("Todos los casos límite pasan. ✔")
``` 

```text
Todos los casos pasan. ✔
```