# Ejercicio 14 — Encontrando un Pico Local en un Arreglo

> ★★★ Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan. Es el formato de la pregunta larga del examen final. (C2 a C5)

---

## 1. ¿Cuál es el problema? Especificación

**Problema (Pico Local).** Dado un arreglo `A` de `n` números reales distintos, encontrar el índice `i` de un **pico local**. Un pico local es un elemento que es estrictamente mayor que sus vecinos inmediatos.

**Precisión sobre las fronteras.** Para evitar casos límite engorrosos, definimos dos elementos virtuales (centinelas) en los extremos:
- `A[-1] = -∞`
- `A[n] = -∞`

Formalmente, buscamos un índice `i` (con `0 ≤ i < n`) tal que:
```text
A[i-1] < A[i] > A[i+1]
```

**Modelo.** Trabajamos en el modelo de comparaciones de la conferencia 5: el algoritmo solo accede a los datos mediante preguntas binarias de la forma `A[i] < A[j]`, cada pregunta cuesta 1, y el costo es el número de preguntas en el peor caso. Los centinelas `A[-1] = A[n] = -∞` son una convención para escribir las condiciones de frontera; no son datos del arreglo.

Ejemplo.
```text

A = [1, 3, 5, 4, 2, 8, 6]
```

El elemento `A[2] = 5` es un pico local porque `3 < 5 > 4`.
El elemento `A[5] = 8` también es un pico local porque `2 < 8 > 6`.
La respuesta correcta puede ser cualquiera de los índices 2 o 5.

## 2. ¿Qué algoritmo lo resuelve? 

La solución por fuerza bruta revisaría todos los elementos, lo cual cuesta `O(n)`. Pero podemos hacer algo mucho más inteligente.

**La idea.** Supongamos que en la posición `mid` el vecino derecho es más grande: `A[mid] < A[mid+1]`. Afirmamos que entonces hay un pico en algún lugar de `A[mid+1..n-1]`. La razón es un ascenso que no puede durar para siempre.

Empieza en `mid+1` y avanza a la derecha mientras cada elemento sea mayor que el anterior. La sucesión de valores por la que pasas es estrictamente creciente, y una sucesión estrictamente creciente dentro de un arreglo finito no puede continuar indefinidamente: o se acaba el arreglo, o el siguiente elemento deja de ser mayor. Sea `j` la posición donde se detiene. En los dos casos posibles se cumple `A[j] > A[j+1]`:

    Si j = n-1, entonces A[j+1] es el centinela -∞, y A[j] > -∞.

    Si j < n-1, la subida se detuvo precisamente porque A[j] > A[j+1].

Y como llegamos a `j` subiendo desde `mid+1`, también `A[j] > A[j-1]` (o `j = mid+1`, y entonces `A[j-1] = A[mid] < A[mid+1] = A[j]`). Luego `A[j]` es un pico local, y está en la mitad derecha.

De forma simétrica, si `A[mid] > A[mid+1]`, el mismo ascenso hecho hacia la izquierda se detiene en un pico de `A[0..mid]`, porque el centinela izquierdo también es `-∞`.

**Lo que esto compra**. No sabemos dónde está el pico, pero la comparación `A[mid] < A[mid+1]` nos da un certificado de que hay uno en `[mid+1, hi]`. Con eso podemos descartar la mitad izquierda sin perder la garantía de encontrar un pico. La búsqueda binaria no persigue el pico: mantiene la garantía de que el intervalo actual contiene al menos uno, y cada comparación reduce ese intervalo a la mitad.


## 3. El algoritmo
```python

def buscar_pico(A):
    """
    Dado un arreglo A de n números distintos, devuelve el índice de un pico local.
    Usa centinelas virtuales A[-1] = A[n] = -infinito.
    """
    if not A:
        return -1
        
    lo, hi = 0, len(A) - 1
    
    while lo < hi:
        mid = (lo + hi) // 2
        
        # Comparamos el elemento del medio con su vecino derecho.
        # Si el vecino derecho es mayor, la pendiente sube hacia la derecha.
        if A[mid] < A[mid + 1]:
            lo = mid + 1
        else:
            # A[mid] > A[mid + 1]: la pendiente baja hacia la derecha.
            # Por tanto, el pico debe estar en la mitad izquierda (incluyendo mid).
            hi = mid
            
    # Cuando lo == hi, hemos aislado un pico local.
    return lo
```

## 4. ¿Es correcto? Demostración con invariante (C3)

Para demostrar la correctitud usamos dos invariantes que se mantienen simultáneamente. Son más útiles que el invariante único de "hay un pico en `[lo, hi]`", porque capturan la información que el algoritmo realmente necesita en los bordes.

### 4.1. Los dos invariantes

Definimos, para `0 ≤ lo ≤ hi < n`:

    Invariante 1 (borde izquierdo): A[lo-1] < A[lo], donde A[-1] = -∞.

    Invariante 2 (borde derecho): A[hi] > A[hi+1], donde A[n] = -∞.

**Inicialización.** `lo = 0`, `hi = n-1`.

    I1: A[-1] = -∞ < A[0], porque A[0] es un número real. ✔

    I2: A[n-1] > A[n] = -∞, porque A[n-1] es un número real. ✔

**Mantenimiento.** Supongamos `I1` e `I2` antes de una vuelta. Calculamos `mid = (lo+hi)//2` y hay dos casos:

Caso `A[mid] < A[mid+1]`: el algoritmo hace `lo = mid+1`.

    I1: A[new lo - 1] = A[mid] < A[mid+1] = A[new lo]. ✔

    I2: hi no cambia, así que I2 se mantiene. ✔

Caso `A[mid] > A[mid+1]`: el algoritmo hace `hi = mid`.

    I1: lo no cambia, así que I1 se mantiene. ✔

    I2: A[new hi] = A[mid] > A[mid+1] = A[new hi + 1]. ✔

**Conclusión**. El bucle termina cuando `lo = hi`. Sea `i = lo`. Por `I1`, `A[i-1] < A[i]`; por `I2`, `A[i] > A[i+1]`. Por tanto, `i` es un pico local. ∎

**Terminación.** El intervalo `[lo, hi]` tiene tamaño `hi - lo + 1`, que decrece estrictamente en cada iteración que no termina (porque `mid < hi` cuando `lo < hi`, y tanto `lo = mid+1` como `hi = mid` reducen el tamaño). Como el tamaño es un entero no negativo, el bucle termina en a lo sumo `⌈log₂ n⌉` iteraciones. ✔

## 5. Complejidad

No basta con decir `O(log n)`. Vamos a demostrar que `buscar_pico` hace en el peor caso exactamente `⌈log₂ n⌉` comparaciones, que es lo que la cota inferior de la sección 6 pedirá.

## 5.1. Cota superior para el algoritmo

**Lema (cota superior).** Para todo `k ≥ 1`, cualquier ejecución de `buscar_pico` sobre un intervalo de tamaño `k = hi − lo + 1` hace a lo sumo `⌈log₂ k⌉` comparaciones, independientemente del contenido del arreglo.

**Demostración.** Por inducción sobre `k`.

- **Base.** `k = 1`: el bucle no entra porque `lo = hi`, así que se hacen `0 = ⌈log₂ 1⌉` comparaciones.

- **Paso.** Sea `k ≥ 2` y sea `mid = (lo + hi) // 2`. La única comparación de la iteración es `A[mid] < A[mid + 1]`. Según su respuesta, el algoritmo recurre sobre uno de dos intervalos:

  - Si `A[mid] < A[mid + 1]`, el nuevo intervalo es `[mid + 1, hi]`, de tamaño `hi − mid`.
  - Si `A[mid] > A[mid + 1]`, el nuevo intervalo es `[lo, mid]`, de tamaño `mid − lo + 1`.

  Como `mid − lo = ⌊(k − 1)/2⌋`, los dos tamaños posibles son:

  ```text
  tamaño izquierdo = ⌊(k − 1)/2⌋ + 1 = ⌈k/2⌉
  tamaño derecho   = (k − 1) − ⌊(k − 1)/2⌋ = ⌊k/2⌋
  ```

  En ambos casos, el nuevo intervalo tiene tamaño

  ```text
  k' ≤ ⌈k/2⌉.
  ```

  Por hipótesis de inducción, la ejecución sobre ese subintervalo hace a lo sumo `⌈log₂ k'⌉` comparaciones. Como `log₂` es creciente y `k' ≤ ⌈k/2⌉`, se tiene

  ```text
  ⌈log₂ k'⌉ ≤ ⌈log₂ ⌈k/2⌉⌉.
  ```

  Falta usar la identidad

  ```text
  ⌈log₂ ⌈k/2⌉⌉ = ⌈log₂ k⌉ − 1    para todo k ≥ 2.
  ```

  **Justificación de la identidad.** Sea `m = ⌈log₂ k⌉`. Entonces

  ```text
  2^{m−1} < k ≤ 2^m.
  ```

  Dividiendo entre 2,

  ```text
  2^{m−2} < k/2 ≤ 2^{m−1}.
  ```

  De la desigualdad izquierda, `k/2 > 2^{m−2}`, y por definición de techo, `⌈k/2⌉ ≥ k/2 > 2^{m−2}`. De la desigualdad derecha, como `2^{m−1}` es entero y `k/2 ≤ 2^{m−1}`, se tiene `⌈k/2⌉ ≤ 2^{m−1}`. Por tanto,

  ```text
  2^{m−2} < ⌈k/2⌉ ≤ 2^{m−1},
  ```

  y esto significa exactamente que

  ```text
  ⌈log₂ ⌈k/2⌉⌉ = m − 1 = ⌈log₂ k⌉ − 1.
  ```

  Entonces, sumando la comparación de la iteración más el costo del subproblema,

  ```text
  costo ≤ 1 + ⌈log₂ k'⌉
        ≤ 1 + ⌈log₂ ⌈k/2⌉⌉
        = 1 + (⌈log₂ k⌉ − 1)
        = ⌈log₂ k⌉.
  ```

  Esto cierra la inducción. ∎

**Observación.** El lema da una cota superior para el algoritmo, no una igualdad para todos los intervalos. La igualdad exacta para el problema completo se obtiene al combinarlo con la cota inferior de la sección 6, como se hace en la sección 5.2.

**Comentario sobre la demostración.** La inducción es directamente sobre el tamaño del intervalo, sin definir una función auxiliar `U(k)`. Eso evita tener que justificar que `U` es no decreciente: en el paso inductivo basta con que el subintervalo tenga tamaño `k' ≤ ⌈k/2⌉`, porque `⌈log₂ ·⌉` es monótona no decreciente.

### 5.2. Optimalidad exacta

**Teorema (optimalidad exacta)**. En el modelo de comparaciones binarias, `buscar_pico` hace exactamente `⌈log₂ n⌉` comparaciones en el peor caso sobre arreglos de n elementos distintos.

**Demostración.**

    Por la sección 4, buscar_pico es correcto.

    Por el lema de la sección 5.1, buscar_pico hace a lo sumo ⌈log₂ n⌉ comparaciones en el peor caso.

    Por la cota inferior de la sección 6, cualquier algoritmo correcto de comparaciones necesita al menos ⌈log₂ n⌉ comparaciones en el peor caso.

Por tanto, el costo en el peor caso de `buscar_pico` es a la vez `≤ ⌈log₂ n⌉` y `≥ ⌈log₂ n⌉`. Luego es exactamente
```text

⌈log₂ n⌉.
```
∎

Así, la igualdad
```text

costo del algoritmo = ⌈log₂ n⌉ = cota inferior
```
no se sigue solo de la inducción de la sección 5.1, sino de combinar la cota superior del algoritmo con la cota inferior para todos los algoritmos correctos. No hace falta construir a mano una instancia que fuerce el peor caso: la sección 6 ya garantiza que cualquier algoritmo correcto, incluido el nuestro, paga al menos `⌈log₂ n⌉`.

### 5.3. Traza sobre dos ejemplos

**Ejemplo A**. `A = [1, 3, 5, 4, 2, 8, 6]`, `n = 7`.

| paso | lo | hi | mid | A[mid] < A[mid+1] | nuevo intervalo | comparaciones |
|------|----|----|-----|-------------------|-----------------|---------------|
| 1    | 0  | 6  | 3   | 4 < 2 → no        | [0, 3]          | 1             |
| 2    | 0  | 3  | 1   | 3 < 5 → sí        | [2, 3]          | 2             |
| 3    | 2  | 3  | 2   | 5 < 4 → no        | [2, 2]          | 3             |
| 4    | 2  | 2  | —   | termina           | devuelve 2      | 3             |

Resultado: 3 comparaciones, que coincide con `⌈log₂ 7⌉ = 3`. El índice 2 es pico porque `A[1] = 3 < A[2] = 5 > A[3] = 4`.

**Ejemplo B** (peor caso alcanzado para `n = 7`). `A = [1, 2, 3, 7, 6, 5, 4]`.

| paso | lo | hi | mid | A[mid] < A[mid+1] | nuevo intervalo | comparaciones |
|------|----|----|-----|-------------------|-----------------|---------------|
| 1    | 0  | 6  | 3   | 7 < 6 → no        | [0, 3]          | 1             |
| 2    | 0  | 3  | 1   | 2 < 3 → sí        | [2, 3]          | 2             |
| 3    | 2  | 3  | 2   | 3 < 7 → sí        | [3, 3]          | 3             |
| 4    | 3  | 3  | —   | termina           | devuelve 3      | 3             |

Resultado: 3 comparaciones. El índice 3 es pico porque `A[2] = 3 < A[3] = 7 > A[4] = 6`.

**Contraejemplo al “caso típico”**. `A = [1, 2, 3, 4, 5, 6, 7]` es estrictamente creciente. El algoritmo hace solo 2 comparaciones: siempre baja a la derecha y termina en el último elemento. Eso muestra que no toda instancia alcanza el peor caso; la tabla del ejemplo B muestra que sí existen instancias que lo alcanzan.

### 5.4. Memoria

El algoritmo usa `O(1)` memoria adicional: solo las variables `lo`, `hi`, `mid` y el índice devuelto. No usa recursión ni estructuras auxiliares.

## 6. Cota mínima (C5)

**Teorema.** Cualquier algoritmo de comparaciones que encuentre un pico local en un arreglo de `n` números distintos hace al menos `⌈log₂ n⌉` comparaciones en el peor caso.

**Demostración (por información)**. Construimos `n` instancias distintas `A^{(0)}`, `A^{(1)}`, …, `A^{(n−1)}`, una por cada posición posible del pico:

Para cada `i ∈ {0, 1, …, n−1}`:

    A^{(i)}[j] = j + 1 para j < i (estrictamente creciente),

    A^{(i)}[i] = n (el máximo),

    A^{(i)}[j] = n − (j − i) para j > i (estrictamente decreciente).

Por ejemplo, para `n = 5`:
```text

i = 0: [5, 4, 3, 2, 1]
i = 1: [1, 5, 4, 3, 2]
i = 2: [1, 2, 5, 4, 3]
i = 3: [1, 2, 3, 5, 4]
i = 4: [1, 2, 3, 4, 5]
```

Verificación de las instancias.

    Elementos distintos. Los valores son {1, 2, …, n}, todos distintos.

    Pico único en la posición i. Para j < i la sucesión es estrictamente creciente; para j > i, estrictamente decreciente; en i está el máximo global n, mayor que ambos vecinos. Luego A^{(i)}[i] es el único pico local de A^{(i)}.

Por tanto, un algoritmo correcto que reciba `A^{(i)}` debe devolver necesariamente el índice i.

El árbol de decisión. Cualquier algoritmo correcto, sobre las `n` instancias, produce `n` hojas distintas: si dos instancias `A^{(i)}` y `A^{(j)}` con `i ≠ j` terminaran en la misma hoja, recibirían la misma salida; pero la salida correcta en una es `i` y en la otra es `j`, así que el algoritmo se equivocaría en al menos una. Contradicción.

Un árbol binario con al menos `n` hojas tiene altura al menos `⌈log₂ n⌉`. La altura es el número de comparaciones en el peor caso. Por tanto, cualquier algoritmo correcto necesita al menos `⌈log₂ n⌉` comparaciones en el peor caso. ∎

Este argumento es de información, y es exacto (no solo asintótico): da `⌈log₂ n⌉`, no solo `Ω(log n)`. Es posible también dar un argumento de adversario (descartar la mitad en cada respuesta), pero la versión por instancias es más corta y no deja cabos sueltos.

**Conclusión: optimalidad exacta**. Por el lema de la sección 5.1, `buscar_pico` hace en el peor caso `⌈log₂ n⌉` comparaciones. Por la cota inferior, ningún algoritmo de comparaciones puede hacer menos. Por tanto el algoritmo es óptimo, no solo asintóticamente sino en la constante del peor caso:
```text

costo del algoritmo  =  ⌈log₂ n⌉  =  cota inferior
```

Y como la cota inferior se aplica al propio algoritmo, no hace falta exhibir una instancia concreta que alcance el peor caso: la optimalidad exacta se sigue del emparejamiento de las dos cotas. (La traza del ejemplo B de la sección 5 muestra, de todas formas, que ese peor caso se alcanza en la práctica.)

## 7. Verificación experimental y casos límite

### 7.1. Versión del algoritmo que cuenta comparaciones
```python

def buscar_pico_contando(A):
    """Igual que buscar_pico, pero devuelve (índice, número de comparaciones)."""
    if not A:
        return -1, 0
    lo, hi = 0, len(A) - 1
    comparaciones = 0
    while lo < hi:
        mid = (lo + hi) // 2
        comparaciones += 1
        if A[mid] < A[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo, comparaciones
```

### 7.2. Oráculo: fuerza bruta
```python
import math

def pico_fuerza_bruta(A):
    """Oráculo O(n): devuelve el índice del primer pico, o -1."""
    n = len(A)
    for i in range(n):
        izq = A[i-1] if i > 0 else -math.inf
        der = A[i+1] if i < n-1 else -math.inf
        if izq < A[i] > der:
            return i
    return -1

def verificar_pico(A, idx):
    """Comprueba que A[idx] es un pico local, con centinelas."""
    n = len(A)
    if idx < 0 or idx >= n:
        return False
    izq = A[idx - 1] if idx > 0 else -math.inf
    der = A[idx + 1] if idx < n - 1 else -math.inf
    return izq < A[idx] > der
```
### 7.3. Casos límite
```python

import math, random, itertools

# 1. Estrictamente creciente: el pico es el último.
A1 = [1, 2, 3, 4, 5]
assert verificar_pico(A1, buscar_pico(A1))

# 2. Estrictamente decreciente: el pico es el primero.
A2 = [5, 4, 3, 2, 1]
assert verificar_pico(A2, buscar_pico(A2))

# 3. Pico en el medio.
A3 = [1, 3, 5, 4, 2]
assert verificar_pico(A3, buscar_pico(A3))

# 4. Arreglo de tamaño 1: trivialmente pico (los dos vecinos son -∞).
A4 = [42]
assert verificar_pico(A4, buscar_pico(A4))

# 5. Arreglo de tamaño 2: el mayor de los dos.
A5 = [10, 20]
assert verificar_pico(A5, buscar_pico(A5))
A5b = [20, 10]
assert verificar_pico(A5b, buscar_pico(A5b))

print("Casos límite superados. ✔")
```

### 7.4. Prueba aleatoria contra el oráculo
```python

random.seed(2026)
fallos = 0
for _ in range(10_000):
    n = random.randint(1, 100)
    A = random.sample(range(1, 1000), n)  # elementos distintos
    idx = buscar_pico(A)
    if not verificar_pico(A, idx):
        fallos += 1
print(f"10 000 instancias aleatorias, fallos = {fallos}")
```
```text
Salida esperada: 10 000 instancias aleatorias, fallos = 0.
```

### 7.5. Prueba exhaustiva para n ≤ 8 y confirmación de la cota exacta
```python

print(f"{'n':>2} {'peor caso medido':>16} {'⌈log₂ n⌉':>10} {'coincide':>10}")
for n in range(1, 9):
    peor = 0
    for P in itertools.permutations(range(1, n + 1)):
        idx, c = buscar_pico_contando(list(P))
        assert verificar_pico(list(P), idx), f"fallo en {P}"
        peor = max(peor, c)
    cota = math.ceil(math.log2(n))
    print(f"{n:>2} {peor:>16} {cota:>10} {str(peor == cota):>10}")
```
Salida esperada:
```text

 n   peor caso medido   ⌈log₂ n⌉   coincide
 1                 0          0       True
 2                 1          1       True
 3                 2          2       True
 4                 2          2       True
 5                 3          3       True
 6                 3          3       True
 7                 3          3       True
 8                 3          3       True
```

Para cada `n ≤ 8`, el peor caso medido sobre todas las permutaciones coincide con `⌈log₂ n⌉`. Esto no es una demostración: es solo una comprobación para `n` pequeño. La demostración de la cota exacta está en las secciones 5 y 6.

### 7.6. La precondición "elementos distintos" es esencial

El algoritmo usa comparaciones estrictas `(<)`. Si se permiten elementos repetidos, puede devolver un índice que no es pico, incluso cuando existe un pico en el arreglo.

Contraejemplo 1 (no existe pico estricto). A = [1, 1, 1]. El algoritmo recorre:
```text

lo=0, hi=2, mid=1: A[1] < A[2] → 1 < 1 → no → hi=1
lo=0, hi=1, mid=0: A[0] < A[1] → 1 < 1 → no → hi=0
devuelve 0
```
`A[0] = 1` no es pico (necesita `1 > A[1] = 1`, que es falso). En este arreglo no existe ningún pico estricto; el problema, tal como está especificado, no se puede cumplir, pero el algoritmo devuelve una respuesta incorrecta en lugar de señalar el fracaso. La precondición "elementos distintos" garantiza que hay pico (por el argumento del máximo global).

Contraejemplo 2 (existe pico, pero el algoritmo devuelve otro índice). `A = [1, 2, 2, 3]`. El pico real es la posición 3 `(2 < 3 > -∞)`. El algoritmo:
```text

lo=0, hi=3, mid=1: A[1] < A[2] → 2 < 2 → no → hi=1
lo=0, hi=1, mid=0: A[0] < A[1] → 1 < 2 → sí → lo=1
devuelve 1
```
`A[1] = 2`, vecinos `A[0] = 1` y `A[2] = 2`. Comprueba `1 < 2 ✓` pero `2 > 2 ✗`. No es pico. El algoritmo falla aunque exista un pico en la posición 3.

**Conclusión:** la precondición "elementos distintos" no es un detalle técnico, es parte del problema. Sin ella, la cota inferior de la sección 6 también deja de valer (las instancias `A^{(i)}` se pueden confundir). Se puede adaptar el algoritmo para elementos repetidos usando comparaciones no estrictas y centinelas `-∞` a los lados, pero entonces cambia el problema: la cota y la optimalidad hay que replantearlas.

### 7.7. Tabla de traza sobre un ejemplo pequeño

`A = [1, 3, 5, 4, 2, 8, 6]` (mismo ejemplo de la sección 1):
```text

lo  hi  mid  A[mid]  A[mid+1]  comparación  nuevo [lo, hi]
0   6   3    4       2         4 < 2 → no   [0, 3]
0   3   1    3       5         3 < 5 → sí   [2, 3]
2   3   2    5       4         5 < 4 → no   [2, 2]
2   2   —    —       —         termina       devuelve 2
```

Comprobación: `A[2] = 5` es pico `(3 < 5 > 4)`. ✓