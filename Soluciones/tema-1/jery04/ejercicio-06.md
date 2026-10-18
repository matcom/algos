# Ejercicio 6: Búsqueda en una matriz con filas y columnas ordenadas

> **Enunciado.** Una matriz $n \times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en $o(n)$. (C3, C5)

## 1. Especificación del problema

**Entrada.** Una matriz $A[0..n-1][0..n-1]$ y un valor $x$, con la precondición de orden

$$A[r][c] \leq A[r][c+1] \quad \text{y} \quad A[r][c] \leq A[r+1][c] \qquad \text{(siempre que los índices existan).}$$

**Salida.**

- Si $x$ está en $A$, una posición $(r, c)$ con $A[r][c] = x$.
- Si no, `"no está"`.

**Modelo.** Comparaciones entre $x$ y una entrada de la matriz; cada comparación devuelve $<$, $=$ o $>$. El costo es el número de comparaciones en el peor caso (el mismo modelo del ejercicio 2).

**Precisiones que el enunciado no da y hay que fijar:**

- **"Creciente".** Se lee como *no decreciente* ($\leq$). El algoritmo funciona con esa lectura, que incluye la estricta. La cota inferior se demuestra con matrices *estrictamente* crecientes, que son un caso particular. Por tanto, el resultado vale con las dos lecturas.
- **Qué significa $O(n)$.** La matriz tiene $n^2$ celdas. Un algoritmo de $O(n)$ comparaciones lee solo $O(\sqrt{N})$ de las $N = n^2$ celdas de la entrada: es sublineal en el tamaño de la entrada.
- **Qué se compara.** Solo $x$ contra celdas. En §6.5 se muestra que permitir comparar celdas entre sí no cambia el orden de la cota.

## 2. Observación clave

La hipótesis solo ordena **dentro de cada fila y de cada columna**. Por transitividad, $A[r][c] \leq A[r'][c']$ siempre que $r \leq r'$ y $c \leq c'$. Pero dos celdas con $r < r'$ y $c > c'$, como $A[0][n-1]$ y $A[n-1][0]$, **no están relacionadas** por la hipótesis. Es un orden parcial, no un orden total, y por eso la matriz no se puede tratar como un arreglo ordenado.

Primeros intentos:

| Estrategia | Comparaciones |
|---|---|
| Recorrer toda la matriz | $n^2$ |
| Búsqueda binaria en cada fila | $n \lceil \log_2(n+1) \rceil = O(n \log n)$ |
| Escalera desde una esquina (§3) | $\leq 2n - 1 = O(n)$ |

**Por qué la esquina superior derecha.** $A[0][n-1]$ es el **máximo de su fila** y el **mínimo de su columna**. Al compararlo con $x$:

- si $A[0][n-1] < x$, todo el resto de la fila es menor que $x$: la fila entera se descarta;
- si $A[0][n-1] > x$, todo el resto de la columna es mayor que $x$: la columna entera se descarta.

Cada comparación elimina una fila o una columna del rectángulo candidato. En la esquina superior izquierda, que es mínimo de ambas, una respuesta $<$ no descarta nada; la inferior derecha tiene el problema simétrico. La esquina inferior izquierda sirve por simetría.

## 3. Algoritmo

```python
def buscar(A, x):
    n = len(A)
    i, j = 0, n - 1                    # esquina superior derecha
    while i < n and j >= 0:            # el rectángulo candidato no está vacío
        if A[i][j] == x:
            return ("está", (i, j))
        elif A[i][j] < x:
            i += 1                     # se descarta la fila i (a la izquierda de j)
        else:
            j -= 1                     # se descarta la columna j (por debajo de i)
    return ("no está", None)
```

Para una matriz $m \times n$ basta cambiar la guarda a `i < m` (con `j` empezando en `n - 1`); el costo pasa a $m + n - 1$.

## 4. Invariante (correctitud parcial)

### 4.1. El invariante

Sea el **rectángulo candidato**

$$R(i, j) = \{\, (r, c) : i \leq r \leq n-1,\ 0 \leq c \leq j \,\},$$

las filas desde $i$ hacia abajo y las columnas hasta $j$ hacia la izquierda.

```
                  columnas 0 … j      columnas j+1 … n-1
  filas 0 … i-1  [  descartadas    |     descartadas     ]
  filas i … n-1  [     R(i,j)      |     descartadas     ]
```

> **$I(i, j)$.** Ninguna celda fuera de $R(i, j)$ vale $x$.

Equivalentemente: todas las apariciones de $x$ en $A$ están dentro de $R(i, j)$.

### 4.2. Demostración en tres pasos

**Inicialización.** Antes de la primera vuelta, $i = 0$ y $j = n - 1$, así que $R(0, n-1) = A$ entera. No hay celdas fuera de $R$, y el invariante se cumple vacuamente. ✔

**Mantenimiento.** Supongamos $I(i, j)$ con $i < n$ y $j \geq 0$ (condición del ciclo). Entonces $(i, j) \in R(i, j)$ y la comparación es válida. Hay tres casos:

- $A[i][j] == x$: el algoritmo devuelve `("está", (i, j))`, que es correcto. No hay más vueltas que analizar.

- $A[i][j] < x$: el algoritmo hace $i \leftarrow i + 1$, y el nuevo rectángulo es $R(i+1, j) = R(i, j) \setminus \{(i, c) : c \leq j\}$. Para toda columna $c \leq j$, **por el orden de la fila $i$**,
$$A[i][c] \leq A[i][j] < x,$$
así que $A[i][c] \neq x$. Las celdas nuevas que quedan fuera de $R$ no valen $x$, y las que ya estaban fuera tampoco. ✔

- $A[i][j] > x$: el algoritmo hace $j \leftarrow j - 1$, y el nuevo rectángulo es $R(i, j-1) = R(i, j) \setminus \{(r, j) : r \geq i\}$. Para toda fila $r \geq i$, **por el orden de la columna $j$**,
$$A[r][j] \geq A[i][j] > x,$$
así que $A[r][j] \neq x$. ✔

En cada caso de descarte, el invariante se restablece. Cada una de las dos hipótesis de orden se usa exactamente en un caso.

**Conclusión.** Al salir del ciclo sin haber devuelto, $i = n$ o $j < 0$: el rectángulo $R(i, j)$ está **vacío**. Por $I(i, j)$, ninguna celda de $A$ vale $x$, y `"no está"` es correcto. Si salió por la rama de igualdad, la respuesta es correcta por la propia comparación. ∎

**Nota (la lección de la conferencia 3).** El invariante solo sirve si, además de ser inductivo, la condición de salida lo convierte en la respuesta. Aquí esa condición es "$R$ vacío", y es exactamente lo que fallaría si la guarda estuviera mal escrita ($j > 0$ en vez de $j \geq 0$): el ciclo saldría con la columna $0$ todavía en $R$, sin haberla revisado. El experimento de §7 lo mide.

## 5. Terminación y costo

### 5.1. Potencial

$$\Phi(i, j) = (n - i) + (j + 1),$$

el número de filas más el número de columnas que le quedan a $R(i, j)$.

- **Entero.** Sí.
- **Acotado.** Inicialmente $\Phi = 2n$. Cuando el ciclo ejecuta el cuerpo, $n - i \geq 1$ y $j + 1 \geq 1$, así que $\Phi \geq 2$.
- **Decrece estrictamente.** En las ramas $<$ y $>$, $\Phi$ baja exactamente $1$ (se pierde una fila o una columna). La rama $=$ devuelve y no itera.

$\Phi$ baja $1$ por vuelta desde $2n$ y el cuerpo solo se ejecuta con $\Phi \geq 2$, así que hay como máximo $2n - 1$ vueltas y el algoritmo termina. Junto con la correctitud parcial, **hay correctitud total**.

### 5.2. Costo

Cada vuelta hace **exactamente una comparación** de $x$ con una celda, más un número constante de operaciones (guarda, actualización de un índice).

$$\boxed{\ \#\text{comparaciones} \leq 2n - 1 = O(n)\ }$$

Memoria extra: $O(1)$ (dos índices y un contador).

**La cota $2n-1$ se alcanza.** Con $A[r][c] = 2(r + c)$ y $x = 2n - 3$, los valores son todos pares y $x$ no está. El puntero visita $(0, n-1), (0, n-2), (1, n-2), (1, n-3), \ldots, (n-1, 0)$ alternando $>$ y $<$, y sale con $j = -1$ tras $2(n-1) + 1 = 2n - 1$ comparaciones.

## 6. Cota mínima: el adversario

### 6.1. Por qué no basta contar salidas

La salida tiene $n^2 + 1$ posibilidades (cada celda, o "no está"), de modo que el argumento de información de la conferencia 5 solo da del orden de $\log n$ comparaciones. Es el contraste que ya apareció en la conferencia 5: la información da $\Omega(n \log n)$ para ordenar pero solo $\Omega(\log n)$ para el máximo, donde fue el **adversario** el que dio la cota exacta. Aquí pasa lo mismo: contar salidas es débil porque la estructura del orden parcial impide aprovechar toda la información de cada comparación.

### 6.2. La familia de entradas

Sean $x = 2n - 3$ y la matriz base

$$S[r][c] = 2(r + c).$$

Para $k = 0, \ldots, n-1$, sea $S_k$ la matriz que resulta de **cambiar a $x$ el valor de la celda** $D_k = (k, n-1-k)$ de la antidiagonal $r + c = n - 1$.

**Propiedades.**

1. $S$ es **estrictamente creciente** en filas y columnas, y todos sus valores son pares, así que $x$ (impar) **no está** en $S$.
2. Valores de $S$ según la posición:
   - si $r + c \leq n - 2$: $S[r][c] \leq 2n - 4 = x - 1 < x$;
   - si $r + c = n - 1$ (antidiagonal): $S[r][c] = 2n - 2 = x + 1 > x$;
   - si $r + c \geq n$: $S[r][c] \geq 2n = x + 3 > x$.
3. $S_k$ sigue siendo **estrictamente creciente**: los vecinos de $D_k$ por la izquierda y por arriba tienen $r + c = n - 2$, con valor $2n - 4 < x$, y los vecinos por la derecha y por abajo tienen $r + c = n$, con valor $2n > x$. Como el orden por filas y columnas solo relaciona celdas adyacentes, no hay más que comprobar.
4. $x$ aparece en $S_k$ **exactamente una vez**, en $D_k$.

Son $n + 1$ entradas: $S$ (la respuesta es "no está") y $S_0, \ldots, S_{n-1}$ (la respuesta es "está"). Todas cumplen la precondición.

### 6.3. El adversario

Ante cada comparación de $x$ con $A[r][c]$, el adversario responde **como lo haría $S$**:

$$\text{respuesta} = \begin{cases} A[r][c] < x & \text{si } r + c \leq n - 2, \\ A[r][c] > x & \text{si } r + c \geq n - 1. \end{cases}$$

Una comparación sobre una celda fuera de la antidiagonal tiene la misma respuesta en $S$ y en todas las $S_k$. Una comparación sobre la celda $D_j$ tiene la misma respuesta en $S$ y en $S_k$ para todo $k \neq j$, y solo en $S_j$ la respuesta sería $=$. Es decir:

> Mientras el algoritmo no haya comparado $x$ con $D_j$, no puede distinguir $S$ de $S_j$.

Es el mismo mecanismo que en el máximo (conferencia 5): una celda que nunca se mira se puede cambiar sin contradecir ninguna respuesta.

### 6.4. El teorema

**Teorema.** Todo algoritmo determinista que decide, en el modelo de comparaciones de $x$ con celdas, si $x$ está en una matriz $n \times n$ con filas y columnas ordenadas hace **al menos $n$ comparaciones** en el peor caso. En particular, no existe tal algoritmo con $o(n)$ comparaciones.

**Demostración.** Ejecutemos el algoritmo contra el adversario (es decir, sobre la entrada $S$). Sea $Q$ el conjunto de celdas de la antidiagonal con las que compara. Si el algoritmo hiciera menos de $n$ comparaciones, entonces $|Q| < n$ y existiría $j$ con $D_j \notin Q$.

Sobre $S_j$ todas las respuestas del algoritmo serían idénticas a las de $S$: las dos matrices solo difieren en $D_j$, que no se consultó. Un algoritmo determinista con las mismas respuestas hace las mismas preguntas y da la misma salida. Esa salida es `"no está"`, correcta para $S$ pero **incorrecta para $S_j$**, que contiene a $x$. Contradicción.

Luego, sobre la entrada $S$, un algoritmo correcto compara con **las $n$ celdas de la antidiagonal**, y hace al menos $n$ comparaciones. ∎

**Conclusión.** El problema tiene complejidad $\Theta(n)$ comparaciones: la escalera hace $\leq 2n - 1$ y ningún algoritmo hace menos de $n$.

### 6.5. Observaciones

**(a) Comparar celdas entre sí no ayuda.** Si se permitieran comparaciones entre dos celdas, el adversario sigue respondiendo como $S$. En $S$ todas las celdas de la antidiagonal valen $2n - 2$. Una comparación entre $D_a$ y $D_b$ distingue $S$ de $S_k$ solo si $k \in \{a, b\}$ (en $S_k$, la celda $D_k$ es menor que las demás); una comparación entre una celda de la antidiagonal y otra celda no la distingue de ninguna $S_k$, porque las otras celdas valen $\leq 2n-4$ o $\geq 2n$. Cada comparación "cubre" a lo sumo $2$ de los $n$ valores de $k$, así que hacen falta al menos $\lceil n/2 \rceil$ comparaciones. La cota sigue siendo $\Omega(n)$.

**(b) Estricto y no estricto.** La cota se demostró con matrices estrictamente crecientes y el algoritmo con no decrecientes. Por tanto, el resultado $\Theta(n)$ vale con ambas lecturas de "creciente".

**(c) Por qué $\Omega(n)$.** La antidiagonal es una **anticadena** de tamaño $n$ en el orden parcial de la matriz: sus celdas no están ordenadas entre sí, así que la hipótesis de orden no impide que cualquiera de ellas valga $x$, de manera independiente. En un arreglo ordenado (ejercicio 2) el orden es total y cada comparación descarta la mitad; aquí el orden parcial solo permite descartar una fila o una columna.

**(d) La constante.** El algoritmo hace $2n - 1$ y el adversario da $n$; la brecha es un factor $2$ que no afecta a la pregunta ($\Theta(n)$). Para $n = 2, 3, 4$, el óptimo exacto calculado por búsqueda exhaustiva es $2n - 1$ (§7.3). No se demuestra aquí que lo sea para todo $n$.

## 7. Experimento

### 7.1. Código

El código siguiente implementa el algoritmo, un mutante con un error plantado y el generador exhaustivo de matrices monótonas.

```python
import random

def buscar(A, x):
    """Escalera desde la esquina superior derecha. Devuelve (pos | None, comparaciones)."""
    n = len(A)
    i, j, c = 0, n - 1, 0
    while i < n and j >= 0:
        c += 1
        if A[i][j] == x:
            return (i, j), c
        elif A[i][j] < x:
            i += 1
        else:
            j -= 1
    return None, c

def buscar_mutante(A, x):
    """Error plantado: j > 0 en lugar de j >= 0 (nunca mira la columna 0)."""
    n = len(A)
    i, j, c = 0, n - 1, 0
    while i < n and j > 0:
        c += 1
        if A[i][j] == x:
            return (i, j), c
        elif A[i][j] < x:
            i += 1
        else:
            j -= 1
    return None, c

def monotonas(n, V):
    """Todas las matrices n x n con entradas en 0..V y filas y columnas no decrecientes."""
    celdas = [(r, c) for r in range(n) for c in range(n)]
    def rec(k, M):
        if k == len(celdas):
            yield tuple(tuple(f) for f in M)
            return
        r, c = celdas[k]
        lo = max(M[r][c - 1] if c else 0, M[r - 1][c] if r else 0)
        for v in range(lo, V + 1):
            M[r][c] = v
            yield from rec(k + 1, M)
        M[r][c] = 0
    yield from rec(0, [[0] * n for _ in range(n)])

# 1) Exhaustivo: correctitud, cota 2n-1 y justeza
for n, V in [(1, 3), (2, 4), (3, 4), (4, 3)]:
    maxc = 0
    for M in monotonas(n, V):
        presentes = {v for f in M for v in f}
        for x in range(-1, V + 2):
            pos, c = buscar(M, x)
            assert (pos is not None) == (x in presentes)
            if pos:
                assert M[pos[0]][pos[1]] == x
            assert c <= 2 * n - 1
            maxc = max(maxc, c)
    assert maxc == 2 * n - 1

# 2) La familia del adversario: S y S_k
def S(n):
    return [[2 * (r + c) for c in range(n)] for r in range(n)]

def S_k(n, k):
    M = S(n)
    M[k][n - 1 - k] = 2 * n - 3
    return M

def estricta(M):
    n = len(M)
    return (all(M[r][c] < M[r][c + 1] for r in range(n) for c in range(n - 1)) and
            all(M[r][c] < M[r + 1][c] for r in range(n - 1) for c in range(n)))

for n in range(2, 41):
    x = 2 * n - 3
    assert estricta(S(n)) and all(v != x for f in S(n) for v in f)
    assert buscar(S(n), x) == (None, 2 * n - 1)            # la escalera alcanza 2n-1
    for k in range(n):
        M = S_k(n, k)
        assert estricta(M)
        assert [(r, c) for r in range(n) for c in range(n) if M[r][c] == x] == [(k, n - 1 - k)]
        assert all(M[r][c] == S(n)[r][c] for r in range(n) for c in range(n) if r + c != n - 1)

# 3) El mutante, con matrices monótonas aleatorias
random.seed(2026)
n, ensayos, fallos, solo_col0 = 6, 20000, 0, 0
for _ in range(ensayos):
    B = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            lo = max(B[r][c - 1] if c else 0, B[r - 1][c] if r else 0)
            B[r][c] = lo + random.randint(0, 3)
    if random.random() < 0.5:
        x = random.choice([v for f in B for v in f])
    else:
        x = random.randint(-1, B[-1][-1] + 1)
    esta = any(x in f for f in B)
    if (buscar_mutante(B, x)[0] is not None) != esta:
        fallos += 1
        solo_col0 += all(B[r][c] != x for r in range(n) for c in range(1, n))
print(f"mutante: {fallos}/{ensayos} fallos; de ellos, con x solo en la columna 0: {solo_col0}")
```

### 7.2. Resultados (ejecutado)

| Comprobación | Casos | Resultado |
|---|---|---|
| Correctitud y $\leq 2n-1$ comparaciones, todas las matrices monótonas | $n=1,2,3,4$ con entradas en $0..3$ o $0..4$: 24, 735, 28 812 y 148 176 instancias | se cumple; el máximo observado es exactamente $2n-1$ ($1, 3, 5, 7$) |
| Familia del adversario: $S$ y $S_k$ estrictamente crecientes, $x$ solo en $D_k$ | $n = 2, \ldots, 40$ | se cumple; la escalera hace $2n-1$ comparaciones sobre $S$ |
| Mutante con guarda $j > 0$ | 20 000 matrices aleatorias $6 \times 6$ | **1269 fallos (6,3 %)**; todos con $x$ presente solo en la columna $0$ |

Es decir, el mutante pasa el $93{,}7$ % de las pruebas aleatorias. La demostración dice dónde mirar: el fallo ocurre exactamente cuando $x$ solo está en la columna $0$, porque el ciclo sale con $R$ no vacío y el invariante ya no se convierte en la respuesta (§4.2, Conclusión).

### 7.3. Óptimo exacto para $n$ pequeño

Para ver cuánto de la brecha entre $n$ y $2n-1$ es real, se calcula por búsqueda exhaustiva el menor número de comparaciones $k$ para el que **existe** una estrategia (árbol de decisión) que decide la pertenencia en **todas** las matrices monótonas con entradas en $0..V$ y todos los $x \in 0..V$.

```python
def optimo_exacto(n, V):
    inst = []
    for M in monotonas(n, V):
        plano = [v for f in M for v in f]
        for x in range(V + 1):
            inst.append((plano, x, x in plano))
    signo = [[(p[k] > x) - (p[k] < x) for (p, x, _) in inst] for k in range(n * n)]
    memo = {}
    def decidible(S, k):
        if len({inst[i][2] for i in S}) <= 1:        # todas las instancias dan la misma respuesta
            return True
        if k == 0:
            return False
        if (S, k) not in memo:
            ok = False
            for c in range(n * n):                    # probar cada celda como siguiente pregunta
                partes = {}
                for i in S:
                    partes.setdefault(signo[c][i], []).append(i)
                if len(partes) >= 2 and all(decidible(frozenset(p), k - 1) for p in partes.values()):
                    ok = True
                    break
            memo[(S, k)] = ok
        return memo[(S, k)]
    S0, k = frozenset(range(len(inst))), 0
    while not decidible(S0, k):
        k += 1
    return k

for n, V in [(2, 4), (3, 4), (4, 3)]:
    print(n, V, optimo_exacto(n, V))
```

| $n$ | $V$ | Instancias | Óptimo exacto | $2n - 1$ |
|---|---|---|---|---|
| 2 | 4 | 525 | 3 | 3 |
| 3 | 4 | 20 580 | 5 | 5 |
| 4 | 3 | 98 784 | 7 | 7 |

Como esta familia es un subconjunto de todas las entradas posibles, el resultado es una cota mínima válida para el problema completo en esos $n$. Combinada con la escalera ($\leq 2n - 1$), significa que **$2n - 1$ es la complejidad exacta para $n = 2, 3, 4$**. Es evidencia numérica, no una demostración para todo $n$.

## 8. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Decidir si $x$ está en una matriz con filas y columnas ordenadas. Modelo: comparaciones de $x$ con celdas. El orden es parcial, no total. |
| ¿Qué algoritmo? | Escalera desde la esquina superior derecha: $A[i][j] < x$ descarta una fila, $A[i][j] > x$ descarta una columna. |
| ¿Es correcto? | **Invariante** $I(i,j)$: ninguna celda fuera de $R(i,j)$ vale $x$. **Potencial**: $(n-i) + (j+1)$, que baja $1$ por vuelta desde $2n$. |
| ¿Cuánto cuesta? | A lo sumo $2n - 1$ comparaciones (se alcanza) y $O(1)$ de memoria. Para $m \times n$: $m + n - 1$. |
| ¿Se puede mejor? | No en orden: **adversario** con la familia $S, S_0, \ldots, S_{n-1}$ obliga a comparar las $n$ celdas de la antidiagonal, así que $\geq n$ comparaciones. $\Theta(n)$. Exacto $2n-1$ para $n \leq 4$ (búsqueda exhaustiva). |
