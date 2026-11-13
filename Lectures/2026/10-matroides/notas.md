# Matroides {#chap-matroides}

El capítulo 9 demostró dos golosos, y cada uno pidió su propio intercambio: dos tareas
vecinas en el retraso máximo, una planificación entera reconstruida en la caché. Este
capítulo pregunta cuándo esa demostración se puede hacer una sola vez para toda una
familia de problemas, y la respuesta es exacta. El goloso que ordena los elementos por
peso y agrega cada uno si el conjunto sigue siendo factible es óptimo **para cualquier
función de peso** si y solo si los conjuntos factibles forman un **matroide**. El
intercambio, que en el capítulo 9 había que inventar, pasa a ser un axioma.

```{python echo=false output=asis}
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_10.py
import figuras_10 as F
```

## 1. Una demostración para muchos golosos

Kruskal, que ya viste en Estructuras de Datos, recorre las aristas de la más barata a la
más cara y agrega cada una si no cierra un ciclo. Cambia "arista" por "elemento" y "no
cierra un ciclo" por "el conjunto sigue siendo factible", y tienes un algoritmo que no
sabe nada de grafos. Recibe un conjunto $E$, un peso $w(e) \ge 0$ para cada elemento y
un **oráculo** que responde si un conjunto es factible. Lo factible lo llamaremos
**independiente**, por razones que la §4 explica.

```{python continue}
def goloso(E, w, independiente):
    """Recorre E de mayor a menor peso y agrega lo que deja el conjunto independiente."""
    S = []
    for e in sorted(E, key=lambda e: -w[e]):
        if independiente(S + [e]):
            S.append(e)
    return S

def peso(S, w):
    return sum(w[e] for e in S)

def optimo(E, w, independiente):
    """Oráculo de fuerza bruta: el mayor peso entre todos los conjuntos independientes."""
    return max(peso(C, w) for r in range(len(E) + 1)
               for C in itertools.combinations(E, r) if independiente(list(C)))
```

El costo es ordenar más una consulta al oráculo por elemento: $O(n \log n + n\,T)$
con $n = |E|$, si el oráculo tarda $T$. Toda la dificultad está en otra parte: ¿para qué
oráculos el resultado es óptimo?

## 2. El experimento: bosques y emparejamientos del mismo grafo

Tomemos un grafo chico, el **diamante**: cuatro vértices, el ciclo $a, b, c, d$ y la
diagonal $ac$. Sobre sus cinco aristas hay dos nociones naturales de "factible". Un
conjunto de aristas es un **bosque** si no tiene ciclos, y es un **emparejamiento** si
no tiene dos aristas con un vértice en común. Corremos el goloso con todas las
funciones de peso que dan a cada arista un valor en $\{1, 2, 3\}$, que son $3^5$, y lo
comparamos con la fuerza bruta.

```{python continue}
def es_bosque(aristas):
    padre = {}
    def raiz(x):
        while padre.get(x, x) != x:
            x = padre[x]
        return x
    for u, v in aristas:
        a, b = raiz(u), raiz(v)
        if a == b:
            return False
        padre[a] = b
    return True

def es_emparejamiento(aristas):
    extremos = [x for e in aristas for x in e]
    return len(extremos) == len(set(extremos))

D = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "c")]
primer_fallo = {}
for nombre, ind in [("bosques", es_bosque), ("emparejamientos", es_emparejamiento)]:
    fallos = 0
    for valores in itertools.product([1, 2, 3], repeat=len(D)):
        w = dict(zip(D, valores))
        if peso(goloso(D, w, ind), w) < optimo(D, w, ind):
            fallos += 1
            primer_fallo.setdefault(nombre, w)
    print(f"{nombre:16} el goloso falla en {fallos} de {3 ** len(D)} funciones de peso")
w_mal = primer_fallo["emparejamientos"]
print("primer fallo:", [w_mal[e] for e in D],
      " goloso:", peso(goloso(D, w_mal, es_emparejamiento), w_mal),
      " óptimo:", optimo(D, w_mal, es_emparejamiento))
```

Sobre los bosques el goloso no falla nunca. Sobre los emparejamientos falla en 27 de
las 243 funciones. El primer fallo da pesos 1, 2, 1, 2 a las aristas del ciclo y 3 a la
diagonal. El goloso toma primero la diagonal, que toca $a$ y $c$. Cada arista del ciclo
tiene uno de esos dos vértices como extremo, así que no puede agregar ninguna y se queda
en 3. Las dos aristas opuestas de peso 2 suman 4
(@fig-matroides-diamante).

```{python continue echo=false output=asis}
pos_d = {"a": (0, 0), "b": (100, 0), "c": (100, 100), "d": (0, 100)}
print(F.diamante(pos_d, D, w_mal, goloso(D, w_mal, es_emparejamiento),
                 [("b", "c"), ("d", "a")],
                 pie="El diamante con los pesos del primer fallo. El goloso sobre "
                     "emparejamientos toma la diagonal de peso 3 y ya no puede agregar "
                     "ninguna arista del ciclo. Las dos aristas opuestas de peso 2 suman 4."))
```

Mismo grafo, mismo algoritmo, mismos pesos. Lo que cambia es la familia de conjuntos
factibles, así que la respuesta a la pregunta de la §1 tiene que ser una propiedad de
la familia.

## 3. Sistemas de independencia y matroides

Un **sistema de independencia** es un par $(E, \mathcal I)$, con $E$ finito y
$\mathcal I$ una familia de subconjuntos de $E$, los **independientes**, que cumple:

- **(I1)** $\emptyset \in \mathcal I$.
- **(I2) Herencia.** Si $B \in \mathcal I$ y $A \subseteq B$, entonces $A \in \mathcal I$.

Los bosques y los emparejamientos lo cumplen: quitar aristas no crea ciclos ni vértices
compartidos. El goloso solo tiene sentido sobre un sistema así, porque construye el
conjunto de a un elemento y necesita que los prefijos de un factible sean factibles.

Un **matroide** es un sistema de independencia que además cumple:

- **(I3) Intercambio.** Si $A, B \in \mathcal I$ y $|A| < |B|$, existe $e \in B \setminus A$
  tal que $A \cup \{e\} \in \mathcal I$.

Dicho en palabras: un independiente chico siempre se puede agrandar con algún elemento
de uno más grande. Los emparejamientos del diamante no lo cumplen, y el par que lo
rompe es el de la figura: $A = \{ac\}$ y $B = \{bc, da\}$. Las dos aristas de $B$ tocan
un extremo de la diagonal, así que ninguna se puede agregar a $A$.

Una **base** es un independiente maximal, que no se puede agrandar. El ejercicio 3
pide demostrar que con (I3) todas las bases tienen el mismo tamaño, el **rango** del
matroide. Ninguna demostración de este capítulo lo usa, y la §5 lo evita a propósito.

## 4. Cuatro familias de matroides

**Uniforme.** Los independientes son los subconjuntos de a lo sumo $k$ elementos. Si
$|A| < |B| \le k$, cualquier $e \in B \setminus A$ sirve, porque $|A \cup \{e\}| \le k$.

**De partición.** $E$ está repartido en clases $E_1, \dots, E_m$ y cada clase tiene un
cupo $c_j$. Un conjunto es independiente si toma a lo sumo $c_j$ elementos de cada
$E_j$. Si $|A| < |B|$, hay una clase donde $B$ tiene más elementos que $A$; ahí $A$
está por debajo del cupo, porque $|A \cap E_j| < |B \cap E_j| \le c_j$, y cualquier
elemento de $B \cap E_j$ que no esté en $A$ sirve.

**Lineal.** $E$ es un conjunto de vectores de un espacio vectorial, y los independientes
son los subconjuntos linealmente independientes. Un vector se puede agregar a $A$
exactamente cuando no está en el espacio generado por $A$. Si $|A| < |B|$ y ningún vector de
$B$ se pudiera agregar a $A$, todos estarían en el espacio generado por $A$, que tiene
dimensión $|A|$. Pero $B$ es independiente y genera un espacio de dimensión $|B| > |A|$
dentro de ese. Hassler Whitney introdujo la palabra matroide en «On the abstract
properties of linear dependence» (*American Journal of Mathematics* 57(3), 1935)
precisamente para quedarse con estas tres propiedades de la independencia lineal y
olvidar los vectores. De ahí el nombre de los independientes.

**Gráfico.** $E$ son las aristas de un grafo con $n$ vértices, y los independientes son
los bosques. La herencia ya la vimos. Para el intercambio hace falta contar componentes:
un bosque con $k$ aristas sobre $n$ vértices tiene exactamente $n - k$ componentes
conexas, porque cada arista de un bosque une dos componentes distintas y las reduce en
una. Si $|A| < |B|$, el bosque $B$ tiene menos componentes que $A$. Si toda arista de
$B$ tuviera los dos extremos en una misma componente de $A$, cada componente de $B$
estaría dentro de una componente de $A$, y $B$ tendría al menos tantas componentes como
$A$. Así que alguna arista de $B$ une dos componentes de $A$, no es de $A$ y no cierra
ningún ciclo: esa sirve.

La demostración garantiza **una** arista, no todas. En la @fig-matroides-intercambio,
el bosque $A$ tiene 4 aristas y dos componentes, una de ellas el vértice 3 solo. De las
aristas de $B$ que no están en $A$, todas menos una caen dentro de la componente grande.

```{python continue}
G6 = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (0, 4), (1, 5)]
A6 = [(0, 1), (1, 2), (1, 4), (2, 5)]
B6 = [(1, 2), (0, 3), (4, 5), (0, 4), (1, 5)]
assert es_bosque(A6) and es_bosque(B6) and len(A6) < len(B6)
fuera = [e for e in B6 if e not in A6]
sirven = [e for e in fuera if es_bosque(A6 + [e])]
print("aristas de B fuera de A:", fuera)
print("las que se pueden agregar a A:", sirven)
```

```{python continue echo=false output=asis}
comp = {}
for v in range(6):                      # componentes de A6, para colorear
    comp.setdefault(v, v)
cambio = True
while cambio:
    cambio = False
    for u, v in A6:
        m = min(comp[u], comp[v])
        if comp[u] != m or comp[v] != m:
            comp[u] = comp[v] = m
            cambio = True
numero = {r: i for i, r in enumerate(sorted(set(comp.values())))}
pos6 = {0: (0, 0), 1: (80, 0), 2: (160, 0), 3: (0, 80), 4: (80, 80), 5: (160, 80)}
print(F.intercambio(pos6, G6, A6, B6, {v: numero[comp[v]] for v in comp}, sirven,
                    pie="El intercambio en el matroide gráfico. A la izquierda el bosque "
                        "A, con cada vértice coloreado por su componente; a la derecha el "
                        "bosque B, más grande. De las cuatro aristas de B que no están en A "
                        "(en color) solo una, la roja, une dos componentes de A, y el intercambio "
                        "garantiza que haya al menos una."))
```

Para los ejemplos chicos, los tres axiomas se comprueban por fuerza bruta. El
comprobador recorre todos los pares de independientes, así que solo sirve para
conjuntos de unos pocos elementos, pero es el oráculo que usaremos para probar
afirmaciones.

```{python continue}
def familia(E, independiente):
    return {frozenset(C) for r in range(len(E) + 1)
            for C in itertools.combinations(E, r) if independiente(list(C))}

def es_matroide(I):
    if frozenset() not in I:
        return False
    if any(A - {x} not in I for A in I for x in A):
        return False
    return all(any(A | {e} in I for e in B - A)
               for A in I for B in I if len(A) < len(B))

print("bosques del diamante:", es_matroide(familia(D, es_bosque)))
print("emparejamientos del diamante:", es_matroide(familia(D, es_emparejamiento)))
print("bosques del grafo de la figura:", es_matroide(familia(G6, es_bosque)))
```

## 5. El goloso es óptimo sobre un matroide

**Teorema 1.** Si $(E, \mathcal I)$ es un matroide, para toda función de peso
$w : E \to \mathbb R_{\ge 0}$ el goloso de la §1 devuelve un independiente de peso
máximo.

*Demostración.* El conjunto del goloso es independiente, porque solo agrega un elemento
cuando el oráculo lo acepta. Sean $g_1, \dots, g_k$ sus elementos en el orden en que los
tomó, que es de peso no creciente. Sea $O$ un independiente cualquiera, con sus elementos
ordenados de mayor a menor peso, $o_1, \dots, o_m$. Vamos a demostrar algo más fuerte que
$w(G) \ge w(O)$: que $m \le k$ y que $w(g_i) \ge w(o_i)$ para cada $i \le m$. El goloso
le gana a $O$ posición por posición.

Supongamos que no, y sea $i \le m$ el primer índice donde falla: o bien $i = k + 1$
(a $O$ le sobran elementos), o bien $i \le k$ y $w(o_i) > w(g_i)$. Tomamos
$A = \{g_1, \dots, g_{i-1}\}$ y $B = \{o_1, \dots, o_i\}$. Los dos son independientes,
$A$ porque es parte del conjunto del goloso y $B$ porque es parte de $O$, y
$|A| = i - 1 < i = |B|$. Por (I3) hay un $e \in B \setminus A$ con
$A \cup \{e\} \in \mathcal I$, y como $B$ está ordenado, $w(e) \ge w(o_i)$.

Ahora miramos el momento en que el goloso examinó $e$.

- Si $i \le k$, entonces $w(e) \ge w(o_i) > w(g_i)$, así que el goloso examinó $e$
  antes que $g_i$. En ese momento su conjunto $S$ tenía solo elementos tomados antes
  de $g_i$, es decir, $S \subseteq A$.
- Si $i = k + 1$, entonces $A$ es todo el conjunto del goloso, y en cualquier momento
  $S \subseteq A$.

En los dos casos $S \cup \{e\} \subseteq A \cup \{e\}$, que es independiente, y **por
herencia** $S \cup \{e\}$ también lo es. El oráculo habría dicho que sí y el goloso habría
tomado $e$. Entonces $e \in A$, contra lo que dijimos. Este es el paso fácil de saltarse: (I3) da un elemento que se puede agregar *al final*, a $A$, y es (I2) la que
garantiza que también se podía agregar *antes*, cuando el goloso lo tuvo delante.

Con $m \le k$ y la desigualdad posición por posición, y usando que los pesos son no
negativos para los $g_i$ con $i > m$:
$$w(G) = \sum_{i=1}^{k} w(g_i) \ge \sum_{i=1}^{m} w(g_i) \ge \sum_{i=1}^{m} w(o_i) = w(O). \qquad \blacksquare$$

La demostración no usó que todas las bases midan lo mismo: el caso $i = k + 1$ lo
reemplaza. Fíjate también en lo que da de más: para cada $j$, los $j$ primeros
elementos del goloso pesan al menos tanto como cualquier independiente de $j$ elementos.

## 6. Sin intercambio, hay pesos que lo rompen

El Teorema 1 tiene recíproco, y es lo que convierte a los matroides en *la* respuesta y
no en una respuesta.

**Teorema 2.** Si $(E, \mathcal I)$ es un sistema de independencia que no es matroide,
hay una función de peso $w \ge 0$ para la que el goloso no devuelve un independiente de
peso máximo.

*Demostración.* Como (I3) falla, hay $A, B \in \mathcal I$ con $|A| < |B|$ tales que
$A \cup \{e\} \notin \mathcal I$ para todo $e \in B \setminus A$. Sean $a = |A|$,
$b = |B|$ y $c = |A \cap B|$. Definimos
$$w(e) = \begin{cases} a + 2 & e \in A, \\ a + 1 & e \in B \setminus A, \\ 0 & \text{en otro caso.} \end{cases}$$
El goloso examina primero los elementos de $A$, que pesan más, y los toma todos, porque
todo subconjunto de $A$ es independiente. Después examina los de $B \setminus A$ con su
conjunto igual a $A$, y rechaza cada uno, porque $A \cup \{e\} \notin \mathcal I$; como
rechaza, su conjunto sigue siendo $A$ para el siguiente. Lo que agregue después pesa 0.
Su peso total es $a(a + 2)$. El conjunto $B$ pesa $c(a + 2) + (b - c)(a + 1)$, y con
$b \ge a + 1$:
$$w(B) - a(a+2) = (b - c)(a + 1) - (a - c)(a + 2) \ge (a - c + 1)(a + 1) - (a - c)(a + 2) = c + 1 \ge 1. \qquad \blacksquare$$

Los dos teoremas juntos son el **teorema de Rado-Edmonds**. Alexander Schrijver
(*Combinatorial Optimization*, Springer, 2003, Teorema 40.1) atribuye una dirección a
Richard Rado («Note on independence functions», *Proceedings of the London Mathematical
Society* 7, 1957) y la otra a David Gale («Optimal assignments in an ordered set: an application of matroid theory»,
*Journal of Combinatorial Theory* 4, 1968) y a
Jack Edmonds («Matroids and the greedy algorithm», *Mathematical Programming* 1, 1971).

Una demostración de este tamaño merece un experimento que pueda fallar. Sobre un
conjunto de cuatro elementos se pueden enumerar todos los sistemas de independencia.
Para cada matroide probamos el goloso con todos los pesos en $\{0, 1, 2, 3\}^4$; para
cada uno que no lo es, la construcción del Teorema 2. Y una versión rota de la
construcción, con el mismo peso en $A$ y en $B$, para ver que la comprobación sabe
decir que no.

```{python continue}
U = [0, 1, 2, 3]
no_vacios = [frozenset(C) for r in range(1, 5) for C in itertools.combinations(U, r)]
sistemas = []
for mascara in range(1 << len(no_vacios)):
    I = {frozenset()} | {X for j, X in enumerate(no_vacios) if mascara >> j & 1}
    if all(X - {x} in I for X in I for x in X):
        sistemas.append(I)

def mejor(I, w):
    return max(peso(X, w) for X in I)

matroides = falla_matroide = falla_construccion = rota_no_falla = 0
for I in sistemas:
    ind = lambda S, I=I: frozenset(S) in I
    if es_matroide(I):
        matroides += 1
        for valores in itertools.product(range(4), repeat=4):
            w = dict(zip(U, valores))
            falla_matroide += peso(goloso(U, w, ind), w) < mejor(I, w)
        continue
    A, B = next((A, B) for A in I for B in I
                if len(A) < len(B) and not any(A | {e} in I for e in B - A))
    w = {e: len(A) + 2 if e in A else len(A) + 1 if e in B else 0 for e in U}
    falla_construccion += peso(goloso(U, w, ind), w) == mejor(I, w)
    w_rota = {e: 1 if e in A | B else 0 for e in U}
    rota_no_falla += peso(goloso(U, w_rota, ind), w_rota) == mejor(I, w_rota)

print("sistemas de independencia sobre 4 elementos:", len(sistemas))
print("matroides:", matroides, "  no matroides:", len(sistemas) - matroides)
print("matroides con algún peso donde el goloso falla:", falla_matroide)
print("no matroides donde la construcción no lo hace fallar:", falla_construccion)
print("no matroides donde la versión rota no lo hace fallar:", rota_no_falla)
```

Hay 167 sistemas de independencia sobre cuatro elementos y 68 son matroides. En los 68
el goloso acierta con los 256 pesos, y en los 99 restantes la construcción lo hace
fallar. La versión rota no lo hace fallar en 69 de los 99: con el mismo peso en $A$ y
en $B \setminus A$, el goloso puede examinar primero los elementos de $B$ y tomar el
conjunto bueno. Por eso los pesos del Teorema 2 tienen que separar $a + 2$ de $a + 1$.

## 7. Kruskal como caso particular

Un **árbol generador** de un grafo conexo es un árbol, es decir, un bosque conexo, que
contiene todos los vértices. Por la cuenta de la §4, son exactamente los bosques con
$n - 1$ aristas, que tienen una sola componente. En el matroide gráfico de un grafo conexo, las bases son
exactamente los árboles generadores: un bosque con menos de $n - 1$ aristas tiene más de
una componente, y como el grafo es conexo, alguna arista del grafo une dos de ellas.

Queremos el árbol de **costo mínimo**, y el Teorema 1 habla de peso máximo. Sea $M$ un
número mayor que todos los costos y $w(e) = M - c(e) > 0$. Con pesos positivos, un
independiente de peso máximo es una base, porque si no lo fuera se le podría agregar un
elemento y pesaría más. Para cada árbol generador $T$, $w(T) = (n - 1)M - c(T)$, así
que maximizar $w$ entre las bases es minimizar $c$. Y ordenar por $w$ decreciente es
ordenar por $c$ creciente. El goloso sobre el matroide gráfico con estos pesos es
Kruskal, línea por línea.

Lo único que queda es el oráculo. "¿$S \cup \{uv\}$ es un bosque?" es lo mismo que
"¿$u$ y $v$ están en componentes distintas de $S$?", y eso lo responde el union-find
del capítulo 4, §7, sin recorrer $S$.

```{python continue}
class UnionFind:
    def __init__(self, n):
        self.padre, self.rango = list(range(n)), [0] * n
    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:
            raiz = self.padre[raiz]
        while self.padre[x] != raiz:          # compresión de caminos
            self.padre[x], x = raiz, self.padre[x]
        return raiz
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rango[a] < self.rango[b]:
            a, b = b, a
        self.padre[b] = a
        self.rango[a] += self.rango[a] == self.rango[b]
        return True

def kruskal(n, aristas, c):
    """El goloso del matroide gráfico con w = M - c, y el oráculo en union-find."""
    uf, arbol = UnionFind(n), []
    for e in sorted(aristas, key=lambda e: c[e]):
        if uf.union(*e):          # extremos en componentes distintas: lo acepta
            arbol.append(e)
    return arbol

def arbol_minimo(n, aristas, c):
    return min(peso(T, c) for T in itertools.combinations(aristas, n - 1) if es_bosque(T))

rng = random.Random(10)
probados = distintos = 0
while probados < 300:
    n = rng.randint(2, 6)
    aristas = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
    if len(kruskal(n, aristas, {e: 0 for e in aristas})) < n - 1:
        continue                       # no es conexo
    c = {e: rng.randint(1, 9) for e in aristas}
    probados += 1
    distintos += peso(kruskal(n, aristas, c), c) != arbol_minimo(n, aristas, c)
print("grafos conexos probados:", probados, "  Kruskal distinto del mínimo:", distintos)
```

Kruskal coincide con la fuerza bruta en los 300 grafos. El costo es el del goloso
genérico con $T$ casi constante: $O(m \log m)$ para ordenar las $m$ aristas, y el
union-find con unión por rango y compresión, cuya cota de Tarjan es el capítulo 4, §9,
no domina. Lo que en Estructuras de Datos se demostraba con la propiedad del corte aquí
sale del Teorema 1 más la demostración del intercambio de la §4.

## 8. Tareas unitarias con plazos y penalizaciones

Una máquina atiende $n$ tareas que duran una unidad de tiempo cada una, empezando en el
instante 0. La tarea $i$ tiene un plazo $d_i \in \{1, \dots, n\}$ y una penalización
$w_i \ge 0$ que se paga si termina después de su plazo. Un plazo mayor que $n$ se puede
bajar a $n$ sin cambiar nada, porque con $n$ tareas unitarias todo termina a más tardar
en $n$. Queremos el orden de penalización total mínima. Es el ejemplo de Cormen,
Leiserson, Rivest y Stein (*Introduction to Algorithms*, 3.ª ed., MIT Press, 2009,
§16.5).

Cambiemos la pregunta. Si un conjunto $A$ de tareas se puede atender entero a tiempo, se
ponen primero, y las demás después en cualquier orden, pagando su penalización. Así que
minimizar lo que se paga es lo mismo que **maximizar el peso de un conjunto que se puede
atender a tiempo**, y la pregunta es si esos conjuntos forman un matroide. Sea
$N_t(A)$ el número de tareas de $A$ con plazo a lo sumo $t$.

**Lema 3.** $A$ se puede atender entero a tiempo si y solo si $N_t(A) \le t$ para todo
$t = 1, \dots, n$.

*Demostración.* Si hay un orden donde todas llegan a tiempo, las tareas de plazo a lo
sumo $t$ ocupan casillas distintas entre las $t$ primeras, así que son a lo sumo $t$.
Al revés, atiende $A$ por plazo creciente. Si la tarea en la posición $p$ tiene plazo
$d$, las $p$ primeras tienen plazo a lo sumo $d$, así que $p \le N_d(A) \le d$: termina
en $p$, a tiempo. $\blacksquare$

**Lema 4.** Los conjuntos que se pueden atender a tiempo son los independientes de un
matroide.

*Demostración.* (I1) y (I2) son inmediatos: quitar tareas no sube ningún $N_t$. Para
(I3), sean $|A| < |B|$, los dos con $N_t \le t$. Sea $k$ el mayor instante en
$\{0, \dots, n\}$ con $N_k(B) \le N_k(A)$; existe porque $N_0 = 0$ para los dos, y
$k < n$ porque $N_n(B) = |B| > |A| = N_n(A)$. Las tareas de $B$ con plazo mayor que $k$
son $|B| - N_k(B)$, más que las $|A| - N_k(A)$ de $A$, así que alguna, $x$, no está en
$A$. Al agregar $x$ a $A$, el conteo $N_t$ no cambia para $t < d_x$ y **sube en 1
para todo $t \ge d_x$**. Para $t \le k$ no cambia, porque $d_x > k$. Para $t > k$,
$N_t(A) < N_t(B)$ por la elección de $k$, así que
$N_t(A \cup \{x\}) \le N_t(A) + 1 \le N_t(B) \le t$. $\blacksquare$

El oráculo es el Lema 3, y el algoritmo es el mismo `goloso` de la §1.

```{python continue}
def cabe(S, d):
    """Lema 3: N_t(S) <= t para todo t."""
    n = len(d)
    cuenta = [0] * (n + 1)
    for i in S:
        cuenta[d[i]] += 1
    acumulado = 0
    for t in range(1, n + 1):
        acumulado += cuenta[t]
        if acumulado > t:
            return False
    return True

def tareas(d, w):
    E = list(range(len(d)))
    A = goloso(E, dict(enumerate(w)), lambda S: cabe(S, d))
    orden = sorted(A, key=lambda i: d[i])
    return orden, [i for i in E if i not in A]

def penalizacion_minima(d, w):
    return min(sum(w[i] for p, i in enumerate(orden) if p + 1 > d[i])
               for orden in itertools.permutations(range(len(d))))

d = [4, 2, 2, 1, 3, 2]
w = [90, 70, 50, 40, 30, 20]
orden, rechazadas = tareas(d, w)
print("orden:", [i + 1 for i in orden], "  rechazadas:", [i + 1 for i in rechazadas])
print("penalización:", sum(w[i] for i in rechazadas),
      "  fuerza bruta:", penalizacion_minima(d, w))
```

Sigue la traza con las tareas numeradas por penalización decreciente. Las tareas 1, 2
y 3 entran. La 4 tiene plazo 1, y con ella habría tres tareas de plazo a lo sumo 2,
así que $N_2 = 3 > 2$ y se rechaza, aunque penaliza 40. La 5 tiene plazo 3, deja
$N_3 = 3$, y entra. La 6 tiene plazo 2 y se rechaza por el mismo $N_2$. La penalización
es 60, la de la fuerza bruta (@fig-matroides-horario).

```{python continue echo=false output=asis}
print(F.horario(d, w, orden, rechazadas,
                pie="El horario de las seis tareas. Las cuatro que eligió el goloso van "
                    "a tiempo, ordenadas por plazo; la 4 y la 6 se rechazan porque con "
                    "cualquiera de ellas habría tres tareas de plazo a lo sumo 2."))
```

Una instancia no prueba nada, pero sirve para comparar contra el oráculo.

```{python continue}
rng = random.Random(10)
malas = 0
for _ in range(500):
    n = rng.randint(1, 7)
    dd = [rng.randint(1, n) for _ in range(n)]
    ww = [rng.randint(1, 50) for _ in range(n)]
    malas += sum(ww[i] for i in tareas(dd, ww)[1]) != penalizacion_minima(dd, ww)
print("instancias donde el goloso no es óptimo:", malas, "de 500")
```

El capítulo 9 demostró el plazo más cercano con un intercambio de vecinas inventado
para ese problema. Aquí no hubo que inventar nada para el goloso: bastó el Lema 4, y el
Teorema 1 hizo el resto.

## 9. El error plantado: comprobar solo en su plazo

El oráculo del Lema 3 recorre todos los instantes. Hay un atajo que suena bien: "la
tarea $x$ entra si hay lugar antes de su plazo", es decir, si las tareas ya elegidas
con plazo a lo sumo $d_x$ son menos que $d_x$. Mira un solo instante en vez de $n$.

```{python continue}
def cabe_atajo(S, d, x):
    return sum(1 for i in S if d[i] <= d[x]) + 1 <= d[x]

def tareas_atajo(d, w):
    A = []
    for x in sorted(range(len(d)), key=lambda i: -w[i]):
        if cabe_atajo(A, d, x):
            A.append(x)
    return A

def penalizacion_real(A, d, w):
    orden = sorted(A, key=lambda i: d[i])
    tarde = sum(w[i] for p, i in enumerate(orden) if p + 1 > d[i])
    return tarde + sum(w[i] for i in range(len(d)) if i not in A)

for dd, ww in [([2, 2, 1], [30, 20, 10]), (d, w)]:
    A = tareas_atajo(dd, ww)
    print("plazos", dd, " atajo elige", [i + 1 for i in A],
          " paga", penalizacion_real(A, dd, ww),
          " el goloso paga", sum(ww[i] for i in tareas(dd, ww)[1]))
```

Con tres tareas de plazos 2, 2 y 1, el atajo toma las dos primeras y después la
tercera, porque ninguna de las elegidas tiene plazo a lo sumo 1. Pero ahora hay tres
tareas de plazo a lo sumo 2, y una llega tarde: paga 20 donde se podía pagar 10. En la
instancia de la §8 paga 100 en vez de 60, porque acepta la tarea 4. ¿Lo atrapan las
pruebas?

```{python continue}
rng = random.Random(11)
def bateria(nombre, generar, N=2000):
    peor = 0
    for _ in range(N):
        dd, ww = generar()
        peor += penalizacion_real(tareas_atajo(dd, ww), dd, ww) > \
                sum(ww[i] for i in tareas(dd, ww)[1])
    print(f"{nombre:34} el atajo pierde en {peor:4} de {N}")

def al_azar():
    n = rng.randint(2, 7)
    return [rng.randint(1, n) for _ in range(n)], [rng.randint(1, 50) for _ in range(n)]
def plazos_distintos():
    n = rng.randint(2, 7)
    return rng.sample(range(1, n + 1), n), [rng.randint(1, 50) for _ in range(n)]
def urgentes_caras():
    n = rng.randint(2, 7)
    return (sorted(rng.randint(1, n) for _ in range(n)),
            sorted(rng.sample(range(1, 100), n), reverse=True))

bateria("al azar", al_azar)
bateria("plazos distintos", plazos_distintos)
bateria("las más urgentes son las más caras", urgentes_caras)
```

Al azar pierde en algo más de una de cada diez instancias, así que una batería
aleatoria lo atrapa. Las otras dos baterías no lo atrapan nunca, y son las que uno
escribe a mano. Con plazos todos distintos hay a lo sumo una tarea por plazo, así que
$N_t \le t$ vale para cualquier conjunto y los dos oráculos aceptan todo. Si las tareas
caras son las urgentes, el goloso las examina por plazo creciente: cuando llega a $x$,
ninguna elegida tiene plazo mayor que $d_x$, y entonces el conteo en $d_x$ es el mismo
que en cualquier $t \ge d_x$. En los dos casos mirar un solo instante alcanza.

La demostración lo anunciaba. En el Lema 4, el paso que importa es "al agregar $x$,
$N_t$ sube en 1 para todo $t \ge d_x$". El atajo comprueba solo $t = d_x$, y la tarea de
plazo 1 rompe $t = 2$. Y en el Teorema 1, el paso "el oráculo habría dicho que sí"
supone que el oráculo responde exactamente la pertenencia a $\mathcal I$. Un oráculo
que acepta conjuntos que no son independientes ya no corre el goloso de *ese*
matroide, y el teorema no dice nada.

## 10. Dos matroides: el emparejamiento bipartito

En un grafo **bipartito** los vértices están en dos lados, izquierdo y derecho, y cada
arista une un vértice de cada lado. Un conjunto de aristas es un emparejamiento si cada
vértice izquierdo toca a lo sumo una y cada vértice derecho toca a lo sumo una. Cada
mitad de la condición es un matroide de partición: las clases de la primera son las
aristas de cada vértice izquierdo, con cupo 1, y las de la segunda, las de cada vértice
derecho. Los emparejamientos son los conjuntos independientes **en los dos a la vez**:
la **intersección** de dos matroides.

La intersección hereda (I1) y (I2), pero no (I3). El ciclo de cuatro aristas, que es
bipartito, ya lo rompe por el mismo motivo que el diamante: una arista sola contra las
dos aristas disjuntas que la tocan, una en cada extremo. El goloso, entonces, puede fallar. ¿Cuánto?

```{python continue}
rng = random.Random(10)
razon_minima, caso = 1.0, None
for _ in range(3000):
    izq, der = rng.randint(1, 4), rng.randint(1, 4)
    E = [(f"u{i}", f"v{j}") for i in range(izq) for j in range(der) if rng.random() < 0.6]
    if not E:
        continue
    w = {e: rng.randint(1, 20) for e in E}
    r = peso(goloso(E, w, es_emparejamiento), w) / optimo(E, w, es_emparejamiento)
    if r < razon_minima:
        razon_minima, caso = r, w
print("razón mínima goloso / óptimo:", razon_minima)
print("el caso:", caso)
```

En 3 000 grafos bipartitos al azar el goloso nunca bajó de la mitad del óptimo, y llegó
a la mitad. En el caso que se imprime, tres aristas de peso 6 forman un camino, y el
goloso, que desempata por el orden de la lista, toma la del medio, que bloquea a las
otras dos.

Que la mitad es una garantía, y no una casualidad de estas 3 000 instancias, es el
ejercicio 10. Bernhard Korte y Dirk Hausmann («An analysis of the greedy heuristic for
independence systems», *Annals of Discrete Mathematics* 2, 1978) demostraron la versión
general: sobre la intersección de $k$ matroides el goloso obtiene al menos $1/k$ del
óptimo.

Para dos matroides hay algoritmos exactos de tiempo polinomial, que ya no son golosos:
Eugene Lawler («Matroid intersection algorithms», *Mathematical Programming* 9, 1975) da
uno para el común independiente de peso máximo. Este libro no los desarrolla. El caso
bipartito, que es el que más se usa, vuelve en el capítulo 13 como flujo máximo.

## 11. Tres matroides: el camino hamiltoniano

Con tres matroides la frontera ya no es la del goloso, sino la de cualquier algoritmo.
Sea $D$ un grafo dirigido con $n$ vértices, y llamemos independiente a un conjunto de
arcos que cumple tres condiciones: sin dirección, no tiene ciclos (matroide gráfico);
entra a lo sumo un arco en cada vértice (partición por la cabeza); sale a lo sumo uno de
cada vértice (partición por la cola).

**Lema 5.** $D$ tiene un camino hamiltoniano dirigido si y solo si hay un conjunto de
$n - 1$ arcos independiente en los tres matroides.

*Demostración.* Los $n - 1$ arcos de un camino hamiltoniano cumplen las tres
condiciones. Al revés, con a lo sumo un arco que entra y uno que sale por vértice, cada
componente de los arcos elegidos es un camino dirigido o un ciclo dirigido, y la primera
condición descarta los ciclos. Un bosque con $n - 1$ aristas sobre $n$ vértices tiene
$n - (n - 1) = 1$ componente, por la cuenta de la §4. Es un solo camino dirigido que pasa
por todos los vértices. $\blacksquare$

```{python continue}
def hamiltoniano(n, arcos):
    return any(all((p[i], p[i + 1]) in arcos for i in range(n - 1))
               for p in itertools.permutations(range(n)))

def tres_matroides(n, arcos):
    return any(len({v for _, v in S}) == n - 1 and len({u for u, _ in S}) == n - 1
               and es_bosque(S) for S in itertools.combinations(sorted(arcos), n - 1))

rng = random.Random(10)
distintos = 0
for _ in range(400):
    n = rng.randint(2, 5)
    arcos = {(u, v) for u in range(n) for v in range(n) if u != v and rng.random() < 0.35}
    distintos += hamiltoniano(n, arcos) != tres_matroides(n, arcos)
print("digrafos donde las dos respuestas difieren:", distintos, "de 400")
```

El capítulo 19 demuestra que el ciclo hamiltoniano dirigido es NP-completo, y el camino
sale de ahí partiendo un vértice $v$ en dos copias: $v_{\text{sal}}$ con los arcos que
salían de $v$ y $v_{\text{ent}}$ con los que entraban. Como a $v_{\text{sal}}$ no entra
ningún arco y de $v_{\text{ent}}$ no sale ninguno, todo camino hamiltoniano del grafo
nuevo empieza en $v_{\text{sal}}$ y termina en $v_{\text{ent}}$, y es un ciclo
hamiltoniano del original. Al revés, un ciclo hamiltoniano del original, abierto en
$v$, es un camino hamiltoniano de $v_{\text{sal}}$ a $v_{\text{ent}}$. Así que el común independiente máximo de tres matroides, aun
sin pesos, no tiene algoritmo polinomial salvo que P = NP.

## 12. La regla

Antes de inventar un intercambio para un goloso, pregunta si los conjuntos factibles
forman un matroide. Si lo forman, la demostración ya está hecha y el algoritmo es
ordenar y consultar un oráculo; todo el trabajo es demostrar (I3) y escribir un oráculo
que responda **exactamente** la independencia. Si no lo forman, el Teorema 2 garantiza
que hay pesos donde el goloso falla, y la pregunta pasa a ser cuántos matroides hacen
falta para describir el problema: con uno basta el goloso, con dos hace falta un
algoritmo de intersección, y con tres ya estamos en el terreno de la Parte III.

## Resumen

- Un **sistema de independencia** cumple $\emptyset \in \mathcal I$ y la herencia. Un
  **matroide** cumple además el intercambio: un independiente chico se agranda con algún
  elemento de uno más grande.
- Uniformes, de partición, lineales y gráficos son matroides; los emparejamientos de un
  grafo, en general, no.
- **Rado-Edmonds:** el goloso es óptimo para toda función de peso no negativa si y solo
  si el sistema es un matroide. Una dirección compara posición por posición y usa la
  herencia para decir que el goloso "habría tomado" el elemento; la otra construye los
  pesos $a + 2$, $a + 1$ y 0.
- **Kruskal** es el goloso del matroide gráfico con $w = M - c$, y el union-find es su
  oráculo.
- Las **tareas unitarias con plazos** forman un matroide: un conjunto cabe si y solo si
  $N_t \le t$ para todo $t$. Comprobarlo solo en el plazo de la tarea nueva es un error
  que las baterías hechas a mano no ven.
- Los **emparejamientos bipartitos** son la intersección de dos matroides de partición.
  El goloso garantiza la mitad, y el óptimo pide otro algoritmo. Con **tres** matroides
  está el camino hamiltoniano dirigido.

## Ejercicios

1. **[demostración]** Asigna a cada arista $uv$ de un grafo con $n$ vértices el vector de
   $\{0, 1\}^n$ con unos en las posiciones $u$ y $v$, con la suma módulo 2. Demuestra que
   un conjunto de aristas es un bosque si y solo si sus vectores son linealmente
   independientes sobre ese cuerpo. Concluye que el matroide gráfico es lineal, sin usar
   la demostración de la §4.

2. **[entrada que rompe]** Los emparejamientos del diamante no son un matroide, y el
   diamante tiene 5 aristas. Encuentra el grafo con menos aristas cuyos emparejamientos
   no forman un matroide, y demuestra que con menos aristas que el tuyo siempre lo forman.

3. **[demostración]** Demuestra que en un matroide todas las bases tienen el mismo
   tamaño. Después demuestra que, para todo $X \subseteq E$, todos los independientes
   maximales contenidos en $X$ tienen el mismo tamaño.

4. **[demostración]** Sea $(E, \mathcal I)$ un matroide. Llama $\mathcal I^*$ a la familia
   de los $X \subseteq E$ tales que $E \setminus X$ contiene una base. Demuestra que
   $(E, \mathcal I^*)$ es un matroide, el **dual**. ¿Qué son las bases del dual de un
   matroide gráfico de un grafo conexo?

5. **[traza]** Siete tareas unitarias tienen plazos $d = (2, 2, 1, 4, 3, 4, 2)$ y
   penalizaciones $w = (60, 50, 45, 40, 35, 30, 25)$. Corre el goloso a mano: para cada
   tarea di si entra y, si se rechaza, qué $N_t$ supera a $t$. Da el horario final y la
   penalización. ¿Qué elegiría el atajo de la §9?

6. **[entrada que rompe]** Da un sistema de independencia y una función de peso donde
   el goloso obtiene menos de la mitad del óptimo. Después, para cada $\varepsilon > 0$,
   uno donde obtiene menos de $\varepsilon$ veces el óptimo.

7. **[modelar]** Los elementos de $E$ están repartidos en clases y se quiere elegir a lo
   sumo $k$ elementos en total y a lo sumo $c_j$ de la clase $j$, con peso máximo. Es la
   intersección de un matroide uniforme y uno de partición. Demuestra que, aun así, es un
   matroide, y que por tanto el goloso es óptimo. Después compara con los dos matroides de
   partición de la §10: mira cómo se cortan las clases de una restricción con las de la
   otra, y di qué propiedad de esos cortes usó tu demostración.

8. **[modelar]** Una **ramificación** de un grafo dirigido es un conjunto de arcos sin
   ciclos (ignorando la dirección) donde a cada vértice entra a lo sumo un arco. Escribe
   las ramificaciones como intersección de dos matroides. Da un grafo dirigido con pocos
   arcos donde no forman un matroide, y pesos donde el goloso no da la ramificación de
   peso máximo.

9. **[demostración]** Sea un grafo bipartito con lados $L$ y $R$. Llama independiente a
   un $X \subseteq L$ si hay un emparejamiento que cubre todos los vértices de $X$.
   Demuestra que es un matroide, el **transversal**. Pista: dados dos emparejamientos,
   mira las componentes de su diferencia simétrica.

10. **[cambio de hipótesis] ★** El Teorema 1 supone un solo matroide. Supón ahora que
    $\mathcal I = \mathcal I_1 \cap \mathcal I_2$ es la intersección de dos matroides
    sobre el mismo $E$. Demuestra que, para todo $w \ge 0$, el goloso obtiene al menos la
    mitad del peso óptimo. ¿En qué paso de la demostración del Teorema 1 aparece el
    factor 2?

11. **[implementar y medir]** El oráculo `cabe` de la §8 cuesta $O(n)$ por consulta, y
    el goloso de tareas cuesta $O(n^2)$. Implementa otra versión: cada tarea aceptada se
    coloca en la casilla libre más tardía que no pase su plazo, y se rechaza si no hay
    ninguna; encuentra esa casilla con un union-find sobre las casillas. Demuestra que
    acepta las mismas tareas que `tareas`, y compara los tiempos de las dos para
    $n = 10^3, 10^4, 10^5$ con plazos y penalizaciones al azar. La versión cuadrática
    tardaría casi una hora con $n = 10^5$: mídela hasta $10^4$ y extrapola.
