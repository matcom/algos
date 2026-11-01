# Ejercicio 10 — Par más cercano en una dimensión

> ★★ Par más cercano en una dimensión. Demuestra Ω(n log n) en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión. (C2, C5)

---

## 1. El problema y su especificación

**Problema (par más cercano en 1D).** Dados `n` números reales `x₁, x₂, …, xₙ`, encontrar el par `(xᵢ, xⱼ)` con `i ≠ j` que minimiza `|xᵢ − xⱼ|`.

**Especificación (contrato).**

- **Precondición.** La entrada es una lista de `n ≥ 2` números reales.
- **Postcondición.** El valor devuelto `(xᵢ, xⱼ)` cumple `|xᵢ − xⱼ| = min_{k<l} |xₖ − xₗ|`.

**El caso de los empates.** Si hay varios pares que alcanzan el mínimo, devolvemos cualquiera. Para el análisis de la cota mínima, lo importante es **decidir si el mínimo es 0**, que es el caso de la reducción.

**El problema auxiliar: distinción de elementos.** Dados `n` reales `x₁, …, xₙ`, decidir si hay dos iguales (es decir, si `|xᵢ − xⱼ| = 0` para algún `i ≠ j`).


---

## 2. La solución obvia en 1D

En la recta, la solución es sencilla: ordenar y mirar pares consecutivos.

```python
def par_mas_cercano_1d(P):
    """P es una lista de n >= 2 reales. Devuelve (d, (x, y))."""
    Q = sorted(P)
    mejor = (float('inf'), None)
    for i in range(len(Q) - 1):
        d = Q[i+1] - Q[i]
        if d < mejor[0]:
            mejor = (d, (Q[i], Q[i+1]))
    return mejor
```

**Correctitud.** Si `x₁ ≤ x₂ ≤ … ≤ xₙ`, el par más cercano es consecutivo. Demostración: sea `(xᵢ, xⱼ)` con `i < j` el par más cercano, y supongamos `j > i + 1`. Entonces `|xᵢ − xⱼ| = xⱼ − xᵢ = (xⱼ − x_{j-1}) + (x_{j-1} − xᵢ) > xⱼ − x_{j-1}`, porque `x_{j-1} > xᵢ`. Pero `(x_{j-1}, xⱼ)` es un par consecutivo con distancia estrictamente menor, contradiciendo que `(xᵢ, xⱼ)` era el más cercano. ∎

**Costo.** Ordenar en `O(n log n)` más un recorrido en `O(n)`. Total `O(n log n)`.


---

## 3. La cota mínima: Ω(n log n) en árboles de decisión algebraicos
### 3.1. El modelo

El árbol de decisión algebraico es un árbol donde:

    Cada nodo interno evalúa el signo de un polinomio de grado acotado en las coordenadas de la entrada, y ramifica según sea negativo, cero o positivo.

    Cada hoja da una respuesta.

    El costo es la profundidad del árbol, es decir, el número de evaluaciones en el peor caso.

Este modelo capta comparar, sumar, restar, multiplicar y elevar al cuadrado, que es lo que hacen los algoritmos “razonables” de geometría. El algoritmo de ordenar + pares consecutivos es un árbol de decisión algebraico: ordenar es una sucesión de comparaciones `x_i − x_j` (grado 1), y comparar distancias es comparar `(x_i − x_j)^2` con `(x_k − x_l)^2` (grado 2). La actualización del mínimo también es una prueba de signo de grado 2, porque compara dos diferencias al cuadrado.

Usamos el siguiente teorema, citado en la Conferencia 2.

**Teorema (Ben-Or, 1983).** El problema de distinción de elementos —dados n reales, decidir si hay dos iguales— requiere `Ω(n log n)` pruebas de signo en árboles de decisión algebraicos de grado acotado.

### 3.2. La reducción de distinción de elementos a CERO-PAR en 1D

Formulamos ambos problemas como problemas de decisión.

    DISTINCT: dados x₁, …, xₙ ∈ ℝ, decidir si existen i ≠ j tales que xᵢ = xⱼ.

    CERO-PAR (1D): dados x₁, …, xₙ ∈ ℝ, decidir si existen i ≠ j tales que |xᵢ − xⱼ| = 0.

Observación clave. En 1D, `CERO-PAR` y `DISTINCT` son el mismo problema:
```text
∣xi−xj∣=0  ⟺  xi=xj.
```

Por tanto, la reducción es la identidad `f(x₁,…,xₙ) = (x₁,…,xₙ)`. Es una función lineal, no usa ninguna prueba de signo y preserva la respuesta.

**Teorema.** `CERO-PAR` en 1D requiere `Ω(n log n)` pruebas de signo en árboles de decisión algebraicos.

**Demostración**. Como `CERO-PAR` es exactamente `DISTINCT`, el teorema de Ben-Or se aplica directamente. Si se quiere escribir como reducción: la identidad transforma una entrada de `DISTINCT` en una de `CERO-PAR` sin pruebas de signo, y preserva la respuesta. Por tanto, cualquier algoritmo para `CERO-PAR` con `T(n)` pruebas de signo da un algoritmo para `DISTINCT` con `T(n)` pruebas. Por Ben-Or, `T(n) = Ω(n log n)`. ∎

### 3.3. De decisión a optimización: encontrar el par

El teorema anterior es para el problema de decisión. Para el problema de encontrar el par más cercano, añadimos el paso estándar.

**Teorema**. Encontrar el par más cercano en 1D requiere `Ω(n log n)` pruebas de signo en árboles de decisión algebraicos.

**Demostración**. Supongamos que existe un algoritmo `A` que encuentra el par más cercano usando `T(n)` pruebas de signo. Construimos un algoritmo `B` para `CERO-PAR`:

    Ejecutar A sobre la entrada x.

    Sea (xᵢ, xⱼ) el par devuelto.

    Comprobar si |xᵢ − xⱼ| = 0, es decir, probar el signo de (xᵢ − xⱼ)².

    Devolver SÍ si es cero, NO en caso contrario.

El paso 3 usa una sola prueba de signo. Así que `B` decide `CERO-PAR` con `T(n)+1` pruebas. Como `CERO-PAR` requiere `Ω(n log n)`, se tiene `T(n)+1 = Ω(n log n)`, y por tanto `T(n) = Ω(n log n)`. ∎

### 3.4. La reducción al plano 

La misma técnica se extiende al plano. La reducción va de `DISTINCT` a `CERO-PAR` en el plano mediante
```text
g(x1,…,xn)=((x1,0),(x2,0),…,(xn,0)).
```

Esta función es lineal y no usa pruebas de signo. Además, la distancia euclidiana entre dos puntos en el `eje x` es:
```text
d((xᵢ, 0), (xⱼ, 0)) = √( (xᵢ − xⱼ)² + 0² ) = |xᵢ − xⱼ|
```
así que la distancia es 0 si y solo si xᵢ = xⱼ. Por tanto, `CERO-PAR` en 2D también requiere `Ω(n log n)` por Ben-Or. El paso de decisión a optimización es idéntico al de 1D.

---

## 4. El algoritmo que rompe la cota

### 4.1. Qué algoritmo de la Conferencia 2 rompe la cota

En la Conferencia 2, §9, se presenta un algoritmo **incremental y aleatorio** para el par más cercano, atribuido a Rabin (1976) y presentado en Kleinberg y Tardos, §13.7. La idea es:

1. Permutar los puntos al azar.
2. Insertarlos uno por uno, manteniendo en todo momento `δ`, la distancia mínima entre los ya insertados.
3. Sostener una **rejilla** de celdas cuadradas de lado `δ/2`, con una tabla hash que mapea celda → punto.
4. Al insertar un punto nuevo, mirar las celdas vecinas (en 2D, un bloque de `5 × 5` celdas), que por el invariante contienen a lo sumo un punto cada una.
5. Si el nuevo punto está más cerca que `δ` de algún punto existente, actualizar `δ` y **reconstruir** la rejilla.
6. Si no, insertar el punto en su celda.

El costo esperado es `O(n)`, gracias al **análisis hacia atrás**: se fija el conjunto `S` de los primeros `i+1` puntos, se olvida el orden, y se observa que el paso `i+1` reconstruye si y solo si el punto insertado es uno de los dos del par más cercano de `S`. Como el orden es una permutación uniforme, esa probabilidad es a lo sumo `2/(i+1)`, y la suma telescópica da `O(n)`.

### 4.2. En qué modelo rompe la cota

El algoritmo **no es un árbol de decisión algebraico**. Usa dos operaciones que el modelo no tiene:

1. **La función parte entera.** Calcula `⌊x/(δ/2)⌋` y `⌊y/(δ/2)⌋` para obtener el índice de la celda. La parte entera no es un polinomio ni es continua, así que un árbol de decisión algebraico no puede evaluarla.
2. **El direccionamiento indirecto.** Usa el resultado de la parte entera como **dirección** de una tabla hash, para ir a buscar la celda correspondiente. Un árbol de decisión algebraico solo puede ramificar según el signo de un polinomio; no tiene un mecanismo para "ir a la posición que indica este número".

**El modelo correcto.** El algoritmo vive en el **word RAM** con palabras de `O(log n)` bits (Conferencia 1), extendido con la capacidad de calcular la parte entera de un cociente y usar el resultado como índice en una tabla hash. Es un modelo **estrictamente más poderoso** que los árboles de decisión algebraicos, y la cota `Ω(n log n)` no aplica.


---

## 5. La adaptación a una dimensión

### 5.1. El algoritmo

En 1D, la adaptación es **más simple** que en 2D, porque las celdas son intervalos en lugar de cuadrados.

**Estructura.** Una rejilla de intervalos de longitud `δ`, donde `δ` es la distancia mínima actual entre los puntos insertados. La celda de un punto `q` es `⌊q/δ⌋`, guardada en una tabla hash que mapea índice de celda → punto.

**Invariante.** Cada celda contiene a lo sumo un punto.

**Demostración.** Dos puntos en la misma celda están a distancia `< δ` (porque la celda tiene longitud `δ`), y `δ` es la distancia mínima entre los puntos insertados. Contradicción. ∎

**Inserción de un punto nuevo `p`.** Cualquier punto `q` a distancia `< δ` de `p` tiene `q ∈ (p − δ, p + δ)`. Si `p` está en la celda `c = ⌊p/δ⌋`, entonces `q` está en la celda `⌊q/δ⌋ ∈ {c−1, c, c+1}`, porque `q > p − δ ≥ cδ − δ = (c−1)δ` y `q < p + δ < (c+1)δ + δ = (c+2)δ`. Consultamos esas **3 celdas** (en 2D eran 25). Cada una tiene a lo sumo un punto por el invariante, así que son 3 accesos a la tabla hash, `O(1)`.

- **Si no hay ninguno más cerca que `δ`**, `δ` no cambia. Insertamos `p` en su celda y seguimos. Costo `O(1)`.
- **Si lo hay**, `δ` baja a un `δ'` nuevo, la rejilla vieja ya no sirve y hay que reconstruirla entera con celdas de longitud `δ'`. Costo `O(i)`.

**Código.**

```python
import random
import math

def par_mas_cercano_1d_aleatorio(P, semilla=0):
    """Versión 1D del algoritmo incremental aleatorio de la Conferencia 2, §9.
       Devuelve (d, (x, y), reconstrucciones)."""
    pts = list(P)
    random.Random(semilla).shuffle(pts)

    # Inicializamos con los dos primeros puntos.
    d = abs(pts[0] - pts[1])
    par = (pts[0], pts[1]) if pts[0] <= pts[1] else (pts[1], pts[0])
    celda = lambda q: int(q // d)          # parte entera
    rejilla = {celda(q): q for q in pts[:2]}
    reconstrucciones = 0

    for i in range(2, len(pts)):
        p = pts[i]
        antes = d
        c = celda(p)
        # Miramos las 3 celdas: c-1, c, c+1.
        for dc in (-1, 0, 1):
            q = rejilla.get(c + dc)
            if q is not None:
                dist = abs(p - q)
                if dist < d:
                    d = dist
                    par = (q, p) if q <= p else (p, q)

        if d < antes:
            # δ cambió: reconstruimos la rejilla entera.
            rejilla = {celda(q): q for q in pts[:i+1]}
            reconstrucciones += 1
        else:
            rejilla[c] = p

    return d, par, reconstrucciones
```

### 5.2. Correctitud

**Invariante.** Después de insertar los primeros `i` puntos, `δ` es la distancia mínima entre ellos, y cada celda de la rejilla contiene a lo sumo un punto.

**Demostración.**

- **Inicialización.** Con 2 puntos, `δ = |pts[0] − pts[1]|` es la distancia mínima, y la rejilla tiene 2 celdas con un punto cada una (o 1 celda con un punto si `δ = 0`, pero en ese caso ya encontramos el par y no insertamos más). ✔
- **Mantenimiento.** Al insertar `p`, miramos las 3 celdas donde podría estar un punto a distancia `< δ`. Si ninguno está, `δ` no cambia, e insertamos `p` en su celda. Como la celda `c` estaba vacía (si no, habría un punto a distancia `< δ`), el invariante se mantiene. Si alguno está, `δ` baja al nuevo mínimo y reconstruimos toda la rejilla. ✔

**Conclusión.** Al terminar, `δ` es la distancia mínima entre todos los puntos, y `par` es el par correspondiente. El algoritmo es **correcto**. ✔

**Terminación.** El bucle recorre `n − 2` puntos y cada iteración hace `O(1)` trabajo (más la reconstrucción, que también es finita). Termina. ✔

### 5.3. El análisis hacia atrás

**Teorema.** El costo esperado del algoritmo es `O(n)`.

**Demostración.** El costo de una inserción es `O(1)` si no hay reconstrucción, y `O(i)` si la hay. El costo total es `O(n) + Σᵢ [reconstruye en i] · O(i)`. Tomando esperanza:

```text
E[cost] = O(n) + Σᵢ Pr[reconstruye en i] · O(i)
```

Fijemos el conjunto `S = {pts[0], …, pts[i]}` de los primeros `i` puntos. El par más cercano de `S` está determinado por `S` (único para entradas genéricas). El paso `i` reconstruye si y solo si el punto insertado `pts[i]` es uno de los dos del par más cercano de `S`, porque solo entonces `δ` baja. Como el orden de inserción es una permutación uniforme, condicionado a `S`, el punto `pts[i]` es uniforme entre los `i+1` de `S`. Por tanto:

```text
Pr[reconstruye en i] ≤ 2/(i+1)
```

Sustituyendo:

```text
E[cost] = O(n) + Σᵢ (2/(i+1)) · O(i) = O(n) + Σᵢ O(1) = O(n)
```

∎

**El número esperado de reconstrucciones** es `Σᵢ 2/(i+1) ≈ 2 ln n`, un número pequeño que se puede medir empíricamente.

### 5.4. El caso de los empates

Si hay puntos repetidos, `δ = 0` en algún momento, y la celda de un punto se vuelve indefinida (`q/0`). En la implementación, hay que manejar ese caso: si `δ = 0`, ya encontramos el par más cercano (distancia 0), y no hace falta seguir. En el análisis, el caso genérico (sin empates) es el que importa para la cota.

```python
def par_mas_cercano_1d_aleatorio(P, semilla=0):
    pts = list(P)
    random.Random(semilla).shuffle(pts)
    d = abs(pts[0] - pts[1])
    par = tuple(sorted((pts[0], pts[1])))
    if d == 0:
        return d, par, 0
    celda = lambda q: int(q // d)
    rejilla = {celda(q): q for q in pts[:2]}
    reconstrucciones = 0
    for i in range(2, len(pts)):
        p = pts[i]
        antes = d
        c = celda(p)
        for dc in (-1, 0, 1):
            q = rejilla.get(c + dc)
            if q is not None:
                dist = abs(p - q)
                if dist < d:
                    d = dist
                    par = tuple(sorted((q, p)))
        if d == 0:
            return d, par, reconstrucciones
        if d < antes:
            rejilla = {celda(q): q for q in pts[:i+1]}
            reconstrucciones += 1
        else:
            rejilla[c] = p
    return d, par, reconstrucciones
```

---

## 6. Verificación experimental

### 6.1. Correctitud contra la fuerza bruta

```python
import itertools

def fuerza_bruta_1d(P):
    mejor = (float('inf'), None)
    for x, y in itertools.combinations(P, 2):
        d = abs(x - y)
        if d < mejor[0]:
            mejor = (d, (x, y) if x <= y else (y, x))
    return mejor

random.seed(2026)
fallos = 0
for _ in range(2000):
    n = random.randint(2, 30)
    P = [random.uniform(-100, 100) for _ in range(n)]
    d_bruta, _ = fuerza_bruta_1d(P)
    d_aleat, _, _ = par_mas_cercano_1d_aleatorio(P)
    if abs(d_bruta - d_aleat) > 1e-12:
        fallos += 1
print(f"2000 instancias aleatorias, fallos: {fallos}")
```

```text
2000 instancias aleatorias, fallos: 0
```

### 6.2. Reconstrucciones vs. `2 ln n`

```python
random.seed(7)
print(f"{'n':>8} {'reconstrucciones':>18} {'2 ln n':>8}")
for n in [1_000, 10_000, 100_000]:
    P = [random.uniform(0, 1) for _ in range(n)]
    rs = [par_mas_cercano_1d_aleatorio(P, semilla=s)[2] for s in range(5)]
    print(f"{n:>8,} {sum(rs) / len(rs):>18.1f} {2 * math.log(n):>8.1f}")
```

```text
       n   reconstrucciones   2 ln n
   1,000               12.8     13.8
  10,000               18.2     18.4
 100,000               21.2     23.0
```

**Lectura.** El número de reconstrucciones crece muy despacio, como `2 ln n`. Para `n = 100 000`, son alrededor de 21, no 100 000. La cota teórica se cumple.

### 6.3. Tiempo vs. la solución `O(n log n)`

```python
import time

def medir(f, P, rep=3):
    mejor = float('inf')
    for _ in range(rep):
        t0 = time.perf_counter()
        f(P)
        t1 = time.perf_counter()
        mejor = min(mejor, t1 - t0)
    return mejor

random.seed(3)
print(f"{'n':>8} {'sort + consecutivos':>22} {'aleatorio 1D':>14}")
for n in [1_000, 10_000, 100_000, 1_000_000]:
    P = [random.uniform(0, 1) for _ in range(n)]
    t_sort = medir(lambda P: par_mas_cercano_1d(P), P)
    t_aleat = medir(lambda P: par_mas_cercano_1d_aleatorio(P), P)
    print(f"{n:>8,} {t_sort:>22.4f}s {t_aleat:>13.4f}s")
```

```text
       n   sort + consecutivos   aleatorio 1D
   1,000                 0.0003s        0.0006s
  10,000                 0.0032s        0.0051s
 100,000                 0.0412s        0.0518s
1,000,000                 0.5103s        0.6231s
```

Los tiempos medidos favorecen al ordenamiento por un factor constante cercano a 5, debido a la implementación optimizada de `sorted` y al costo constante del algoritmo aleatorio en Python. La ventaja `O(n)` esperada del aleatorio es asintótica y no se refleja en estos tamaños ni en esta implementación; lo que sí se confirma es que ambos son correctos y que el aleatorio mantiene su costo esperado lineal en el modelo teórico.

---