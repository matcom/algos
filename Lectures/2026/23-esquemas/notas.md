# Esquemas de aproximación {#chap-esquemas}

```{python echo=false output=asis}
import math
import os
import random
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_23.py
import figuras_23 as F23
```

El capítulo 21 terminó con una tabla de razones: 2 para vertex cover, $4/3$ para LPT,
$H_n$ para set cover. Cada una es un número fijo, y para mejorarlo hacía falta otra
cota del óptimo u otro algoritmo. Este capítulo cambia la pregunta. En lugar de un
algoritmo con una razón, queremos una **familia** de algoritmos, uno por cada
$\varepsilon > 0$, que se acerque al óptimo tanto como pidamos y cobre la precisión en
tiempo. La pregunta que ordena todo el capítulo es dónde se cobra: en el exponente de
$n$, o como un factor polinomial en $1/\varepsilon$. Y la respuesta, que es la parte
sorprendente, la deciden los números que trae la entrada.

## 1. Una familia de algoritmos

**Definición.** Un **esquema de aproximación polinomial** (PTAS, por *polynomial-time
approximation scheme*) para un problema de minimización es un algoritmo que recibe una
entrada $I$ y un $\varepsilon > 0$, devuelve una solución factible de costo a lo sumo
$(1 + \varepsilon)\,\mathrm{OPT}(I)$, y para cada $\varepsilon$ fijo corre en tiempo
polinomial en $|I|$. Para maximización, el valor es al menos
$(1 - \varepsilon)\,\mathrm{OPT}(I)$. Si además el tiempo es polinomial en $|I|$ **y en
$1/\varepsilon$** a la vez, el esquema es **totalmente polinomial** (FPTAS).

La diferencia está en dónde aparece $\varepsilon$. Un algoritmo que tarda
$O(n^{1/\varepsilon})$ es un PTAS: con $\varepsilon = 1/2$ es cuadrático, con
$\varepsilon = 1/10$ es de grado 10, y para cada $\varepsilon$ fijo es un polinomio. No
es un FPTAS, porque $n^{1/\varepsilon}$ no está acotado por ningún polinomio en $n$ y
$1/\varepsilon$. Un algoritmo de $O(n^3/\varepsilon)$ sí es un FPTAS: pedir diez veces
más precisión cuesta diez veces más tiempo, y el exponente de $n$ no se mueve.

Con $n = 100$ y $\varepsilon = 0{,}01$, el primero hace del orden de $10^{200}$ pasos y
el segundo $10^8$. Los dos son "polinomiales para cada $\varepsilon$", y solo uno se
puede ejecutar.

El capítulo 1, §8 llamó **pseudopolinomial** a un algoritmo polinomial en el valor de
los números de la entrada pero no en su cantidad de bits, como la tabla de $O(nW)$ de
la mochila, y el capítulo 16, §3 explicó por qué esa tabla no pone a la mochila en P.
Este capítulo la usa, cambiada de índice, para construir un FPTAS.

## 2. La tabla por valores

La mochila 0-1 es la del capítulo 20, §2: el objeto $i$ pesa $p_i$ y vale $v_i$,
enteros positivos, y la capacidad es $W$. La tabla `mochila_dp` del capítulo 20 guarda
el mejor valor para cada capacidad $c \le W$, en $O(nW)$: es barata cuando los
**pesos** son chicos.

Hay otra tabla que se puede llenar, con los papeles cambiados. Para cada valor $x$,
guardamos el **menor peso** con el que se consigue valor exactamente $x$ usando los
objetos vistos hasta ahora. Con $V = \sum_i v_i$, hay $V + 1$ valores posibles, y cada
objeto actualiza la tabla en una pasada de derecha a izquierda, como la otra:
$$\mathrm{peso}_i(x) = \min\bigl(\mathrm{peso}_{i-1}(x),\;
\mathrm{peso}_{i-1}(x - v_i) + p_i\bigr).$$
La respuesta es el mayor $x$ con $\mathrm{peso}_n(x) \le W$. Cuesta $O(nV)$, y como
$V \le n\,v_{\max}$, es $O(n^2 v_{\max})$: barata cuando los **valores** son chicos.

Para devolver el conjunto y no solo el valor, cada objeto deja una fila de bits que dice
en qué valores mejoró la tabla. Recorrerlas de atrás hacia adelante reconstruye la
elección sin copiar listas, que costaría un factor $n$ más.

```{python continue}
def mochila_valores(p, v, W):
    """Mochila exacta por valores: O(n * sum(v)). Devuelve (valor, objetos)."""
    V = sum(v)
    INF = float("inf")
    peso = [0] + [INF] * V          # peso[x]: menor peso con valor exactamente x
    mejoro = []
    for i in range(len(p)):
        fila = bytearray(V + 1)
        for x in range(V, v[i] - 1, -1):
            if peso[x - v[i]] + p[i] < peso[x]:
                peso[x] = peso[x - v[i]] + p[i]
                fila[x] = 1
        mejoro.append(fila)
    mejor = max(x for x in range(V + 1) if peso[x] <= W)
    S, x = [], mejor
    for i in reversed(range(len(p))):
        if mejoro[i][x]:
            S.append(i)
            x -= v[i]
    return mejor, S[::-1]

def fuerza_bruta(p, v, W):
    n, mejor = len(p), 0
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        if sum(p[i] for i in S) <= W:
            mejor = max(mejor, sum(v[i] for i in S))
    return mejor

rng = random.Random(23)
for _ in range(800):
    n = rng.randint(1, 8)
    p = [rng.randint(1, 30) for _ in range(n)]
    v = [rng.randint(1, 100) for _ in range(n)]
    W = rng.randint(1, sum(p))
    valor, S = mochila_valores(p, v, W)
    assert valor == fuerza_bruta(p, v, W)
    assert sum(p[i] for i in S) <= W and sum(v[i] for i in S) == valor
print("800 instancias: el valor y el conjunto coinciden con la fuerza bruta")
```

La segunda `assert` mira el conjunto reconstruido: un error en la reconstrucción
pasaría la primera y no la segunda.

## 3. Redondear los valores

Ahora la idea, que es casi una broma: si la tabla es barata cuando los valores son
chicos, **hagamos chicos los valores**. Dividimos cada $v_i$ por un paso $\mu$, tiramos
la parte fraccionaria, resolvemos exacto con los valores redondeados $v'_i$ y
devolvemos el conjunto que salga, que es factible porque los pesos no se tocaron.

¿Qué paso elegir? El primer intento que se le ocurre a uno es una constante, por
ejemplo $\mu = 1\,000$. No sirve: si todos los valores son menores que 1 000, todos se
redondean a 0 y el algoritmo devuelve cualquier cosa; si son del orden de $10^{12}$,
la tabla sigue siendo enorme. El paso tiene que medirse con la escala de la entrada.
La escala más a mano es el mayor valor, $v_{\max}$, y el paso que hace funcionar las
cuentas de §4 y §5 es
$$\mu = \frac{\varepsilon\, v_{\max}}{n}, \qquad v'_i = \Bigl\lfloor \frac{v_i}{\mu}
\Bigr\rfloor = \Bigl\lfloor \frac{n\, v_i}{\varepsilon\, v_{\max}} \Bigr\rfloor.$$
Con este paso, el objeto más valioso queda con $v'_i = \lfloor n/\varepsilon \rfloor$,
y todos los demás con algo menor o igual. Antes de redondear se tiran los objetos que
no caben solos, los de $p_i > W$, y $n$ y $v_{\max}$ se cuentan **después**, como hace
el código. Parece limpieza, y no lo es: la §4 dice por qué, y la §6 qué pasa si se
olvida.

```{python continue}
def fptas_mochila(p, v, W, eps):
    """FPTAS de mochila: eps es una Fraction. Devuelve (valor real, objetos)."""
    caben = [i for i in range(len(p)) if p[i] <= W]
    if not caben:
        return 0, []
    n, vmax = len(caben), max(v[i] for i in caben)
    # v'_i = piso(n v_i / (eps vmax)), en aritmética entera
    vr = [(v[i] * n * eps.denominator) // (eps.numerator * vmax) for i in caben]
    _, S = mochila_valores([p[i] for i in caben], vr, W)
    S = [caben[j] for j in S]
    return sum(v[i] for i in S), S

rng = random.Random(21)
p = [rng.randint(1, 20) for _ in range(8)]
v = [rng.randint(10, 100) for _ in range(8)]
W, eps = sum(p) // 2, Fraction(1, 2)
mu = eps * max(v) / len(p)
vr = [math.floor(x / mu) for x in v]
valor, S = fptas_mochila(p, v, W, eps)
print(f"pesos {p}, W = {W}")
print(f"valores {v}, mu = {mu} = {float(mu):.3f}")
print(f"redondeados {vr}")
print(f"FPTAS: objetos {[i + 1 for i in S]}, valor {valor}; óptimo {fuerza_bruta(p, v, W)}")
```

El redondeo va en enteros porque, con $\mu$ en coma flotante, un múltiplo exacto de
$\mu$ puede dar $3{,}9999\ldots$ y redondearse a 3.

```{python continue echo=false output=asis}
print(F23.redondeo(v, vr, float(mu), pie=(
    f"Los ocho valores del ejemplo con ε = 1/2, así que μ = εv<sub>max</sub>/n = "
    f"{float(mu):.3f}. Cada columna llega a v<sub>i</sub>; la parte azul es "
    f"μ·v'<sub>i</sub>, lo que el algoritmo ve, y la naranja es lo que el redondeo "
    f"tiró, siempre menos de un paso μ.")))
```

La @fig-esq-redondeo muestra lo que ve el algoritmo. Ninguna columna pierde un paso
completo, y eso es todo lo que la demostración necesita: cada objeto pierde menos de
$\mu$, y un conjunto tiene a lo sumo $n$ objetos. En este ejemplo el redondeo sí cambió
la respuesta: el FPTAS devuelve 235 y el óptimo vale 241. Perdió 6, y $\varepsilon = 1/2$
le permitía perder hasta la mitad.

## 4. La razón 1 − ε

**Teorema 1.** Para todo $\varepsilon$ con $0 < \varepsilon < 1$, `fptas_mochila`
devuelve un conjunto factible de valor al menos $(1 - \varepsilon)\,\mathrm{OPT}$.

*Demostración.* Sea $S$ el conjunto que devuelve y $S^*$ uno óptimo, los dos dentro de
los objetos que caben. Escribimos $v(A) = \sum_{i \in A} v_i$ y
$v'(A) = \sum_{i \in A} v'_i$. Hay tres pasos.

Primero, el redondeo pierde menos de un paso por objeto. Como $v'_i = \lfloor v_i/\mu
\rfloor$, se cumple $v_i/\mu - 1 < v'_i \le v_i/\mu$, y multiplicando por $\mu$,
$$v_i - \mu < \mu\, v'_i \le v_i.$$

Segundo, $S$ es óptimo para los valores redondeados, porque la tabla de §2 es exacta, y
$S^*$ es factible. Entonces $v'(S) \ge v'(S^*)$.

Tercero, encadenamos:
$$v(S) \;\ge\; \mu\, v'(S) \;\ge\; \mu\, v'(S^*) \;>\; v(S^*) - |S^*|\,\mu \;\ge\;
\mathrm{OPT} - n\mu \;=\; \mathrm{OPT} - \varepsilon\, v_{\max}.$$
La primera desigualdad es la mitad derecha del primer paso, sumada sobre $S$; la
segunda es el segundo paso; la tercera es la mitad izquierda del primer paso, sumada
sobre $S^*$.

Falta comparar $\varepsilon\, v_{\max}$ con $\varepsilon\,\mathrm{OPT}$, y aquí está el
paso que se salta casi todo el mundo: $v_{\max} \le \mathrm{OPT}$. Es cierto porque el
objeto más valioso **cabe solo** en la mochila, así que el conjunto que lo contiene a él
solo es factible y vale $v_{\max}$. Y cabe solo porque el algoritmo tiró los que no
caben antes de calcular $v_{\max}$. Con eso, $v(S) > \mathrm{OPT} - \varepsilon\,
\mathrm{OPT} = (1-\varepsilon)\,\mathrm{OPT}$. $\square$

La demostración nunca calcula $\mathrm{OPT}$: compara contra él a través de
$v_{\max}$, una cota del óptimo que sí se calcula. Es la técnica del capítulo 21, §1.

La idea de redondear los valores y resolver exacto con la tabla por valores es de Oscar
Ibarra y Chul Kim, "Fast Approximation Algorithms for the Knapsack and Sum of Subset
Problems" (*Journal of the ACM* 22(4), 1975, pp. 463–468). Esta es la versión
simplificada de Williamson y Shmoys, *The Design of Approximation Algorithms*
(Cambridge University Press, 2011, §3.1).

Ahora la comprobación contra el oráculo, con tres valores de $\varepsilon$:

```{python continue}
def peor_razon(eps, veces=600, semilla=1):
    rng = random.Random(semilla)
    peor = Fraction(1)
    for _ in range(veces):
        n = rng.randint(1, 8)
        p = [rng.randint(1, 30) for _ in range(n)]
        v = [rng.randint(1, 1000) for _ in range(n)]
        W = rng.randint(1, sum(p))
        opt = fuerza_bruta(p, v, W)
        valor, _ = fptas_mochila(p, v, W, eps)
        if opt > 0:
            assert valor >= (1 - eps) * opt
            peor = min(peor, Fraction(valor, opt))
    return peor

for eps in [Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)]:
    print(f"eps = {eps}: peor razón medida {float(peor_razon(eps)):.3f}, "
          f"cota {float(1 - eps):.3f}")
```

La cota se cumple siempre, y con holgura: el peor caso medido está muy por encima de
$1 - \varepsilon$. La holgura viene del tercer paso, que supone que **cada** objeto del
óptimo pierde casi un paso entero y que el óptimo tiene $n$ objetos, y además que
$\mathrm{OPT} = v_{\max}$. Con $n \ge 2$ las dos últimas no pueden pasar a la vez: si el
óptimo tiene los $n$ objetos, vale más que $v_{\max}$. El ejercicio 9 busca
entradas que se acerquen a la cota.

## 5. El tiempo

**Teorema 2.** `fptas_mochila` corre en tiempo $O(n^3/\varepsilon)$.

*Demostración.* Tirar los objetos que no caben y redondear cuesta $O(n)$. Cada valor
redondeado cumple $v'_i \le \lfloor n\,v_{\max}/(\varepsilon\, v_{\max}) \rfloor =
\lfloor n/\varepsilon \rfloor$, así que la suma de los redondeados es
$V' \le n \lfloor n/\varepsilon \rfloor$. La tabla de §2 sobre esos valores hace $n$
pasadas de a lo sumo $V' + 1$ celdas cada una, con trabajo constante por celda, y la
reconstrucción recorre $n$ filas. En total, $O(n \cdot n^2/\varepsilon) =
O(n^3/\varepsilon)$. $\square$

Lo que se cuenta es el número de operaciones sobre enteros de
$O(\log(n\,v_{\max}/\varepsilon) + \log(n\,p_{\max}))$ bits (los valores y los pesos
acumulados que guarda la tabla), como en el modelo RAM del capítulo 1. En el modelo por bit hay
que multiplicar por el costo de sumar dos de esos números, que es lineal en su largo:
sigue siendo polinomial en el tamaño de la entrada y en $1/\varepsilon$.

El tiempo ya no depende de $v_{\max}$. Con valores de hasta $10^6$ y 40 objetos, la
tabla exacta de §2 tendría hasta $40 \cdot 40 \cdot 10^6$ celdas. Midamos el FPTAS:

```{python continue}
rng = random.Random(5)
n = 40
p40 = [rng.randint(1, 1000) for _ in range(n)]
v40 = [rng.randint(1, 10**6) for _ in range(n)]
W40 = sum(p40) // 2
print(f"tabla exacta: {n * sum(v40):.3g} celdas")
medidas = []
for k in [2, 4, 8, 16, 32]:
    eps = Fraction(1, k)
    vmax = max(v40)
    celdas = n * sum((x * n * k) // vmax for x in v40)
    t = math.inf
    for _ in range(3):                     # el mínimo de tres, contra el ruido
        t0 = time.perf_counter()
        valor, _ = fptas_mochila(p40, v40, W40, eps)
        t = min(t, time.perf_counter() - t0)
    medidas.append((k, t))
    print(f"1/eps = {k:2d}: {celdas:7d} celdas, {t:.3f} s, valor {valor}")
```

```{python continue echo=false output=asis}
print(F23.tiempos(medidas, pie=(
    "Tiempo medido del FPTAS sobre 40 objetos con valores hasta 10⁶, contra 1/ε, en "
    "escala logarítmica. La recta de pendiente 1 pasa por el último punto: es lo que "
    "predice O(n³/ε) con n fijo.")))
```

El número de celdas se duplica cada vez que se duplica $1/\varepsilon$, porque cada
$v'_i$ es proporcional a $1/\varepsilon$ salvo el piso. En la
@fig-esq-tiempo el tiempo sigue en conjunto a la recta de pendiente 1, aunque los
primeros puntos, de centésimas de segundo, se mueven de una corrida a otra: se midieron
en una máquina compartida. El conteo de celdas es exacto y no depende de la máquina.
Fíjate también en la columna del valor:
pasar de $\varepsilon = 1/2$ a $1/32$ cambia el resultado en menos de una parte en mil.
El óptimo de esta entrada no lo calculamos, y no hace falta para saber que el valor de
la última fila está a lo sumo un 3,125 % por debajo de él.

## 6. El error plantado: el objeto que no cabe

La variante plantada es la que se olvida del filtro. Calcula $v_{\max}$ sobre todos
los objetos, incluidos los que pesan más que $W$, y redondea con ese paso:

```{python continue}
def fptas_sin_filtro(p, v, W, eps):
    n, vmax = len(p), max(v)
    vr = [(x * n * eps.denominator) // (eps.numerator * vmax) for x in v]
    _, S = mochila_valores(p, vr, W)
    return sum(v[i] for i in S), S

def bateria(generar, veces=1000, eps=Fraction(1, 2)):
    rng = random.Random(7)
    fallos = alguno_no_cabe = 0
    for _ in range(veces):
        p, v, W = generar(rng)
        opt = fuerza_bruta(p, v, W)
        valor, _ = fptas_sin_filtro(p, v, W, eps)
        alguno_no_cabe += max(p) > W
        fallos += valor < (1 - eps) * opt
    return fallos, alguno_no_cabe

def como_el_20(rng):                 # la instancia del capítulo 20: W = suma/2
    n = rng.randint(2, 8)
    p = [rng.randint(1, 20) for _ in range(n)]
    v = [rng.randint(1, 20) for _ in range(n)]
    return p, v, sum(p) // 2

def todos_caben(rng):
    p, v, _ = como_el_20(rng)
    return p, v, rng.randint(max(p), sum(p))

print("W = suma/2:      (fallos, con alguno que no cabe) =", bateria(como_el_20))
print("todos caben:     (fallos, con alguno que no cabe) =", bateria(todos_caben))
p = [11] + [1] * 10
v = [1000] + [40] * 10
print("construida: sin filtro", fptas_sin_filtro(p, v, 10, Fraction(1, 2))[0],
      "| con filtro", fptas_mochila(p, v, 10, Fraction(1, 2))[0],
      "| óptimo", fuerza_bruta(p, v, 10))
```

La batería que genera instancias como las del capítulo 20 ve el error en 14 de 1 000
entradas, y la que solo genera mochilas donde todo cabe no lo ve nunca: sin un objeto
que no quepa, las dos versiones son el mismo algoritmo. La entrada construida lo
muestra entero. Un objeto de valor 1 000 que no cabe fija el paso en
$\mu = 1\,000/22$, los diez objetos de valor 40 se redondean a 0, y la tabla no tiene
ninguna razón para meterlos: devuelve 0 contra un óptimo de 400. La razón no es mala,
es nula. Bajar $\varepsilon$ no lo arregla: esta entrada se salva con
$\varepsilon = 2/5$, pero para cada $\varepsilon$ basta con que el objeto que no cabe
valga más de $440/\varepsilon$ para que los diez vuelvan a redondearse a 0.

La demostración anunciaba el lugar exacto. El único paso que usaba el filtro era
$v_{\max} \le \mathrm{OPT}$, y es el que falla: el $v_{\max}$ de la variante es el de
un objeto que ningún conjunto factible contiene. Leer la demostración preguntando qué
hipótesis usa cada paso encuentra el error sin ejecutar nada.

## 7. Números chicos, números grandes

La mochila tiene un FPTAS porque tiene una tabla por valores que se deja redondear: el
redondeo convierte una entrada de números grandes en una de números chicos, y la tabla resuelve
exacto las de números chicos. ¿Pasa lo mismo con todo problema NP-duro que tenga
números? No, y para decir por qué hace falta separar dos clases de dificultad.

Para una entrada $I$, sea $\mathrm{Max}(I)$ el mayor número que aparece en ella (el
mayor valor, peso o capacidad, en la mochila). Un algoritmo es pseudopolinomial si
corre en tiempo polinomial en $|I|$ y $\mathrm{Max}(I)$. Escribir los números en
unario, con $x$ símbolos para el número $x$, hace que la entrada mida a lo sumo
$|I| \cdot \mathrm{Max}(I)$ símbolos y al menos $\mathrm{Max}(I)$, así que un algoritmo
pseudopolinomial es uno polinomial sobre esa codificación.

**Definición.** Un problema es **fuertemente NP-duro** si existe un polinomio $p$ tal
que el problema restringido a las entradas con $\mathrm{Max}(I) \le p(|I|)$ ya es
NP-duro. Dicho de otra forma: sigue siendo difícil aunque todos sus números sean
chicos, y por tanto aunque se escriban en unario.

Un problema sin números, como vertex cover, 3-SAT o 3-coloración, es fuertemente NP-duro
sin más: sus únicos números son índices de vértices o de variables, que no pasan de
$|I|$. TSP también lo es, aunque tenga distancias: el capítulo 19, §7 demostró que es
NP-completo con distancias 1 y 2, que son números chicos. La mochila, en cambio, no lo
es, salvo que P = NP, por el teorema siguiente.

**Teorema 3** (Garey y Johnson, 1978). Si un problema fuertemente NP-duro tiene un
algoritmo pseudopolinomial, entonces P = NP.

*Demostración.* Sea $p$ el polinomio de la definición, y $A$ el algoritmo
pseudopolinomial, que corre en tiempo $q(|I|, \mathrm{Max}(I))$ con $q$ un polinomio.
Sobre las entradas con $\mathrm{Max}(I) \le p(|I|)$, $A$ corre en tiempo
$q(|I|, p(|I|))$, que es un polinomio en $|I|$. Así que el problema restringido, que es
NP-duro, se resuelve en tiempo polinomial, y P = NP. $\square$

La mochila tiene tabla pseudopolinomial, así que no es fuertemente NP-dura si P ≠ NP: el capítulo 19, §11 la demostró NP-completa con una
meta $T$ del orden de $10^{n+k}$, y esos números enormes son imprescindibles.

El artículo es "'Strong' NP-Completeness Results: Motivation, Examples, and
Implications" (*Journal of the ACM* 25(3), 1978, pp. 499–508), de Michael Garey y
David Johnson.

## 8. 3-partición y el makespan

El problema que separa las dos clases es este.

**3-PARTICIÓN.** Dados $3q$ enteros positivos $a_1, \dots, a_{3q}$ y una meta $B$, con
$B/4 < a_i < B/2$ para todo $i$ y $\sum_i a_i = qB$, ¿se pueden repartir en $q$ grupos
que sumen $B$ cada uno?

Las cotas $B/4 < a_i < B/2$ obligan a que cada grupo tenga exactamente tres números: dos
suman menos de $B$, y cuatro suman más. De ahí el nombre. Por ejemplo, con $B = 20$, los
números $6, 6, 7, 7, 7, 7$ se reparten en $\{6, 7, 7\}$ y $\{6, 7, 7\}$.

Garey y Johnson demostraron que 3-PARTICIÓN es NP-completo aunque los números se
escriban en unario: es fuertemente NP-completo. La demostración pasa por emparejamiento
tridimensional y por un problema intermedio de cuatro números por grupo, y es larga;
está en su libro *Computers and Intractability: A Guide to the Theory of
NP-Completeness* (W. H. Freeman, 1979). Aquí la usamos sin demostrarla.

Con ella sale el resultado que este capítulo necesita sobre el balanceo de carga del
capítulo 21, §5.

**Teorema 4.** El makespan mínimo con $n$ tareas y $m$ máquinas, cuando $m$ es parte
de la entrada, es fuertemente NP-duro.

*Demostración.* Dada una instancia $a_1, \dots, a_{3q}$, $B$ de 3-PARTICIÓN, construimos
$3q$ tareas de duraciones $t_i = a_i$ y $m = q$ máquinas, y preguntamos si el makespan
puede ser a lo sumo $B$. La construcción copia los números, así que es polinomial y
**no los agranda**: el mayor número de la instancia construida es $\max(\max_i a_i, q)$,
y si los $a_i$ eran polinomiales en el tamaño, lo siguen siendo.

Si hay una 3-partición, cada grupo va a una máquina, que carga $B$. Al revés, si hay
una asignación de makespan a lo sumo $B$, como las cargas suman $qB$ y son $q$
máquinas, cada una carga exactamente $B$, y los grupos de tareas de cada máquina son una
3-partición. Como 3-PARTICIÓN restringido a números polinomiales es NP-completo, el
makespan restringido a números polinomiales es NP-duro. $\square$

Con $m = 2$ el problema es PARTICIÓN, que el capítulo 21, §5 citó como NP-completo. Pero
PARTICIÓN tiene tabla pseudopolinomial: se marca qué sumas entre 0 y $T/2$ se pueden
formar, en $O(nT)$. Con $m$ fijo, la tabla guarda las cargas de las $m - 1$ primeras
máquinas, y tiene $O(T^{m-1})$ entradas: pseudopolinomial para cada $m$ fijo, y
exponencial en $m$. El teorema 4 no dice cuál es el mejor exponente, pero sí que $m$ no
puede salir de él del todo: con $m$ libre no hay algoritmo pseudopolinomial, si P ≠ NP.

## 9. Un FPTAS resuelve exacto

Un FPTAS que se pide con un $\varepsilon$ lo bastante chico ya no aproxima: acierta.

**Teorema 5** (Garey y Johnson, 1978). Sea un problema de optimización cuyo objetivo
toma valores enteros, y supón que $\mathrm{OPT}(I) \le r(|I|, \mathrm{Max}(I))$ para
un polinomio $r$. Si el problema tiene un FPTAS, tiene un algoritmo exacto
pseudopolinomial.

*Demostración.* Lo hacemos para minimizar; maximizar es igual con $1 - \varepsilon$.
Dada $I$, llamamos al FPTAS con $\varepsilon = 1/(r(|I|, \mathrm{Max}(I)) + 1)$. Devuelve
una solución de costo
$$c \;\le\; (1 + \varepsilon)\,\mathrm{OPT} \;=\; \mathrm{OPT} +
\frac{\mathrm{OPT}}{r + 1} \;<\; \mathrm{OPT} + 1,$$
porque $\mathrm{OPT} \le r < r + 1$. Como $c$ y $\mathrm{OPT}$ son enteros y
$c \ge \mathrm{OPT}$, queda $c = \mathrm{OPT}$. El tiempo es polinomial en $|I|$ y en
$1/\varepsilon = r + 1$, que es polinomial en $|I|$ y $\mathrm{Max}(I)$. $\square$

Juntando los teoremas 3 y 5:

**Corolario 6.** Si P ≠ NP, ningún problema fuertemente NP-duro con objetivo entero
acotado por un polinomio en $|I|$ y $\mathrm{Max}(I)$ tiene FPTAS.

Los casos de la Parte III caen solos. El makespan con $m$ libre tiene
$\mathrm{OPT} \le \sum_i t_i \le n\,\mathrm{Max}(I)$, y el teorema 4 lo hace fuertemente
NP-duro: no tiene FPTAS. Vertex cover tiene $\mathrm{OPT} \le n$ y no tiene números: no
tiene FPTAS. TSP métrico tiene $\mathrm{OPT} \le n\,\mathrm{Max}(I)$ y es NP-duro con
distancias 1 y 2: no tiene FPTAS. Fíjate en que el corolario no dice nada sobre PTAS:
excluye solo la versión "totalmente" polinomial.

Con la mochila el teorema 5 corre al revés, y se puede ejecutar. Su óptimo cumple
$\mathrm{OPT} \le n\,v_{\max}$, así que el FPTAS con $\varepsilon = 1/(n\,v_{\max} + 1)$
tiene que dar el óptimo exacto. Con $\varepsilon = 1/2$, en cambio, no tiene por qué:

```{python continue}
rng = random.Random(9)
distintos = 0
for _ in range(300):
    n = rng.randint(1, 7)
    p = [rng.randint(1, 15) for _ in range(n)]
    v = [rng.randint(1, 15) for _ in range(n)]
    W = rng.randint(max(p), sum(p))
    opt = fuerza_bruta(p, v, W)
    assert fptas_mochila(p, v, W, Fraction(1, n * max(v) + 1))[0] == opt
    distintos += fptas_mochila(p, v, W, Fraction(1, 2))[0] != opt
print(f"300 instancias: con eps = 1/(n vmax + 1), siempre el óptimo; "
      f"con eps = 1/2, {distintos} veces otro valor")
```

Como algoritmo exacto es malo, $O(n^4 v_{\max})$, peor que la tabla de §2. El teorema
está para dar **imposibilidades**: sin algoritmo pseudopolinomial no hay FPTAS. La
segunda cuenta del bloque muestra que la primera comprueba algo: con
$\varepsilon = 1/2$ el mismo algoritmo se equivoca.

## 10. Balanceo con m fijo: un PTAS

El capítulo 21, §7 prometió algo que se acerque al óptimo tanto como se quiera cuando
$m$ es fijo. La razón $2 - 1/m$ del capítulo 21, §5 salía de
$L \le T/m + (1 - 1/m)\,t_j$, con $t_j$ la última tarea de la máquina más cargada. Si
esa tarea es **chica** comparada con el óptimo, la regla de Graham es casi óptima. Las
que estorban son las grandes, y no pueden ser muchas: las grandes, óptimas por fuerza
bruta; las chicas, con la regla de Graham.

El algoritmo, con $q = \lceil 1/\varepsilon \rceil$ y $k = \min(n,\, m(q - 1))$:

1. Ordena las tareas de mayor a menor. Las $k$ primeras son las **largas**.
2. Asigna las largas de forma óptima, probando las asignaciones posibles.
3. Asigna cada tarea corta, de mayor a menor, a la máquina menos cargada.

El oráculo para el paso 2 es la ramificación con poda del capítulo 21, §6, cambiada
para que devuelva también la asignación:

```{python echo=false}
# Cadena nueva: el balanceo de carga no usa nada de la mochila.
import math
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))
import figuras_23 as F23
```

```{python continue}
def carga_optima(t, m):
    """Makespan mínimo y una asignación que lo alcanza, por ramificación con poda."""
    orden = sorted(range(len(t)), key=lambda j: -t[j])
    mejor, mejor_asign = sum(t) + 1, None
    asign = [0] * len(t)
    def poner(k, carga):
        nonlocal mejor, mejor_asign
        if max(carga) >= mejor:
            return
        if k == len(orden):
            mejor, mejor_asign = max(carga), asign[:]
            return
        j = orden[k]
        for i in range(m):
            if carga[i] not in carga[:i]:      # máquinas con igual carga son iguales
                carga[i] += t[j]
                asign[j] = i
                poner(k + 1, carga)
                carga[i] -= t[j]
    poner(0, [0] * m)
    return mejor, mejor_asign

def ptas_carga(t, m, eps, k=None):
    if k is None:
        k = min(len(t), m * (math.ceil(1 / eps) - 1))
    orden = sorted(range(len(t)), key=lambda j: -t[j])
    largas, cortas = orden[:k], orden[k:]
    asign = [None] * len(t)
    carga = [0] * m
    if largas:
        _, a = carga_optima([t[j] for j in largas], m)
        for pos, j in enumerate(largas):
            asign[j] = a[pos]
            carga[a[pos]] += t[j]
    for j in cortas:                            # la regla de Graham
        i = min(range(m), key=lambda i: carga[i])
        carga[i] += t[j]
        asign[j] = i
    return max(carga), asign, largas

def comprobar(eps, k=None, veces=300, semilla=23):
    rng = random.Random(semilla)
    peor, violaciones = Fraction(1), 0
    for _ in range(veces):
        m = rng.randint(2, 3)
        t = [rng.randint(1, 30) for _ in range(rng.randint(m + 1, 10))]
        opt = carga_optima(t, m)[0]
        L = ptas_carga(t, m, eps, k)[0]
        violaciones += L > (1 + (1 - Fraction(1, m)) * eps) * opt
        peor = max(peor, Fraction(L, opt))
    return float(peor), violaciones

for eps in [Fraction(1), Fraction(1, 2), Fraction(1, 3)]:
    peor, malas = comprobar(eps)
    print(f"eps = {eps}: peor razón {peor:.3f}, violaciones de la cota {malas}")
peor, malas = comprobar(Fraction(1, 5), k=0)
print(f"eps = 1/5 con k = 0, sin largas: peor razón {peor:.3f}, violaciones {malas}")
```

La cota que se comprueba es $(1 + (1 - 1/m)\varepsilon)\,\mathrm{OPT}$, que es la que
demuestra la §11, un poco mejor que $1 + \varepsilon$. La última línea es la
comprobación de que la comprobación puede fallar: con $k = 0$ el algoritmo es LPT puro,
y la cota de $\varepsilon = 1/5$ le queda chica. Si no la violara nunca, el experimento
no estaría midiendo nada de lo que aportan las tareas largas.

¿Por qué $1/5$ y no $1/3$? Porque con $\varepsilon = 1/3$ la cota es
$1 + (1 - 1/m)/3 = 4/3 - 1/(3m)$, exactamente la garantía de LPT del capítulo 21, §7. El
esquema garantiza algo que LPT no garantiza solo cuando $\varepsilon < 1/3$.

```{python continue}
rng = random.Random(8)
t = [rng.randint(1, 20) for _ in range(11)]
L, asign, largas = ptas_carga(t, 3, Fraction(1, 2))
print(f"tareas {t}")
print(f"largas {[t[j] for j in largas]}, makespan {L}, óptimo {carga_optima(t, 3)[0]}")
```

```{python continue echo=false output=asis}
print(F23.ptas_carga(t, asign, largas, 3, pie=(
    f"El PTAS con m = 3 y ε = 1/2, así que q = 2 y k = 3·(2 − 1) = 3. Las tres tareas "
    f"largas (azul) se asignaron probando todas las formas; las otras ocho (naranja) entraron "
    f"de mayor a menor en la máquina menos cargada. Makespan {L}.")))
```

## 11. La demostración y el costo

**Teorema 7** (Graham, 1969). Con $m$ máquinas y $\varepsilon > 0$, `ptas_carga` da un
makespan $L \le (1 + (1 - 1/m)\,\varepsilon)\,\mathrm{OPT} \le (1+\varepsilon)\,
\mathrm{OPT}$.

*Demostración.* Sea $i$ la máquina con carga $L$ y $j$ la última tarea que recibió.
Hay dos casos, según $j$ sea larga o corta.

*$j$ es larga.* Entonces la máquina $i$ no recibió ninguna corta, porque las cortas se
asignan después de todas las largas y $j$ es su última. Su carga es la que tenía en la
asignación óptima de las largas, que es a lo sumo el makespan óptimo de las largas
solas. Y ese es a lo sumo $\mathrm{OPT}$, porque quitar tareas no empeora el óptimo.
Así que $L \le \mathrm{OPT}$.

*$j$ es corta.* Cuando llegó $j$, la máquina $i$ era la menos cargada y cargaba
$L - t_j$. El argumento del teorema 3 del capítulo 21 se aplica igual, porque solo usa
que todas las máquinas cargaban al menos eso y que las tareas ya repartidas suman a lo
sumo $T - t_j$:
$$L \le \frac{T}{m} + \Bigl(1 - \frac{1}{m}\Bigr) t_j \le \mathrm{OPT} +
\Bigl(1 - \frac{1}{m}\Bigr) t_j.$$
Falta acotar $t_j$. Como $j$ es corta, hubo $k$ tareas largas antes en el orden, y cada
una dura al menos $t_j$. Con $j$, son $k + 1 = m(q - 1) + 1$ tareas de duración al
menos $t_j$ (si $k = n$, no hay cortas y este caso no ocurre). En cualquier asignación,
por el principio del palomar, alguna máquina recibe al menos
$\lceil (m(q - 1) + 1)/m \rceil = q$ de ellas, así que $\mathrm{OPT} \ge q\,t_j$, y $t_j
\le \mathrm{OPT}/q \le
\varepsilon\,\mathrm{OPT}$, porque $q = \lceil 1/\varepsilon \rceil \ge 1/\varepsilon$.
Sustituyendo, $L \le (1 + (1 - 1/m)\,\varepsilon)\,\mathrm{OPT}$. $\square$

El paso que decide $k$ es ese palomar. Hace falta que las tareas al menos tan largas
como $t_j$ obliguen a alguna máquina del óptimo a cargar $q$ de ellas, y eso pide
$m(q - 1) + 1$ tareas: con $m(q - 1)$ caben $q - 1$ por máquina. Por eso
$k = m(q - 1)$ es el menor número de largas con el que la demostración funciona, y
cada tarea larga de más multiplica por $m$ la fuerza bruta. Con $\varepsilon = 1$ sale
$k = 0$, la regla de Graham sola, y la cota es $2 - 1/m$, la del capítulo 21.

El algoritmo y su análisis son de Ronald Graham, en el mismo artículo de LPT, "Bounds
on Multiprocessing Timing Anomalies" (*SIAM Journal on Applied Mathematics* 17(2),
1969, pp. 416–429). La atribución es la de Williamson y Shmoys (2011, notas del
capítulo 3).

Ahora el costo. Ordenar es $O(n \log n)$ y la regla de Graham sobre las cortas es
$O(nm)$. El paso 2 prueba, en el peor caso, todas las asignaciones de $k$ tareas a $m$
máquinas, que son $m^k$, y cada una se evalúa en $O(k)$. En total
$O(n \log n + nm + k\,m^k)$ con $k = m(\lceil 1/\varepsilon \rceil - 1) <
m/\varepsilon$. Para $m$ y $\varepsilon$ fijos,
$m^k$ es una constante, y el tiempo es $O(n \log n)$: es un PTAS. Pero la constante:

```{python continue}
for m in [2, 3, 5]:
    fila = []
    for q in [2, 4, 10]:
        k = m * (q - 1)
        fila.append(f"eps = 1/{q}: k = {k}, m^k = {float(m ** k):.2g}")
    print(f"m = {m}:  " + ";  ".join(fila))
```

Con tres máquinas y $\varepsilon = 1/10$ son $7{,}6 \cdot 10^{12}$ asignaciones, y la
cota crece exponencialmente en $1/\varepsilon$: es un PTAS y no un FPTAS. Con $m$ fijo
el problema sí tiene FPTAS, redondeando como en §3 la tabla de cargas de §8
(ejercicio 6); Sartaj Sahni aplicó esa técnica a este problema en "Algorithms for
Scheduling Independent Tasks" (*Journal of the ACM* 23(1), 1976, pp. 116–127). Con $m$
libre hay PTAS: Dorit Hochbaum y David Shmoys dieron uno de tiempo
$O((n/\varepsilon)^{1/\varepsilon^2})$ en "Using Dual Approximation Algorithms for
Scheduling Problems: Theoretical and Practical Results" (*Journal of the ACM* 34(1),
1987, pp. 144–162). Que no sea polinomial en $1/\varepsilon$ lo obliga el corolario 6.

## 12. El mapa de la Parte III

Con este capítulo se cierra la Parte III, y se puede dibujar lo que se sabe de cada
problema de optimización que vimos. Las garantías se ordenan de la más fuerte a la más
débil: exacto en tiempo polinomial, FPTAS, PTAS, razón constante, razón que crece con
$n$, ninguna razón. Para cada problema marcamos la mejor que el libro demuestra o cita,
y tachamos las que son imposibles si P ≠ NP.

```{python continue}
clases = ["exacto", "FPTAS", "PTAS", "razón cte.", "razón ~ ln n", "ninguna"]
EXACTO, FPTAS, PTAS, CTE, CRECE, NINGUNA = range(6)
# (problema, mejor garantía, primera clase posible si P != NP, de dónde sale)
mapa = [
    ("Mochila", FPTAS, FPTAS, "cap. 19, §11; §4–5"),
    ("Makespan, m fijo", FPTAS, FPTAS, "cap. 21, §5; ej. 6"),
    ("Makespan, m libre", PTAS, PTAS, "§8–9; Hochbaum y Shmoys"),
    ("Empaquetamiento en cajas", CTE, CTE, "cap. 21, ej. 4; ej. 5"),
    ("k-center métrico", CTE, CTE, "cap. 21, §8–9"),
    ("MAX-3SAT", CTE, CTE, "cap. 21, §12"),
    ("Vertex cover", CTE, CTE, "cap. 21, §3; Dinur y Safra"),
    ("TSP métrico", CTE, CTE, "cap. 22, §7–9"),
    ("Set cover", CRECE, CRECE, "cap. 21, §10–11"),
    ("TSP general", NINGUNA, NINGUNA, "cap. 22, §2; §12"),
]
justos = [nombre for nombre, logrado, posible, _ in mapa if logrado == posible]
print(f"{len(justos)} de {len(mapa)} problemas con la mejor clase posible si P != NP")
```

```{python continue echo=false output=asis}
print(F23.mapa(clases, mapa, pie=(
    "La Parte III en una tabla. El punto es la mejor garantía que el libro demuestra o "
    "cita; las × son garantías imposibles si P ≠ NP. A la derecha, de dónde sale cada "
    "marca.")))
```

La @fig-esq-mapa se lee por filas, y en las diez el punto toca la primera casilla sin
tachar: por clases, lo que el libro da es lo mejor posible si P ≠ NP. Tres filas
merecen una palabra.

- **Vertex cover y TSP métrico.** El corolario 6 solo excluye el FPTAS; el PTAS lo
  excluyen la cota de $123/122$ para TSP métrico del capítulo 22, §9, y, para vertex
  cover, Irit Dinur y Samuel Safra, que demostraron que aproximar con razón menor que $1{,}3606$ es NP-duro ("On the
  hardness of approximating vertex cover", *Annals of Mathematics* 162(1), 2005,
  pp. 439–485).
- **TSP general.** El teorema 1 del capítulo 22 está escrito para una constante
  $\alpha$, pero la demostración funciona igual con una razón $\alpha(n)$ que se
  calcule en tiempo polinomial, como $\ln n$, con el costo
  $c = \lceil (\alpha(n) - 1)n \rceil + 2$, que se escribe con pocos bits y cumple
  $(n - 1) + c > \alpha(n)\,n$, lo único que usa la demostración. Así que
  tampoco hay razón que crezca con $n$.

Que la clase sea justa no quiere decir que la razón lo sea. Vertex cover tiene razón
2, y la imposibilidad ya no está en $1{,}3606$: aproximarlo con razón $\sqrt 2 - \varepsilon$
es NP-duro. Subhash Khot, Dor Minzer y Muli Safra lo dejaron condicionado a una
hipótesis sobre los grafos de Grassmann ("On Independent Sets, 2-to-2 Games and
Grassmann Graphs", ECCC TR16-124, 2016) y la demostraron en "Pseudorandom sets in
Grassmann graph have near-perfect expansion" (*Annals of Mathematics* 198(1), 2023,
pp. 1–92). Entre $\sqrt 2$ y 2 no se sabe. TSP métrico tiene casi $3/2$, y la
imposibilidad publicada empieza en $123/122$.

## 13. La regla {#esquemas-13-la-regla}

Un esquema de aproximación cambia precisión por tiempo, y la pregunta es dónde se paga
$\varepsilon$. La respuesta la deciden los números:

- Un FPTAS da un algoritmo exacto pseudopolinomial (teorema 5). Si el problema es
  difícil **también** con números chicos (fuertemente NP-duro), ese algoritmo no existe
  y no hay FPTAS si P ≠ NP. Lo más que puede haber es un PTAS, que paga $\varepsilon$ en
  el exponente. El makespan con $m$ libre es el ejemplo.
- El recíproco no vale en general: tener una tabla pseudopolinomial no basta. Hace
  falta una tabla que se deje redondear, es decir, donde el error del redondeo se pueda
  acotar contra el óptimo. Para la mochila, con el paso $\varepsilon\,v_{\max}/n$ y la
  cota $v_{\max} \le \mathrm{OPT}$, la tabla redondeada da un FPTAS.

Y cuando un esquema existe, su demostración compara, como en el capítulo 21, contra
una cota del óptimo que se puede calcular: $\mathrm{OPT} \ge v_{\max}$ en la mochila,
y $\mathrm{OPT} \ge q\,t_j$ en el makespan, que dan las $m(q - 1) + 1$ tareas más
largas.

## Resumen {#esquemas-resumen}

- Un PTAS da $1 \pm \varepsilon$ en tiempo polinomial en $n$ para cada $\varepsilon$
  fijo; un FPTAS, en tiempo polinomial en $n$ y $1/\varepsilon$ a la vez.
  $O(n^{1/\varepsilon})$ es PTAS y no FPTAS.
- La tabla por valores resuelve la mochila exacta en $O(n\sum v_i)$, pseudopolinomial
  en los valores.
- El FPTAS redondea $v'_i = \lfloor v_i/\mu \rfloor$ con $\mu = \varepsilon v_{\max}/n$
  y resuelve exacto con $v'$. Cada objeto pierde menos de $\mu$, el óptimo tiene a lo
  sumo $n$ objetos, y $v_{\max} \le \mathrm{OPT}$: razón $1 - \varepsilon$.
- El tiempo es $O(n^3/\varepsilon)$, porque cada $v'_i \le \lfloor n/\varepsilon
  \rfloor$, y no depende de $v_{\max}$.
- $v_{\max} \le \mathrm{OPT}$ solo vale si se descartan los objetos que no caben. Sin
  ese filtro, la razón puede ser 0, y las pruebas donde todo cabe no lo ven.
- Fuertemente NP-duro: NP-duro aun con números polinomiales en el tamaño. Entonces no
  hay algoritmo pseudopolinomial si P ≠ NP.
- 3-PARTICIÓN es fuertemente NP-completo, y por eso también el makespan con $m$ libre.
- Un FPTAS con $\varepsilon = 1/(r+1)$ resuelve exacto si el objetivo es entero y
  $\mathrm{OPT} \le r$. Problema fuertemente NP-duro con objetivo acotado: sin FPTAS.
- Makespan con $m$ fijo: las $m(q - 1)$ tareas largas óptimas y el resto con Graham da
  $1 + (1 - 1/m)\varepsilon$, en tiempo $O(n \log n + k\,m^k)$. Este algoritmo es un
  PTAS y no un FPTAS; el problema con $m$ fijo sí tiene FPTAS (ejercicio 6).

## Ejercicios {#esquemas-ejercicios}

1. Ejecuta a mano `fptas_mochila` con $\varepsilon = 1/2$ sobre cinco objetos de pesos
   $7, 1, 8, 4, 4$, valores $46, 50, 54, 48, 9$ y capacidad $W = 10$. Calcula $\mu$ y
   los valores redondeados, llena la tabla por valores y di qué conjunto devuelve.
   Encuentra el óptimo y compara la razón obtenida con $1 - \varepsilon$. ¿Cuál de los
   pasos de la demostración del teorema 1 es el que más pierde en esta entrada?

2. En la versión de optimización de suma de subconjuntos se dan enteros positivos
   $a_1, \dots, a_n$ y una meta $T$, y se busca el subconjunto de mayor suma que no pase
   de $T$. El algoritmo exacto mantiene la lista ordenada de las sumas posibles que no
   pasan de $T$. Modifícalo para que, después de cada número, **recorte** la lista: con $\delta = \varepsilon/(2n)$, borra cada suma
   $y$ para la que quedó otra $z$ con $y/(1 + \delta) \le z < y$. Demuestra que la
   lista recortada tiene una longitud polinomial en $n$, $1/\varepsilon$ y
   $\log T$, y que el resultado es al menos $(1 - \varepsilon)$ veces el óptimo.
   Impleméntalo y compáralo con `fptas_mochila` usando $p_i = v_i = a_i$.

3. Mejora el tiempo del FPTAS a $O(n^2/\varepsilon)$. Sea $G$ el valor que se obtiene
   metiendo los objetos que caben por orden decreciente de $v_i/p_i$ hasta el primero
   que no entra, y $L = \max(G, v_{\max})$. Usando la cota de la mochila fraccionaria
   del capítulo 20, §3, demuestra que $L \le \mathrm{OPT} \le 2L$. Después redondea con
   $\mu = \varepsilon L/n$ y demuestra la razón $1 - \varepsilon$ y el tiempo. Pista para
   el tiempo: ¿hasta qué valor redondeado hace falta llenar la tabla? ¿Por qué hace
   falta el $v_{\max}$ dentro del máximo?

4. Usa el corolario 6 para demostrar que, si P ≠ NP, ni el clique máximo ni la
   coloración con el menor número de colores tienen FPTAS. Después demuestra algo más
   fuerte para la coloración, usando que 3-coloración es NP-completa (capítulo 18): si
   P ≠ NP, no hay algoritmo polinomial de razón menor que $4/3$, y por tanto tampoco
   PTAS.

5. En **empaquetamiento en cajas** hay objetos de tamaños enteros $s_1, \dots, s_n$ y
   cajas de capacidad $C$, y se busca usar el menor número de cajas. (a) Demuestra que es
   fuertemente NP-duro con una reducción desde 3-PARTICIÓN. (b) La regla **Next Fit**
   mete cada objeto en la caja abierta si cabe, y si no, cierra esa caja y abre otra.
   Demuestra que usa a lo sumo $2\,\mathrm{OPT}$ cajas. (c) Con el ejercicio 4 del
   capítulo 21, explica la fila de empaquetamiento de la @fig-esq-mapa: qué casillas
   están tachadas y por qué.

6. ★ Construye un FPTAS para el makespan con $m$ fijo. Primero escribe una tabla exacta
   que, tarea por tarea, guarde el conjunto de vectores de cargas alcanzables, y acota
   su tamaño en función de $n$, $m$ y $T = \sum t_j$. Después redondea las duraciones
   con un paso proporcional a $\varepsilon\,T/(mn)$, y demuestra que el makespan real de
   la asignación que sale es a lo sumo $(1 + \varepsilon)\,\mathrm{OPT}$. Cuenta el
   tiempo como un polinomio en $n$ y $1/\varepsilon$ cuyo grado depende de $m$. ¿Es eso
   compatible con el teorema 4?

7. Una versión "más rápida" del FPTAS usa el paso $\mu = \varepsilon\, v_{\max}$, sin
   dividir por $n$. Calcula su tiempo. Después construye, para $\varepsilon = 1/2$, una
   entrada donde todos los objetos caben y la versión rápida devuelve menos de
   $(1 - \varepsilon)\,\mathrm{OPT}$. ¿Qué paso de la demostración del teorema 1 deja de
   valer, y cuánto puede llegar a perder en función de $n$?

8. k-center, del capítulo 21, §8, tiene razón 2, y el makespan tiene un PTAS cuando se
   fija $m$. (a) Demuestra que k-center métrico, con $k$ parte de la entrada, no tiene
   PTAS si P ≠ NP. (b) Ahora fija $k$. Da un algoritmo **exacto** polinomial para cada
   $k$ fijo, y di su tiempo. (c) ¿Por qué fijar $m$ en el makespan no da un algoritmo
   exacto polinomial, si P ≠ NP? ¿Qué diferencia entre los dos problemas lo explica?

9. Mide la calidad de `fptas_mochila` contra `fuerza_bruta` para
   $\varepsilon \in \{1/2, 1/4, 1/8\}$ en instancias de 6 a 12 objetos, con valores al
   azar y con valores casi iguales. Después busca, con búsqueda local sobre pesos y
   valores, entradas de 6 objetos que minimicen la razón para $\varepsilon = 1/2$. ¿Qué
   tan cerca de $1 - \varepsilon$ llegas? Explica, mirando la demostración del teorema
   1, qué tendría que pasar a la vez para alcanzarla.

10. Una empresa evalúa 80 proyectos, cada uno con un costo en pesos de hasta $10^9$ y
    un beneficio estimado, con un presupuesto fijo. (a) Modela la elección y compara la
    tabla por capacidad, la tabla por valores y el FPTAS. ¿Cuál usarías si los
    beneficios se estiman con un error de un 5 %, y con qué $\varepsilon$? (b) La misma
    empresa tiene 30 camiones idénticos y 90 contenedores; cada uno ocupa más de un
    cuarto y menos de la mitad de un camión, entre todos llenan exactamente los 30, y
    cada camión tiene que salir lleno. Di qué problema es y qué puedes esperar de un
    algoritmo polinomial.
