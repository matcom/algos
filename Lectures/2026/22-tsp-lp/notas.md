# TSP métrico y redondeo de programas lineales {#chap-tsp-lp}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
from fractions import Fraction
from functools import lru_cache

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_22.py
import figuras_22 as F22
```

El capítulo 21 resolvió cinco problemas con una sola idea: una cota del óptimo que se
puede calcular, y una demostración de que el algoritmo paga a lo sumo $\alpha$ veces esa
cota. Este capítulo usa la misma idea con dos cotas nuevas. En el problema del viajante
con distancias métricas la cota es el árbol generador mínimo, y mirar con cuidado qué
parte de la cota se desperdicia lleva la razón de 2 a $3/2$. En vertex cover con pesos
la cota es el óptimo de un **programa lineal**, un problema que se resuelve en tiempo
polinomial y que queda por debajo del óptimo entero; el algoritmo lee la solución
fraccionaria y la redondea. Antes de las dos, una frontera: sin la desigualdad
triangular, el viajante no admite ninguna razón constante, salvo que P = NP.

## 1. El viajante, otra vez

Es la tercera vez que el libro trabaja con el viajante. Un recorrido visita una vez
cada una de $n$ ciudades y vuelve al inicio, y cuesta la suma de las distancias de sus
$n$ tramos. El capítulo 11, §9 lo resolvió exacto con Held-Karp en $O(2^n n^2)$. El
capítulo 19, §7 demostró que la versión de decisión es NP-completa, aun con distancias
1 y 2. Y el capítulo 21 dio la técnica para rendirse con garantía.

Aquí las distancias son simétricas, $d(u, v) = d(v, u)$, y cuando se diga **métrica**
cumplen además la desigualdad triangular, $d(u, w) \le d(u, v) + d(v, w)$, como los
puntos del plano. El oráculo es la recursión del capítulo 11, §9, sin los contadores.

```{python continue}
def held_karp(d):
    n = len(d)
    todas = (1 << (n - 1)) - 1                       # el bit j-1 es la ciudad j
    g = [[math.inf] * n for _ in range(todas + 1)]
    for j in range(1, n):
        g[1 << (j - 1)][j] = d[0][j]
    for S in range(1, todas + 1):
        for j in range(1, n):
            bit = 1 << (j - 1)
            if S & bit and S != bit:
                resto = S ^ bit
                g[S][j] = min(g[resto][i] + d[i][j] for i in range(1, n)
                              if resto >> (i - 1) & 1)
    return min(g[todas][j] + d[j][0] for j in range(1, n))
```

## 2. Sin desigualdad triangular no hay razón

El capítulo 21, §9 mostró que k-center no admite razón mejor que 2. Con el viajante
general pasa algo más fuerte: no admite **ninguna** razón constante. La herramienta es
la reducción del capítulo 19, §7, que daba distancia 1 a las aristas de un grafo y 2 a
las que faltan. Esa diferencia es pequeña: un recorrido que usa una no-arista cuesta
$n + 1$ contra $n$, y con $n \ge 10$ un algoritmo de razón $1{,}1$ no distingue los
dos casos. La idea
es hacer la no-arista tan cara que un algoritmo con garantía no pueda permitírsela.

**Teorema 1** (Sahni y Gonzalez, "P-complete approximation problems", *Journal of the
ACM* 23(3), 1976, pp. 555–565). Si P ≠ NP, para ninguna constante
$\alpha \ge 1$ hay una $\alpha$-aproximación polinomial del viajante con distancias
simétricas arbitrarias.

*Demostración.* Sea $A$ una $\alpha$-aproximación. Dado un grafo $G = (V, E)$ con $n$
vértices, construimos en tiempo $O(n^2)$ la entrada con una ciudad por vértice,
$d(u, v) = 1$ si $\{u, v\} \in E$ y $d(u, v) = c = (\alpha - 1)n + 2$ si no.

Si $G$ tiene un ciclo hamiltoniano, ese ciclo es un recorrido de costo $n$, así que
$\mathrm{OPT} = n$ y $A$ devuelve un recorrido de costo a lo sumo $\alpha n$. Si $G$ no
lo tiene, todo recorrido usa al menos una no-arista, y sus otros $n - 1$ tramos cuestan
al menos 1 cada uno, así que cuesta al menos $(n - 1) + c = \alpha n + 1$.

Entonces $G$ tiene ciclo hamiltoniano si y solo si $A$ devuelve un recorrido de costo a
lo sumo $\alpha n$, y esto se decide en tiempo polinomial. Como ciclo hamiltoniano es
NP-completo (capítulo 19, §6), P = NP. $\square$

El paso que se suele saltar es el tamaño de $c$: tiene que caber en un número de
$O(\log n)$ bits para que la reducción sea polinomial, y cabe porque $\alpha$ es
constante. Probémoslo sobre dos grafos de 10 y 8 vértices: el de
Petersen, que no tiene ciclo hamiltoniano, y el cubo, que sí lo tiene.

```{python continue}
def entrada_tsp(n, aristas, alfa):
    caro = (alfa - 1) * n + 2
    E = {frozenset(e) for e in aristas}
    return [[0 if i == j else 1 if frozenset((i, j)) in E else caro
             for j in range(n)] for i in range(n)]

petersen = (10, [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)]
            + [(5 + i, 5 + (i + 2) % 5) for i in range(5)])
cubo = (8, [(u, u ^ b) for u in range(8) for b in (1, 2, 4) if u < u ^ b])
for nombre, (n, aristas) in (("Petersen", petersen), ("cubo", cubo)):
    print(f"{nombre}: n = {n}, óptimo {held_karp(entrada_tsp(n, aristas, 2))}, "
          f"2n = {2 * n}")
```

Con $\alpha = 2$, el cubo da óptimo 8 y Petersen da 21, uno más que $2n = 20$. Un
algoritmo de razón 2 tendría que devolver a lo sumo 16 en el cubo, y en Petersen nunca
podría bajar de 21: la respuesta separa los dos casos.

Con $c > 2$, las distancias $1$ y $c$ no cumplen la desigualdad triangular, que es la
hipótesis que usa el resto del capítulo.

## 3. La cota del árbol mínimo

Desde aquí, la distancia es métrica. ¿Qué número fácil de calcular queda por debajo de
cualquier recorrido? Quita un tramo cualquiera de un recorrido: queda un camino que
pasa por las $n$ ciudades, y un camino que pasa por todos los vértices es un árbol
generador.

**Lema 2.** Si $T$ es un árbol generador mínimo de las ciudades, con peso $w(T)$,
entonces $w(T) \le \mathrm{OPT}$.

*Demostración.* Sea $R$ un recorrido óptimo y $e$ uno de sus tramos. $R - e$ es un
camino hamiltoniano, que es un árbol generador, así que
$w(T) \le w(R - e) = \mathrm{OPT} - d(e) \le \mathrm{OPT}$. $\square$

El lema no usa la desigualdad triangular. El árbol mínimo se calcula con Prim o con Kruskal, el goloso que el capítulo
10, §7 demostró óptimo como caso de un matroide. Aquí va Prim en su versión de
$O(n^2)$, que es la buena para un grafo completo:

```{python continue}
def distancias(P):
    return [[math.dist(p, q) for q in P] for p in P]

def costo(d, gira):
    return sum(d[a][b] for a, b in zip(gira, gira[1:] + gira[:1]))

def prim(d):
    n = len(d)
    dentro, mejor, padre = [False] * n, [math.inf] * n, [None] * n
    mejor[0], arbol = 0, []
    for _ in range(n):
        u = min((v for v in range(n) if not dentro[v]), key=lambda v: mejor[v])
        dentro[u] = True
        if padre[u] is not None:
            arbol.append((padre[u], u))
        for v in range(n):
            if not dentro[v] and d[u][v] < mejor[v]:
                mejor[v], padre[v] = d[u][v], u
    return arbol

rng = random.Random(22)
P = [(rng.random(), rng.random()) for _ in range(9)]
d = distancias(P)
T = prim(d)
opt = held_karp(d)
print(f"árbol mínimo {sum(d[u][v] for u, v in T):.3f}, óptimo {opt:.3f}")
```

Sobre 9 puntos al azar (semilla 22) el árbol pesa 2,512 y el recorrido óptimo 3,469. La
cota está a un 28 % del óptimo. Queda construir un recorrido a partir del árbol, y
demostrar que no cuesta mucho más que él.

## 4. El doble árbol

Recorre el árbol como lo haría una búsqueda en profundidad: sales de la raíz, bajas por
cada hijo y vuelves. Ese paseo cruza cada arista del árbol dos veces, una al bajar y
otra al subir, así que cuesta exactamente $2w(T)$, y pasa por todas las ciudades. No es
un recorrido, porque repite ciudades. Para convertirlo en uno, salta las repetidas: si
el paseo va $u \to v \to w$ y $v$ ya se visitó, ve directo de $u$ a $w$. Eso es un
**atajo**. Lo que queda es la lista de ciudades en el orden en que el paseo las ve por
primera vez, que es el **preorden** del árbol.

```{python continue}
def preorden(n, arbol, raiz=0):
    vecinos = [[] for _ in range(n)]
    for u, v in arbol:
        vecinos[u].append(v)
        vecinos[v].append(u)
    orden, visto = [], [False] * n
    def bajar(u):
        visto[u] = True
        orden.append(u)
        for v in sorted(vecinos[u]):
            if not visto[v]:
                bajar(v)
    bajar(raiz)
    return orden

def doble_arbol(d):
    return preorden(len(d), prim(d))

gira = doble_arbol(d)
print(f"doble árbol {costo(d, gira):.3f}, 2·árbol {2 * sum(d[u][v] for u, v in T):.3f}, "
      f"óptimo {opt:.3f}")
```

```{python continue echo=false output=asis}
print(F22.doble_arbol(P, T, gira, pie=(
    "El doble árbol sobre 9 puntos al azar (semilla 22). A la izquierda, el árbol "
    "mínimo con la posición de cada ciudad en el preorden. A la derecha, el recorrido "
    "que sale de visitar las ciudades en ese orden; cada flecha que no sigue una "
    "arista del árbol (en gris) es un atajo sobre ciudades ya vistas.")))
```

La @fig-tsp-doble-arbol muestra los dos pasos. El recorrido cuesta 4,302, por debajo
del doble del árbol, 5,024, y un 24 % por encima del óptimo.

**Teorema 3.** Con distancias métricas, el doble árbol devuelve un recorrido de costo
a lo sumo $2\,\mathrm{OPT}$, en tiempo $O(n^2)$.

*Demostración.* Sea $W$ el paseo del árbol, de costo $2w(T)$, y $v_1, \dots, v_n$ el
preorden. Entre dos ciudades consecutivas del preorden, $v_i$ y $v_{i+1}$, el paseo
recorre un tramo $v_i = a_0, a_1, \dots, a_k = v_{i+1}$, y aplicando la desigualdad
triangular $k - 1$ veces,
$$d(v_i, v_{i+1}) \le d(a_0, a_1) + d(a_1, a_2) + \dots + d(a_{k-1}, a_k).$$
Lo mismo con el tramo final, de $v_n$ de vuelta a la raíz. Los tramos del paseo entre
ciudades consecutivas del preorden no se solapan y juntos forman todo $W$. Sumando,
el recorrido cuesta a lo sumo $2w(T)$, y por el lema 2, a lo sumo $2\,\mathrm{OPT}$.
Prim cuesta $O(n^2)$ y el preorden $O(n)$. $\square$

El único paso que usa la métrica es el de los atajos, y es el que el teorema 1 hace
imposible: con distancias 1 y $c$, un atajo de dos tramos de costo 1 puede costar $c$.
El ejercicio 2 pide escribir con cuidado por qué saltar varias ciudades seguidas no
alarga, y el ejercicio 3, una familia donde la razón se acerca a 2.

## 5. Contra el oráculo

¿Cuánto paga el doble árbol en la práctica? Una batería de puntos al azar, de 5 a 9
ciudades, contra Held-Karp:

```{python continue}
def bateria(algoritmo, semilla=22, veces=150):
    rng = random.Random(semilla)
    razones = []
    for _ in range(veces):
        Q = [(rng.random(), rng.random()) for _ in range(rng.randint(5, 9))]
        dq = distancias(Q)
        gira = algoritmo(dq)
        assert sorted(gira) == list(range(len(Q)))       # es un recorrido
        razones.append(costo(dq, gira) / held_karp(dq))
    return razones

r_doble = bateria(doble_arbol)
print(f"{len(r_doble)} entradas, peor {max(r_doble):.3f}, "
      f"promedio {sum(r_doble) / len(r_doble):.3f}")
```

La peor razón medida es 1,412, lejos de 2, y en promedio el doble árbol paga un 12 %
de más. La batería no encuentra el peor caso; el ejercicio 3 lo construye.

## 6. Lo que se paga de más

¿Dónde se pierde la razón 2? En que el paseo cruza **cada** arista dos veces. Para
recorrer un multigrafo de un tirón y volver al inicio basta que cada vértice tenga
grado par: se entra y se sale el mismo número de veces. Duplicar el árbol es la manera
más cara de lograrlo; basta arreglar los vértices de grado impar.

**Euler.** Un multigrafo conexo en el que todo vértice tiene grado par tiene un
**circuito euleriano**: un paseo cerrado que usa cada arista exactamente una vez.

*Demostración.* Por inducción sobre el número de aristas. Sal de un vértice $v$ con
aristas y camina usando aristas no usadas. Cada vez que entras a un $u \ne v$ has usado
un número impar de sus aristas, y como su grado es par queda al menos una para salir;
así que el paseo solo se puede trancar en $v$, y se tranca en algún momento porque las
aristas son finitas. Queda un circuito $C$. Al quitar las aristas de $C$ los grados
siguen pares, y cada componente con aristas tiene, por inducción, su circuito; cada
componente toca a $C$ porque el multigrafo era conexo, y su circuito se empalma en $C$
en un vértice común. $\square$

El algoritmo que sale de la demostración es el de Hierholzer, y con una pila hace el
empalme sin buscarlo: cuando un vértice se queda sin aristas, pasa al circuito.

```{python continue}
def euleriano(n, aristas):
    vecinos = [[] for _ in range(n)]
    for k, (u, v) in enumerate(aristas):
        vecinos[u].append((v, k))
        vecinos[v].append((u, k))
    usada, pila, circuito = [False] * len(aristas), [aristas[0][0]], []
    while pila:
        u = pila[-1]
        while vecinos[u] and usada[vecinos[u][-1][1]]:
            vecinos[u].pop()
        if vecinos[u]:
            v, k = vecinos[u].pop()
            usada[k] = True
            pila.append(v)
        else:
            circuito.append(pila.pop())
    assert len(circuito) == len(aristas) + 1          # usó cada arista una vez
    return circuito[::-1]
```

¿Cuántos vértices de grado impar puede tener el árbol? Un número **par**, porque la
suma de los grados es el doble del número de aristas; el ejercicio 5 pide escribirlo.
Así que los impares se pueden emparejar entre sí, y agregar una arista por pareja sube
en uno el grado de cada impar. Si el emparejamiento es barato, el multigrafo es barato.

## 7. Christofides

El algoritmo, en cuatro pasos:

1. Calcula un árbol generador mínimo $T$.
2. Sea $I$ el conjunto de vértices de grado impar en $T$. Calcula un **emparejamiento
   perfecto de costo mínimo** $M$ sobre $I$, con las distancias como costo.
3. $T + M$ es conexo y con grados pares: toma un circuito euleriano.
4. Aplica atajos al circuito.

El paso 2 se puede hacer en tiempo polinomial con el algoritmo de Jack Edmonds para
emparejamientos de peso mínimo en grafos generales ("Maximum matching and a polyhedron
with 0,1-vertices", *Journal of Research of the National Bureau of Standards* 69B,
1965), que no estudiamos. El código usa una DP sobre subconjuntos de $I$, como
Held-Karp, que cuesta $O(2^{|I|}\,|I|)$: exponencial, y suficiente con $|I| \le 8$. Que
Christofides sea polinomial depende de Edmonds, no de este código.

```{python continue}
def emparejamiento_minimo(d, impares):
    @lru_cache(maxsize=None)
    def mejor(libres):                  # libres: máscara sobre la lista de impares
        if libres == 0:
            return 0.0, ()
        i = (libres & -libres).bit_length() - 1
        opciones = []
        for j in range(i + 1, len(impares)):
            if libres >> j & 1:
                c, M = mejor(libres & ~(1 << i) & ~(1 << j))
                opciones.append((c + d[impares[i]][impares[j]],
                                 M + ((impares[i], impares[j]),)))
        return min(opciones)
    return mejor((1 << len(impares)) - 1)[1]

def atajos(circuito):
    visto, gira = set(), []
    for v in circuito:
        if v not in visto:
            visto.add(v)
            gira.append(v)
    return gira

def christofides_pasos(d):
    n, T = len(d), prim(d)
    grado = [0] * n
    for u, v in T:
        grado[u] += 1
        grado[v] += 1
    impares = [v for v in range(n) if grado[v] % 2 == 1]
    M = emparejamiento_minimo(d, impares)
    return atajos(euleriano(n, T + list(M))), T, impares, M

def christofides(d):
    return christofides_pasos(d)[0]

gira_c, T, impares, M = christofides_pasos(d)
print(f"impares {impares}, emparejamiento {sum(d[u][v] for u, v in M):.3f}, "
      f"Christofides {costo(d, gira_c):.3f}, óptimo {opt:.3f}")
```

```{python continue echo=false output=asis}
print(F22.christofides(P, T, impares, M, gira_c, pie=(
    "Christofides sobre los mismos 9 puntos. A la izquierda, el árbol mínimo, sus "
    "seis vértices de grado impar (con anillo) y el emparejamiento perfecto de costo "
    "mínimo entre ellos. A la derecha, el recorrido que sale del circuito euleriano "
    "de árbol más emparejamiento, después de los atajos.")))
```

En la @fig-tsp-christofides el árbol tiene seis vértices impares, el emparejamiento
cuesta 1,374 y el recorrido 3,488, apenas un 0,5 % sobre el óptimo, contra el 24 % del
doble árbol en la misma entrada.

## 8. La razón 3/2

El costo de Christofides es a lo sumo $w(T) + w(M)$, por el mismo argumento de los
atajos del teorema 3. Ya sabemos que $w(T) \le \mathrm{OPT}$. Falta una cota para el
emparejamiento, y tiene que ser $\mathrm{OPT}/2$.

**Lema 4.** Si $I$ es un conjunto de ciudades de tamaño par y $M$ es un emparejamiento
perfecto de costo mínimo sobre $I$, entonces $w(M) \le \mathrm{OPT}/2$.

*Demostración.* Sea $R$ un recorrido óptimo de todas las ciudades. Recórrelo saltando
las ciudades que no están en $I$: queda un ciclo $R_I$ que visita las ciudades de $I$
en el orden de $R$, y por la desigualdad triangular, como en el teorema 3,
$w(R_I) \le w(R) = \mathrm{OPT}$. Numera las ciudades de $I$ en ese orden,
$u_1, \dots, u_{2m}$. Los tramos de $R_I$ se parten en dos emparejamientos perfectos de
$I$: los impares, $\{u_1 u_2, u_3 u_4, \dots, u_{2m-1} u_{2m}\}$, y los pares,
$\{u_2 u_3, \dots, u_{2m} u_1\}$. Sus costos suman $w(R_I)$, así que uno de los dos
cuesta a lo sumo $w(R_I)/2 \le \mathrm{OPT}/2$, y $M$, que es el mínimo, cuesta a lo
sumo eso. $\square$

El lema usa dos hipótesis: la desigualdad triangular, para atajar $R$ hasta $R_I$, y
que $M$ sea **mínimo**. Con un emparejamiento cualquiera no dice nada.

**Teorema 5** (Christofides, 1976). Con distancias métricas, Christofides devuelve un
recorrido de costo a lo sumo $\tfrac32\,\mathrm{OPT}$, en tiempo polinomial.

*Demostración.* $T + M$ tiene grados pares: un vértice par de $T$ no está en $I$ y
conserva su grado, y uno impar recibe exactamente una arista de $M$. Es conexo porque
contiene a $T$. Por Euler tiene un circuito que usa cada arista una vez y cuesta
$w(T) + w(M)$. Ese circuito pasa por todas las ciudades, y los atajos, por la
desigualdad triangular como en el teorema 3, no lo alargan. Con el lema 2 y el lema 4,
el costo es a lo sumo $\mathrm{OPT} + \mathrm{OPT}/2$. El tiempo es el de Prim, el del
emparejamiento de Edmonds, y $O(n)$ para el circuito y los atajos. $\square$

Nicos Christofides lo publicó como "Worst-case analysis of a new heuristic for the
travelling salesman problem" (Management Science Research Report 388, Carnegie-Mellon
University, 1976). Anatoliy Serdyukov llegó al mismo algoritmo por su lado, en un
artículo en ruso de 1978 (*Upravlyaemye sistemy* 17, pp. 76–79), y por eso hoy se le
llama también Christofides-Serdyukov; la historia la cuentan René van Bevern y Viktoriia
Slugina en *Historia Mathematica* 53 (2020), pp. 118–127.

Ahora la misma batería de §5, y dentro de ella la cota del lema 4, que es la parte
nueva de la demostración:

```{python continue}
def emparejamientos(I):                     # el oráculo: todos los perfectos
    if not I:
        yield ()
        return
    for j in range(1, len(I)):
        for resto in emparejamientos(I[1:j] + I[j + 1:]):
            yield ((I[0], I[j]),) + resto

r_chr = bateria(christofides)
peor_M, iguales = 0, 0
rng = random.Random(7)
for _ in range(150):
    Q = [(rng.random(), rng.random()) for _ in range(rng.randint(5, 9))]
    dq = distancias(Q)
    _, _, I, MQ = christofides_pasos(dq)
    wM = sum(dq[u][v] for u, v in MQ)
    fuerza = min(sum(dq[u][v] for u, v in m) for m in emparejamientos(I))
    iguales += abs(wM - fuerza) < 1e-12
    peor_M = max(peor_M, wM / held_karp(dq))
print(f"Christofides: peor {max(r_chr):.3f}, promedio {sum(r_chr) / len(r_chr):.3f}")
print(f"la DP del emparejamiento coincide con la enumeración en {iguales} de 150")
print(f"emparejamiento / óptimo: el mayor fue {peor_M:.3f} (el lema dice ≤ 0,5)")
```

Christofides no pasa de 1,185 en las mismas entradas en las que el doble árbol llegó a
1,412, y su promedio es 1,038. La DP del emparejamiento coincide con la enumeración
de todos los emparejamientos perfectos en las 150 entradas. El emparejamiento llega a 0,498 del óptimo: la cota del
lema 4 se cumple casi con igualdad, así que la comprobación habría fallado con un
emparejamiento apenas peor que el mínimo.

## 9. La razón 3/2 se alcanza

La batería no pasa de 1,185. ¿Es $3/2$ un defecto de la demostración, y el algoritmo es
mejor? No. Pon $k + 1$ puntos en la recta, $(0, 0), (1, 0), \dots, (k, 0)$, y $k$ más
a altura $h = 0{,}85$, en $(i + \tfrac12, h)$. Cada punto de arriba está a distancia
$\delta = \sqrt{0{,}25 + h^2} \approx 0{,}986$ de los dos de abajo más cercanos, y
todas las demás distancias son al menos 1. El árbol mínimo es entonces el zigzag que
alterna abajo y arriba: tiene $2k$ aristas de largo $\delta$, y ningún árbol puede
tener aristas más cortas. El zigzag es un camino, así que sus únicos impares son los
dos extremos, $(0, 0)$ y $(k, 0)$, a distancia $k$. Christofides tiene que cruzar la
tira entera para emparejarlos.

Para comparar no hace falta el óptimo: basta un recorrido conocido, porque cualquier
recorrido cuesta al menos el óptimo y la razón contra él es una **cota inferior** de la
razón real. Usamos el borde de la tira: la fila de abajo, el último punto de arriba,
la fila de arriba hacia atrás y vuelta al inicio.

```{python continue}
def tira(k, h=0.85):
    return [(i, 0.0) for i in range(k + 1)] + [(i + 0.5, h) for i in range(k)]

for k in (3, 5, 20, 100):
    Q = tira(k)
    dq = distancias(Q)
    borde = list(range(k + 1)) + list(range(2 * k, k, -1))
    c, b = costo(dq, christofides(dq)), costo(dq, borde)
    exacto = f", Held-Karp {held_karp(dq):.3f}" if len(Q) <= 11 else ""
    print(f"k = {k:3d}: Christofides {c:7.3f}, borde {b:7.3f}{exacto}, "
          f"razón ≥ {c / b:.3f}")
delta = math.hypot(0.5, 0.85)
print(f"δ = {delta:.3f}, límite (2δ + 1)/2 = {(2 * delta + 1) / 2:.3f}, "
      f"123/122 = {123 / 122:.3f}")
```

Christofides paga $2k\delta + k$ y el borde cuesta $2k - 1 + 2\delta$, así que la razón
tiende a $(2\delta + 1)/2 \approx 1{,}486$ cuando $k$ crece: con $k = 100$ ya va por
1,479. Y $\delta$ se puede acercar a 1 tanto como se quiera subiendo $h$ hacia
$\sqrt3/2$, sin que el zigzag deje de ser el único árbol mínimo. Para $k = 3$ y $k = 5$, Held-Karp
confirma que el borde es óptimo.

¿Y la del problema? Durante 45 años nadie mejoró $3/2$ para el TSP métrico. Anna
Karlin, Nathan Klein y Shayan Oveis Gharan lo lograron en "A (slightly) improved
approximation algorithm for metric TSP" (STOC 2021, pp. 32–45), con un algoritmo
aleatorizado de razón $3/2 - \varepsilon$ para algún $\varepsilon > 10^{-36}$. Del otro
lado, Marek Karpinski, Michael Lampis y Richard Schmied demostraron en "New
inapproximability bounds for TSP" (*Journal of Computer and System Sciences* 81(8),
2015, pp. 1665–1677) que aproximar con razón menor que $123/122$ es NP-duro.

Después el margen creció un poco. Leonid Gurvits, Nathan Klein y Jonathan Leake
afinaron el análisis del mismo algoritmo hasta $3/2 - 2{,}18 \cdot 10^{-34}$ ("From trees
to polynomials and back again: new capacity bounds with applications to TSP", ICALP
2024, LIPIcs 297, artículo 79), y Karlin, Klein y Oveis Gharan lo hicieron determinista
("A deterministic better-than-3/2 approximation algorithm for metric TSP", IPCO 2023,
LNCS, pp. 261–274). Del lado de la dificultad, 123/122 sigue siendo la mejor cota
publicada que encontramos al escribir este capítulo, en noviembre de 2026. Entre 1,008
y 1,5 está lo que no se sabe.

## 10. Vertex cover con pesos

Cada vértice $v$ tiene un peso $w_v > 0$, y se quiere un vertex
cover de peso mínimo. El algoritmo del capítulo 21, §3 mete los dos extremos de cada
arista descubierta, y con pesos eso es un desastre: en una estrella con el centro de
peso 1 y las hojas de peso 100, la primera arista mete el centro y una hoja.

```{python echo=false}
# Cadena nueva: los bloques de vertex cover no re-ejecutan los del viajante.
import itertools
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))
import figuras_22 as F22
```

```{python continue}
def cubrimiento_emparejamiento(aristas):              # capítulo 21, §3
    C = set()
    for u, v in aristas:
        if u not in C and v not in C:
            C |= {u, v}
    return C

estrella = [(0, v) for v in range(1, 6)]
w = [1] + [100] * 5
C = cubrimiento_emparejamiento(estrella)
print(f"cubrimiento {sorted(C)}, peso {sum(w[v] for v in C)}; el centro solo pesa {w[0]}")
```

Paga 101 donde basta 1: el tamaño de un emparejamiento, la cota del capítulo 21,
cuenta vértices y no pesos.

Escribe el problema como un programa con una variable $x_v$ por vértice, que vale 1 si
$v$ está en el cubrimiento y 0 si no:
$$\min \sum_{v} w_v x_v \quad\text{sujeto a}\quad x_u + x_v \ge 1 \text{ para cada }
\{u, v\} \in E, \qquad x_v \in \{0, 1\}.$$
Es un **programa lineal entero**, tan difícil como vertex cover. La **relajación lineal** cambia $x_v \in \{0, 1\}$ por $0 \le x_v \le 1$: el
objetivo y las restricciones son lineales, y las variables, reales. Llamemos
$\mathrm{LP}$ a su óptimo.

**Lema 6.** $\mathrm{LP} \le \mathrm{OPT}$.

*Demostración.* El vector característico de un cubrimiento óptimo cumple
$0 \le x_v \le 1$ y todas las restricciones, así que es una solución factible de la
relajación, con valor $\mathrm{OPT}$. El mínimo de la relajación no puede ser mayor.
$\square$

Las soluciones factibles forman un **poliedro** dentro del cubo $[0, 1]^n$, y un
resultado básico de la programación lineal dice que, si el óptimo existe, se alcanza
en un vértice del poliedro: un punto donde $n$ restricciones linealmente independientes
se cumplen con igualdad. Con un grafo chico podemos encontrar todos los vértices así:
elegir $n$ restricciones, resolver el sistema y quedarse con las soluciones que
cumplen todas las demás.

```{python continue}
def resolver(A, r):                         # Gauss con fracciones; None si es singular
    n = len(A)
    M = [list(fila) + [ri] for fila, ri in zip(A, r)]
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return tuple(M[i][-1] / M[i][i] for i in range(n))

def restricciones(n, aristas):              # cada una es (a, r), con a·x >= r
    e = lambda S: tuple(Fraction(int(k in S)) for k in range(n))
    return ([(e(set(a)), 1) for a in aristas] + [(e({v}), 0) for v in range(n)]
            + [(tuple(-x for x in e({v})), -1) for v in range(n)])

def vertices(n, aristas):
    R = restricciones(n, aristas)
    V = set()
    for S in itertools.combinations(R, n):
        x = resolver([a for a, _ in S], [r for _, r in S])
        if x and all(sum(ai * xi for ai, xi in zip(a, x)) >= r for a, r in R):
            V.add(x)
    return sorted(V)

triangulo = [(0, 1), (1, 2), (0, 2)]
V3 = vertices(3, triangulo)
print(len(V3), "vértices:", [tuple(str(v) for v in x) for x in V3])
```

```{python continue echo=false output=asis}
print(F22.poliedro(V3, restricciones(3, triangulo), pie=(
    "El poliedro de la relajación de vertex cover en un triángulo, dentro del cubo "
    "unitario (en gris). Sus cinco vértices salieron de la enumeración: cuatro "
    "enteros, que son los cubrimientos de 2 y 3 vértices, y uno fraccionario, "
    "(½, ½, ½), que es el óptimo de la relajación con pesos iguales.")))
```

La @fig-tsp-poliedro muestra el caso más chico que ya tiene un vértice fraccionario.
Con pesos 1, el vértice $(\tfrac12, \tfrac12, \tfrac12)$ vale $3/2$ y cada cubrimiento
vale al menos 2: la relajación queda estrictamente por debajo del óptimo entero. La
distancia entre los dos es el precio de relajar, y el ejercicio 7 la mide en $K_n$.

## 11. Resolver el programa lineal

La relajación sirve como cota porque se puede calcular en tiempo polinomial. Leonid
Khachiyan lo demostró para todo programa lineal con el método del elipsoide
("Polynomial algorithms in linear programming", *USSR Computational Mathematics and
Mathematical Physics* 20(1), 1980, pp. 53–72). En la práctica se usa el **simplex**, que va
de vértice en vértice del poliedro mejorando el objetivo. Cómo funciona no es tema de
este libro: lo usamos como el `sorted` de Python, comprobado contra la enumeración de
vértices.

El simplex más simple arranca en el origen, que no es factible para vertex cover. El
cambio $z_v = 1 - x_v$ lo arregla: las restricciones pasan a $z_u + z_v \le 1$ y $0 \le z_v \le 1$, el origen las cumple,
y minimizar $\sum w_v x_v$ es maximizar $\sum w_v z_v$. Es la relajación de **conjunto
independiente** (capítulo 16, §10).

```{python continue}
def simplex(A, b, c):
    """max c·z con A z <= b, z >= 0 y b >= 0, en fracciones exactas (regla de Bland)."""
    m, n = len(A), len(c)
    T = [[Fraction(x) for x in A[i]] + [Fraction(int(i == k)) for k in range(m)]
         + [Fraction(b[i])] for i in range(m)]
    obj = [Fraction(-x) for x in c] + [Fraction(0)] * (m + 1)
    base = list(range(n, n + m))
    while (e := next((j for j in range(n + m) if obj[j] < 0), None)) is not None:
        r = min((i for i in range(m) if T[i][e] > 0),
                key=lambda i: (T[i][-1] / T[i][e], base[i]))
        T[r] = [x / T[r][e] for x in T[r]]
        for i in range(m):
            if i != r and T[i][e] != 0:
                T[i] = [a - T[i][e] * b for a, b in zip(T[i], T[r])]
        obj = [a - obj[e] * b for a, b in zip(obj, T[r])]
        base[r] = e
    z = [Fraction(0)] * n
    for i, v in enumerate(base):
        if v < n:
            z[v] = T[i][-1]
    return obj[-1], z

def relajacion(n, aristas, w):
    A = ([[int(k in a) for k in range(n)] for a in aristas]
         + [[int(k == v) for k in range(n)] for v in range(n)])
    valor, z = simplex(A, [1] * (len(aristas) + n), w)
    return sum(w) - valor, [1 - zi for zi in z]

def grafo_al_azar(n, p, rng):
    return [a for a in itertools.combinations(range(n), 2) if rng.random() < p]

rng, distintos, probados = random.Random(22), 0, 0
for _ in range(120):
    n = rng.randint(2, 5)
    aristas = grafo_al_azar(n, 0.5, rng)
    if aristas:
        w = [rng.randint(1, 9) for _ in range(n)]
        lp, x = relajacion(n, aristas, w)
        oraculo = min(sum(wi * xi for wi, xi in zip(w, v)) for v in vertices(n, aristas))
        distintos += lp != oraculo
        probados += 1
print(f"{probados} grafos, el simplex difiere de la enumeración en {distintos}")
```

En ninguno de los 92 grafos de hasta 5 vértices difieren.

## 12. Redondear

Tenemos un $x$ fraccionario con $\sum w_v x_v = \mathrm{LP} \le \mathrm{OPT}$. Hay que
convertirlo en un cubrimiento sin pagar mucho más. La restricción de una arista dice
$x_u + x_v \ge 1$, así que uno de los dos extremos vale al menos $1/2$. Eso sugiere la
regla: toma $v$ si $x_v \ge 1/2$.

**Teorema 7** (Hochbaum, 1982). El conjunto $C = \{v : x_v \ge 1/2\}$, con $x$ un
óptimo de la relajación, es un vertex cover de peso a lo sumo $2\,\mathrm{OPT}$.

*Demostración.* Es un cubrimiento: si $\{u, v\} \in E$, $x_u + x_v \ge 1$, y si los dos
fueran menores que $1/2$ la suma sería menor que 1. Para el peso, cada $v \in C$ cumple
$1 \le 2x_v$, así que
$$w(C) = \sum_{v \in C} w_v \le \sum_{v \in C} 2 w_v x_v \le 2 \sum_v w_v x_v
= 2\,\mathrm{LP} \le 2\,\mathrm{OPT},$$
donde la segunda desigualdad agrega los términos de los $v \notin C$, que son no
negativos, y la última es el lema 6. El tiempo es el de resolver la relajación, que es
polinomial. $\square$

El paso que se salta es "al menos": la regla tiene que tomar $x_v = 1/2$, porque la
suma de los dos extremos puede ser exactamente 1 con los dos en $1/2$. La sección
siguiente muestra qué pasa si no. Dorit Hochbaum publicó este redondeo para set cover
con pesos en "Approximation algorithms for the set covering and vertex cover problems"
(*SIAM Journal on Computing* 11(3), 1982, pp. 555–556), y el ejercicio 8 lo pide en esa
generalidad. Ahora contra la fuerza bruta:

```{python continue}
def redondeo(n, aristas, w):
    lp, x = relajacion(n, aristas, w)
    return {v for v in range(n) if x[v] >= Fraction(1, 2)}, lp, x

def optimo(n, aristas, w):
    return min(sum(w[v] for v in S) for k in range(n + 1)
               for S in itertools.combinations(range(n), k)
               if all(u in S or v in S for u, v in aristas))

def es_cubrimiento(C, aristas):
    return all(u in C or v in C for u, v in aristas)

rng, casos = random.Random(22), []
for _ in range(500):
    n = rng.randint(3, 8)
    aristas = grafo_al_azar(n, rng.choice([0.2, 0.3, 0.5]), rng)
    if aristas:
        casos.append((n, aristas, [rng.randint(1, 20) for _ in range(n)]))

peor, valores, hueco = 0, set(), 0
for n, aristas, w in casos:
    C, lp, x = redondeo(n, aristas, w)
    opt = optimo(n, aristas, w)
    assert es_cubrimiento(C, aristas) and lp <= opt
    peor = max(peor, Fraction(sum(w[v] for v in C), opt))
    hueco = max(hueco, opt / lp)
    valores |= set(x)
print(f"{len(casos)} grafos, peor razón {float(peor):.3f}, "
      f"mayor OPT/LP {float(hueco):.3f}, valores de x: {sorted(str(v) for v in valores)}")
pesos = [16, 4, 20]
print(f"triángulo con pesos {pesos}: (1/2, 1/2, 1/2) vale {sum(pesos) / 2:g}, "
      f"óptimo {optimo(3, triangulo, pesos)}, redondear ese punto paga {sum(pesos)}")
```

La razón 2 se alcanza en algún grafo de la batería, así que el teorema 7 no tiene
holgura que ganar con otra demostración. Un ejemplo de cómo pasa: en un triángulo con
pesos 16, 4 y 20, el punto $(\tfrac12, \tfrac12, \tfrac12)$ vale 20, igual que el
cubrimiento óptimo $\{16, 4\}$; si el simplex devuelve ese punto, el redondeo toma los
tres vértices y paga 40.

El simplex solo devolvió 0, $1/2$ y 1, y no es suerte: los vértices de este poliedro
tienen siempre coordenadas en $\{0, 1/2, 1\}$ (George Nemhauser y Leslie Trotter, "Vertex packings: Structural
properties and algorithms", *Mathematical Programming* 8, 1975, pp. 232–248). El
ejercicio 6 lo pide.

## 13. El error plantado: redondear con `round`

La regla de §12 dice "redondea". Python tiene una función para eso, y la variante que
uno escribe sin pensar es esta:

```{python continue}
def redondeo_round(n, aristas, w):
    lp, x = relajacion(n, aristas, w)
    return {v for v in range(n) if round(x[v]) == 1}

pasa_razon = no_cubre = 0
for n, aristas, w in casos:
    C = redondeo_round(n, aristas, w)
    pasa_razon += sum(w[v] for v in C) <= 2 * optimo(n, aristas, w)
    no_cubre += not es_cubrimiento(C, aristas)
print(f"razón ≤ 2 en {pasa_razon} de {len(casos)}; no es cubrimiento en {no_cubre}")
print("round(1/2) =", round(Fraction(1, 2)), " round(0.5) =", round(0.5),
      " round(1.5) =", round(1.5))
```

Una batería que mide la razón la aprueba en las 456 entradas. No es una batería
exigente: `redondeo_round` toma un subconjunto de lo que toma el redondeo correcto, así
que su peso nunca puede pasar de 2·OPT. Es una comprobación que no puede fallar, y por
eso no dice nada. La batería que verifica que la salida sea un cubrimiento la atrapa en
74 entradas.

La causa: `round` redondea los empates al **par** más cercano, así que $1/2$ va a 0 y
$3/2$ va a 2. Y por Nemhauser y Trotter, los valores fraccionarios del óptimo son
justo $1/2$, el único valor ambiguo. En el triángulo con pesos iguales el óptimo de la relajación es
$(\tfrac12, \tfrac12, \tfrac12)$, y `redondeo_round` devuelve el conjunto vacío.

La demostración del teorema 7 lo anunciaba en su primera línea. De $x_u + x_v \ge 1$
sale que uno de los dos vale **al menos** $1/2$, no estrictamente más de $1/2$. `round` deja fuera justo las aristas con los dos extremos en $1/2$.

## 14. La regla

Una aproximación se diseña eligiendo la cota, y la cota decide la razón. Las tres de
este capítulo:

| Problema | Cota del óptimo | Algoritmo | Razón | Se alcanza |
|---|---|---|---|---|
| TSP métrico | árbol mínimo | doble árbol | 2 | ejercicio 3 |
| TSP métrico | árbol + OPT/2 (lema 4) | Christofides | 3/2 | la tira de §9 |
| Vertex cover con pesos | relajación lineal | redondeo en 1/2 | 2 | la batería de §12 |
| TSP general | ninguna sirve | — | ninguna constante | teorema 1 |

La relajación lineal es la cota más general de las que ha visto el libro: no hay que
encontrar una estructura como el emparejamiento o el árbol, basta escribir el problema
como programa entero. Lo difícil pasa a ser redondear sin perder mucho, y el ejercicio 7
mide cuánto se puede perder. El capítulo 23 cambia de pregunta:
una familia de algoritmos que se acerca al óptimo tanto como se quiera, pagando en
tiempo.

## Resumen {#tsp-lp-resumen}

- Sin desigualdad triangular, el TSP no admite ninguna razón constante si P ≠ NP: con
  peso $(\alpha - 1)n + 2$ en las no-aristas, una $\alpha$-aproximación decidiría ciclo
  hamiltoniano.
- Quitar un tramo de un recorrido deja un árbol generador, así que el árbol mínimo
  acota el óptimo por debajo.
- El doble árbol visita las ciudades en preorden. Los atajos no alargan por la
  desigualdad triangular, y la razón es 2.
- Un multigrafo conexo con grados pares tiene circuito euleriano; un árbol tiene un
  número par de vértices impares.
- Christofides agrega al árbol un emparejamiento perfecto mínimo de sus impares. El
  emparejamiento cuesta a lo sumo OPT/2, porque el óptimo atajado a los impares se
  parte en dos emparejamientos. La razón es 3/2, y se alcanza en el límite.
- Para el TSP métrico ya se sabe garantizar un poco menos de 3/2, por un $\varepsilon$ del
  orden de $10^{-34}$, y con un algoritmo determinista; por debajo de $123/122$ es
  NP-duro.
- Vertex cover con pesos: la relajación lineal es una cota que se calcula en tiempo
  polinomial, y tomar los $x_v \ge 1/2$ da razón 2.
- `round` de Python lleva $1/2$ a 0, y los óptimos de esta relajación viven en
  $\{0, 1/2, 1\}$: redondear con `round` no devuelve un cubrimiento. Una batería que
  solo mide la razón no lo ve.

## Ejercicios {#tsp-lp-ejercicios}

1. Sean las seis ciudades $a = (0, 5)$, $b = (2, 0)$, $c = (4, 0)$, $d = (4, 3)$,
   $e = (7, 6)$ y $f = (8, 4)$ del plano, con la distancia euclídea (todas las
   distancias son distintas). Ejecuta Prim a mano desde $a$, y después el doble árbol
   con raíz $a$, visitando los hijos de cada vértice por orden alfabético. Da el
   recorrido y su costo, y compáralo con el doble del peso del árbol.

2. Demuestra con cuidado que los atajos no alargan: si $W = w_0, w_1, \dots, w_m$ es un
   paseo cerrado que pasa por todas las ciudades y $R$ es la lista de sus primeras
   apariciones, entonces $\mathrm{costo}(R) \le \mathrm{costo}(W)$ cuando la distancia
   es métrica. Señala exactamente dónde entra la desigualdad triangular y da un ejemplo
   de cuatro ciudades sin ella donde los atajos alargan.

3. Construye una familia de entradas métricas, una para cada $n$, en las que el doble
   árbol, para algún árbol mínimo y algún orden de visita de los hijos, devuelve un
   recorrido cuya razón contra el óptimo tiende a 2. Demuestra cuánto vale el óptimo.
   (Pista: el capítulo 19, §7 ya tenía una métrica con distancias 1 y 2.)

4. Ejecuta Christofides a mano sobre las seis ciudades del ejercicio 1: el árbol, sus
   vértices de grado impar, los costos de los emparejamientos perfectos posibles entre
   ellos, el circuito euleriano de árbol más emparejamiento que da Hierholzer desde
   $a$ tomando los vecinos por orden alfabético, y el recorrido después de los atajos.
   Compara su costo con el del ejercicio 1. Después busca otro circuito euleriano del
   mismo multigrafo que, con atajos, dé un recorrido distinto, y compara los dos.

5. Demuestra que en todo grafo (o multigrafo) finito el número de vértices de grado
   impar es par. ¿Dónde usa esto el algoritmo de Christofides, y qué fallaría en el
   paso 2 si no fuera cierto?

6. ★ Sea $x$ una solución factible de la relajación de vertex cover que **no** tiene
   todas sus coordenadas en $\{0, 1/2, 1\}$. Construye dos soluciones factibles
   $x^+ \ne x^-$ con $x = (x^+ + x^-)/2$, moviendo en $+\varepsilon$ las coordenadas
   que están en $(0, 1/2)$ y en $-\varepsilon$ las que están en $(1/2, 1)$, y al revés.
   Deduce que todo vértice del poliedro tiene coordenadas en $\{0, 1/2, 1\}$, y que la
   relajación tiene un óptimo con esos valores.

7. En el grafo completo $K_n$ con todos los pesos iguales a 1, calcula el óptimo de la
   relajación de vertex cover y demuestra que lo es, y calcula el cubrimiento mínimo.
   ¿Qué dice el cociente entre los dos sobre cualquier algoritmo cuya razón se
   demuestre comparando contra $\mathrm{LP}$, como el teorema 7?

8. En set cover con pesos (capítulo 21, §10), sea $f$ el mayor número de conjuntos que
   contienen a un mismo elemento. Escribe el programa entero y su relajación, y
   demuestra que tomar los conjuntos con $x_S \ge 1/f$ da un cubrimiento de costo a lo
   sumo $f \cdot \mathrm{OPT}$. ¿Qué algoritmo del capítulo es el caso $f = 2$?
   Modela con esto elegir cámaras de seguridad, cada una con su precio, que vigilen
   todos los pasillos de un edificio, si cada pasillo lo ven a lo sumo tres cámaras.

9. Implementa el doble árbol y Christofides y mide su razón real contra `held_karp` en
   puntos al azar del cuadrado unidad, para $n$ de 6 a 13, con al menos 50 entradas
   por tamaño. Grafica la peor razón y la promedio de cada algoritmo contra $n$.
   ¿Crece la diferencia entre los dos con $n$?

10. En el TSP **asimétrico** las distancias cumplen la desigualdad triangular pero
    $d(u, v)$ puede ser distinta de $d(v, u)$. Recorre la demostración del teorema 5
    paso a paso y di cuáles dejan de valer: el lema 2, los atajos, el lema 4 y el
    circuito euleriano. Para cada uno, da una entrada chica que lo muestre o explica
    por qué sigue valiendo.
