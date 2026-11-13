# Reducciones desde 3-SAT a grafos {#chap-reducciones-grafos}

```{python echo=false output=asis}
import itertools
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_18.py
import figuras_18 as F18
```

El capítulo 16 dejó tres problemas de grafos atados entre sí: conjunto independiente,
clique y vertex cover están los tres en P o ninguno lo está. El capítulo 17 dejó 3-SAT
como primer problema NP-completo cómodo. Este capítulo une las dos cosas con dos
reducciones, una a conjunto independiente y otra a 3-coloración, y de paso agrega set
cover. Lo que importa no es la lista de problemas sino cómo se construyen las
reducciones: con **gadgets**, piezas chicas de la instancia de destino que imitan una
pieza de la fórmula. Un gadget se puede verificar solo, enumerando sus casos, y el
error plantado de este capítulo muestra por qué conviene hacerlo antes de probar la
reducción completa.

## 1. Lo que falta

El corolario 7 del capítulo 16 dice que si uno de conjunto independiente, clique y
vertex cover es NP-completo, los tres lo son. La receta de la §7 de ese capítulo pide,
en su paso 2, un problema que ya se sepa NP-completo, y el corolario 5 del capítulo 17
lo da: 3-SAT. Falta una sola reducción, 3-SAT $\le_p$ CONJUNTO-INDEPENDIENTE.

Una instancia de 3-SAT es una fórmula $\varphi$ con $n$ variables y $m$ cláusulas de
tres literales sobre tres variables distintas. Toda reducción desde 3-SAT tiene que
representar tres cosas en el problema de destino:

- **La elección**: cada variable vale verdadero o falso, y no las dos cosas.
- **La coherencia**: si una solución usa $x$ en una cláusula, no puede usar
  $\lnot x$ en otra.
- **La cláusula**: cada cláusula tiene al menos un literal verdadero.

Cada una se construye con un pedazo del grafo, y ese pedazo es el gadget. Ya viste uno
en el capítulo 17, §4: la ventana de $2 \times 3$ era una pieza de tamaño fijo que
comprobaba una condición local, y la fórmula entera era una copia de la ventana por
cada posición de la tabla. Aquí el material es otro (vértices y aristas en lugar de
cláusulas) y la idea es la misma.

## 2. 3-SAT ≤ₚ conjunto independiente

Fíjate en qué se comprueba cuando se verifica una asignación: se recorre la fórmula y,
en cada cláusula, se encuentra **un literal que la hace verdadera**. Ese literal es un
testigo, y un conjunto independiente de tamaño $m$ podría elegir uno por cláusula.

El primer intento pone un vértice por literal que aparece en la fórmula, une $x$ con
$\lnot x$, une los literales de una misma cláusula (para que el conjunto tome uno
solo de cada una) y pide tamaño $m$. Falla en la fórmula satisfacible
$(x_1 \lor x_2 \lor x_3) \land (x_1 \lor x_2 \lor \lnot x_3)$. Sus cuatro literales
$x_1, x_2, x_3, \lnot x_3$ son adyacentes dos a dos: $x_1$ y $x_2$ comparten
cláusula, cada uno de ellos comparte una con $x_3$ y otra con $\lnot x_3$, y
$x_3$ con $\lnot x_3$ son opuestos. El mayor independiente tiene un vértice, y se
pedían dos. El problema es que $x_1$ es testigo de las dos cláusulas y el conjunto lo
cuenta una sola vez. El arreglo es darle a cada **aparición** su propio vértice.

**Construcción.** Para cada cláusula $C_j = (\ell_{j,0} \lor \ell_{j,1} \lor
\ell_{j,2})$, tres vértices $(j, 0), (j, 1), (j, 2)$, unidos en un triángulo. Entre
dos apariciones de cláusulas distintas, una arista si sus literales son opuestos,
$x$ y $\lnot x$. El tamaño pedido es $k = m$.

```{python continue}
def a_independiente(phi):
    """3-SAT -> conjunto independiente. phi es una lista de cláusulas de tres enteros:
    x_i es i y ¬x_i es -i. El vértice (j, i) es la aparición i de la cláusula j."""
    V = [(j, i) for j in range(len(phi)) for i in range(3)]
    E = [(u, v) for u, v in itertools.combinations(V, 2)
         if u[0] == v[0] or phi[u[0]][u[1]] == -phi[v[0]][v[1]]]
    return V, E, len(phi)

phi1 = [[1, -2, 3], [-1, 2, 3], [-1, -2, -3]]
V1, E1, k1 = a_independiente(phi1)
print(len(V1), "vértices,", len(E1), "aristas, k =", k1)
```

Las 9 aristas de los triángulos son las negras de la @fig-red-independiente, y las
otras 6 unen literales opuestos. El conjunto resaltado lo encontró el decisor de la §3.

**Teorema 1.** 3-SAT $\le_p$ CONJUNTO-INDEPENDIENTE.

*Construcción y costo.* El grafo tiene $3m$ vértices, $3m$ aristas de triángulos y a
lo sumo $\binom{3m}{2}$ en total. Recorrer los pares cuesta $O(m^2)$, polinomial en
el tamaño de la fórmula.

*Si $\varphi$ es satisfacible, el grafo tiene un independiente de tamaño $m$.* Toma
una asignación que la cumple y, en cada cláusula, una aparición de un literal
verdadero. Son $m$ vértices, uno por triángulo, así que ninguna arista de triángulo
tiene los dos extremos en el conjunto. Una arista de conflicto une $x$ con $\lnot x$,
y los dos no pueden ser verdaderos a la vez, así que tampoco tiene los dos extremos
dentro. El conjunto es independiente.

*Si el grafo tiene un independiente $S$ con $|S| \ge m$, $\varphi$ es satisfacible.*
Un triángulo aporta a $S$ a lo sumo un vértice, porque sus tres vértices son
adyacentes dos a dos. Hay $m$ triángulos y $|S| \ge m$, así que **$S$ tiene
exactamente un vértice en cada triángulo**. Define la asignación así: si una aparición
de $x$ está en $S$, $x$ es verdadera; si una de $\lnot x$ está en $S$, $x$ es falsa;
si ninguna, $x$ vale cualquier cosa. Está bien definida porque $S$ no contiene a la
vez una aparición de $x$ y una de $\lnot x$, que serían adyacentes. Cada cláusula
tiene su vértice en $S$, y su literal es verdadero por definición. $\square$

La frase en negrita es la que hace funcionar la vuelta. Sin los triángulos, $S$ podría
tomar dos apariciones de la misma cláusula y ninguna de otra.

## 3. Probarla contra el oráculo

Para probar la reducción hacen falta un decisor de conjunto independiente y uno de
3-SAT. El de 3-SAT prueba las $2^n$ asignaciones. El de independiente ramifica sobre
el vértice $v$ de menor grado entre los candidatos: algún independiente máximo
contiene a $v$ o a uno de sus vecinos, porque si no contuviera a ninguno se le podría
agregar $v$. Así cada rama elige $v$ o un vecino suyo, lo mete en el conjunto y borra
sus vecinos. Los conjuntos son máscaras de bits, como en el capítulo 11, §9.

```{python continue}
def independiente(V, E, k):
    """Un conjunto independiente de tamaño k, o None."""
    idx = {v: i for i, v in enumerate(V)}
    ady = [0] * len(V)
    for u, v in E:
        ady[idx[u]] |= 1 << idx[v]
        ady[idx[v]] |= 1 << idx[u]

    def bits(x):
        while x:
            b = x & -x
            yield b.bit_length() - 1
            x ^= b

    def rec(cand, k):
        if k == 0:
            return 0
        if cand.bit_count() < k:
            return None
        v = min(bits(cand), key=lambda i: (ady[i] & cand).bit_count())
        for w in [v, *bits(ady[v] & cand)]:
            s = rec(cand & ~ady[w] & ~(1 << w), k - 1)
            if s is not None:
                return s | 1 << w
        return None

    s = rec((1 << len(V)) - 1, k)
    return None if s is None else [v for v in V if s >> idx[v] & 1]

def cumple(phi, a):
    return all(any(a[abs(l)] == (l > 0) for l in c) for c in phi)

def satisfacible(phi, n):
    """El oráculo: una asignación que cumple phi, o None."""
    for bits in itertools.product([False, True], repeat=n):
        if cumple(phi, a := dict(enumerate(bits, 1))):
            return a
    return None

def asignacion(phi, S, n):
    """La vuelta del teorema 1: leer la asignación desde el independiente."""
    a = {x: False for x in range(1, n + 1)}        # las variables sin testigo
    for j, i in S:
        a[abs(phi[j][i])] = phi[j][i] > 0
    return a

S1 = independiente(V1, E1, k1)
print("S =", [phi1[j][i] for j, i in S1], "->", asignacion(phi1, S1, 3))
```

```{python continue echo=false output=asis}
print(F18.independiente(phi1, S1, ident="red-independiente",
      pie="El grafo de la fórmula de tres cláusulas: un triángulo por cláusula (negro) "
          "y una arista entre cada par de apariciones opuestas (naranja). El conjunto "
          "relleno es el independiente de tamaño 3 que encontró el decisor."))
```

La vuelta del teorema se lee en la @fig-red-independiente: el conjunto toma
$\lnot x_2$ de la primera cláusula y $\lnot x_1$ de la segunda y de la tercera. Que
$\lnot x_1$ sea testigo de dos cláusulas no es problema, porque cada aparición tiene
su vértice. La asignación es $x_1 = x_2 = $ falso, y $x_3$, que no tiene testigo,
queda en falso porque así la inicializa el código; con $x_3$ verdadero también
cumpliría las tres.

Ahora la batería. Las fórmulas al azar con pocas cláusulas por variable son casi todas
satisfacibles, y una batería de instancias sí prueba media demostración (capítulo 16,
§13). Por eso tiene tres partes. La primera son **todas** las fórmulas sobre $x_1,
x_2, x_3$ sin cláusulas repetidas: una cláusula elige el signo de cada variable, así
que hay 8 cláusulas posibles y $2^8 - 1 = 255$ fórmulas no vacías. La segunda son
fórmulas sobre 5 variables con una asignación plantada, que son sí. La tercera son
fórmulas sobre 5 variables que contienen las 8 cláusulas de tres variables elegidas al
azar, que son no: cada asignación de esas tres variables hace falsa exactamente una de
las 8.

```{python continue}
def formula_al_azar(n, m):
    return [[x * random.choice((1, -1)) for x in random.sample(range(1, n + 1), 3)]
            for _ in range(m)]

def con_solucion(n, m):
    a = {x: random.random() < 0.5 for x in range(1, n + 1)}
    phi = []
    while len(phi) < m:
        c = formula_al_azar(n, 1)[0]
        if cumple([c], a):
            phi.append(c)
    return phi

def sin_solucion(n, m):
    x, y, z = random.sample(range(1, n + 1), 3)
    phi = [[s * x, t * y, u * z] for s, t, u in itertools.product((1, -1), repeat=3)]
    phi += formula_al_azar(n, m)
    random.shuffle(phi)
    return phi

patrones = [[s * 1, t * 2, u * 3] for s, t, u in itertools.product((1, -1), repeat=3)]
todas = [list(c) for r in range(1, 9) for c in itertools.combinations(patrones, r)]
random.seed(18)
bateria = ([(phi, 3) for phi in todas]
           + [(con_solucion(5, random.randint(1, 15)), 5) for _ in range(100)]
           + [(sin_solucion(5, random.randint(0, 6)), 5) for _ in range(100)])

inicio, si, no = time.perf_counter(), 0, 0
for phi, n in bateria:
    V, E, k = a_independiente(phi)
    S = independiente(V, E, k)
    assert (S is not None) == (satisfacible(phi, n) is not None)
    if S is not None:
        assert cumple(phi, asignacion(phi, S, n))
        si += 1
    else:
        no += 1
print(f"{len(bateria)} fórmulas: {si} sí y {no} no, todas bien, "
      f"en {time.perf_counter() - inicio:.2f} s")
print("no entre las", len(todas), "de x1, x2, x3:",
      sum(satisfacible(phi, 3) is None for phi in todas))
```

El decisor coincide con el oráculo en todas, y en las sí la asignación que se lee del
conjunto cumple la fórmula, que es la vuelta del teorema ejecutada. Entre las 255
fórmulas de tres variables hay una sola insatisfacible, la de las 8 cláusulas: si
falta una, la asignación que la hace falsa cumple las otras siete. Una batería
exhaustiva y chica, sola, vería el lado no una sola vez, y por eso lleva la tercera
parte.

Karp, en el artículo de 1972 que cita el capítulo 16, reduce SAT a clique en la p. 97.
Su grafo tiene un vértice $\langle \sigma, i \rangle$ por cada literal $\sigma$ de la
cláusula $C_i$, aristas entre apariciones de cláusulas distintas cuyos literales no son
opuestos, y $k$ igual al número de cláusulas. Es el complemento del nuestro, lo que
por el teorema 4 del capítulo 16 da la misma reducción:

```{python continue}
iguales = 0
for phi in todas:
    V, E, k = a_independiente(phi)
    karp = {frozenset((u, v)) for u, v in itertools.combinations(V, 2)
            if u[0] != v[0] and phi[u[0]][u[1]] != -phi[v[0]][v[1]]}
    pares = {frozenset(p) for p in itertools.combinations(V, 2)}
    iguales += karp == pares - {frozenset(e) for e in E}
print("el grafo de Karp es el complemento del nuestro en", iguales, "de", len(todas))
```

## 4. Clique y vertex cover

**Corolario 2.** CONJUNTO-INDEPENDIENTE, CLIQUE y VERTEX-COVER son NP-completos.

*Demostración.* Conjunto independiente está en NP (capítulo 16, §4), 3-SAT es
NP-completo (corolario 5 del capítulo 17) y 3-SAT $\le_p$ CONJUNTO-INDEPENDIENTE por
el teorema 1. El lema 3 del capítulo 16 da que conjunto independiente es NP-completo,
y la segunda frase del corolario 7 del mismo capítulo da los otros dos. $\square$

Vale la pena mirar qué dice esto de lo que ya sabes. El capítulo 11, §2 calcula el
independiente de peso máximo **en un árbol** en tiempo lineal, y eso no contradice el
corolario: la dificultad es del peor caso sobre grafos generales, y los grafos de la
reducción, llenos de triángulos, no son árboles. El ejercicio 6 mira otra familia, la
de los grafos bipartitos, donde el problema también está en P. El capítulo 20 vuelve
sobre vertex cover para resolverlo exacto con árboles de búsqueda acotados, y el 21
para aproximarlo con razón 2.

## 5. Vertex cover ≤ₚ set cover

En **set cover** se da un universo finito $U$, una familia de subconjuntos
$S_1, \dots, S_t \subseteq U$ y un entero $k$, y se pregunta si hay $k$ conjuntos de
la familia cuya unión es $U$. Está en NP: el certificado es la lista de índices, y el
verificador calcula la unión.

Un vertex cover es un conjunto de vértices que toca todas las aristas. Si se piensa
cada vértice como "el conjunto de aristas que toca", cubrir las aristas con vértices
es cubrir el universo de las aristas con esos conjuntos.

**Teorema 3.** VERTEX-COVER $\le_p$ SET-COVER.

*Construcción.* Dado $(G, k)$ con $G = (V, E)$, el universo es $U = E$, la familia
tiene un conjunto $S_v = \{e \in E : v \in e\}$ por vértice, y el número es el mismo
$k$. Se calcula en $O(|V| \cdot |E|)$.

*Si $C$ es un vertex cover con $|C| \le k$*, toma $\{S_v : v \in C\}$. Cada arista $e$
tiene un extremo $v \in C$, y entonces $e \in S_v$: la unión es $U$.

*Si $S_{v_1}, \dots, S_{v_r}$ con $r \le k$ cubren $U$*, el conjunto
$\{v_1, \dots, v_r\}$ es un vertex cover: cada arista $e$ está en algún $S_{v_i}$, y
**estar en $S_{v_i}$ quiere decir que $v_i$ es un extremo de $e$**. $\square$

Es la reducción de Karp, p. 98 ("NODE COVER ∝ SET COVERING"), con las mismas
palabras: los elementos son las aristas, y $S_j$ es el conjunto de aristas que inciden
en el vértice $j$.

```{python continue}
def a_set_cover(n, E, k):
    return list(range(len(E))), [{i for i, e in enumerate(E) if v in e} for v in range(n)], k

def hay_cover(n, E, k):
    return any(all(u in S or v in S for u, v in E)
               for S in map(set, itertools.combinations(range(n), min(k, n))))

def hay_set_cover(U, familia, k):
    return any(set(U) <= set().union(*sub)
               for sub in itertools.combinations(familia, min(k, len(familia))))

random.seed(5)
casos = si = 0
for _ in range(150):
    n = random.randint(1, 7)
    E = [p for p in itertools.combinations(range(n), 2) if random.random() < 0.5]
    for k in range(n + 1):
        r = hay_cover(n, E, k)
        assert r == hay_set_cover(*a_set_cover(n, E, k))
        casos, si = casos + 1, si + r
print(f"{casos} instancias (G, k), {si} sí y {casos - si} no: la respuesta se preserva")
```

Aquí las dos partes de la batería salen parejas sin esfuerzo, porque se prueba cada
$k$ de 0 a $n$ y los $k$ chicos son no. Set cover queda NP-completo por el lema 3 del
capítulo 16. Vuelve en el capítulo 21, con el algoritmo goloso que lo aproxima con
razón $H_n$, y el ejercicio 4 lo relaciona con su dual, hitting set.

## 6. 3-coloración

Un **3-coloreo** de un grafo asigna a cada vértice uno de tres colores de modo que los
extremos de cada arista tengan colores distintos. 3-COLORACIÓN pregunta si un grafo
tiene uno. Está en NP, con el coloreo como certificado. Con dos colores el problema
está en P: un BFS que alterna colores en cada componente, como dice el capítulo 16,
§3, encuentra el coloreo o una arista que lo impide. Con tres colores, la reducción de
esta sección y las dos siguientes lo hace NP-completo.

Las tres cosas de la §1 se construyen así. Primero, un triángulo de tres vértices
nuevos, que llamamos $T$, $F$ y $B$ (verdadero, falso y base). En todo 3-coloreo sus
tres colores son distintos, así que **les ponen nombre a los colores**: el color de
$T$ significa verdadero, el de $F$ falso, el de $B$ ninguno de los dos. Los colores
son intercambiables, y el triángulo de la paleta fija cuál es cuál.

Después, para cada variable $x_i$, dos vértices $x_i$ y $\lnot x_i$ unidos entre sí y
los dos unidos a $B$. El triángulo $x_i, \lnot x_i, B$ obliga a cada literal a tener
el color de $T$ o el de $F$ (no el de $B$, al que es adyacente), y a los dos opuestos
a tener colores distintos. Elección y coherencia salen juntas, en un triángulo. A
diferencia del conjunto independiente, aquí hay un vértice por literal y no por
aparición: el color del vértice $x_i$ **es** el valor de $x_i$, y todas las cláusulas
lo leen del mismo sitio.

Lo difícil es la cláusula. Hace falta un gadget que se enchufe a tres vértices
literales $a, b, c$ y a la paleta, que se pueda colorear si alguno de los tres tiene
el color de $T$, y que no se pueda colorear si los tres tienen el de $F$.

## 7. El gadget de cláusula

Empecemos por un "O" de dos entradas. Un triángulo nuevo $p, q, r$, con $p$ unido a
la entrada $x$ y $q$ unido a la entrada $y$. La salida es $r$. Antes de demostrar
nada, el experimento: para cada par de colores de entrada, qué colores puede tomar $r$
en algún coloreo del triángulo.

```{python continue}
T, F, B = "T", "F", "B"

def o_posibles(x, y):
    """Los colores posibles de la salida r del triángulo p, q, r con p ~ x y q ~ y."""
    return sorted({r for p, q, r in itertools.permutations("TFB") if p != x and q != y})

for x, y in itertools.product("TF", repeat=2):
    print(f"entradas {x}, {y}: r puede ser {', '.join(o_posibles(x, y))}")
```

La tabla dice dos cosas, y una tercera que no dice. Si las dos entradas son $F$, la
salida es $F$: $p$ y $q$ no pueden ser $F$, así que son $T$ y $B$ en algún orden, y
$r$ se queda con el tercero. Si alguna entrada es $T$, la salida **puede** ser $T$. Lo
que no dice es que el triángulo calcule el O: con entradas $T$ y $F$ la salida puede
ser también $F$ o $B$. El gadget no tiene por qué calcular la función, le basta con
dos garantías, y las dos se escriben como lema.

**Lema 4** (el O). Sean $x, y$ vértices con colores en $\{T, F\}$ y $p, q, r$ un
triángulo con $p$ adyacente a $x$ y $q$ adyacente a $y$. (a) Si $x$ e $y$ son $F$, en
todo coloreo $r$ es $F$. (b) Si alguno es $T$, hay un coloreo de $p, q$ con $r = T$.

*Demostración.* (a) está arriba. (b) Para $r = T$ hace falta $\{p, q\} = \{F, B\}$ con
$p \ne x$ y $q \ne y$. Si $x = T$, pon $q$ distinto de $y$ dentro de $\{F, B\}$ (si
$y = F$, $q = B$; si $y = T$, cualquiera) y $p$ el otro, que no es $T$. Si $y = T$ es
simétrico. $\square$

El gadget de cláusula encadena dos: un O con entradas $a, b$ y salida $r_1$, y otro con
entradas $r_1, c$ y salida $r_2$. Por último, $r_2$ se une a $F$ y a $B$, lo que lo
obliga a ser $T$. Son 6 vértices nuevos y 12 aristas por cláusula.

```{python continue}
GADGET = [("p1", "q1"), ("q1", "r1"), ("p1", "r1"), ("p1", "a"), ("q1", "b"),
          ("p2", "q2"), ("q2", "r2"), ("p2", "r2"), ("p2", "r1"), ("q2", "c"),
          ("r2", "F"), ("r2", "B")]
INTERNOS = ["p1", "q1", "r1", "p2", "q2", "r2"]

def coloreos(gadget, a, b, c):
    """Todos los coloreos de los 6 vértices internos, con los literales y la paleta fijos."""
    fijo = {"a": a, "b": b, "c": c, "T": T, "F": F, "B": B}
    salida = []
    for cols in itertools.product("TFB", repeat=6):
        col = {**fijo, **dict(zip(INTERNOS, cols))}
        if all(col[u] != col[v] for u, v in gadget):
            salida.append(col)
    return salida

casos = {abc: coloreos(GADGET, *abc) for abc in itertools.product("TF", repeat=3)}
for abc, cs in casos.items():
    print(", ".join(abc), "->", len(cs), "coloreos de", 3 ** 6)
```

Son $3^6 = 729$ coloreos internos por caso, y en los 8 casos de $(a, b, c)$ hay
coloreo salvo en uno: $F, F, F$, con 0. La @fig-red-gadget-casos muestra un coloreo
de cada caso, el primero que encontró la enumeración. La enumeración propone el
enunciado, y la demostración dice por qué es cierto.

**Lema 5** (la cláusula). Con la paleta coloreada $T, F, B$ y $a, b, c$ coloreados en
$\{T, F\}$, los 6 vértices internos del gadget se pueden colorear si y solo si alguno
de $a, b, c$ es $T$.

*Demostración.* *Si los tres son $F$, no hay coloreo.* Por el lema 4 (a) sobre el
primer O, $r_1$ es $F$. Entonces **las dos entradas del segundo O, $r_1$ y $c$, son
$F$**, y por el lema 4 (a) otra vez $r_2$ es $F$. Pero $r_2$ es adyacente a $F$.

*Si alguno es $T$, hay coloreo.* Si $a$ o $b$ es $T$, el lema 4 (b) da un coloreo del
primer O con $r_1 = T$, y entonces el segundo O tiene una entrada $T$ y el lema 4 (b)
da $r_2 = T$. Si $a$ y $b$ son $F$, entonces $c$ es $T$; el primer O da $r_1 = F$, y
el segundo, con entrada $c = T$, da $r_2 = T$. En los dos casos $r_2 = T$ es distinto
de $F$ y de $B$, sus dos vecinos de la paleta. $\square$

El lema 4 pide entradas en $\{T, F\}$, y por eso en la segunda parte se elige $r_1$
entre $T$ y $F$, aunque haya coloreos con $r_1 = B$.

```{python continue echo=false output=asis}
print(F18.gadget_casos(GADGET, [(abc, cs[0] if cs else None) for abc, cs in casos.items()],
      ident="red-gadget-casos",
      pie="Arriba, el gadget de cláusula con sus 6 vértices internos, las entradas a, b, c "
          "a la izquierda y los vértices F y B de la paleta a la derecha. Debajo, los 8 "
          "casos de los literales, cada uno con el primer coloreo que encontró la "
          "enumeración. En F, F, F no hay ninguno."))
```

## 8. 3-SAT ≤ₚ 3-coloración

La instancia completa tiene el triángulo de la paleta, un triángulo $x_i, \lnot x_i,
B$ por variable y un gadget por cláusula, con sus entradas $a, b, c$ conectadas a los
vértices de los tres literales de la cláusula y sus vértices $F$ y $B$ identificados
con los de la paleta. Son $3 + 2n + 6m$ vértices y $3 + 3n + 12m$ aristas.

```{python continue}
def a_coloracion(phi, n, gadget=GADGET):
    """3-SAT -> 3-coloración. Vértices: "T", "F", "B", los literales como enteros, y los
    internos del gadget de la cláusula j como (j, nombre)."""
    E = [(T, F), (F, B), (T, B)]
    for x in range(1, n + 1):
        E += [(x, -x), (x, B), (-x, B)]
    for j, (a, b, c) in enumerate(phi):
        nombre = {"a": a, "b": b, "c": c, "T": T, "F": F, "B": B}
        E += [tuple(nombre.get(v, (j, v)) for v in e) for e in gadget]
    return E

phi3 = [[1, 2, 3], [-1, -2, 3]]
E3 = a_coloracion(phi3, 3)
print(len({v for e in E3 for v in e}), "vértices y", len(E3), "aristas")
```

Para la fórmula de dos cláusulas sobre tres variables son $3 + 6 + 12 = 21$ vértices y
$3 + 9 + 24 = 36$ aristas.

**Teorema 6.** 3-SAT $\le_p$ 3-COLORACIÓN.

*Construcción y costo.* La de arriba, de tamaño $O(n + m)$ y calculable en tiempo
lineal: cada gadget es una copia de un grafo fijo.

*Si $\varphi$ es satisfacible, el grafo es 3-coloreable.* Toma una asignación que la
cumple. Colorea la paleta $T, F, B$, cada literal verdadero con $T$ y cada falso con
$F$. Las aristas de la paleta y de los triángulos de variable quedan bien. En cada
cláusula hay un literal verdadero, y el lema 5 da un coloreo de sus vértices internos
que respeta las 12 aristas del gadget. Falta ver que los coloreos de gadgets distintos
no chocan, y no pueden: **un vértice interno solo es adyacente a vértices internos de
su gadget, a literales y a $F$ y $B$**, y todas esas aristas están entre las que el
lema 5 ya comprobó.

*Si el grafo es 3-coloreable, $\varphi$ es satisfacible.* Toma un 3-coloreo. Los tres
vértices de la paleta tienen colores distintos, así que se pueden renombrar los
colores para que se llamen $T$, $F$ y $B$ como sus vértices. Cada literal es adyacente
a $B$, así que es $T$ o $F$, y $x_i$ y $\lnot x_i$ son adyacentes, así que tienen
colores distintos. Define $x_i$ verdadera si su vértice es $T$. El gadget de cada
cláusula está coloreado, y por el lema 5 alguno de sus tres literales es $T$: la
cláusula se cumple. $\square$

El código necesita un decisor de 3-coloración que no sepa nada de la reducción. Este
hace vuelta atrás con propagación: cuando a un vértice le queda un solo color posible,
ese color se borra de sus vecinos. Además, cuando los vértices sin decidir se separan
en componentes que no se tocan, resuelve cada una por su lado. Esa partición no mira
la estructura de los gadgets, es la misma para cualquier grafo, y es la que deja
correr la batería en segundos.

```{python continue}
def tres_colorear(E):
    """Un 3-coloreo del grafo de aristas E (dict vértice -> 0, 1, 2), o None."""
    ady = {}
    for u, v in E:
        ady.setdefault(u, set()).add(v)
        ady.setdefault(v, set()).add(u)

    def propaga(dom, pila):
        while pila:
            v = pila.pop()
            (k,) = dom[v]
            for w in ady[v]:
                if k in dom[w]:
                    dom[w] = dom[w] - {k}
                    if not dom[w]:
                        return False
                    if len(dom[w]) == 1:
                        pila.append(w)
        return True

    def componentes(abiertos):
        resto, comps = set(abiertos), []
        while resto:
            pila = [resto.pop()]
            comp = set(pila)
            while pila:
                for w in ady[pila.pop()] & resto:
                    resto.discard(w)
                    comp.add(w)
                    pila.append(w)
            comps.append(comp)
        return comps

    def rec(dom, zona):
        abiertos = [v for v in zona if len(dom[v]) > 1]
        if not abiertos:
            return dom
        comps = componentes(abiertos)
        if len(comps) > 1:                  # no comparten aristas: una a la vez
            for comp in comps:
                d = rec(dom, comp)
                if d is None:
                    return None
                dom = {**dom, **{v: d[v] for v in comp}}
            return dom
        v = max(abiertos, key=lambda v: (-len(dom[v]), len(ady[v])))
        for k in sorted(dom[v]):
            d = {**dom, v: {k}}
            if propaga(d, [v]) and (r := rec(d, zona)) is not None:
                return r
        return None

    r = rec({v: {0, 1, 2} for v in ady}, list(ady))
    return None if r is None else {v: min(s) for v, s in r.items()}

def con_nombres(col):
    """Renombra los colores como los vértices de la paleta, como en la demostración."""
    nombre = {col[T]: T, col[F]: F, col[B]: B}
    return {v: nombre[k] for v, k in col.items()}
```

Resolver las componentes por separado es correcto porque dos componentes no comparten
aristas entre vértices abiertos: lo que se elija en una no le quita colores a la otra.
La batería es la misma de la §3, con 3-SAT como oráculo, y en las instancias sí se
comprueban el coloreo y la asignación leída de él.

```{python continue}
inicio, si, no, peor = time.perf_counter(), 0, 0, 0.0
for phi, n in bateria:
    t0 = time.perf_counter()
    E = a_coloracion(phi, n)
    col = tres_colorear(E)
    peor = max(peor, time.perf_counter() - t0)
    assert (col is not None) == (satisfacible(phi, n) is not None)
    if col is not None:
        assert all(col[u] != col[v] for u, v in E)
        c = con_nombres(col)
        assert cumple(phi, {x: c[x] == T for x in range(1, n + 1)})
        si += 1
    else:
        no += 1
print(f"{len(bateria)} fórmulas: {si} sí y {no} no, todas bien, "
      f"en {time.perf_counter() - inicio:.2f} s (la peor, {peor:.3f} s)")

col3 = con_nombres(tres_colorear(E3))
print("literales:", {x: col3[x] for x in (1, 2, 3)})
```

La @fig-red-instancia es la instancia completa de la fórmula de dos cláusulas, con el
coloreo que devolvió el decisor. Se lee la asignación $x_1 = $ falso, $x_2 = $
verdadero, $x_3 = $ falso: $x_2$ cumple la primera cláusula y $\lnot x_1$ la segunda.

Karp, en la p. 99 de su artículo, reduce 3-SAT a número
cromático, la pregunta de si un grafo se colorea con $k$ colores, con un $k$ que crece
con la fórmula. Que tres colores ya bastan para la dificultad lo demostró Larry
Stockmeyer en "Planar 3-colorability is polynomial complete" (*ACM SIGACT News* 5(3),
1973, pp. 19–25), incluso para grafos planares.

```{python continue echo=false output=asis}
print(F18.instancia(3, phi3, E3, col3, ident="red-instancia",
      pie="La instancia de 3-coloración de (x₁ ∨ x₂ ∨ x₃) ∧ (¬x₁ ∨ ¬x₂ ∨ x₃): la paleta "
          "arriba, los triángulos de variable en el medio y un gadget por cláusula "
          "abajo, con el coloreo que encontró el decisor (azul T, naranja F, gris B). "
          "Las aristas de r₂ a F y a B van en gris."))
```

## 9. El error plantado

La variante cambia una arista de sitio: el segundo O toma su entrada de $p_1$ en lugar
de $r_1$. Parece lo mismo, porque $p_1$ también está en el primer triángulo y también
depende de $a$.

```{python continue}
ROTO = [("p2", "p1") if e == ("p2", "r1") else e for e in GADGET]

def probar(nombre, instancias):
    fallos_si = fallos_no = sies = noes = 0
    for phi, n in instancias:
        bien = satisfacible(phi, n) is not None
        dice = tres_colorear(a_coloracion(phi, n, ROTO)) is not None
        if bien:
            sies, fallos_si = sies + 1, fallos_si + (dice != bien)
        else:
            noes, fallos_no = noes + 1, fallos_no + (dice != bien)
    print(f"{nombre:<13} sí: {fallos_si} fallos de {sies:<4} "
          f"no: {fallos_no} fallos de {noes}")

random.seed(9)
probar("con solución", [(con_solucion(5, random.randint(1, 15)), 5) for _ in range(150)])
probar("al azar", [(formula_al_azar(4, random.randint(1, 10)), 4) for _ in range(150)])
probar("todas", [(phi, 3) for phi in todas])
roto = {"".join(abc): len(coloreos(ROTO, *abc)) for abc in itertools.product("TF", repeat=3)}
print("gadget roto, coloreos por caso:", " ".join(f"{k}:{v}" for k, v in roto.items()))
```

Las fórmulas con solución plantada no pueden encontrar el error: la reducción rota
contesta sí a toda fórmula, y todas ellas son sí. Las fórmulas al azar sobre 4
variables, con hasta 10 cláusulas, tampoco lo encuentran, porque no salió ninguna
insatisfacible. La batería exhaustiva sobre tres variables lo encuentra en su única
instancia no. Y la última línea lo encuentra sin construir ninguna fórmula: el gadget
roto tiene coloreo en los 8 casos, también en $F, F, F$.

La demostración lo anunciaba. La dirección "si los tres son $F$, no hay coloreo" del
lema 5 usa la frase en negrita: **las dos entradas del segundo O son $F$**. Eso vale
para $r_1$, que el lema 4 (a) obliga a ser $F$, y no vale para $p_1$, que con $a = F$
es $T$ o $B$. Con $p_1 = B$, el segundo O tiene una entrada que no es $F$, y $r_2$
puede ser $T$. Fíjate en qué dirección vive el error: la del teorema 6 que va de un
coloreo a una asignación, la que solo ejercitan las instancias no.

## 10. Qué hace un buen gadget

Las dos reducciones de este capítulo tienen la misma forma, y el gadget de cláusula
de 3-coloración muestra las cuatro propiedades que la hacen funcionar.

**Se comunica por una interfaz chica.** El gadget toca el resto del grafo solo en
$a, b, c$ y en $F$ y $B$. Por eso la demostración del teorema 6 se arma con un hecho
local por pieza: el lema 5 habla de un gadget, y la frase en negrita del teorema dice
que no hay más aristas que mirar.

**Su especificación es una tabla finita.** Sobre la interfaz hay 8 casos, y en cada
uno la pregunta "¿se puede completar?" tiene respuesta por enumeración de $3^6$
coloreos. Un gadget que se puede comprobar así no necesita fe.

**Prohíbe exactamente lo que tiene que prohibir.** El gadget no calcula el O de sus
entradas, y no hace falta: solo tiene que dejar sin salida el caso $F, F, F$ y dejar
salida en los otros siete. Pedirle que $r_2$ valga exactamente $a \lor b \lor c$ sería
pedir más de lo que la demostración usa, y costaría un gadget más grande.

**Tiene tamaño constante.** 6 vértices y 12 aristas por cláusula, lo que hace la
reducción lineal en la fórmula. Las ventanas del capítulo 17, §4 tenían la misma
propiedad, y es la que hizo polinomial la fórmula de Cook-Levin.

## 11. La regla, y el mapa

**Un gadget se verifica solo, por enumeración y en las dos direcciones, antes de
probar la reducción completa.** Una reducción probada con instancias al azar ve sobre
todo el lado de la respuesta que domina, y en 3-SAT con pocas cláusulas por variable
ese lado es sí. El error de la §9 deja intacto ese lado y rompe el otro, y la
enumeración de 8 casos lo encuentra en el primer intento. Es la regla del capítulo 16,
§13 llevada a la pieza: allí se probaban las dos direcciones de la reducción, aquí se
prueban las del gadget, que son 8 casos y no infinitas fórmulas.

La @fig-red-mapa muestra lo que llevamos demostrado. Cada flecha es una reducción con
su capítulo, y las grises son las del capítulo 19.

```{python continue echo=false output=asis}
print(F18.mapa(ident="red-mapa",
      pie="Las reducciones demostradas hasta este capítulo, con el número del capítulo "
          "en cada flecha. Las grises son las del capítulo 19. Todo lo que está a la "
          "derecha de SAT es NP-completo."))
```

## Resumen

- Una reducción desde 3-SAT representa tres cosas: la elección de cada variable, la
  coherencia entre sus apariciones y que cada cláusula tenga un literal verdadero. Cada
  una es un gadget.
- 3-SAT $\le_p$ CONJUNTO-INDEPENDIENTE: un triángulo por cláusula, un vértice por
  aparición, aristas entre literales opuestos, $k = m$. Un vértice por literal no
  funciona, porque un literal puede ser testigo de dos cláusulas.
- Conjunto independiente, clique y vertex cover son NP-completos. El grafo de Karp para
  clique es el complemento del nuestro.
- VERTEX-COVER $\le_p$ SET-COVER: el universo son las aristas y cada vértice da el
  conjunto de las aristas que toca.
- 3-SAT $\le_p$ 3-COLORACIÓN: la paleta $T, F, B$ nombra los colores, el triángulo
  $x_i, \lnot x_i, B$ hace la elección y la coherencia, y el gadget de cláusula, dos O
  encadenados con la salida unida a $F$ y $B$, se colorea si y solo si algún literal es
  $T$. Tamaño $3 + 2n + 6m$ vértices.
- El O de un triángulo no calcula el O: solo garantiza "$F, F \to F$" y "con una
  entrada $T$, la salida puede ser $T$". Basta.
- Cambiar la entrada del segundo O de $r_1$ a $p_1$ hace que la reducción diga sí a
  toda fórmula. Solo lo ven las instancias no, y la enumeración de los 8 casos del
  gadget.
- Un buen gadget tiene interfaz chica, especificación finita, prohíbe lo justo y tiene
  tamaño constante. Se verifica solo antes que la reducción entera.

## Ejercicios

1. Construye el grafo de conjunto independiente de la §2 para
   $(x_1 \lor x_2 \lor x_3) \land (x_1 \lor \lnot x_2 \lor x_4) \land
   (\lnot x_1 \lor x_3 \lor \lnot x_4) \land (x_2 \lor x_3 \lor x_4)$. Encuentra a mano
   un independiente de tamaño 4 y lee la asignación. Después construye el grafo del
   primer intento, con un vértice por literal: ¿tiene un independiente de tamaño 4?

2. Implementa la enumeración de la §7 de forma que, para cada una de las 12 aristas del
   gadget, construya el gadget sin esa arista y diga en cuáles de los 8 casos cambia la
   respuesta. ¿Hay aristas que sobran? Para cada una que sobre, explica con el lema 4
   por qué, y di si la demostración del lema 5 la usaba.

3. Demuestra 3-COLORACIÓN $\le_p$ 4-COLORACIÓN, y deduce que $k$-COLORACIÓN es
   NP-completo para todo $k \ge 3$. Escribe las dos direcciones.

4. En **hitting set** se da un universo $U$, una familia de subconjuntos
   $A_1, \dots, A_t$ y un $k$, y se pregunta si hay $H \subseteq U$ con $|H| \le k$ que
   corte a todos los $A_i$. Demuestra SET-COVER $\le_p$ HITTING-SET y
   HITTING-SET $\le_p$ SET-COVER. Después, escribe VERTEX-COVER como un caso particular
   de hitting set y di qué tamaño tienen sus conjuntos.

5. Un **conjunto dominante** de $G$ es un $D \subseteq V$ tal que todo vértice está en
   $D$ o tiene un vecino en $D$. Demuestra que DOMINANTE ("¿hay uno de tamaño a lo sumo
   $k$?") es NP-completo reduciendo desde vertex cover. Pista: agrega un vértice por
   arista. Cuidado con los vértices que en $G$ no tienen aristas.

6. Dos cambios de hipótesis. (a) 2-COLORACIÓN está en P. Intenta repetir la §6 con dos
   colores y di qué pieza de la construcción no existe. (b) El teorema de König dice que
   en un grafo bipartito el menor vertex cover tiene el tamaño del mayor emparejamiento.
   Úsalo con el capítulo 13, §12 para decidir conjunto independiente en bipartitos en
   tiempo polinomial. ¿Por qué no contradice el corolario 2? Señala qué parte del grafo
   de la §2 no puede estar en un grafo bipartito.

7. Un compañero cambia el final del gadget: une $r_2$ a $T$ y a $B$ en lugar de a $F$ y
   a $B$. Encuentra **todos** los casos de $(a, b, c)$ en los que la respuesta del
   gadget es la equivocada y di, en cada uno, si se equivoca coloreando de más o de
   menos. ¿Qué respondería la reducción con este gadget para una fórmula cuyos
   literales son todos positivos?

8. Una facultad tiene que poner los exámenes finales en 3 franjas horarias, y dos
   asignaturas con un estudiante en común no pueden ir en la misma franja. Modela el
   problema como coloración de un grafo. Un colega dice que, como 3-COLORACIÓN es
   NP-completo, decidir si los exámenes caben en 3 franjas es difícil. ¿Qué reducción
   hace falta para afirmarlo, en qué dirección, y existe?

9. Demuestra que CLIQUE ("¿hay un clique de tamaño al menos $k$?") está en P si se
   restringe a grafos de grado máximo 3. Da el algoritmo y su costo. El teorema 4 del
   capítulo 16 transforma clique en conjunto independiente con el complemento: ¿por qué
   eso no da que conjunto independiente esté en P en grafos de grado máximo 3?

10. ★ Demuestra que VERTEX-COVER sigue siendo NP-completo en grafos de grado máximo 3.
    Parte del ejercicio 6 del capítulo 17 (3-SAT con cada variable a lo sumo tres veces,
    con cláusulas de dos o tres literales) en la forma que da su pista, adapta la §2 a
    cláusulas de dos literales y cuenta el grado de cada vértice del grafo. ¿Qué pasaría
    con el grado si la fórmula solo cumpliera "cada variable a lo sumo tres veces", sin
    la forma de la pista?
