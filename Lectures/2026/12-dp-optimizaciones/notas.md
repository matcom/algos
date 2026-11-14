# Optimizaciones de programación dinámica {#chap-dp-optimizaciones}

Hasta aquí, lo difícil de una programación dinámica era encontrar la recurrencia. En
este capítulo la recurrencia ya está bien, y la pregunta es **cuánto cuesta evaluarla**.
Veremos dos maneras de bajar ese costo: hacer menos transiciones, porque el óptimo vive
en una franja estrecha, y guardar menos memoria, recalculando. Las dos son teoremas
sobre la recurrencia, y el error plantado muestra qué pasa cuando se aplica una a un
problema que no cumple su hipótesis.

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
import tracemalloc

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_12.py
import figuras as F
import figuras_12 as G
```

## 1. Cuando la recurrencia ya está bien

Una programación dinámica cuesta, en tiempo, el número de estados por el trabajo de
cada uno, y en memoria, lo que se guarda. La subsecuencia común más larga tiene $nm$
estados y trabajo constante en cada uno; Held-Karp, en el capítulo 11, tiene $2^n n$
estados y $O(n)$ de trabajo en cada uno.

El ejemplo de este capítulo es una DP **sobre intervalos**: el estado es un intervalo
$[i, j]$ y la transición elige un punto de corte $k$ dentro de él. Son $O(n^2)$ estados
con $O(n)$ cortes cada uno, $O(n^3)$ en total. Knuth demostró en 1971 que, para el árbol
binario de búsqueda óptimo, el corte óptimo de $[i, j]$ está atrapado entre los cortes
óptimos de dos intervalos vecinos, y que recorrer solo esa franja cuesta $O(n^2)$ en
total.

La segunda mitad baja la memoria de la subsecuencia común más larga de $O(nm)$ a
$O(n + m)$ con un divide y vencerás sobre la tabla
(D. S. Hirschberg, «A linear space algorithm for computing maximal common
subsequences», *Communications of the ACM* 18(6), 1975, 341–343). Su tiempo se acota por sustitución, como en el capítulo 6, §10.

## 2. El árbol binario de búsqueda óptimo

Tenemos $n$ claves ordenadas, $1 < 2 < \dots < n$, y sabemos cuántas veces se va a
buscar cada una: la clave $k$ se busca $f_k$ veces. Buscar una clave que está a
profundidad $p$ (la raíz tiene profundidad 0) cuesta $p + 1$ comparaciones. Queremos el
árbol binario de búsqueda que minimiza el total,
$$\sum_{k=1}^{n} f_k\,(p_k + 1).$$
Un árbol equilibrado no sirve: una clave muy buscada conviene subirla aunque el árbol
quede cojo.

Llamemos $c(i, j)$ al costo mínimo de un árbol con las claves $i+1, \dots, j$, con
$c(i, i) = 0$ para el árbol vacío, y $w(i, j) = f_{i+1} + \dots + f_j$. Si la raíz es
$k$, el subárbol izquierdo tiene las claves $i+1, \dots, k-1$ y el derecho
$k+1, \dots, j$. Al colgarlos de la raíz, cada una de sus claves baja un nivel y paga
una comparación más, y la raíz paga una. En total se suma una vez la frecuencia de cada
clave del intervalo:
$$c(i, j) = w(i, j) + \min_{i < k \le j} \bigl( c(i, k-1) + c(k, j) \bigr).$$
Los subárboles de un árbol óptimo tienen que ser óptimos, porque cambiar uno por otro
más barato no toca el resto de la cuenta. El resultado es $c(0, n)$. Llamamos
$K(i, j)$ a la **mayor** raíz que alcanza el mínimo; el porqué de "mayor" aparece en la
§6.

El código llena la tabla por intervalos de largo creciente y cuenta cuántas veces evalúa
un corte. El oráculo enumera todos los árboles con las claves dadas, que para 7 claves
son 429 (el número de Catalan), y les calcula el costo con la definición.

```{python continue}
def abb_optimo(f):
    """c[i][j]: costo mínimo con las claves i+1..j. K[i][j]: la mayor raíz óptima."""
    n = len(f)
    pre = [0]
    for x in f:
        pre.append(pre[-1] + x)                     # w(i, j) = pre[j] - pre[i]
    c = [[0] * (n + 1) for _ in range(n + 1)]
    K = [[0] * (n + 1) for _ in range(n + 1)]
    evaluaciones = 0
    for d in range(1, n + 1):                       # d = j - i claves
        for i in range(n - d + 1):
            j = i + d
            mejor = None
            for k in range(i + 1, j + 1):
                evaluaciones += 1
                v = c[i][k - 1] + c[k][j]
                if mejor is None or v <= mejor:     # <= se queda con la mayor raíz
                    mejor, K[i][j] = v, k
            c[i][j] = mejor + pre[j] - pre[i]
    return c, K, evaluaciones

def arboles(i, j):
    """Todos los árboles con las claves i+1..j, como (raíz, izquierdo, derecho)."""
    if i == j:
        yield None
        return
    for k in range(i + 1, j + 1):
        for izq in arboles(i, k - 1):
            for der in arboles(k, j):
                yield (k, izq, der)

def costo(arbol, f, nivel=1):
    if arbol is None:
        return 0
    k, izq, der = arbol
    return f[k - 1] * nivel + costo(izq, f, nivel + 1) + costo(der, f, nivel + 1)

random.seed(12)
instancias = 0
for n in range(1, 8):
    for _ in range(20):
        f = [random.randint(0, 9) for _ in range(n)]
        assert abb_optimo(f)[0][0][n] == min(costo(a, f) for a in arboles(0, n))
        instancias += 1
print("árboles con 7 claves:", sum(1 for _ in arboles(0, 7)))
print("instancias en que la DP coincide con la enumeración:", instancias)
```

Hay $\Theta(n^2)$ intervalos y el de largo $d$ prueba $d$ raíces, así que la DP hace
$\sum_{d=1}^{n} d\,(n - d + 1) = n(n+1)(n+2)/6$ evaluaciones: es $\Theta(n^3)$. El resto
del trabajo, la suma de prefijos y la tabla, es $O(n^2)$.

## 3. La tabla de raíces

Antes de buscar un atajo, miremos qué raíces elige la DP. Tomamos ocho claves con
frecuencias variadas e imprimimos $K(i, j)$: la fila es $i$ y la columna es $j$.

```{python continue}
f = [3, 8, 2, 5, 9, 1, 4, 6]
n = len(f)
c, K, _ = abb_optimo(f)
print("costo óptimo:", c[0][n])
for i in range(n):
    print(f"i={i}:", " ".join(f"{K[i][j]:2d}" if j > i else " ." for j in range(1, n + 1)))
```

Fíjate en dos cosas. En cada fila, las raíces nunca bajan al moverse a la derecha: si al
intervalo se le agrega una clave por la derecha, la raíz no se mueve a la izquierda. Y en
cada columna nunca bajan al moverse hacia abajo: si al intervalo se le quita una clave
por la izquierda, la raíz tampoco se mueve a la izquierda. Juntas dicen que
$$K(i, j-1) \;\le\; K(i, j) \;\le\; K(i+1, j).$$
La raíz del intervalo $[i, j]$ está entre la raíz del intervalo sin su última clave y la
del intervalo sin su primera clave. En la figura, esas dos celdas son las vecinas de la
izquierda y de abajo.

```{python continue echo=false output=asis}
print(G.raices(K, n, (0, n), ident="dpopt-raices",
      pie=f"La tabla de raíces óptimas K(i, j) de las {n} claves. La raíz de "
          f"[0, {n}] está entre la de su vecina izquierda, K(0, {n-1}) = {K[0][n-1]}, "
          f"y la de su vecina de abajo, K(1, {n}) = {K[1][n]}: Knuth prueba "
          + ("una sola raíz" if K[1][n] == K[0][n-1] else f"{K[1][n] - K[0][n-1] + 1} raíces")
          + f" en lugar de {n}."))
```

Un ejemplo no es un teorema. Probamos la desigualdad en tres mil instancias al azar de
hasta 12 claves, con frecuencias entre 0 y 4 para que haya muchos empates.

```{python continue}
def monotona(K, n):
    return all(K[i][j - 1] <= K[i][j] <= K[i + 1][j]
               for i in range(n) for j in range(i + 2, n + 1))

random.seed(3)
casos = [[random.randint(0, 4) for _ in range(random.randint(2, 12))]
         for _ in range(3000)]
print("violaciones:", sum(not monotona(abb_optimo(f)[1], len(f)) for f in casos),
      "de", len(casos))
```

Ninguna. El experimento propone el enunciado y las §5 y §6 lo demuestran. La función
`monotona` sí puede fallar: en la §7 encuentra violaciones.

## 4. Knuth: recorrer solo la franja

Si la desigualdad vale, al calcular $c(i, j)$ basta probar las raíces
$k \in [K(i, j-1),\, K(i+1, j)]$. Las dos vecinas son más cortas y ya están
calculadas. Los intervalos de una clave, sin vecinas, se llenan aparte.

```{python continue}
def abb_knuth(f):
    n = len(f)
    pre = [0]
    for x in f:
        pre.append(pre[-1] + x)
    c = [[0] * (n + 1) for _ in range(n + 1)]
    K = [[0] * (n + 1) for _ in range(n + 1)]
    evaluaciones = 0
    for i in range(n):
        c[i][i + 1], K[i][i + 1] = f[i], i + 1
    for d in range(2, n + 1):
        for i in range(n - d + 1):
            j = i + d
            mejor = None
            for k in range(K[i][j - 1], K[i + 1][j] + 1):     # la franja
                evaluaciones += 1
                v = c[i][k - 1] + c[k][j]
                if mejor is None or v <= mejor:
                    mejor, K[i][j] = v, k
            c[i][j] = mejor + pre[j] - pre[i]
    return c, K, evaluaciones

for f in casos:
    assert abb_knuth(f)[0][0][len(f)] == abb_optimo(f)[0][0][len(f)]
print("Knuth coincide con la DP cúbica en", len(casos), "instancias")

random.seed(4)
evals = []
for n in (10, 20, 40, 80, 160):
    f = [random.randint(1, 100) for _ in range(n)]
    e3, e2 = abb_optimo(f)[2], abb_knuth(f)[2]
    cota = sum(2 * n - d for d in range(2, n + 1))
    evals.append((n, e3, e2))
    print(f"n={n:3d}  cúbica {e3:6d}  Knuth {e2:5d}  cota {cota:5d}  Knuth/n² {e2 / n**2:.2f}")
```

**Lema (la suma telescópica).** Si los $K$ cumplen la desigualdad de la §3, el algoritmo
hace a lo sumo $(3n^2 - 5n + 2)/2$ evaluaciones.

*Demostración.* Fijemos el largo $d \ge 2$. El intervalo que empieza en $i$ prueba
$K(i+1, i+d) - K(i, i+d-1) + 1$ raíces, y sumamos sobre $i = 0, \dots, n-d$. El primer
término del sumando $i$ es $K(i+1, i+d)$, y el segundo término del sumando $i+1$ es
$-K(i+1, (i+1) + d - 1)$, que es el mismo número con signo contrario. Todo se cancela
salvo los extremos:
$$\sum_{i=0}^{n-d} \bigl( K(i+1, i+d) - K(i, i+d-1) + 1 \bigr)
  = K(n-d+1, n) - K(0, d-1) + (n - d + 1).$$
Una raíz está entre 1 y $n$, así que esto es a lo sumo $n - 1 + n - d + 1 = 2n - d$. Al
sumar sobre $d = 2, \dots, n$ queda
$\sum_{d=2}^{n} (2n - d) = 2n(n-1) - \bigl(n(n+1)/2 - 1\bigr) = (3n^2 - 5n + 2)/2$. $\square$

La columna "cota" de la salida es esa suma, y el conteo de Knuth queda siempre debajo,
cerca de $n^2$. El paso que todo el mundo se salta es que la franja **no es corta**: una
celda sola puede probar casi $n$ raíces. Lo corto es la suma de una diagonal, como en el
análisis agregado del capítulo 4, §2.

```{python continue echo=false output=asis}
print(F.grafica_log_log(
    {"DP cúbica": [(n, e3) for n, e3, _ in evals],
     "Knuth": [(n, e2) for n, _, e2 in evals]},
    "número de claves n", "evaluaciones", ident="dpopt-evaluaciones",
    pie="Evaluaciones de un corte, contadas, en escala logarítmica. La pendiente de "
        "la DP cúbica es 3 y la de Knuth es 2."))
```

Falta lo principal: que la desigualdad de la §3 sea cierta, y que con ella el algoritmo
devuelva el óptimo.

## 5. La desigualdad del cuadrilátero

La demostración pasa por una propiedad de $c$ sobre cuatro índices. Una función $g$
sobre intervalos cumple la **desigualdad del cuadrilátero** si
$$g(a, c) + g(b, d) \;\le\; g(a, d) + g(b, c) \qquad \text{para } a \le b \le c \le d.$$
Se lee así: los dos intervalos que se cruzan, $[a, c]$ y $[b, d]$, cuestan juntos a lo
sumo lo que el intervalo que los contiene a los dos, $[a, d]$, más el que está dentro de
los dos, $[b, c]$. Antes de demostrarla para $c$, la probamos con el código.

```{python continue}
def cuadrilatero(g, n):
    return all(g[a][cc] + g[b][d] <= g[a][d] + g[b][cc]
               for a, b, cc, d in itertools.combinations_with_replacement(range(n + 1), 4))

print("c cumple la desigualdad en",
      sum(cuadrilatero(abb_optimo(f)[0], len(f)) for f in casos[:300]), "de 300 casos")
```

Las sumas de frecuencias la cumplen con igualdad: $w(a, c) + w(b, d)$ cuenta una vez las
claves de $(a, b]$ y $(c, d]$ y dos veces las de $(b, c]$, igual que
$w(a, d) + w(b, c)$. Además $w$ es **monótona por inclusión**: si
$[b, c] \subseteq [a, d]$, entonces $w(b, c) \le w(a, d)$, porque las frecuencias no son
negativas.

Para escribir la demostración llamamos $c_k(i, j) = w(i, j) + c(i, k-1) + c(k, j)$ al
costo de usar la raíz $k$ en $[i, j]$. Entonces $c(i, j) = \min_k c_k(i, j)$, y para
cualquier raíz válida, $c(i, j) \le c_k(i, j)$. Ese "para cualquier raíz" es la
herramienta: para acotar un costo por arriba basta proponer una raíz, sin que sea la
óptima.

**Lema 1 (Yao).** Si $w$ cumple la desigualdad del cuadrilátero y es monótona por
inclusión, $c$ cumple la desigualdad del cuadrilátero.

*Demostración.* Por inducción en $d - a$. Si $a = b$ o $c = d$, los dos lados son
iguales término a término. Quedan dos casos.

*Caso $b = c$*, con $a < b < d$. Hay que ver que $c(a, b) + c(b, d) \le c(a, d)$,
porque $c(b, b) = 0$. Sea $z = K(a, d)$. Si $z \le b$, proponemos $z$ como raíz de
$[a, b]$, lo que vale porque $a < z \le b$:
$$c(a, b) + c(b, d) \le w(a, b) + c(a, z-1) + c(z, b) + c(b, d).$$
Los índices $z \le b \le b \le d$ cumplen la hipótesis de inducción, porque
$d - z < d - a$, y dan $c(z, b) + c(b, d) \le c(z, d) + c(b, b) = c(z, d)$. Con
$w(a, b) \le w(a, d)$, que es la monotonía, queda
$w(a, d) + c(a, z-1) + c(z, d) = c_z(a, d) = c(a, d)$. Si $z > b$, proponemos $z$ como
raíz de $[b, d]$, porque $b < z \le d$:
$$c(a, b) + c(b, d) \le c(a, b) + w(b, d) + c(b, z-1) + c(z, d).$$
La inducción sobre $a \le b \le b \le z-1$, donde $z - 1 - a < d - a$, da
$c(a, b) + c(b, z-1) \le c(a, z-1)$, y con $w(b, d) \le w(a, d)$ queda otra vez
$c_z(a, d) = c(a, d)$.

*Caso $b < c$*, con $a < b$ y $c < d$. Sean $z = K(a, d)$ e $y = K(b, c)$, las raíces
óptimas del lado derecho. Usamos esas mismas raíces en el lado izquierdo, cruzadas.

Si $z \le y$, proponemos $z$ para $[a, c]$ (vale: $a < z \le y \le c$) e $y$ para
$[b, d]$ (vale: $b < y \le c < d$):
$$c(a, c) + c(b, d) \le w(a, c) + w(b, d) + c(a, z-1) + c(b, y-1) + c(z, c) + c(y, d).$$
La inducción sobre $z \le y \le c \le d$, con $d - z < d - a$, da
$c(z, c) + c(y, d) \le c(z, d) + c(y, c)$. La desigualdad de $w$ da
$w(a, c) + w(b, d) \le w(a, d) + w(b, c)$. Reagrupando,
$$c(a, c) + c(b, d) \le \bigl[w(a, d) + c(a, z-1) + c(z, d)\bigr]
  + \bigl[w(b, c) + c(b, y-1) + c(y, c)\bigr] = c(a, d) + c(b, c).$$

Si $z > y$, proponemos $y$ para $[a, c]$ (vale: $a < b < y \le c$) y $z$ para $[b, d]$
(vale: $b < y < z \le d$):
$$c(a, c) + c(b, d) \le w(a, c) + w(b, d) + c(a, y-1) + c(b, z-1) + c(y, c) + c(z, d).$$
Ahora la inducción va sobre $a \le b \le y-1 \le z-1$, que vale porque $y > b$, y
$z - 1 - a < d - a$: da $c(a, y-1) + c(b, z-1) \le c(a, z-1) + c(b, y-1)$. Con la
desigualdad de $w$ se reagrupa igual que antes en $c_z(a, d) + c_y(b, c)$. $\square$

La monotonía de $w$ solo se usó en el caso $b = c$, donde el intervalo de dentro es
vacío y no tiene raíz que proponer. El ejercicio 9 muestra que no sobra.

## 6. La monotonía de la raíz

**Lema 2.** Si $c$ cumple la desigualdad del cuadrilátero, para $j - i \ge 2$,
$$K(i, j-1) \le K(i, j) \le K(i+1, j).$$

*Demostración de $K(i, j) \le K(i+1, j)$.* Tomemos dos raíces $k < k'$ que valen para
los dos intervalos $[i, j]$ e $[i+1, j]$, es decir, $i + 1 < k < k' \le j$. La
desigualdad del cuadrilátero sobre $i \le i+1 \le k-1 \le k'-1$ dice
$$c(i, k-1) + c(i+1, k'-1) \le c(i, k'-1) + c(i+1, k-1).$$
Sumamos a los dos lados $w(i, j) + w(i+1, j) + c(k, j) + c(k', j)$ y agrupamos:
$$c_k(i, j) + c_{k'}(i+1, j) \le c_{k'}(i, j) + c_k(i+1, j),$$
o sea,
$$c_{k'}(i+1, j) - c_k(i+1, j) \;\le\; c_{k'}(i, j) - c_k(i, j). \tag{$*$}$$
En palabras: si la raíz mayor $k'$ es al menos tan buena como $k$ en $[i, j]$, también
lo es en $[i+1, j]$. Ahora supongamos, por contradicción, que $k' = K(i, j)$ es mayor que
$k = K(i+1, j)$. Como $k > i + 1$, las dos raíces valen en los dos intervalos. El lado
derecho de $(*)$ es $\le 0$ porque $k'$ es óptima en $[i, j]$, así que
$c_{k'}(i+1, j) \le c_k(i+1, j)$, que es el mínimo. Entonces $k'$ también es óptima en
$[i+1, j]$ y es mayor que $K(i+1, j)$, que era la mayor. Contradicción.

*Demostración de $K(i, j-1) \le K(i, j)$.* Es la misma con el otro extremo. Para
$i < k < k' \le j-1$, la desigualdad sobre $k \le k' \le j-1 \le j$ es
$c(k, j-1) + c(k', j) \le c(k, j) + c(k', j-1)$. Sumando
$w(i, j) + w(i, j-1) + c(i, k-1) + c(i, k'-1)$ y agrupando,
$$c_{k'}(i, j) - c_k(i, j) \;\le\; c_{k'}(i, j-1) - c_k(i, j-1).$$
Si $k = K(i, j)$ fuera menor que $k' = K(i, j-1)$, el lado derecho sería $\le 0$, y $k'$
sería óptima en $[i, j]$ y mayor que $K(i, j)$. Contradicción. $\square$

El paso delicado está en "sumamos a los dos lados". Para llegar a
$(*)$, cada $c_k$ tiene que llevar el **mismo** término $w(i, j)$ sea cual sea la raíz,
porque si no, al agrupar sobra una diferencia de $w$ que la desigualdad no controla. En
el árbol de búsqueda se cumple: lo que se suma al colgar los subárboles depende del
intervalo, no de la raíz. La §7 es lo que pasa cuando no se cumple.

El otro paso delicado es la palabra "mayor". El lema habla de la mayor raíz óptima, y la
contradicción usa justo eso. Por simetría (invirtiendo el orden de las claves) también
vale con la menor (ejercicio 2), aunque el experimento de la §3 solo probó la mayor. Lo
que esta demostración no cubre es mezclar criterios, guardar a veces la mayor y a veces
la menor.

**Teorema (Knuth, 1971).** El algoritmo de la §4 calcula $c(0, n)$ en $O(n^2)$.

*Demostración.* Por inducción en el largo, el algoritmo guarda en cada celda el
verdadero $K(i, j)$, la mayor raíz óptima. Para $d = 1$ es la única raíz. Para $d \ge 2$,
las vecinas guardan sus verdaderos $K$, y por el Lema 2 el verdadero $K(i, j)$ está en la
franja. Así que el mínimo sobre la franja es el mínimo sobre todas las raíces, y el
recorrido con `<=` se queda con la última raíz óptima de la franja, que es $K(i, j)$
porque ninguna raíz óptima es mayor. El costo es el lema de la suma telescópica. $\square$

Knuth lo publicó en «Optimum binary search trees» (*Acta Informatica* 1, 1971,
14–25), también con búsquedas fallidas. Frances Yao dio la condición general, la desigualdad del cuadrilátero
sobre $w$ más la monotonía, en «Efficient dynamic programming using quadrangle
inequalities» (*STOC*, 1980, 429–435).

## 7. El error plantado: Knuth en la cadena de matrices

La cadena de matrices de Estructuras de Datos tiene la misma forma. Las matrices
$A_1, \dots, A_n$ tienen dimensiones $d_0 \times d_1, d_1 \times d_2, \dots$, y el costo
mínimo de multiplicar $A_{i+1} \cdots A_j$ es
$$m(i, j) = \min_{i < k < j} \bigl( m(i, k) + m(k, j) + d_i\, d_k\, d_j \bigr),
\qquad m(i, i+1) = 0.$$
Es una DP sobre intervalos con un corte $k$, cúbica. La tentación es recorrer solo la
franja $[K(i, j-1), K(i+1, j)]$, como en la §4.

```{python continue}
def cadena(dims, knuth=False):
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    K = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1):
        m[i][i + 2], K[i][i + 2] = dims[i] * dims[i + 1] * dims[i + 2], i + 1
    for d in range(3, n + 1):
        for i in range(n - d + 1):
            j = i + d
            # una franja vacía dejaría mejor = None (TypeError)
            cortes = range(K[i][j - 1], K[i + 1][j] + 1) if knuth else range(i + 1, j)
            mejor = None
            for k in cortes:
                v = m[i][k] + m[k][j] + dims[i] * dims[k] * dims[j]
                if mejor is None or v <= mejor:
                    mejor, K[i][j] = v, k
            m[i][j] = mejor
    return m[0][n], K

def falla(dims):
    return cadena(dims)[0] != cadena(dims, knuth=True)[0]

random.seed(7)
al_azar = lambda n: [random.randint(1, 100) for _ in range(n + 1)]
baterias = {
    "8 matrices cuadradas": lambda: [7] * 9,
    "3 matrices al azar": lambda: al_azar(3),
    "8 matrices, dimensiones crecientes": lambda: sorted(al_azar(8)),
    "8 matrices, dimensiones decrecientes": lambda: sorted(al_azar(8), reverse=True),
    "4 matrices al azar": lambda: al_azar(4),
    "8 matrices al azar": lambda: al_azar(8),
}
for nombre, gen in baterias.items():
    print(f"{nombre:38s} {sum(falla(gen()) for _ in range(1000)):4d} fallos de 1000")
```

Las tres primeras baterías no lo ven nunca. Con matrices cuadradas todos los órdenes
cuestan lo mismo, y con tres matrices la franja de $[0, 3]$ va de $K(0, 2) = 1$ a
$K(1, 3) = 2$: todos los cortes. Cuatro matrices al azar, en cambio, fallan más de una
vez de cada cinco. Recorramos todas las dimensiones de 1 a 6:

```{python continue}
for n in (3, 4):
    malas = [d for d in itertools.product(range(1, 7), repeat=n + 1) if falla(list(d))]
    print(n, "matrices:", len(malas), "fallan; la primera:", malas[0] if malas else None)
dims = [1, 1, 2, 2, 1]
optimo, K = cadena(dims)
print("óptimo:", optimo, "  con la franja:", cadena(dims, knuth=True)[0])
print("K(0,3) =", K[0][3], "  K(1,4) =", K[1][4], "  K(0,4) =", K[0][4])
print("costo de cada corte de [0,4]:",
      {k: cadena(dims[:k + 1])[0] + cadena(dims[k:])[0] + dims[0] * dims[k] * dims[4]
       for k in (1, 2, 3)})
print("la tabla de raíces es monótona:", monotona(K, 4))
```

La raíz óptima de $[0, 4]$ queda a la izquierda de la franja, y la función `monotona`
de la §3 lo detecta.

¿Qué paso de la demostración anunciaba el error? El de la §6 que agrupaba los términos.
En la cadena, lo que se suma al elegir el corte es $d_i\, d_k\, d_j$, que **depende de
$k$**. Repitamos ese paso con los subproblemas de la cadena, $m(i, k) + m(k, j)$ en lugar
de $c(i, k-1) + c(k, j)$, y $m_k(i, j) = m(i, k) + m(k, j) + d_i d_k d_j$. Para llegar a
$m_k(i, j) + m_{k'}(i+1, j)$ el lado izquierdo recibe $d_i d_k d_j + d_{i+1} d_{k'} d_j$,
y para llegar a $m_{k'}(i, j) + m_k(i+1, j)$ el derecho recibe
$d_i d_{k'} d_j + d_{i+1} d_k d_j$. Los dos ya no son iguales: el izquierdo recibe
$$d_j\,(d_{i+1} - d_i)\,(d_{k'} - d_k)$$
más que el derecho, una cantidad que puede ser positiva, y $(*)$ deja de seguirse. La forma de la recurrencia era la misma, pero la hipótesis no, y una
batería de pruebas con matrices cuadradas o con cadenas cortas no lo distingue.

## 8. Memoria: la tabla de la subsecuencia común

La subsecuencia común más larga de $X$ (largo $n$) e $Y$ (largo $m$) llena una tabla $L[i][j] = \mathrm{LCS}(X_{<i}, Y_{<j})$, donde $X_{<i}$ son
las $i$ primeras letras de $X$:
$L[i][j] = L[i-1][j-1] + 1$ si $X_{i-1} = Y_{j-1}$, y si no,
$\max(L[i-1][j], L[i][j-1])$. Para la **longitud** basta la fila anterior. Para
saber **cuál** es la subsecuencia se recorre la tabla hacia atrás desde $L[n][m]$, y
hay que haberla guardado entera.

```{python continue}
def lcs_tabla(X, Y):
    n, m = len(X), len(Y)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            L[i][j] = (L[i - 1][j - 1] + 1 if X[i - 1] == Y[j - 1]
                       else max(L[i - 1][j], L[i][j - 1]))
    s, i, j = [], n, m                      # el camino hacia atrás
    while i and j:
        if X[i - 1] == Y[j - 1]:
            s.append(X[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(s))

print(lcs_tabla("ALGORITMO", "LOGARITMO"))
```

Con dos cadenas de un millón de letras, la tabla tiene $10^{12}$ celdas. Hirschberg
recupera la subsecuencia con $O(n + m)$ números, sin cambiar el tiempo $O(nm)$.

## 9. Hirschberg: el punto medio

La idea es preguntar por **un** punto del camino y no por el camino entero. Partimos
$X$ en $h = \lfloor n/2 \rfloor$. El camino óptimo cruza la fila $h$ en alguna columna
$k$. Si supiéramos $k$, la subsecuencia sería la de $X_{<h}$ con $Y_{<k}$ seguida de la
de $X_{\ge h}$ con $Y_{\ge k}$: dos problemas con a lo sumo $\lceil n/2 \rceil\, m$
celdas entre los dos, que se resuelven igual, recursivamente.

Para encontrar $k$ alcanza con longitudes, que sí caben en una fila. Sea
$F_k = \mathrm{LCS}(X_{<h}, Y_{<k})$, la última fila de la DP sobre la mitad de arriba,
y $B_k = \mathrm{LCS}(X_{\ge h}, Y_{\ge k})$, que es la DP sobre las dos cadenas al
revés.

**Lema 3.** $\mathrm{LCS}(X, Y) = \max_{0 \le k \le m} (F_k + B_k)$.

*Demostración.* ($\ge$) Para cada $k$, una subsecuencia común de $X_{<h}$ e $Y_{<k}$
seguida de una de $X_{\ge h}$ e $Y_{\ge k}$ es común a $X$ e $Y$, porque en las dos
cadenas la primera parte termina antes de que empiece la segunda. Mide $F_k + B_k$.

($\le$) Sea $S$ una subsecuencia común óptima, con sus letras emparejadas a posiciones
crecientes de $X$ y de $Y$. Sea $k$ la posición de $Y$ que sigue a la última letra de $S$
emparejada con una posición de $X$ menor que $h$ (o $k = 0$ si no hay ninguna). Las
letras emparejadas en $X_{<h}$ caen en $Y_{<k}$. Las demás están emparejadas con
posiciones de $X$ mayores o iguales que $h$ y, como los emparejamientos crecen en las
dos cadenas, con posiciones de $Y$ mayores o iguales que $k$. Así que
$|S| \le F_k + B_k$. $\square$

```{python continue}
CELDAS = [0]          # cuenta las celdas que calcula cada fila

def fila_adelante(X, Y, i0, i1, j0, j1):
    """F[t] = LCS(X[i0:i1], Y[j0:j0+t]), guardando una sola fila."""
    prev = [0] * (j1 - j0 + 1)
    for i in range(i0, i1):
        cur = [0]
        for j in range(j0, j1):
            cur.append(prev[j - j0] + 1 if X[i] == Y[j] else max(prev[j - j0 + 1], cur[-1]))
        prev = cur
        CELDAS[0] += j1 - j0
    return prev

def fila_atras(X, Y, i0, i1, j0, j1):
    """B[t] = LCS(X[i0:i1], Y[j0+t:j1]), la misma DP de derecha a izquierda."""
    prev = [0] * (j1 - j0 + 1)
    for i in range(i1 - 1, i0 - 1, -1):
        cur = [0] * (j1 - j0 + 1)
        for j in range(j1 - 1, j0 - 1, -1):
            t = j - j0
            cur[t] = prev[t + 1] + 1 if X[i] == Y[j] else max(prev[t], cur[t + 1])
        prev = cur
        CELDAS[0] += j1 - j0
    return prev

def corte(X, Y, i0, i1, j0, j1):
    h = (i0 + i1) // 2
    Fh = fila_adelante(X, Y, i0, h, j0, j1)
    Bh = fila_atras(X, Y, h, i1, j0, j1)
    t = max(range(j1 - j0 + 1), key=lambda t: Fh[t] + Bh[t])
    return h, j0 + t, Fh, Bh

X, Y = "ALGORITMO", "LOGARITMO"
h, k, Fh, Bh = corte(X, Y, 0, len(X), 0, len(Y))
print("h =", h, " k =", k, " F + B =", [a + b for a, b in zip(Fh, Bh)])
```

```{python continue echo=false output=asis}
print(G.hirschberg_corte(X, Y, h, Fh, Bh, k, ident="dpopt-hirschberg",
      pie=f"El primer nivel de Hirschberg sobre {X} y {Y}. La fila {h} parte a X; "
          f"debajo, F + B para cada columna. El máximo, "
          f"{Fh[k] + Bh[k]}, se alcanza primero en k = {k}, y la recursión sigue solo "
          f"en los dos rectángulos sombreados."))
```

El máximo, 7, es la longitud de la subsecuencia LGRITMO que encontró la tabla en la
§8, como dice el lema, y el código toma el primer $k$ que lo alcanza. Cualquiera sirve: la demostración del ($\ge$) no pide que el
punto sea único.

## 10. Hirschberg: el algoritmo y su costo

La recursión usa índices para no copiar pedazos de $Y$ en cada nivel. Cuando a $X$ le queda una letra, la respuesta es esa letra si aparece
en el pedazo de $Y$, y si no, nada.

```{python continue}
def hirschberg(X, Y, i0=0, i1=None, j0=0, j1=None, salida=None):
    if i1 is None:
        i1, j1, salida = len(X), len(Y), []
    if i0 == i1 or j0 == j1:
        pass
    elif i1 - i0 == 1:
        CELDAS[0] += j1 - j0
        if any(X[i0] == Y[j] for j in range(j0, j1)):
            salida.append(X[i0])
    else:
        h, k = corte(X, Y, i0, i1, j0, j1)[:2]     # no guardamos las filas
        hirschberg(X, Y, i0, h, j0, k, salida)
        hirschberg(X, Y, h, i1, k, j1, salida)
    return "".join(salida)

def es_subsecuencia(s, X):
    it = iter(X)
    return all(letra in it for letra in s)

random.seed(10)
for _ in range(2000):
    X = "".join(random.choice("ACGT") for _ in range(random.randint(0, 14)))
    Y = "".join(random.choice("ACGT") for _ in range(random.randint(0, 14)))
    s = hirschberg(X, Y)
    assert len(s) == len(lcs_tabla(X, Y)) and es_subsecuencia(s, X) and es_subsecuencia(s, Y)
print("Hirschberg coincide con la tabla en 2000 pares; ALGORITMO, LOGARITMO ->",
      hirschberg("ALGORITMO", "LOGARITMO"))
```

Sobre ALGORITMO y LOGARITMO, Hirschberg devuelve LORITMO y la tabla devolvía LGRITMO.
Las dos miden 7: hay más de una óptima. Por eso la prueba compara longitudes y comprueba
que la salida sea subsecuencia de las dos cadenas.

**El tiempo.** Contemos las celdas. Un nivel con $n$ letras de $X$ y $m$ de $Y$ calcula
$h \cdot m$ celdas hacia adelante y $(n - h)\, m$ hacia atrás: exactamente $nm$, lo mismo
que la tabla entera. Después recurre sobre $h \times k$ y $(n - h) \times (m - k)$, que
suman a lo sumo $\lceil n/2 \rceil\, m$ celdas, la mitad de la tabla si $n$ es par. Si las mitades fueran exactas, la recurrencia sería
$C(n, m) = nm + C(n/2, k) + C(n/2, m-k)$, y la suposición $C \le 2nm$ cerraría por
sustitución: $nm + 2\tfrac{n}{2}k + 2\tfrac{n}{2}(m-k) = 2nm$. Esto es lo que se suele
decir: Hirschberg hace el doble de trabajo que la tabla.

Con techos la cuenta no cierra, y la medición lo confirma:

```{python continue}
def celdas(X, Y):
    CELDAS[0] = 0
    hirschberg(X, Y)
    return CELDAS[0]

for n in (8, 9, 1024):
    print(f"n={n:4d}, sin letras comunes: celdas/(nm) = {celdas('A' * n, 'B' * 5) / (5 * n):.3f}")
X = "".join(random.choice("ACGT") for _ in range(512))
Y = "".join(random.choice("ACGT") for _ in range(512))
print(f"n=m=512 al azar: celdas/(nm) = {celdas(X, Y) / 512**2:.3f}")
```

Con $n = 9$ y ninguna letra en común, todas las sumas $F_k + B_k$ valen 0 y el código
elige $k = 0$: la mitad de abajo, con $\lceil 9/2 \rceil = 5$ letras, se queda con todo
$Y$.

**Lema 4.** Sea $G(1) = 1$ y $G(n) = n + G(\lceil n/2 \rceil)$ para $n \ge 2$. Hirschberg
calcula a lo sumo $G(n)\, m$ celdas, y $G(n) \le 2n + \lceil \log_2 n \rceil - 1$.

*Demostración.* Primero, $G$ no decrece: $G(2) = 3 > G(1)$, y si $G$ no decrece hasta
$n - 1$, entonces $G(n) - G(n-1) = 1 + G(\lceil n/2 \rceil) - G(\lceil (n-1)/2 \rceil)
\ge 1$. Ahora, por inducción en $n$. Con $n = 1$ el código recorre $Y$ una vez: $m$
celdas. Con $n \ge 2$, el nivel cuesta $nm$ y las mitades tienen
$\lfloor n/2 \rfloor \le \lceil n/2 \rceil$ letras, así que por inducción y porque $G$ no
decrece,
$$C(n, m) \le nm + G(\lfloor n/2 \rfloor)\,k + G(\lceil n/2 \rceil)(m - k)
  \le nm + G(\lceil n/2 \rceil)\,m = G(n)\,m.$$
Para la cota de $G$, también por inducción: $G(1) = 1 = 2 + 0 - 1$, y para $n \ge 2$,
usando $2\lceil n/2 \rceil \le n + 1$ y $\lceil \log_2 \lceil n/2 \rceil \rceil =
\lceil \log_2 n \rceil - 1$,
$$G(n) \le n + 2\lceil n/2 \rceil + \lceil \log_2 \lceil n/2 \rceil \rceil - 1
  \le 2n + \lceil \log_2 n \rceil - 1. \qquad \square$$

Así que $C(n, m) \le 2nm + m\lceil \log_2 n \rceil$: el doble de la tabla más un término
despreciable frente a $nm$. Con $n = 9$, $G(9) = 20 > 18$, la razón 2,222 de la salida;
con $n = 8$, potencia de 2, queda 1,875. Al azar da casi exactamente 2.

**La memoria.** En cada momento viven las dos filas del nivel que se está calculando,
$O(m)$, y la pila de la recursión, de profundidad $\lceil \log_2 n \rceil$ con un número
constante de índices por nivel. Las filas de un nivel se liberan antes de bajar, porque
`hirschberg` se queda solo con $h$ y $k$. Si desempaquetara `h, k, _, _`, la variable
`_` retendría una fila en cada nivel de la pila, y la memoria sería $\Theta(m \log n)$
cuando el corte cae siempre en un extremo. La salida tiene a lo sumo
$\min(n, m)$ letras. En total, $O(n + m)$. Lo medimos con `tracemalloc`, que registra el
pico de memoria que reserva Python:

```{python continue}
def pico(funcion, X, Y):
    tracemalloc.start()
    funcion(X, Y)
    _, maximo = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return maximo

random.seed(11)
memoria = {"tabla": [], "Hirschberg": []}
for n in (50, 100, 200, 400):
    X = "".join(random.choice("ACGT") for _ in range(n))
    Y = "".join(random.choice("ACGT") for _ in range(n))
    a, b = pico(lcs_tabla, X, Y), pico(hirschberg, X, Y)
    memoria["tabla"].append((n, a))
    memoria["Hirschberg"].append((n, b))
    print(f"n=m={n:3d}  tabla {a / 1024:8.1f} KiB   Hirschberg {b / 1024:5.1f} KiB")
for n in (2, 16, 256):    # sin letras comunes: el corte siempre en k = 0
    print(f"n={n:3d}, m=2000, sin letras comunes: Hirschberg "
          f"{pico(hirschberg, 'A' * n, 'B' * 2000) / 1024:5.1f} KiB")
```

```{python continue echo=false output=asis}
print(F.grafica_log_log(memoria, "largo n = m", "bytes", ident="dpopt-memoria",
      pie="Pico de memoria medido con tracemalloc, en escala logarítmica. La tabla "
          "completa crece con pendiente 2; Hirschberg, con pendiente menor que 1 en "
          "estos tamaños."))
```

Cuando $n$ se duplica, la tabla multiplica su memoria casi por cuatro, de 326,4 a
1282,0 KiB entre 200 y 400, y Hirschberg por menos de dos, de 5,2 a 10,0 KiB. En los
tamaños chicos pesa lo que Python reserva igual para cualquier llamada. Las cadenas al
azar no ponen a prueba la pila, porque los pedazos de $Y$ se achican al bajar. La entrada
sin letras comunes sí: deja todo $Y$ en la mitad de abajo en cada nivel, y aun así el pico
no crece con la profundidad.
Se paga el doble de tiempo para no guardar lo que se puede recalcular.

## 11. Otras dos franjas

**Divide y vencerás sobre el corte.** Algunas DP tienen capas: partir los $n$ primeros
elementos en $t$ bloques cuesta
$D_t(i) = \min_{j < i} \bigl( D_{t-1}(j) + C(j, i) \bigr)$, donde $C(j, i)$ es el costo
del bloque $(j, i]$. Evaluada así, cada capa cuesta $O(n^2)$. Si el corte óptimo
$\mathrm{opt}(i)$ no decrece con $i$, se calcula primero el del $i$ del medio, recorriendo
todos los candidatos, y después la mitad izquierda solo busca a la izquierda de él y la
derecha solo a la derecha. Cada nivel de esa recursión recorre en total $O(n)$
candidatos, porque los rangos de los $i$ de un mismo nivel se tocan solo en los extremos,
y hay $\lceil \log_2 n \rceil$ niveles: $O(n \log n)$ por capa. Como en Knuth, la
monotonía del corte es un teorema que hay que demostrar para cada $C$.

**La envolvente de rectas** (*convex hull trick*). Si la transición tiene la forma
$D(i) = \min_{j < i} \bigl( D(j) + b_j\, a_i \bigr)$, cada $j$ es una recta
$y = b_j x + D(j)$, y $D(i)$ es el mínimo de esas rectas en $x = a_i$. Si las pendientes
$b_j$ llegan ordenadas, se guardan en una pila solo las rectas que son mínimas en algún
punto. Cada recta entra una vez y sale a lo sumo una vez, como en el análisis agregado
del capítulo 4, y si además las $a_i$ crecen, las consultas avanzan con un puntero: $O(n)$
en total en lugar de $O(n^2)$.

## 12. La regla {#dp-optimizaciones-12-la-regla}

Una optimización de programación dinámica es un teorema sobre la recurrencia, y su
hipótesis es la lista de lo que el problema tiene que cumplir. Knuth pide que lo que se
suma no dependa del corte, cumpla la desigualdad del cuadrilátero y sea monótono por
inclusión. Hirschberg pide que el valor de un camino sea la suma de sus dos mitades, que
es lo que usó el Lema 3. Que la recurrencia tenga la misma forma no basta.

## Resumen {#dp-optimizaciones-resumen}

- Las optimizaciones de una DP bajan el tiempo (estados por transiciones) o la memoria
  sin tocar la recurrencia.
- **Árbol binario de búsqueda óptimo:**
  $c(i, j) = w(i, j) + \min_k (c(i, k-1) + c(k, j))$, cúbica tal como está.
- **Knuth:** la mayor raíz óptima cumple $K(i, j-1) \le K(i, j) \le K(i+1, j)$. Recorrer
  solo esa franja cuesta $O(n^2)$, por una suma telescópica sobre cada diagonal.
- La monotonía sale de la **desigualdad del cuadrilátero**
  $c(a, c) + c(b, d) \le c(a, d) + c(b, c)$, que $c$ hereda de $w$ si $w$ la cumple y es
  monótona por inclusión (Yao, 1980).
- El paso clave es que $w(i, j)$ no depende del corte. En la cadena de matrices sí, y
  Knuth da mal sin que lo vean las pruebas con matrices cuadradas o con 3 matrices.
- **Hirschberg:** el punto donde el camino óptimo cruza la fila media sale de dos filas,
  hacia adelante y hacia atrás. La subsecuencia común se recupera en memoria
  $O(n + m)$ y con a lo sumo $2nm + m\lceil \log_2 n \rceil$ celdas.

## Ejercicios {#dp-optimizaciones-ejercicios}

1. **[traza]** Cinco claves tienen frecuencias $f = (4, 2, 6, 3, 1)$. Llena a mano las
   tablas $c(i, j)$ y $K(i, j)$ (la mayor raíz óptima) y dibuja el árbol óptimo. Marca
   en la tabla de raíces las celdas donde Knuth prueba una sola raíz.

2. **[demostración]** Demuestra el Lema 2 para la **menor** raíz óptima. ¿Qué cambia en
   la contradicción? Si un programa guarda la mayor raíz en unas celdas y la menor en
   otras, ¿sigue valiendo la demostración del teorema de Knuth? ¿Y su resultado?

3. **[demostración]** El lema de la suma telescópica da $(3n^2 - 5n + 2)/2$. Demuestra
   que la DP cúbica hace exactamente $n(n+1)(n+2)/6$ evaluaciones y que Knuth hace al
   menos $n(n-1)/2$ en cualquier instancia. Para frecuencias todas iguales, ¿cuántas
   hace? Compara con la cota.

4. **[implementar y medir]** Hay $n$ montones de piedras en fila. Mezclar dos montones
   vecinos cuesta la suma de los dos, y se quiere mezclarlos todos en uno con costo
   mínimo. Escribe la DP sobre intervalos, implementa la versión cúbica y la de Knuth,
   compáralas en instancias al azar y mide las evaluaciones para $n = 10, \dots, 160$.
   La recurrencia es $c(i, j) = w(i, j) + \min_{i<k<j} (c(i, k) + c(k, j))$, con el
   corte compartido. ¿Qué cambia en los Lemas 1 y 2?

5. **[traza]** Aplica el primer nivel de Hirschberg a $X = \text{PARALELO}$ e
   $Y = \text{PARABOLA}$: calcula $F$ y $B$, las sumas $F_k + B_k$ y el corte $k$. Sigue
   la recursión hasta obtener la subsecuencia.

6. **[demostración]** Demuestra que, si $n$ es una potencia de 2, Hirschberg calcula a
   lo sumo $2nm$ celdas. Construye entradas con $n = 5$ y con $n = 9$ que obliguen a más
   de $2nm$ celdas con el código de la §10, y demuestra que con $n = 3$ o $n = 7$
   ninguna entrada lo logra.

7. **[modelar]** Se quiere partir un arreglo de $n$ enteros no negativos en $t$ bloques
   contiguos minimizando la suma de los cuadrados de las sumas de los bloques. Escribe
   la DP por capas de la §11. Demuestra que $C(j, i) = (P_i - P_j)^2$, con $P$ las sumas
   de prefijos, cumple la desigualdad del cuadrilátero, y adapta el Lema 2 para
   concluir que el corte óptimo no decrece. Implementa la optimización por divide y
   vencerás y demuestra que cuesta $O(t\, n \log n)$.

8. **[modelar]** Implementa la envolvente de rectas de la §11 para
   $D(i) = \min_{j < i} (D(j) + b_j\, a_i)$, con $D(0) = 0$, las $b_j$ decrecientes y
   las $a_i$ crecientes. Pruébala contra la DP cuadrática y explica por qué cada recta
   que sale de la pila no vuelve a ser mínima en ninguna consulta futura.

9. **[entrada que rompe]** Con tres claves, da una función $w(i, j)$ que no dependa de
   la raíz, con $w(i, i) = 0$ y valores que pueden ser negativos, que cumpla la
   desigualdad del cuadrilátero (también con $b = c$) y para la que la mayor raíz
   óptima no cumpla $K(i, j-1) \le K(i, j) \le K(i+1, j)$. ¿En qué caso de la
   demostración del Lema 1 se rompe el argumento?

10. **[cambio de hipótesis] ★** La distancia de edición con costos arbitrarios cobra
    $\delta(x)$ por borrar $x$, $\iota(y)$ por insertar $y$ y $\sigma(x, y)$ por
    sustituir. ¿Sigue valiendo Hirschberg? Reescribe el Lema 3 para este problema,
    demuéstralo y di qué propiedad de los costos usa. ¿Y si el costo de un hueco de
    largo $\ell$ fuera $\ell^2$ en lugar de proporcional a $\ell$?
