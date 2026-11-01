# Ejercicio 9 — La mezcla "optimizada" que se salta la última comparación

> ★★ Una mezcla "optimizada" de dos listas ordenadas de largo n deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla. (C5)

---

## 1. El algoritmo que se quiere "optimizar"

La mezcla estándar de dos listas ordenadas `A` y `B`, ambas de largo `n`, compara los frentes de las dos listas y saca el menor. Se detiene cuando una de las dos listas se agota, y entonces copia lo que queda de la otra.

La "optimización" propuesta dice: **cuando a la lista `A` le queda un solo elemento, dejamos de comparar y lo ponemos al final**. La idea intuitiva es que, si `A` ya casi se acabó, su último elemento debe ser el mayor de lo que queda, y no vale la pena compararlo con los elementos restantes de `B`.

```python
def mezclar_optimizado(A, B):
    """Mezcla A y B, ambas ordenadas de largo n.
       'Optimización': cuando a A le queda 1 elemento, se deja de comparar
       y se pone al final. Si B se agota antes, se copia el resto de A."""
    i = j = 0
    salida = []
    n = len(A)
    while i < n and j < n:
        # ¿A tiene un solo elemento? Entonces "optimizamos".
        if n - i == 1:
            salida.extend(B[j:])       # el resto de B
            salida.append(A[i])        # y el último de A al final
            return salida
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    # Si B se agotó primero, copiamos el resto de A (comportamiento estándar).
    salida.extend(A[i:])
    salida.extend(B[j:])
    return salida
```

**El caso interesante** es cuando `B` todavía tiene elementos y `A` se queda con uno solo. Ahí es donde la "optimización" cambia el comportamiento respecto de la mezcla estándar.

---

## 2. Cuántas comparaciones hace en el peor caso

Contemos las comparaciones de elementos (no las comprobaciones de índices como n - i == 1).

Hay dos formas en que termina el bucle:

    1. La optimización se dispara cuando i = n - 1 y j < n. Antes de ese momento se han sacado n - 1 elementos de A y j elementos de B. Cada elemento sacado consumió exactamente una comparación de elementos. Por tanto, las comparaciones son (n - 1) + j. Como j ≤ n - 1, esto es ≤ 2n - 2.

    2. El bucle termina porque B se agotó (j = n) sin que la optimización se haya disparado. En ese caso, como la optimización no se disparó, i ≤ n - 2 (si i = n - 1, la condición n - i == 1 habría disparado antes). Las comparaciones son i + n ≤ (n - 2) + n = 2n - 2.

En los dos casos, el algoritmo hace a lo sumo 2n - 2 comparaciones de elementos. El máximo 2n - 2 se alcanza, por ejemplo, cuando la optimización se dispara con j = n - 1 (queda un elemento de A y uno de B), o cuando el bucle termina con i = n - 2 y j = n.

**Comparación con la mezcla estándar.** La mezcla estándar hace a lo sumo `2n - 1` comparaciones (cada comparación saca un elemento, y el último sale sin comparar). La versión optimizada hace a lo sumo `2n - 2` en todos los casos. En su peor caso ahorra una comparación respecto del peor caso estándar; si `B` se agota primero sin que la optimización se dispare, hace las mismas comparaciones que la mezcla estándar sobre esa entrada.

**Tabla de comparaciones.**

| Algoritmo | Peor caso | Comentario |
|---|---|---|
| Mezcla estándar | `2n - 1` | Cota exacta; se alcanza con la entrada intercalada. |
| Mezcla "optimizada" | `2n - 2` | Ahorra a lo sumo una comparación respecto del peor caso estándar.|

---

## 3. La cota mínima: `2n - 1` comparaciones

La Conferencia 5 demuestra el siguiente teorema.

> **Teorema (mezclar).** Mezclar dos listas ordenadas de largo `n` requiere `2n - 1` comparaciones en el peor caso.

**Demostración (resumen).** El adversario responde como si la entrada fuera la **intercalada perfecta**:

```text
a₁ < b₁ < a₂ < b₂ < … < aₙ < bₙ
```

Esa cadena tiene `2n - 1` pares de vecinos, y cada par tiene un elemento de cada lista. Si un algoritmo termina sin haber comparado algún par de vecinos, por ejemplo `aᵢ` con `bᵢ`, se pueden intercambiar los valores de `aᵢ` y `bᵢ` sin que ninguna comparación hecha cambie de respuesta, pero la salida correcta cambia. El algoritmo daría la misma salida para las dos entradas y se equivocaría en una. Por tanto, tiene que comparar los `2n - 1` pares. ∎

**Consecuencia.** Cualquier algoritmo **correcto** que mezcle dos listas ordenadas de largo `n` hace **al menos `2n - 1` comparaciones** en el peor caso.

---

## 4. La cota mínima como detector del error

El algoritmo "optimizado" hace a lo sumo `2n - 2` comparaciones. La cota mínima dice que **cualquier algoritmo correcto necesita al menos `2n - 1`**. Por tanto:

> **El algoritmo "optimizado" no puede ser correcto.**

No hace falta probarlo, ni ejecutarlo, ni buscar un contraejemplo. **La cota mínima lo detecta sin correr nada.** Un algoritmo que promete hacer menos que una cota demostrada está mal, por definición: si fuera correcto, violaría el teorema.

**La lógica del argumento.**

1. La cota mínima es un teorema: **todo** algoritmo correcto hace `≥ 2n - 1` comparaciones.
2. El algoritmo "optimizado" hace `≤ 2n - 2` comparaciones.
3. Si el algoritmo fuera correcto, sería un algoritmo correcto que hace `≤ 2n - 2 < 2n - 1` comparaciones, contradiciendo el teorema.
4. Por tanto, el algoritmo es **incorrecto**. La "optimización" introduce un error.

**Lo que la cota no dice.** La cota no dice **en qué entrada** falla el algoritmo. Para eso hace falta el adversario de la sección 5.

---

## 5. La entrada del adversario: la intercalada perfecta

El adversario de la demostración de la cota es exactamente el que hace fallar al algoritmo. Tomemos:

```text
A = [1, 3, 5, …, 2n-1]      (los impares)
B = [2, 4, 6, …, 2n]        (los pares)
```

La entrada intercalada perfecta es `1 < 2 < 3 < 4 < … < 2n-1 < 2n`, y el resultado correcto es esa misma secuencia.

### 5.1. Traza con `n = 4`

```text
A = [1, 3, 5, 7]
B = [2, 4, 6, 8]
```

| Paso | `i` | `j` | `A[i]` | `B[j]` | Comparación | Salida | ¿Optimización? |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | 0 | 0 | 1 | 2 | `1 ≤ 2` → saca `A` | `[1]` | No (`n-i=4`) |
| 2 | 1 | 0 | 3 | 2 | `3 > 2` → saca `B` | `[1, 2]` | No (`n-i=3`) |
| 3 | 1 | 1 | 3 | 4 | `3 ≤ 4` → saca `A` | `[1, 2, 3]` | No (`n-i=2`) |
| 4 | 2 | 1 | 5 | 4 | `5 > 4` → saca `B` | `[1, 2, 3, 4]` | No (`n-i=2`) |
| 5 | 2 | 2 | 5 | 6 | `5 ≤ 6` → saca `A` | `[1, 2, 3, 4, 5]` | No (`n-i=2`) |
| 6 | 3 | 2 | 7 | 6 | **- (`n - i == 1`)** | `[1,2,3,4,5,6,8,7]` | **Sí** |

En el paso 6, `n - i = 4 - 3 = 1`. La optimización dispara: copia el resto de `B` (`6, 8`) y luego pone el último de `A` (`7`). La salida es:

```text
[1, 2, 3, 4, 5, 6, 8, 7]
```

**La salida correcta es `[1, 2, 3, 4, 5, 6, 7, 8]`.** El algoritmo puso `8` antes que `7`, y están al revés. **Falla.**

### 5.2. La traza general

Para n ≥ 2, antes de disparar la optimización se han hecho 2n - 3 comparaciones y se ha sacado alternadamente:
```text

a₁, b₁, a₂, b₂, …, a_{n-1}
```
En ese momento i = n - 1 y j = n - 2. La optimización copia el resto de B:
```text

B[j:] = [b_{n-1}, b_n] = [2n - 2, 2n]
```
y luego pone el último de A:
```text

A[i] = a_n = 2n - 1
```

La salida es:
```text

[1, 2, 3, …, 2n-2, 2n, 2n-1]
```

La salida correcta es [1, 2, 3, …, 2n-1, 2n]. El algoritmo intercambia los dos últimos elementos.

### 5.3. ¿Por qué falla?

El algoritmo asume que el último elemento de `A` es el mayor de lo que queda. Pero en la entrada intercalada, el último elemento de `A` (`2n-1`) es **menor** que el último elemento de `B` (`2n`). La optimización coloca `2n` antes que `2n-1`, y eso está mal.


### 5.4. Verificación experimental

```python
import random

def mezclar_optimizado(A, B):
    i = j = 0
    salida = []
    n = len(A)
    while i < n and j < n:
        if n - i == 1:
            salida.extend(B[j:])
            salida.append(A[i])
            return salida
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    salida.extend(A[i:])
    salida.extend(B[j:])
    return salida


def mezclar_estandar(A, B):
    i = j = 0
    salida = []
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    salida.extend(A[i:])
    salida.extend(B[j:])
    return salida


print(f"{'n':>3} {'A':>22} {'B':>22} {'salida opt':>30} {'correcta':>30} {'¿falla?':>8}")
for n in [2, 3, 4, 5, 6]:
    A = [2*k + 1 for k in range(n)]
    B = [2*k + 2 for k in range(n)]
    opt = mezclar_optimizado(A, B)
    est = mezclar_estandar(A, B)
    print(f"{n:>3} {str(A):>22} {str(B):>22} {str(opt):>30} {str(est):>30} {str(opt != est):>8}")
```

```text
  n                   A                     B                   salida opt                              correcta     ¿falla?
  2              [1, 3]                [2, 4]                 [1, 2, 4, 3]                             [1, 2, 3, 4]     True
  3           [1, 3, 5]             [2, 4, 6]              [1, 2, 3, 4, 6, 5]                    [1, 2, 3, 4, 5, 6]     True
  4        [1, 3, 5, 7]          [2, 4, 6, 8]            [1, 2, 3, 4, 5, 6, 8, 7]          [1, 2, 3, 4, 5, 6, 7, 8]     True
  5     [1, 3, 5, 7, 9]        [2, 4, 6, 8, 10]    [1, 2, 3, 4, 5, 6, 7, 8, 10, 9]  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]     True
  6   [1, 3, 5, 7, 9, 11]  [2, 4, 6, 8, 10, 12]   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]     True
```

En todos los casos, el algoritmo "optimizado" produce una salida incorrecta. **La cota mínima lo anticipó sin correr nada.**

### 5.5. Conteo de comparaciones en la entrada del adversario

```python
def mezclar_contando(A, B):
    i = j = 0
    comparaciones = 0
    salida = []
    n = len(A)
    while i < n and j < n:
        if n - i == 1:
            salida.extend(B[j:])
            salida.append(A[i])
            return salida, comparaciones
        comparaciones += 1
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    salida.extend(A[i:])
    salida.extend(B[j:])
    return salida, comparaciones


print(f"{'n':>3} {'comparaciones':>14} {'2n-3':>6} {'2n-1 (cota)':>12} {'¿< cota?':>10}")
for n in [2, 3, 4, 5, 8, 16, 32, 64]:
    A = [2*k + 1 for k in range(n)]
    B = [2*k + 2 for k in range(n)]
    _, c = mezclar_contando(A, B)
    print(f"{n:>3} {c:>14} {2*n-3:>6} {2*n-1:>12} {str(c < 2*n-1):>10}")
```

```text
  n   comparaciones   2n-3   2n-1 (cota)  ¿< cota?
  2                1      1            3       True
  3                3      3            5       True
  4                5      5            7       True
  5                7      7            9       True
  8               13     13           15       True
 16               29     29           31       True
 32               61     61           63       True
 64              125    125          127       True
```

En esta entrada, el algoritmo "optimizado" hace exactamente `2n - 3` comparaciones, que también es menos que la cota 2n - 1. El máximo `2n - 2` se alcanza en otra intercalación, pero esta entrada ya basta para violar la cota y para hacer fallar al algoritmo.

---
