# Algoritmos de aproximación {#chap-aproximacion}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_21.py
import figuras_21 as F21
```

Los capítulos 16 a 19 demostraron que vertex cover, set cover, 3-SAT y una docena de
problemas más son NP-completos, y el capítulo 20 los resolvió exactos pagando tiempo
exponencial. Este capítulo cambia el trato: tiempo polinomial, y a cambio una solución
que puede no ser óptima pero que, en **toda** entrada, cuesta a lo sumo un factor fijo
del óptimo. El obstáculo es evidente: para comparar contra el óptimo hay que conocerlo,
y el óptimo es justo lo que no sabemos calcular. Todo el capítulo resuelve ese obstáculo
con una sola idea, que se repite cinco veces con cinco disfraces: encontrar una **cota
del óptimo que sí se puede calcular**, y comparar contra ella.

## 1. Rendirse con garantía

Un problema de optimización asigna a cada solución factible de una entrada $I$ un costo,
que se quiere mínimo, o un valor, que se quiere máximo. Llamamos $\mathrm{OPT}(I)$ al
mejor. El capítulo 16, §2 estudió la versión de decisión; aquí volvemos a la de
optimización, porque lo que se aproxima es un número.

**Definición.** Un algoritmo $A$ es una **$\alpha$-aproximación** de un problema de
minimización si corre en tiempo polinomial en el tamaño de la entrada y, para toda
entrada $I$, devuelve una solución factible con
$$c(A(I)) \le \alpha \cdot \mathrm{OPT}(I), \qquad \alpha \ge 1.$$
Para maximización, $v(A(I)) \ge \alpha \cdot \mathrm{OPT}(I)$ con $\alpha \le 1$. El
número $\alpha$ se llama la **razón de aproximación**, y puede depender del tamaño de
la entrada, como el $H_n$ de §11.

Fíjate en el "para toda entrada". Una heurística que en las pruebas da el 101 % del
óptimo no es una aproximación de razón 1,01 hasta que alguien lo demuestra, y §4 muestra
una que gana en casi todas las pruebas al azar y no tiene la razón que parece.

¿Cómo se demuestra $c(A(I)) \le \alpha\,\mathrm{OPT}(I)$ sin conocer
$\mathrm{OPT}(I)$? Con un número intermedio $B(I)$ que cumple dos cosas:
$$B(I) \le \mathrm{OPT}(I) \qquad\text{y}\qquad c(A(I)) \le \alpha \cdot B(I).$$
La primera se demuestra sobre **cualquier** solución, incluida la óptima que no
conocemos. La segunda se demuestra sobre la solución que el algoritmo construyó, que sí
conocemos. Es el mismo movimiento de la cota mínima del capítulo 5, ahora dentro de
una sola entrada: allí se acotaba lo que cuesta todo algoritmo, aquí lo que cuesta toda
solución. Para maximizar, $B(I) \ge \mathrm{OPT}(I)$. Casi todo el trabajo está en
elegir $B$, y la razón que sale depende de lo ajustada que sea.

## 2. Vertex cover: una cota del óptimo

Un **vertex cover** de un grafo $G = (V, E)$ es un conjunto $C \subseteq V$ que toca
todas las aristas: para cada $\{u, v\} \in E$, $u \in C$ o $v \in C$. Encontrar uno
mínimo es NP-duro: el capítulo 16, §10 lo liga a conjunto independiente, y el capítulo 18 lo demuestra NP-completo. ¿Qué número, fácil de calcular, es siempre menor o
igual que el mínimo?

Mira un grafo cualquiera y elige aristas que **no compartan extremos**, un
**emparejamiento** $M$. Cada arista de $M$ tiene que quedar tocada por el cubrimiento,
así que el cubrimiento contiene al menos uno de sus dos extremos. Como las aristas de
$M$ no comparten extremos, esos vértices son distintos.

**Lema 1.** Si $M$ es un emparejamiento de $G$ y $C$ es un vertex cover de $G$,
entonces $|C| \ge |M|$.

*Demostración.* La función que a cada arista de $M$ le asigna un extremo que está en
$C$ (existe porque $C$ cubre) es inyectiva: dos aristas distintas de $M$ no comparten
extremos, así que no pueden recibir el mismo vértice. Una función inyectiva de $M$ en
$C$ da $|M| \le |C|$. $\square$

El paso que todo el mundo se salta es el de la inyectividad, y es el único que usa que
$M$ sea un emparejamiento. Guárdalo, porque §4 lo rompe.

## 3. Emparejamiento maximal: razón 2

La cota del lema 1 sugiere el algoritmo. Recorre las aristas; cada vez que encuentres
una que nadie toca todavía, mete **los dos** extremos en el cubrimiento. Meter uno solo
parecería más económico, pero no sabemos cuál de los dos usa el óptimo. Metiendo los
dos pagamos a lo sumo el doble de lo que paga el óptimo en esa arista.

```{python continue}
def cubrimiento_emparejamiento(aristas):
    C, M = set(), []
    for u, v in aristas:
        if u not in C and v not in C:   # arista descubierta
            C |= {u, v}
            M.append((u, v))
    return C, M

def es_cubrimiento(C, aristas):
    return all(u in C or v in C for u, v in aristas)

def cubrimiento_optimo(n, aristas):          # el oráculo: fuerza bruta
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            if es_cubrimiento(set(S), aristas):
                return k

def grafo_al_azar(n, p, rng):
    aristas = [(u, v) for u in range(n) for v in range(u + 1, n)
               if rng.random() < p]
    rng.shuffle(aristas)
    return aristas

aristas = grafo_al_azar(8, 0.3, random.Random(4))
C, M = cubrimiento_emparejamiento(aristas)
print(f"{len(aristas)} aristas, emparejamiento {len(M)}, cubrimiento {len(C)}, "
      f"óptimo {cubrimiento_optimo(8, aristas)}")
```

```{python continue echo=false output=asis}
print(F21.emparejamiento(8, aristas, M, C, pie=(
    "El algoritmo sobre el grafo de 8 vértices de la semilla 4. Las tres aristas "
    "gruesas son las que encontró descubiertas, y no comparten extremos: el óptimo "
    "necesita al menos 3 vértices. El algoritmo toma sus 6 extremos. El óptimo "
    "real, por fuerza bruta, es 4.")))
```

La @fig-aprox-emparejamiento muestra los tres números a la vez: la cota $|M| = 3$, el
óptimo 4 y la solución 6. La razón en esta entrada es $6/4 = 1{,}5$. La garantía que
vamos a demostrar no compara la solución con el óptimo, que no conocemos, sino con la
cota: $6 = 2 \cdot 3$.

**Teorema 2.** `cubrimiento_emparejamiento` devuelve un vertex cover $C$ con
$|C| \le 2\,\mathrm{OPT}$, en tiempo $O(|V| + |E|)$.

*Demostración.* Es un cubrimiento: cuando el recorrido pasa por una arista, o ya estaba
tocada o el algoritmo mete sus dos extremos; después de eso sigue tocada, porque $C$
solo crece. Las aristas de $M$ forman un emparejamiento: cada una se agregó cuando sus
dos extremos estaban fuera de $C$, así que no comparte extremos con ninguna agregada
antes, y la propia agregación mete sus dos extremos en $C$, lo que impide que una
posterior los use. Entonces $|C| = 2|M| \le 2\,\mathrm{OPT}$ por el lema 1. Con $C$
guardado como arreglo de booleanos, cada arista cuesta $O(1)$. $\square$

$M$ es además **maximal**: no se le puede agregar ninguna arista, porque toda arista
quedó tocada. El teorema no lo usa, pero es lo que le da nombre al algoritmo.

Ahora el experimento contra el oráculo, en grafos al azar de hasta 9 vértices:

```{python continue}
def bateria(algoritmo, semilla=21, veces=1500):
    rng = random.Random(semilla)
    razones = []
    for _ in range(veces):
        n = rng.randint(2, 9)
        aristas = grafo_al_azar(n, rng.choice([0.2, 0.3, 0.5, 0.7]), rng)
        if not aristas:
            continue
        C = algoritmo(aristas)
        assert es_cubrimiento(C, aristas)
        razones.append(len(C) / cubrimiento_optimo(n, aristas))
    return razones

razones = bateria(lambda a: cubrimiento_emparejamiento(a)[0])
print(f"{len(razones)} grafos, peor razón {max(razones):.2f}, "
      f"promedio {sum(razones) / len(razones):.3f}, "
      f"razón 2 en {sum(r == 2 for r in razones)}")
```

La razón 2 no es una cota holgada: se alcanza en más de la mitad de los grafos
chicos, porque en un grafo de pocas aristas el emparejamiento y el óptimo coinciden a
menudo. El ejercicio 2 pide la familia de grafos en la que se alcanza siempre, para
cualquier orden de las aristas.

## 4. El error plantado: un extremo por arista

El teorema 2 paga los dos extremos de cada arista descubierta, y eso parece un
desperdicio. Una mejora natural: tomar uno solo, el que toca más aristas que todavía
faltan por cubrir. Sigue siendo un cubrimiento por el mismo argumento de antes.

```{python continue}
def un_extremo(aristas):
    C = set()
    for u, v in aristas:
        if u not in C and v not in C:
            grado = lambda x: sum(1 for a, b in aristas
                                  if x in (a, b) and a not in C and b not in C)
            C.add(u if grado(u) >= grado(v) else v)
    return C

malas = bateria(un_extremo)
print(f"{len(malas)} grafos, peor razón {max(malas):.2f}, "
      f"promedio {sum(malas) / len(malas):.3f}, "
      f"más de 2 en {sum(r > 2 for r in malas)}")
```

Sobre las mismas 1 309 entradas, la variante es mucho mejor: su razón promedio es 1,014, contra
1,692 de la versión correcta, y no pasa de 2 en ninguna.
Ninguna batería de grafos al azar como esta va a señalarla.

La demostración del teorema 2 sí la señala. Con un extremo por arista ya no se puede
decir "las aristas que dispararon una elección no comparten extremos": dos de ellas
pueden compartir justo el extremo que **no** se tomó. Sin eso, el lema 1 no se aplica y
no hay cota del óptimo contra la cual comparar. Donde falla la demostración está la
entrada que rompe el algoritmo: muchas aristas que comparten el extremo que la regla
deja fuera.

Construyámosla. A la izquierda, $k$ vértices $0, \dots, k - 1$. Para cada $i$ de $k$
hasta 2, agregamos a la derecha $\lfloor k / i \rfloor$ vértices nuevos, cada uno unido
a $i$ vértices consecutivos y distintos de la izquierda. Los $k$ de la izquierda son un
cubrimiento, así que $\mathrm{OPT} \le k$. Ordenamos las aristas para que lleguen
primero las de los vértices derechos de más grado:

```{python continue}
def instancia_mala(k):
    aristas, siguiente = [], k
    for i in range(k, 1, -1):              # primero los de grado mayor
        for j in range(k // i):
            for a in range(j * i, j * i + i):
                aristas.append((siguiente, a))
            siguiente += 1
    return siguiente, aristas

for k in (6, 12, 24, 48, 96):
    n, aristas_k = instancia_mala(k)
    C = un_extremo(aristas_k)
    print(f"k = {k:3d}: {n:4d} vértices, un extremo toma {len(C):4d}, "
          f"la izquierda cubre con {k:3d}, razón ≥ {len(C) / k:.2f}")
```

Un vértice de la izquierda nunca tiene más aristas pendientes que el derecho con el que
se compara, así que la regla toma siempre el derecho, y termina tomando casi todos.
Con $k = 24$ ya paga 60 vértices donde bastan 24: la razón es al menos 2,50, y la
garantía de 2 que parecía heredada del teorema 2 es falsa. Con $k = 96$ va por 3,78 y
sigue subiendo con $k$.

La moraleja es la del capítulo 3, §5, aplicada a la calidad en lugar de a la
correctitud: la variante devuelve siempre un cubrimiento, pasa todas las pruebas de
correctitud y gana en promedio, y aun así no tiene garantía. Una razón de aproximación
es una afirmación sobre el peor caso, y solo una demostración la sostiene.

## 5. Balanceo de carga: la regla de Graham

Tenemos $m$ máquinas idénticas y $n$ tareas con duraciones $t_1, \dots, t_n$ enteras y
positivas. Una asignación reparte las tareas entre las máquinas; la **carga** de una
máquina es la suma de las duraciones que recibió, y el **makespan** es la mayor carga.
Queremos el makespan mínimo. Con $m = 2$, decidir si el makespan puede ser $T/2$ es
PARTICIÓN, que uno de los ejercicios del capítulo 19 demuestra NP-completo.

Dos cotas del óptimo salen sin pensar mucho:
$$\mathrm{OPT} \ge \max_j t_j, \qquad \mathrm{OPT} \ge \frac{1}{m} \sum_j t_j.$$
La primera, porque la tarea más larga va entera en alguna máquina. La segunda, porque
las $m$ cargas suman $T = \sum_j t_j$, y la mayor de $m$ números es al menos su
promedio.

La regla de Graham es lo primero que uno haría con las tareas en la mano: cada tarea,
en el orden en que llega, a la máquina que en ese momento está menos cargada.

```{python echo=false}
# Cadena nueva: los bloques de carga no re-ejecutan los de vertex cover.
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))
import figuras_21 as F21
```

```{python continue}
def graham(t, m):
    carga, asign = [0] * m, []
    for x in t:
        i = min(range(m), key=lambda i: carga[i])   # la menos cargada
        carga[i] += x
        asign.append(i)
    return max(carga), asign

t = [2, 3, 2, 4, 1, 3, 2, 6]
L, asign = graham(t, 3)
print(f"makespan {L}, máquinas {[a + 1 for a in asign]}, "
      f"promedio {sum(t) / 3:.2f}, mayor tarea {max(t)}")
```

```{python continue echo=false output=asis}
print(F21.graham(t, asign, 3, ultima=len(t) - 1, pie=(
    "La regla de Graham sobre ocho tareas y tres máquinas. La última tarea, de "
    "duración 6, llega cuando la menos cargada lleva 5 y la deja en 11. Las dos "
    "cotas del óptimo, el promedio 23/3 y la mayor tarea 6, quedan a la izquierda.")))
```

La @fig-aprox-graham tiene la demostración entera dibujada. La máquina que termina
última es $M_3$, y su última tarea es $t_8 = 6$. Antes de $t_8$, $M_3$ cargaba 5, y era
la menos cargada; por eso la carga anterior no puede pasar del promedio. Lo que se pasa
del promedio es, como mucho, una tarea, y una tarea no pasa del óptimo.

**Teorema 3** (Graham, 1966). La regla de la máquina menos cargada da un makespan
$L \le (2 - 1/m)\,\mathrm{OPT}$.

*Demostración.* Sea $i$ la máquina con carga $L$ y $j$ la última tarea que recibió.
Cuando llegó $j$, la máquina $i$ cargaba $L - t_j$ y era la menos cargada, así que
cada una de las $m$ máquinas cargaba al menos $L - t_j$ en ese momento. En ese momento
las máquinas tienen repartidas las tareas anteriores a $j$, que suman a lo sumo
$T - t_j$. Sumando las $m$ cargas,
$$m(L - t_j) \le T - t_j, \qquad\text{así que}\qquad
L \le \frac{T}{m} + \Bigl(1 - \frac{1}{m}\Bigr) t_j.$$
Con las dos cotas del óptimo, $T/m \le \mathrm{OPT}$ y $t_j \le \mathrm{OPT}$, queda
$L \le (2 - 1/m)\,\mathrm{OPT}$. $\square$

El paso que se salta casi todo el mundo es escribir $T - t_j$ y no $T$: con $T$ sale la
razón 2, que es cierta pero más floja, y el $-1/m$ desaparece. El $-1/m$ no es un
adorno: el ejercicio 2 pide una entrada donde se alcanza exactamente $2 - 1/m$.

En la figura, $L = 11$, $T/m = 23/3$ y $t_j = 6$, y en efecto
$11 \le 23/3 + (2/3) \cdot 6 = 11{,}67$. El óptimo de esa entrada es 8, así que la
razón real es $11/8$. El artículo es "Bounds for Certain Multiprocessing Anomalies"
(*Bell System Technical Journal* 45(9), 1966, pp. 1563–1581), de Ronald Graham.

## 6. LPT: las grandes primero

La demostración del teorema 3 dice qué hay que arreglar: la razón se va por la última
tarea, que puede ser la más grande de todas. Si la última fuera pequeña, el exceso sobre
el promedio sería pequeño. Eso lleva a ordenar las tareas de mayor a menor antes de
aplicar la regla. Es la regla **LPT** (*longest processing time first*).

```{python continue}
def lpt(t, m):
    return graham(sorted(t, reverse=True), m)
```

Un primer argumento ya mejora la razón a $3/2$. Sea otra vez $i$ la máquina con carga
$L$ y $j$ su última tarea, con las tareas numeradas en el orden decreciente
$t_1 \ge t_2 \ge \dots$. Si $j \le m$, la tarea $j$ entró en una máquina vacía (las
primeras $m$ tareas van cada una a una máquina distinta, porque una máquina vacía carga
0 y las demás no) y $L = t_j \le \mathrm{OPT}$. Si $j > m$, las tareas
$1, \dots, m + 1$ duran todas al menos $t_j$, y en cualquier asignación dos de esas
$m + 1$ comparten máquina, así que $\mathrm{OPT} \ge 2 t_j$. Con la desigualdad de la
demostración del teorema 3, $L \le T/m + t_j \le \mathrm{OPT} + \mathrm{OPT}/2$.

El experimento sugiere que $3/2$ tampoco es la verdad. El oráculo es una ramificación
con poda, como la del capítulo 20, que no prueba dos máquinas con la misma carga:

```{python continue}
def carga_optima(t, m):
    mejor = sum(t)
    t = sorted(t, reverse=True)
    def poner(j, carga):
        nonlocal mejor
        if max(carga) >= mejor:
            return                            # esta rama ya no mejora
        if j == len(t):
            mejor = max(carga)
            return
        for i in range(m):
            if carga[i] not in carga[:i]:     # máquinas con igual carga son iguales
                carga[i] += t[j]
                poner(j + 1, carga)
                carga[i] -= t[j]
    poner(0, [0] * m)
    return mejor

rng = random.Random(21)
peor_g, peor_l = {}, {}
for _ in range(2000):
    m = rng.randint(2, 4)
    t = [rng.randint(1, 20) for _ in range(rng.randint(m + 1, 9))]
    opt = carga_optima(t, m)
    g, l = graham(t, m)[0], lpt(t, m)[0]
    assert g <= (2 - Fraction(1, m)) * opt
    peor_g[m] = max(peor_g.get(m, 0), Fraction(g, opt))
    peor_l[m] = max(peor_l.get(m, 0), Fraction(l, opt))
for m in sorted(peor_g):
    print(f"m = {m}: Graham peor {float(peor_g[m]):.3f} (cota {2 - 1/m:.3f}), "
          f"LPT peor {float(peor_l[m]):.3f} (cota 3/2)")
```

En 2 000 entradas al azar, LPT nunca pasa de 1,133, lejos de 1,5. El experimento
propone una cota cercana a $4/3$; la sección siguiente la demuestra.

## 7. LPT: la razón 4/3

**Teorema 4** (Graham, 1969). LPT da un makespan $L \le (4/3 - 1/(3m))\,\mathrm{OPT}$.

La idea: la cuenta del teorema 3 funciona bien cuando la última tarea es pequeña, menor
que $\mathrm{OPT}/3$. Si es grande, todas las anteriores también lo son, porque vienen
ordenadas, y en una entrada donde todas las tareas pasan de $\mathrm{OPT}/3$ cada
máquina del óptimo tiene a lo sumo dos. Hay que demostrar que en ese caso LPT no se
equivoca nunca.

**Lema 5.** Sean $t_1 \ge \dots \ge t_k$ las primeras $k$ tareas de LPT, y $C^*$ el
makespan óptimo de esas $k$ tareas solas. Si $t_k > C^*/3$, la máquina que recibe la
tarea $k$ queda con carga a lo sumo $C^*$.

*Demostración.* Si $k \le m$, la tarea $k$ entra en una máquina vacía, y $t_k \le C^*$.
Supón $k > m$, y llama **grandes** a las tareas $j < k$ con $t_j + t_k > C^*$. Como las
tareas están ordenadas, las grandes son $1, \dots, b$ para algún $b$.

Mira una asignación óptima de las $k$ tareas. Ninguna máquina tiene tres, porque
$3 t_k > C^*$. Una tarea grande no comparte máquina con nadie: cualquier otra dura al
menos $t_k$, y juntas pasarían de $C^*$. Entonces las $b$ grandes ocupan $b$ máquinas
para ellas solas, y las otras $k - b$ tareas (la $k$ incluida) caben de a dos en las
$m - b$ restantes:
$$k - b \le 2(m - b). \tag{$*$}$$
Como $k - b \ge 1$, también $m - b \ge 1$.

Ahora mira LPT justo antes de la tarea $k$. Las tareas $1, \dots, m$ fueron cada una a
una máquina vacía distinta, así que las $b$ grandes están en $b$ máquinas distintas, y
cada una de las otras $m - b$ máquinas empezó con una tarea $j$ que no es grande. Si
alguna de esas $m - b$ máquinas sigue con esa sola tarea, su carga es
$t_j \le C^* - t_k$; la máquina que LPT elige carga a lo sumo eso, y queda con a lo
sumo $C^*$. Si no, cada una de las $m - b$ tiene al menos dos tareas, ninguna grande, y
entre las tareas $1, \dots, k - 1$ hay al menos $2(m - b)$ que no son grandes. Pero son
$k - 1 - b$, y por $(*)$, $k - 1 - b < 2(m - b)$. Contradicción. $\square$

La hipótesis $t_k > C^*/3$ se usó dos veces, para descartar máquinas con tres tareas
en el óptimo. Comprobémoslo, y comprobemos que sin ella el lema es falso: si la
comprobación no pudiera fallar, no estaría comprobando nada.

```{python continue}
def comprobar_lema(con_hipotesis, veces=600):
    rng = random.Random(3)
    pasos = fallos = 0
    for _ in range(veces):
        m = rng.randint(2, 3)
        t = sorted((rng.randint(1, 20) for _ in range(rng.randint(m + 1, 8))),
                   reverse=True)
        carga = [0] * m
        for k, x in enumerate(t):
            i = min(range(m), key=lambda i: carga[i])
            carga[i] += x
            opt_k = carga_optima(t[:k + 1], m)
            if 3 * x > opt_k or not con_hipotesis:
                pasos += 1
                fallos += carga[i] > opt_k
    return pasos, fallos

print("con t_k > C*/3: (pasos, fallos) =", comprobar_lema(True))
print("sin hipótesis:  (pasos, fallos) =", comprobar_lema(False))
```

Con la hipótesis, el lema se cumple en los 2 137 pasos donde aplica. Sin ella, la
máquina elegida pasa del óptimo en 204 de 3 429 pasos.

*Demostración del teorema 4.* Sea $i$ la máquina con carga $L$ y $j$ su última tarea.
LPT sobre las tareas $1, \dots, j$ hace lo mismo que sobre todas hasta el paso $j$, así
que esa máquina carga $L$ también allí. Sea $C^*$ el óptimo de esas $j$ tareas; quitar
tareas no empeora el óptimo, así que $C^* \le \mathrm{OPT}$.

- Si $t_j > C^*/3$, el lema 5 da $L \le C^* \le \mathrm{OPT}$.
- Si $t_j \le C^*/3$, la desigualdad del teorema 3 aplicada a las $j$ tareas, cuya suma
  es a lo sumo $m C^*$, da
  $L \le C^* + (1 - 1/m)\,C^*/3 = (4/3 - 1/(3m))\,C^*$.

En los dos casos $L \le (4/3 - 1/(3m))\,\mathrm{OPT}$. $\square$

El artículo es "Bounds on Multiprocessing Timing Anomalies" (*SIAM Journal on Applied
Mathematics* 17(2), 1969, pp. 416–429). La cota se alcanza: el ejercicio 1 te hace
trazar LPT en una entrada que lo prueba para $m = 3$. Y el capítulo 23 vuelve sobre este
problema con un esquema que, para $m$ fijo, se acerca al óptimo tanto como se quiera.

## 8. k-center: el más lejano

Ahora un problema de ubicar: hay $n$ puntos con una distancia $d$ que es una **métrica**
(simétrica, cero solo de un punto a sí mismo, y con la desigualdad triangular
$d(x, z) \le d(x, y) + d(y, z)$). Hay que elegir $k$ de ellos como centros para que el
punto peor atendido quede lo más cerca posible de su centro:
$$r(C) = \max_{p} \min_{c \in C} d(p, c), \qquad |C| = k.$$
Piensa en $k$ estaciones de bomberos y la casa que queda más lejos de la suya.

¿Qué cota del óptimo se calcula aquí? Supón que encuentras $k + 1$ puntos a distancia al
menos $r$ entre sí, dos a dos. Con $k$ centros, dos de esos $k + 1$ puntos quedan con el
mismo centro óptimo $c^*$, y por la desigualdad triangular
$r \le d(x, y) \le d(x, c^*) + d(c^*, y) \le 2\,\mathrm{OPT}$. Así que
$\mathrm{OPT} \ge r/2$: $k + 1$ puntos dispersos son un certificado de que el óptimo no
puede ser muy bueno.

El algoritmo construye ese certificado mientras elige. Empieza con cualquier punto como
primer centro, y después agrega cada vez el punto **más lejano** de los centros que ya
tiene:

```{python echo=false}
# Cadena nueva: los bloques de k-center no re-ejecutan los de vertex cover y carga.
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))
import figuras_21 as F21
```

```{python continue}
def mas_lejano(P, k):
    C = [0]
    while len(C) < k:
        C.append(max(range(len(P)),
                     key=lambda j: min(math.dist(P[j], P[c]) for c in C)))
    return C

def radio(P, C):
    return max(min(math.dist(p, P[c]) for c in C) for p in P)

def radio_optimo(P, k):                      # el oráculo: todos los subconjuntos
    return min(radio(P, S) for S in itertools.combinations(range(len(P)), k))

rng = random.Random(4)
P = [(rng.random(), rng.random()) for _ in range(22)]
C = mas_lejano(P, 4)
r = radio(P, C)
lejano = max(range(len(P)), key=lambda j: min(math.dist(P[j], P[c]) for c in C))
print(f"centros {C}, radio {r:.3f}, óptimo {radio_optimo(P, 4):.3f}")
```

```{python continue echo=false output=asis}
print(F21.kcentro(P, C, r, lejano, pie=(
    "El más lejano con k = 4 sobre 22 puntos al azar (semilla 4). Los cuadrados son "
    "los centros, numerados en el orden en que los eligió; los círculos tienen el "
    "radio logrado. El punto marcado es el que lo realiza: él y los cuatro centros "
    "están a distancia al menos r entre sí.")))
```

**Teorema 6.** El más lejano devuelve $k$ centros con $r(C) \le 2\,\mathrm{OPT}$, en
tiempo $O(nk)$ si se guarda para cada punto su distancia al centro más cercano.

*Demostración.* Sea $r = r(C)$ y $q$ el punto que lo realiza. Afirmamos que los $k + 1$
puntos $c_1, \dots, c_k, q$ están a distancia al menos $r$ dos a dos. La distancia de
$q$ al conjunto de centros solo baja cuando el conjunto crece, y al final vale $r$; así
que en cada momento valía al menos $r$. Cuando se eligió $c_i$, era el más lejano del
conjunto de entonces, más lejano que $q$, así que estaba a distancia al menos $r$ de
cada centro anterior. Y $q$ está a distancia al menos $r$ de todos los centros
finales. Con el argumento de antes, $r \le 2\,\mathrm{OPT}$. Para el tiempo, cada
nuevo centro actualiza las $n$ distancias en $O(n)$. $\square$

El código guarda el conjunto y recalcula, que es más corto de leer y cuesta
$O(nk^2)$. En la @fig-aprox-kcentro el radio logrado es 0,445 y el óptimo 0,315: la
razón en esa entrada es 1,41. Sobre entradas al azar contra el oráculo:

```{python continue}
rng = random.Random(21)
peor = 0
for _ in range(800):
    k = rng.randint(2, 4)
    Q = [(rng.random(), rng.random()) for _ in range(rng.randint(k + 2, 10))]
    rq, opt = radio(Q, mas_lejano(Q, k)), radio_optimo(Q, k)
    assert rq <= 2 * opt + 1e-12
    peor = max(peor, rq / opt)
print(f"800 entradas, peor razón {peor:.3f}")
```

La razón 2 casi se alcanza con puntos al azar en el plano: 1,992. Teofilo Gonzalez
publicó este recorrido en "Clustering to minimize the maximum intercluster distance"
(*Theoretical Computer Science* 38, 1985, pp. 293–306), para la variante que minimiza
el mayor diámetro de los grupos, con la misma razón 2 y la misma hipótesis triangular.

## 9. No hay razón $2 - \varepsilon$

Con un problema NP-duro lo normal es no saber si una razón se puede mejorar. Con
k-center sí sabemos: 2 es lo mejor posible, salvo que P = NP. La herramienta es la
reducción del capítulo 16, usada de una manera nueva: el problema de partida se
convierte en una entrada donde el óptimo vale 1 o vale 2, sin término medio, y un
algoritmo que aproximara mejor que 2 distinguiría los dos casos.

El problema de partida es **conjunto dominante**: dado $G = (V, E)$ y $k$, ¿hay
$D \subseteq V$ con $|D| \le k$ tal que todo vértice está en $D$ o es vecino de alguien
de $D$? Es NP-completo, y la reducción desde vertex cover es uno de los ejercicios del
capítulo 18.

**Teorema 7.** Si P ≠ NP, para ningún $\varepsilon > 0$ hay una
$(2 - \varepsilon)$-aproximación polinomial de k-center métrico.

*Demostración.* Dado $(G, k)$ con $k \le |V|$, los puntos son los vértices, con
$d(u, v) = 1$ si $\{u, v\} \in E$, $d(u, v) = 2$ si $u \ne v$ no son vecinos, y
$d(u, u) = 0$. Es una métrica: en tres puntos distintos, $d(x, z) \le 2 \le d(x, y) +
d(y, z)$, porque cada sumando vale al menos 1; si dos coinciden, la desigualdad es
inmediata.

Si $G$ tiene un conjunto dominante de tamaño a lo sumo $k$, completándolo con vértices
cualesquiera hasta tener $k$ se obtienen $k$ centros con radio a lo sumo 1, y
$\mathrm{OPT} \le 1$. Si no lo tiene, cualquier elección de $k$ centros deja un vértice
que ni es centro ni es vecino de un centro, a distancia 2, y $\mathrm{OPT} = 2$.

Supón un algoritmo polinomial $A$ de razón $2 - \varepsilon$. En el primer caso devuelve
radio a lo sumo $(2 - \varepsilon) \cdot 1 < 2$, y como todas las distancias son 0, 1
o 2, el radio es a lo sumo 1. En el segundo, todo radio es 2. Mirando si $A$ devolvió
radio 2 decidimos conjunto dominante en tiempo polinomial, y P = NP. $\square$

Fíjate en dónde entró la métrica: solo en que las distancias 1 y 2 cumplen la
desigualdad triangular. El ejercicio 9 pregunta qué pasa si se quita. La dificultad de
aproximar k-center la observaron Wen-Lian Hsu y George Nemhauser en "Easy and hard
bottleneck location problems" (*Discrete Applied Mathematics* 1(3), 1979,
pp. 209–215), y el resumen del artículo de Gonzalez también dice que su factor 2 es el
mejor posible si P ≠ NP.

## 10. Set cover goloso

**Set cover** con pesos: un universo $U$ de $n$ elementos, conjuntos
$S_1, \dots, S_s \subseteq U$ con costos $c_j > 0$, y hay que elegir conjuntos de costo
total mínimo cuya unión sea $U$. Es NP-duro: vertex cover es el caso en que cada
elemento (una arista) está en exactamente dos conjuntos (sus extremos), que es la
reducción del capítulo 18.

El goloso del capítulo 9 elegía por el valor más alto. Aquí lo natural es elegir el
conjunto más barato **por elemento nuevo que cubre**: si $R$ es lo que falta cubrir, el
que minimiza $c_j / |S_j \cap R|$. El cociente es el **precio** que pagan los
elementos que ese conjunto cubre por primera vez, y lo anotamos, porque es la cota que
vamos a necesitar.

```{python echo=false}
# Cadena nueva: set cover y MAX-3SAT.
import itertools
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(".."))
```

```{python continue}
def set_cover_goloso(U, conjuntos, costo):
    falta, elegidos, precio = set(U), [], {}
    while falta:
        j = min((j for j in range(len(conjuntos)) if conjuntos[j] & falta),
                key=lambda j: Fraction(costo[j], len(conjuntos[j] & falta)))
        nuevos = conjuntos[j] & falta
        for e in nuevos:
            precio[e] = Fraction(costo[j], len(nuevos))
        falta -= nuevos
        elegidos.append(j)
    return elegidos, precio

U = set(range(6))
conjuntos = [{0, 1, 2, 3}, {0, 1}, {2, 3, 4, 5}, {4, 5}]
costo = [5, 1, 5, 1]
elegidos, precio = set_cover_goloso(U, conjuntos, costo)
print("elige", elegidos, "costo", sum(costo[j] for j in elegidos))
print("precios", {e: str(p) for e, p in sorted(precio.items())})
```

En el ejemplo, los dos conjuntos de costo 1 cubren dos elementos cada uno a precio
$1/2$, y los de costo 5 cubren cuatro a $5/4$. El goloso toma los dos baratos y le
quedan los elementos 2 y 3, que solo están en conjuntos de costo 5; toma uno y paga 7.
El óptimo es $\{0,1,2,3\}$ con $\{4,5\}$, que cuesta 6. Fíjate en la suma de precios:
$4 \cdot \tfrac12 + 2 \cdot \tfrac52 = 7$, que es exactamente lo que pagó.

## 11. $H_n$ por reparto de costos

Ese último hecho vale siempre: cada vez que el goloso paga $c_j$, reparte ese costo en
partes iguales entre los $|S_j \cap R|$ elementos nuevos, así que

$$\text{costo del goloso} = \sum_{e \in U} \mathrm{precio}(e).$$

Ahora el costo está escrito elemento por elemento, y el óptimo también cubre cada
elemento. Si demostramos que ningún conjunto puede tener elementos "demasiado caros" en
total comparado con lo que cuesta, la comparación sale sumando. Escribimos
$H_d = 1 + \tfrac12 + \dots + \tfrac1d$, que cumple $H_d \le 1 + \ln d$.

**Lema 8.** Para todo conjunto $S$ de costo $c$, $\sum_{e \in S} \mathrm{precio}(e) \le
c \cdot H_{|S|}$.

*Demostración.* Ordena los elementos de $S$ por el momento en que el goloso los cubrió:
$e_1, \dots, e_d$, con $d = |S|$ y los empates en cualquier orden. Justo antes del paso
que cubre a $e_i$, ninguno de $e_i, \dots, e_d$ está cubierto, así que $S$ le ofrece al
goloso al menos $d - i + 1$ elementos nuevos a un precio por elemento de a lo sumo
$c / (d - i + 1)$. El goloso elige el conjunto con el menor precio por elemento, así que
el precio que paga $e_i$ es a lo sumo ese:
$$\mathrm{precio}(e_i) \le \frac{c}{d - i + 1}.$$
Sumando para $i = 1, \dots, d$: $c\,(1/d + 1/(d-1) + \dots + 1) = c\,H_d$. $\square$

El paso fino es el de los empates: los elementos que se cubren en el mismo paso que
$e_i$ y van después de él en el orden siguen sin cubrir justo antes de ese paso, así que
la cuenta $d - i + 1$ no cambia.

**Teorema 9.** El goloso paga a lo sumo $H_n \cdot \mathrm{OPT}$, con $n = |U|$.

*Demostración.* Sea $\mathcal{O}$ la familia óptima. Cada elemento está en al menos un
conjunto de $\mathcal{O}$, y los precios son positivos, así que
$$\sum_{e \in U} \mathrm{precio}(e) \le \sum_{S \in \mathcal{O}} \sum_{e \in S}
\mathrm{precio}(e) \le \sum_{S \in \mathcal{O}} c_S\,H_{|S|} \le H_n \cdot
\mathrm{OPT}. \qquad \square$$

Esto es el reparto de costos: el costo del algoritmo se reparte entre los elementos, y
el lema 8 dice que ningún conjunto del óptimo carga con más de $H_n$ veces su costo. La
cota del óptimo de este capítulo es menos visible que las anteriores: es la suma de
precios dividida por $H_n$. Comprobemos el lema 8 y el teorema contra el oráculo:

```{python continue}
def set_cover_optimo(U, conjuntos, costo):
    return min(sum(costo[j] for j in T)
               for r in range(1, len(conjuntos) + 1)
               for T in itertools.combinations(range(len(conjuntos)), r)
               if set().union(*(conjuntos[j] for j in T)) >= U)

def H(d):
    return sum(Fraction(1, i) for i in range(1, d + 1))

rng = random.Random(21)
peor, n_inst = 0, 0
for _ in range(1000):
    n = rng.randint(3, 9)
    U = set(range(n))
    S = [s for s in (set(e for e in U if rng.random() < 0.4)
                     for _ in range(rng.randint(3, 8))) if s]
    if not S or set().union(*S) != U:
        continue
    c = [rng.randint(1, 10) for _ in S]
    elegidos, precio = set_cover_goloso(U, S, c)
    pagado = sum(c[j] for j in elegidos)
    assert pagado == sum(precio.values())
    for Sj, cj in zip(S, c):
        assert sum(precio[e] for e in Sj) <= cj * H(len(Sj))      # lema 8
    opt = set_cover_optimo(U, S, c)
    assert pagado <= H(n) * opt                                   # teorema 9
    peor, n_inst = max(peor, Fraction(pagado, opt)), n_inst + 1
print(f"{n_inst} entradas, peor razón {float(peor):.2f}")
```

El peor caso medido, 1,8, queda lejos de $H_9 \approx 2{,}83$, pero eso es por el tamaño
de las entradas: el ejercicio 3 pide una familia en la que el goloso paga
$\Theta(\log n)$ veces el óptimo. Vašek Chvátal demostró la cota con pesos en "A Greedy
Heuristic for the Set-Covering Problem" (*Mathematics of Operations Research* 4(3),
1979, pp. 233–235). Y no se puede hacer mucho mejor: Irit Dinur y David Steurer
demostraron en "Analytical approach to parallel repetition" (STOC 2014, pp. 624–633)
que aproximar set cover con razón $(1 - \varepsilon)\ln n$ es NP-duro para todo
$\varepsilon > 0$. Como $H_n \le 1 + \ln n$, el goloso está a un término de orden menor
de lo mejor posible.

## 12. MAX-3SAT: 7/8 por linealidad de la esperanza

El último ejemplo maximiza, y la cota del óptimo es la más tonta posible. En MAX-3SAT
hay $k$ cláusulas, cada una con exactamente tres literales de variables **distintas**,
y se quiere una asignación que satisfaga el mayor número. El óptimo es a lo sumo $k$. Esa
es la cota.

El algoritmo tampoco piensa: a cada variable, verdadero o falso a cara o cruz. Una
cláusula queda sin satisfacer solo si sus tres literales salen falsos, y como son de
tres variables distintas, eso pasa con probabilidad $(1/2)^3 = 1/8$. Sea $X_C$ la
indicadora de que la cláusula $C$ queda satisfecha y $X = \sum_C X_C$. Por linealidad de
la esperanza, la herramienta del capítulo 8, §4,
$$E[X] = \sum_C E[X_C] = \frac{7}{8}\,k \ge \frac{7}{8}\,\mathrm{OPT}.$$
La linealidad no pide independencia entre cláusulas, y aquí no la hay: dos cláusulas que
comparten una variable dependen una de la otra.

```{python continue}
def satisfechas(F, a):
    return sum(any(a[x] == signo for x, signo in C) for C in F)

rng = random.Random(21)
v, k = 10, 40
F = [[(x, rng.random() < 0.5) for x in rng.sample(range(v), 3)] for _ in range(k)]
todas = [satisfechas(F, a) for a in itertools.product([False, True], repeat=v)]
print(f"promedio sobre las {len(todas)} asignaciones: "
      f"{Fraction(sum(todas), len(todas))}, 7k/8 = {Fraction(7 * k, 8)}")
```

El promedio exacto sobre las $2^{10}$ asignaciones es 35, que es $7 \cdot 40 / 8$. No es
casualidad de la semilla: el promedio sobre todas las asignaciones es la esperanza, y la
cuenta de arriba la fija en $7k/8$ para cualquier fórmula.

Hay dos consecuencias. La primera: **toda** fórmula de 3-SAT con cláusulas así tiene una
asignación que satisface al menos $7k/8$ cláusulas, porque una variable aleatoria no
puede estar siempre por debajo de su esperanza. Es una demostración de existencia por
azar, sin construir nada; en particular, toda fórmula con a lo sumo 7 cláusulas de este
tipo es satisfacible.

La segunda: un algoritmo de Las Vegas (capítulo 8) que repite hasta encontrar una
asignación con al menos $7k/8$ cláusulas satisfechas termina rápido. Sea $p$ la
probabilidad de que una asignación al azar lo logre, y $k'$ el mayor entero
estrictamente menor que $7k/8$. Las asignaciones malas satisfacen a lo sumo $k'$
cláusulas y las buenas a lo sumo $k$, así que
$$\frac{7}{8}k = E[X] \le k'(1 - p) + kp \le k' + kp.$$
Como $8k' < 7k$ son enteros, $7k - 8k' \ge 1$, es decir $\tfrac78 k - k' \ge \tfrac18$.
Entonces $kp \ge 1/8$, $p \ge 1/(8k)$, y el número esperado de intentos es a lo sumo
$8k$ (la esperanza de una geométrica, capítulo 8). Medido sobre la fórmula de arriba:

```{python continue}
intentos = []
for _ in range(2000):
    n_int = 1
    while 8 * satisfechas(F, [rng.random() < 0.5 for _ in range(v)]) < 7 * k:
        n_int += 1
    intentos.append(n_int)
print(f"intentos: promedio {sum(intentos) / len(intentos):.2f}, "
      f"máximo {max(intentos)}, cota 8k = {8 * k}")
```

Hicieron falta 1,64 intentos en promedio y 10 como máximo, contra una cota de 320.
La cota $8k$ es muy holgada en esta fórmula, pero es una garantía para todas. El
ejercicio 7 quita el azar del todo.

Y aquí también la razón es la mejor posible. Johan Håstad demostró en "Some optimal
inapproximability results" (*Journal of the ACM* 48(4), 2001, pp. 798–859) que, para
todo $\varepsilon > 0$, aproximar MAX-3SAT con cláusulas de exactamente tres literales
con razón $7/8 + \varepsilon$ es NP-duro. Tirar monedas, sin mirar la fórmula, es lo
mejor que un algoritmo polinomial puede garantizar si P ≠ NP.

## 13. La regla

Una razón de aproximación es una demostración contra una cota del óptimo que se puede
calcular, y la cota decide la razón. Los cinco problemas del capítulo, con la cota que
usó cada uno:

| Problema | Cota del óptimo | Razón | Lo que se sabe del otro lado |
|---|---|---|---|
| Vertex cover | un emparejamiento | 2 | |
| Balanceo de carga | $\max t_j$ y $T/m$ | $2 - 1/m$; LPT $4/3 - 1/(3m)$ | capítulo 23 |
| k-center métrico | $k + 1$ puntos a distancia $\ge r$ | 2 | $2 - \varepsilon$ es NP-duro (§9) |
| Set cover | la suma de precios entre $H_n$ | $H_n$ | $(1 - \varepsilon)\ln n$ es NP-duro |
| MAX-3SAT | el número de cláusulas | $7/8$ | $7/8 + \varepsilon$ es NP-duro |

Cuando una razón no mejora, casi siempre es porque la cota no da más: el emparejamiento
puede ser la mitad del óptimo, el promedio de carga puede estar lejos del makespan. Para
mejorar la razón hay que mejorar la cota. El capítulo 22 cambia de cota: la solución de
un programa lineal, que se calcula en tiempo polinomial y queda por debajo del óptimo
entero, sirve para el vertex cover con pesos y para el TSP métrico. Y el capítulo 23
cambia de pregunta: en lugar de una razón fija, una familia de algoritmos, uno por cada
$\varepsilon$, que llega a $1 + \varepsilon$ pagando más tiempo.

## Resumen

- Una $\alpha$-aproximación corre en tiempo polinomial y cumple $c \le \alpha \cdot
  \mathrm{OPT}$ (minimizar) o $v \ge \alpha \cdot \mathrm{OPT}$ (maximizar) en **toda**
  entrada.
- La técnica: una cota $B \le \mathrm{OPT}$ que se puede calcular y $c \le \alpha B$.
- Vertex cover: un emparejamiento acota el óptimo por debajo; tomar los dos extremos de
  cada arista descubierta da razón 2.
- Tomar un solo extremo por arista rompe la cota, gana en las pruebas al azar y no tiene
  razón 2: con $k = 24$ paga 2,5 veces un cubrimiento conocido.
- Balanceo de carga: $\mathrm{OPT} \ge \max t_j$ y $\mathrm{OPT} \ge T/m$. Graham da
  $2 - 1/m$ mirando la última tarea de la máquina más cargada. LPT da
  $4/3 - 1/(3m)$: si la última tarea pasa de $\mathrm{OPT}/3$, LPT no se equivoca.
- k-center métrico: el más lejano da razón 2, porque deja $k + 1$ puntos a distancia
  $\ge r$ y dos comparten centro óptimo. Mejor que 2 es NP-duro, desde conjunto
  dominante con distancias 1 y 2.
- Set cover: el goloso por costo por elemento nuevo da $H_n \le 1 + \ln n$, repartiendo
  el costo en precios y acotando lo que paga cada conjunto del óptimo.
- MAX-3SAT: una asignación al azar satisface $7k/8$ cláusulas en esperanza, así que
  siempre existe una así, y repetir encuentra una en a lo sumo $8k$ intentos esperados.

## Ejercicios

1. Ejecuta LPT a mano con $m = 3$ máquinas sobre las tareas de duraciones
   $5, 5, 4, 4, 3, 3, 3$, anotando las cargas después de cada tarea. Encuentra el
   makespan óptimo y demuestra que lo es con una cota del óptimo, sin enumerar
   asignaciones. Compara la razón obtenida con $4/3 - 1/(3m)$.

2. Entradas ajustadas. (a) Para cada $n \ge 1$, da un grafo en el que
   `cubrimiento_emparejamiento` devuelve exactamente el doble del óptimo **sea cual sea
   el orden** en que recorre las aristas. (b) Para cada $m \ge 2$, da una lista de
   tareas, en un orden de llegada, en la que la regla de Graham da un makespan
   exactamente $2 - 1/m$ veces el óptimo. Demuestra en los dos casos cuánto vale el
   óptimo.

3. Para cada $k \ge 2$, construye una entrada de set cover con todos los costos iguales
   a 1, del orden de $2^k$ elementos, en la que el óptimo usa 2 conjuntos y el goloso de
   §10, sin empates en ningún paso, usa $k$. Deduce que la razón del goloso no está
   acotada por ninguna constante. (Pista: dos conjuntos grandes que parten el universo,
   y otros que crecen al doble.)

4. En **empaquetamiento en cajas** hay $n$ objetos de tamaños en $(0, 1]$ y cajas de
   capacidad 1, y se quiere usar el menor número de cajas. Supón que PARTICIÓN
   (¿se pueden repartir enteros positivos en dos grupos de igual suma?) es NP-completo,
   como pide uno de los ejercicios del capítulo 19. Demuestra que si P ≠ NP no hay
   algoritmo polinomial de razón $\alpha < 3/2$ para empaquetamiento en cajas.

5. En set cover sin pesos, cada elemento está en a lo sumo $f$ conjuntos. Considera el
   algoritmo que, mientras quede algún elemento sin cubrir, elige uno cualquiera de
   ellos y toma **todos** los conjuntos que lo contienen. Demuestra que tiene razón
   $f$. ¿A qué algoritmo de este capítulo se reduce cuando la entrada sale de la
   reducción de vertex cover a set cover del capítulo 18?

6. ★ En MAX-CUT se parte el conjunto de vértices de un grafo con $m$ aristas en dos
   lados, y se quiere maximizar el número de aristas que cruzan. La búsqueda local
   empieza con cualquier partición y, mientras algún vértice tenga más vecinos de su
   propio lado que del otro, lo cambia de lado. Demuestra que hace a lo sumo $m$
   cambios y que al terminar cruzan al menos $m/2$ aristas. Deduce que es una
   $1/2$-aproximación, y di cuál fue la cota del óptimo.

7. Quita el azar del algoritmo de §12 por **esperanzas condicionales**: decide las
   variables una a una; para $x_1$, calcula el número esperado de cláusulas satisfechas
   si $x_1$ es verdadero y el resto al azar, y lo mismo con $x_1$ falso, y quédate con
   el valor que da la esperanza mayor; repite con $x_2$, y así. Demuestra que la
   asignación final satisface al menos $7k/8$ cláusulas y que cada esperanza se calcula
   en tiempo polinomial. Impleméntalo y compáralo con el algoritmo de Las Vegas en
   fórmulas al azar de 10 a 20 variables: cláusulas satisfechas y tiempo.

8. Implementa un buscador de malas entradas para LPT con $m = 2$: búsqueda al azar, o
   local sobre las duraciones, de entradas de a lo sumo 7 tareas con duraciones en
   $[1, 30]$, que maximice la razón contra `carga_optima`. ¿Llegas a la cota
   $4/3 - 1/(3m)$? Haz lo mismo para la regla de Graham con el orden de llegada como
   parte de la búsqueda, y compara las dos razones máximas que encuentres con las
   medidas en §6.

9. En k-center, quita la desigualdad triangular: las distancias siguen siendo simétricas
   y positivas entre puntos distintos, pero nada más. Señala el paso de la demostración
   del teorema 6 que deja de valer. Después demuestra que, si P ≠ NP, no hay algoritmo
   polinomial de razón $\alpha$ para **ninguna** constante $\alpha \ge 1$.

10. Una ciudad quiere ubicar bases de ambulancias en algunas de sus 60 policlínicas. Se
    conocen los tiempos de viaje entre cada par de policlínicas por la red de calles.
    (a) La dirección de salud pide el menor número de bases tal que toda policlínica
    quede a lo sumo a 10 minutos de una base. (b) El presupuesto alcanza para 6 bases,
    y se quiere que el peor tiempo de llegada sea el menor posible. Modela cada versión
    como uno de los problemas del capítulo, di qué algoritmo usarías y qué garantía da.
    ¿Cumplen los tiempos de viaje la hipótesis que necesita el teorema 6 si se miden
    como caminos más cortos en la red, y qué cambia si se miden en un solo sentido de
    calles con dirección única?
