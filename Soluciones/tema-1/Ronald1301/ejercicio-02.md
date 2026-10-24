# Ejercicio 2 — Búsqueda binaria: invariante, potencial y cota de información

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que
> la hace óptima.

## 1. El problema y su contrato

**Entrada:** un arreglo ordenado $a_1 \le a_2 \le \dots \le a_n$ y un valor $x$.
**Salida:** una posición $i$ con $a_i = x$, o "no está".
**Precondición:** el arreglo está ordenado (conferencia 3, §1: sin ella el contrato no
dice nada).

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)                 # busco en A[lo:hi]  (hi exclusivo)
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return m
        elif A[m] < x:
            lo = m + 1                 # x no puede estar en A[lo:m+1]
        else:
            hi = m                     # x no puede estar en A[m:hi]
    return -1
```

## 2. Correctitud parcial — el invariante

> **Invariante.** Si $x$ está en $A$, entonces está en el subarreglo `A[lo:hi]`.

Se demuestra en los tres pasos de la conferencia 3, §1.

- **Inicialización.** Antes de la primera vuelta `lo=0`, `hi=n`, así que `A[lo:hi]` es
  todo el arreglo. Trivialmente, si $x$ está, está ahí.
- **Mantenimiento.** Supongamos el invariante antes de una vuelta y sea
  $m=\lfloor(lo+hi)/2\rfloor$.
  - Si `A[m] == x`, devolvemos $m$: correcto.
  - Si `A[m] < x`: como el arreglo está ordenado, para todo $k \le m$ vale
    $a_k \le a_m < x$, así que $x\ne a_k$. Luego $x$, si está, está en `A[m+1:hi]`, y
    poner `lo = m+1` conserva el invariante.
  - Si `A[m] > x`: para todo $k \ge m$, $a_k \ge a_m > x$, así que $x$, si está, está
    en `A[lo:m]`, y poner `hi = m` conserva el invariante.
- **Conclusión.** El ciclo sale cuando `lo >= hi`, es decir `A[lo:hi]` vacío. Por el
  invariante, si $x$ estuviera, estaría en un rango vacío: imposible. Luego "no está"
  es correcto. Y cuando sale por `return m` es porque `A[m] == x`. En ambos casos la
  postcondición se cumple.

## 3. Terminación — el potencial

> **Potencial.** $\Phi = hi - lo$, el ancho del rango de búsqueda. Es un entero
> $\ge 0$ y **baja estrictamente** en cada vuelta.

Sea $m=\lfloor(lo+hi)/2\rfloor$ con `lo < hi`, de modo que $lo \le m < hi$.

- Rama `lo = m+1`: el ancho nuevo es $hi-(m+1) = (hi-lo)-(m+1-lo) < hi-lo$ porque
  $m+1-lo \ge 1$.
- Rama `hi = m`: el ancho nuevo es $m-lo < hi-lo$ porque $m < hi$.

Como $\Phi$ es un entero no negativo que baja al menos 1 por vuelta y arranca en $n$,
el ciclo hace a lo sumo $n$ vueltas y termina. (De hecho el rango se **parte por la
mitad**, así que hace $\Theta(\log n)$ vueltas; el potencial solo prueba que termina.)

> **Cuidado con el `+1`** (conferencia 3, ejercicio 7): si se escribiera `lo = m` en
> vez de `lo = m+1`, en la rama `A[m] < x` el ancho no bajaría cuando $m=lo$
> (ocurre con `hi = lo+1`), el potencial se estanca y el ciclo **no termina**.

## 4. Figura — el potencial se parte por la mitad

Búsqueda de $x=23$ en `[2,5,8,12,17,23,30,41]` ($n=8$). `|` marca `lo`; `)` marca `hi`.
`^` es el `m` comparado. $\Phi = hi-lo$.

```
índice:     0   1   2   3   4   5   6   7
valor:      2   5   8  12  17  23  30  41
          --------------------------------------------------
v0  |2   5   8  12  17  23  30  41)   m=3 (12<23) -> lo=4   Φ=8
                        ^
v1               |17  23  30  41)      m=5 (23=23) -> ¡encontrado! Φ=4
                      ^
          --------------------------------------------------
Φ: 8 -> 4 -> (hallado). Cada vuelta al menos lo divide entre dos.
```

El ancho cae $8\to4\to\dots$; en el peor caso (elemento ausente) llega a $0$ tras
$\lceil\log_2(n+1)\rceil$ vueltas.

## 5. Cota de información — por qué es óptima (C5, §3)

Modelo: **comparaciones** (conferencia 5, §1). Cada comparación de $x$ con un elemento
responde $<,\,=,\,>$. Para forzar un árbol **binario** y obtener $\log_2$ en vez de
$\log_3$, miramos solo los casos en que **$x$ no está**: entonces ninguna comparación
responde $=$ y solo se usan dos ramas (conferencia 5, §3, "la búsqueda binaria también
es óptima").

**Los huecos.** Si $x$ no está, cae en uno de los $n+1$ **huecos**: antes de $a_1$,
entre $a_i$ y $a_{i+1}$, o después de $a_n$.

```
   h0   a1   h1   a2   h2   a3   h3  ...  a_n   h_n
   ──●────────●────────●──── ...  ────────●──────────
      (n+1 huecos: h0, h1, ..., h_n)
```

**Lema (C5, §3).** Dos valores en huecos distintos deben llegar a hojas distintas del
árbol de decisión. Si cayeran en la misma hoja, entre sus huecos hay un elemento $a_i$
con el que el algoritmo no comparó; tomando $x=a_i$ recibe las mismas respuestas, llega
a la misma hoja y el algoritmo diría "no está", pero $a_i$ sí está: contradicción.

**Consecuencia.** El árbol binario de los casos "no está" tiene al menos $n+1$ hojas,
y por el lema 1 de C5 (un árbol de altura $h$ tiene $\le 2^h$ hojas) su altura es al
menos $\lceil\log_2(n+1)\rceil$. Luego **todo** algoritmo de comparaciones necesita
$\ge \lceil\log_2(n+1)\rceil$ comparaciones en el peor caso.

**La búsqueda binaria la alcanza:** cada comparación parte el rango por la mitad, así
que tras $\lceil\log_2(n+1)\rceil$ comparaciones queda un solo hueco. Cota y algoritmo
coinciden $\Rightarrow$ **óptima** en el modelo de comparaciones.

| $n$ | huecos $n+1$ | $\lceil\log_2(n+1)\rceil$ | comparaciones de la búsqueda binaria |
|---|---|---|---|
| 1 | 2 | 1 | 1 |
| 3 | 4 | 2 | 2 |
| 7 | 8 | 3 | 3 |
| 15 | 16 | 4 | 4 |
| 1000 | 1001 | 10 | 10 |

## 6. Comprobación — el invariante y la cota, ejecutados

```python
import math, random

def busqueda_binaria_vigilada(A, x):
    lo, hi, comparaciones = 0, len(A), 0
    while lo < hi:
        # invariante: si x está en A, está en A[lo:hi]
        if x in A:
            assert A[lo:hi].count(x) >= 1
        m = (lo + hi) // 2
        comparaciones += 1
        if A[m] == x:
            return m, comparaciones
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    return -1, comparaciones

random.seed(0)
peor = {}
for n in [1, 3, 7, 15, 1000]:
    A = sorted(random.sample(range(10 * n + 5), n))
    maxc = 0
    for x in range(10 * n + 5):          # todos los x: presentes y en cada hueco
        _, c = busqueda_binaria_vigilada(A, x)
        maxc = max(maxc, c)
    peor[n] = (maxc, math.ceil(math.log2(n + 1)))
    assert maxc <= math.ceil(math.log2(n + 1)) + 1   # ±1 por la comparación de '='
print("n -> (peor caso medido, cota ceil(log2(n+1)))")
for n, v in peor.items():
    print(f"{n:>5} -> {v}")
```

**Salida:**

```
n -> (peor caso medido, cota ceil(log2(n+1)))
    1 -> (1, 1)
    3 -> (2, 2)
    7 -> (3, 3)
   15 -> (4, 4)
 1000 -> (10, 10)
```

El peor caso medido iguala la cota de información: ni el invariante se viola nunca, ni
el algoritmo supera $\lceil\log_2(n+1)\rceil$ comparaciones.

## 7. Resumen

- **Invariante** (correctitud parcial): *si $x$ está, está en `A[lo:hi]`*.
- **Potencial** (terminación): $\Phi=hi-lo$, entero $\ge0$ que baja cada vuelta.
- **Cota de información** (C5): $\lceil\log_2(n+1)\rceil$ comparaciones, contando los
  $n+1$ huecos; la búsqueda binaria la alcanza, así que es óptima en el modelo de
  comparaciones.
