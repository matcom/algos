# Ejercicio 7 — Mediana de dos arreglos ordenados

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> El $k$-ésimo menor de los $2n$ elementos de dos arreglos ordenados de largo $n$.
> Diseña un algoritmo $O(\log n)$, demuestra su correctitud y da la cota de
> información.


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

## 4. Correctitud — guía para redactar la prueba (pendiente)

Redacta la prueba usando como invariante que el intervalo $[lo,hi]$ contiene **algún**
corte válido; no supongas que ese corte es único.

1. ¿Por qué existe al menos un corte válido con exactamente $k$ elementos a la
   izquierda? Considera el arreglo combinado ya ordenado y cuenta cuántos de esos $k$
   elementos pertenecen a $A$.
2. Si $A[i-1]>B[j]$, ¿por qué ningún corte válido puede tener índice $i$ o mayor?
   ¿Qué argumento simétrico vale si $B[j-1]>A[i]$?
3. Cuando se cumplen las dos desigualdades de frontera, ¿por qué el mayor elemento de
   la izquierda es el $k$-ésimo menor?
4. Da una medida entera del intervalo y explica por qué cada actualización lo reduce.

Hay arreglos con valores repetidos y varios cortes válidos. La prueba debe funcionar
aunque haya más de uno.
## 5. Costo

| recurso | valor |
|---|---|
| tiempo | $O(\log\min(m,n)) = O(\log n)$ para $m=n$ |
| memoria extra | $O(1)$ (solo índices) |

Mucho mejor que mezclar los dos arreglos hasta la posición $k$, que sería $O(k)=O(n)$.

## 6. Cota de información — guía para redactarla (pendiente)

La cuenta actual no demuestra que cada corte produzca una hoja distinta. Para rehacerla:

1. Fija $k=n$ y considera cuál de los $2n$ elementos puede ocupar el rango $n$.
   Construye una familia de entradas ordenadas que permita que cada identidad sea la
   respuesta.
2. ¿Cuántas respuestas distintas debe distinguir el algoritmo?
3. ¿Cuántos hijos tiene cada nodo si una comparación de elementos puede dar $<,=,>$?
   Usa esas cantidades para obtener una cota de altura y compárala con las
   $O(\log n)$ comparaciones del algoritmo.

Completa la demostración con tu propia redacción antes de entregar.
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

