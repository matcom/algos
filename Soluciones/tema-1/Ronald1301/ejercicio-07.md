# Ejercicio 7 — Mediana de dos arreglos ordenados

> El $k$-ésimo menor de los $2n$ elementos de dos arreglos ordenados de largo $n$.
> Diseña un algoritmo $O(\log n)$, demuestra su correctitud y da la cota de
> información.

*(Borrador preparado con asistencia de IA, siguiendo el formato de Agustin y los materiales del Tema 1.)*

## 1. El problema

Dos arreglos ordenados $A$ y $B$. Se pide el $k$-ésimo menor del multiconjunto
$A\cup B$ (la mediana es el caso $k=n$ ó el promedio de los $k=n$ y $k=n+1$). Queremos
$O(\log(m+n))$, que para $m=n$ es $O(\log n)$.

El algoritmo recorre el ciclo de la conferencia 2: fuerza bruta $\to$ divide y vencerás
$\to$ cota mínima.

## 2. Idea: elegir una "partición" por binaria sobre $A$

Buscamos una **partición** que deje exactamente $k$ elementos a la izquierda. Tomamos
$i$ elementos de $A$ y $j=k-i$ de $B$ al lado izquierdo. La partición es válida si todo
elemento de la izquierda es $\le$ todo elemento de la derecha, lo que equivale a:
$$A[i-1] \le B[j] \quad\text{y}\quad B[j-1] \le A[i].$$
Si $A[i-1] > B[j]$, hay que mover $i$ hacia la izquierda; si $B[j-1] > A[i]$, hacia la
derecha. Esto es una **búsqueda binaria sobre $i$** en $[\,\max(0,k-|B|),\ \min(k,|A|)\,]$.

```python
def kth(A, B, k):
    """1-indexado: devuelve el k-esimo menor de A∪B. Requiere 1<=k<=len(A)+len(B)."""
    if len(A) > len(B):                     # binaria sobre el mas corto -> O(log min)
        A, B = B, A
    m, n = len(A), len(B)
    INF = float("inf")
    lo, hi = max(0, k - n), min(k, m)       # i: cuantos de A van a la izquierda
    while lo <= hi:
        i = (lo + hi) // 2
        j = k - i
        Aizq = A[i-1] if i > 0 else -INF
        Ader = A[i]   if i < m else  INF
        Bizq = B[j-1] if j > 0 else -INF
        Bder = B[j]   if j < n else  INF
        if Aizq <= Bder and Bizq <= Ader:   # particion valida
            return max(Aizq, Bizq)          # el mayor de la izquierda = k-esimo
        elif Aizq > Bder:                   # demasiado de A: mover i a la izquierda
            hi = i - 1
        else:                               # muy poco de A: mover i a la derecha
            lo = i + 1

def mediana(A, B):
    N = len(A) + len(B)
    if N % 2:
        return kth(A, B, N // 2 + 1)
    return (kth(A, B, N // 2) + kth(A, B, N // 2 + 1)) / 2
```

## 3. Figura — la partición que busca el algoritmo

$A=[1,3,8,9,15]$, $B=[7,11,18,19,21]$, $k=5$ (quinto menor). Con $i=2$ de $A$ y $j=3$
de $B$ a la izquierda:

```
            izquierda (k=5 elementos)        |   derecha
   A :   1    3   ‖   8    9   15             ‖   corte A tras i=2
   B :   7   11   18 ‖ 19   21                ‖   corte B tras j=3
          └────┬────┘                            └───┬────┘
   izq = {1,3, 7,11,18}   der = {8,9,15, 19,21}

   condiciones:  A[i-1]=3 ≤ B[j]=19  ✓     B[j-1]=18 ≤ A[i]=8 ?  ✗  (18>8)
   -> B[j-1] > A[i]: mover i a la DERECHA (tomar mas de A)
```

En este ejemplo, la búsqueda sigue moviendo el corte a la derecha: con $i=3,j=2$ aún
se cumple $B[j-1]=11>A[i]=9$. Al llegar a $i=4,j=1$, las fronteras son
$A[i-1]=9\le B[j]=11$ y $B[j-1]=7\le A[i]=15$. La partición ya es válida; sus cinco
elementos izquierdos son $1,3,7,8,9$, así que el quinto menor es $9$, el mayor de la
izquierda.

## 4. Correctitud — invariante (C3)

> **Invariante.** El intervalo $[lo,hi]$ de valores de $i$ **contiene** siempre el
> $i^\*$ que produce la partición válida.

- **Inicialización.** $i$ debe cumplir $0\le i\le m$ y $0\le k-i\le n$, es decir
  $\max(0,k-n)\le i\le\min(k,m)$. Ese es exactamente $[lo,hi]$ inicial, que contiene
  a $i^\*$.
- **Mantenimiento.** En cada vuelta se mira $i$ y se comparan las cuatro fronteras.
  - Si `Aizq <= Bder and Bizq <= Ader`: la partición es válida; **todo** izquierdo
    $\le$ **todo** derecho (porque dentro de cada arreglo ya está ordenado y las
    fronteras cruzadas lo garantizan), luego el mayor de la izquierda es el $k$-ésimo
    menor global. Devolvemos y terminamos.
  - Si `Aizq > Bder` ($A[i-1]>B[j]$): entonces $A[i-1]$ es demasiado grande para estar
    a la izquierda; cualquier partición válida usa **menos** de $A$, así $i^\*<i$ y
    poner $hi=i-1$ mantiene a $i^\*$ en el intervalo.
  - Si `Bizq > Ader` ($B[j-1]>A[i]$): simétrico, $i^\*>i$, $lo=i+1$.
- **Conclusión.** Siempre existe una partición válida (lema abajo), y como el invariante
  mantiene $i^\*\in[lo,hi]$ y el intervalo se reduce, la búsqueda da con ella.

**Lema de existencia.** La función "número de elementos $\le$ al valor de corte" es
monótona en $i$, así que la condición de validez tiene solución única $i^\*$; como
$k\le m+n$, el corte con $k$ a la izquierda existe. (Es el mismo estilo de demostración
de "si la solución óptima tiene cierta propiedad" de C2, §3.)

**Terminación (potencial).** $\Phi=hi-lo$ baja a la mitad cada vuelta (binaria),
$\ge0$: $O(\log(hi-lo))=O(\log\min(m,n))$ vueltas, $O(1)$ cada una. **$O(\log n)$.**

## 5. Costo

| recurso | valor |
|---|---|
| tiempo | $O(\log\min(m,n)) = O(\log n)$ para $m=n$ |
| memoria extra | $O(1)$ (solo índices) |

Mucho mejor que mezclar los dos arreglos hasta la posición $k$, que sería $O(k)=O(n)$.

## 6. Cota de información (C5, §3)

Modelo de **comparaciones**. ¿Cuántas salidas distintas puede tener el problema? El
$k$-ésimo menor es uno de los $m+n$ elementos; equivalentemente, el resultado está
determinado por **cuántos** elementos de $A$ quedan a la izquierda del corte, es decir
por el índice $i^\*\in[\max(0,k-n),\min(k,m)]$. El número de valores posibles de $i^\*$
es
$$L = \min(k,m) - \max(0,k-n) + 1 \le \min(m,n)+1.$$

Por el lema 1 de C5 (árbol binario de altura $h$ tiene $\le 2^h$ hojas), un algoritmo
de comparaciones que distingue $L$ salidas necesita altura
$$h \ge \lceil \log_2 L \rceil = \Omega(\log \min(m,n)) = \Omega(\log n).$$

Como el algoritmo de la §2 hace $O(\log n)$ comparaciones y la cota de información es
$\Omega(\log n)$, el algoritmo es **óptimo** en el modelo de comparaciones. (C5, §3: la
información da $\log_2$ del número de salidas; aquí las salidas son las $\sim\min(m,n)$
posiciones posibles del corte.)

## 7. Comprobación — contra el oráculo de mezcla

```python
import random

def kth_oraculo(A, B, k):
    return sorted(A + B)[k - 1]

random.seed(7)
pruebas, peor_vueltas = 0, 0
for _ in range(20_000):
    m = random.randint(1, 30)
    n = random.randint(1, 30)
    A = sorted(random.randint(-20, 20) for _ in range(m))
    B = sorted(random.randint(-20, 20) for _ in range(n))
    for k in range(1, m + n + 1):
        assert kth(A, B, k) == kth_oraculo(A, B, k)
    # mediana
    N = m + n
    if N % 2:
        med = kth_oraculo(A, B, N // 2 + 1)
    else:
        med = (kth_oraculo(A, B, N // 2) + kth_oraculo(A, B, N // 2 + 1)) / 2
    assert mediana(A, B) == med
    pruebas += 1
print(f"{pruebas:,} pares (A,B): kth y mediana coinciden con el oraculo para todo k")
```

**Salida:**

```
20,000 pares (A,B): kth y mediana coinciden con el oraculo para todo k
```

## 8. Resumen

- **Algoritmo:** binaria sobre cuántos elementos de $A$ van a la izquierda del corte;
  $O(\log\min(m,n))$, memoria $O(1)$.
- **Invariante:** $[lo,hi]$ contiene siempre el corte válido $i^\*$; la partición
  válida da el $k$-ésimo como el mayor de la izquierda.
- **Cota de información:** hay $\sim\min(m,n)$ salidas posibles $\Rightarrow$
  $\Omega(\log n)$ comparaciones; el algoritmo la alcanza y es óptimo.

