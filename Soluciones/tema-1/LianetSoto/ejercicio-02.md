# Ejercicio 2 — Invariante, potencial y cota de información de la búsqueda binaria

> ★ Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima. (C3, C5)

---

## 1. El problema y su especificación

**Problema.** Dado un arreglo ordenado `A[0..n-1]` y un valor `x`, devolver una posición `i` con `A[i] = x`, o `-1` si `x` no está en `A`.

**Modelo.** Comparaciones entre elementos del arreglo y `x`. Cada comparación devuelve uno de tres signos: `<`, `=`, `>`. Contamos el número de comparaciones.

**Especificación (contrato).**

- **Precondición.** `A` está ordenado de forma no decreciente: `A[0] ≤ A[1] ≤ … ≤ A[n-1]`.
- **Postcondición.** El valor devuelto `r` cumple:
  - `r = -1` y `x ∉ A`, o
  - `0 ≤ r < n` y `A[r] = x`.

Sobre un arreglo desordenado el algoritmo no es incorrecto: el contrato simplemente no dice nada. La búsqueda binaria es **correcta parcialmente** si, cuando termina, cumple la postcondición, y **termina** para toda entrada que cumpla la precondición. La correctitud total es las dos cosas.

---

## 2. El algoritmo

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)          # rango candidato: A[lo:hi]
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return m
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    return -1
```

Tres detalles que hay que respetar:

1. El rango candidato es **semiabierto**: `A[lo:hi]` incluye `lo` y excluye `hi`.
2. Cuando `A[m] < x`, sabemos que `A[lo..m]` no puede contener `x`, así que `lo = m + 1` (no `lo = m`).
3. Cuando `A[m] > x`, sabemos que `A[m..hi-1]` no puede contener `x`, así que `hi = m` (no `hi = m - 1`).


---

## 3. Correctitud parcial: el invariante

### 3.1. Enunciado del invariante

> **Invariante `I(lo, hi)`.** Si `x` está en `A`, entonces `x` está en `A[lo:hi]`.

Es decir: el rango candidato **nunca pierde** una posición donde podría estar `x`.

### 3.2. Inicialización

Antes de la primera vuelta, `lo = 0` y `hi = n`. El rango `A[0:n]` es el arreglo entero. Trivialmente, si `x` está en `A`, está en `A[0:n]`. ✔

### 3.3. Mantenimiento

Supongamos `I(lo, hi)` y `lo < hi`. Sea `m = (lo + hi) // 2`, y consideremos las tres ramas del `if`:

**Rama 1: `A[m] == x`.** El algoritmo devuelve `m`, y la postcondición se cumple en el acto. No hay nada que mantener porque el ciclo termina.

**Rama 2: `A[m] < x`.** Como `A` está ordenado, para todo `i ≤ m` se tiene `A[i] ≤ A[m] < x`. Por tanto, si `x ∈ A`, la posición de `x` es mayor que `m`, es decir, `x ∈ A[m+1:hi]`. El algoritmo asigna `lo = m + 1`, y el nuevo rango `A[m+1:hi]` contiene a `x` si `x ∈ A`. Así que `I(m+1, hi)` se cumple. ✔

**Rama 3: `A[m] > x`.** Análogamente, para todo `i ≥ m` se tiene `A[i] ≥ A[m] > x`, así que si `x ∈ A`, la posición de `x` es menor que `m`, es decir, `x ∈ A[lo:m]`. El algoritmo asigna `hi = m`, y el nuevo rango `A[lo:m]` contiene a `x`. Así que `I(lo, m)` se cumple. ✔

### 3.4. Conclusión

Cuando el ciclo termina, `lo == hi`, así que el rango `A[lo:hi]` es vacío. Por el invariante, si `x ∈ A` entonces `x ∈ ∅`, lo que es imposible. Por tanto `x ∉ A`, y devolver `-1` es correcto. ✔

### 3.5. Visualización

Para `A = [1, 3, 5, 7, 9, 11, 13]` y `x = 5`:

```text
paso  lo  hi   m   A[m]   decisión
  0    0   7   3    7     A[m] > x  →  hi = 3
  1    0   3   1    3     A[m] < x  →  lo = 2
  2    2   3   2    5     A[m] = x  →  devuelve 2
```

En cada paso, si `5` está en `A`, sigue dentro del rango `A[lo:hi]`:

```text
inicio:    [1  3  5  7  9 11 13]     lo=0, hi=7
paso 1:    [1  3  5]                  lo=0, hi=3
paso 2:    [      5]                  lo=2, hi=3
paso 3:    encontrado en A[2]
```

Y para `x = 6`, que no está en `A`:

```text
inicio:    [1  3  5  7  9 11 13]     lo=0, hi=7
paso 1:    [1  3  5]                  lo=0, hi=3
paso 2:    [      5]                  lo=2, hi=3
paso 3:    [         ]                lo=3, hi=3   →  x ∉ A
```

### 3.6. Invariante vigilado

Ejecutamos el algoritmo con un `assert` que comprueba el invariante en cada vuelta:

```python
def binaria_vigilada(A, x):
    lo, hi = 0, len(A)
    pasos = 0
    while lo < hi:
        pasos += 1
        assert (x not in A) or any(A[i] == x for i in range(lo, hi)), \
            f"Invariante roto: lo={lo}, hi={hi}"
        m = (lo + hi) // 2
        if A[m] == x:
            return m, pasos
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    assert x not in A, f"x={x} ∈ A pero el rango quedó vacío"
    return -1, pasos
```

Probamos con muchos arreglos, todos los valores del rango y también valores fuera:

```python
import random

random.seed(7)
casos = 0
for _ in range(2000):
    n = random.randint(1, 15)
    A = sorted(random.sample(range(-20, 20), n))
    for x in range(-25, 25):
        binaria_vigilada(A, x)
        casos += 1
print(f"invariante verificado en {casos} consultas, sin fallos")
```

```text
invariante verificado en 100000 consultas, sin fallos
```

---

## 4. Terminación: el potencial

### 4.1. Enunciado del potencial

> **Potencial.** `Φ(lo, hi) = hi - lo`, la cantidad de posiciones que todavía podrían contener a `x`.

Propiedades:

- `Φ ≥ 0` siempre, porque `lo ≤ hi` (el ciclo solo sigue si `lo < hi`).
- `Φ` es un entero.
- Antes de la primera vuelta, `Φ = n`.
- Cada vuelta que no devuelve reduce `Φ` estrictamente.

### 4.2. Por qué baja

Sea `m = (lo + hi) // 2` y `lo < hi`. Entonces `lo ≤ m < hi`.

- Si `A[m] < x`, el algoritmo hace `lo = m + 1`. El nuevo potencial es
  ```text
  Φ' = hi - (m + 1) = (hi - lo) - (m - lo) - 1 < hi - lo = Φ
  ```
  porque `m ≥ lo`.

- Si `A[m] > x`, el algoritmo hace `hi = m`. El nuevo potencial es
  ```text
  Φ' = m - lo < hi - lo = Φ
  ```
  porque `m < hi`.

En los dos casos, `Φ' < Φ`. Como `Φ` es un entero no negativo que baja en cada vuelta, el ciclo termina.

### 4.3. Cuántas vueltas

Más aún, el potencial **se reduce a la mitad** aproximadamente en cada vuelta:

- Si `Φ = 2k`, entonces `m = lo + k`, y `Φ' ≤ k`.
- Si `Φ = 2k + 1`, entonces `m = lo + k`, y `Φ' ≤ k + 1 = ⌈Φ/2⌉`.

En general, `Φ' ≤ ⌊Φ/2⌋`. Después de `t` vueltas, `Φ ≤ ⌊n/2^t⌋`. Cuando `Φ = 0` el ciclo termina, así que

```text
t ≤ ⌈log₂(n + 1)⌉
```

que es exactamente la cota de información de la sección siguiente.

### 4.4. Potencial medido

```python
def binaria_potencial(A, x):
    lo, hi = 0, len(A)
    filas = [(lo, hi, hi - lo)]
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            break
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
        filas.append((lo, hi, hi - lo))
    for i in range(1, len(filas)):
        assert filas[i][2] < filas[i-1][2], "El potencial no bajó"
    return filas

A = [1, 3, 5, 7, 9, 11, 13]
for x in (5, 6):
    print(f"x = {x}:")
    print(f"{'paso':>5} {'lo':>4} {'hi':>4} {'Φ':>4}")
    for i, (lo, hi, phi) in enumerate(binaria_potencial(A, x)):
        print(f"{i:>5} {lo:>4} {hi:>4} {phi:>4}")
    print()
```

```text
x = 5:
 paso   lo   hi    Φ
    0    0    7    7
    1    0    3    3
    2    2    3    1

x = 6:
 paso   lo   hi    Φ
    0    0    7    7
    1    0    3    3
    2    2    3    1
    3    3    3    0
```

El potencial baja estrictamente: `7 → 3 → 1 → 0`. En `x = 5` el ciclo corta antes porque encuentra `x`; en `x = 6` llega hasta `Φ = 0`, que es el peor caso.

---

## 5. Cota mínima: el argumento de información

### 5.1. El modelo

Como en la Conferencia 5, el modelo es **comparaciones**: el algoritmo solo puede preguntar el signo de `x - A[i]`. Con las respuestas `<`, `=`, `>` va construyendo un árbol de decisión trinario.

### 5.2. El árbol de decisión

```text
                       x ? A[3]
                    /     |     \
              <    /      =      \    >
                 /       |        \
          x ? A[1]      "A[3]"   x ? A[5]
         /   |   \               /   |   \
       <    =    >             <    =    >
      /     |     \           /     |     \
 x?A[0]  "A[1]" x?A[2]  x?A[4]  "A[5]" x?A[6]
  /|\            /|\     /|\            /|\
 h0 ...         h2 h3  h4 h5          h6 h7
```

Cada nodo interno es una comparación; cada hoja, una salida. El **peor caso** es la altura del árbol.

### 5.3. Los huecos

Cuando `x` no está en `A`, cae en uno de los `n + 1` **huecos**:

```text
      h0   a1   h1   a2   h2   a3   h3   a4   h4   a5   h5
      |    |    |    |    |    |    |    |    |    |    |
      ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑
     -∞  antes  entre  entre  entre  entre  entre  entre  después
          de a1 a1,a2 a2,a3 a3,a4 a4,a5 a5,+∞
```

**Lema (C5, lema 4).** Si `x₁` y `x₂` caen en huecos distintos, un algoritmo correcto los lleva a hojas distintas.

**Demostración.** Supongamos que `x₁ < x₂` caen en huecos distintos y terminan en la misma hoja. Entre sus huecos hay al menos un elemento `a` de `A`. El algoritmo no comparó con ese `a` (si lo hubiera hecho, `x₁` habría recibido `<` y `x₂` habría recibido `>`, y estarían en caminos distintos). Ahora tomemos `x = a`. En cada comparación con un elemento a la izquierda o a la derecha de los dos huecos, `a` recibe la misma respuesta que `x₁` y `x₂`. Así que `a` recorre el mismo camino y llega a la misma hoja, donde el algoritmo dice "no está", aunque `a` sí está. Contradicción. □

### 5.4. El teorema

**Teorema.** Todo algoritmo de búsqueda por comparaciones correcto sobre un arreglo ordenado de `n` elementos hace, en el peor caso, al menos `⌈log₂(n + 1)⌉` comparaciones.

**Demostración.** Por el lema, los `n + 1` huecos van a hojas distintas. En la parte del árbol que solo usa las ramas `<` y `>`, que es un árbol binario, el número de hojas es a lo sumo `2^h` donde `h` es la altura. Por el lema 1 de la Conferencia 5, `2^h ≥ n + 1`, es decir, `h ≥ ⌈log₂(n + 1)⌉`. □

### 5.5. La búsqueda binaria lo alcanza

Con `A = [1, 3, 5, 7, 9, 11, 13]`, hay `n = 7` elementos y `n + 1 = 8` huecos. Para que la traza sea completa hay que cubrir las dos clases de entradas:

- **Elementos de `A`:** `x ∈ {1, 3, 5, 7, 9, 11, 13}`. El algoritmo termina en cuanto compara con `x`.
- **Huecos:** un representante por cada intervalo entre elementos. Cualquier otro valor del mismo hueco recibe las mismas respuestas y recorre el mismo camino.

La traza completa, con un representante por hueco, es:

| `x` | categoría | camino | comparaciones | resultado |
|---:|---|---|---:|---|
| `0` | hueco `h0` (`x < 1`) | `x<7`, `x<3`, `x<1` | `3` | `-1` |
| `1` | `A[0]` | `x<7`, `x<3`, `x=1` | `3` | encontrado en `A[0]` |
| `2` | hueco `h1` (`1 < x < 3`) | `x<7`, `x<3`, `x>1` | `3` | `-1` |
| `3` | `A[1]` | `x<7`, `x=3` | `2` | encontrado en `A[1]` |
| `4` | hueco `h2` (`3 < x < 5`) | `x<7`, `x>3`, `x<5` | `3` | `-1` |
| `5` | `A[2]` | `x<7`, `x>3`, `x=5` | `3` | encontrado en `A[2]` |
| `6` | hueco `h3` (`5 < x < 7`) | `x<7`, `x>3`, `x>5` | `3` | `-1` |
| `7` | `A[3]` | `x=7` | `1` | encontrado en `A[3]` |
| `8` | hueco `h4` (`7 < x < 9`) | `x>7`, `x<11`, `x<9` | `3` | `-1` |
| `9` | `A[4]` | `x>7`, `x<11`, `x=9` | `3` | encontrado en `A[4]` |
| `10` | hueco `h5` (`9 < x < 11`) | `x>7`, `x<11`, `x>9` | `3` | `-1` |
| `11` | `A[5]` | `x>7`, `x=11` | `2` | encontrado en `A[5]` |
| `12` | hueco `h6` (`11 < x < 13`) | `x>7`, `x>11`, `x<13` | `3` | `-1` |
| `13` | `A[6]` | `x>7`, `x>11`, `x=13` | `3` | encontrado en `A[6]` |
| `14` | hueco `h7` (`x > 13`) | `x>7`, `x>11`, `x>13` | `3` | `-1` |

Las ocho hojas de huecos están a profundidad `3 = ⌈log₂(8)⌉`. Los elementos se encuentran antes: `7` en una comparación, `3` y `11` en dos, y el resto en tres. Por tanto, el peor caso sobre **todas** las entradas es `3`, y coincide con la cota del lema 4.

Para la cota inferior basta mirar los huecos: son `n + 1 = 8` hojas distintas en el subárbol que solo usa las ramas `<` y `>`, y un árbol binario de altura `h` tiene a lo sumo `2^h` hojas. Así que `h ≥ ⌈log₂(8)⌉ = 3`. La búsqueda binaria alcanza esa altura, así que es óptima en el modelo de comparaciones.

### 5.6. Tabla para varios `n`

```python
import math

def peor_caso_binaria(n):
    A = list(range(n))
    peor = 0
    for x in range(-1, n + 1):
        lo, hi, c = 0, n, 0
        while lo < hi:
            c += 1
            m = (lo + hi) // 2
            if A[m] == x:
                break
            elif A[m] < x:
                lo = m + 1
            else:
                hi = m
        peor = max(peor, c)
    return peor

print(f"{'n':>5} {'peor caso':>10} {'⌈log₂(n+1)⌉':>14}")
for n in [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 32, 100, 1000, 1023, 1024]:
    print(f"{n:>5} {peor_caso_binaria(n):>10} {math.ceil(math.log2(n + 1)):>14}")
```

```text
    n  peor caso   ⌈log₂(n+1)⌉
    1          1              1
    2          2              2
    3          2              2
    4          3              3
    5          3              3
    6          3              3
    7          3              3
    8          4              4
   15          4              4
   16          5              5
   31          5              5
   32          6              6
  100          7              7
 1000         10             10
 1023         10             10
 1024         11             11
```

En todos los casos el peor caso coincide exactamente con `⌈log₂(n + 1)⌉`. La búsqueda binaria es **óptima** en el modelo de comparaciones.

---

## 6. Verificación experimental conjunta

El siguiente programa junta las tres piezas: invariante, potencial y comparación con la cota. Corre sobre muchos arreglos y valores, y comprueba que:

1. El invariante se mantiene en cada vuelta.
2. El potencial baja estrictamente en cada vuelta.
3. El número de comparaciones en el peor caso coincide con `⌈log₂(n + 1)⌉`.

```python
import math, random

def analizar(A, x):
    lo, hi = 0, len(A)
    comparaciones = 0
    potenciales = [hi - lo]
    while lo < hi:
        # invariante
        assert (x not in A) or any(A[i] == x for i in range(lo, hi))
        comparaciones += 1
        m = (lo + hi) // 2
        if A[m] == x:
            return m, comparaciones, potenciales
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
        potenciales.append(hi - lo)
    # el potencial bajó en cada vuelta
    for i in range(1, len(potenciales)):
        assert potenciales[i] < potenciales[i-1]
    assert x not in A
    return -1, comparaciones, potenciales

random.seed(2026)
for n in range(1, 50):
    for _ in range(50):
        A = sorted(random.sample(range(-100, 100), n))
        for x in range(-105, 105):
            analizar(A, x)

# peor caso y cota
print(f"{'n':>5} {'peor caso':>10} {'cota':>6} {'coincide':>10}")
for n in [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023]:
    A = list(range(n))
    peor = max(analizar(A, x)[1] for x in range(-1, n + 1))
    cota = math.ceil(math.log2(n + 1))
    print(f"{n:>5} {peor:>10} {cota:>6} {str(peor == cota):>10}")
```

```text
    n  peor caso   cota  coincide
    1          1      1      True
    3          2      2      True
    7          3      3      True
   15          4      4      True
   31          5      5      True
   63          6      6      True
  127          7      7      True
  255          8      8      True
  511          9      9      True
 1023         10     10      True
```

Sin un solo fallo en medio millón de consultas. El experimento confirma los tres teoremas a la vez.

---
