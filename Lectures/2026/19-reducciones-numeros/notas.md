# Reducciones a secuencias y números {#chap-reducciones-numeros}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_19.py
import figuras_19 as F19
```

Hasta el capítulo 18, cada solución fue un conjunto: de vértices independientes, de
vértices que cubren, de colores. Un gadget era un pedazo de grafo que obliga a elegir
ciertos vértices o prohíbe elegir otros. Este capítulo llega a problemas donde la
solución tiene otra forma. En ciclo hamiltoniano y en TSP la solución es un **orden**
de los vértices, y en suma de subconjuntos y mochila es una **suma** de números. La
pregunta de diseño es la misma de siempre, dónde se esconde la elección de un valor
de verdad, pero el material es otro. En un orden se esconde en el sentido en que se
recorre una fila de vértices, y en una suma, en qué número se suma. En los dos casos
el peligro también es el mismo: que dos piezas de la construcción se comuniquen por
donde la demostración no previó. Al final del capítulo quedan demostrados los once
problemas que el plan del curso prometió para la Parte III.

## 1. Dos formas nuevas de solución

El capítulo 16 demostró que conjunto independiente, clique y vertex cover se reducen
entre sí. El capítulo 17 demostró que SAT es NP-completo y redujo SAT a 3-SAT. El
capítulo 18 redujo 3-SAT a conjunto independiente, vertex cover a set cover y 3-SAT a
3-coloración. Son siete problemas, y en todos el certificado es un subconjunto o una
función de los vértices a unos pocos valores.

Los dos problemas nuevos ya aparecieron como ejemplos de certificado en el capítulo
16, ejercicio 1:

- **Ciclo hamiltoniano.** Dado un grafo, ¿hay un ciclo que pasa exactamente una vez
  por cada vértice? Lo estudiamos primero en grafos dirigidos, donde el ciclo sigue el
  sentido de los arcos.
- **Suma de subconjuntos.** Dados enteros positivos $a_1, \dots, a_m$ y una meta $T$,
  ¿hay un subconjunto que sume exactamente $T$?

Los dos están en NP. El certificado del primero es el orden de los vértices, que se
comprueba arco por arco en tiempo lineal. El del segundo es el subconjunto, que se
comprueba con una suma de $m$ números de a lo sumo tantos bits como la entrada.

El triángulo del capítulo 18 no sirve aquí. Un ciclo hamiltoniano no elige vértices,
porque los visita todos, y una suma no tiene vértices. Partimos, como en el capítulo
18, de 3-SAT tal como lo definió el capítulo 17, §10: cada cláusula tiene exactamente
tres literales, sobre tres variables distintas. Escribimos $n$ para el número de
variables y $k$ para el de cláusulas.

## 2. Una elección binaria dentro de un ciclo

Un ciclo hamiltoniano pasa por todos los vértices, así que la elección no puede ser
"pasar o no pasar por este vértice". Tiene que ser **cómo** pasar. La idea es una fila
de vértices $v_1, v_2, \dots, v_b$ con arcos entre vecinos en los dos sentidos, a la
que solo se puede entrar y de la que solo se puede salir por los extremos. Un ciclo
que la visita entera tiene dos maneras de hacerlo: de $v_1$ a $v_b$ o de $v_b$ a $v_1$.
Una fila por variable, y "de izquierda a derecha" quiere decir que la variable es
verdadera.

Falta la cláusula. Tiene que ser algo que el ciclo pueda visitar solo si alguno de sus
literales es verdadero. Pon un vértice $c$ para la cláusula y, si $x_i$ aparece en
ella, los arcos $v_p \to c \to v_{p+1}$ entre dos vértices consecutivos de la fila $i$.
Un ciclo que recorre la fila de izquierda a derecha puede desviarse: en vez de ir de
$v_p$ a $v_{p+1}$, va de $v_p$ a $c$ y de $c$ a $v_{p+1}$. Un ciclo que la recorre de
derecha a izquierda no puede, porque llega a $v_{p+1}$ antes que a $v_p$. Si aparece
$\lnot x_i$, los arcos van al revés, $v_{p+1} \to c \to v_p$, y el desvío solo sirve
de derecha a izquierda.

Hazlo a mano con una variable y la cláusula $(x_1)$: una fila $v_1 v_2 v_3 v_4$, el
desvío $v_2 \to c \to v_3$, y un arco de vuelta de cada extremo de la fila al otro
pasando por un vértice $s$. El ciclo $s, v_1, v_2, c, v_3, v_4, s$ existe, y el que
recorre la fila al revés no puede visitar $c$. Con $(\lnot x_1)$ pasa lo contrario.

Dos detalles salen de este ejemplo. Primero, cada cláusula necesita su propio par de
vértices en cada fila: un recorrido hace un solo desvío entre dos vértices
consecutivos. Segundo, una cláusula tiene tres literales, así que $c$ tiene arcos a
tres filas distintas, y nada impide en principio que el ciclo entre a $c$ desde una
fila y salga hacia otra. Para eso, entre par y par se deja un vértice de separación.
La §5 muestra exactamente dónde se usa.

## 3. La construcción

Cada fila tiene $b = 3k + 3$ vértices $v_{i,1}, \dots, v_{i,b}$. La cláusula $j$ usa
las posiciones $3j$ y $3j + 1$, y las posiciones $2, 5, \dots, 3k + 2$ quedan de
separación. Además hay un vértice $s$ con arcos a los dos extremos de la primera fila,
arcos de cada extremo de la fila $i$ a cada extremo de la fila $i + 1$, arcos de los
extremos de la última fila a un vértice $t$, y el arco $t \to s$. Si $x_i$ aparece en
la cláusula $j$, se agregan $v_{i,3j} \to c_j \to v_{i,3j+1}$, y si aparece $\lnot
x_i$, se agregan $v_{i,3j+1} \to c_j \to v_{i,3j}$.

```{python continue}
def a_hamiltoniano(clausulas, n):
    """3-SAT -> ciclo hamiltoniano dirigido. Las variables son 1..n; -i es ¬x_i."""
    k = len(clausulas)
    b = 3 * k + 3
    v = lambda i, p: ("v", i, p)
    arcos = []
    for i in range(1, n + 1):
        for p in range(1, b):
            arcos += [(v(i, p), v(i, p + 1)), (v(i, p + 1), v(i, p))]
    extremos = lambda i: [v(i, 1), v(i, b)]
    arcos += [("s", e) for e in extremos(1)]
    for i in range(1, n):
        arcos += [(e, f) for e in extremos(i) for f in extremos(i + 1)]
    arcos += [(e, "t") for e in extremos(n)] + [("t", "s")]
    for j, c in enumerate(clausulas, 1):
        for l in c:
            i, p = abs(l), 3 * j
            if l > 0:
                arcos += [(v(i, p), ("c", j)), (("c", j), v(i, p + 1))]
            else:
                arcos += [(v(i, p + 1), ("c", j)), (("c", j), v(i, p))]
    vertices = list(dict.fromkeys(x for a in arcos for x in a))
    return vertices, arcos

phi = [[1, -2, 3], [-1, 2, 3]]
V, A = a_hamiltoniano(phi, 3)
n, k = 3, len(phi)
print("vértices:", len(V), " n(3k+3)+k+2 =", n * (3 * k + 3) + k + 2)
print("arcos:   ", len(A), " 6nk+8n+6k+1 =", 6 * n * k + 8 * n + 6 * k + 1)
```

Para la fórmula $(x_1 \lor \lnot x_2 \lor x_3) \land (\lnot x_1 \lor x_2 \lor x_3)$
salen 31 vértices y 73 arcos. Las cuentas generales son $n(3k + 3) + k + 2$
vértices, y $6nk + 8n + 6k + 1$ arcos: $2(b - 1)$ por fila, $4n + 1$ entre filas y con
$s$ y $t$, y seis por cláusula. El grafo es lineal en el tamaño de la fórmula y se
escribe en ese tiempo.

Para ver un ciclo hace falta buscarlo. La búsqueda en profundidad sale de $s$ y avanza
por arcos a vértices no visitados. Sin poda tarda demasiado incluso en este grafo, y
la poda que basta es una: después de cada paso, todos los vértices que faltan tienen
que poder alcanzarse desde el vértice actual por vértices no visitados. Si alguno
quedó aislado, ninguna continuación del camino lo va a recoger.

```{python continue}
def ciclos_hamiltonianos(vertices, arcos):
    """Genera los ciclos hamiltonianos dirigidos que empiezan en "s"."""
    sal = {}
    for u, w in arcos:
        sal.setdefault(u, []).append(w)
    N, visto = len(vertices), {"s"}

    def todos_alcanzables(u):
        pila, alcanzados = [u], {u}
        while pila:
            for w in sal.get(pila.pop(), []):
                if w not in visto and w not in alcanzados:
                    alcanzados.add(w)
                    pila.append(w)
        return len(alcanzados) - 1 == N - len(visto)

    def dfs(camino):
        for w in sal.get(camino[-1], []):
            if w == "s" and len(camino) == N:
                yield list(camino)
            elif w not in visto:
                visto.add(w)
                camino.append(w)
                if len(camino) == N or todos_alcanzables(w):
                    yield from dfs(camino)
                camino.pop()
                visto.discard(w)
    yield from dfs(["s"])

def asignacion_del_ciclo(ciclo, n):
    """x_i es verdadera si el ciclo pasa por v_{i,1} antes que por v_{i,2}."""
    lugar = {x: r for r, x in enumerate(ciclo)}
    return {i: lugar[("v", i, 1)] < lugar[("v", i, 2)] for i in range(1, n + 1)}

ciclo = next(ciclos_hamiltonianos(V, A))
valor = asignacion_del_ciclo(ciclo, 3)
print("asignación leída del ciclo:", valor)
print("desvíos:", [(ciclo[r - 1][1], x[1]) for r, x in enumerate(ciclo) if x[0] == "c"],
      "  (fila, cláusula)")
```

El primer ciclo que encuentra la búsqueda recorre las tres filas de izquierda a
derecha, así que se lee la asignación con las tres variables verdaderas, que cumple la
fórmula. Visita $c_1$ y $c_2$ desviándose desde la fila 3, por el literal $x_3$, que
está en las dos cláusulas. La @fig-rn-filas lo dibuja.

```{python continue echo=false output=asis}
print(F19.filas(3, phi, A, ciclo, valor, ident="rn-filas",
      pie="El grafo de (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₃), con el ciclo que encontró "
          "la búsqueda. Cada fila se recorre entera en un sentido, que da el valor de "
          "la variable. Los puntos grises son los vértices de separación. Los arcos "
          "naranjas son los desvíos por las cláusulas, los dos desde la fila de x₃; "
          "cada cláusula está dibujada debajo de la fila desde la que se desvía el ciclo."))
```

## 4. El experimento {#reducciones-numeros-4-el-experimento}

Antes de demostrar nada, contemos. Si la construcción hace lo que queremos, cada ciclo
debería corresponder a una asignación que cumple la fórmula y a la elección, para cada
cláusula, de un literal verdadero desde cuya fila desviarse. Si eso es así, el número
de ciclos es
$$\sum_{a} \prod_{j=1}^{k} t_j(a),$$
donde $a$ recorre las $2^n$ asignaciones y $t_j(a)$ es el número de literales
verdaderos de la cláusula $j$ con $a$. Una asignación que deja una cláusula falsa
aporta un factor 0.

```{python continue}
def cuenta_predicha(clausulas, n):
    total = 0
    for bits in itertools.product([False, True], repeat=n):
        a = dict(enumerate(bits, 1))
        total += math.prod(sum(a[abs(l)] == (l > 0) for l in c) for c in clausulas)
    return total

def formula_al_azar(n, k):
    return [[random.choice([1, -1]) * x for x in random.sample(range(1, n + 1), 3)]
            for _ in range(k)]

random.seed(19)
distintas, inicio = 0, time.perf_counter()
for _ in range(24):
    f = formula_al_azar(3, random.randint(1, 2))
    contados = sum(1 for _ in ciclos_hamiltonianos(*a_hamiltoniano(f, 3)))
    distintas += contados != cuenta_predicha(f, 3)
print("24 fórmulas, conteos distintos:", distintas)
print("la del ejemplo:", sum(1 for _ in ciclos_hamiltonianos(V, A)),
      "ciclos, predichos", cuenta_predicha(phi, 3))
```

En las 24 fórmulas al azar los dos números coinciden, y en la del ejemplo son 16. El
experimento propone un enunciado más fuerte que "satisfacible si y solo si tiene
ciclo": una correspondencia exacta entre ciclos y pares (asignación, literal elegido
por cláusula). No prueba nada para fórmulas más grandes, y en particular no mira
ninguna fórmula insatisfacible con más de dos cláusulas, que es donde se rompen las
reducciones mal hechas. Eso lo decide la demostración.

## 5. La demostración

**Teorema 1.** 3-SAT $\le_p$ CICLO-HAMILTONIANO-DIRIGIDO, y por lo tanto ciclo
hamiltoniano dirigido es NP-completo.

*Demostración.* Ya vimos la pertenencia a NP en la §1 y el costo de la construcción en
la §3. Faltan las dos direcciones.

*Si la fórmula se cumple con $a$*, recorre la fila $i$ de izquierda a derecha si $a$
hace verdadera a $x_i$, y de derecha a izquierda si no. Las filas se encadenan por los
arcos entre extremos, de $s$ a la primera fila y de la última a $t$, y $t \to s$ cierra
el ciclo. Para cada cláusula $j$, elige un literal verdadero, de la variable $x_i$. Si
es $x_i$, la fila $i$ va de izquierda a derecha y pasa de $v_{i,3j}$ a $v_{i,3j+1}$:
cambia ese arco por $v_{i,3j} \to c_j \to v_{i,3j+1}$. Si es $\lnot x_i$, la fila va
de derecha a izquierda y el desvío es $v_{i,3j+1} \to c_j \to v_{i,3j}$. Cada cláusula
usa su propio par de posiciones, así que los desvíos no chocan, y el ciclo resultante
pasa una vez por cada vértice.

La otra dirección necesita un lema, y es el paso que todo el mundo se salta. Sin él,
nada impide que el ciclo entre a $c_j$ desde una fila y salga hacia otra, y entonces
las filas ya no se recorren enteras.

**Lema 2.** En un ciclo hamiltoniano del grafo construido, si el ciclo llega a $c_j$
desde la fila $i$, sale de $c_j$ hacia el vértice vecino de la misma fila: de
$v_{i,3j}$ a $v_{i,3j+1}$ si $x_i$ está en la cláusula, de $v_{i,3j+1}$ a $v_{i,3j}$
si está $\lnot x_i$.

*Demostración.* Tomemos el caso positivo; el negativo es el mismo con la fila leída al
revés. El ciclo llega por $v_{i,3j} \to c_j$ y supongamos que sale por $c_j \to w$ con
$w \ne v_{i,3j+1}$. Mira $u = v_{i,3j+1}$. Sus arcos de entrada vienen de $v_{i,3j}$,
de $v_{i,3j+2}$ y de $c_j$. El sucesor de $v_{i,3j}$ es $c_j$ y el sucesor de $c_j$ es
$w$, así que el predecesor de $u$ es $v_{i,3j+2}$. Sus arcos de salida van a
$v_{i,3j}$ y a $v_{i,3j+2}$, porque la posición $3j + 1$ no tiene otro arco hacia una
cláusula. No puede volver a su predecesor, porque un ciclo hamiltoniano de más de dos
vértices no tiene ciclos de largo 2, así que el sucesor de $u$ es $v_{i,3j}$. Ahora
$v_{i,3j}$ tiene predecesor $u$ y sucesor $c_j$, y no le queda nada para nadie más.

Aquí entra el vértice de separación $g = v_{i,3j-1}$. Sus únicos vecinos son
$v_{i,3j-2}$ y $v_{i,3j}$, porque las posiciones de separación no tienen arcos a
cláusulas. Con $v_{i,3j}$ ocupado, el predecesor y el sucesor de $g$ tendrían que ser
los dos $v_{i,3j-2}$, otro ciclo de largo 2. Contradicción. En el caso negativo, el
mismo argumento ocupa $v_{i,3j+1}$ y deja sin salida a $g = v_{i,3j+2}$. $\square$

*Si el grafo tiene un ciclo hamiltoniano*, el lema dice que cada visita a una cláusula
es un desvío $v \to c_j \to v'$ entre dos vértices consecutivos de una fila. Cambia
cada desvío por el arco $v \to v'$, que existe porque las filas tienen arcos en los dos
sentidos. Queda un ciclo hamiltoniano del grafo sin vértices de cláusula, y en ese
grafo los vértices interiores de una fila solo tienen vecinos en su fila. Si el ciclo
va de $v_{i,1}$ a $v_{i,2}$, el sucesor de $v_{i,2}$ no puede ser $v_{i,1}$, así que
es $v_{i,3}$, y así hasta $v_{i,b}$. Si va de $v_{i,2}$ a $v_{i,1}$, la fila se
recorre entera al revés. Cada fila se recorre entera en un sentido, y define $a$: $x_i$
verdadera si la fila $i$ va de izquierda a derecha.

Cada $c_j$ fue visitada por un desvío desde alguna fila $i$. Si el desvío es
$v_{i,3j} \to c_j \to v_{i,3j+1}$, la fila $i$ va de izquierda a derecha, $x_i$ es
verdadera y es un literal de la cláusula $j$. Si es $v_{i,3j+1} \to c_j \to v_{i,3j}$,
la fila va al revés, $x_i$ es falsa, y $\lnot x_i$, que es el literal de la cláusula,
es verdadero. Toda cláusula se cumple. $\square$

Las dos direcciones juntas dan más que el teorema. La primera construye un ciclo por
cada asignación que cumple y cada elección de un literal verdadero por cláusula, y la
segunda muestra que no hay otros: es la correspondencia que el experimento contó. En
la versión sin vértices de separación, con filas de $2k + 2$ vértices, el conteo de la
§4 deja de coincidir: para una sola cláusula aparecen ciclos que entran a $c_1$ desde
una fila y salen a otra. El lema es lo que los excluye.

## 6. Del grafo dirigido al no dirigido

En un grafo no dirigido ya no hay sentidos que obliguen a nada. La reducción de Karp
(1972, p. 98) reemplaza cada vértice $v$ por un camino de tres vértices,
$v_0 - v_1 - v_2$, y cada arco $u \to v$ por una arista $u_2 - v_0$. La entrada es el
extremo $0$ y la salida es el extremo $2$.

**Teorema 3.** CICLO-HAMILTONIANO-DIRIGIDO $\le_p$ CICLO-HAMILTONIANO, y el segundo es
NP-completo.

*Demostración.* El grafo nuevo tiene $3n$ vértices y $2n + m$ aristas, para $n$
vértices y $m$ arcos. Un ciclo dirigido $w^1, w^2, \dots, w^n$ da el ciclo no
dirigido que recorre $w^1_0, w^1_1, w^1_2, w^2_0, \dots, w^n_2$ y vuelve a $w^1_0$,
porque cada arco $w^r \to w^{r+1}$ es la arista $w^r_2 - w^{r+1}_0$.

Al revés, sea $H$ un ciclo hamiltoniano del grafo nuevo. El vértice $v_1$ tiene grado
2, así que $H$ usa sus dos aristas, $v_0 - v_1$ y $v_1 - v_2$. Elige el sentido de
recorrido de $H$ en que algún vértice $u$ se pasa como $u_0, u_1, u_2$. Después de
$u_2$, $H$ sigue por una arista que no es $u_1 - u_2$. Las otras aristas de $u_2$ van a
vértices $w_0$ con $u \to w$ un arco. Así que $H$ llega a $w_0$, y como $w_1$ va pegado
a $w_0$ en $H$, sigue por $w_1$ y $w_2$. Por inducción, $H$ pasa por los tríos en el
orden $0, 1, 2$, y cada paso de un trío al siguiente es un arco del grafo original. La
sucesión de tríos es un ciclo hamiltoniano dirigido. $\square$

El vértice del medio es lo que fuerza el sentido. Sin él, con $v_0 - v_1$ como única
pieza por vértice, el argumento de grado no sale, y el ejercicio 2 te pide la entrada
que lo rompe. Comprobamos el teorema con la programación dinámica sobre subconjuntos
del capítulo 11, §9, en versión de decisión: `alcanza[S]` es el conjunto de vértices
donde puede terminar un camino que sale del vértice 0 y visita exactamente $S$.

```{python continue}
def tiene_ciclo(N, vecinos):
    """vecinos[v]: máscara de los w con arco v -> w. ¿Hay ciclo hamiltoniano?"""
    alcanza = [0] * (1 << N)
    alcanza[1] = 1                                   # el camino {0} termina en 0
    for S in range(1, 1 << N):
        r = alcanza[S]
        if not (S & 1) or not r:
            continue
        for v in range(N):
            if r >> v & 1:
                libres = vecinos[v] & ~S
                while libres:
                    w = libres & -libres
                    libres ^= w
                    alcanza[S | w] |= w
    final = alcanza[(1 << N) - 1]
    return any(final >> v & 1 and vecinos[v] & 1 for v in range(N))

def triplica(n, arcos):
    vecinos = [0] * (3 * n)
    def arista(a, b):
        vecinos[a] |= 1 << b
        vecinos[b] |= 1 << a
    for v in range(n):
        arista(3 * v, 3 * v + 1)
        arista(3 * v + 1, 3 * v + 2)
    for u, v in arcos:
        arista(3 * u + 2, 3 * v)
    return 3 * n, vecinos

random.seed(6)
iguales = con_ciclo = 0
for _ in range(150):
    n = random.choice([3, 4])
    arcos = [(u, v) for u in range(n) for v in range(n) if u != v and random.random() < 0.45]
    dirigido = [sum(1 << v for w, v in arcos if w == u) for u in range(n)]
    d = tiene_ciclo(n, dirigido)
    con_ciclo += d
    iguales += d == tiene_ciclo(*triplica(n, arcos))
print(f"150 digrafos, {con_ciclo} con ciclo: misma respuesta en {iguales}")
```

En los 150 digrafos al azar, 24 con ciclo hamiltoniano y el resto sin él, el grafo
triplicado da la misma respuesta. Que haya digrafos de las dos clases importa: con
solo instancias sí, la mitad difícil de la demostración no se estaría probando.

## 7. TSP

La versión de decisión del problema del viajante, que el capítulo 11, §9 resolvió en
su versión de optimización con $O(2^n n^2)$ operaciones, es esta. Dadas $n$
ciudades, una distancia entera $d(u, v)$ para cada par y un presupuesto $B$, ¿hay un
recorrido que visita cada ciudad una vez, vuelve al inicio y cuesta a lo sumo $B$?
Está en NP, con el recorrido como certificado.

**Teorema 4.** CICLO-HAMILTONIANO $\le_p$ TSP, y TSP es NP-completo.

*Demostración.* Dado $G = (V, E)$ con $n$ vértices, pon una ciudad por vértice,
$d(u, v) = 1$ si $\{u, v\} \in E$ y $d(u, v) = 2$ si no, y $B = n$. Son $\binom{n}{2}$
distancias, tiempo $O(n^2)$. Un recorrido tiene exactamente $n$ tramos, y cada uno
cuesta al menos 1, así que cuesta al menos $n$, con igualdad si y solo si todos sus
tramos cuestan 1. Si $G$ tiene un ciclo hamiltoniano, ese ciclo es un recorrido de
costo $n$. Si hay un recorrido de costo a lo sumo $n$, todos sus tramos cuestan 1,
son aristas de $G$, y el recorrido es un ciclo hamiltoniano de $G$. $\square$

Las distancias 1 y 2 cumplen la desigualdad triangular, porque $d(u, w) \le 2 \le
d(u, v) + d(v, w)$. Así que la reducción demuestra algo más: TSP sigue siendo
NP-completo cuando las distancias son métricas. El capítulo 22 usa la misma reducción
con otros pesos para un resultado distinto, sobre aproximación.

```{python continue}
def held_karp(d):
    n = len(d)
    g = {(1, 0): 0}
    for S in range(1, 1 << n):
        if not S & 1:
            continue
        for v in range(n):
            if (S, v) not in g:
                continue
            for w in range(n):
                if not S >> w & 1:
                    T = S | 1 << w
                    g[T, w] = min(g.get((T, w), math.inf), g[S, v] + d[v][w])
    todo = (1 << n) - 1
    return min(g[todo, v] + d[v][0] for v in range(1, n))

random.seed(7)
bien = 0
for _ in range(100):
    n = random.randint(4, 7)
    E = {(u, v) for u, v in itertools.combinations(range(n), 2) if random.random() < 0.5}
    vecinos = [sum(1 << w for w in range(n) if (min(v, w), max(v, w)) in E)
               for v in range(n)]
    d = [[0 if u == v else (1 if (min(u, v), max(u, v)) in E else 2) for v in range(n)]
         for u in range(n)]
    bien += (held_karp(d) <= n) == tiene_ciclo(n, vecinos)
print("100 grafos: recorrido de costo ≤ n exactamente cuando hay ciclo:", bien)
```

## 8. Suma de subconjuntos: una columna por restricción

Ahora el material es un número. ¿Dónde se esconde una elección en una suma? En qué
números entran. La idea que hace todo posible es leer un número como un vector de
dígitos: si al sumar nunca hay acarreo, la suma de los números es la suma de sus
vectores columna por columna, y cada columna es una restricción independiente.

Pon una columna por variable y una por cláusula. Para la variable $x_i$ hay dos números,
$y_i$ (para el literal $x_i$) y $z_i$ (para $\lnot x_i$), los dos con un 1 en la
columna de $x_i$. La meta $T$ tiene un 1 en esa columna, así que entra exactamente uno
de los dos: es la elección del valor de verdad. Además, $y_i$ tiene un 1 en la columna
de cada cláusula donde aparece $x_i$, y $z_i$ en cada una donde aparece $\lnot x_i$.
Con la asignación elegida, la columna de la cláusula $j$ suma $t_j$, el número de sus
literales verdaderos, entre 0 y 3.

El primer intento es poner meta 1 en la columna de la cláusula. Falla con una
asignación que cumple la cláusula con dos literales verdaderos, porque la columna suma
2. Lo que queremos es "al menos 1", y una suma exacta no sabe decir "al menos". El
arreglo es rellenar: dos números de **holgura** por cláusula, $g_j$ con un 1 y $h_j$
con un 2 en la columna de la cláusula, y meta 4. Con $t_j = 1$ entran los dos, con
$t_j = 2$ entra $h_j$, con $t_j = 3$ entra $g_j$. Con $t_j = 0$, las holguras suman a
lo sumo $1 + 2 = 3$ y no llegan.

```{python continue}
def a_suma(clausulas, n, base=10, meta_clausula=4):
    """3-SAT -> suma de subconjuntos. Devuelve las filas (nombre, dígitos), los
    números y la meta. Columnas: x_1..x_n, después C_1..C_k."""
    k = len(clausulas)
    filas = []
    for i in range(1, n + 1):
        for nombre, l in ((f"y{i}", i), (f"z{i}", -i)):
            filas.append((nombre, [int(c == i - 1) for c in range(n)] +
                                  [int(l in cl) for cl in clausulas]))
    for j in range(k):
        for nombre, h in ((f"g{j + 1}", 1), (f"h{j + 1}", 2)):
            filas.append((nombre, [0] * n + [h * (c == j) for c in range(k)]))
    meta = [1] * n + [meta_clausula] * k
    valor = lambda digitos: sum(d * base ** e for e, d in enumerate(reversed(digitos)))
    return filas, [valor(d) for _, d in filas], valor(meta), meta

filas, numeros, T, meta = a_suma(phi, 3)
for (nombre, digitos), a in zip(filas, numeros):
    print(f"{nombre}: {a:>6}")
print(f"T:  {T:>6}")
```

Para la fórmula de la §3 salen diez números de cinco dígitos y la meta 11 144. La
asignación que leímos del ciclo, con las tres variables verdaderas, elige $y_1$, $y_2$
e $y_3$. Las cláusulas quedan con $t_1 = 2$ y $t_2 = 2$, así que entran $h_1$ y $h_2$.

```{python continue}
elegidas = [f"y{i}" if valor[i] else f"z{i}" for i in range(1, 4)]
columnas = [sum(d[3 + j] for nombre, d in filas if nombre in elegidas) for j in range(2)]
elegidas += [f"{'gh'[e]}{j + 1}" for j, t in enumerate(columnas) for e in range(2)
             if (4 - t) >> e & 1]
suma = sum(a for (nombre, _), a in zip(filas, numeros) if nombre in elegidas)
print("elegidas:", elegidas, " suma:", suma, " T:", T)
```

Las holguras se eligen escribiendo $4 - t_j$ en binario: el bit 1 es $g_j$ y el bit 2
es $h_j$. La @fig-rn-tabla muestra la tabla con esas cinco filas marcadas.

```{python continue echo=false output=asis}
print(F19.tabla(3, 2, filas, meta, elegidas, ident="rn-tabla",
      pie="La tabla de la reducción para (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₃), en base "
          "10. Las filas marcadas son el subconjunto que eligió el código para la "
          "asignación con las tres variables verdaderas, y suman T = 11144. Ninguna "
          "columna pasa de 6, así que no hay acarreos."))
```

## 9. La demostración

**Teorema 5.** 3-SAT $\le_p$ SUMA-DE-SUBCONJUNTOS, y suma de subconjuntos es
NP-completo.

*Demostración.* La pertenencia a NP está en la §1. La construcción produce $2n + 2k$
números de $n + k$ dígitos decimales cada uno, más la meta: $O((n + k)^2)$ dígitos,
que se escriben en ese tiempo. Es polinomial en el tamaño de la fórmula.

El paso que todo el mundo se salta es este: **en la suma de cualquier subconjunto no
hay acarreos**. En una columna de variable solo hay dos unos, de $y_i$ y $z_i$. En una
columna de cláusula hay tres unos, de los tres literales, y las holguras 1 y 2: a lo
sumo $3 + 1 + 2 = 6 < 10$. Así que la suma de un subconjunto tiene, en cada columna,
exactamente la suma de esa columna, y es igual a $T$ si y solo si cada columna suma
el dígito de $T$.

*Si la fórmula se cumple con $a$*, elige $y_i$ si $x_i$ es verdadera y $z_i$ si no.
Cada columna de variable suma 1. La columna de la cláusula $j$ suma $t_j \in
\{1, 2, 3\}$, y las holguras completan $4 - t_j \in \{1, 2, 3\}$ como en la §8. La suma
es $T$.

*Si un subconjunto suma $T$*, sin acarreos cada columna de variable suma 1, así que
contiene exactamente uno de $y_i$, $z_i$. Define $a$ por eso: $x_i$ verdadera si entró
$y_i$. La columna de la cláusula $j$ suma 4, y es $t_j$ más lo que aportan las
holguras elegidas, que es a lo sumo 3. Entonces $t_j \ge 1$: la cláusula tiene un
literal verdadero con $a$. $\square$

Mira el tamaño de los números. La meta tiene $n + k$ dígitos, así que vale del orden
de $10^{n + k}$: exponencial en el tamaño de la fórmula, aunque se escribe con
$O(n + k)$ dígitos. El capítulo 16, ejercicio 10, pide reconciliar esto con la
tabla de $O(mT)$ que resuelve la suma de subconjuntos.

El experimento cuenta, como en la §4, algo más fino que la respuesta: cuántos
subconjuntos suman $T$, frente a cuántas asignaciones cumplen la fórmula. Para contar
subconjuntos de hasta 26 números sin probar los $2^{26}$, partimos la lista en dos
mitades, contamos las sumas de cada mitad y emparejamos.

```{python continue}
def cuenta_subconjuntos(numeros, T):
    def sumas(xs):
        c = Counter({0: 1})
        for a in xs:
            nuevo = Counter()
            for s, veces in c.items():
                nuevo[s] += veces
                nuevo[s + a] += veces
            c = nuevo
        return c
    mitad = len(numeros) // 2
    izq, der = sumas(numeros[:mitad]), sumas(numeros[mitad:])
    return sum(veces * der.get(T - s, 0) for s, veces in izq.items())

def asignaciones_que_cumplen(clausulas, n):
    return sum(all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clausulas)
               for bits in itertools.product([False, True], repeat=n))

random.seed(9)
distintas = 0
for _ in range(40):
    n = random.choice([3, 4])
    f = formula_al_azar(n, random.randint(1, 5))
    _, numeros_f, T_f, _ = a_suma(f, n)
    distintas += cuenta_subconjuntos(numeros_f, T_f) != asignaciones_que_cumplen(f, n)
print("40 fórmulas: conteos distintos:", distintas)
print("la del ejemplo:", cuenta_subconjuntos(numeros, T), "subconjuntos,",
      asignaciones_que_cumplen(phi, 3), "asignaciones")
```

En las 40 fórmulas los dos números coinciden, y en la del ejemplo son 6 y 6: a cada
asignación que cumple le corresponde exactamente un subconjunto. Por qué las holguras
no dan más de una manera de completar es el ejercicio 5.

## 10. El error plantado

Las holguras admiten otra elección que también es correcta: dos holguras de 1 por
cláusula y meta 3, porque con $t_j = 0$ suman 2 y no llegan. Mezclar las dos es fácil:
holguras 1 y 2 con meta 3. El código cambia en un número.

Probémosla como se prueba casi siempre una reducción: con fórmulas que tienen solución,
construidas eligiendo primero una asignación y después solo cláusulas que esa
asignación cumple.

```{python continue}
def con_asignacion_plantada(n, k):
    a = {i: random.random() < 0.5 for i in range(1, n + 1)}
    f = []
    while len(f) < k:
        c = formula_al_azar(n, 1)[0]
        if any(a[abs(l)] == (l > 0) for l in c):
            f.append(c)
    return f

def responde(f, n, meta_clausula):
    _, numeros_f, T_f, _ = a_suma(f, n, meta_clausula=meta_clausula)
    return cuenta_subconjuntos(numeros_f, T_f) > 0

random.seed(10)
plantadas = [con_asignacion_plantada(4, random.randint(2, 6)) for _ in range(30)]
for meta_c in (4, 3):
    fallos = sum(not responde(f, 4, meta_c) for f in plantadas)
    print(f"meta {meta_c}: 30 fórmulas con solución plantada, fallos: {fallos}")
```

Ningún fallo con ninguna de las dos. Las instancias que distinguen son las fórmulas
**insatisfacibles**. Cada cláusula de tres variables hace falsa un octavo de las asignaciones, así que una
fórmula insatisfacible tiene al menos ocho cláusulas. Las ocho cláusulas sobre tres
variables, una por cada combinación de signos, lo son: cada asignación hace falsa exactamente la cláusula
que tiene todos los signos al revés. Construimos una batería con esas ocho cláusulas
sobre tres variables elegidas al azar entre cuatro, más algunas cláusulas al azar, que
no pueden volverla satisfacible.

```{python continue}
def insatisfacible(n, extra):
    x = random.sample(range(1, n + 1), 3)
    f = [[s1 * x[0], s2 * x[1], s3 * x[2]]
         for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
    f += formula_al_azar(n, extra)
    random.shuffle(f)
    return f

random.seed(11)
insat = [insatisfacible(4, random.randint(0, 2)) for _ in range(10)]
assert all(asignaciones_que_cumplen(f, 4) == 0 for f in insat)
for meta_c in (4, 3):
    fallos = sum(responde(f, 4, meta_c) for f in insat)
    print(f"meta {meta_c}: 10 fórmulas insatisfacibles, fallos: {fallos}")
```

Con meta 3 falla en las diez. De hecho falla en toda fórmula: con meta 3 cualquier
asignación sirve, porque una cláusula con $t_j = 0$ se completa con las dos holguras,
$0 + 1 + 2 = 3$. La reducción manda toda fórmula a una instancia con solución.

La demostración lo anunciaba en la última línea: "lo que aportan las holguras es a lo
sumo 3", y de ahí $t_j \ge 1$ porque la meta es 4. Esa línea compara la suma de las
holguras con la meta, y con meta 3 la comparación ya no da nada. Es la dirección "no ⇒
no" otra vez, como en el capítulo 16, §11 y el capítulo 17, §9. Una batería de
instancias con solución plantada no puede encontrar este error, por grande que sea,
porque la dirección "sí ⇒ sí" de la versión rota es verdadera.

## 11. Mochila

La versión de decisión de la mochila es esta. Dados $m$ objetos con pesos $w_i$ y
valores $v_i$ enteros positivos, una capacidad $W$ y una meta $V$, ¿hay un subconjunto
de peso total a lo sumo $W$ y valor total al menos $V$? Está en NP: el certificado es
el subconjunto, y se comprueba con dos sumas.

**Teorema 6.** SUMA-DE-SUBCONJUNTOS $\le_p$ MOCHILA, y mochila es NP-completa.

*Demostración.* Dados $a_1, \dots, a_m$ y $T$, pon $w_i = v_i = a_i$ y $W = V = T$.
Copiar los números es lineal. Para un subconjunto $S$, las dos condiciones dicen
$\sum_{i \in S} a_i \le T$ y $\sum_{i \in S} a_i \ge T$, que juntas dicen
$\sum_{i \in S} a_i = T$. Así que el mismo $S$ es solución de las dos instancias.
$\square$

Es la reducción más corta del capítulo, y es porque suma de subconjuntos ya es un caso
particular de la mochila, el de objetos cuyo valor es igual a su peso. El problema que
Karp (1972, p. 95, problema 18) llamó KNAPSACK es exactamente la suma de subconjuntos:
dados $(a_1, \dots, a_r, b)$, ¿tiene $\sum a_j x_j = b$ una solución 0-1?

La tabla de $O(mW)$ de Estructuras de Datos resuelve la mochila, y no contradice el
teorema: el capítulo 1, §8 la llamó pseudopolinomial. El capítulo 23 vuelve sobre esto
para distinguir problemas como la mochila, difíciles solo cuando los números son
enormes, de otros que siguen siendo difíciles con números chicos.

## 12. Lo que queda demostrado

Con el capítulo 17 como raíz, la Parte III demostró que estos once problemas son
NP-completos: SAT, 3-SAT, conjunto independiente, clique, vertex cover, set cover,
3-coloración, ciclo hamiltoniano (dirigido y no dirigido), TSP, suma de subconjuntos y
mochila.

```{python continue}
reducciones = [
    ("SAT", "3-SAT", 17), ("3-SAT", "independiente", 18),
    ("independiente", "clique", 16), ("independiente", "vertex cover", 16),
    ("vertex cover", "set cover", 18), ("3-SAT", "3-coloración", 18),
    ("3-SAT", "ciclo ham. dirigido", 19),
    ("ciclo ham. dirigido", "ciclo ham. no dirigido", 19),
    ("ciclo ham. no dirigido", "TSP", 19),
    ("3-SAT", "suma de subconjuntos", 19), ("suma de subconjuntos", "mochila", 19),
]
alcanzados = {"SAT"}
for u, v, _ in reducciones:          # están en orden: cada origen ya está demostrado
    assert u in alcanzados
    alcanzados.add(v)
print(len(alcanzados), "problemas NP-completos con", len(reducciones), "reducciones")
```

El código comprueba que la lista está bien ordenada: cada reducción parte de un
problema ya demostrado. Son 12 nombres porque el ciclo hamiltoniano cuenta dos veces,
dirigido y no dirigido. La @fig-rn-mapa lo dibuja.

```{python continue echo=false output=asis}
print(F19.mapa(reducciones, ident="rn-mapa",
      pie="Las reducciones de la Parte III, con el capítulo de cada una. Todas parten "
          "de SAT, que el capítulo 17 demostró NP-completo desde la definición. En "
          "naranja, las de este capítulo."))
```

Las rutas no son únicas. Karp (1972, figura 1, p. 96) llegó al ciclo hamiltoniano
dirigido desde vertex cover (NODE COVER) y a KNAPSACK desde el problema de cubrimiento
exacto, y de KNAPSACK a PARTITION, que es el ejercicio 6. Elegimos partir de 3-SAT
porque la elección binaria de una variable se ve directamente en la construcción.

## 13. La regla {#reducciones-numeros-13-la-regla}

Los dos materiales del capítulo dejaron el mismo peligro. En el grafo, un ciclo podía
entrar a una cláusula desde una fila y salir hacia otra; en los números, una columna
podía pasarle un acarreo a la siguiente. Y en el error plantado, las holguras podían
llenar ellas solas el hueco de una cláusula falsa. La regla es:

**Una reducción es correcta cuando sus piezas solo se comunican por donde la
demostración dice.** Los vértices de separación cortan el paso de una fila a otra, la
base 10 corta el acarreo, y la meta 4 deja a las holguras un punto por debajo de lo
que hace falta. Cada una de esas piezas aparece en la demostración en la dirección "no
⇒ no", y por eso se comprueba con instancias no: es la única dirección en que una pieza
olvidada se nota.

## Resumen {#reducciones-numeros-resumen}

- Ciclo hamiltoniano y suma de subconjuntos están en NP: el certificado es el orden o
  el subconjunto.
- En un ciclo, el valor de una variable es el sentido en que se recorre su fila. Una
  cláusula es un vértice al que solo se llega por un desvío en el sentido de un literal
  verdadero.
- Filas de $3k + 3$ vértices con un vértice de separación entre pares. El lema 2 usa
  esos vértices para impedir que un ciclo entre a una cláusula por una fila y salga por
  otra.
- La reducción a ciclo hamiltoniano da un ciclo por cada asignación que cumple y cada
  elección de un literal verdadero por cláusula, y ninguno más.
- Dirigido a no dirigido con tres vértices por vértice (Karp, 1972). El del medio tiene
  grado 2 y fuerza el sentido.
- TSP de decisión desde ciclo hamiltoniano con distancias 1 y 2 y presupuesto $n$. Las
  distancias son métricas, así que TSP métrico también es NP-completo.
- Suma de subconjuntos desde 3-SAT: una columna por variable con meta 1 y una por
  cláusula con meta 4 y holguras 1 y 2. Cada columna suma a lo sumo 6, así que en base
  10 no hay acarreos.
- La meta tiene $n + k$ dígitos y vale del orden de $10^{n+k}$. Mochila contiene a suma
  de subconjuntos con $w_i = v_i = a_i$.
- Con holguras 1 y 2 y meta 3, toda fórmula tiene solución. Las baterías con solución
  plantada no lo ven.
- Once problemas NP-completos, todos desde SAT. Una reducción es correcta cuando sus
  piezas solo se comunican por donde la demostración dice.

## Ejercicios {#reducciones-numeros-ejercicios}

1. Construye a mano el grafo de la §3 para $(x_1 \lor x_2 \lor \lnot x_3) \land
   (\lnot x_1 \lor \lnot x_2 \lor x_3)$: cuántos vértices y arcos tiene, y cuáles
   son los arcos de cada vértice de cláusula. Para la asignación con $x_1$ verdadera y
   $x_2$, $x_3$ falsas, escribe todos los ciclos hamiltonianos que le
   corresponden, y comprueba su número con la fórmula de la §4.

2. Cambia la reducción de la §6 para que use dos vértices por vértice, $v_0 - v_1$, y
   la arista $u_1 - v_0$ por cada arco $u \to v$. Encuentra un grafo dirigido sin ciclo
   hamiltoniano cuyo grafo construido sí lo tenga. Di en qué paso de la demostración
   del teorema 3 se usa el vértice del medio.

3. Escribe la tabla de la §8 para $(x_1 \lor \lnot x_2 \lor \lnot x_3) \land (x_2 \lor
   x_3 \lor \lnot x_4) \land (\lnot x_1 \lor x_3 \lor x_4)$ y su meta $T$. Encuentra
   una asignación que cumpla la fórmula y el subconjunto que le corresponde, con las
   holguras de cada cláusula.

4. La demostración del teorema 5 usa que en base 10 no hay acarreos. ¿Cuál es la base
   más chica en la que, con las mismas holguras y la misma meta, ningún subconjunto
   produce acarreos? Después, demuestra que la reducción sigue siendo correcta en
   algunas bases donde sí puede haber acarreos, y encuentra la más chica en que lo es.
   Pista: mira la columna de más a la derecha primero.

5. Demuestra que la reducción de la §8 es **parsimoniosa**: el número de subconjuntos
   que suman $T$ es igual al número de asignaciones que cumplen la fórmula. ¿Sigue
   siéndolo con dos holguras de 1 y meta 3?

6. PARTICIÓN pregunta si unos enteros positivos se pueden repartir en dos grupos de
   igual suma. Demuestra que es NP-completo con una reducción desde suma de
   subconjuntos que agrega un número. Después, EMPAQUETAMIENTO (versión de decisión)
   pregunta si unos objetos de tamaños $s_1, \dots, s_m$ caben en $q$ cajas de
   capacidad $C$. Demuestra que es NP-completo desde partición.

7. CAMINO-MÁS-LARGO pregunta si un grafo no dirigido con pesos positivos tiene un
   camino simple de peso al menos $L$. Demuestra que es NP-completo. Puedes usar que
   camino hamiltoniano es NP-completo (capítulo 16, ejercicio 6, más el teorema 3). ¿Por
   qué no contradice que el camino más **corto** se calcule en tiempo polinomial?

8. Queremos reducir SAT a suma de subconjuntos sin pasar por 3-SAT, con cláusulas de
   cualquier largo. La columna de una cláusula de $m$ literales puede sumar de 0 a $m$
   por los literales. Diseña las holguras de esa columna y su meta para que la
   reducción sea correcta, con la menor cantidad de números de holgura que puedas, y
   di qué base hace falta para que no haya acarreos. Demuestra las dos direcciones.

9. ★ Supón que existe una reducción polinomial de 3-SAT a suma de subconjuntos en la
   que la meta $T$ de la instancia construida es siempre a lo sumo $p(|\varphi|)$, con
   $p$ un polinomio. Demuestra que entonces $P = NP$. ¿Qué dice esto de cualquier
   reducción de 3-SAT a suma de subconjuntos, si $P \ne NP$?

10. Implementa la composición 3-SAT → ciclo hamiltoniano dirigido → no dirigido → TSP.
    Mide cuántas ciudades y distancias produce para $n$ variables y $k$ cláusulas, y
    escribe la fórmula exacta. Para fórmulas con $n = 3$ y $k = 1$, ¿puede la tabla de
    Held-Karp del capítulo 11 decidir la instancia de TSP en tu máquina? Estima cuánta
    memoria haría falta.

11. Escribe los números de la §8 en base 2 en lugar de base 10, con las mismas
    holguras y la misma meta. Encuentra una fórmula insatisfacible cuya instancia tenga
    un subconjunto que suma $T$, y muestra el subconjunto. Busca primero entre las
    fórmulas de la §10.
