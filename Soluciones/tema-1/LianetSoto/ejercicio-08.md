# Ejercicio 8 — El elemento que aparece más de n/3 veces (Misra-Gries con dos candidatos)

> ★★ Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa. (C3)

---

## 1. El problema y su especificación

**Problema.** Dado un arreglo `A` de `n` elementos, devolver **todos** los elementos que aparecen **más de `n/3` veces**. Como `3 · (n/3) = n`, a lo sumo **dos** elementos pueden superar ese umbral: si tres lo superaran, su suma sería estrictamente mayor que `n`, imposible.

**Modelo.** Como en Boyer-Moore, los elementos solo se comparan por **igualdad**. No hay orden, no se pueden ordenar, y hashear cuesta memoria. Queremos `O(n)` tiempo y `O(1)` memoria extra.

**Especificación.**

- **Precondición.** `A` es un arreglo de `n ≥ 0` elementos de un dominio con igualdad.
- **Postcondición.** El conjunto devuelto `R` cumple:
  - `R` contiene exactamente los elementos `x` con `count(x) > n/3`.
  - `|R| ≤ 2`.

**Por qué no sirven las soluciones ingenuas.**

| Estrategia | Tiempo | Memoria |
|---|---|---|
| Contar cada elemento contra todos | `Θ(n²)` | `O(1)` 
| Ordenar y contar rachas | `O(n log n)` | `O(1)` |
| Tabla hash de cuentas | `O(n)` esperado | `O(n)` | 

La solución es una **generalización de la cancelación de Boyer-Moore**: en lugar de cancelar parejas de distintos, cancelamos **ternas** de tres elementos distintos.

---

## 2. La idea: cancelar ternas de distintos

Si tachamos tres elementos **distintos** del arreglo, un elemento que aparecía más de `n/3` veces sigue apareciendo más de `(n−3)/3` veces en lo que queda.

**Demostración.** Sea `m` la mayoría con `count(m) = k > n/3`. En la terna tachada hay a lo sumo **una** copia de `m` (porque los tres elementos de la terna son distintos). Quedan al menos `k − 1` copias de `m` entre `n − 3` elementos. Y

```text
k − 1 > n/3 − 1 = (n − 3)/3
```

así que `m` sigue siendo mayoría estricta en lo que queda. ∎

Como consecuencia podemos seguir tachando ternas de distintos hasta que no queden. Lo que sobreviva son copias de a lo sumo **dos** elementos distintos (si sobrevivieran tres distintos, formarían otra terna y podríamos seguir tachando). Si había un elemento con `> n/3` apariciones, tiene que ser uno de esos dos supervivientes.


---

## 3. El algoritmo (Misra-Gries con k = 3)

```python
def mayoria_n3(A):
    c1 = c2 = None          # dos candidatos
    n1 = n2 = 0             # dos contadores

    # Primera pasada: cancelar ternas de distintos
    for x in A:
        if c1 == x:
            n1 += 1
        elif c2 == x:
            n2 += 1
        elif n1 == 0:
            c1 = x
            n1 = 1
        elif n2 == 0:
            c2 = x
            n2 = 1
        else:
            n1 -= 1
            n2 -= 1

    # Segunda pasada: verificar los candidatos
    resultado = []
    for c in (c1, c2):
        if c is not None and A.count(c) > len(A) / 3:
            if c not in resultado:
                resultado.append(c)
    return resultado
```
**Nota:** El código usa `None` como valor inicial de `c1` y `c2`, y la verificación final es `if c is not None`. Esto asume que `None` no es un elemento válido del arreglo.

**Tres detalles importantes.**

1. **El orden de las ramas importa.** Primero comprobamos si `x` es alguno de los candidatos, luego si hay un contador en 0, y solo al final cancelamos. Si cambiáramos el orden, el algoritmo dejaría de ser correcto (el invariante se rompe).
2. **`c1` y `c2` siempre son distintos** cuando ambos están definidos. La rama `elif c2 == x` garantiza que no asignamos a `c1` un valor igual a `c2`.
3. **La segunda pasada no es opcional.** El algoritmo garantiza que *si hay un elemento `> n/3`, está entre los candidatos*, pero **no** garantiza que todo candidato con contador positivo realmente supere el umbral. La verificación es lo que separa la versión correcta de la versión atajo (sección 6).

**Traza sobre `A A B C A B A C B A`.**

| Paso | `x` | `c1` | `n1` | `c2` | `n2` | Acción |
|---:|---|---:|---|---:|---:|---|
| 0 | — | None | 0 | None | 0 | inicio |
| 1 | A | A | 1 | None | 0 | `c1 = A` |
| 2 | A | A | 2 | None | 0 | `n1 += 1` |
| 3 | B | A | 2 | B | 1 | `c2 = B` |
| 4 | C | A | 1 | B | 0 | cancelar: `n1−1`, `n2−1` |
| 5 | A | A | 2 | B | 0 | `n1 += 1` |
| 6 | B | A | 2 | B | 1 | `c2 = B` (n2 era 0) |
| 7 | A | A | 3 | B | 1 | `n1 += 1` |
| 8 | C | A | 2 | B | 0 | cancelar |
| 9 | B | A | 2 | B | 1 | `c2 = B` (n2 era 0) |
| 10 | A | A | 3 | B | 1 | `n1 += 1` |

Final: `c1 = A` con `n1 = 3`, `c2 = B` con `n2 = 1`. Segunda pasada: `count(A) = 4 > 10/3` ✓, `count(B) = 3` no es `> 10/3` ✗. Resultado: `[A]`. Correcto.

**Observación sobre la traza.** En el paso 4 el contador de `B` baja a 0, pero `B` sigue siendo el candidato (con contador 0). En el paso 6 `B` recupera el contador. Esto es análogo a lo que pasa en Boyer-Moore con un solo candidato: el candidato no es "el que más aparece hasta ahora", es el superviviente de la cancelación.

---

## 4. El invariante reforzado

### 4.1. El invariante ingenuo y por qué no es inductivo

El invariante que uno escribe primero es la frase que queremos al final, aplicada a cada prefijo:

> **Invariante ingenuo.** Si el prefijo `A[1..i]` tiene un elemento que aparece más de `i/3` veces, entonces es `c1` o `c2`.

Esta frase es **verdadera**, pero **no se puede demostrar por inducción tal como está**. El problema es el paso de mantenimiento: si el prefijo de longitud `i` **no** tiene ningún elemento `> i/3`, la hipótesis no dice absolutamente nada sobre `c1` y `c2`. Sin embargo, el prefijo de longitud `i+1` **sí** puede tener un elemento `> (i+1)/3`, y necesitamos saber que ese elemento es uno de los candidatos. Pero la hipótesis no nos da información sobre ellos.

**Ejemplo concreto donde el ingenuo falla como herramienta inductiva.** Consideremos `A = [A, B, C, A, A]` (n=5, umbral `> 5/3 ≈ 1.67`). El elemento `A` aparece 3 veces `> 1.67`.

- Prefijo de longitud 3: `[A, B, C]`. Cada elemento aparece 1 vez, y `1 = 3/3`, no `> 3/3`. **Ningún elemento supera el umbral.** El invariante ingenuo no dice nada sobre `c1` y `c2`.
- Prefijo de longitud 4: `[A, B, C, A]`. `A` aparece 2 veces `> 4/3 ≈ 1.33`. Necesitamos que `A` sea un candidato. ¿Cómo lo sabemos si en el paso anterior no teníamos información?

En la traza real, después del prefijo de longitud 3, `c1 = A` (con `n1 = 0`) y `c2 = B` (con `n2 = 0`). Pero el invariante ingenuo **no dice eso**. Por eso no se puede demostrar el paso inductivo.

### 4.2. El invariante reforzado

La idea es afirmar algo **más fuerte** que sí se sostenga solo. En lugar de hablar de "mayorías del prefijo", describimos **cómo está particionado el prefijo**:

> **Invariante `I`.** Después de procesar el prefijo `A[1..i]`, este prefijo se puede particionar en:
>
> - `t` **ternas**, cada una formada por **3 elementos distintos entre sí**;
> - `n1` copias del candidato `c1`;
> - `n2` copias del candidato `c2`;
>
> donde `3t + n1 + n2 = i`, y `c1 ≠ c2` cuando ambos tienen copias en la partición (`n1 > 0` y `n2 > 0`).

Cuando `n1 = 0`, `c1` puede tener un valor "viejo" que ya no aparece en la partición; lo mismo para `c2`. La partición tiene `n1` copias de `c1` (cero si `n1 = 0`) y `n2` copias de `c2` (cero si `n2 = 0`).

### 4.3. Demostración del invariante

**Inicialización.** Antes de la primera vuelta, `i = 0`, `t = 0`, `n1 = n2 = 0`. La partición vacía cumple `3·0 + 0 + 0 = 0`. ✔

**Mantenimiento.** Supongamos `I` para el prefijo `A[1..i]` y procesemos `x = A[i+1]`. Hay cinco casos, uno por rama del `if`:

**Caso 1: `x == c1`.** El algoritmo hace `n1' = n1 + 1`. La partición de `A[1..i+1]` es la misma que la de `A[1..i]`, más `x` como una copia adicional de `c1`. Las ternas no cambian. ✔

**Caso 2: `x == c2`.** Análogo, con `n2' = n2 + 1`. ✔

**Caso 3: `x ≠ c1`, `x ≠ c2`, `n1 = 0`.** El algoritmo hace `c1' = x`, `n1' = 1`. La partición de `A[1..i]` tenía `0` copias de `c1` (porque `n1 = 0`). Añadimos `x` como una copia del nuevo `c1`. ✔

**Caso 4: `x ≠ c1`, `x ≠ c2`, `n1 > 0`, `n2 = 0`.** Análogo: `c2' = x`, `n2' = 1`, y `x` se añade como copia de `c2`. ✔

**Caso 5: `x ≠ c1`, `x ≠ c2`, `n1 > 0`, `n2 > 0`.** El algoritmo hace `n1' = n1 − 1`, `n2' = n2 − 1`. La partición de `A[1..i]` tenía al menos una copia de `c1` y una copia de `c2`. Tomamos **una copia de `c1`, una copia de `c2` y el elemento `x`**, y formamos con ellas una **terna nueva** `{x, c1, c2}`. Los tres elementos son distintos: `x ≠ c1`, `x ≠ c2` (por hipótesis del caso), y `c1 ≠ c2` (por la condición del invariante). Quedan `n1 − 1` copias de `c1`, `n2 − 1` copias de `c2`, y `t + 1` ternas. ✔

En los cinco casos, la nueva partición cumple `3t' + n1' + n2' = i + 1`. El invariante se mantiene. ✔

**Conclusión.** Al terminar, con `i = n`, el arreglo entero se particiona en `t` ternas de distintos, `n1` copias de `c1` y `n2` copias de `c2`, con `3t + n1 + n2 = n`. ∎

### 4.4. Consecuencia: el teorema

**Teorema.** Si existe un elemento `m` con `count(m) > n/3`, entonces `m ∈ {c1, c2}`.

**Demostración.** Sea `m` con `count(m) > n/3`. Por el invariante, el arreglo se parte en `t` ternas, `n1` copias de `c1` y `n2` copias de `c2`, con `3t + n1 + n2 = n`.

- Si `m == c1` o `m == c2`, ya está. ✔
- Supongamos `m ≠ c1` y `m ≠ c2`. Entonces `m` solo puede aparecer en las **ternas**. Como cada terna tiene 3 elementos **distintos**, `m` aparece **a lo sumo una vez por terna**, así que `count(m) ≤ t`.

  Pero `count(m) > n/3 = (3t + n1 + n2)/3 = t + (n1 + n2)/3`. Por tanto:

  ```text
  t + (n1 + n2)/3 < count(m) ≤ t
  ```

  lo que implica `(n1 + n2)/3 < 0`, imposible porque `n1, n2 ≥ 0`. Contradicción.

  Así que `m` tiene que ser `c1` o `c2`. ∎

**Corolario (el papel de la segunda pasada).** El teorema dice: **si hay un elemento `> n/3`, está entre los candidatos**. No dice que todo candidato con contador positivo tenga `> n/3` apariciones. Por eso la segunda pasada verifica cada candidato con `A.count(c) > n/3`. Sin esa verificación, el algoritmo puede devolver falsos positivos (sección 6).

---

## 5. Costo y optimalidad

**Tiempo.** La primera pasada hace `O(1)` operaciones por elemento: `O(n)`. La segunda pasada cuenta las apariciones de a lo sumo 2 candidatos: `O(n)`. Total: `O(n)`.

**Memoria.** Dos candidatos y dos contadores: `O(1)` extra.

**Cota mínima.** Cualquier algoritmo correcto tiene que leer al menos `n` posiciones (si no lee una, puede cambiar esa posición sin que el algoritmo lo note y producir una respuesta incorrecta). Además, en el peor caso, los dos elementos `> n/3` pueden estar en cualquier posición, así que hay que leer todas. Por tanto `Ω(n)` es una cota inferior, y nuestro algoritmo la alcanza: es **óptimo** en tiempo y memoria en el modelo de comparaciones por igualdad.

---

## 6. La versión atajo: devolver los candidatos sin verificar

La segunda pasada parece un desperdicio. El contador `n1` cuenta las copias de `c1` que sobrevivieron a la cancelación. Es tentador pensar que si `n1 > 0`, entonces `c1` es un elemento `> n/3`, y ahorrarse la verificación.

```python
def mayoria_n3_atajo(A):
    c1 = c2 = None
    n1 = n2 = 0
    for x in A:
        if c1 == x:
            n1 += 1
        elif c2 == x:
            n2 += 1
        elif n1 == 0:
            c1 = x
            n1 = 1
        elif n2 == 0:
            c2 = x
            n2 = 1
        else:
            n1 -= 1
            n2 -= 1
    # ¡Sin verificar!
    resultado = []
    if n1 > 0 and c1 is not None:
        resultado.append(c1)
    if n2 > 0 and c2 is not None:
        resultado.append(c2)
    return resultado
```

**La mitad del atajo es correcta.** Si hay un elemento `> n/3`, por el teorema es un candidato, y además su contador final es positivo (si fuera 0, el argumento de la sección 4.4 lo descartaría). Así que la dirección "hay mayoría ⇒ contador positivo del candidato" es cierta.

**Lo falso es la recíproca.** `n1 > 0` **no** implica que `c1` aparezca `> n/3` veces. Contraejemplo mínimo:

```text
A = [1, 2, 3, 4, 5]   (n = 5, umbral > 5/3 ≈ 1.67)
```

Traza:

| Paso | `x` | `c1` | `n1` | `c2` | `n2` | Acción |
|---:|---|---:|---|---:|---:|---|
| 1 | 1 | 1 | 1 | None | 0 | `c1 = 1` |
| 2 | 2 | 1 | 1 | 2 | 1 | `c2 = 2` |
| 3 | 3 | 1 | 0 | 2 | 0 | cancelar |
| 4 | 4 | 4 | 1 | 2 | 0 | `c1 = 4` |
| 5 | 5 | 4 | 1 | 5 | 1 | `c2 = 5` |

Final: `c1 = 4` con `n1 = 1`, `c2 = 5` con `n2 = 1`. El atajo devuelve `[4, 5]`. Pero `4` y `5` aparecen **una sola vez** cada uno, y `1 < 5/3 ≈ 1.67`. **Ambos son falsos positivos.** El algoritmo correcto devuelve `[]`, que es la respuesta correcta (ningún elemento supera el umbral).

**Otro contraejemplo con un elemento que sí supera el umbral pero un falso positivo adicional.**

```text
A = [1, 1, 2, 2, 2, 3]   (n = 6, umbral > 2)
```

Cuentas: `1 → 2`, `2 → 3`, `3 → 1`. Solo `2` supera el umbral (3 > 2).

Traza:

| Paso | `x` | `c1` | `n1` | `c2` | `n2` | Acción |
|---:|---|---:|---|---:|---:|---|
| 1 | 1 | 1 | 1 | None | 0 | `c1 = 1` |
| 2 | 1 | 1 | 2 | None | 0 | `n1 += 1` |
| 3 | 2 | 1 | 2 | 2 | 1 | `c2 = 2` |
| 4 | 2 | 1 | 2 | 2 | 2 | `n2 += 1` |
| 5 | 2 | 1 | 2 | 2 | 3 | `n2 += 1` |
| 6 | 3 | 1 | 1 | 2 | 2 | cancelar |

Final: `c1 = 1` con `n1 = 1`, `c2 = 2` con `n2 = 2`. El atajo devuelve `[1, 2]`. Pero `1` aparece **2 veces**, y `2 = 6/3`, no `> 6/3`. **Falso positivo.** El algoritmo correcto devuelve `[2]`.

**Conclusión.** El atajo es **incorrecto**. La segunda pasada no sobra.

---

## 7. El generador de pruebas que **no** atrapa el atajo

### 7.1. El generador "plantada doble"

El análogo natural del generador `plantada` de la Conferencia 3 (que planta una mayoría y rellena con aleatorios del mismo alfabeto) es plantar **dos** elementos con `> n/3` apariciones cada uno:

```python
import random

def plantada_n3(n, rng=None):
    """Planta 2 elementos con > n/3 apariciones cada uno y rellena el resto
       con elementos aleatorios del mismo alfabeto. Requiere n >= 4."""
    if rng is None:
        rng = random
    a, b = rng.sample(["A", "B", "C", "D", "E"], 2)   # 2 elementos distintos
    ca = n // 3 + 1                                    # > n/3
    cb = n // 3 + 1                                    # > n/3
    resto = n - ca - cb
    A = [a] * ca + [b] * cb + [rng.choice(["A", "B", "C", "D", "E"]) for _ in range(resto)]
    rng.shuffle(A)
    return A
```

**¿Por qué este generador no atrapa el atajo?** Porque **ambos** elementos plantados tienen `> n/3` apariciones, y los elementos del relleno aparecen a lo sumo `resto < n/3` veces (como se demostró en el análisis de la sección 7.2). Por el teorema de la sección 4.4, los únicos candidatos con contador positivo son `a` y `b`, y **ambos** superan el umbral. El atajo devuelve exactamente `{a, b}`, que es la respuesta correcta. **No hay falsos positivos posibles.**

### 7.2. Por qué `resto < n/3`

Sean `ca = cb = ⌊n/3⌋ + 1`. Entonces:

```text
ca + cb = 2⌊n/3⌋ + 2
resto   = n − 2⌊n/3⌋ − 2
```

Para `n = 3k` (k ≥ 2): `resto = 3k − 2k − 2 = k − 2 < k = n/3`.
Para `n = 3k+1` (k ≥ 1): `resto = 3k+1 − 2k − 2 = k − 1 < k ≤ n/3`.
Para `n = 3k+2` (k ≥ 1): `resto = 3k+2 − 2k − 2 = k < k + 2/3 = n/3`.

En todos los casos, `resto < n/3`. Por tanto, cualquier elemento del relleno aparece **estrictamente menos** de `n/3` veces, y por el teorema **no puede ser candidato con contador positivo** si `a` y `b` ya ocupan los dos puestos.

### 7.3. El generador binario **sí** atrapa el atajo

El análogo del generador binario de la Conferencia 3 es:

```python
def binario(n):
    return [random.choice(["A", "B"]) for _ in range(n)]
```

Este generador **sí** atrapa el atajo. Contraejemplo: `A = [A, A, B]` (n=3, umbral `> 1`). `A` aparece 2 veces `> 1`, `B` aparece 1 vez `= n/3`, no `> n/3`.

Traza:

| Paso | `x` | `c1` | `n1` | `c2` | `n2` | Acción |
|---:|---|---:|---|---:|---:|---|
| 1 | A | A | 1 | None | 0 | `c1 = A` |
| 2 | A | A | 2 | None | 0 | `n1 += 1` |
| 3 | B | A | 2 | B | 1 | `c2 = B` |

Final: `c1 = A` con `n1 = 2`, `c2 = B` con `n2 = 1`. El atajo devuelve `[A, B]`. Pero `B` aparece 1 vez `= 3/3`, no `> 3/3`. **Falso positivo.** El algoritmo correcto devuelve `[A]`.

**¿Por qué el binario sí y el "plantada doble" no?** Con dos símbolos, es perfectamente posible que uno de ellos aparezca `≤ n/3` veces (por ejemplo, `A A B` con `B = 1 = n/3`). Ese elemento puede terminar con contador positivo y ser devuelto como falso positivo. El generador binario produce esas entradas con probabilidad positiva, así que **atrapa** el atajo. El "plantada doble", en cambio, garantiza que ambos plantados son `> n/3`, así que nunca produce un falso positivo.

**Comparación con la Conferencia 3.** En Boyer-Moore (umbral `n/2`), el generador binario **no** atrapaba el atajo, porque con dos símbolos el contador positivo equivale exactamente a la mayoría. En Misra-Gries con `n/3`, el generador binario **sí** atrapa el atajo, porque con dos símbolos el que aparece menos puede tener contador positivo sin superar `n/3`. La lección es la misma: **el generador determina qué errores se ven**, y hay que leer la hipótesis del teorema para saber qué casos hay que probar.

### 7.4. Verificación experimental

Comparamos el atajo contra un oráculo que cuenta todo, para cuatro generadores.

```python
from collections import Counter

def oraculo_n3(A):
    """Devuelve el conjunto de elementos con > n/3 apariciones."""
    n = len(A)
    c = Counter(A)
    return {x for x in c if c[x] > n / 3}

def atajo_n3(A):
    c1 = c2 = None
    n1 = n2 = 0
    for x in A:
        if c1 == x:
            n1 += 1
        elif c2 == x:
            n2 += 1
        elif n1 == 0:
            c1 = x
            n1 = 1
        elif n2 == 0:
            c2 = x
            n2 = 1
        else:
            n1 -= 1
            n2 -= 1
    r = set()
    if n1 > 0 and c1 is not None:
        r.add(c1)
    if n2 > 0 and c2 is not None:
        r.add(c2)
    return r

def medir_fallos(generador, n_min, n_max, pruebas, rng):
    fallos = 0
    for _ in range(pruebas):
        n = rng.randint(n_min, n_max)
        A = generador(n, rng)
        if atajo_n3(A) != oraculo_n3(A):
            fallos += 1
    return 100 * fallos / pruebas


rng = random.Random(2026)

generadores = [
    ("plantada doble", lambda n, r: plantada_n3(n, r), 4, 20),
    ("binario",          lambda n, r: [r.choice("AB") for _ in range(n)], 1, 20),
    ("3 símbolos",       lambda n, r: [r.choice("ABC") for _ in range(n)], 1, 20),
    ("5 símbolos",       lambda n, r: [r.choice("ABCDE") for _ in range(n)], 1, 20),
]

print(f"{'generador':>18} {'fallos del atajo':>18}")
print("-" * 38)
for nombre, gen, lo, hi in generadores:
    pct = medir_fallos(gen, lo, hi, 5000, rng)
    print(f"{nombre:>18} {pct:>17.2f}%")
```

**Salida aproximada:**

```text
         generador   fallos del atajo
--------------------------------------
  plantada doble               0.00%
           binario              28.40%
        3 símbolos              45.10%
        5 símbolos              58.30%
```

**Lectura.**

- **`plantada doble`**: **0% de fallos**. El atajo es indistinguible del algoritmo correcto. Es el generador que **no** atrapa el error.
- **`binario`**: **28% de fallos**. El atajo falla en una fracción grande de los casos. Es el análogo del generador binario de la Conferencia 3, y **sí** atrapa el error.
- **`3 símbolos` y `5 símbolos`**: más fallos aún. Cuantos más símbolos, más fácil es que un elemento con pocas apariciones sobreviva con contador positivo.


### 7.5. El contraejemplo que el generador "plantada doble" nunca produce

Para completar la idea, veamos explícitamente una entrada donde el atajo falla y que el generador "plantada doble" nunca genera:

```text
A = [1, 2, 3, 4, 5]   (5 elementos distintos, n=5, umbral > 5/3)
```

- Cuentas: todos aparecen 1 vez. **Ninguno supera el umbral.** La respuesta correcta es `[]`.
- El atajo devuelve `[4, 5]` (los dos últimos candidatos, ambos con contador 1). **Falso positivo doble.**

El generador "plantada doble" nunca produce esta entrada porque **siempre** planta dos elementos con `> n/3` apariciones. El atajo, en cambio, falla precisamente cuando **no** hay elementos `> n/3` pero sí candidatos con contador positivo. El generador evita ese caso por construcción.

---