# Flujo máximo: push-relabel {#chap-push-relabel}

El capítulo 13 resolvió el flujo máximo manteniendo siempre un flujo válido y
mejorándolo por caminos de aumento. Este capítulo hace la apuesta contraria: durante
casi toda la ejecución lo que tenemos **no es un flujo**. Los vértices pueden recibir
más de lo que sacan, y el algoritmo empuja ese sobrante cuesta abajo, arista por
arista, sin mirar nunca un camino entero. Que algo tan local termine con un flujo
máximo se demuestra con un invariante de una línea, y su costo se cuenta con el
potencial del capítulo 4.

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
import time
from collections import deque

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_14.py
sys.setrecursionlimit(10_000)
import figuras as F
import figuras_14 as G
```

## 1. Otra manera de mover el flujo

Una red, como en el capítulo 13, tiene $V$ vértices, $E$ aristas, un origen $s$, un
destino $t$ y capacidades $c(u, v) \ge 0$. Un flujo respeta las capacidades y, en cada
vértice distinto de $s$ y $t$, saca lo mismo que recibe (conservación).

Un **preflujo** cumple la primera y debilita la segunda: en cada vértice
$u \ne s, t$ entra **al menos** lo que sale. Lo que sobra es el **exceso**,
$$e(u) = \sum_{v} f(v, u) - \sum_{v} f(u, v) \ \ge\ 0,$$
y un vértice con $e(u) > 0$ es **activo**. Un preflujo sin vértices activos es un
flujo. La red residual es la del capítulo 13; en una fórmula, la capacidad residual es
$r(u, v) = c(u, v) - f(u, v) + f(v, u)$, y $(u, v)$ es una arista residual si
$r(u, v) > 0$.

El método es de Goldberg y Tarjan, *A new approach to the maximum-flow problem*
(Journal of the ACM 35(4), 921–940, 1988), que atribuyen la idea del preflujo a
Karzanov.

La imagen que ayuda es la del agua. Cada vértice está a una **altura** $h(u)$, y el
agua solo baja, un escalón por vez; un vértice atascado se levanta lo justo para
volver a tener por dónde bajar. Lo que no cabe por el cuello de botella vuelve a $s$,
y para eso los atascados tendrán que subir por encima de $s$.

## 2. Empujar y reetiquetar

Las reglas son tres.

- **Inicio.** $h(s) = V$ y $h(u) = 0$ para todos los demás. Todas las aristas que salen
  de $s$ se saturan: $f(s, v) = c(s, v)$, y cada $v$ recibe ese exceso.
- **Empujar** desde un vértice activo $u$ por una arista residual $(u, v)$ que sea
  **admisible**, es decir, con $h(u) = h(v) + 1$. Se mandan
  $\delta = \min(e(u), r(u, v))$ unidades. Si $\delta = r(u, v)$ la arista desaparece
  de la red residual y el empuje es **saturante**; si no, $u$ se queda sin exceso y el
  empuje es **no saturante**.
- **Reetiquetar** un vértice activo $u$ que no tiene ninguna arista admisible:
  $$h(u) \leftarrow 1 + \min\{\, h(v) : (u, v) \text{ residual} \,\}.$$

El algoritmo genérico aplica, mientras haya activos, cualquiera de las dos a cualquier
activo. Siempre se puede una de ellas: la §4 demuestra que un activo tiene alguna
arista residual.

En el código, la arista `k` y su inversa `k ^ 1` forman un par: empujar por una es
devolverle capacidad a la otra.

```{python continue}
class Red:
    """Red residual. La arista k llega a dst[k] con capacidad residual cap[k].
    Se guardan en pares: la inversa de k es k ^ 1, con capacidad residual 0 al
    principio."""

    def __init__(self, n):
        self.n = n
        self.ady = [[] for _ in range(n)]   # aristas que salen de cada vértice
        self.dst, self.cap = [], []

    def arista(self, u, v, c):
        for a, b, x in ((u, v, c), (v, u, 0)):
            self.ady[a].append(len(self.dst))
            self.dst.append(b)
            self.cap.append(x)


def red_de(n, aristas):
    R = Red(n)
    for u, v, c in aristas:
        R.arista(u, v, c)
    return R
```

El genérico elige el activo de menor número y la primera arista admisible. Cuenta las
operaciones, puede vigilar el invariante de la §3 y guarda un diario para dibujar.

```{python continue}
def invariante(R, h):
    for u in range(R.n):
        for k in R.ady[u]:
            if R.cap[k] > 0:
                assert h[u] <= h[R.dst[k]] + 1, f"arista residual ({u}, {R.dst[k]})"


def generico(R, s, t, h_s=None, vigilar=False, diario=None):
    n, dst, cap = R.n, R.dst, R.cap
    h, e = [0] * n, [0] * n
    h[s] = n if h_s is None else h_s
    for k in R.ady[s]:                       # saturar todo lo que sale de s
        e[dst[k]] += cap[k]
        cap[k ^ 1] += cap[k]
        cap[k] = 0
    cuenta = {"reetiquetar": 0, "saturante": 0, "no saturante": 0}
    op = "inicio"
    while True:
        if vigilar:
            invariante(R, h)
        if diario is not None:
            diario.append((op, h[:], e[:], cap[:]))
        activos = [v for v in range(n) if v not in (s, t) and e[v] > 0]
        if not activos:
            return e[t], h, cuenta
        u = activos[0]
        for k in R.ady[u]:
            v = dst[k]
            if cap[k] > 0 and h[u] == h[v] + 1:          # admisible: empujar
                d = min(e[u], cap[k])
                cap[k] -= d; cap[k ^ 1] += d
                e[u] -= d; e[v] += d
                op = "saturante" if cap[k] == 0 else "no saturante"
                break
        else:                                            # ninguna: reetiquetar
            h[u] = 1 + min(h[dst[k]] for k in R.ady[u] if cap[k] > 0)
            op = "reetiquetar"
        cuenta[op] += 1
```

Probémoslo en una red de cinco vértices donde $s$ puede soltar 6 unidades pero a $t$
solo le caben 3.

```{python continue}
NOMBRES = "sabct"
EJEMPLO = [(0, 1, 4), (0, 2, 2), (1, 3, 3), (1, 2, 1),
           (2, 3, 1), (2, 4, 1), (3, 4, 2)]
diario = []
valor, h, cuenta = generico(red_de(5, EJEMPLO), 0, 4, vigilar=True, diario=diario)
print("flujo:", valor, "  operaciones:", len(diario) - 1, " ", cuenta)
print("alturas finales:", dict(zip(NOMBRES, h)))
```

```{python continue echo=false output=asis}
_m = [(f"paso {k}", *diario[k][1:]) for k in (0, 12, len(diario) - 1)]
_m[0] = ("al empezar", *diario[0][1:])
_m[2] = (f"al terminar (paso {len(diario) - 1})", *diario[-1][1:])
print(G.alturas(_m, EJEMPLO, NOMBRES, 0, 4, ident="pr-alturas",
      pie="La red del ejemplo con cada vértice a su altura, en tres momentos del "
          "genérico. Los activos van rellenos, con su exceso al lado. Una arista oscura "
          "va saturada, una celeste lleva algo de flujo y una gris nada. La línea roja es "
          "la altura V = 5."))
```

La @fig-pr-alturas cuenta la historia. Al empezar, $a$ y $b$ reciben 6 unidades en el
suelo. Los primeros empujes mandan 4 a $c$ y 1 a $t$, pero de $c$ a $t$ solo caben 2.
Lo que sobra tiene que volver a $s$. La unidad que quedó en $b$ rebota entre $a$ y $b$
por la arista de capacidad 1, dos escalones por vuelta, hasta que $b$ supera a $s$ y se
la devuelve. Después $c$ manda 2 a $t$, sube a 6 y devuelve sus otras 2 unidades por
$a$. Al terminar, $t$ recibió 3, y $a$, $b$ y $c$ quedaron a altura 6, por encima de
$V$. Nada de esto buscó un camino.

## 3. La función de altura

**Invariante.** En todo momento, $h(s) = V$, $h(t) = 0$, y para cada arista residual
$(u, v)$,
$$h(u) \le h(v) + 1.$$
Dicho con agua: ninguna arista residual baja más de un escalón.

*Demostración*, por inducción sobre las operaciones, como en el capítulo 3.

- **Al empezar.** Las aristas que bajan desde $s$ están saturadas, así que no son
  residuales. Las que llegan a $s$ suben, y las demás unen vértices de altura 0.
- **Empujar** por $(u, v)$, con $h(u) = h(v) + 1$, no cambia ninguna altura. Puede
  quitar $(u, v)$ de la red residual, lo que no rompe nada. Y puede **agregar** la
  inversa $(v, u)$, que es el paso que todo el mundo se salta: hay que comprobar
  $h(v) \le h(u) + 1$, y vale con holgura porque $h(v) = h(u) - 1$.
- **Reetiquetar** $u$ cambia solo $h(u)$. Para las aristas que salen de $u$, la nueva
  altura es $1 + \min h(v)$ sobre ellas, así que $h(u) \le h(v) + 1$ para todas. Para
  las que entran, $(w, u)$, se cumplía $h(w) \le h(u) + 1$ con la altura vieja, y la
  nueva es mayor (lo vemos ahora), así que se sigue cumpliendo.

Falta lo de "la nueva es mayor". Si se reetiqueta $u$, ninguna arista residual
$(u, v)$ es admisible: $h(u) \ne h(v) + 1$, y con el invariante, $h(u) \le h(v)$.
Entonces $1 + \min h(v) \ge h(u) + 1$. Un reetiquetado sube la altura al menos 1, y
como nada más cambia alturas, **las alturas nunca bajan**. $\square$

## 4. Correctitud

Que el algoritmo termina lo demuestran las §6 a §8. Aquí, que lo que deja es un flujo
máximo, con un lema que también usará la §6.

**Lema (camino de vuelta).** Si $u$ es activo, en la red residual hay un camino de $u$
a $s$.

*Demostración.* Sea $X$ el conjunto de vértices a los que $u$ llega en la red
residual, y supongamos que $s \notin X$. Ninguna arista residual sale de $X$: para
$w \in X$ y $y \notin X$, $r(w, y) = 0$, así que $f(w, y) = c(w, y)$ y $f(y, w) = 0$.
Por las aristas entre $X$ y el resto, el flujo solo **sale** de $X$. Al sumar los
excesos de $X$, el flujo interno se cancela y queda
$$\sum_{w \in X} e(w) = \sum_{y \notin X,\ w \in X} f(y, w) - \sum_{w \in X,\ y \notin X} f(w, y) = 0 - \sum f(w, y) \le 0.$$
Como $s \notin X$, todos los excesos de $X$ son $\ge 0$, así que todos son 0, y en
particular $e(u) = 0$, contra que $u$ es activo. $\square$

**Teorema.** Si el genérico termina, el preflujo que deja es un flujo máximo.

*Demostración.* Termina cuando no hay activos, así que todo vértice distinto de $s$ y
$t$ tiene exceso 0, y el preflujo es un flujo. Supongamos que en su red residual hay
un camino de $s$ a $t$. Se puede tomar simple, así que tiene a lo sumo $V - 1$ aristas,
y por el invariante cada arista baja a lo sumo un escalón. Entonces
$$V = h(s) \le h(t) + (V - 1) = V - 1,$$
una contradicción. No hay camino de aumento, y por Max-Flow Min-Cut (capítulo 13) el
flujo es máximo. $\square$

Comprobémoslo contra un oráculo que no comparte nada con el algoritmo: el corte
mínimo por fuerza bruta sobre los $2^{V-2}$ cortes, que por Max-Flow Min-Cut vale lo
mismo que el flujo máximo.

```{python continue}
def corte_minimo_bruto(n, aristas, s, t):
    otros = [v for v in range(n) if v not in (s, t)]
    return min(sum(c for u, v, c in aristas if u in S and v not in S)
               for k in range(len(otros) + 1)
               for S in ({s, *X} for X in itertools.combinations(otros, k)))


def aleatoria(n, m, cmax, rng):
    return [(*rng.sample(range(n), 2), rng.randint(1, cmax)) for _ in range(m)]


rng = random.Random(1)
probadas = 0
for _ in range(1000):
    n = rng.randint(2, 7)
    A = aleatoria(n, rng.randint(0, 14), rng.choice([1, 3, 10]), rng)
    valor, _, _ = generico(red_de(n, A), 0, n - 1, vigilar=True)
    assert valor == corte_minimo_bruto(n, A, 0, n - 1), A
    probadas += 1
print(probadas, "redes al azar: el invariante se cumplió en cada paso y el flujo "
      "coincidió con el corte mínimo")
```

## 5. El error que la demostración anuncia {#push-relabel-5-el-error-que-la-demostracion-anuncia}

Después del capítulo 13 es tentador pensar así: $s$ solo tiene que estar "por encima
de los caminos", y en Dinic lo que importa es la distancia de $s$ a $t$. Con
$h(s) = d(s, t)$, el exceso que sobra vuelve antes y nos ahorramos reetiquetados.

```{python continue}
def distancia(n, aristas, s, t):
    """La distancia de s a t en la red original, por BFS (n si no hay camino)."""
    vecinos = [[] for _ in range(n)]
    for u, v, c in aristas:
        vecinos[u].append(v)
    d = {s: 0}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v in vecinos[u]:
            if v not in d:
                d[v] = d[u] + 1
                cola.append(v)
    return d.get(t, n)


def capas(k, w, cmax, rng):
    """s, k capas de w vértices con aristas solo de una capa a la siguiente, t."""
    n, A = 2 + k * w, []
    capa = lambda i: range(1 + i * w, 1 + (i + 1) * w)
    A += [(0, v, rng.randint(1, cmax)) for v in capa(0)]
    A += [(u, v, rng.randint(1, cmax)) for i in range(k - 1)
          for u in capa(i) for v in capa(i + 1) if rng.random() < 0.5]
    A += [(u, n - 1, rng.randint(1, cmax)) for u in capa(k - 1)]
    return n, A


baterias = {
    "chicas, V ≤ 7":
        lambda r: (n := r.randint(2, 7), aleatoria(n, r.randint(1, 14), 10, r)),
    "medianas, V = 8..10":
        lambda r: (n := r.randint(8, 10), aleatoria(n, 3 * n, 10, r)),
    "en capas":
        lambda r: capas(r.randint(2, 3), r.randint(2, 3), 10, r),
}
for nombre, generar in baterias.items():
    r, fallos, N = random.Random(5), 0, 1000
    for _ in range(N):
        n, A = generar(r)
        h_s = distancia(n, A, 0, n - 1)
        valor, _, _ = generico(red_de(n, A), 0, n - 1, h_s=h_s)
        fallos += valor != corte_minimo_bruto(n, A, 0, n - 1)
    print(f"{nombre:20}  la atrapa en {fallos:3} de {N} redes ({fallos / N:.1%})")
```

La variante está mal, y casi no se nota. En redes chicas al azar falla en 3 de cada
mil, y en redes en capas, la forma de los ejemplos de Dinic, ni una vez en mil. Hay
que ir a redes medianas, con más caminos alternativos, para verla fallar a menudo.
Cuando falla, termina con un flujo válido y más chico que el máximo: ninguna
comprobación local se queja.

La demostración de la §4 lo había dicho. Su última línea necesita que $h(s)$ sea
mayor que la longitud de **cualquier** camino residual simple de $s$ a $t$, no la del
más corto en la red original. Los caminos residuales usan aristas inversas que la red
original no tiene, y pueden ser mucho más largos que $d(s, t)$. Uno así puede
sobrevivir hasta el final, bajando un escalón por arista, y el algoritmo se detiene con
un camino de aumento delante. El $V$ de la inicialización es la cota de la longitud de
un camino simple, y la demostración lo usa. Qué valores de $h(s)$ siguen
siendo correctos es el ejercicio 10, y la respuesta no es "solo $V$".

## 6. Las alturas no se escapan

Ahora la terminación. Primero, cuánto suben las alturas en redes al azar.

```{python continue}
r, peor = random.Random(3), {}
for _ in range(3000):
    n = r.randint(3, 8)
    A = aleatoria(n, r.randint(2, 16), r.choice([1, 2, 5]), r)
    _, h, _ = generico(red_de(n, A), 0, n - 1)
    peor[n] = max(peor.get(n, 0), max(h[v] for v in range(1, n - 1)))
for n in sorted(peor):
    print(f"V = {n}:  mayor altura vista {peor[n]:2},  cota 2V − 1 = {2 * n - 1}")
```

Las alturas pasan de $V$, porque devolver exceso a $s$ obliga a subir por encima de
él, pero no llegan a $2V - 1$, que es lo que se demuestra.

**Lema.** En todo momento, $h(u) \le 2V - 1$ para todo vértice $u$.

*Demostración.* Para $s$ y $t$ es obvio, porque nunca cambian. Un vértice $u$ solo
cambia de altura cuando se reetiqueta, y solo se reetiqueta si es activo. Justo después
de reetiquetarlo sigue activo, así que por el lema del camino de vuelta hay un camino
residual de $u$ a $s$, que se puede tomar simple, con a lo sumo $V - 1$ aristas. El
invariante dice que cada arista baja a lo sumo un escalón, así que
$h(u) \le h(s) + (V - 1) = 2V - 1$. Entre reetiquetados la altura no cambia. $\square$

**Corolario.** Cada vértice se reetiqueta a lo sumo $2V - 1$ veces, porque empieza en
0, cada reetiquetado lo sube al menos 1 (§3) y no pasa de $2V - 1$. Los reetiquetados
son a lo sumo $(2V - 1)(V - 2) < 2V^2$ en total.

## 7. Empujes saturantes: a lo sumo $2VE$

En la @fig-pr-alturas, la unidad que rebota entre $a$ y $b$ sube dos escalones por
vuelta.

**Lema.** Hay a lo sumo $2V - 1$ empujes saturantes por cada par de vértices unidos por
una arista, y a lo sumo $(2V - 1)E < 2VE$ en total.

*Demostración.* En un empuje saturante de $u$ a $v$, $h(u) = h(v) + 1$ y $(u, v)$ deja
de ser residual. Solo un empuje de $v$ a $u$ la devuelve, y exige $h(v) = h(u) + 1$:
como las alturas no bajan, $h(v)$ subió al menos 2, y para volver a empujar de $u$ a
$v$, también $h(u)$. Así que $h(u) + h(v)$ crece al menos 2 entre dos empujes
saturantes consecutivos sobre el par, en cualquier sentido. La suma empieza en al menos 1 en el primero de ellos (una de las dos es
$\ge 1$ porque difieren en 1) y no pasa de $4V - 3$, porque ninguna altura pasa de
$2V - 1$ y las dos no pueden estar en $2V - 1$ a la vez si una es la otra más uno. Eso
deja a lo sumo $2V - 1$ empujes saturantes por par. Cada par corresponde al menos a una
arista de la red, así que hay a lo sumo $E$ pares. $\square$

## 8. Empujes no saturantes: el potencial

Un empuje no saturante deja a $u$ sin exceso, pero puede activar a $v$, y un mismo
exceso se parte y se reúne muchas veces. Para contarlos usamos el método del potencial
del capítulo 4.

$$\Phi = \sum_{v \text{ activo}} h(v).$$

Cumple las condiciones de un buen potencial (capítulo 4, §3): es 0 al empezar, porque
los activos están en el suelo, nunca es negativo, y sube cuando se acumula una deuda,
exceso que está alto y alguien tendrá que bajar. Al terminar también es 0.

- Un **reetiquetado** de $u$ sube $\Phi$ en lo que subió $h(u)$. Sumado sobre toda la
  ejecución, es a lo sumo $2V - 1$ por vértice: $(2V - 1)(V - 2)$ en total.
- Un **empuje saturante** de $u$ a $v$ no cambia alturas, pero puede activar a $v$, y
  entonces $\Phi$ sube en $h(v) \le 2V - 1$. En total, a lo sumo $(2V - 1) \cdot 2VE$.
- Un **empuje no saturante** de $u$ a $v$ desactiva a $u$, que resta $h(u)$, y como
  mucho activa a $v$, que suma $h(v) = h(u) - 1$. $\Phi$ baja al menos 1.

Como $\Phi$ empieza y termina en 0, lo que baja es igual a lo que sube. Cada empuje no
saturante baja al menos 1, así que
$$\#\text{no saturantes} \le (2V - 1)(V - 2) + (2V - 1)\,2VE \le 4V^2 (V + E).$$
Si la red subyacente es conexa, que es lo que pasa cuando quitamos los vértices que
no tocan ninguna arista, $E \ge V - 1$ y la cota queda en $O(V^2 E)$. Junto con las
dos de antes, el genérico hace $O(V^2 E)$ operaciones y termina.

```{python continue echo=false output=asis}
_pasos = [(op, sum(hh[v] for v in range(1, 4) if ee[v] > 0))
          for op, hh, ee, _ in diario]
print(G.potencial(_pasos, ident="pr-potencial",
      pie=f"El potencial Φ, suma de las alturas de los activos, en las "
          f"{len(diario) - 1} operaciones del ejemplo de la §2, coloreado por la "
          f"operación que lo movió."))
```

En la @fig-pr-potencial, lo que bajan los tres empujes no saturantes lo acumularon
los reetiquetados. Hay también empujes saturantes que lo **bajan**: si $u$ se queda sin
exceso y $v$ ya era activo, nadie se activa. La demostración solo acota lo que suben.

¿Qué tan cerca están las tres cotas de lo que pasa? Midamos el peor cociente entre lo
contado y la cota, en diez redes al azar de cada tamaño.

```{python continue}
r = random.Random(3)
print("   V    E  reetiq./2V²  saturantes/2VE  no satur./4V²(V+E)")
for n, m in [(20, 80), (40, 160), (80, 320)]:
    peor = [0.0, 0.0, 0.0]
    for _ in range(10):
        _, _, c = generico(red_de(n, aleatoria(n, m, 100, r)), 0, n - 1)
        cotas = (2 * n * n, 2 * n * m, 4 * n * n * (n + m))
        cuentas = (c["reetiquetar"], c["saturante"], c["no saturante"])
        peor = [max(p, x / y) for p, x, y in zip(peor, cuentas, cotas)]
    print(f"{n:4} {m:4}  {peor[0]:11.3f}  {peor[1]:14.3f}  {peor[2]:18.4f}")
```

Los reetiquetados llegan a cerca del 40 % de su cota. Los empujes saturantes no llegan
al 5 %, y los no saturantes se quedan en milésimas: la cuenta del potencial cobra a
cada empuje saturante el peor caso, $2V - 1$, y casi ninguno lo paga. Una cota de peor
caso no promete ser ajustada en redes al azar, pero la tabla sugiere que el orden en
que se eligen los activos tiene margen, y eso es lo que usan las §9 y §10.

Falta el costo de cada operación. Con una lista de activos y la **arista actual** de la
§9, cada empuje cuesta $O(1)$, cada reetiquetado $O(\deg u)$ y los recorridos de
listas suman $O(VE)$. El total es $O(V^2 E)$.

## 9. FIFO: $O(V^3)$

En lugar de operaciones sueltas, se **descarga** un vértice: se empuja todo el exceso
que se pueda y, si se queda sin aristas admisibles con exceso todavía, se reetiqueta.
Cada vértice guarda su **arista actual**, un puntero que avanza por su lista y vuelve
al principio solo al reetiquetar. Los activos esperan en una cola FIFO.

**Lema (arista actual).** Cuando la arista actual de $u$ llega al final de la lista, $u$
no tiene ninguna arista admisible, así que reetiquetarlo es legal.

*Demostración.* El puntero deja atrás $(u, v)$ solo si no era admisible. Mientras $u$
no se reetiquete, no puede volverse admisible: $h(u)$ no cambia y $h(v)$ no baja. Si
$(u, v)$ era residual, el invariante daba $h(u) \le h(v)$, y así sigue. Si no lo era,
tiene que volver a serlo. Eso pasa solo por un empuje
de $v$ a $u$, que exige $h(v) = h(u) + 1$, y entonces $h(u) = h(v) - 1 \ne h(v) + 1$.
$\square$

Con el lema, cada vértice recorre su lista entera a lo sumo una vez por reetiquetado:
$O(\deg u \cdot V)$ por vértice, $O(VE)$ en total, que es lo que faltaba en la §8.

Un vértice que se reetiqueta vuelve al final de la cola aunque le quede exceso. Así,
una descarga termina sin exceso o con un reetiquetado, y en los dos casos hace a lo
sumo un empuje no saturante, porque ese empuje deja al vértice sin exceso. La implementación es el ejercicio 8; la de la §10 usa la misma descarga.

**Teorema** (Goldberg y Tarjan, 1988). FIFO hace a lo sumo $4V^3$ empujes no
saturantes.

*Demostración.* Partimos la ejecución en **pasadas** sobre la cola. La pasada 1 descarga
los vértices que se activaron al inicializar; la pasada $i + 1$ descarga los que
entraron en la cola durante la pasada $i$. En una pasada cada vértice se descarga a lo
sumo una vez, así que hace a lo sumo un empuje no saturante: a lo sumo $V$ por pasada.
Falta contar las pasadas, y para eso usamos otro potencial,
$$\Psi = \max\{\, h(v) : v \text{ activo} \,\}.$$
En una pasada sin reetiquetados, cada vértice descargado mandó todo su exceso un
escalón más abajo, así que al final todos los activos están más abajo que el más alto
del principio: $\Psi$ baja al menos 1. Si hay reetiquetados, $\Psi$ puede subir, pero
como mucho hasta la nueva altura de un vértice reetiquetado, que estaba activo al
empezar la pasada (se descargó en ella) y por lo tanto no más alto que $\Psi$, así que lo que sube
$\Psi$ en toda la ejecución es menos de $2V^2$, lo que suben las alturas en total. Las
pasadas con reetiquetado son menos de $2V^2$, una por reetiquetado como mucho. Las
otras bajan $\Psi$, que empieza en 0 y no es negativo, así que son menos de $2V^2$.
En total, menos de $4V^2$ pasadas y de $4V^3$ empujes no saturantes. $\square$

Con los $O(VE)$ de los recorridos y $E \le V^2$, el tiempo es $O(V^3)$, mejor que el
$O(V^2 E)$ de Dinic en redes densas.

## 10. Mayor etiqueta: $O(V^2 \sqrt{E})$

La segunda regla descarga siempre el activo **más alto**. Goldberg y Tarjan observan
que también da $O(V^3)$ (el ejercicio 5). Cheriyan y Maheshwari demostraron
$O(V^2 \sqrt{E})$ en *Analysis of preflow push algorithms for maximum network flow*
(SIAM Journal on Computing 18(6), 1057–1086, 1989). La demostración que sigue, otra
vez un potencial, es la de Cheriyan y Mehlhorn, *An analysis of the highest-level
selection rule in the preflow-push max-flow algorithm* (Information Processing
Letters 69(5), 239–242, 1999).

**Teorema.** Con la regla de mayor etiqueta, hay $O(V^2 \sqrt{E})$ empujes no
saturantes.

*Demostración.* Sea $H$ la mayor altura de un activo. Una **fase** es un tramo de la
ejecución en que $H$ no cambia. Contemos las fases. $H$ empieza en 0 y no es negativo.
Solo sube por un reetiquetado del vértice más alto, y sube como mucho lo que subió ese
vértice. Así que $H$ cambia hacia arriba menos de $2V^2$ veces, una por reetiquetado, y
la suma de lo que sube es menos de $2V^2$, lo que suben las alturas en total. Cada
bajada es de al menos 1, y lo que baja no puede pasar de lo que sube, así que $H$ baja
menos de $2V^2$ veces. Hay a lo sumo $4V^2$ fases.

Dentro de una fase, todos los empujes salen de vértices a altura $H$, porque la regla
elige al más alto. Uno que hace un empuje no saturante se queda sin exceso, y nadie
puede dárselo de nuevo en la fase, porque no hay activos a altura $H + 1$. Así que hay
a lo sumo un empuje no saturante por vértice a altura $H$. Y nadie cambia de altura:
reetiquetar a uno de altura $H$ cambiaría $H$ y terminaría la fase.

Para un parámetro $K$, una fase es **barata** si tiene a lo sumo $K$ empujes no
saturantes, y **cara** si no. Las baratas suman a lo sumo $4V^2 K$. Para las caras
usamos el potencial
$$\Phi = \frac{1}{K} \sum_{v \text{ activo}} \phi(v), \qquad \phi(v) = |\{\, w : h(w) \le h(v) \,\}|,$$
donde $\phi(v)$ cuenta los vértices que no están más altos que $v$, y vale entre 1 y
$V$. $\Phi$ empieza en a lo sumo $V^2 / K$ y nunca es negativo.

- Un **reetiquetado** de $u$ sube $\phi(u)$ como mucho a $V$, y solo puede **bajar** el
  $\phi$ de los demás. Sube $\Phi$ a lo sumo $V / K$.
- Un **empuje saturante** activa como mucho a un vértice: sube $\Phi$ en a lo sumo
  $V / K$.
- Un **empuje no saturante** de $u$ a $v$, con $h(v) = h(u) - 1$, desactiva a $u$ y
  como mucho activa a $v$. Cambia $K \cdot \Phi$ en $\phi(v) - \phi(u)$ o menos, y
  $\phi(u) - \phi(v)$ es exactamente el número de vértices a altura $h(u)$.

En una fase cara hay más de $K$ empujes no saturantes desde vértices distintos a altura
$H$, y las alturas no cambian en la fase: hay más de $K$ vértices a altura $H$ todo el
tiempo, y cada empuje no saturante baja $\Phi$ en más de 1. Lo que baja $\Phi$ en total es a lo sumo lo que sube más
su valor inicial:
$$\#\text{no saturantes en fases caras} \le \frac{V}{K}\left(2V^2 + 2VE\right) + \frac{V^2}{K}.$$
Sumando las dos clases, $O(V^2 K + (V^3 + V^2 E)/K)$, y con $K = \sqrt{E}$ y
$V = O(E)$, $O(V^2 \sqrt{E})$. $\square$

El paso que todo el mundo se salta es el primero de la lista: que reetiquetar a $u$ no
sube el $\phi$ de nadie más. Si $\phi$ contara los vértices **más altos** en lugar de
los más bajos, un reetiquetado subiría el potencial de muchos a la vez y la cuenta no
cerraría.

El **tiempo** también es $O(V^2 \sqrt{E})$: los recorridos de listas suman $O(VE)$, y
$VE \le V^2 \sqrt{E}$ porque $E \le V^2$. La implementación guarda los activos en
cubetas por altura y recuerda la cubeta más
alta que puede tener a alguien. La misma función lleva ya las dos heurísticas de la
§11, apagadas por omisión.

```{python continue}
def mayor_etiqueta(R, s, t, gap=False, global_cada=None):
    n, dst, cap, ady = R.n, R.dst, R.cap, R.ady
    h, e, actual = [0] * n, [0] * n, [0] * n
    h[s] = n
    cubeta = [[] for _ in range(2 * n)]      # cubeta[k]: activos con altura k
    en_altura = [0] * (2 * n)                # vértices distintos de s con altura k
    cuenta = {"reetiquetar": 0, "saturante": 0, "no saturante": 0, "global": 0}

    def empujar(u, k, d):
        v = dst[k]
        cap[k] -= d; cap[k ^ 1] += d
        if e[v] == 0 and v != s and v != t:
            cubeta[h[v]].append(v)
        e[u] -= d; e[v] += d

    def mover(v, nueva):                     # cambia la altura y lleva la cuenta
        if h[v] < n: en_altura[h[v]] -= 1
        h[v] = nueva
        if nueva < n: en_altura[nueva] += 1
        actual[v] = 0
        if e[v] > 0 and v != t:
            cubeta[nueva].append(v)

    def relabel_global():            # h(v) = distancia residual a t, o a s más n
        nueva = [None] * n
        for raiz, base in ((t, 0), (s, n)):
            nueva[raiz] = base
            cola = deque([raiz])
            while cola:
                v = cola.popleft()
                for k in ady[v]:
                    u = dst[k]               # la arista residual es u -> v: k ^ 1
                    if cap[k ^ 1] > 0 and nueva[u] is None:
                        nueva[u] = nueva[v] + 1
                        cola.append(u)
        for v in range(n):                   # el que no llega a nadie: 2n - 1
            if v not in (s, t) and (nueva[v] or 2 * n - 1) > h[v]:
                mover(v, nueva[v] or 2 * n - 1)
        cuenta["global"] += 1

    en_altura[0] = n - 1
    for k in ady[s]:
        empujar(s, k, cap[k])
    if global_cada:
        relabel_global()
    alto, desde_global = 2 * n - 1, 0
    while alto >= 0:
        if not cubeta[alto]:
            alto -= 1
            continue
        u = cubeta[alto].pop()
        if h[u] != alto or e[u] == 0:        # entrada vieja: ya se movió
            continue
        while e[u] > 0:
            if actual[u] == len(ady[u]):
                viejo = h[u]
                mover(u, 1 + min(h[dst[k]] for k in ady[u] if cap[k] > 0))
                cuenta["reetiquetar"] += 1
                desde_global += 1
                if gap and viejo < n and en_altura[viejo] == 0:   # el hueco
                    for w in range(n):
                        if w != s and viejo < h[w] < n:
                            mover(w, n + 1)
                alto = max(alto, h[u])
                break
            k = ady[u][actual[u]]
            if cap[k] > 0 and h[u] == h[dst[k]] + 1:
                empujar(u, k, min(e[u], cap[k]))
                cuenta["saturante" if cap[k] == 0 else "no saturante"] += 1
            else:
                actual[u] += 1
        if global_cada and desde_global >= global_cada * n:
            relabel_global()
            desde_global, alto = 0, 2 * n - 1
    return e[t], cuenta

r = random.Random(1)
for _ in range(500):
    n = r.randint(2, 7)
    A = aleatoria(n, r.randint(0, 14), 10, r)
    oraculo = corte_minimo_bruto(n, A, 0, n - 1)
    for g, c in ((False, None), (True, None), (True, 1)):
        assert mayor_etiqueta(red_de(n, A), 0, n - 1, g, c)[0] == oraculo, (A, g, c)
print("mayor etiqueta, con y sin heurísticas: 500 redes, todas coinciden "
      "con el oráculo")
```

## 11. Las heurísticas: relabel global y gap

En la @fig-pr-alturas, lo que más operaciones costó fue devolver a $s$ el exceso que no
cabía: el vaivén entre $a$ y $b$, que sube de dos en dos hasta pasar de $V$. Las cotas
lo absorben, pero en la práctica es casi todo el trabajo. Las dos heurísticas que
siguen lo atacan, y las estudiaron Cherkassky y Goldberg en *On implementing the push-relabel method for
the maximum flow problem* (Algorithmica 19(4), 390–410, 1997).

**Relabel global.** Cada tanto, se recalculan todas las alturas como distancias
exactas en la red residual: $h(v)$ pasa a ser la distancia de $v$ a $t$, y si $v$ no
llega a $t$, $V$ más su distancia a $s$. Son dos búsquedas en anchura hacia atrás,
$O(V + E)$.

**Lema.** El relabel global no baja ninguna altura y deja el invariante en pie.

*Demostración.* Sea $d(v)$ la distancia residual de $v$ a $t$. Sobre un camino
residual más corto, el invariante da $h(v) \le h(t) + d(v) = d(v)$: la distancia nunca
es menor que la altura. Para
los que no llegan a $t$, el mismo argumento hacia $s$ da $h(v) \le V + d_s(v)$. Las
nuevas alturas son distancias, y las distancias cumplen la desigualdad del invariante
por definición: si $(u, v)$ es residual, $d(u) \le d(v) + 1$. Falta un caso: $u$ no
llega a $t$ y $v$ sí. Entonces la arista $(u, v)$ residual haría que $u$ llegara a $t$,
contradicción. El caso contrario, $u$ llega a $t$ y $v$ no, da $d(u) \le V - 1 <
V + d_s(v) + 1$. $\square$

Un vértice que no llega ni a $t$ ni a $s$ no tiene exceso (lema del camino de vuelta),
y el código lo pone a $2V - 1$: sus aristas residuales van a vértices en su misma
situación, y nadie está más alto, así que el invariante sigue en pie.

**Gap.** Si no queda ningún vértice a cierta altura $k < V$, todos los que están entre
$k$ y $V$ suben de golpe a $V + 1$. El invariante no deja bajar de a dos escalones, así
que desde arriba de $k$ no se llega a $t$ sin pasar por la altura $k$, donde no hay
nadie: ese exceso solo puede volver a $s$. Que no cambia la respuesta es el
ejercicio 6.

**Qué se hereda y qué no.** Las dos heurísticas respetan el invariante y no bajan
alturas, y eso alcanza para la correctitud (§4) y para las cotas de operaciones de las
§6 a §8, que solo usan esas dos cosas y que ninguna altura pasa de $2V - 1$. Las §9 y
§10 piden leer una palabra de otra manera: allí "reetiquetado" era lo único que subía
alturas, y ahora también suben con un relabel global o un gap. Con "reetiquetado"
leído como "cualquier subida de altura", las dos demostraciones siguen, porque lo que
suben las alturas en total sigue siendo menos de $2V^2$. Lo que no se hereda es el
costo de la heurística misma, que hay que contar aparte. El relabel global cuesta
$O(V + E)$; hecho cada $V$ reetiquetados, como en el código, son a lo sumo $2V$
llamadas y $O(VE)$ en total, pero hecho en cada pasada de FIFO serían hasta $4V^2$
llamadas y se perdería el $O(V^3)$. El gap del código recorre los $V$ vértices en cada
hueco, y con hasta $2V^2$ huecos eso es $O(V^3)$, más que el $O(V^2 \sqrt{E})$ de mayor
etiqueta. Una implementación cuidadosa guarda listas de vértices por altura y paga
cada vértice que mueve con la altura que gana, que ya está en la cuenta.

Midamos en una familia que llamamos **embudo**, el ejemplo en grande: $s$ inyecta mucho
más de lo que cabe por las pocas aristas que llegan a $t$.

```{python continue}
def dinic(R, s, t):                          # el del capítulo 13, sobre esta Red
    n, dst, cap, ady = R.n, R.dst, R.cap, R.ady
    total = 0
    while True:
        nivel = [-1] * n
        nivel[s] = 0
        cola = deque([s])
        while cola:
            u = cola.popleft()
            for k in ady[u]:
                if cap[k] > 0 and nivel[dst[k]] < 0:
                    nivel[dst[k]] = nivel[u] + 1
                    cola.append(dst[k])
        if nivel[t] < 0:
            return total
        actual = [0] * n

        def bloquear(u, f):
            if u == t:
                return f
            while actual[u] < len(ady[u]):
                k = ady[u][actual[u]]
                v = dst[k]
                if cap[k] > 0 and nivel[v] == nivel[u] + 1:
                    d = bloquear(v, min(f, cap[k]))
                    if d:
                        cap[k] -= d; cap[k ^ 1] += d
                        return d
                actual[u] += 1
            return 0

        while (f := bloquear(s, math.inf)):
            total += f


def embudo(n, r):
    A = [(u, v, c) for u, v, c in aleatoria(n, 4 * n, 100, r)
         if v != 0 and u != n - 1]       # nada entra a s ni sale de t
    A += [(0, v, 100) for v in r.sample(range(1, n - 1), n // 4)]
    A += [(u, n - 1, r.randint(1, 100)) for u in r.sample(range(1, n - 1), 5)]
    return A


metodos = {
    "Dinic":          lambda R, s, t: (dinic(R, s, t), None),
    "mayor etiqueta": mayor_etiqueta,
    "m. e. + heur.":  lambda R, s, t: mayor_etiqueta(R, s, t, True, 1),
}
r = random.Random(4)
tiempos = {m: [] for m in metodos}
print(f"    V  {'método':>15}  {'ms':>8}  {'operaciones':>11}"
      f"  {'op./V²':>7}  {'op./V':>6}")
for n in (50, 100, 200, 300):
    A = embudo(n, r)
    valores = set()
    for m, f in metodos.items():
        mejor = math.inf
        for _ in range(3):                   # el mejor de tres, por el ruido
            R = red_de(n, A)
            t0 = time.perf_counter()
            valor, c = f(R, 0, n - 1)
            mejor = min(mejor, time.perf_counter() - t0)
        valores.add(valor)
        tiempos[m].append((n, mejor * 1000))
        ops = ("" if c is None
               else c["reetiquetar"] + c["saturante"] + c["no saturante"])
        c2, c1 = ("", "") if c is None else (f"{ops / n**2:.2f}", f"{ops / n:.1f}")
        print(f"{n:5}  {m:>15}  {mejor * 1000:8.1f}  {ops:>11}  {c2:>7}  {c1:>6}")
    assert len(valores) == 1                 # los tres dan el mismo flujo
(_, td), (_, th) = tiempos["Dinic"][-1], tiempos["m. e. + heur."][-1]
print(f"con V = {n}, m. e. + heur. tarda {th / td:.1f} veces lo que Dinic")
```

```{python continue echo=false output=asis}
print(F.grafica_log_log(tiempos, "V (vértices)", "ms", ident="pr-tiempos",
      pie="Tiempo (el mejor de tres) de los tres métodos sobre una red embudo de "
          "cada tamaño, en ejes logarítmicos."))
```

Los conteos son la parte robusta de la medición. Sin heurísticas, mayor etiqueta hace
unas $1{,}5\,V^2$ operaciones, casi todas para subir el exceso sobrante por encima de
$V$ escalón a escalón. Con relabel global y gap caen a entre 8 y 15 por vértice: el
relabel global pone de una vez a cada vértice donde lo iba a llevar el vaivén. La
@fig-pr-tiempos muestra lo mismo en tiempo.

Lo que la tabla **no** dice es qué algoritmo es más rápido. En Python y en esta
familia, push-relabel con heurísticas no le gana con claridad a Dinic: la última línea
da el cociente en el tamaño mayor, que cambia con la carga de la máquina, y cada
relabel global es una búsqueda en anchura completa.

## 12. Cierre: qué se puede tocar

¿Cuánto se puede cambiar un algoritmo sin volver a demostrarlo? Las demostraciones lo
dicen si se leen como la lista de lo que usan:

- La correctitud (§4) usa el invariante y que $h(s)$ supere la longitud de cualquier
  camino residual simple. El error plantado tocó lo segundo y se rompió.
- Las cotas (§6 a §8) usan además que las alturas nunca bajan.
- Las reglas de orden (§9, §10) usan además cuál activo se elige.

Una heurística que respeta el invariante y no baja alturas, como el relabel global y
el gap, hereda la correctitud y las cuentas de operaciones; su propio costo hay que
contarlo aparte (§11). Una que cambia la inicialización, aunque parezca inocente, no
hereda nada. **La demostración
no dice qué hacer: dice qué se puede tocar.**

El capítulo 15 vuelve sobre los cortes globales con un algoritmo aleatorio, y el 24
sobre el flujo máximo en tiempo casi lineal.

## Resumen {#push-relabel-resumen}

- Un **preflujo** respeta capacidades y deja que entre más de lo que sale; el sobrante
  es el **exceso**, y un vértice con exceso es **activo**.
- Se empieza con $h(s) = V$ y las aristas de $s$ saturadas, y se repite **empujar**
  por una arista residual con $h(u) = h(v) + 1$ o **reetiquetar** a $1 + \min h(v)$.
- El **invariante** es $h(u) \le h(v) + 1$ en toda arista residual. Al terminar no hay
  camino de aumento, porque uno simple baja a lo sumo $V - 1$.
- El **error plantado**, $h(s) = d(s, t)$, falla poco y en silencio, donde la
  demostración lo anunciaba.
- Un activo tiene camino residual a $s$: $h \le 2V - 1$, menos de $2V^2$
  reetiquetados y menos de $2VE$ empujes saturantes.
- Los no saturantes se cuentan con $\Phi = \sum_{\text{activo}} h(v)$: $O(V^2 E)$ en
  total.
- **FIFO** da $O(V^3)$ por pasadas; **mayor etiqueta**, $O(V^2 \sqrt{E})$ con fases
  baratas y caras.
- El **relabel global** y el **gap** heredan la correctitud y las cuentas de
  operaciones; su costo se cuenta aparte. En el embudo, hasta $V = 300$, bajan las
  operaciones de unas $1{,}5\,V^2$ a entre 8 y 15 por vértice.

## Ejercicios {#push-relabel-ejercicios}

1. **Traza.** Ejecuta a mano el genérico sobre la red de vértices $s, a, b, c, t$ con
   aristas $s \to a$ (3), $s \to b$ (3), $a \to b$ (2), $a \to c$ (2), $b \to c$ (1),
   $b \to t$ (2) y $c \to t$ (3). Elige siempre el activo que va primero en el orden
   $a, b, c$, y prueba sus aristas en el orden en que se crearon, incluidas las
   inversas. Anota en cada paso la operación, las alturas y los excesos. ¿Cuántas
   operaciones de cada tipo hiciste, y qué flujo queda?

2. **Traza.** Toma el estado del paso 12 de la @fig-pr-alturas (los flujos salen del
   `diario`). Calcula a mano el relabel global en ese momento y di si hay un hueco que
   dispare el gap. Si en ese paso se hubiera hecho solo el relabel global, ¿cuántos
   empujes y reetiquetados se habría ahorrado el genérico? ¿Y con solo el gap?

3. **Demostración.** El lema de la §6 da $h(u) \le 2V - 1$. Demuestra que, en el
   genérico sin heurísticas, ningún vértice llega a $2V - 1$. (Separa los caminos de $u$ a $s$ que pasan por $t$
   de los que no.)

4. **Demostración.** Demuestra que si en algún momento $h(u) \ge V$, entonces $u$ no
   tiene camino residual a $t$. ¿Qué quiere decir esto sobre el exceso de $u$?

5. **Demostración.** Demuestra que la regla de mayor etiqueta hace $O(V^3)$ empujes no
   saturantes con un argumento como el de pasadas de FIFO, sin el parámetro $K$ de la
   §10. ¿Qué papel juega la regla en tu argumento?

6. **Demostración.** Demuestra que la heurística gap no cambia la respuesta: que
   subir a $V + 1$ a todos los vértices entre el hueco y $V$ mantiene el invariante,
   no baja ninguna altura, y por lo tanto deja en pie las demostraciones de las §4
   a §8.

7. **Modelar.** Al terminar, ¿cómo obtienes un corte mínimo de la red residual?
   Demuestra que su capacidad es igual al flujo. Después demuestra que se puede leer
   **antes** de terminar, en cuanto ningún activo tiene camino residual a $t$. ¿Para
   qué sirve eso si solo se quiere el valor del flujo?

8. **Implementar y medir.** Implementa FIFO (§9) con la cola y la arista actual, y
   compruébala contra el oráculo de la §4. Mídela contra `dinic` y `mayor_etiqueta` en
   la familia embudo y en redes al azar, en operaciones y tiempo. ¿Dónde se separan
   FIFO y mayor etiqueta, y qué le pasa a FIFO con el relabel global?

9. ★ **Entrada que rompe.** Busca una familia de redes y una regla de elección de
   activos en la que los empujes no saturantes crezcan lo más rápido que puedas en
   función de $V$ y $E$. Compara con la cota $4V^2(V + E)$ de la §8: ¿qué parte de la
   demostración paga tu familia?

10. **Cambio de hipótesis.** Inicializa con $h(s) = k$ en lugar de $V$. ¿Para qué
    valores de $k$ sigue siendo correcto? Explora con el oráculo de la §4 y demuestra
    lo que encuentres. ¿Cómo cambian las cotas de las §6 a §8?
