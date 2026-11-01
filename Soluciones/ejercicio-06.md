# Ejercicio 6 - Buscar en una matriz con filas y columnas ordenadas

> Una matriz $m\times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un
> algoritmo que decida si contiene un valor $v$ en $O(m+n)$ comparaciones, demuestra su
> correctitud con un invariante, y demuestra con un adversario que no se puede en
> $o(m+n)$.

## 1. El problema

Matriz $A$ de $m$ filas y $n$ columnas, con cada fila creciente de izquierda a derecha
y cada columna creciente de arriba a abajo. Dado $v$, decidir si $v\in A$. El modelo es
de **comparaciones** (C5, §1): el costo es el número de comparaciones de $v$ con
entradas de $A$.

## 2. El algoritmo - "escalera" desde la esquina superior derecha

Empezamos en la esquina **superior derecha** $(0, n-1)$ y en cada paso descartamos una
fila entera o una columna entera:

```python
def buscar_matriz(A, v):
    if not A or not A[0]:
        return False
    m, n = len(A), len(A[0])
    i, j = 0, n - 1                     # esquina superior derecha
    while i < m and j >= 0:
        if A[i][j] == v:
            return True
        elif A[i][j] > v:               # toda la columna j (debajo) es > v
            j -= 1                       #   -> descarto la columna j
        else:                            # A[i][j] < v: toda la fila i (a la izq.) es < v
            i += 1                       #   -> descarto la fila i
    return False
```

**Por qué la esquina superior derecha funciona:** ese elemento es el **mayor de su
fila** y el **menor de su columna**. Así, al compararlo con $v$:
- si es $>v$, todos los de su columna (hacia abajo) son aún mayores $\Rightarrow$ la
  columna entera queda descartada;
- si es $<v$, todos los de su fila (hacia la izquierda) son aún menores $\Rightarrow$
  la fila entera queda descartada.

Cada comparación elimina una fila o una columna. (La esquina inferior izquierda
funciona igual por simetría; las esquinas superior-izquierda e inferior-derecha **no**,
porque ahí el elemento es mínimo/máximo en ambos sentidos y una comparación no
desambigua.)

## 3. Figura - el camino en escalera

Matriz $4\times5$, buscando $v=17$. `◄` marca la celda comparada; la flecha indica si
baja (fila descartada) o va a la izquierda (columna descartada).

```
        c0   c1   c2   c3   c4
      +----+----+----+----+----+
  f0  |  1    4    7   11   15◄|  15<17 -> bajar (descarto fila 0)
      +----+----+----+----+----+
  f1  |  2    5    8   12   19◄|  19>17 -> izquierda (descarto col 4)
      +----+----+----+---◄+----+
  f1  |  2    5    8   12 |     |  12<17 -> bajar (descarto fila 1)
      +----+----+----+---◄+----+
  f2  |  3    6    9   16   22 |  16<17 -> bajar (descarto fila 2)
      +----+----+---◄+----+----+
  f3  | 10   13   14   17   24 |  17=17 -> ENCONTRADO
      +----+----+----◄----+----+

Camino: (0,4)→(1,4)→(1,3)→(2,3)→(3,3). 5 comparaciones ≤ m+n = 9.
```

El camino solo **baja** o va a la **izquierda**: nunca retrocede. Por eso da a lo sumo
$m+n$ pasos.

## 4. Correctitud - el invariante

> **Invariante.** Al inicio de cada vuelta, si $v$ está en la matriz, está en el
> subrectángulo `A[i..m-1][0..j]` (filas de $i$ hacia abajo, columnas de $0$ a $j$).

- **Inicialización.** $i=0$, $j=n-1$: el subrectángulo es toda la matriz. ✓
- **Mantenimiento.** Sea $(i,j)$ la celda actual, dentro del rectángulo.
  - `A[i][j] > v`: por columnas crecientes, $A[k][j] \ge A[i][j] > v$ para todo
    $k\ge i$, así que **ninguna** celda de la columna $j$ (en el rectángulo) es $v$.
    Poner $j\leftarrow j-1$ conserva el invariante.
  - `A[i][j] < v`: por filas crecientes, $A[i][k] \le A[i][j] < v$ para todo $k\le j$,
    así que ninguna celda de la fila $i$ (en el rectángulo) es $v$. Poner
    $i\leftarrow i+1$ conserva el invariante.
  - `A[i][j] == v`: devolvemos `True`, correcto.
- **Conclusión.** El ciclo sale cuando $i=m$ o $j<0$: el subrectángulo es **vacío**.
  Por el invariante, si $v$ estuviera, estaría en un rectángulo vacío: imposible. Luego
  `False` es correcto.

**Terminación (potencial).** $\Phi = (m-i) + (j+1)$ = filas + columnas vivas. Cada
vuelta no terminal hace $i{+}{+}$ o $j{-}{-}$, bajando $\Phi$ en 1; $\Phi\ge0$. Arranca
en $m+n$, luego **a lo sumo $m+n$ vueltas**, una comparación cada una: **$O(m+n)$**. ✓

## 5. Cota mínima $\Omega(m+n)$ - argumento de adversario (C5, §5)

Modelo de comparaciones. Un **adversario** (C5, §5) responde las comparaciones de forma
consistente para que el algoritmo no pueda decidir con menos de $m+n-1$ comparaciones.

**La construcción.** El adversario fija de antemano la **antidiagonal**: coloca los
valores de modo que exista una "frontera" en escalera entre las celdas $<v$ (arriba a
la izquierda) y las $>v$ (abajo a la derecha), y decide si $v$ está o no **solo al
final**, según lo que el algoritmo haya mirado. Concretamente, considera las $m+n-1$
celdas de una antidiagonal (o la escalera frontera) donde podría estar $v$: son
mutuamente incomparables por el orden parcial (ninguna está arriba-izquierda de otra),
así que saber el resultado en una no dice nada sobre las demás.

**Estrategia del adversario.** Mantiene como "posible ubicación de $v$" cualquier celda
de la frontera que el algoritmo **no haya comparado todavía**. A cada comparación de
$v$ con una celda responde consistentemente con "$v$ no está aquí" (mayor o menor según
la posición), eliminando **a lo sumo una** celda frontera como candidata. Mientras
quede más de una celda frontera no comparada, existen **dos** matrices consistentes con
todas las respuestas: una con $v$ en una de esas celdas y otra sin $v$. El algoritmo no
puede distinguirlas, así que si responde, se equivoca en una.

**Conteo.** La frontera tiene $m+n-1$ celdas incomparables. Cada comparación tacha a lo
sumo una. Para que quede a lo sumo una celda dudosa (y poder responder), el algoritmo
necesita al menos $(m+n-1)-1 = m+n-2$ comparaciones; de hecho debe inspeccionar
información equivalente a las $m+n-1$ celdas frontera. Luego **todo** algoritmo de
comparaciones hace $\Omega(m+n)$ comparaciones en el peor caso.

Como el algoritmo de la §2 hace $\le m+n$ comparaciones y la cota es $\Omega(m+n)$, el
algoritmo es **óptimo** en el modelo de comparaciones (C5, §5–6: la cota mínima viene
con su modelo pegado).

## 6. Comprobación - correctitud, costo y la frontera adversaria

```python
import random

def buscar_matriz(A, v):
    if not A or not A[0]:
        return False, 0
    m, n = len(A), len(A[0])
    i, j, comp = 0, n - 1, 0
    while i < m and j >= 0:
        comp += 1
        if A[i][j] == v:
            return True, comp
        elif A[i][j] > v:
            j -= 1
        else:
            i += 1
    return False, comp

def matriz_ordenada(m, n, rng):
    """Genera una matriz con filas y columnas crecientes."""
    A = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            arriba = A[i-1][j] if i else 0
            izq = A[i][j-1] if j else 0
            A[i][j] = max(arriba, izq) + rng.randint(1, 3)
    return A

rng = random.Random(0)
peor = 0
for _ in range(3000):
    m, n = rng.randint(1, 12), rng.randint(1, 12)
    A = matriz_ordenada(m, n, rng)
    v = rng.randint(0, A[-1][-1] + 2)
    presente = any(v in fila for fila in A)
    hallado, comp = buscar_matriz(A, v)
    assert hallado == presente                       # correctitud contra fuerza bruta
    assert comp <= m + n                             # cota superior O(m+n)
    peor = max(peor, comp)
print(f"3000 matrices: correcto siempre, y nunca mas de m+n comparaciones")
print(f"peor numero de comparaciones observado = {peor}")
```

**Salida:**

```
3000 matrices: correcto siempre, y nunca mas de m+n comparaciones
peor numero de comparaciones observado = 19
```

($19 \le 12+12=24$.) La correctitud coincide con la fuerza bruta y el costo nunca pasa
de $m+n$.

## 7. Resumen

- **Algoritmo:** escalera desde la esquina superior derecha; cada comparación descarta
  una fila o una columna $\Rightarrow$ $O(m+n)$.
- **Invariante:** si $v$ está, está en `A[i..m-1][0..j]`; se conserva porque la esquina
  es máxima de su fila y mínima de su columna.
- **Cota mínima:** adversario sobre la frontera de $m+n-1$ celdas incomparables da
  $\Omega(m+n)$; el algoritmo es óptimo en comparaciones.
