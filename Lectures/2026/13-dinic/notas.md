# Flujo máximo: Dinic {#chap-dinic}

¿Cuánto se puede mandar de un punto a otro de una red cuando cada conexión tiene un
tope? El primer algoritmo que uno escribe se atasca porque no puede deshacer lo que
mandó. Con la red residual, que sí puede, Ford-Fulkerson es correcto, y su demostración
da el teorema del flujo máximo y el corte mínimo. Dinic trabaja por fases, y su cota
$O(V^2 E)$ sale de un invariante: la distancia de la fuente al sumidero sube en cada
fase. El error plantado rompe ese invariante sin cambiar ni una respuesta.

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
from collections import deque

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_13.py
sys.setrecursionlimit(10000)
import figuras as F
import figuras_13 as G

INF = float("inf")
POS = {0: (0, 50), 1: (90, 0), 2: (90, 100), 3: (190, 100), 4: (190, 0), 5: (280, 50)}
```

## 1. Redes y flujos

Una **red** es un grafo dirigido $G = (V, E)$ con una capacidad entera $c(u, v) \ge 0$ en
cada arista y dos vértices distinguidos, la **fuente** $s$ y el **sumidero** $t$. Un
**flujo** es una función $f$ sobre las aristas que cumple dos condiciones:

- **capacidad**: $0 \le f(u, v) \le c(u, v)$ en cada arista;
- **conservación**: en cada vértice distinto de $s$ y $t$, lo que entra es igual a lo
  que sale.

El **valor** $|f|$ es lo que sale de $s$ menos lo que entra en $s$. El problema del flujo
máximo pide un flujo de valor máximo: tuberías con caudal tope, o enlaces con ancho de
banda, donde nada se acumula en los nodos intermedios.

El capítulo 10, §10, vio el emparejamiento bipartito como intersección de dos matroides,
donde el goloso garantiza solo la mitad. La §12 lo resuelve exacto como flujo.

El ejemplo tiene seis vértices y ocho aristas. Salió de una búsqueda al azar que pedía
que el goloso de la §2 se atasque, que Dinic haga tres fases, que una de ellas deshaga
flujo y que el corte mínimo no sea el de alrededor de $s$ o de $t$.

```{python continue}
NOMBRES = "sabcdt"
s, a, b, c, d, t = range(6)
EJEMPLO = [(s, a, 3), (s, b, 9), (b, a, 2), (a, c, 3),
           (a, d, 9), (b, c, 9), (c, t, 4), (d, t, 7)]

def es_flujo(n, aristas, f, s, t):
    """Comprueba capacidad y conservación, y devuelve el valor."""
    neto = [0] * n
    for (u, v, cap), x in zip(aristas, f):
        assert 0 <= x <= cap, (u, v)
        neto[u] -= x
        neto[v] += x
    assert all(neto[v] == 0 for v in range(n) if v not in (s, t))
    return -neto[s]
```

## 2. El goloso que se atasca

La primera idea: buscar un camino de $s$ a $t$ con capacidad sobrante en todas sus
aristas, mandar por él el mínimo de los sobrantes y repetir. La búsqueda es en anchura,
así que cada camino es uno de los más cortos.

En el código, la arista $i$ ocupa la posición $2i$, con `cap` igual a lo que le sobra, y
su gemela $(v, u)$ la posición $2i + 1$, que empieza en 0. La gemela de `e` es `e ^ 1`.
Por ahora el goloso ignora las gemelas (`inversas=False`); la §3 dice para qué sirven.

```{python continue}
def red(n, aristas):
    ady = [[] for _ in range(n)]
    hacia, cap = [], []
    for u, v, c in aristas:
        ady[u].append(len(hacia)); hacia.append(v); cap.append(c)
        ady[v].append(len(hacia)); hacia.append(u); cap.append(0)
    return ady, hacia, cap

def camino_bfs(ady, hacia, cap, s, t, inversas=True):
    previa = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for e in ady[u]:
            if e % 2 == 1 and not inversas:
                continue
            if cap[e] > 0 and hacia[e] not in previa:
                previa[hacia[e]] = e
                cola.append(hacia[e])
    if t not in previa:
        return None
    camino, v = [], t
    while v != s:
        camino.append(previa[v])
        v = hacia[previa[v] ^ 1]
    return camino[::-1]

def ford_fulkerson(n, aristas, s, t, inversas=True):
    R = red(n, aristas)
    ady, hacia, cap = R
    total, aumentos = 0, []
    while (camino := camino_bfs(ady, hacia, cap, s, t, inversas)) is not None:
        x = min(cap[e] for e in camino)
        for e in camino:
            cap[e] -= x
            cap[e ^ 1] += x
        total += x
        aumentos.append(([hacia[e ^ 1] for e in camino] + [t], x))
    return total, aumentos, R

def nombres(aumentos):
    return [("".join(NOMBRES[v] for v in cam), x) for cam, x in aumentos]

def flujo_de(aristas, cap):
    return [cap[2 * i + 1] for i in range(len(aristas))]   # lo que tiene la gemela

v0, aum0, R0 = ford_fulkerson(6, EJEMPLO, s, t, inversas=False)
print("goloso:", nombres(aum0), "valor", v0)
F9 = [3, 6, 2, 0, 5, 4, 4, 5]
print("otro flujo, valor", es_flujo(6, EJEMPLO, F9, s, t))
```

El goloso manda 3 por $s\,a\,c\,t$, 1 por $s\,b\,c\,t$ y 2 por $s\,b\,a\,d\,t$, y se queda en 6.
El flujo `F9` vale 9 y la comprobación lo acepta, así que 6 no es el máximo. (De dónde
sale `F9` lo vemos en la §4.)

Ningún camino estuvo mal elegido en su momento: $s\,a\,c\,t$ es uno de los más cortos.
Pero sus 3 unidades ocupan $c{\to}t$, la única salida de $c$, y $a$ tenía otra salida
libre, $a{\to}d$. Si esas 3 fueran por $d$, $c{\to}t$ quedaría para lo que viene de $b$.
`F9` no manda nada por $a{\to}c$, y el goloso no puede retirar lo que ya puso ahí. Un
algoritmo de caminos tiene que poder deshacer.

## 3. La red residual

Dado un flujo $f$, la **red residual** $G_f$ tiene, por cada arista $(u, v)$ de $G$, hasta
dos aristas:

- $(u, v)$ con capacidad residual $c(u, v) - f(u, v)$, lo que todavía cabe;
- $(v, u)$ con capacidad residual $f(u, v)$, lo que se puede devolver.

Se queda solo con las de capacidad positiva. Mandar $x$ por la inversa $(v, u)$ es bajar
$f(u, v)$ en $x$. Un **camino de aumento** es un camino de $s$ a $t$ en $G_f$.

La representación del código ya es la residual: `cap[e]` es la capacidad residual de
`e`, y empujar `x` por `e` resta en `e` y suma en `e ^ 1`, también en el goloso, que solo
no mira las gemelas. El flujo de la arista $i$ es lo que tiene su gemela.

```{python continue}
ady, hacia, cap0 = R0
camino = camino_bfs(ady, hacia, cap0, s, t, inversas=True)
print("camino en la residual del goloso:",
      " ".join(NOMBRES[hacia[e ^ 1]] for e in camino) + " t",
      "| inversas usadas:", [e for e in camino if e % 2 == 1],
      "| sobrante:", min(cap0[e] for e in camino))
```

```{python continue echo=false output=asis}
res0 = [(hacia[e ^ 1], hacia[e], cap0[e]) for e in range(len(cap0)) if cap0[e] > 0]
en_camino = {(hacia[e ^ 1], hacia[e]) for e in camino}
print(G.red_y_residual(POS, NOMBRES, EJEMPLO, flujo_de(EJEMPLO, cap0), res0, en_camino,
      ident="dinic-residual",
      pie="Izquierda: el flujo de valor 6 del goloso (naranja, saturadas). Derecha: su "
          "red residual; inversas en azul y, en rojo, el camino s b c a d t."))
```

En la red residual de la @fig-dinic-residual hay un camino que el goloso no veía:
$s \to b \to c \to a \to d \to t$, con sobrante 3. El paso $c \to a$ es la posición 7, la
gemela de $a{\to}c$. Mandar 3 por él retira las 3 unidades de $a{\to}c$: lo que llegaba a
$c$ desde $a$ ahora llega desde $b$, y lo que salía de $a$ hacia $c$ ahora sale hacia
$d$.

## 4. Ford-Fulkerson

El **método de Ford y Fulkerson** es el goloso sobre la residual: aumentar mientras haya
camino de aumento. Es el código de antes con `inversas=True`.

```{python continue}
v1, aum1, R1 = ford_fulkerson(6, EJEMPLO, s, t)
print("Ford-Fulkerson:", nombres(aum1), "valor", v1)
F1 = flujo_de(EJEMPLO, R1[2])
print("flujo final:", F1, "== F9:", F1 == F9)
```

Los tres primeros aumentos son los del goloso, el cuarto es el de la figura, y el
flujo final es `F9`.

**Termina.** Con capacidades enteras, las residuales son enteras siempre: empiezan
enteras y cada aumento suma y resta el mínimo de varias. Cada aumento sube el valor en
al menos 1. El valor nunca pasa de
$C_s$, la suma de las capacidades de las aristas que salen de $s$, así que hay a lo sumo
$C_s$ aumentos. De paso queda demostrada la **integralidad**: el flujo final es entero en
cada arista. La §12 la necesita.

**Lo que no sabemos todavía** es si parar sin camino de aumento quiere decir haber
llegado al máximo. Tampoco tenemos una buena cota de tiempo: $C_s$ depende de los
números de la entrada y no de su tamaño, y el ejercicio 3 da una red de cuatro vértices
donde una mala elección de caminos llega a esa cota.

## 5. Cortes

Un **corte** $(S, T)$ es una partición de $V$ con $s \in S$ y $t \in T$. Su **capacidad**
es la suma de las capacidades de las aristas que van de $S$ a $T$:
$$c(S, T) = \sum_{u \in S,\ v \in T} c(u, v).$$
Las aristas de $T$ a $S$ no cuentan. Escribimos $f(S, T)$ para el flujo total de $S$ a
$T$ y $f(T, S)$ para el de vuelta.

**Lema 1.** Para todo flujo $f$ y todo corte $(S, T)$, $|f| = f(S, T) - f(T, S)$.

*Demostración.* Para cada vértice $v$, sea $\text{neto}(v)$ lo que sale de $v$ menos lo
que entra. Por conservación, $\text{neto}(v) = 0$ si $v \ne s, t$, y por definición
$\text{neto}(s) = |f|$. Como $t \notin S$,
$$|f| = \sum_{v \in S} \text{neto}(v).$$
Ahora mira cada arista $(u, v)$ en esa suma. Si los dos extremos están en $S$, su flujo
aparece una vez sumando (en $\text{neto}(u)$) y una vez restando (en $\text{neto}(v)$), y
se cancela. Si $u \in S$ y $v \in T$, aparece solo sumando. Si $u \in T$ y $v \in S$,
solo restando. Lo que queda es $f(S, T) - f(T, S)$. $\square$

**Lema 2.** Para todo flujo $f$ y todo corte $(S, T)$, $|f| \le c(S, T)$.

*Demostración.* Por el Lema 1, $|f| = f(S, T) - f(T, S) \le f(S, T) \le c(S, T)$, porque
el flujo es no negativo y no pasa de la capacidad. $\square$

Por el Lema 2, el mínimo de $c(S, T)$ sobre los $2^{V-2}$ cortes acota el flujo máximo
por arriba. La §6 demuestra que es igual, y eso lo convierte en un oráculo.

```{python continue}
def capacidad(aristas, S):
    return sum(c for u, v, c in aristas if u in S and v not in S)

def corte_bruto(n, aristas, s, t):
    otros = [v for v in range(n) if v not in (s, t)]
    return min(capacidad(aristas, {s, *X})
               for k in range(len(otros) + 1)
               for X in itertools.combinations(otros, k))

print("corte mínimo por fuerza bruta:", corte_bruto(6, EJEMPLO, s, t))
```

Hay un corte de capacidad 9 y un flujo de valor 9. Por el Lema 2, ningún flujo pasa de
9, así que `F9` es máximo. Y ningún corte baja de 9, porque `F9` cabe en todos.

## 6. Max-Flow Min-Cut

**Teorema** (Ford y Fulkerson, 1956). Para un flujo $f$ en una red, son equivalentes:

1. $f$ es un flujo máximo;
2. no hay camino de $s$ a $t$ en la red residual $G_f$;
3. $|f| = c(S, T)$ para algún corte $(S, T)$.

*Demostración.* (1) $\Rightarrow$ (2). Si hubiera un camino de aumento, aumentar por su
mínimo sobrante, que es positivo, daría un flujo de valor mayor.

(2) $\Rightarrow$ (3). Sea $S$ el conjunto de vértices alcanzables desde $s$ en $G_f$, y
$T = V \setminus S$. Por (2), $t \in T$, así que $(S, T)$ es un corte. Mira una arista
$(u, v)$ con $u \in S$ y $v \in T$. Si $f(u, v) < c(u, v)$, la arista $(u, v)$ estaría en
$G_f$, y $v$ sería alcanzable; entonces $f(u, v) = c(u, v)$. Ahora mira una arista
$(u, v)$ con $u \in T$ y $v \in S$. Si $f(u, v) > 0$, su inversa $(v, u)$ estaría en
$G_f$ con capacidad $f(u, v)$, y $u$ sería alcanzable desde $v$; entonces
$f(u, v) = 0$. Este es el paso que se suele saltar: no basta con que las aristas de $S$ a
$T$ estén llenas, también hace falta que las de vuelta estén vacías, y eso lo da la
inversa. Por el Lema 1,
$$|f| = f(S, T) - f(T, S) = c(S, T) - 0.$$

(3) $\Rightarrow$ (1). Por el Lema 2, todo flujo $g$ cumple $|g| \le c(S, T) = |f|$.
$\square$

Dos consecuencias. Ford-Fulkerson es correcto, porque para cuando se cumple (2). Y el
flujo máximo trae su certificado: la demostración de (2) $\Rightarrow$ (3) construye el
corte, los alcanzables desde $s$ en la residual final, y quien reciba flujo y corte
puede comprobar los dos sin creerle nada al algoritmo.

```{python continue}
def alcanzables(ady, hacia, cap, s):
    vistos, pila = {s}, [s]
    while pila:
        u = pila.pop()
        for e in ady[u]:
            if cap[e] > 0 and hacia[e] not in vistos:
                vistos.add(hacia[e])
                pila.append(hacia[e])
    return vistos

S1 = alcanzables(*R1, s)
print("S =", sorted(NOMBRES[v] for v in S1), "capacidad", capacidad(EJEMPLO, S1))
```

```{python continue echo=false output=asis}
print(G.corte_minimo(POS, NOMBRES, EJEMPLO, flujo_de(EJEMPLO, R1[2]), S1,
      ident="dinic-corte",
      pie="El corte de la residual final: S, sombreado, son los alcanzables desde s. "
          "Las aristas de S a T están llenas y la de T a S está vacía."))
```

La @fig-dinic-corte muestra las dos mitades de la demostración en el ejemplo. Las aristas
$s{\to}a$, $b{\to}a$ y $c{\to}t$ salen de $S$ y están llenas, $3 + 2 + 4 = 9$. La arista
$a{\to}c$ entra en $S$ y está vacía: es justo la que el cuarto aumento vació.

## 7. Caminos más cortos y grafo de niveles

Nuestro Ford-Fulkerson con búsqueda en anchura tiene nombre: es el algoritmo de Edmonds
y Karp (1972), que aumenta siempre por un camino con el menor número de aristas. La §11
demuestra que hace $O(VE)$ aumentos de $O(E)$ cada uno. Pero cada aumento recorre el
grafo entero para un solo camino. Dinic (1970) calcula las distancias una vez y empuja
por **todos** los caminos más cortos antes de volver a calcularlas.

Sea $\ell(v)$ la distancia de $s$ a $v$ en $G_f$, contando aristas, con $\ell(v) = \infty$
si $v$ no es alcanzable. El **grafo de niveles** $L_f$ tiene las aristas $(u, v)$ de $G_f$
con $\ell(v) = \ell(u) + 1$. Todo camino más corto de $s$ a $t$ en $G_f$ usa solo aristas
de $L_f$, porque en un camino más corto cada paso avanza exactamente un nivel. Un flujo
en $L_f$ es **bloqueante** si todo camino de $s$ a $t$ en $L_f$ tiene una arista
saturada.

## 8. Dinic

Una **fase** de Dinic calcula los niveles con una BFS y suma un flujo bloqueante del
grafo de niveles, hasta que $t$ deja de ser alcanzable. El flujo bloqueante lo busca una
búsqueda en profundidad que solo avanza un nivel por paso, con un **puntero de arista
actual** `it[u]`: la próxima arista de $u$ que vale la pena mirar. Un puntero solo avanza
cuando la arista no sirve más en esta fase: no es de nivel, está saturada, o por ella no
se llega a $t$. Si por la arista pasó flujo pero le sobra, el puntero se queda, porque la
próxima búsqueda puede volver a usarla.

```{python continue}
def niveles(ady, hacia, cap, s):
    nivel = [-1] * len(ady)
    nivel[s] = 0
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for e in ady[u]:
            if cap[e] > 0 and nivel[hacia[e]] < 0:
                nivel[hacia[e]] = nivel[u] + 1
                cola.append(hacia[e])
    return nivel

def empujar(u, x, t, ady, hacia, cap, nivel, it):
    """Manda hasta x unidades de u a t por el grafo de niveles."""
    if u == t:
        return x
    while it[u] < len(ady[u]):
        e = ady[u][it[u]]
        v = hacia[e]
        if cap[e] > 0 and nivel[v] == nivel[u] + 1:
            y = empujar(v, min(x, cap[e]), t, ady, hacia, cap, nivel, it)
            if y > 0:
                cap[e] -= y
                cap[e ^ 1] += y
                return y              # el puntero se queda: a e le puede sobrar
        it[u] += 1                    # e no sirve más en esta fase
    return 0

def dinic(n, aristas, s, t, empujar=empujar, traza=None):
    R = red(n, aristas)
    ady, hacia, cap = R
    total = 0
    while True:
        nivel = niveles(ady, hacia, cap, s)
        if nivel[t] < 0:
            return total, R
        antes, it, fase = cap[:], [0] * n, 0
        while (y := empujar(s, INF, t, ady, hacia, cap, nivel, it)) > 0:
            fase += y
        total += fase
        if traza is not None:
            traza.append((nivel[t], fase, nivel, antes, cap[:]))

traza = []
v2, R2 = dinic(6, EJEMPLO, s, t, traza=traza)
print("Dinic: valor", v2, "| fases (distancia, flujo):",
      [(d, x) for d, x, *_ in traza])
```

En el ejemplo, Dinic hace tres fases. La primera tiene distancia 3 y manda 4; la segunda,
distancia 4 y manda 2 por $s\,b\,a\,d\,t$; la tercera, distancia 5 y manda 3 por el camino
de la @fig-dinic-residual, el que deshace $a{\to}c$. Las distancias suben de una fase a
la siguiente, y eso es lo que la §9 demuestra.

```{python continue}
d1, x1, nivel1, antes1, despues1 = traza[0]
de_nivel = [(hacia[e ^ 1], hacia[e], antes1[e]) for e in range(len(antes1))
            if antes1[e] > 0 and nivel1[hacia[e]] == nivel1[hacia[e ^ 1]] + 1]
print("grafo de niveles de la fase 1:",
      [(NOMBRES[u] + NOMBRES[v], r) for u, v, r in de_nivel])
print("flujo bloqueante:", x1, "| máximo dentro del grafo de niveles:",
      dinic(6, de_nivel, s, t)[0])
```

```{python continue echo=false output=asis}
fuera1 = [(hacia[e ^ 1], hacia[e], antes1[e]) for e in range(len(antes1))
          if antes1[e] > 0 and nivel1[hacia[e]] != nivel1[hacia[e ^ 1]] + 1]
empujado = {(hacia[e ^ 1], hacia[e]): antes1[e] - despues1[e]
            for e in range(len(antes1)) if antes1[e] > despues1[e]}
print(G.grafo_niveles(POS, NOMBRES, nivel1, de_nivel, fuera1, empujado,
      ident="dinic-niveles",
      pie="El grafo de niveles de la fase 1 y su flujo bloqueante (empujado/residual; "
          "naranja, saturadas). La arista b→a, punteada, une dos vértices del mismo nivel "
          "y queda fuera."))
```

En la @fig-dinic-niveles, la búsqueda mandó 3 por $s\,a\,c\,t$, que satura $s{\to}a$ y
$a{\to}c$, y 1 por $s\,b\,c\,t$, que satura $c{\to}t$. Todo camino de $s$ a $t$ del grafo de
niveles pasa por $s{\to}a$ o por $c{\to}t$: el flujo de 4 es bloqueante. En el mismo grafo
cabe 7 (3 por $s\,a\,d\,t$ y 4 por $s\,b\,c\,t$): bloqueante no es máximo, y no hace falta
que lo sea, porque la fase 3 deshace lo necesario.

Antes de demostrar nada, comparamos contra el oráculo de la §5. Para saber que la
comparación puede fallar, le pasamos también el goloso de la §2. La batería tiene dos
mitades: 500 redes al azar de 4 a 8 vértices, y 500 redes **en capas**, con $k$ capas de
$w$ vértices y aristas solo de una capa a la siguiente.

```{python continue}
def red_al_azar(rng, n, p, cmax):
    return [(u, v, rng.randint(1, cmax)) for u in range(n) for v in range(n)
            if u != v and v != 0 and u != n - 1 and rng.random() < p]

def red_en_capas(rng, k, w, cmax):
    n = k * w + 2
    A = [(0, 1 + j, rng.randint(1, cmax)) for j in range(w)]
    for c in range(k - 1):                      # capa c -> capa c + 1
        for i in range(w):
            for j in range(w):
                if rng.random() < 0.5:
                    u, v = 1 + c * w + i, 1 + (c + 1) * w + j
                    A.append((u, v, rng.randint(1, cmax)))
    A += [(1 + (k - 1) * w + j, n - 1, rng.randint(1, cmax)) for j in range(w)]
    return n, A

rng = random.Random(13)
REDES = []
for _ in range(500):
    n = rng.randint(4, 8)
    REDES.append((n, red_al_azar(rng, n, rng.choice([0.3, 0.5, 0.7]),
                                 rng.choice([1, 3, 10]))))
for _ in range(500):
    REDES.append(red_en_capas(rng, rng.choice([2, 3]), rng.choice([2, 3]),
                              rng.choice([3, 10])))
OPT = [corte_bruto(n, A, 0, n - 1) for n, A in REDES]
for nombre, lote in (("al azar", range(500)), ("en capas", range(500, 1000))):
    mal_dinic = sum(dinic(*REDES[i], 0, REDES[i][0] - 1)[0] != OPT[i] for i in lote)
    mal_goloso = sum(ford_fulkerson(*REDES[i], 0, REDES[i][0] - 1, inversas=False)[0]
                     != OPT[i] for i in lote)
    print(f"500 redes {nombre}: Dinic falla en {mal_dinic}, "
          f"el goloso en {mal_goloso}")
```

Dinic coincide con el corte mínimo en todas. El goloso no falla en ninguna de las 500
redes al azar y falla en 34 de las 500 en capas. Es la lección del capítulo 2, §7: una
batería al azar prueba la distribución de la que sale, y la uniforme casi nunca produce
caminos que compitan por las mismas aristas del medio, que es lo que atasca al goloso
en el ejemplo.

El artículo original de Yefim Dinitz salió en ruso en *Doklady Akademii Nauk SSSR*
194(4), 1970. Él mismo cuenta («Dinitz' Algorithm: The Original Version and Even's
Version», 2006) que la versión conocida por el mundo con su nombre es una modificación de
Shimon Even y Alon Itai.

## 9. La distancia sube en cada fase

El experimento primero: sobre las mismas 1 000 redes, un `assert` de que la distancia
crece de fase en fase y de que no hay más de $V - 1$ fases.

```{python continue}
def distancias(n, A, empujar=empujar):
    tr = []
    dinic(n, A, 0, n - 1, empujar=empujar, traza=tr)
    return [d for d, *_ in tr]

for n, A in REDES:
    ds = distancias(n, A)
    assert all(x < y for x, y in zip(ds, ds[1:])) and len(ds) <= n - 1
print("distancias estrictamente crecientes en las", len(REDES), "redes")
```

**Lema 3.** Sea $d$ la distancia de $s$ a $t$ al empezar una fase, y $\ell$ los niveles de
esa BFS. Al terminar la fase, todo camino de $s$ a $t$ en la residual tiene al menos
$d + 1$ aristas.

*Demostración.* Primero un invariante: **durante toda la fase, cada arista residual
$(u, v)$ con $\ell(u)$ finito cumple $\ell(v) \le \ell(u) + 1$.** Al principio de la fase
es cierto porque $\ell$ es una distancia de BFS: si $(u, v)$ está en la residual, $v$ está
a lo sumo un paso más lejos que $u$. Durante la fase, el único cambio que puede hacer
aparecer una arista nueva (o darle capacidad a una que no tenía) es empujar por una
arista $(u, v)$ del grafo de niveles, lo que le da capacidad a la inversa $(v, u)$. Como
$\ell(v) = \ell(u) + 1$, esa inversa va de un nivel al anterior, y cumple el invariante con
holgura. Las aristas que solo pierden capacidad no lo pueden romper.

El invariante tiene otra consecuencia: ninguna arista residual sale de un vértice
alcanzado hacia uno con $\ell = \infty$, así que un camino que sale de $s$ se queda entre
vértices con nivel finito.

Ahora toma un camino $s = v_0, v_1, \dots, v_k = t$ en la residual al final de la fase.
Sus saltos de nivel suman
$$\sum_{i=1}^{k} \bigl(\ell(v_i) - \ell(v_{i-1})\bigr) = \ell(t) - \ell(s) = d,$$
y cada salto vale a lo sumo 1, así que $k \ge d$. Si $k = d$, todos los saltos valen
exactamente 1. Una arista residual con salto 1 no puede ser nueva, porque las nuevas
bajan un nivel. Entonces es una arista del grafo de niveles a la que le queda capacidad.
El camino entero estaría en el grafo de niveles sin ninguna arista saturada, y eso
contradice que el flujo de la fase es bloqueante. Por lo tanto $k \ge d + 1$. $\square$

La palabra que hace el trabajo es **bloqueante**, en la última línea. El resto del
argumento vale para cualquier flujo empujado por el grafo de niveles.

**Corolario.** Dinic hace a lo sumo $V - 1$ fases. La distancia de una fase es al menos
1, sube en al menos 1 por fase, y mientras $t$ es alcanzable no pasa de $V - 1$.

## 10. El error plantado: avanzar el puntero de más

Cuando `empujar` manda flujo por `e`, devuelve sin avanzar el puntero. Parece un
descuido, porque la arista "ya se usó", y la variante que lo avanza se escribe sin
pensar:

```{python continue}
def empujar_roto(u, x, t, ady, hacia, cap, nivel, it):
    if u == t:
        return x
    while it[u] < len(ady[u]):
        e = ady[u][it[u]]
        v = hacia[e]
        if cap[e] > 0 and nivel[v] == nivel[u] + 1:
            y = empujar_roto(v, min(x, cap[e]), t, ady, hacia, cap, nivel, it)
            if y > 0:
                cap[e] -= y
                cap[e ^ 1] += y
                it[u] += 1            # el error: a e le puede sobrar capacidad
                return y
        it[u] += 1
    return 0

mal_valor = sum(dinic(n, A, 0, n - 1, empujar=empujar_roto)[0] != o
                for (n, A), o in zip(REDES, OPT))
no_crece = sum(any(x >= y for x, y in zip(ds, ds[1:]))
               for ds in (distancias(n, A, empujar_roto) for n, A in REDES))
print(f"variante: valor equivocado en {mal_valor} de {len(REDES)} redes; "
      f"distancia que no crece en {no_crece}")
```

El valor es correcto en las 1 000 redes: el oráculo, que en la §8 atrapó al goloso,
aquí no ve nada. El `assert` de la §9 sí: la distancia deja de crecer en 280 de las
1 000.

El valor no puede fallar porque la variante sigue aumentando por caminos de la residual
y solo termina cuando $t$ deja de ser alcanzable, así que el teorema de la §6 vale igual.
Lo que se rompe es la palabra "bloqueante" del Lema 3. Si la búsqueda manda $y$ unidades
por una arista con capacidad mayor que $y$, la variante la salta, y la fase puede
terminar con un camino del grafo de niveles sin aristas saturadas. La fase siguiente
tiene la misma distancia y el corolario deja de valer.

Cuánto cuesta lo muestra una familia: $s{\to}a$ con capacidad $k^2$, $a{\to}b_i$ con $k$
para $i < k$, todas las $b_i{\to}c_j$ con 1 y $c_j{\to}t$ con $k$. Cada camino lleva 1
unidad, por el cuello $b_i{\to}c_j$, así que el primer empuje deja sobrante en
$s{\to}a$ y la variante salta la única arista que sale de $s$.

```{python continue}
def familia(k):
    s, a, t = 0, 1, 2 * k + 2
    A = [(s, a, k * k)]
    A += [(a, 2 + i, k) for i in range(k)]
    A += [(2 + i, 2 + k + j, 1) for i in range(k) for j in range(k)]
    A += [(2 + k + j, t, k) for j in range(k)]
    return 2 * k + 3, A

for k in (2, 4, 8, 16):
    n, A = familia(k)
    bien, mal = distancias(n, A), distancias(n, A, empujar_roto)
    print(f"k={k:2}  V={n:2}  valor={dinic(n, A, 0, n - 1)[0]:3}  "
          f"fases Dinic={len(bien)}  fases variante={len(mal):3}  "
          f"distancias variante={sorted(set(mal))}")
```

Dinic hace una fase y la variante $k^2$, todas de distancia 4: con $k = 16$ son 256 fases
en una red de 35 vértices, más que $V - 1$, y cada una paga una BFS para mandar 1
unidad.

## 11. El costo de una fase

**Lema 4.** Una fase de Dinic cuesta $O(VE)$.

*Demostración.* La BFS cuesta $O(V + E)$. En el flujo bloqueante contamos los pasos de
`empujar`, las veces que la búsqueda avanza de $u$ a $v$ por una arista.

Los pasos de un camino que llega a $t$: cada camino tiene a lo sumo $V - 1$ aristas, y
cada aumento satura la arista que dio el mínimo. Esa arista no recupera capacidad en la
fase, porque haría falta empujar por su inversa, que baja un nivel y no está en el grafo
de niveles. Hay a lo sumo $E$ aumentos y $O(VE)$ pasos de esta clase.

Los pasos que no llegan a $t$: si la búsqueda entra en $v$ y vuelve con 0, el puntero de
$u$ avanza, igual que con las aristas que se descartan sin entrar. Cada puntero recorre
su lista una sola vez por fase, y las listas suman $2E$ posiciones.

Cada llamada desde $s$ acaba en un aumento o en el fin de la fase: hay a lo sumo $E + 1$.
En total, $O(V + E + VE + E) = O(VE)$. $\square$

**Teorema.** Dinic calcula un flujo máximo en tiempo $O(V^2 E)$.

*Demostración.* Correcto por la §6, porque termina cuando no hay camino de aumento. A lo
sumo $V - 1$ fases por el corolario del Lema 3, y $O(VE)$ por fase por el Lema 4.
$\square$

La variante de la §10 cumple el Lema 4 en cada fase; lo que pierde es la cuenta de fases.

El mismo invariante da la cota de **Edmonds-Karp**, aunque Edmonds-Karp no trabaje por
fases. Sea $\ell$ el resultado de la BFS en el momento en que la distancia de $s$ a $t$
llega a $d$. Mientras la distancia valga $d$, cada aumento va por un camino de $d$
aristas, y el argumento del Lema 3 dice que todas sus aristas saltan exactamente un
nivel, o sea que son del grafo de niveles de ese momento. El aumento satura una de
ellas, que no recupera capacidad mientras la distancia valga $d$ (su inversa baja un
nivel, y un camino de $d$ aristas no puede usarla). Así que hay a lo sumo $E$ aumentos
con distancia $d$, y como la distancia nunca baja (el mismo argumento), hay a lo sumo
$V - 1$ valores de $d$. Son $O(VE)$ aumentos de $O(E)$ cada uno: $O(VE^2)$. Edmonds y
Karp lo demostraron de otra manera, que es el ejercicio 4.

## 12. Capacidades unitarias y Hopcroft-Karp

El emparejamiento bipartito máximo del capítulo 10, §10, es un flujo máximo. A un grafo
bipartito con lados $X$ e $Y$ se le agrega una fuente $s$ con una arista a cada
$x \in X$, una arista de cada $y \in Y$ al sumidero $t$, y las aristas del grafo se
orientan de $X$ a $Y$; todas con capacidad 1. Por la integralidad de la §4 hay un flujo
máximo entero, y sus aristas de $X$ a $Y$ con flujo 1 forman un emparejamiento, porque a
cada $x$ le entra a lo sumo 1 y de cada $y$ sale a lo sumo 1. Al revés, todo
emparejamiento da un flujo de su tamaño.

Una red es
**unitaria** si todas las capacidades valen 1, no hay aristas antiparalelas, y cada
vértice distinto de $s$ y $t$ tiene una sola arista de entrada o una sola de salida. En la
red bipartita, cada $x$ tiene una sola de entrada y cada $y$ una sola de salida.

**Lema 5.** La red residual de un flujo entero en una red unitaria es unitaria.

*Demostración.* Sin antiparalelas, cada arista $(u, v)$ deja en la residual exactamente
una arista de capacidad 1: $(u, v)$ si su flujo es 0, o $(v, u)$ si es 1. Toma un vértice
$v$ con una sola arista de entrada, $(u, v)$. Si su flujo es 0, por conservación no sale
nada de $v$; en la residual entra solo $(u, v)$, porque las inversas de las salidas no
están. Si su flujo es 1, sale exactamente 1 por una arista $(v, w)$; en la residual,
$(u, v)$ se convirtió en $(v, u)$, y entra solo $(w, v)$. En los dos casos entra una sola
arista. El caso de una sola arista de salida es simétrico. $\square$

**Lema 6.** Si $f^*$ es un flujo máximo, el flujo máximo de $G_f$ vale $|f^*| - |f|$.

*Demostración.* La capacidad residual de un corte $(S, T)$ es
$$\sum_{u \in S, v \in T} \bigl(c(u, v) - f(u, v)\bigr) + \sum_{u \in T, v \in S} f(u, v)
= c(S, T) - f(S, T) + f(T, S) = c(S, T) - |f|,$$
por el Lema 1. El corte mínimo de $G_f$ es el de $G$ menos $|f|$, y por el teorema de la
§6 aplicado a $G_f$, ese es su flujo máximo. $\square$

Un flujo entero de valor $k$ se **descompone en caminos**: desde $s$ se sigue cualquier
arista con flujo positivo, y por conservación siempre hay por dónde seguir. Si se repite
un vértice, se quita ese ciclo del recorrido; al llegar a $t$, se resta 1 a lo largo del camino y se
repite. Salen $k$ caminos. En una red unitaria pasa a lo sumo 1 unidad por cada vértice
interno, así que los caminos no comparten vértices internos.

**Teorema.** En una red unitaria, Dinic hace menos de $2\sqrt V + 1$ fases, cada una en
$O(E)$, y cuesta $O(E \sqrt V)$.

*Demostración.* Una fase cuesta $O(E)$: con capacidades 1, cada aumento satura todas las
aristas de su camino, así que cada arista entra en a lo sumo un camino que llega a $t$, y
los pasos que no llegan avanzan un puntero, como en el Lema 4.

Para las fases, sea $p = \lceil \sqrt V \rceil$. Después de $p$ fases, por el Lema 3 la
distancia es al menos $p + 1$. Por el Lema 6, lo que falta por mandar es un flujo de
valor $|f^*| - |f|$ en $G_f$, que es unitaria por el Lema 5, y se descompone en
$|f^*| - |f|$ caminos sin vértices internos comunes. Cada uno tiene al menos $p + 1$
aristas, o sea al menos $p$ vértices internos. Como hay $V - 2$ vértices internos en
total, $|f^*| - |f| \le (V - 2)/p < \sqrt V$. Cada fase siguiente suma al menos 1, así que
quedan menos de $\sqrt V$ fases. En total, menos de $p + \sqrt V \le 2\sqrt V + 1$.
$\square$

Sobre la red bipartita, esto es el algoritmo de Hopcroft y Karp
(«An $n^{5/2}$ algorithm for maximum matchings in bipartite graphs», *SIAM Journal on
Computing* 2(4), 1973), que en cada fase busca un conjunto maximal de caminos de aumento
más cortos sin vértices comunes.

¿Se alcanza la cota de fases? Para $m = 1, \dots, k$, toma una escalera
$x_1 y_1 x_2 y_2 \dots x_m y_m$: cada $x_i$ es vecino de $y_i$ y, si $i > 1$, de
$y_{i-1}$, que va primero en su lista, y $x_1$ va último en la lista de $s$. La primera
fase empareja cada $x_i$ con $y_{i-1}$ y deja libres a $x_1$ y a $y_m$; el único camino
de aumento recorre la escalera entera, con $2m + 1$ aristas. Cada escalera tiene otro
largo, así que se completa en otra fase. El código compara antes contra el oráculo de la
§5 en grafos bipartitos chicos.

```{python continue}
def red_bipartita(L, R, aristas_xy, orden_s=None):
    n = L + R + 2
    A = [(0, 1 + x, 1) for x in (orden_s or range(L))]
    A += [(1 + x, 1 + L + y, 1) for x, y in aristas_xy]
    A += [(1 + L + y, n - 1, 1) for y in range(R)]
    return n, A

rng = random.Random(7)
fallos = 0
for _ in range(300):
    L, R = rng.randint(1, 5), rng.randint(1, 5)
    n, A = red_bipartita(L, R, [(x, y) for x in range(L) for y in range(R)
                                if rng.random() < 0.4])
    fallos += dinic(n, A, 0, n - 1)[0] != corte_bruto(n, A, 0, n - 1)
print("300 grafos bipartitos, fallos:", fallos)
```

```{python continue}
def escalera(k):
    aristas_xy, orden_s, base = [], [], 0
    for m in range(1, k + 1):
        xs = list(range(base, base + m))
        orden_s += xs[1:] + xs[:1]                  # x_1 al final
        for i in range(m):
            if i > 0:
                aristas_xy.append((base + i, base + i - 1))   # primero y_{i-1}
            aristas_xy.append((base + i, base + i))
        base += m
    return base, base, aristas_xy, orden_s

for k in (2, 4, 8, 16):
    n, A = red_bipartita(*escalera(k))
    valor, fases = dinic(n, A, 0, n - 1)[0], len(distancias(n, A))
    print(f"k={k:2}  V={n:3}  emparejamiento={valor:3}  fases={fases:2}  "
          f"2√V+1={2 * math.sqrt(n) + 1:5.1f}")
```

Con $k$ escaleras, $V = k^2 + k + 2$ y hay $k$ fases, cerca de $\sqrt V$: la cota se
alcanza salvo por un factor 2.

La condición de grado no es un detalle. Sin ella, por un vértice puede pasar mucho flujo,
los caminos de la descomposición comparten vértices y el argumento se cae. Contar
aristas en lugar de vértices da $O(\sqrt E)$ fases, que es el ejercicio 5. Shimon Even y
Robert Tarjan («Network flow and testing graph connectivity», *SIAM Journal on Computing*
4(4), 1975) demostraron además $O(V^{2/3} E)$ para ese caso y $O(\sqrt V E)$ para el caso
con capacidades unitarias en los vértices, y que esas cotas son ajustadas para Dinic.

## 13. La regla

La regla del capítulo: **una cota de costo que sale de un invariante se comprueba con el
invariante, no con la salida.** En la §10 las dos versiones dan el mismo flujo en todas
las redes; la diferencia está en la sucesión de distancias, que ningún oráculo de valores
ve y el `assert` de la §9 sí.

El capítulo 14 llega a la misma cota $O(V^2 E)$ con otra idea, preflujos que violan la
conservación. El capítulo 15 contrasta el corte $s$-$t$ con el corte mínimo global, que
el algoritmo aleatorio de Karger encuentra sin fijar $s$ ni $t$. Y el problema sigue
abierto por arriba: James Orlin («Max flows in $O(nm)$ time, or
better», STOC 2013) bajó la cota a $O(VE)$, y Li Chen, Rasmus Kyng, Yang P. Liu, Richard
Peng, Maximilian Probst Gutenberg y Sushant Sachdeva («Maximum Flow and Minimum-Cost Flow
in Almost-Linear Time», FOCS 2022; versión completa en *Journal of the ACM* 72(3), 2025)
lo resolvieron en tiempo $E^{1+o(1)}$ para capacidades enteras acotadas por un
polinomio en el tamaño del grafo. El epílogo vuelve sobre ese resultado.

## Resumen

- El goloso de caminos se atasca porque no puede retirar lo que mandó.
- La **red residual** tiene lo que sobra hacia adelante y lo que se puede devolver hacia
  atrás. **Ford-Fulkerson** aumenta por ella y, con capacidades enteras, termina con un
  flujo entero.
- **Max-Flow Min-Cut**: $f$ es máximo si y solo si no hay camino de aumento si y solo si
  $|f| = c(S, T)$ para algún corte. El corte mínimo se lee de la residual final: los
  alcanzables desde $s$. Las aristas de $S$ a $T$ están llenas y las de $T$ a $S$,
  vacías.
- **Dinic**: por fases, BFS de niveles y flujo **bloqueante** con puntero de arista
  actual. La distancia de $s$ a $t$ sube en cada fase (Lema 3), así que hay a lo sumo
  $V - 1$ fases de $O(VE)$: $O(V^2 E)$.
- El mismo invariante da $O(VE^2)$ para **Edmonds-Karp**.
- Avanzar el puntero tras un empuje parcial deja el valor correcto y rompe el bloqueo:
  de 1 a $k^2$ fases en la familia construida.
- En una **red unitaria** (capacidad 1, una sola entrada o una sola salida por vértice),
  Dinic hace menos de $2\sqrt V + 1$ fases de $O(E)$: $O(E\sqrt V)$. Sobre el
  emparejamiento bipartito es **Hopcroft-Karp**.

## Ejercicios

1. **[traza]** Ejecuta Dinic a mano sobre la red $s{\to}a$ 4, $s{\to}b$ 8, $b{\to}a$ 1,
   $a{\to}c$ 4, $a{\to}d$ 2, $b{\to}c$ 7, $c{\to}t$ 9, $d{\to}t$ 9, $d{\to}b$ 2,
   recorriendo las aristas de cada vértice en el orden de la lista. Da los niveles, el
   grafo de niveles y el flujo bloqueante de cada fase. Lee de la residual final el
   corte mínimo y comprueba que su capacidad es el valor del flujo.

2. **[traza]** Un grafo bipartito tiene las listas $x_0{:}\ y_2, y_3, y_4$;
   $x_1{:}\ y_1, y_2, y_3$; $x_2{:}\ y_2$; $x_3{:}\ y_1$; $x_4{:}\ y_2$. Ejecuta
   Hopcroft-Karp (Dinic sobre la red de la §12) con los $x$ en ese orden: fases,
   distancias y emparejamiento. Con $S$ el lado de la fuente del corte de la residual
   final, demuestra que $(X \setminus S) \cup (Y \cap S)$ toca todas las aristas y tiene
   el tamaño del emparejamiento, y concluye que este es máximo sin enumerar nada.

3. **[entrada que rompe]** La red tiene $s{\to}a$, $s{\to}b$, $a{\to}t$ y $b{\to}t$ con
   capacidad $C$, y $a{\to}b$ con capacidad 1. Da una sucesión de caminos de aumento con
   la que Ford-Fulkerson hace $2C$ aumentos. ¿Cuántos hace Edmonds-Karp? ¿Qué dice esto
   de la cota de la §4?

4. **[demostración]** En Edmonds-Karp, una arista es **crítica** en un aumento si da el
   mínimo y queda saturada. Demuestra que la distancia de $s$ a cada vértice nunca baja,
   que entre dos veces en que $(u, v)$ es crítica la distancia de $s$ a $u$ sube en al
   menos 2, y concluye que hay $O(VE)$ aumentos.

5. **[demostración] ★** Una red tiene capacidades 1 y ninguna arista antiparalela, pero
   no cumple la condición de grado de la §12. Demuestra que Dinic hace a lo sumo
   $2\sqrt E$ fases. ¿Qué cambia en la demostración de la §12, y por qué la residual
   sigue teniendo a lo sumo $E$ aristas?

6. **[demostración]** Menger, versión de vértices: en un grafo dirigido, si $(u, w)$ no
   es arista, el máximo de caminos de $u$ a $w$ sin vértices internos comunes es igual al
   mínimo de vértices (distintos de $u$ y $w$) cuya eliminación deja a $w$ inalcanzable.
   Demuéstralo con flujo máximo, desdoblando cada vértice $v$ en
   $v_{\text{in}} \to v_{\text{out}}$ con capacidad 1. ¿Qué capacidad llevan las demás
   aristas, y por qué el corte mínimo no las usa?

7. **[modelar]** Con cotas inferiores, cada arista pide
   $\lambda(u, v) \le f(u, v) \le c(u, v)$. Agrega una arista $t \to s$ de capacidad
   infinita y reduce la existencia de un flujo factible, con conservación en todos los
   vértices, a un flujo máximo en otra red. Demuestra las dos direcciones.

8. **[modelar]** El proyecto $i$ da una ganancia $p_i$, que puede ser negativa, y algunos
   proyectos exigen otros. Se busca un conjunto cerrado por prerrequisitos de ganancia
   máxima. Plantéalo como un corte mínimo, demuestra que los cortes de capacidad finita
   son los conjuntos cerrados, e implementa la reducción con el `dinic` del capítulo
   contra la enumeración de los $2^n$ conjuntos para $n \le 12$.

9. **[cambio de hipótesis]** Las capacidades son reales. ¿Qué demostraciones del capítulo
   usan que son enteras? ¿Termina Dinic, y con qué cota? ¿Por qué el argumento de la §4
   no basta para Ford-Fulkerson con caminos arbitrarios?

10. **[implementar y medir]** Cuenta las aristas examinadas por Edmonds-Karp y por
    `dinic` en redes al azar densas y en redes de capas ($k$ capas de $w$ vértices). ¿Cómo
    crece el cociente con $k$ y con $w$? Explica por qué las cotas $O(VE^2)$ y $O(V^2E)$
    no lo predicen.
