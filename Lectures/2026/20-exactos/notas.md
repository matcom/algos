# Resolver exacto un problema NP-duro {#chap-exactos}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_20.py
import figuras_20 as F20
```

Los capítulos 16 a 19 terminaron con una lista de problemas NP-completos: conjunto
independiente, vertex cover, mochila y ocho más. Por el capítulo 16, §12, si
$P \ne NP$ ninguno tiene un algoritmo polinomial en el peor caso. Pero eso no obliga a
probar las $2^n$ soluciones. Este capítulo da tres maneras de no probarlas todas,
cada una con una garantía distinta, y termina con la pregunta de hasta dónde se puede
llegar: una hipótesis sobre 3-SAT que, si es cierta, pone un piso a cuánto se puede
bajar la exponencial.

## 1. Tres maneras de no probarlo todo

Un algoritmo **exacto** devuelve siempre la respuesta óptima. Ya viste uno que mejora
la fuerza bruta: Held-Karp, en el capítulo 11, §9, resuelve el viajante en
$O(2^n n^2)$ en vez de $(n-1)!$. Sigue siendo exponencial, y no hay contradicción con
nada: lo que la NP-completitud prohíbe (si $P \ne NP$) es lo polinomial, no lo
exponencial pequeño.

Las tres técnicas del capítulo garantizan cosas distintas, y conviene tenerlo claro
desde el principio:

- **Podar** (branch and bound, sobre mochila). Recorre el árbol de todas las
  decisiones, pero no abre un subárbol si una cota demuestra que de ahí no sale nada
  mejor que lo ya encontrado. Garantiza la respuesta exacta y no garantiza nada sobre
  el tiempo.
- **Parametrizar** (vertex cover con $k$ chico). La exponencial deja de depender del
  tamaño del grafo y pasa a depender del tamaño $k$ de la solución: $O(2^k (n + m))$.
- **Bajar la base** (conjunto independiente). El algoritmo sigue siendo exponencial en
  $n$, pero con una base demostrada menor que 2.

## 2. Mochila: el árbol de decisiones

La mochila 0-1 del capítulo 19, §11: hay $n$ objetos, el objeto $i$ pesa $p_i$ y vale
$v_i$, enteros positivos, y la mochila aguanta $W$. Se busca el subconjunto de mayor
valor con peso total a lo sumo $W$. La programación dinámica de Estructuras de Datos
la resuelve en $O(nW)$, que es exponencial en el tamaño de la entrada, porque $W$ se
escribe con $\log_2 W$ bits.

Todas las soluciones forman un árbol binario: en el nivel $i$ se decide el objeto $i$,
meterlo o no. Tiene $2^n$ hojas y $2^{n+1} - 1$ nodos. La idea para no recorrerlo
entero: si en un nodo ya sabes que lo mejor que puede salir de ahí no supera lo mejor
que has visto, no hace falta abrirlo. Para eso hace falta una **cota superior** del
valor de cualquier forma de completar el nodo, que sea barata de calcular.

La cota que usamos es la de la mochila fraccionaria, que se explica en la §3. El
código ordena los objetos por densidad $v_i / p_i$ de mayor a menor, decide en ese
orden y, en cada nodo, suma a lo ya ganado el valor que se obtiene llenando la
capacidad restante con los objetos que faltan, por orden, y partiendo el primero que
no cabe.

```{python continue}
def mochila_bb(pesos, valores, W, ordenar=True, podar=True, registro=None):
    n = len(pesos)
    orden = list(range(n))
    if ordenar:
        orden.sort(key=lambda i: valores[i] / pesos[i], reverse=True)
    p = [pesos[i] for i in orden]
    v = [valores[i] for i in orden]
    mejor, nodos = 0, 0

    def cota(i, cap):              # mochila fraccionaria sobre los objetos i, i+1, ...
        total = 0
        for j in range(i, n):
            if p[j] <= cap:
                cap -= p[j]
                total += v[j]
            else:
                return total + v[j] * cap / p[j]
        return total

    def rama(i, cap, val, padre, etiqueta):
        nonlocal mejor, nodos
        nodos += 1
        yo = nodos
        mejor = max(mejor, val)
        c = val + cota(i, cap) if i < n else val
        estado = "hoja" if i == n else "abre"
        if i < n and podar and c <= mejor:
            estado = "poda"
        if registro is not None:
            registro.append(dict(id=yo, padre=padre, etiqueta=etiqueta,
                                 val=val, cota=c, estado=estado))
        if estado != "abre":
            return
        if p[i] <= cap:
            rama(i + 1, cap - p[i], val + v[i], yo, f"+{orden[i]}")
        rama(i + 1, cap, val, yo, f"-{orden[i]}")

    rama(0, W, 0, None, "raíz")
    return mejor, nodos

def mochila_dp(pesos, valores, W):
    mejor = [0] * (W + 1)
    for p, v in zip(pesos, valores):
        for c in range(W, p - 1, -1):
            mejor[c] = max(mejor[c], mejor[c - p] + v)
    return mejor[W]

def instancia(rng, n, maxw=20):
    p = [rng.randint(1, maxw) for _ in range(n)]
    v = [rng.randint(1, maxw) for _ in range(n)]
    return p, v, sum(p) // 2

rng = random.Random(1)
for _ in range(2000):
    p, v, W = instancia(rng, rng.randint(1, 10))
    assert mochila_bb(p, v, W)[0] == mochila_dp(p, v, W)
    assert mochila_bb(p, v, W, podar=False)[0] == mochila_dp(p, v, W)
print("2000 instancias con n <= 10: con poda y sin poda, igual que la DP")
```

Fíjate en dos detalles. La rama de meter el objeto solo se crea si cabe, así que cada
nodo es una solución parcial factible. Y la poda compara con `<=`: si la cota empata
con lo mejor visto, abrir el nodo no puede mejorar el valor.

## 3. La cota de la mochila fraccionaria

En la **mochila fraccionaria** se puede meter una fracción $x_i \in [0, 1]$ de cada
objeto, que pesa $x_i p_i$ y vale $x_i v_i$. Es la misma pregunta con más soluciones
permitidas.

**Lema 1.** El óptimo fraccionario es al menos el óptimo 0-1.

*Demostración.* Una solución 0-1 es una fraccionaria con todos los $x_i$ en
$\{0, 1\}$, así que el máximo fraccionario se toma sobre un conjunto que contiene al
otro. $\square$

**Lema 2.** Si $v_1/p_1 \ge v_2/p_2 \ge \dots \ge v_n/p_n$, el goloso que mete los
objetos enteros en ese orden y parte el primero que no cabe da el óptimo fraccionario.

*Demostración.* Si todos los objetos caben, el goloso los mete todos y no se puede
hacer más. Si no, el goloso da $x_i = 1$ para $i < j$, una fracción $x_j \in [0, 1)$ y
$x_i = 0$ para $i > j$, con peso total exactamente $W$. Sea $y$ cualquier solución
fraccionaria, y escribe $d_i = v_i / p_i$. Entonces
$$\sum_i v_i (x_i - y_i) = \sum_i d_i \, p_i (x_i - y_i).$$
Compara cada término con $d_j \, p_i (x_i - y_i)$. Si $i < j$, $x_i - y_i = 1 - y_i \ge
0$ y $d_i \ge d_j$, así que $d_i p_i (x_i - y_i) \ge d_j p_i (x_i - y_i)$. Si $i > j$,
$x_i - y_i = -y_i \le 0$ y $d_i \le d_j$: multiplicar un número no positivo por algo
menor da algo mayor o igual, y la misma desigualdad vale. Si $i = j$, es una igualdad.
Sumando,
$$\sum_i v_i (x_i - y_i) \ge d_j \sum_i p_i (x_i - y_i) = d_j \Big(W - \sum_i p_i
y_i\Big) \ge 0,$$
porque $y$ pesa a lo sumo $W$. $\square$

El paso que todo el mundo se salta está en "$d_i \ge d_j$ si $i < j$". Es el único
lugar donde se usa el orden, y la §5 muestra qué pasa cuando falta.

**Teorema 3.** `mochila_bb` devuelve el valor óptimo.

*Demostración.* Todo valor que guarda `mejor` es el de una solución factible, así que
el resultado no supera el óptimo. Para la otra desigualdad, toma una solución óptima y
su camino en el árbol. Si la búsqueda llega a su hoja, `mejor` alcanza el óptimo. Si
no, algún nodo del camino se podó, con `mejor` $\ge$ `val` + cota en ese momento. Los
objetos que faltan en ese nodo están ordenados por densidad, así que por los lemas 1
y 2 la cota es al menos el valor de cualquier forma 0-1 de completarlo, en particular
de la que lleva a la solución óptima. Entonces `mejor` ya era al menos el óptimo, y
nunca baja. $\square$

## 4. El experimento

Lo que no dice el teorema es cuánto se ahorra. Medimos los nodos visitados, con la
cota y sin ella, en el peor de 20 instancias al azar por tamaño, con pesos y valores
entre 1 y 100.

```{python continue output=asis}
rng = random.Random(2)
print("| $n$ | nodos con cota | nodos sin cota | $2^{n+1} - 1$ |\n|---:|---:|---:|---:|")
for n in [10, 15, 20, 25, 30]:
    con = sin = 0
    for _ in range(20):
        p, v, W = instancia(rng, n, 100)
        con = max(con, mochila_bb(p, v, W)[1])
        if n <= 15:
            sin = max(sin, mochila_bb(p, v, W, podar=False)[1])
    print(f"| {n} | {con} | {sin if sin else '—'} | {2 ** (n + 1) - 1} |")
```

Sin cota, el árbol solo se recorta por los objetos que no caben, y con $n = 15$ ya
pasa de cuarenta mil nodos. Con cota, los nodos crecen muy despacio en esta
distribución: el peor caso de cada fila queda en a lo sumo unos cientos. La @fig-exactos-bb
muestra el árbol completo de una instancia de 6 objetos.

```{python continue echo=false output=asis}
p6 = [5, 11, 10, 4, 7, 11]
v6 = [9, 12, 11, 3, 11, 2]
W6 = sum(p6) // 2
reg6 = []
opt6, nodos6 = mochila_bb(p6, v6, W6, registro=reg6)
podas6 = sum(r["estado"] == "poda" for r in reg6)
sin6 = mochila_bb(p6, v6, W6, podar=False)[1]
assert opt6 == mochila_dp(p6, v6, W6)
print(F20.arbol_bb(reg6, pie=(
    f"Branch and bound sobre pesos {tuple(p6)}, valores {tuple(v6)} y W = {W6}. "
    f"Cada nodo muestra lo ganado (arriba) y la cota fraccionaria (abajo); las "
    f"aristas dicen qué objeto entra (+) o queda fuera (−), numerados desde 0 como en el "
    f"código y decididos en orden de densidad. "
    f"Los nodos con ✗ se podaron. Son {nodos6} nodos, {podas6} podados, y el "
    f"óptimo es {opt6}. Sin la cota se visitan {sin6}.")))
```

Mira la raíz: su cota, 33,2, es el valor de la mochila fraccionaria entera. La
primera hoja a la que llega la búsqueda, metiendo objetos por densidad mientras caben,
vale 31, y el óptimo es 32. Cuando la búsqueda vuelve a la raíz, el hijo derecho, el
que deja fuera al objeto 0 (el de mayor densidad, 9/5), tiene cota 29,6 y se poda sin
bajar: es la mitad del árbol, todas las soluciones sin el objeto 0, descartada por un
solo cálculo.

## 5. El error plantado: la cota sin ordenar

La variante parece inocente: la misma función `cota`, pero sobre los objetos en el
orden en que llegaron, sin ordenar por densidad. El código ya la tiene, con
`ordenar=False`. La probamos contra la DP con cinco baterías de 2 000 instancias.

```{python continue}
def bateria(gen, casos=2000):
    rng = random.Random(3)
    malos = 0
    for _ in range(casos):
        p, v, W = gen(rng)
        if mochila_bb(p, v, W, ordenar=False)[0] != mochila_dp(p, v, W):
            malos += 1
    return malos

def iguales(r):                       # valores = pesos, como en el capítulo 19
    p = [r.randint(1, 20) for _ in range(r.randint(1, 10))]
    return p, list(p), sum(p) // 2

def ordenada(r):
    p, v, W = instancia(r, r.randint(1, 10))
    o = sorted(range(len(p)), key=lambda i: v[i] / p[i], reverse=True)
    return [p[i] for i in o], [v[i] for i in o], W

def holgada(r):
    p, v, _ = instancia(r, r.randint(1, 10))
    return p, v, sum(p)

baterias = {
    "al azar, n <= 10": lambda r: instancia(r, r.randint(1, 10)),
    "al azar, n <= 3": lambda r: instancia(r, r.randint(1, 3)),
    "valores iguales a los pesos": iguales,
    "ya ordenadas por densidad": ordenada,
    "capacidad = suma de los pesos": holgada,
}
for nombre, gen in baterias.items():
    print(f"{nombre:32s} {bateria(gen):4d} de 2000 mal")
```

Las instancias al azar lo atrapan, y tres baterías razonables no lo atrapan nunca. La
de valores iguales a los pesos es la que sale de la reducción de suma de subconjuntos
a mochila del capítulo 19, §11: todas las densidades valen 1, cualquier orden es un
orden por densidad, y la variante es correcta ahí. En las ya ordenadas, el orden de
entrada es el bueno. Con capacidad para todo, la cota nunca parte un objeto y vale la
suma de lo que falta, que es una cota superior en cualquier orden.

La instancia más chica que encontró la búsqueda tiene tres objetos:

```{python continue}
reg = []
print("devuelve", mochila_bb([5, 5, 1], [2, 1, 8], 5, ordenar=False, registro=reg)[0],
      "y el óptimo es", mochila_dp([5, 5, 1], [2, 1, 8], 5))
for r in reg:
    print(f"  {r['etiqueta']:5s} ganado {r['val']}  cota {r['cota']:.1f}  {r['estado']}")
```

En el orden de entrada, la cota de la raíz mete el objeto 0 (peso 5, valor 2) y se
queda sin capacidad: dice 2. Lo que calcula es el valor de una solución fraccionaria
**factible**, que puede quedar por debajo del óptimo 0-1, como aquí, o por encima. No
es una cota superior de nada. Al no meter el objeto 0, la cota vuelve a llenar la mochila con el primer
objeto que encuentra, el 1, de valor 1, y poda una rama que contenía al objeto 2, que
vale 8. La demostración lo anunciaba: el lema 2 usa el orden en un solo paso. Sin ese paso,
el número que calcula `cota` deja de ser el óptimo fraccionario, y el lema 1, que
sigue siendo cierto, ya no dice nada de él.

## 6. Lo que la poda no garantiza

El teorema 3 habla de la respuesta. Del tiempo, lo único demostrado es lo obvio: a lo
sumo $2^{n+1} - 1$ nodos, cada uno con $O(n)$ trabajo para la cota. Las tablas de la
§4 son de instancias al azar, y una instancia al azar no es el peor caso. El
ejercicio 10 te pide una familia de instancias donde la poda casi no sirve. Y si
$P \ne NP$, por el capítulo 19 ningún algoritmo exacto para mochila puede ser
polinomial en el peor caso, use la cota que use.

El método viene de la programación entera: Land y Doig lo publicaron en 1960, en "An
Automatic Method of Solving Discrete Programming Problems" (*Econometrica* 28(3),
pp. 497–520). Lo que cambia de un problema a otro es la cota, y la regla para elegirla
es la de la §3: tiene que ser una cota superior demostrada del valor de toda forma de
completar el nodo, por ejemplo el óptimo de una relajación, y no el valor de una
solución que uno sabe construir.

## 7. Vertex cover con $k$ chico

Vertex cover pregunta si un grafo con $n$ vértices y $m$ aristas tiene un conjunto de
a lo sumo $k$ vértices que toque todas las aristas. Es NP-completo (capítulo 16, §10 y
capítulo 18). Pero en muchas aplicaciones $k$ es chico comparado con $n$: un grafo de
conflictos con miles de vértices donde se quieren quitar diez.

Probar todos los conjuntos de tamaño $k$ cuesta $\binom{n}{k} \cdot O(m)$, que es
$O(n^k m)$. Para cada $k$ fijo es polinomial, pero con $k$ en el exponente de $n$, y
la §8 cuenta cuántos conjuntos son en un grafo de 300 vértices.

¿Cómo se le ocurre a uno algo mejor? Mirando una sola arista $\{u, v\}$. Cualquier
cover la toca, así que contiene a $u$ o a $v$. No hace falta adivinar entre $n$
vértices: hay dos opciones, y cada una gasta una unidad del presupuesto $k$.

## 8. El árbol de profundidad $k$

```{python echo=false}
# Cadena nueva: vertex cover no usa nada de la mochila.
import itertools, math, os, random, sys, time
sys.path.insert(0, os.path.abspath(".."))
import figuras_20 as F20
```

```{python continue}
def cover_k(aristas, k, cuenta=None, registro=None, padre=None, etiqueta="raíz"):
    if cuenta is not None:
        cuenta[0] += 1
    yo = len(registro) if registro is not None else None
    if registro is not None:
        registro.append(dict(padre=padre, etiqueta=etiqueta, k=k,
                             arista=aristas[0] if aristas else None))
    if not aristas:
        if registro is not None: registro[yo]["fin"] = "sí"
        return True
    if k == 0:
        if registro is not None: registro[yo]["fin"] = "no"
        return False
    u, v = aristas[0]
    for x in (u, v):
        resto = [(a, b) for a, b in aristas if a != x and b != x]
        if cover_k(resto, k - 1, cuenta, registro, yo, str(x)):
            return True
    return False

def cover_bruta(n, aristas, k):
    return any(all(a in S or b in S for a, b in aristas)
               for t in range(min(k, n) + 1)
               for S in map(set, itertools.combinations(range(n), t)))

rng = random.Random(5)
for _ in range(1500):
    n = rng.randint(1, 8)
    E = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.4]
    for k in range(5):
        c = [0]
        assert cover_k(E, k, c) == cover_bruta(n, E, k)
        assert c[0] <= 2 ** (k + 1) - 1
print("1500 grafos con n <= 8, k = 0..4: igual que la fuerza bruta, "
      "y nunca más de 2^(k+1) - 1 nodos")
```

**Teorema 4.** `cover_k(E, k)` responde si el grafo de aristas $E$ tiene un vertex
cover de tamaño a lo sumo $k$, en tiempo $O(2^k (n + m))$.

*Demostración.* Correctitud, por inducción en $k$. Sin aristas, el conjunto vacío es
un cover, y la respuesta sí es correcta. Con aristas y $k = 0$, ningún conjunto vacío
las cubre, y la respuesta no es correcta. Si $k > 0$ y $\{u, v\} \in E$: si hay un
cover $S$ con $|S| \le k$, contiene a $u$ o a $v$; digamos $u$. Entonces
$S - \{u\}$ cubre todas las aristas que no tocan a $u$, que son las de `resto`, con
$|S - \{u\}| \le k - 1$, y por inducción la llamada sobre $u$ dice sí. Al revés, si
la llamada sobre $x \in \{u, v\}$ dice sí, por inducción hay un cover $S'$ de `resto`
con $|S'| \le k - 1$, y $S' \cup \{x\}$ cubre $E$: las aristas que faltaban en
`resto` son justo las que tocan a $x$.

Costo: cada llamada hace a lo sumo dos llamadas con $k - 1$, así que el árbol de
llamadas es binario de profundidad a lo sumo $k$ y tiene a lo sumo
$1 + 2 + \dots + 2^k = 2^{k+1} - 1$ nodos. Fuera de sus llamadas, cada nodo filtra la lista de
aristas a lo sumo dos veces, en tiempo $O(m)$. El total es $O(2^k m)$, que está en
$O(2^k (n + m))$. $\square$

La @fig-exactos-cover muestra el árbol en el ciclo de 7 vértices con $k = 3$. Un ciclo
de 7 necesita 4 vértices, así que la respuesta es no y el árbol sale completo.

```{python continue echo=false output=asis}
ciclo = [(i, (i + 1) % 7) for i in range(7)]
ciclo = [tuple(sorted(e)) for e in ciclo]
regc, cc = [], [0]
res = cover_k(ciclo, 3, cc, regc)
assert res is False and cc[0] == 2 ** 4 - 1
print(F20.arbol_cover(regc, pie=(
    f"El árbol de búsqueda de cover_k en el ciclo 0–1–…–6–0 con k = 3. Cada nodo "
    f"interno muestra la primera arista que queda; las aristas del árbol, el vértice "
    f"que se mete en el cover. Las {sum(r.get('fin') == 'no' for r in regc)} hojas "
    f"llegan a k = 0 con aristas sin cubrir. Son {cc[0]} nodos, 2⁴ − 1.")))
```

¿Cuánto se acerca la cota de nodos a lo que pasa? En un grafo de 300 vértices con un
cover plantado de tamaño $k$ (cada vértice del cover se une a 40 vértices al azar),
preguntamos por $k$, que es sí, y por $k - 1$, que es no.

```{python continue}
rng = random.Random(8)
n = 300
for k in [4, 6, 8, 10]:
    C = rng.sample(range(n), k)
    E = sorted({tuple(sorted((c, x))) for c in C
                for x in rng.sample(range(n), 40) if x != c})
    for kk in (k, k - 1):
        c = [0]
        t = time.perf_counter()
        r = cover_k(E, kk, c)
        t = time.perf_counter() - t
        print(f"m = {len(E)}  k = {kk:2d}  {'sí' if r else 'no'}  "
              f"nodos {c[0]:5d}  2^(k+1) - 1 = {2 ** (kk + 1) - 1:5d}  {t:.3f} s")
print(f"fuerza bruta con k = 10: binom(300, 10) = {math.comb(300, 10):.2e} conjuntos")
```

En todas las filas el árbol sale completo, también cuando la respuesta es sí. Como
`cover_k` se detiene en cuanto encuentra un cover, un árbol completo con respuesta sí
quiere decir que lo encontró en la última hoja que visita. El teorema 4 da el techo,
y aquí se alcanza. Con $k = 10$ son unas dos mil llamadas en un grafo de
cientos de aristas, contra los $\binom{300}{10}$, unos $1{,}4 \cdot 10^{18}$, de la
fuerza bruta.

## 9. Complejidad parametrizada

El teorema 4 es el primer ejemplo de una clase con nombre. Un problema con un
parámetro $k$ es **tratable con parámetro fijo** (FPT, por *fixed-parameter
tractable*) si se resuelve en tiempo $f(k) \cdot n^{O(1)}$, con $f$ cualquier función
que dependa solo de $k$. La diferencia con $O(n^k)$ es dónde está el $k$: en FPT, el
grado del polinomio no crece con $k$, y para cada $k$ fijo el algoritmo escala como un
polinomio fijo.

Dos observaciones. La primera: la reducción del capítulo 16,
§10, $(G, k) \mapsto (G, n - k)$, lleva conjunto independiente a vertex cover
preservando la respuesta. No por eso conjunto independiente con parámetro $k$ hereda
el teorema 4, y el ejercicio 8 te pide ver qué se rompe. La segunda: la base 2 del
teorema 4 sale de ramificar en una arista cualquiera. Con reglas de ramificación más
finas se baja. Chen, Kanj y Xia, en "Improved Upper Bounds for Vertex Cover"
(*Theoretical Computer Science* 411(40–42), pp. 3736–3756, 2010), llegan a
$O(1{,}2738^k + kn)$ con espacio polinomial.

Otra idea de la misma familia es el **kernel**: en tiempo polinomial, reducir la
instancia a una equivalente de tamaño acotado por una función de $k$, y después
resolver esa. El ejercicio 3 construye un kernel de vertex cover con $O(k^2)$ aristas.

## 10. Conjunto independiente: ramificar en un vértice

Volvemos a medir en $n$. Para el conjunto independiente máximo, la fuerza bruta prueba
$2^n$ subconjuntos. La ramificación más simple también da $2^n$: tomar un vértice $v$
y probar con $v$ y sin $v$. Para bajar la base hay que ganar algo en una de las dos
ramas, y la rama que mete a $v$ gana: borra $v$ y todos sus vecinos, $N[v]$, porque
ninguno puede acompañarlo. Si $v$ tiene grado $d$, esa rama baja a $n - 1 - d$
vértices. Con $d \ge 3$, a $n - 4$ o menos.

¿Y si ningún vértice tiene grado 3 o más? Entonces el grafo es fácil.

**Lema 5.** Si todo vértice tiene grado a lo sumo 2, cada componente conexa es un
camino o un ciclo, y el conjunto independiente máximo tiene $\lceil c/2 \rceil$
vértices en un camino de $c$ vértices y $\lfloor c/2 \rfloor$ en un ciclo de $c$.

*Demostración.* Una componente conexa con grados a lo sumo 2 es un camino o un ciclo:
si tiene un vértice de grado a lo sumo 1, se recorre desde él sin volver, y si todos
tienen grado 2, el recorrido vuelve al inicio. En un camino $u_1 u_2 \dots u_c$, los
de posición impar son independientes, $\lceil c/2 \rceil$. No hay más: los pares
$\{u_1, u_2\}, \{u_3, u_4\}, \dots$ (más $\{u_c\}$ solo si $c$ es impar) son
$\lceil c/2 \rceil$ grupos, y cada uno aporta a lo sumo un vértice. En un ciclo de
$c \ge 3$, si $S$ es independiente, el sucesor de cada vértice de $S$ en el ciclo no
está en $S$; esos sucesores son distintos, así que $2|S| \le c$. Y $\lfloor c/2
\rfloor$ se alcanza con posiciones alternas, dejando sin usar la última si $c$ es
impar. Las componentes no comparten aristas, y los máximos se suman. $\square$

**Lema 6.** Para todo vértice $v$,
$I(G) = \max\big(I(G - v),\; 1 + I(G - N[v])\big)$, donde $I(G)$
es el tamaño del conjunto independiente máximo.

*Demostración.* Las dos expresiones son tamaños de conjuntos independientes de $G$:
uno de $G - v$ lo es, y uno de $G - N[v]$ más $v$ también, porque $v$ no tiene vecinos
fuera de $N[v]$. Así que el máximo no supera $I(G)$. Al revés, toma $S$ máximo.
Si $v \notin S$, $S$ es independiente en $G - v$. Si $v \in S$, ningún vecino de $v$
está en $S$, y $S - \{v\}$ es independiente en $G - N[v]$. $\square$

El código usa máscaras de bits para los conjuntos de vértices. Elige el vértice de
grado máximo. Si ese grado es a lo sumo 2, aplica el lema 5. Si no, aplica el lema 6.

```{python echo=false}
# Cadena nueva: conjunto independiente no usa nada de lo anterior.
import itertools, math, os, random, sys
sys.path.insert(0, os.path.abspath(".."))
import figuras_20 as F20
```

```{python continue}
def independiente_max(n, aristas):
    vec = [0] * n
    for a, b in aristas:
        vec[a] |= 1 << b
        vec[b] |= 1 << a
    llamadas = 0

    def caminos_y_ciclos(S, g):            # lema 5, componente por componente
        total, vistos = 0, 0
        for x in range(n):
            if S >> x & 1 and not vistos >> x & 1:
                comp, pila = 0, [x]
                vistos |= 1 << x
                while pila:
                    y = pila.pop()
                    comp |= 1 << y
                    r = vec[y] & S & ~vistos
                    while r:
                        z = (r & -r).bit_length() - 1
                        r &= r - 1
                        vistos |= 1 << z
                        pila.append(z)
                c = bin(comp).count("1")
                e = sum(g[y] for y in range(n) if comp >> y & 1) // 2
                total += c // 2 if e == c else (c + 1) // 2
        return total

    def rec(S):
        nonlocal llamadas
        llamadas += 1
        if not S:
            return 0
        g = {x: bin(vec[x] & S).count("1") for x in range(n) if S >> x & 1}
        v = max(g, key=lambda x: g[x])
        if g[v] <= 2:
            return caminos_y_ciclos(S, g)
        sin_v = rec(S & ~(1 << v))
        con_v = 1 + rec(S & ~(1 << v) & ~vec[v])       # lema 6
        return max(sin_v, con_v)

    return rec((1 << n) - 1), llamadas

def independiente_bruta(n, aristas):
    return max(len(S) for t in range(n + 1)
               for S in itertools.combinations(range(n), t)
               if not any(a in S and b in S for a, b in aristas))

rng = random.Random(6)
for _ in range(600):
    n = rng.randint(1, 12)
    E = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.35]
    assert independiente_max(n, E)[0] == independiente_bruta(n, E)
print("600 grafos con n <= 12: igual que la fuerza bruta")
```

En un camino, la componente tiene $c - 1$ aristas, y en un ciclo, $c$. Por eso el
código distingue los dos casos comparando aristas con vértices.

## 11. La recurrencia

Primero el experimento. Contamos las llamadas a `rec` en grafos al azar de grado medio
cercano a 4, el peor de 10 por tamaño, y las ponemos junto a dos números: $2^n$, y la
solución de
$$C(n) = 1 + C(n - 1) + C(n - 4) \text{ para } n \ge 4, \qquad C(n) = 1 \text{ para }
n \le 3,$$
que es lo que daría la rama del lema 6 si cada llamada bajara exactamente a $n - 1$ y
$n - 4$.

```{python continue}
C = [1, 1, 1, 1]
for n in range(4, 41):
    C.append(1 + C[n - 1] + C[n - 4])
alfa = 1.5
for _ in range(60):                      # raíz de x^4 = x^3 + 1, por Newton
    alfa -= (alfa ** 4 - alfa ** 3 - 1) / (4 * alfa ** 3 - 3 * alfa ** 2)
print(f"alfa = {alfa:.6f}")

rng = random.Random(7)
medidas = []
for n in range(10, 41, 5):
    peor = 0
    for _ in range(10):
        E = [(a, b) for a in range(n) for b in range(a + 1, n)
             if rng.random() < 4 / (n - 1)]
        peor = max(peor, independiente_max(n, E)[1])
    medidas.append((n, peor))
    print(f"n = {n}  llamadas {peor:4d}  C(n) = {C[n]:6d}  "
          f"C(n)/alfa^n = {C[n] / alfa ** n:.3f}  2^n = {2 ** n}")
```

Tres cosas salen de la tabla. Las llamadas medidas quedan muy por debajo de $C(n)$,
y $C(n)$ muy por debajo de $2^n$. Y el cociente $C(n)/\alpha^n$ se estabiliza, lo que
propone que $C(n)$ crece como $\alpha^n$. Eso es lo que hay que demostrar.

**Teorema 7.** Sea $\alpha$ la única raíz real mayor que 1 de $x^4 = x^3 + 1$. En un
grafo de $n$ vértices, `independiente_max` hace a lo sumo $C(n) < 2 \alpha^n$
llamadas, y corre en tiempo $O(\alpha^n (n + m))$.

*Demostración.* La raíz es única: $f(x) = x^4 - x^3 - 1$ vale $-1$ en $x = 1$, tiende
a infinito, y $f'(x) = x^2 (4x - 3) > 0$ para $x \ge 1$.

$C$ no decrece: para $n \ge 4$, $C(n) = 1 + C(n-1) + C(n-4) > C(n-1)$. Ahora, por
inducción en $n$, las llamadas $L(G)$ sobre un grafo de $n$ vértices son a lo sumo
$C(n)$. Si el grado máximo es a lo sumo 2 (en particular si $n \le 3$), hay una sola
llamada. Si no, $n \ge 4$, $v$ tiene grado $d \ge 3$ y
$$L(G) = 1 + L(G - v) + L(G - N[v]) \le 1 + C(n - 1) + C(n - 1 - d)
\le 1 + C(n - 1) + C(n - 4) = C(n),$$
usando la inducción y que $C$ no decrece.

Para resolver $C$, el $+1$ estorba. El truco es sumarle 1. Si $D(n) = C(n) + 1$, para
$n \ge 4$
$$D(n) = C(n) + 1 = \big(C(n-1) + 1\big) + \big(C(n-4) + 1\big) = D(n-1) + D(n-4),$$
y $D(n) = 2$ para $n \le 3$. Por inducción,
$D(n) \le 2\alpha^n$: para $n \le 3$, $2 \le 2\alpha^n$ porque $\alpha > 1$; para
$n \ge 4$,
$$D(n) \le 2\alpha^{n-1} + 2\alpha^{n-4} = 2\alpha^{n-4}(\alpha^3 + 1) =
2\alpha^{n-4} \alpha^4 = 2\alpha^n.$$
Así $C(n) = D(n) - 1 < 2\alpha^n$. Implementada con listas de adyacencia, cada
llamada calcula grados, borra vértices o recorre caminos y ciclos en $O(n + m)$.
$\square$

El código de la §10 usa máscaras de bits, y lo que medimos son sus llamadas, no su
tiempo.

La tabla imprimió $\alpha = 1{,}380278$. Ojo con el redondeo: es **mayor** que
$1{,}38$, y $O(1{,}38^n)$ no es lo que se demostró, porque $(1{,}380278/1{,}38)^n$
crece sin límite. Lo correcto es $O(1{,}3803^n)$, redondeando hacia arriba.

```{python continue echo=false output=asis}
series = {
    "2ⁿ": [(n, 2 ** n) for n, _ in medidas],
    "C(n)": [(n, C[n]) for n, _ in medidas],
    "medidas": medidas,
}
print(F20.grafica_semilog(series, "vértices n", "llamadas", pie=(
    f"Llamadas de independiente_max en el peor de 10 grafos al azar de grado medio "
    f"cercano a 4, contra la cota C(n) del teorema 7 y contra 2ⁿ, con la y en escala "
    f"logarítmica. En n = {medidas[-1][0]}, {medidas[-1][1]} llamadas medidas, "
    f"C(n) = {C[medidas[-1][0]]} y 2ⁿ = {2 ** medidas[-1][0]}.")))
```

En la @fig-exactos-llamadas las tres curvas son casi rectas, y la pendiente es la base.
Las medidas quedan lejos de $C(n)$, y eso no contradice nada: el teorema 7 es una cota
superior sobre todos los grafos, y un grafo al azar no es el peor caso. Este capítulo no demuestra que algún grafo alcance
$C(n)$.

Tarjan y Trojanowski publicaron en 1977 un algoritmo en
$O(2^{n/3})$, "Finding a Maximum Independent Set" (*SIAM Journal on Computing* 6(3),
pp. 537–546), con reglas de ramificación más finas. Xiao y Nagamochi, en "Exact
Algorithms for Maximum Independent Set" (*Information and Computation* 255,
pp. 126–146, 2017), llegan a $1{,}1996^n n^{O(1)}$ con espacio polinomial. El
ejercicio 5 da el primer paso en esa dirección.

## 12. ETH y SETH

¿Se puede bajar la base todo lo que se quiera, hasta un algoritmo en $2^{o(n)}$? Nadie
lo sabe, y la respuesta estándar es una hipótesis.

Impagliazzo y Paturi, en "On the Complexity of $k$-SAT" (*Journal of Computer and
System Sciences* 62(2), pp. 367–375, 2001), definen para cada $k \ge 3$
$$s_k = \inf\{\delta : k\text{-SAT se resuelve en tiempo } O(2^{\delta n})\},$$
con $n$ el número de variables. La fuerza bruta da $s_k \le 1$, y como una fórmula de
$k$-SAT es también una de $(k+1)$-SAT, $s_k \le s_{k+1}$. La **hipótesis del tiempo
exponencial** (ETH) dice que $s_3 > 0$. Implica lo que anunció el capítulo 17, §11: no
hay algoritmo para 3-SAT en tiempo $2^{o(n)}$, porque uno así correría en
$O(2^{\delta n})$ para todo $\delta > 0$.

Para pasar la ETH a conjunto independiente, la idea es la reducción del capítulo 18,
§2: una fórmula de 3-SAT con $m$ cláusulas da un grafo con a lo sumo $3m$ vértices. Un
algoritmo en $2^{o(N)}$ para conjunto independiente, con $N$ vértices, daría uno en
$2^{o(m)}$ para 3-SAT. Pero la ETH habla de $n$, no de $m$, y una fórmula de 3-SAT
puede tener del orden de $n^3$ cláusulas distintas. Hace falta un resultado que
permita suponer $m = O(n)$.

**Lema de esparcimiento** (Impagliazzo, Paturi y Zane, "Which Problems Have Strongly
Exponential Complexity?", *Journal of Computer and System Sciences* 63(4),
pp. 512–530, 2001). Para todo $k$ y todo $\varepsilon > 0$ hay una constante
$c = c(k, \varepsilon)$ tal que toda fórmula $F$ de $k$-SAT con $n$ variables se escribe
como una disyunción $F = F_1 \lor \dots \lor F_t$ con $t \le 2^{\varepsilon n}$, donde
cada $F_i$ es de $k$-SAT sobre las mismas variables y cada variable aparece en a lo
sumo $c$ cláusulas de $F_i$. Las $F_i$ se calculan en tiempo
$\mathrm{poly}(n) \, 2^{\varepsilon n}$.

No lo demostramos. Lo que importa es la consecuencia: cada $F_i$ tiene a lo sumo $cn$
cláusulas, porque cada cláusula contiene alguna variable y cada variable está en a lo
sumo $c$. Las cláusulas de las $F_i$ pueden tener menos de tres literales; se completan
repitiendo uno, lo que no cambia qué asignaciones las satisfacen, y la reducción del
capítulo 18 recibe cláusulas de exactamente tres.

**Teorema 8.** Si se cumple la ETH, conjunto independiente no se resuelve en tiempo
$2^{o(N)}$ en grafos de $N$ vértices.

*Demostración.* Supón un algoritmo $A$ que lo resuelve en tiempo $2^{g(N)}$ con
$g(N)/N \to 0$. Fija $\varepsilon > 0$ y sea $c = c(3, \varepsilon)$. Dada una fórmula
$F$ de 3-SAT con $n$ variables, el lema la parte en $t \le 2^{\varepsilon n}$
fórmulas, cada una con a lo sumo $cn$ cláusulas. La reducción del capítulo 18 lleva
cada $F_i$ a un grafo de $N_i \le 3cn$ vértices en tiempo polinomial, y $A$ decide si
tiene un independiente de tamaño igual al número de cláusulas. $F$ es satisfacible si y
solo si alguna $F_i$ lo es. Como $g(N)/N \to 0$, para $n$ grande
$g(N_i) \le \varepsilon n$ (si $N_i$ es chico, $A$ tarda una constante). El total es
$$\mathrm{poly}(n) \, 2^{\varepsilon n} \cdot 2^{\varepsilon n} = O(2^{3\varepsilon
n}).$$
Esto vale para todo $\varepsilon > 0$, así que $s_3 = 0$, contra la ETH. $\square$

Por el lema 5 del capítulo 16, lo mismo vale para vertex cover en función del número
de vértices: el grafo es el mismo. El ejercicio 9 lo lleva al parámetro $k$.

Fíjate en lo que el teorema **no** dice. No dice que la base $1{,}1996$ de Xiao y
Nagamochi sea la mejor posible, ni da ninguna base concreta. Dice que alguna base
mayor que 1 es inevitable, si la ETH es cierta.

La versión fuerte mira el límite. Como $s_k$ no decrece y no pasa de 1, tiene límite
$s_\infty$. La **hipótesis fuerte del tiempo exponencial** (SETH) dice que
$s_\infty = 1$: para todo $\varepsilon > 0$ hay un $k$ tal que $k$-SAT no se resuelve
en $O(2^{(1 - \varepsilon)n})$. Impagliazzo y Paturi la dejan como problema abierto
en la versión de conferencia de su artículo (CCC 1999). Si es cierta, para cláusulas
largas la fuerza bruta es esencialmente lo mejor posible. Es más fuerte que la ETH y
menos aceptada, y el epílogo vuelve sobre las cotas que dependen de ella.

## 13. La regla

Las tres técnicas del capítulo dieron tres garantías distintas. La poda garantiza la
respuesta, con una demostración que vive en la cota, y no garantiza el tiempo. El
parámetro saca la exponencial de $n$ y la pone en $k$. La recurrencia da una base, y
el error de redondeo de la §11 muestra que una base es un número que se demuestra, no
uno que se recuerda.

La regla: **una garantía de tiempo de un algoritmo exacto es una recurrencia
demostrada, no una poda que anduvo bien en las pruebas.** Y su compañera, la de la
§5: **una cota para podar tiene que ser una cota superior demostrada, como el óptimo
de una relajación, y el paso de la demostración que lo asegura es el que se rompe en
silencio.**

El capítulo 21 renuncia a lo exacto: algoritmos polinomiales con una garantía de
cuánto se alejan del óptimo, empezando por un vertex cover de razón 2.

## Resumen

- Un algoritmo exacto para un problema NP-duro puede mejorar la fuerza bruta sin
  contradecir $P \ne NP$: lo prohibido es el tiempo polinomial, no una exponencial
  menor.
- Branch and bound poda un subárbol cuando una cota superior de su valor no supera lo
  mejor visto. Es exacto si la cota es válida, y no da garantía de tiempo.
- Para mochila, la cota es la mochila fraccionaria, que el goloso por densidad
  resuelve (lema 2). Calculada sin ordenar no es una cota superior: puede quedar por
  debajo del óptimo y podar ramas buenas, y las baterías con valores iguales a los
  pesos no lo detectan.
- Vertex cover con parámetro $k$: una arista obliga a uno de sus dos extremos, y el
  árbol de búsqueda tiene a lo sumo $2^{k+1} - 1$ nodos. $O(2^k (n + m))$ es FPT.
- Conjunto independiente: ramificar en un vértice de grado al menos 3 da
  $C(n) = 1 + C(n-1) + C(n-4)$ y menos de $2 \alpha^n$ llamadas, con
  $\alpha = 1{,}380278$ la raíz de $x^4 = x^3 + 1$. Con grado máximo 2, caminos y
  ciclos se resuelven directo.
- Una base se redondea hacia arriba: $O(1{,}3803^n)$, no $O(1{,}38^n)$.
- ETH: $s_3 > 0$. Con el lema de esparcimiento y la reducción del capítulo 18,
  conjunto independiente y vertex cover no tienen algoritmo en $2^{o(N)}$.
- SETH: $s_k \to 1$. Si vale, para $k$-SAT con $k$ grande la fuerza bruta es
  esencialmente óptima.

## Ejercicios

1. [traza] Corre a mano `mochila_bb` sobre pesos $(8, 8, 2, 6, 10)$, valores
   $(9, 8, 14, 15, 6)$ y $W = 17$. Dibuja el árbol con lo ganado y la cota de cada
   nodo, marca los podados y di cuántos nodos visita. Comprueba tu respuesta con el
   código.

2. [demostración] Demuestra que la cota fraccionaria de un hijo nunca supera la de su
   padre. Demuestra también que si en un nodo la solución fraccionaria del goloso no
   parte ningún objeto, ese nodo no necesita abrirse: su cota es el valor de una
   solución 0-1 que se puede leer directamente.

3. [demostración] Un kernel para vertex cover con parámetro $k$. (a) Demuestra que un
   vértice de grado mayor que $k$ está en todo cover de tamaño a lo sumo $k$. (b) Se
   aplica (a) una y otra vez: mientras haya un vértice de grado mayor que el parámetro
   actual, se mete en el cover, se borra y el parámetro baja en 1. Al final se borran
   los vértices aislados. Demuestra que si en el grafo que queda, con parámetro $k'$,
   hay más de $k'^2$ aristas, la respuesta es no. (c) Concluye un
   algoritmo en $O(n + m + 2^k k^2)$.

4. [demostración] Una regla de ramificación con **vector** $(a, b)$, $1 \le a \le b$,
   produce llamadas que cumplen $T(n) \le 1 + T(n - a) + T(n - b)$. Demuestra que
   $T(n) = O(\beta^n)$, donde $\beta$ es la única raíz mayor que 1 de
   $x^{-a} + x^{-b} = 1$. Calcula $\beta$ para los vectores $(1, 5)$ y $(3, 4)$.

5. [modelar] Mejora `independiente_max` con vértices de grado bajo. (a) Demuestra que
   un vértice de grado 0 o 1 está en algún conjunto independiente máximo, así que se
   puede meter sin ramificar. (b) Sea $v$ de grado 2 con vecinos $u$ y $w$. Demuestra
   que si $u$ y $w$ son adyacentes, hay un máximo que contiene a $v$; y si no lo son,
   hay un máximo que contiene a $v$ o contiene a $u$ y a $w$ a la vez. (c) Escribe el
   vector de la regla (b) cuando todos los grados son al menos 2 y usa el ejercicio 4.
   ¿Mejora la base del teorema 7 del algoritmo completo? Di qué rama manda y qué
   habría que cambiar para mejorarla.

6. [modelar] Suma de subconjuntos (capítulo 19): dados $n$ enteros y un objetivo $T$,
   ¿hay un subconjunto que sume $T$? Parte los números en dos mitades, calcula las
   sumas de cada mitad y combínalas para resolverlo en $O(2^{n/2} \, n)$. Esta idea de
   encuentro a mitad de camino es de Horowitz y Sahni, "Computing Partitions with
   Applications to the Knapsack Problem" (*Journal of the ACM* 21(2), pp. 277–292,
   1974). ★ Quita el factor $n$.

7. [implementar y medir] `mochila_bb` decide los objetos en orden de densidad.
   Escribe una versión que los decida en el orden de entrada pero calcule la cota bien,
   sobre los objetos que faltan ordenados por densidad. Demuestra que sigue siendo
   exacta, y mide los nodos de las dos versiones en las instancias de la §4. Explica la
   diferencia.

8. [cambio de hipótesis] Intenta el esquema del teorema 4 para conjunto independiente
   con parámetro $k$: ¿hay un conjunto de pocos vértices del que alguno tiene que estar
   en la solución? Señala el paso de la demostración que se rompe. Después explica por
   qué la reducción $(G, k) \mapsto (G, n - k)$ del capítulo 16, §10 tampoco lleva el
   teorema 4 a conjunto independiente con parámetro $k$.

9. [demostración] Supón la ETH. Demuestra que vertex cover no se resuelve en tiempo
   $2^{o(k)} \, n^{O(1)}$. Sigue la demostración del teorema 8 y fíjate en cuánto vale
   el parámetro en la instancia que produce la cadena de reducciones.

10. [entrada que rompe] Construye una familia de instancias de mochila, una para cada
    $n$, en la que `mochila_bb` visite al menos $2^n / \mathrm{poly}(n)$ nodos.
    Demuestra la cota y compruébala midiendo.
