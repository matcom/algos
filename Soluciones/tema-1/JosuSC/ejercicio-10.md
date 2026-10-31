# Ejercicio 10: Par más cercano en una dimensión

> **Enunciado.** Par más cercano en una dimensión. Demuestra $\Omega(n \log n)$ en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión. (C2, C5)

## 1. Especificación del problema

**Entrada.** Números reales $x_1, \ldots, x_n$, con $n \geq 2$. Se permiten valores repetidos.

**Salida.** Un par de índices $(i, j)$ con $i \neq j$ que minimiza $|x_i - x_j|$.

**Problemas relacionados.**

- **Distinción de elementos (ED).** Dados $x_1, \ldots, x_n$, decidir si son todos distintos. El conjunto de respuestas "sí" es
$$W = \{\, x \in \mathbb{R}^n : x_i \neq x_j \text{ para todo } i < j \,\}.$$
- **Par más cercano (CP).** El problema de arriba.

**Dos modelos, y la diferencia entre ellos es el centro del ejercicio.**

- **M1. Árbol de decisión algebraico de grado $d$.** Cada nodo interno prueba el signo ($<$, $=$ o $>$) de un polinomio de grado $\leq d$ en las entradas, y tiene tres hijos. Las hojas llevan la salida. El costo es la **altura** del árbol: el número de pruebas en el peor caso. Con $d = 1$ se obtienen los árboles lineales, que incluyen los de comparaciones ($x_i$ contra $x_j$).
- **M2. RAM con parte entera y diccionario, aleatoria.** Operaciones aritméticas, parte entera $\lfloor \cdot \rfloor$ y una tabla hash con operaciones en $O(1)$ esperado. El costo es el tiempo esperado, sobre las elecciones aleatorias del algoritmo y para toda entrada (no se supone ninguna distribución de las entradas).

**Lema 0 (en una dimensión, basta mirar los vecinos).** Si se ordenan los valores, existe un par más cercano formado por dos elementos consecutivos del orden.

*Demostración.* Sea $(p, q)$ un par más cercano con $x_p \leq x_q$, y supongamos que hay un tercer elemento $r$ con $x_p \leq x_r \leq x_q$. Entonces $|x_p - x_r| \leq |x_p - x_q|$, así que $(p, r)$ es al menos tan bueno. Repitiendo, se llega a un par consecutivo. ∎

Por tanto, **ordenar y recorrer las brechas consecutivas** resuelve CP en $O(n \log n)$ pruebas en M1 (el orden con $O(n \log n)$ comparaciones, y $n - 2$ comparaciones más entre diferencias, que son pruebas de grado $1$).

## 2. Cota inferior $\Omega(n \log n)$ por reducción desde ED

### 2.1. La cota de ED

**Teorema A (árboles lineales).** Todo árbol de decisión lineal que decide ED tiene altura $\geq \log_3 n! = \Omega(n \log n)$.

*Demostración.* La región de una hoja es la intersección de las condiciones de su camino: semiespacios abiertos ($\ell < 0$, $\ell > 0$) e hiperplanos ($\ell = 0$) con $\ell$ lineal. Es un conjunto **convexo**.

Sean $a, b \in W$ con ordenamientos distintos. Entonces existen $i, j$ con $a_i < a_j$ y $b_i > b_j$. Supongamos que $a$ y $b$ llegan a la misma hoja. Por convexidad, el segmento $z(t) = (1-t)\,a + t\,b$ está entero en la región de esa hoja. La función $f(t) = z_i(t) - z_j(t)$ es continua, con $f(0) < 0 < f(1)$, así que se anula en algún $t_0$. El punto $z(t_0)$ tiene $z_i = z_j$ (una entrada con repetidos, de respuesta "no") y llega a la misma hoja que $a$ (de respuesta "sí"). Contradicción.

Luego los $n!$ ordenamientos de valores distintos llegan a $n!$ hojas distintas. Un árbol ternario de altura $h$ tiene a lo sumo $3^h$ hojas, así que $3^h \geq n!$, es decir, $h \geq \log_3 n!$. Como $\log_2 n! \geq n \log_2 n - n \log_2 e$, esto es $\Omega(n \log n)$. ∎

**Por qué esto no basta.** Para $d \geq 2$ las regiones de las hojas dejan de ser convexas (por ejemplo, $\{x^2 + y^2 > 1\}$) y el argumento del segmento falla. Hay que contar **componentes conexas**: el conjunto $W$ tiene exactamente $n!$ componentes conexas, una por cada ordenamiento, porque el signo de $x_i - x_j$ es continuo y no se anula en $W$, así que es constante a lo largo de cualquier camino dentro de $W$.

**Teorema B (Ben-Or, 1983).** Si $W \subseteq \mathbb{R}^n$ tiene $N$ componentes conexas, todo árbol de decisión algebraico de grado acotado $d$ que decide si $x \in W$ tiene altura $h = \Omega(\log N - n)$ (la constante depende de $d$).

*La idea:* la región de cada hoja es un conjunto semialgebraico con una cantidad acotada de componentes conexas (Milnor–Thom), así que un árbol de altura $h$ solo puede distinguir $2^{O(h + n)}$ componentes.

**Corolario (cota de ED).** Con $N = n!$:

$$h_{\mathrm{ED}} = \Omega(\log n! - n) = \Omega(n \log n).$$

Este corolario es el punto de partida del ejercicio: **se toma como conocido** (Ben-Or). Lo que se demuestra a continuación es la reducción.

### 2.2. La reducción ED $\leq$ CP

**Lema 1.** Sea $(i, j)$ un par más cercano de $x_1, \ldots, x_n$. Entonces

$$x \text{ tiene todos sus elementos distintos} \iff x_i \neq x_j.$$

*Demostración.*

- ($\Rightarrow$) Si todos son distintos, cualquier par $i \neq j$ cumple $x_i \neq x_j$.
- ($\Leftarrow$, por contrarrecíproca) Si hay un repetido, $x_p = x_q$ con $p \neq q$, la distancia mínima es $0$, y como $(i, j)$ la alcanza, $|x_i - x_j| = 0$, es decir, $x_i = x_j$. ∎

**Construcción.** Sea $T$ un árbol de decisión algebraico de grado $d \geq 1$ y altura $h$ que resuelve CP: cada hoja lleva un par $(i, j)$ con $i \neq j$. Se construye $T'$ reemplazando **cada hoja** $(i, j)$ por un nodo que prueba el polinomio $p = x_i - x_j$ (de grado $1 \leq d$):

- rama $p = 0$: hoja **"hay repetidos"**;
- ramas $p < 0$ y $p > 0$: hoja **"todos distintos"**.

$T'$ es un árbol de decisión algebraico del mismo grado, de altura $h + 1$, y por el Lema 1 **decide ED**.

**Teorema.** Todo árbol de decisión algebraico de grado acotado que resuelve el par más cercano tiene altura $\Omega(n \log n)$.

*Demostración.* Por la construcción, $h_{\mathrm{ED}} \leq h_{\mathrm{CP}} + 1$. Por el Corolario, $h_{\mathrm{ED}} = \Omega(n \log n)$. Luego

$$h_{\mathrm{CP}} \geq h_{\mathrm{ED}} - 1 = \Omega(n \log n). \qquad ∎$$

### 2.3. Observaciones

**(a) La cota vale incluso para la versión de decisión.** La pregunta "¿hay dos puntos a distancia $0$?" es exactamente la negación de ED, así que decidir si la distancia mínima es $\leq 0$ ya cuesta $\Omega(n \log n)$. Un problema más fuerte (calcular el par) no puede ser más barato.

**(b) La cota es ajustada en M1.** El algoritmo de ordenar y recorrer vecinos (Lema 0) hace $O(n \log n)$ pruebas. Por tanto el par más cercano en una dimensión tiene complejidad $\Theta(n \log n)$ en árboles de decisión algebraicos.

**(c) Qué transfiere una reducción.** Una reducción con $O(1)$ trabajo extra transfiere cotas inferiores *dentro de un modelo*: si CP se pudiera resolver en $o(n \log n)$ en un modelo en el que la reducción sea válida, ED también. Eso es lo que se usa en §3: la cota es una afirmación sobre M1, y para escapar de ella hay que salir de M1.

## 3. Qué algoritmo de la conferencia 2 rompe la cota, y en qué modelo

**El algoritmo.** El **algoritmo aleatorio de costo esperado lineal** de la conferencia 2: los puntos se insertan en orden aleatorio; se mantiene la distancia mínima $\delta$ de los puntos ya insertados y una **rejilla** guardada en una **tabla hash**, con celdas cuyo tamaño depende de $\delta$. Para cada punto nuevo, solo se consultan las celdas vecinas. Cada vez que $\delta$ baja, se reconstruye la rejilla. El costo esperado es $O(n)$. Es un algoritmo de la familia de Rabin (1976); la versión incremental con diccionario dinámico, que es la que se adapta abajo, es la de Golin, Raman, Schwarz y Smid (1995).

**El modelo.** Es M2: una **RAM con parte entera y tabla hash**, y costo **esperado**. Sale de M1 por tres lados:

| Ingrediente del algoritmo | Por qué no existe en un árbol de decisión algebraico |
|---|---|
| **Parte entera** $\lfloor x / \delta \rfloor$: calcula la celda de un punto | Cada nodo prueba el signo de un polinomio de grado $\leq d$; la parte entera no es un polinomio (es discontinua, y con ella se separan en $O(1)$ pasos muchas componentes conexas que Ben-Or obliga a pagar una por una). |
| **Tabla hash / acceso indirecto**: `celdas.get(c)` lee una posición de memoria cuya dirección depende de los datos | El árbol no tiene memoria: el camino solo depende de signos de polinomios fijos de la entrada. |
| **Aleatoriedad**: orden de inserción y función hash aleatorios; el costo es esperado | El árbol del Teorema es determinista. Los dos primeros ingredientes son los que sacan al algoritmo del modelo; la aleatoriedad por sí sola no alcanza, porque también se conocen cotas $\Omega(n \log n)$ para árboles de decisión algebraicos aleatorios (Grigoriev, Karpinski, Meyer auf der Heide y Smolensky). |

**Coherencia con la reducción.** En M2, ED se resuelve en $O(n)$ esperado de forma trivial: se inserta cada $x_i$ en una tabla hash y se mira si ya estaba. Eso también "rompe" la cota de ED, que es exactamente lo que dice la reducción: CP y ED no pueden separarse dentro de M1, y fuera de M1 ambos son lineales. La cota no se viola: **una cota mínima es una afirmación sobre un modelo** (conferencia 2), y M2 es otro modelo.

## 4. Adaptación a una dimensión

### 4.1. La idea

Si $\delta$ es la distancia mínima entre los puntos ya insertados, ningún par de ellos está a distancia menor que $\delta$. Se divide la recta en **celdas de ancho $\delta$**: $[c\delta, (c+1)\delta)$, con índice $c = \lfloor x / \delta \rfloor$. Entonces:

1. **Cada celda tiene a lo sumo un punto**: dos puntos de la misma celda estarían a distancia $< \delta$.
2. **Un punto nuevo $p$ solo puede tener un vecino a distancia $< \delta$ en las celdas $c-1$, $c$ y $c+1$**: son 3 celdas, con a lo sumo 3 puntos que mirar.

En el plano la rejilla es de dos dimensiones y hay que mirar una vecindad de celdas (en la versión estándar, de lado $\delta/2$ y vecindad $5 \times 5$). En una dimensión, la misma idea necesita solo **3 celdas**.

### 4.2. El algoritmo

```python
import random

def par_aleatorio(x):
    n = len(x)                                    # n >= 2; x entero o racional exacto
    orden = list(range(n)); random.shuffle(orden)        # inserción en orden aleatorio
    p0, p1 = orden[0], orden[1]
    delta = abs(x[p0] - x[p1]); par = (p0, p1)
    if delta == 0:
        return par, delta                         # distancia 0: no se puede mejorar
    celdas = {}                                   # tabla hash: celda -> índice del punto
    def reconstruir(k):                           # pone orden[0..k-1] con el ancho actual
        celdas.clear()
        for t in orden[:k]:
            celdas[x[t] // delta] = t
    reconstruir(2)
    for k in range(2, n):
        p = orden[k]; c = x[p] // delta
        mejor, cand = delta, None
        for d in (c - 1, c, c + 1):               # solo 3 celdas
            q = celdas.get(d)
            if q is not None and abs(x[p] - x[q]) < mejor:
                mejor, cand = abs(x[p] - x[q]), q
        if cand is None:
            celdas[c] = p                         # no mejora: se inserta
        else:
            delta, par = mejor, (p, cand)         # mejora: nuevo par y nuevo ancho
            if delta == 0:
                return par, delta
            reconstruir(k + 1)                    # la rejilla se rehace con el ancho nuevo
    return par, delta
```

La división `//` supone aritmética exacta (enteros o racionales). Con reales de máquina, el redondeo de $x/\delta$ puede colocar un punto en la celda equivocada.

### 4.3. Lema de las celdas

**Lema 2.** Sean $\delta > 0$ y $c(y) = \lfloor y / \delta \rfloor$.

1. Si $c(p) = c(q)$, entonces $|p - q| < \delta$.
2. Si $|p - q| < \delta$, entonces $c(q) \in \{c(p) - 1,\ c(p),\ c(p) + 1\}$.

*Demostración.* (1) Ambos están en $[c\delta, (c+1)\delta)$, un intervalo semiabierto de longitud $\delta$. (2) Sea $c = c(p)$, o sea, $c\delta \leq p < (c+1)\delta$. Si $|p - q| < \delta$, entonces $q > p - \delta \geq (c-1)\delta$, así que $c(q) \geq c - 1$; y $q < p + \delta < (c+2)\delta$, así que $c(q) \leq c + 1$. ∎

### 4.4. Invariante (correctitud parcial)

Sea $S_k$ el conjunto de los primeros $k$ puntos del orden aleatorio.

> **$J(k)$.** Al empezar el paso $k$ (ya procesados los puntos $\texttt{orden}[0..k-1]$): (1) `par` es un par más cercano de $S_k$ y $\delta > 0$ es su distancia; (2) `celdas` contiene exactamente los puntos de $S_k$, cada uno en la celda $\lfloor x / \delta \rfloor$, y **no hay dos en la misma celda**.

**Inicialización ($k = 2$).** `par` es el único par de $S_2$ y $\delta > 0$ (si fuera $0$, el algoritmo ya habría devuelto). Los dos puntos están a distancia exactamente $\delta$, así que por el Lema 2(1) no comparten celda. ✔

**Mantenimiento.** Sea $p$ el punto nuevo y supongamos $J(k)$.

- **Caso A: existe $q \in S_k$ con $|p - q| < \delta$.** Por el Lema 2(2), todos esos $q$ están en las celdas $c-1$, $c$, $c+1$, que por $J(k)$ contienen a lo sumo un punto cada una. El ciclo los examina a todos y se queda con el más cercano, $q^*$, a distancia $\delta' = \min_{q \in S_k} |p - q| < \delta$. Todos los pares que no involucran a $p$ están a distancia $\geq \delta > \delta'$, así que $(p, q^*)$ es un par más cercano de $S_{k+1}$. Si $\delta' = 0$ ya no se puede mejorar y se devuelve. Si no, se reconstruye la rejilla con ancho $\delta'$: como $\delta'$ es la distancia mínima de $S_{k+1}$, por el Lema 2(1) no hay dos puntos en la misma celda. ✔
- **Caso B: ningún $q \in S_k$ está a distancia $< \delta$.** Los pares que involucran a $p$ están a distancia $\geq \delta$, así que `par` sigue siendo un par más cercano de $S_{k+1}$. Además, la celda de $p$ está vacía (un punto en ella estaría a distancia $< \delta$ por el Lema 2(1)), y al insertarlo no hay colisión. ✔

**Conclusión.** Tras el paso $n - 1$, $S_n$ es todo el conjunto, y por $J(n)$ el par devuelto es un par más cercano. ∎ (Si se devolvió antes por $\delta = 0$, la distancia $0$ es el mínimo posible.)

### 4.5. Costo esperado: análisis hacia atrás

**Teorema.** El tiempo esperado es $O(n)$, para toda entrada.

*Supuestos de M2:* $\lfloor x / \delta \rfloor$ se calcula en $O(1)$ y las operaciones de la tabla hash cuestan $O(1)$ esperado (hash universal).

**Paso 1: probabilidad de reconstruir.** Sea $R_k$ el suceso de que, al insertar el $k$-ésimo punto ($k \geq 3$), $\delta$ baje estrictamente. Condicionado al *conjunto* $S_k$ de los primeros $k$ puntos, su orden interno es una permutación uniforme, así que el último punto es uniforme entre los $k$. Ahora bien, $\delta$ baja si y solo si **todo** par más cercano de $S_k$ contiene al último punto (si hubiera un par más cercano que no lo contiene, la distancia mínima no cambia). El conjunto de puntos contenidos en todos los pares más cercanos tiene a lo sumo $2$ elementos. Por tanto

$$\Pr[R_k] \leq \frac{2}{k}.$$

**Paso 2: suma.** Cada paso $k$ cuesta $O(1)$ esperado (3 consultas y, quizá, una inserción) más, si hay reconstrucción, $O(k)$ esperado (insertar $k$ puntos). El costo esperado total es

$$O(n) + \sum_{k=3}^{n} \Pr[R_k] \cdot O(k) \leq O(n) + \sum_{k=3}^{n} \frac{2}{k} \cdot O(k) = O(n) + O(n) = O(n). \qquad ∎$$

El número esperado de reconstrucciones es $\leq \sum_{k=3}^n 2/k = 2(H_n - 3/2) \approx 2 \ln n$.

**Advertencias.**

- La garantía es de **costo esperado** (sobre el orden aleatorio y el hash), no de peor caso: una permutación desafortunada podría reconstruir en muchos pasos y llegar a $\Theta(n^2)$, con probabilidad ínfima.
- El algoritmo determinista de ordenar y recorrer vecinos hace $O(n \log n)$ en cualquier modelo razonable y es óptimo en M1; el aleatorio gana solo porque M2 tiene $\lfloor \cdot \rfloor$ y tabla hash.

## 5. Experimento

### 5.1. Código

```python
import itertools, random, math, statistics as st
from fractions import Fraction

# --- La reducción ED <= par más cercano, con una referencia por ordenamiento ---
def par_ordenando(x):
    idx = sorted(range(len(x)), key=lambda i: x[i])
    return min(zip(idx, idx[1:]), key=lambda p: abs(x[p[0]] - x[p[1]]))

def distintos_via_reduccion(x):
    i, j = par_ordenando(x)
    return x[i] != x[j]                    # el único test extra de la reducción

tot = 0
for n in range(2, 6):
    for x in itertools.product(range(5), repeat=n):
        assert distintos_via_reduccion(list(x)) == (len(set(x)) == n)
        tot += 1
print("reducción ED <= par más cercano:", tot, "vectores")

# --- El algoritmo de §4, con contadores opcionales ---
def par_aleatorio(x, ops=None):
    n = len(x)
    orden = list(range(n)); random.shuffle(orden)
    p0, p1 = orden[0], orden[1]
    delta = abs(x[p0] - x[p1]); par = (p0, p1)
    if delta == 0:
        return par, delta
    celdas = {}
    def reconstruir(k):
        celdas.clear()
        for t in orden[:k]:
            celdas[x[t] // delta] = t
        if ops is not None:
            ops["dic"] += k; ops["reconstrucciones"] += 1; ops["trabajo_rec"] += k
    reconstruir(2)
    if ops is not None:
        ops["reconstrucciones"] -= 1; ops["trabajo_rec"] -= 2        # la inicial no cuenta
    for k in range(2, n):
        p = orden[k]; c = x[p] // delta
        mejor, cand = delta, None
        for d in (c - 1, c, c + 1):
            q = celdas.get(d)
            if ops is not None:
                ops["dic"] += 1
            if q is not None and abs(x[p] - x[q]) < mejor:
                mejor, cand = abs(x[p] - x[q]), q
        if cand is None:
            celdas[c] = p
            if ops is not None:
                ops["dic"] += 1
        else:
            delta, par = mejor, (p, cand)
            if delta == 0:
                return par, delta
            reconstruir(k + 1)
            if ops is not None:
                ops["rebuild_en"].append(k + 1)
    return par, delta

def referencia(x):
    s = sorted(x)
    return min(b - a for a, b in zip(s, s[1:]))

# --- Correctitud ---
random.seed(1)
casos = 0
for _ in range(30000):                                  # enteros, con y sin muchos repetidos
    n = random.randint(2, 30)
    R = random.choice([3, 10, 100, 10**6, 10**12])
    x = [random.randint(-R, R) for _ in range(n)]
    (i, j), d = par_aleatorio(x)
    assert i != j and abs(x[i] - x[j]) == d == referencia(x), (x, i, j, d)
    casos += 1
for _ in range(3000):                                   # racionales exactos
    n = random.randint(2, 25)
    x = [Fraction(random.randint(-50, 50), random.randint(1, 9)) for _ in range(n)]
    (i, j), d = par_aleatorio(x)
    assert i != j and abs(x[i] - x[j]) == d == referencia(x)
    casos += 1
print("correctitud OK:", casos, "instancias")
```

El bloque siguiente (continúa del anterior) calcula el **árbol de comparaciones óptimo para ED** con $n$ pequeño. Las instancias son todos los órdenes débiles de $n$ elementos (cada punto de $\mathbb{R}^n$ cae en uno), las pruebas son el signo de $x_i - x_j$, y una hoja es válida si todas sus instancias tienen la misma respuesta.

```python
import time
from math import factorial, ceil, log

def optimo_ED(n):
    inst = []
    for v in itertools.product(range(n), repeat=n):
        if set(v) == set(range(len(set(v)))):            # órdenes débiles (rangos densos)
            inst.append(v)
    yes = [len(set(v)) == n for v in inst]
    pares = [(i, j) for i in range(n) for j in range(i + 1, n)]
    sg = {p: [(v[p[0]] > v[p[1]]) - (v[p[0]] < v[p[1]]) for v in inst] for p in pares}
    memo = {}
    def dec(S, k):
        if len({yes[i] for i in S}) <= 1:
            return True
        if k == 0:
            return False
        if (S, k) not in memo:
            ok = False
            for p in pares:
                partes = {}
                for i in S:
                    partes.setdefault(sg[p][i], []).append(i)
                if len(partes) >= 2 and all(dec(frozenset(q), k - 1) for q in partes.values()):
                    ok = True
                    break
            memo[(S, k)] = ok
        return memo[(S, k)]
    S0, k = frozenset(range(len(inst))), 0
    while not dec(S0, k):
        k += 1
    return k, len(inst)

print("n  órdenes_débiles  n!  ceil(log3 n!)  óptimo_exacto")
for n in range(2, 6):                                    # con range(2, 7) el caso n=6 tarda ~2 min
    k, N = optimo_ED(n)
    print(n, N, factorial(n), ceil(log(factorial(n), 3) - 1e-12), k)
```

El último bloque mide el costo esperado del algoritmo aleatorio (tarda unos 2 minutos).

```python
def H(n):
    return sum(1.0 / k for k in range(1, n + 1))

random.seed(2026)
print("n  T  ops_dic/n  reconstr.  2(H_n-3/2)  trabajo_rec/n  log2 n")
for n, T in [(10**3, 400), (10**4, 200), (10**5, 60), (10**6, 15)]:
    a, b, c = [], [], []
    for _ in range(T):
        x = [random.randint(0, 10**15) for _ in range(n)]
        ops = {"dic": 0, "reconstrucciones": 0, "trabajo_rec": 0, "rebuild_en": []}
        par_aleatorio(x, ops)
        a.append(ops["dic"] / n); b.append(ops["reconstrucciones"]); c.append(ops["trabajo_rec"] / n)
    ee = lambda v: st.stdev(v) / math.sqrt(len(v))
    print(f"{n} {T} {st.mean(a):.3f}±{ee(a):.3f} {st.mean(b):.2f}±{ee(b):.2f} "
          f"{2 * (H(n) - 1.5):.2f} {st.mean(c):.3f}±{ee(c):.3f} {math.log2(n):.2f}", flush=True)

# Probabilidad de reconstruir en el paso k, frente a la cota 2/k
random.seed(7)
n, T = 200, 20000
cuenta = {}
for _ in range(T):
    x = [random.randint(0, 10**15) for _ in range(n)]
    ops = {"dic": 0, "reconstrucciones": 0, "trabajo_rec": 0, "rebuild_en": []}
    par_aleatorio(x, ops)
    for k in ops["rebuild_en"]:
        cuenta[k] = cuenta.get(k, 0) + 1
for k in (3, 4, 5, 10, 50, 100, 200):
    print(k, round(cuenta.get(k, 0) / T, 4), round(2 / k, 4))

# Con muchos pares más cercanos empatados (progresión aritmética): la cota 2/k sigue valiendo
random.seed(9)
n, T = 100, 20000
cuenta = {}
for _ in range(T):
    x = list(range(0, n * 7, 7))
    ops = {"dic": 0, "reconstrucciones": 0, "trabajo_rec": 0, "rebuild_en": []}
    par_aleatorio(x, ops)
    for k in ops["rebuild_en"]:
        cuenta[k] = cuenta.get(k, 0) + 1
print({k: round(cuenta.get(k, 0) / T, 4) for k in (3, 4, 5, 10, 50, 100)})
```

### 5.2. Resultados (ejecutado)

| Comprobación | Casos | Resultado |
|---|---|---|
| Reducción: ED $\iff$ ($x_i \neq x_j$ para el par más cercano) | 3900 vectores ($n = 2..5$, valores en $0..4$) | se cumple |
| Correctitud del algoritmo aleatorio (distancia $=$ mínimo por ordenamiento, $i \neq j$) | 33 000 instancias: 30 000 enteros (rangos de $3$ hasta $10^{12}$, con muchos repetidos) y 3000 racionales exactos | se cumple |

**Árbol de comparaciones óptimo para ED** (búsqueda exhaustiva sobre todos los órdenes débiles):

| $n$ | Órdenes débiles | $n!$ | Cota del Teorema A: $\lceil \log_3 n! \rceil$ | Óptimo exacto |
|---|---|---|---|---|
| 2 | 3 | 2 | 1 | 1 |
| 3 | 13 | 6 | 2 | 3 |
| 4 | 75 | 24 | 3 | 5 |
| 5 | 541 | 120 | 5 | 7 |
| 6 | 4683 | 720 | 6 | 10 |

El óptimo exacto respeta siempre la cota del Teorema A. Para $n$ pequeño la cota ternaria es floja (cada hoja "sí" es un ordenamiento y el árbol real necesita más pruebas para separarlos); lo que importa es el orden de crecimiento.

**Costo esperado del algoritmo aleatorio** (valores en $0..10^{15}$, $T$ ejecuciones por tamaño; media $\pm$ error estándar):

| $n$ | $T$ | Operaciones de diccionario por punto | Reconstrucciones | $2(H_n - 3/2)$ | Trabajo de reconstrucción por punto | $\log_2 n$ |
|---|---|---|---|---|---|---|
| $10^3$ | 400 | $6{,}02 \pm 0{,}05$ | $12{,}07 \pm 0{,}16$ | $11{,}97$ | $2{,}03 \pm 0{,}05$ | $9{,}97$ |
| $10^4$ | 200 | $5{,}92 \pm 0{,}07$ | $16{,}36 \pm 0{,}28$ | $16{,}58$ | $1{,}92 \pm 0{,}07$ | $13{,}29$ |
| $10^5$ | 60 | $6{,}15 \pm 0{,}14$ | $21{,}90 \pm 0{,}50$ | $21{,}18$ | $2{,}15 \pm 0{,}14$ | $16{,}61$ |
| $10^6$ | 15 | $5{,}64 \pm 0{,}23$ | $23{,}87 \pm 1{,}66$ | $25{,}79$ | $1{,}64 \pm 0{,}23$ | $19{,}93$ |

Las operaciones por punto se quedan en torno a $6$ (3 consultas $+$ 1 inserción $+$ unas $2$ de reconstrucción) cuando $n$ crece mil veces, mientras que $\log_2 n$ se duplica. El número de reconstrucciones sigue la fórmula $2(H_n - 3/2) \approx 2 \ln n$, y el trabajo de reconstrucción por punto es $\approx 2$, como predice $\sum_k (2/k) \cdot k = 2n$.

**Probabilidad de reconstruir en el paso $k$** ($n = 200$, 20 000 ejecuciones):

| $k$ | 3 | 4 | 5 | 10 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|
| Empírica | 0,6656 | 0,4998 | 0,3985 | 0,2027 | 0,0400 | 0,0198 | 0,0106 |
| Cota $2/k$ | 0,6667 | 0,5000 | 0,4000 | 0,2000 | 0,0400 | 0,0200 | 0,0100 |

Con muchos pares más cercanos empatados (progresión aritmética, $n = 100$), la probabilidad queda por debajo de $2/k$ ($0{,}6655$, $0{,}484$, $0{,}3764$, $0{,}1314$, $0$ y $0$ para $k = 3, 4, 5, 10, 50, 100$), como exige el Paso 1 de §4.5.

## 6. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Dados $x_1, \ldots, x_n$, hallar $(i, j)$ que minimiza $\lvert x_i - x_j \rvert$. En una dimensión basta mirar vecinos del orden. |
| ¿Se puede mejor? (cota) | $\Omega(n \log n)$ en árboles de decisión algebraicos, **por reducción desde ED**: cada hoja $(i,j)$ se cambia por el test $x_i - x_j$ (una prueba más), y por el Lema 1 el árbol decide ED. ED cuesta $\Omega(n \log n)$ (Ben-Or). |
| ¿Es ajustada? | Sí en ese modelo: ordenar y recorrer vecinos hace $O(n \log n)$ pruebas. |
| ¿Quién rompe la cota? | El **algoritmo aleatorio incremental con rejilla y tabla hash** de la conferencia 2, de costo esperado lineal. |
| ¿En qué modelo? | RAM con **parte entera**, **acceso indirecto (tabla hash)** y **aleatoriedad**: tres cosas que un árbol de decisión algebraico no tiene. Una cota es una afirmación sobre un modelo. |
| ¿Cómo en una dimensión? | Celdas de ancho $\delta$, a lo sumo un punto por celda, **3 celdas vecinas**. Invariante: la rejilla contiene los puntos procesados sin colisión y `par` es el más cercano. Reconstrucción con probabilidad $\leq 2/k$ en el paso $k$, así que el costo esperado es $O(n)$. |
