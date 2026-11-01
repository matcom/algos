# Ejercicio 11 — La mochila entera, medida en bits

> ★★ La mochila entera se resuelve con programación dinámica en `O(nW)`, donde `W` es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

---

## 1. El problema y su especificación

**Mochila 0/1.**

- **Entrada.** `n` objetos, cada uno con un peso `w_i ≥ 0` y un valor `v_i ≥ 0`, y una capacidad `W ≥ 0`.
- **Salida.** Un subconjunto `S ⊆ {1,…,n}` que maximiza `Σ_{i∈S} v_i` sujeto a `Σ_{i∈S} w_i ≤ W`.

**Precondición.** Todos los pesos y valores son enteros no negativos, `W` es entero no negativo.

**Postcondición.** El valor devuelto `V*` es `max { Σ_{i∈S} v_i : Σ_{i∈S} w_i ≤ W }`.


---

## 2. La recurrencia

Definimos `K[i][c]` = máximo valor que se puede obtener usando un subconjunto de los primeros `i` objetos con capacidad `c`.

**Recurrencia.**

```text
K[0][c] = 0                                   para todo c
K[i][c] = K[i-1][c]                           si w_i > c
K[i][c] = max( K[i-1][c],                     si w_i ≤ c
               K[i-1][c - w_i] + v_i )
```

**Respuesta.** `K[n][W]`.

**Algoritmo.**

```python
def mochila(pesos, valores, W):
    n = len(pesos)
    K = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = pesos[i-1], valores[i-1]
        for c in range(W + 1):
            if wi <= c:
                K[i][c] = max(K[i-1][c], K[i-1][c - wi] + vi)
            else:
                K[i][c] = K[i-1][c]
    return K[n][W], K
```

**Variante con memoria `O(W)`.** La recurrencia solo mira la fila `i-1` para calcular la fila `i`, así que podemos usar dos filas y reducir la memoria a `O(W)`:

```python
def mochila_rolling(pesos, valores, W):
    anterior = [0] * (W + 1)
    for wi, vi in zip(pesos, valores):
        actual = anterior[:]                     # caso w_i > c
        for c in range(wi, W + 1):
            actual[c] = max(anterior[c], anterior[c - wi] + vi)
        anterior = actual
    return anterior[W]
```

La memoria baja de `O(nW)` a `O(W)`, pero el tiempo sigue siendo `O(nW)`. Para el análisis de esta sección, cualquiera de las dos versiones sirve; el tiempo no cambia.

---

## 3. Correctitud

**Invariante.** Después de la fila `i`, para todo `c` con `0 ≤ c ≤ W`, `K[i][c]` es el máximo valor alcanzable con un subconjunto de los primeros `i` objetos y capacidad `c`.

**Inicialización.** `K[0][c] = 0` para todo `c`: sin objetos, el mejor valor es 0. ✔

**Mantenimiento.** Supongamos el invariante para `i-1`. Para el objeto `i` y la capacidad `c`:

- Si `w_i > c`, el objeto `i` no cabe: `K[i][c] = K[i-1][c]`, correcto.
- Si `w_i ≤ c`, la solución óptima o no incluye el objeto `i` (valor `K[i-1][c]`) o lo incluye (valor `K[i-1][c - w_i] + v_i`). El máximo de los dos es lo que calcula la recurrencia. ✔

**Conclusión.** `K[n][W]` es el máximo valor alcanzable con los `n` objetos y capacidad `W`, que es la respuesta. □

**Terminación.** Dos ciclos acotados por `n` y `W+1`. Termina. □

**Costo.** `O(nW)` tiempo, `O(nW)` memoria (o `O(W)` con la versión rolling).

---

## 4. El tamaño de la entrada, medido en bits

**El tamaño de la entrada es la cantidad de bits que ocupa**, no el valor de sus números.

**Entrada.**

- `n` objetos.
- Para cada objeto `i`: peso `w_i` y valor `v_i`, cada uno codificado en binario.
- Capacidad `W`, codificada en binario.

**Supongamos que todos los números están acotados por `M`**, es decir, `w_i, v_i, W ≤ M`. Entonces:

- Cada `w_i` ocupa `⌈log₂ M⌉ + 1` bits (o `⌈log₂(w_i + 1)⌉`, según la convención).
- Cada `v_i`, lo mismo.
- `W` ocupa `⌈log₂(W + 1)⌉ ≤ ⌈log₂ M⌉ + 1` bits.

**Tamaño total de la entrada:**

```text
B = n · 2 · ⌈log₂ M⌉ + ⌈log₂ M⌉
  = O(n log M) bits
```

El factor `2` viene de que hay dos números por objeto (peso y valor). Si solo nos importa el orden de magnitud y `M ≥ 2`, podemos escribir `B = Θ(n log M)`.

**Ejemplo concreto.** `n = 100` objetos, todos los pesos y valores `≤ M = 10⁶` (unos 20 bits cada uno), y `W = 10⁶` (20 bits). Entrada:

```text
B = 100 · 2 · 20 + 20 = 4 020 bits ≈ 500 bytes
```

Es decir, **medio kilobyte** de entrada.

**Punto clave.** La entrada no "contiene" `W` como una cantidad de `W` celdas; contiene la **representación binaria** de `W`, que ocupa `log₂ W` bits. Aunque el DP recorra `W + 1` columnas, esa `W` puede ser enorme para una entrada minúscula.

---

## 5. ¿Es polinomial el algoritmo `O(nW)`?

**Respuesta corta: no.** Es **pseudopolinomial**. 

**El costo en función del tamaño de la entrada.** Como `W ≤ M`, el costo es

```text
T(n, W) = O(nW) ≤ O(nM)
```

y `M = 2^(log₂ M)`. Sea `b = log₂ M` la cantidad de bits del número más grande. Entonces:

```text
T(n, W) = O(n · 2^b)
```

**Esto es exponencial en `b`**, la cantidad de bits. No importa que sea lineal en `n` y en `W`: lo que manda en la definición de "polinomial en el tamaño de la entrada" es la cantidad de bits `B = Θ(n log M) = Θ(nb)`. Y `T` es exponencial en `b`, no polinomial en `B`.

**Formalmente.** Sea `B(n, W)` el tamaño en bits. Si `T(n, W)` fuera polinomial en `B`, existirían `k` y `c` con

```text
T(n, W) ≤ c · B(n, W)^k
```

para todo `n, W`. Pero tomando `n = 1` y `W = 2^b`, tenemos `B = Θ(b)` y `T = Θ(2^b) = Θ(2^B)`, que **no** es `O(B^k)` para ningún `k` fijo. Por tanto `T` no es polinomial en `B`.

**Consecuencia.** El algoritmo `O(nW)` **es** polinomial cuando `W` está acotado por un polinomio en `n` (porque entonces `b = O(log n)` y `T = O(n · poly(n)) = poly(n)`). Pero **no** es polinomial cuando `W` puede ser exponencialmente grande respecto de `n`, que es el caso general.

**Tabla ilustrativa.** Costo del DP y tamaño de la entrada, para `n = 50` y distintos `W`:

| `W` | bits de `W` | `W` como fracción de `2^bits` | Operaciones del DP (`n·W`) | Tiempo a `10⁹` ops/s |
|---:|---:|---:|---:|---:|
| `10³` | 10 | — | `5 × 10⁴` | `5 × 10⁻⁵ s` |
| `10⁶` | 20 | — | `5 × 10⁷` | `0.05 s` |
| `10⁹` | 30 | — | `5 × 10¹⁰` | `50 s` |
| `10¹²` | 40 | — | `5 × 10¹³` | `14 horas` |
| `10¹⁵` | 50 | — | `5 × 10¹⁶` | `1.6 años` |

**Cada 10 bits más de `W` multiplican el tiempo por 1000.** 

**El contraste con el tamaño de la entrada.** Para `n = 50`:

| `W` | Tamaño de entrada `B` (bits) | Operaciones del DP |
|---:|---:|---:|
| `10³` | `50·2·10 + 10 = 1010` | `5 × 10⁴` |
| `10⁶` | `50·2·20 + 20 = 2020` | `5 × 10⁷` |
| `10⁹` | `50·2·30 + 30 = 3030` | `5 × 10¹⁰` |
| `10¹²` | `50·2·40 + 40 = 4040` | `5 × 10¹³` |

La entrada crece **linealmente** (de 1010 a 4040 bits), pero el tiempo crece **exponencialmente** (de 5×10⁴ a 5×10¹³). Esa es la esencia de la pseudopolinomialidad.

---

## 6. El experimento: medir la explosión

El siguiente programa mide el tiempo del DP para `n = 100` y `W` creciendo, y confirma el crecimiento exponencial.

```python
import time

def mochila_rolling(pesos, valores, W):
    anterior = [0] * (W + 1)
    for wi, vi in zip(pesos, valores):
        actual = anterior[:]
        for c in range(wi, W + 1):
            actual[c] = max(anterior[c], anterior[c - wi] + vi)
        anterior = actual
    return anterior[W]

def medir(n, W, repeticiones=3):
    pesos = [1 + (i * 7919) % 1000 for i in range(n)]
    valores = [1 + (i * 104729) % 1000 for i in range(n)]
    mejor = float("inf")
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        mochila_rolling(pesos, valores, W)
        t1 = time.perf_counter()
        mejor = min(mejor, t1 - t0)
    return mejor

print(f"{'W':>10} {'bits(W)':>8} {'tiempo (s)':>12} {'ops/s aprox':>14}")
for W in [10**3, 10**4, 10**5, 10**6, 10**7]:
    t = medir(100, W)
    print(f"{W:>10,} {W.bit_length():>8} {t:>12.4f} {100 * W / t:>14.2e}")
```

**Salida:**

```text
         W  bits(W)   tiempo (s)   ops/s aprox
     1,000       10       0.0095       1.06e+07
    10,000       14       0.1935       5.17e+06
   100,000       17       1.4633       6.83e+06
 1,000,000       20      17.1219       5.84e+06
```

El tiempo crece con `W` aproximadamente de forma lineal. Al multiplicar `W` por 10 (es decir, sumando entre 3 y 4 bits), el tiempo se multiplica por un factor entre 7 y 20, dependiendo del ruido de la máquina y del intérprete. En cualquier caso, la tendencia es clara:

```text
W:   10^3 → 10^4 → 10^5 → 10^6
t:   1×    → 20×   → 150×  → 1800×
bits: 10   → 14    → 17    → 20
```

**W se multiplica por 10, los bits suman 3.32, y el tiempo se multiplica por un factor cercano a 10**. El tiempo `es ≈ W = 2^bits`. La firma de la exponencial en bits: sumar bits multiplica el costo, en lugar de sumar una cantidad constante.

**El caso extremo.** En esta implementación `(≈ 6 × 10⁶ ops/s)`, un año son `3.15 × 10⁷ s`, lo que permite `3.15 × 10⁷ · 6 × 10⁶ ≈ 1.9 × 10¹⁴` operaciones. Con `n = 100`, el DP necesita `W ≈ 1.9 × 10¹²`, que se codifica en **41 bits**. Suponiendo que los pesos y valores también ocupan unos 41 bits, la entrada total es de `100 · 2 · 41 + 41 = 8241 bits` (unos 1 KB), y el DP hace `100 · 1.9 × 10¹² = 1.9 × 10¹⁴` operaciones: diez órdenes de magnitud más que el número de bits de la entrada. Esa es la esencia de la pseudopolinomialidad: la entrada es minúscula, pero el algoritmo itera sobre un valor que es exponencial en sus bits.

**La tabla de memoria también explota.** La versión con tabla completa usa `(n+1)(W+1)` celdas. Para `n = 100` y `W = 10⁹`, son `10¹¹` celdas, que a 8 bytes cada una son **800 GB**. La versión rolling lo reduce a `W = 10⁹` celdas = **8 GB**, aún así inmanejable en una computadora común. Para `W = 10¹²`, ni hablar.

---

## 7. La comparación con la primalidad por división

La Conferencia 1 mostró que probar divisores hasta `√n` cuesta `O(√n)` operaciones, pero el tamaño de la entrada es `b = log₂ n` bits, así que en función de `b` cuesta `O(2^(b/2))`, que es exponencial. La mochila tiene exactamente la misma estructura.

**Tabla comparativa.**

| | Primalidad por división | Mochila con DP |
|---|---|---|
| Número "grande" de la entrada | `n` (el número a testear) | `W` (la capacidad) |
| Tamaño en bits | `b = ⌈log₂ n⌉` | `b = ⌈log₂ W⌉` (o `log₂ M`) |
| Costo del algoritmo | `O(√n) = O(2^(b/2))` | `O(nW) = O(n · 2^b)` |
| ¿Polinomial en el valor? | Sí, `O(√n)` es `O(n)` | Sí, `O(nW)` es `O(n·W)` |
| ¿Polinomial en los bits? | **No**, exponencial en `b/2` | **No**, exponencial en `b` |
| Clasificación | **Pseudopolinomial** | **Pseudopolinomial** |
| ¿Hay algoritmo polinomial en bits? | **Sí**, AKS (2002) y Miller-Rabin (aleatorio) | **No se conoce**; si `P≠NP`, no existe |

**El paralelismo, paso a paso.**

1. **El número grande no está "en la entrada" como cantidad.** En primalidad, `n` no aparece como `n` celdas; aparece como `b = log₂ n` bits. En mochila, `W` no aparece como `W` celdas; aparece como `b = log₂ W` bits.
2. **El algoritmo itera sobre el valor, no sobre los bits.** La división prueba `√n` divisores (valor), no `b` bits. El DP recorre `W` columnas (valor), no `b` bits.
3. **El costo es polinomial en el valor pero exponencial en los bits.** `√n = 2^(b/2)` y `W = 2^b`. En ambos casos, el exponente crece con `b`.
4. **Por eso se llaman pseudopolinomiales.** Son polinomiales en una medida que no es el tamaño de la entrada, y exponenciales en la medida correcta (bits).

**La diferencia.**

- Para primalidad, la pseudopolinomialidad es una **limitación del algoritmo**, no del problema. Desde 2002 se sabe que primalidad está en `P` (AKS), y ya en los 70 se conocía Miller-Rabin (aleatorio polinomial). El problema **no** es intrínsecamente difícil.
- Para mochila, la pseudopolinomialidad es una **propiedad del problema** (asumiendo `P ≠ NP`). La mochila 0/1 es NP-completa, y si tuviera un algoritmo polinomial en bits, entonces `P = NP`. El DP `O(nW)` es lo mejor que se puede hacer en el caso general, y su exponencialidad en bits es **inevitable** (bajo la conjetura estándar).

**En una frase.** Los dos son pseudopolinomiales; la primalidad tenía una salida, la mochila no la tiene (si `P ≠ NP`).
