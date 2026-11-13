# Algoritmos golosos con argumentos de intercambio {#chap-golosos}

Un algoritmo goloso toma decisiones de una en una, cada vez la que parece mejor en ese
momento, y nunca vuelve atrás. Escribirlo es fácil. Lo difícil es saber si acierta, porque al lado de cada regla buena
hay otra igual de razonable que se equivoca, y las dos pasan las pruebas a mano. Este
capítulo enseña la herramienta con la que se decide: el **argumento de intercambio**.
Se toma una solución óptima cualquiera y se la transforma, paso a paso, en la que
construye el goloso, sin empeorarla nunca.

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_09.py
import figuras_09 as G
```

## 1. Decidir una vez

Seguramente ya usaste algoritmos golosos en un curso de estructuras de datos. Kruskal agrega la arista más
barata que no cierra un ciclo, Dijkstra fija el vértice más cercano que queda por
fijar, y ninguno de los dos revisa una decisión tomada. La demostración habitual de
Kruskal, la propiedad del corte, ya es un intercambio: si un árbol óptimo no usa la
arista más barata de un corte, se le cambia una de sus aristas por ella y no cuesta
más. Este capítulo convierte esa idea en un método: si una solución óptima no hace lo
que hizo el goloso, se la cambia para que lo haga sin que cueste más.

Esa forma ya apareció en el capítulo 3, §9. Para demostrar que Gale-Shapley le da a
cada proponente su mejor pareja válida tomamos el **primer** rechazo malo de la
ejecución, y usamos que todo lo anterior estaba bien. Un intercambio busca, del mismo modo, la
primera decisión en que el goloso y un óptimo difieren, y arregla el óptimo ahí.

El capítulo tiene dos problemas. En el **retraso máximo** el intercambio es local:
dos tareas vecinas se cambian de lugar y nada más se mueve. En la **caché óptima fuera
de línea** no lo es: cambiar una decisión obliga a cambiar otras más adelante. En los
dos casos la demostración necesita una **medida que decrece** con cada paso de la
transformación, y encontrar esa medida es el trabajo.

## 2. El retraso máximo

Una máquina atiende $n$ tareas, una a la vez y sin interrupciones, a partir del
instante 0. La tarea $i$ dura $t_i$ y tiene un plazo $d_i$. Un orden de las tareas fija
cuándo termina cada una: si $i$ va después de las tareas de un conjunto $A$, termina en
$f_i = \sum_{j \in A} t_j + t_i$. Su **retraso** es lo que se pasa del plazo,
$\ell_i = \max(0, f_i - d_i)$, y queremos el orden que minimiza el **retraso máximo**
$L = \max_i \ell_i$. Es la formulación de Kleinberg y Tardos (*Algorithm Design*,
Addison-Wesley, 2005, §4.2), que es el texto que este capítulo sigue en los dos
problemas.

El código calcula $L$ y un oráculo prueba los $n!$ órdenes; con cuatro tareas son 24.

```{python continue}
def detalle(orden, t, d):
    """Instante de terminación y retraso de cada tarea, atendidas en `orden`."""
    fin, finales, retrasos = 0, {}, {}
    for i in orden:
        fin += t[i]
        finales[i] = fin
        retrasos[i] = max(0, fin - d[i])
    return finales, retrasos

def retraso(orden, t, d):
    return max(detalle(orden, t, d)[1].values())

def optimo(t, d):
    return min(retraso(p, t, d) for p in itertools.permutations(range(len(t))))

t = [1, 3, 2, 4]          # duraciones de las tareas 1, 2, 3, 4
d = [8, 3, 6, 10]         # plazos
valores = [retraso(p, t, d) for p in itertools.permutations(range(4))]
print("óptimo:", optimo(t, d))
print("órdenes que lo alcanzan:", valores.count(min(valores)), "de", len(valores))
print("orden 1 2 3 4:", retraso([0, 1, 2, 3], t, d))
```

Hazlo a mano para el orden $1, 2, 3, 4$: las tareas terminan en 1, 4, 6 y 10. La
tarea 2 tenía plazo 3 y termina en 4, así que $L = 1$. Solo 2 de los 24 órdenes
consiguen que nadie llegue tarde, y una regla golosa tiene que dar con uno.

## 3. Tres reglas y un experimento

¿Por qué orden empezar? Hay tres ideas naturales, y cada una tiene su argumento:

- **La más corta primero.** Despacha muchas tareas rápido, y así casi todas terminan
  pronto. Es la regla que minimiza la suma de los tiempos de terminación (el caso de
  pesos iguales del ejercicio 7).
- **La de menor holgura primero.** La holgura $d_i - t_i$ es cuánto puede esperar la
  tarea antes de empezar sin llegar tarde. La de menor holgura es la más urgente.
- **El plazo más cercano primero.** Ordena solo por $d_i$. Ignora las duraciones por
  completo, y eso parece un descuido: una tarea larga con plazo cercano pasa delante de
  diez cortas.

La primera falla con dos tareas. La tarea 1 dura 1 y vence en 100, la tarea 2 dura 10
y vence en 10. La más corta primero hace la 1, y la 2 termina en 11, un instante tarde.
Al revés, las dos llegan a tiempo.

```{python continue}
reglas = {
    "la más corta primero": lambda t, d: sorted(range(len(t)), key=lambda i: t[i]),
    "la de menor holgura":  lambda t, d: sorted(range(len(t)), key=lambda i: d[i] - t[i]),
    "el plazo más cercano": lambda t, d: sorted(range(len(t)), key=lambda i: d[i]),
}
print("dos tareas, la más corta primero:",
      retraso(reglas["la más corta primero"]([1, 10], [100, 10]), [1, 10], [100, 10]),
      "  óptimo:", optimo([1, 10], [100, 10]))
for nombre, regla in reglas.items():
    print(f"{nombre:22}  L = {retraso(regla(t, d), t, d)}")
```

En las cuatro tareas de la sección 2 la menor holgura también se equivoca, con $L = 2$
donde se podía 0. Un ejemplo no decide nada, así que probemos las tres reglas contra el
oráculo en muchas instancias al azar.

```{python continue}
rng = random.Random(9)
fallan = dict.fromkeys(reglas, 0)
N = 2000
for _ in range(N):
    n = rng.randint(2, 5)
    tt = [rng.randint(1, 10) for _ in range(n)]
    dd = [rng.randint(1, 30) for _ in range(n)]
    o = optimo(tt, dd)
    for nombre, regla in reglas.items():
        fallan[nombre] += retraso(regla(tt, dd), tt, dd) > o
for nombre, f in fallan.items():
    print(f"{nombre:22} {f:5} de {N} instancias por encima del óptimo")
```

El plazo más cercano no falla nunca, y las otras dos fallan a menudo. El experimento
propone un teorema, pero 2 000 instancias de hasta cinco tareas no lo demuestran. Las
dos secciones que siguen sí, y explican por qué la regla puede ignorar las
duraciones.

## 4. Inversiones

Antes del intercambio hacen falta dos observaciones sobre la forma de los órdenes.

**Sin tiempo ocioso.** En nuestro modelo un orden no deja huecos: cada tarea empieza
cuando termina la anterior. Un horario podría dejar la máquina parada a ratos, pero
existe un óptimo que no lo hace. Esa demostración es corta y es el ejercicio 3; es la
razón de que podamos hablar de órdenes en vez de horarios.

**Inversiones.** Un orden tiene una **inversión** si una tarea $i$ va antes que otra
$j$ con $d_i > d_j$: la de plazo más lejano va primero. El plazo más cercano produce,
por construcción, un orden sin inversiones. Si hay plazos repetidos, hay varios órdenes
sin inversiones, uno por cada manera de ordenar las tareas con el mismo plazo, y la
regla puede devolver cualquiera. Lo primero es ver que eso no importa.

**Lema 1.** Todos los órdenes sin huecos ni inversiones tienen el mismo retraso máximo.

*Demostración.* Dos órdenes sin inversiones ponen las tareas en orden de plazo no
decreciente, así que solo pueden diferir en el orden de tareas con el mismo plazo.
Fijemos un plazo $\delta$. Las tareas con $d_i = \delta$ forman un bloque contiguo en
los dos órdenes, porque todas las de plazo menor van antes y todas las de plazo mayor
van después. Como no hay huecos, el bloque empieza en el mismo instante en los dos
órdenes (la suma de las duraciones de las tareas de plazo menor) y termina en el mismo
instante $F$ (esa suma más las duraciones del bloque). Dentro del bloque todas comparten
el plazo $\delta$, así que el mayor retraso es el de la que termina última, que es
$\max(0, F - \delta)$ en los dos órdenes. Las tareas de fuera del bloque no se mueven.
Como esto vale para cada plazo, el máximo sobre todas las tareas es el mismo. $\square$

Fíjate en qué se apoya la demostración: en que el retraso del bloque depende solo de
cuándo termina el bloque, y no de quién va dentro. Ahí está por qué la regla puede
ignorar las duraciones al desempatar.

## 5. El intercambio

Ahora la medida que decrece. Tomamos un óptimo sin huecos. Si no tiene inversiones,
por el Lema 1 tiene el mismo $L$ que el plazo más cercano, y terminamos. Si las tiene,
vamos a quitárselas de una en una sin que $L$ suba.

**Lema 2.** Si un orden tiene una inversión, tiene una inversión entre dos tareas
**vecinas**.

*Demostración.* Si ninguna pareja de vecinas está invertida, los plazos son no
decrecientes de cada tarea a la siguiente, y por transitividad de cualquier tarea a
cualquiera posterior. Entonces no hay inversiones. $\square$

**Lema 3.** Si $i$ y $j$ son vecinas, $i$ va justo antes que $j$ y $d_i > d_j$,
cambiarlas de lugar quita exactamente una inversión y no aumenta el retraso máximo.

*Demostración.* Las inversiones primero: el intercambio cambia el orden relativo de la
pareja $i, j$ y de ninguna otra, porque cualquier otra tarea queda del mismo lado de
las dos. La pareja $i, j$ estaba invertida y deja de estarlo, así que se quita una.

Ahora los retrasos. Llamemos $f$ a los tiempos de antes y $f'$ a los de después. Las
tareas que no son $i$ ni $j$ terminan donde terminaban: las de antes de la pareja no
se tocaron, y las de después empiezan cuando termina la pareja, que ocupa el mismo
intervalo. La tarea $j$ ahora va primero, así que termina antes y $\ell'_j \le \ell_j$.
La tarea $i$ ahora termina donde terminaba $j$, $f'_i = f_j$. Como $d_i > d_j$,

$$\ell'_i = \max(0, f_j - d_i) \le \max(0, f_j - d_j) = \ell_j \le L.$$

Ningún retraso nuevo pasa de $L$, y $L' \le L$. $\square$

El paso que todo el mundo se salta es el de "las demás tareas terminan donde
terminaban". Vale porque $i$ y $j$ son **vecinas**: la pareja ocupa el mismo intervalo
antes y después. Si se intercambian dos tareas invertidas que no son vecinas, las del
medio se mueven, y una de ellas puede terminar más tarde y llegar tarde. Por eso existe
el Lema 2, que parece trivial y es el que permite elegir una pareja que no mueve a
nadie más. Y la desigualdad usa la hipótesis $d_i > d_j$ en el único lugar donde hace
falta: es lo que permite comparar el retraso nuevo de $i$ con el viejo de $j$.

Esta es la respuesta que prometió la sección 3: la regla ignora las duraciones porque
el intercambio no las mira. La pareja ocupa el mismo intervalo en cualquier orden, y
solo el plazo decide quién va después.

Veámoslo en las cuatro tareas de la sección 2. La más corta primero da el orden
$1, 3, 2, 4$, que tiene tres inversiones: $1, 3$ y $3, 2$, que son vecinas, y $1, 2$,
que no lo es. El código busca la primera pareja vecina invertida, la cambia, y repite
hasta que no quedan.

```{python continue}
def intercambiar(orden, d):
    """Cambia la primera pareja vecina invertida. Devuelve el orden nuevo y la
    pareja, o (None, None) si el orden no tiene inversiones."""
    for p in range(len(orden) - 1):
        i, j = orden[p], orden[p + 1]
        if d[i] > d[j]:
            return orden[:p] + [j, i] + orden[p + 2:], (i, j)
    return None, None

orden = reglas["la más corta primero"](t, d)
cadena = [(orden, None)]
while True:
    orden, pareja = intercambiar(orden, d)
    if orden is None:
        break
    cadena.append((orden, pareja))
for orden, pareja in cadena:
    cambio = "" if pareja is None else f"  (cambia {pareja[0] + 1} y {pareja[1] + 1})"
    print([i + 1 for i in orden], " L =", retraso(orden, t, d), cambio)
antes, (despues, par) = cadena[0][0], cadena[1]
```

```{python continue echo=false output=asis}
filas = []
for titulo, orden in (("antes", antes), ("después", despues)):
    fin, ret = detalle(orden, t, d)
    filas.append((titulo, orden, fin, ret))
print(G.inversion(t, d, filas, par, ident="golosos-inversion",
      pie="El primer intercambio del Lema 3 sobre las cuatro tareas de la sección 2. "
          "Las tareas 1 y 3 son vecinas y están invertidas (d₁ = 8 > d₃ = 6). Al "
          "cambiarlas, la pareja ocupa el mismo intervalo, la 3 termina antes y la 1 "
          "termina donde terminaba la 3, con un plazo más holgado. Las tareas 2 y 4 "
          "no se mueven, y L no cambia."))
```

En la @fig-golosos-inversion la tarea 1 pasa a terminar en 3, donde terminaba la 3, y
su plazo es 8, más holgado que el 6 de la 3. Pero $L$ sigue en 3, porque lo fija la
tarea 2, que no se movió. El lema solo promete que $L$ no sube, y aquí no baja. Los
dos intercambios siguientes sí lo bajan, hasta el orden $2, 3, 1, 4$, que es el del plazo
más cercano y no deja a nadie tarde. Tres inversiones, tres intercambios.

**Teorema.** El plazo más cercano minimiza el retraso máximo.

*Demostración.* Sea $O$ un orden óptimo, que existe porque hay finitos órdenes. (Si se
permitieran horarios con huecos, el ejercicio 3 dice que alguno sin huecos también es
óptimo, y el teorema vale igual.) Mientras
$O$ tenga inversiones, el Lema 2 da una pareja vecina invertida y el Lema 3 la cambia
sin subir $L$. Cada cambio quita exactamente una inversión, y un orden de $n$ tareas
tiene a lo sumo $\binom{n}{2}$, así que después de un número finito de pasos queda un
orden sin huecos ni inversiones con $L \le L(O)$, que por lo tanto también es óptimo.
El plazo más cercano tampoco tiene huecos ni inversiones, y por el Lema 1 tiene el
mismo $L$. $\square$

La demostración se puede ejecutar, desde órdenes al azar, comprobando en cada paso
las dos promesas del Lema 3.

```{python continue}
def inversiones(orden, d):
    return sum(d[orden[p]] > d[orden[q]]
               for p in range(len(orden)) for q in range(p + 1, len(orden)))

rng = random.Random(3)
pasos = 0
for _ in range(2000):
    n = rng.randint(2, 8)
    tt = [rng.randint(1, 10) for _ in range(n)]
    dd = [rng.randint(1, 20) for _ in range(n)]       # con plazos repetidos
    orden = rng.sample(range(n), n)
    while True:
        nuevo, _ = intercambiar(orden, dd)
        if nuevo is None:
            break
        assert inversiones(nuevo, dd) == inversiones(orden, dd) - 1
        assert retraso(nuevo, tt, dd) <= retraso(orden, tt, dd)
        orden, pasos = nuevo, pasos + 1
    assert retraso(orden, tt, dd) == retraso(reglas["el plazo más cercano"](tt, dd), tt, dd)
print("intercambios comprobados:", pasos)
```

El último `assert` es el Lema 1: el orden final desempata distinto que `sorted` y da
el mismo $L$.

## 6. La caché

El segundo problema viene de la jerarquía de memoria. Una memoria rápida, la
**caché**, tiene lugar para $k$ elementos, y una memoria lenta los tiene todos. Llega
una sucesión de pedidos $x_1, x_2, \dots, x_m$. Si el elemento pedido está en la caché,
es un **acierto** y no cuesta nada. Si no está, es un **fallo**: hay que traerlo de la
memoria lenta y, si la caché está llena, **desalojar** uno para hacerle lugar. La
pregunta es a quién desalojar, y el objetivo es minimizar los fallos.

Vamos a suponer que la sucesión entera se conoce de antemano. Es el problema **fuera
de línea**, y parece artificial, porque un sistema operativo no sabe qué pedirá un
programa. Pero es la vara de medir: para saber si una regla real es buena hay que
compararla con lo mejor posible sobre una traza grabada.

El oráculo lleva, para cada contenido posible de la caché, los menos fallos con que se
llega a él. Es exponencial, pero con pocos elementos es inmediato.

```{python continue}
def fallos_optimos(seq, k):
    """Oráculo: para cada contenido posible de la caché, los menos fallos
    con que se llega a él. Prueba todos los desalojos."""
    estados = {frozenset(): 0}
    for x in seq:
        nuevos = {}
        for c, f in estados.items():
            if x in c:
                opciones = [(c, f)]
            elif len(c) < k:
                opciones = [(c | {x}, f + 1)]
            else:
                opciones = [((c - {y}) | {x}, f + 1) for y in c]
            for c2, f2 in opciones:
                nuevos[c2] = min(f2, nuevos.get(c2, f2))
        estados = nuevos
    return min(estados.values())
```

## 7. Belady, LRU y FIFO

Las reglas que se usan en la práctica miran el pasado. **LRU** (*least recently
used*) desaloja el elemento que lleva más tiempo sin pedirse. **FIFO** desaloja el que
lleva más tiempo en la caché. Si se conoce el futuro hay una regla más directa:
desalojar el elemento cuyo **próximo pedido está más lejos**, o uno que no se vuelve a
pedir nunca. La propuso László Bélády en «A study of replacement algorithms for a
virtual-storage computer» (*IBM Systems Journal* 5(2), 1966) y lleva su nombre.

¿Por qué se le ocurre a uno? Un elemento que se pedirá pronto, si se desaloja, causa un
fallo pronto. El que se pedirá más tarde causa su fallo más tarde, y para entonces
quizás ya hubo que desalojarlo de todas maneras. Convincente, pero la menor holgura
también lo era.

Las tres reglas comparten la simulación, que guarda la caché después de cada pedido.

```{python continue}
def proximo(seq, t, x):
    """Posición del próximo pedido de x después de t; infinito si no hay."""
    for s in range(t + 1, len(seq)):
        if seq[s] == x:
            return s
    return math.inf

def belady(seq, t, cache, ultimo, entrada):
    return max(sorted(cache), key=lambda y: proximo(seq, t, y))

def lru(seq, t, cache, ultimo, entrada):
    return min(cache, key=lambda y: ultimo[y])

def fifo(seq, t, cache, ultimo, entrada):
    return min(cache, key=lambda y: entrada[y])

def simular(seq, k, regla):
    cache, ultimo, entrada, historia = set(), {}, {}, []
    for t, x in enumerate(seq):
        if x not in cache:
            if len(cache) == k:
                cache.remove(regla(seq, t, cache, ultimo, entrada))
            cache.add(x)
            entrada[x] = t
        ultimo[x] = t
        historia.append(frozenset(cache))
    return historia

def fallos(seq, historia):
    antes = [frozenset()] + historia[:-1]
    return sum(x not in c for x, c in zip(seq, antes))

seq, k = list("abcadabcdabe"), 3
for nombre, regla in (("Belady", belady), ("LRU", lru), ("FIFO", fifo)):
    print(f"{nombre:7} {fallos(seq, simular(seq, k, regla))} fallos")
print("óptimo ", fallos_optimos(seq, k), "fallos")
```

```{python continue echo=false output=asis}
H_belady, H_lru = simular(seq, k, belady), simular(seq, k, lru)
print(G.traza(seq, k, [(f"Belady, {fallos(seq, H_belady)} fallos", H_belady),
                       (f"LRU, {fallos(seq, H_lru)} fallos", H_lru)],
      ident="golosos-traza",
      pie="Belady y LRU con una caché de 3 sobre la misma sucesión de 12 pedidos. "
          "Cada columna es la caché después de atender el pedido de arriba, con el "
          "elemento pedido sombreado; el punto rojo marca un fallo. Las dos reglas "
          "difieren por primera vez en el pedido 5."))
```

En la @fig-golosos-traza las dos reglas hacen lo mismo hasta el pedido 5, que pide $d$
con la caché llena de $a$, $b$ y $c$. LRU desaloja $b$, que es la que lleva más tiempo
sin usarse. Belady mira adelante: $a$ se pide en la posición 6, $b$ en la 7 y $c$ en la
8, y desaloja $c$. Del pedido 7 al 11 LRU falla en todos, y en los cuatro primeros
desaloja justo el elemento que se pide a continuación.

Contra el oráculo, en instancias chicas al azar:

```{python continue}
rng = random.Random(9)
por_encima = {"Belady": 0, "LRU": 0, "FIFO": 0}
N = 3000
for _ in range(N):
    kk = rng.randint(2, 4)
    s = [rng.randrange(kk + rng.randint(1, 3)) for _ in range(rng.randint(5, 14))]
    o = fallos_optimos(s, kk)
    for nombre, regla in (("Belady", belady), ("LRU", lru), ("FIFO", fifo)):
        por_encima[nombre] += fallos(s, simular(s, kk, regla)) > o
for nombre, c in por_encima.items():
    print(f"{nombre:7} {c:5} de {N} sucesiones por encima del óptimo")
```

Belady nunca queda por encima. Ahora hay que demostrarlo, y aquí el intercambio de la
sección 5 no alcanza. Si en un óptimo cambiamos un desalojo para que coincida con
Belady, la caché queda con un elemento distinto, y todos los pedidos siguientes se
atienden sobre otra caché. No hay una pareja vecina que se cambie sin tocar nada más.

## 8. Planificaciones reducidas

Para seguir una transformación así hace falta un modelo un poco más general. Una
**planificación** para la sucesión $x_1, \dots, x_m$ es una sucesión de contenidos de la
caché $C_0 = \emptyset, C_1, \dots, C_m$, donde $C_t$ es lo que hay después de atender
el pedido $t$. Tiene que cumplir dos cosas: $x_t \in C_t$ y $|C_t| \le k$. Su costo es
el número de **cargas**, los elementos que entran: $\sum_t |C_t \setminus C_{t-1}|$.

Este modelo deja traer un elemento que nadie pidió. Una planificación es
**reducida** si no lo hace: cuando $x_t$ ya está, no cambia
nada, y cuando no está, lo trae y, si la caché está llena, desaloja exactamente uno.
Las reglas de la sección 7 producen planificaciones reducidas, y en una reducida las
cargas son exactamente los fallos.

Traer algo antes de que se pida nunca ayuda. Lo necesitamos porque la sección 9
produce, en un caso, una planificación no reducida.

**Lema 4.** Para toda planificación $S$ existe una reducida $\bar S$ con a lo sumo
tantas cargas.

*Demostración.* Construimos $\bar S$ pedido a pedido, mirando a $S$. Si $x_t$ está en
la caché de $\bar S$, no se hace nada. Si no está, se trae, y si la caché está llena se
desaloja un elemento que **no esté en $C_t$**, la caché de $S$ en ese instante. Ese
elemento existe: si los $k$ elementos de $\bar S$ estuvieran todos en $C_t$, como $x_t$
también está en $C_t$ y no en $\bar S$, $C_t$ tendría $k + 1$ elementos.

Ahora le asignamos a cada carga de $\bar S$ una carga distinta de $S$. Supongamos que
$\bar S$ trae $x$ en el pedido $t$. Sea $s < t$ el último instante en que $\bar S$
desalojó $x$, o $s = 0$ si nunca lo tuvo. En el instante $s$, $x \notin C_s$: si $s = 0$
porque $C_0$ está vacía, y si no porque $\bar S$ solo desaloja lo que $S$ no tiene. En
el instante $t$, $x \in C_t$, porque $S$ atiende el pedido de $x$. Entonces $S$ cargó
$x$ en algún instante del intervalo $(s, t]$, y esa es la carga que le asignamos. Dos
cargas de $x$ en $\bar S$ tienen intervalos disjuntos, porque entre una y otra $\bar S$
tuvo que desalojar $x$, así que la asignación nunca repite una carga de $S$. $\square$

El código hace la misma construcción, y la probamos con planificaciones que traen
elementos al azar sin que se pidan.

```{python continue}
def cargas(C):
    previa, total = frozenset(), 0
    for c in C:
        total += len(c - previa)
        previa = c
    return total

def reducir(seq, C, k):
    """La construcción del Lema 4: desaloja solo lo que la otra no tiene."""
    R, salida = frozenset(), []
    for t, x in enumerate(seq):
        if x not in R:
            if len(R) == k:
                fuera = sorted(R - C[t])
                assert fuera                    # existe, por el Lema 4
                R = R - {fuera[0]}
            R = R | {x}
        salida.append(R)
    return salida

def planificacion_rara(seq, k, universo, rng):
    """Válida pero no reducida: a veces trae un elemento que nadie pidió."""
    c, C = frozenset(), []
    for x in seq:
        for y in ([rng.choice(universo)] if rng.random() < 0.3 else []) + [x]:
            if y not in c and len(c) == k:
                c = c - {rng.choice(sorted(c))}
            c = c | {y}
        C.append(c)
    return C

rng = random.Random(4)
bajan = 0
for _ in range(2000):
    kk = rng.randint(2, 4)
    universo = list("abcdefg"[:kk + rng.randint(1, 3)])
    s = [rng.choice(universo) for _ in range(rng.randint(5, 16))]
    C = planificacion_rara(s, kk, universo, rng)
    R = reducir(s, C, kk)
    assert all(x in r and len(r) <= kk for x, r in zip(s, R))
    assert cargas(R) == fallos(s, R) <= cargas(C)
    bajan += cargas(R) < cargas(C)
print("planificaciones reducidas: 2000;  con menos cargas que la original:", bajan)
```

## 9. La transformación

Este es el corazón del capítulo. La idea es la de la sección 5, pero la medida que
decrece es otra: el número de pedidos iniciales en que una planificación óptima
coincide con Belady. Escribimos $S_B$ para la planificación de Belady.

**Lema 5.** Sea $S$ una planificación reducida que coincide con $S_B$ en los primeros
$j$ pedidos, es decir, con la misma caché después de cada uno. Existe una planificación
reducida $S'$ que coincide con $S_B$ en los primeros $j + 1$ pedidos y no tiene más
fallos que $S$.

*Demostración.* Sea $C$ la caché común después del pedido $j$ y sea $x = x_{j+1}$. Si
$x \in C$, las dos son reducidas y no hacen nada; si $x \notin C$ y la caché no está
llena, las dos lo traen sin desalojar; si está llena y las dos desalojan el mismo
elemento, coinciden. En esos tres casos basta $S' = S$.

Queda el caso interesante: la caché está llena, $S_B$ desaloja un elemento $f$ y $S$
desaloja otro, $e \ne f$. Después del pedido $j + 1$, la caché de $S$ tiene $f$ donde
la de $S_B$ tiene $e$, y en todo lo demás son iguales. Construimos $S'$ así: en los
primeros $j + 1$ pedidos hace lo mismo que $S_B$, y a partir de ahí **imita a $S$**
mientras se pueda, de modo que su caché sea la de $S$ con $e$ en lugar de $f$. Miremos
qué puede pasar en cada pedido posterior $y$, hasta el primero que obligue a hacer
algo distinto.

- **$y$ no es $e$ ni $f$, y está en la caché de $S$.** Entonces también está en la de
  $S'$, que difiere solo en $e$ y $f$. Las dos aciertan.
- **$y$ no es $e$ ni $f$, y $S$ falla y desaloja un $z \ne f$** (la caché está llena
  desde el pedido $j + 1$, y una reducida la mantiene llena). $S'$ también falla y
  desaloja el mismo $z$, que tiene. Siguen difiriendo solo en $e$ y $f$, con las mismas
  cargas.
- **$y$ no es $e$ ni $f$, y $S$ falla y desaloja $f$.** $S'$ desaloja $e$. Las dos
  cachés quedan **iguales**, y desde aquí $S'$ hace exactamente lo que $S$.
- **$y = e$.** $S$ no tiene $e$ y falla; desaloja algún $z$. Si $z = f$, la caché de $S$
  queda igual a la de $S'$, que tenía $e$ y acierta: $S'$ tiene un fallo menos. Si
  $z \ne f$, $S'$ desaloja también $z$ y **trae $f$**, aunque nadie lo pidió: las dos
  cachés quedan iguales, y las dos hicieron una carga. Desde aquí $S'$ hace lo que $S$.
- **$y = f$.** Este caso no puede ocurrir antes que el anterior, y es el único lugar
  donde la demostración usa que Belady eligió el más lejano. $S_B$ desalojó $f$ porque, entre los elementos de la caché, era el
  de próximo pedido más lejano. Como $e$ estaba en esa caché, el próximo pedido de $e$
  viene antes que el de $f$, o ninguno de los dos se vuelve a pedir. Así que la
  sucesión pide $e$ antes de pedir $f$, y en ese momento $S'$ ya se igualó con $S$.

Si nunca llega ninguno de los dos eventos que igualan las cachés, $S'$ imita a $S$
hasta el final con las mismas cargas. En todos los casos $S'$ tiene a lo sumo tantas
cargas como $S$, y coincide con $S_B$ en los primeros $j + 1$ pedidos.

Falta un detalle: en el subcaso $z \ne f$, $S'$ trajo $f$ sin que se pidiera, y no es
reducida. La reducimos con el Lema 4. La construcción de esa demostración no cambia los
primeros $j + 1$ pedidos, porque en ellos $S'$ ya es reducida: en cada fallo, el único
elemento de la caché reducida que no está en la de $S'$ es justamente el que $S'$
desalojó. El resultado es reducida, coincide con $S_B$ en $j + 1$ pedidos y no tiene
más cargas, que en una reducida son los fallos. $\square$

**Teorema.** La regla de Belady minimiza el número de fallos.

*Demostración.* Sea $S^*$ una planificación con el mínimo de cargas. Por el Lema 4 hay
una reducida con a lo sumo tantas, que también es óptima. Coincide con $S_B$ en los
primeros 0 pedidos. Aplicando el Lema 5 $m$ veces, se llega a una planificación que
coincide con $S_B$ en los $m$ pedidos, es decir, a $S_B$ misma, sin haber aumentado
nunca las cargas. Entonces $S_B$ tiene a lo sumo tantas cargas como $S^*$, y como es
reducida, sus cargas son sus fallos. Toda regla que solo trae lo que se pide, y desaloja
solo cuando hace falta, produce una planificación reducida, así que ninguna tiene menos fallos que Belady. $\square$

La medida que decrece es la cantidad de pedidos en que el óptimo **no** coincide
todavía con Belady. A diferencia de la sección 5, un paso no cambia dos piezas: rehace
la planificación desde el pedido $j + 1$ hasta que las dos cachés se igualan.

El código hace la construcción, con un `assert` en el caso imposible, sobre la
planificación de LRU de la sección 7.

```{python continue}
def transformar(seq, S, k):
    """El Lema 5. Devuelve S′ antes de reducir, S′ reducida, el primer pedido j
    donde S y Belady difieren, el pedido donde las cachés se igualan, e y f."""
    previa = frozenset()
    for j in range(len(seq)):
        B = previa | {seq[j]}
        if seq[j] not in previa and len(previa) == k:
            B = (previa - {belady(seq, j, previa, None, None)}) | {seq[j]}
        if B != S[j]:
            break
        previa = B
    else:
        return S, S, None, None, None, None
    e, f = next(iter(previa - S[j])), next(iter(previa - B))
    Sp, igual = list(S[:j]) + [B], len(seq)
    for t in range(j + 1, len(seq)):
        if igual < len(seq):
            Sp.append(S[t])
            continue
        assert seq[t] != f, "f pedido antes que e"
        if seq[t] == e or f not in S[t]:        # las dos cachés quedan iguales
            Sp.append(S[t])
            igual = t
        else:
            Sp.append((S[t] - {f}) | {e})
    return Sp, reducir(seq, Sp, k), j, igual, e, f

Sp, Sr, j, igual, e, f = transformar(seq, H_lru, k)
print(f"difieren en el pedido {j + 1}: Belady desaloja {f}, LRU desaloja {e}")
print(f"las cachés se igualan en el pedido {igual + 1}, que pide {seq[igual]}")
print("cargas: S =", cargas(H_lru), "  S′ =", cargas(Sp), "  S′ reducida =", cargas(Sr))
```

```{python continue echo=false output=asis}
print(G.transformacion(seq, k, H_lru, Sp, j - 1, igual + 2, e, f,
      ident="golosos-transformacion",
      pie="Un paso del Lema 5 sobre la sucesión de la figura anterior, desde el "
          "pedido 4. S es la planificación de LRU y S′ la que construye la "
          "demostración: coincide con Belady en el pedido 5 y desde ahí imita a S "
          "con e en lugar de f (en naranja). En el pedido 7 llega e, S lo trae "
          "desalojando f, S′ acierta y las dos cachés quedan iguales."))
```

En la @fig-golosos-transformacion se ve el caso $y = e$ con $z = f$. LRU desalojó $b$
en el pedido 5 y Belady desalojó $c$. En el pedido 7 se pide $b$: LRU lo tiene que traer, y al hacerlo desaloja justo $c$,
así que su caché queda igual a la de $S'$, que tenía $b$ y acierta. $S'$ ahorró una
carga, de 10 a 9.

Ahora la transformación entera, desde planificaciones de una regla que desaloja al
azar hasta llegar a Belady, comprobando en cada paso las dos promesas del Lema 5.

```{python continue}
rng = random.Random(9)
pasos = 0
for _ in range(2000):
    kk = rng.randint(2, 4)
    s = [rng.randrange(kk + rng.randint(1, 3)) for _ in range(rng.randint(6, 16))]
    S = simular(s, kk, lambda *_: rng.choice(sorted(_[2])))   # desalojo al azar
    inicial = cargas(S)
    while True:
        _, S2, j, *_ = transformar(s, S, kk)
        if j is None:
            break
        assert cargas(S2) <= cargas(S)
        assert S2[:j + 1] == simular(s[:j + 1], kk, lambda *a: belady(s, *a[1:]))
        S, pasos = S2, pasos + 1
    assert S == simular(s, kk, belady) and cargas(S) == fallos_optimos(s, kk) <= inicial
print("pasos del Lema 5 comprobados:", pasos)
```

Una comprobación que pasa hay que intentar romperla. Si en `belady` se cambia `max`
por `min` (desalojar el de próximo pedido más cercano), salta el `assert` de "f pedido
antes que e": ese caso solo es imposible porque $f$ era el más lejano.

## 10. El error plantado: Belady con ventana

Nuestro Belady recorre la sucesión hacia adelante en cada fallo, $O(m)$ por elemento
de la caché. Un ahorro natural es mirar solo una **ventana** de $w$ pedidos: si un
elemento no aparece en ella, "se pide muy tarde" y da lo mismo cuál se desaloje.

```{python continue}
def belady_ventana(w):
    def regla(seq, t, cache, ultimo, entrada):
        def proximo_en_ventana(y):
            for s in range(t + 1, min(len(seq), t + 1 + w)):
                if seq[s] == y:
                    return s
            return t + 1 + w                       # "muy tarde"
        return max(sorted(cache), key=proximo_en_ventana)
    return regla

rng = random.Random(16)
for largo in (12, 200):
    peor = peor_lru = 0
    N = 400
    for _ in range(N):
        s = [rng.randrange(6) for _ in range(largo)]
        v = fallos(s, simular(s, 4, belady_ventana(16)))
        peor += v > fallos(s, simular(s, 4, belady))
        peor_lru += v > fallos(s, simular(s, 4, lru))
    print(f"k = 4, ventana 16, {largo:3} pedidos: {peor:3} de {N} por encima de Belady,"
          f" {peor_lru:3} por encima de LRU")
```

Con 12 pedidos no falla nunca, y no es suerte: la ventana de 16 cubre la sucesión
entera, así que la variante **es** Belady. Una batería de pruebas cortas contra el
oráculo, que es la única donde el oráculo cabe, no puede verlo. Con 200 pedidos al azar
falla en 1 sucesión de 400, porque con 6 elementos casi siempre todos vuelven dentro de
la ventana. Y la prueba que uno escribiría primero, "no hace más fallos que LRU", no lo
atrapa en ninguna.

La demostración dice dónde buscar. El único lugar donde usó que $f$ es el más lejano
fue en el caso $y = f$: la sucesión pide $e$ antes que $f$. La variante con ventana
rompe exactamente eso cuando hay dos elementos fuera de la ventana: desaloja el primero
en orden alfabético, que puede volver antes que el otro. Esa frase basta para construir
la entrada.

```{python continue}
roto = list("abcd") + list("cd") * 8 + ["a"] + list("cd") * 2 + ["b"]
print("a se pide en", roto.index("a", 1) + 1, " b en", roto.index("b", 2) + 1)
print("Belady:", fallos(roto, simular(roto, 3, belady)),
      "  con ventana 16:", fallos(roto, simular(roto, 3, belady_ventana(16))))
```

En el pedido 4, con $a$, $b$ y $c$ en la caché, la ventana ve a $c$ y no ve ni a $a$ ni
a $b$. Desaloja $a$, que se pide en la posición 21, y conserva $b$, que se pide en la
26. Es el caso $y = f$ que la demostración declaraba imposible. Con la regla de verdad
no lo es: un elemento fuera de la ventana no "se pide muy tarde", se pide en un instante
concreto que la variante decidió no mirar.

La demostración no solo dice que el algoritmo es correcto: dice **qué información
usa**. Belady compara los próximos pedidos de todos los candidatos, y una
implementación que deja de compararlos, aunque sea para los lejanos, ya no es la que se
demostró. El ejercicio 11 la acelera sin cambiar la regla.

## 11. En línea y fuera de línea

Las reglas que deciden solo con lo que ya pasó se llaman **en línea**. ¿Cuánto pierden
contra Belady?
Daniel Sleator y Robert Tarjan la respondieron en «Amortized efficiency of list update and
paging rules» (*Communications of the ACM* 28(2), 1985), el mismo año que los árboles
splay del capítulo 4. Con una caché del mismo tamaño $k$ para las dos reglas, su
Teorema 6 dice que en cualquier sucesión LRU hace a lo sumo $k$ veces los fallos de
Belady, más $k$. Su Teorema 5 dice que ninguna regla en línea garantiza un factor
menor: para cualquiera hay sucesiones arbitrariamente largas donde hace $k$ veces los
fallos de Belady.

La demostración del Teorema 5 es un adversario como los del capítulo 5, §5: con
$k + 1$ elementos en juego, pide siempre uno que la regla no tiene en la caché. Por eso supone que la regla no
usa azar, porque si no el adversario no sabría cuál pedir. El ejercicio 5 construye la
sucesión mala para LRU. Este estudio, el análisis competitivo, queda fuera de este libro.

Los golosos vuelven dos veces. El capítulo 10 dice cuándo un goloso es óptimo para
**cualquier** función de peso, sin inventar un intercambio para cada problema. El
capítulo 21 los usa sin ser óptimos, con una razón de aproximación demostrada.

## 12. La regla

Un goloso no se defiende con un ejemplo, ni con dos mil. Se demuestra encontrando una
medida que decrece mientras se transforma un óptimo cualquiera en la solución del
goloso, sin empeorarlo nunca. En el retraso máximo, la medida fueron las inversiones y
cada paso movía dos piezas vecinas. En la caché, la medida fue el largo del prefijo en
que el óptimo coincide con Belady, y cada paso reconstruía una planificación entera.

Si no aparece la medida, sospecha de la regla: en el Lema 3 la desigualdad compara
plazos, y un intercambio por holguras no la tiene. Y cuando aparece, mira qué hipótesis
usa cada paso, porque esa es la lista de lo que una implementación no puede cambiar.

## Resumen

- Un goloso se demuestra con un **argumento de intercambio**: transformar un óptimo
  en la solución del goloso sin empeorarlo, con una medida que decrece.
- **Retraso máximo:** el plazo más cercano es óptimo. La medida son las inversiones, y
  cambiar dos vecinas invertidas no mueve a ninguna otra tarea y no sube $L$.
- La regla puede ignorar las duraciones porque al cambiar dos vecinas la pareja ocupa
  el mismo intervalo (Lema 3), y los empates en el plazo no importan (Lema 1).
- **Caché fuera de línea:** desalojar el elemento de próximo pedido más lejano (Belady)
  minimiza los fallos. Su demostración rehace planificaciones enteras, y el Lema 4
  quita las cargas que nadie pidió.
- El paso clave es que $f$ no puede pedirse antes que $e$, porque $f$ era el más
  lejano. Belady con ventana rompe exactamente ese paso, y las pruebas cortas no lo
  ven.
- A toda regla en línea que no usa azar se le puede forzar un factor $k$ contra
  Belady, y LRU no pierde más que eso, salvo un término $k$ (Sleator y Tarjan, 1985).

## Ejercicios

1. **[traza]** Seis tareas tienen duraciones $t = (3, 2, 1, 4, 3, 2)$ y plazos
   $d = (6, 8, 9, 9, 14, 15)$. Aplica el plazo más cercano, escribe el instante de
   terminación y el retraso de cada tarea y calcula $L$. ¿Cambia algo si desempatas las
   tareas 3 y 4 al revés?

2. **[entrada que rompe]** (a) Da una instancia de dos tareas donde la menor holgura
   no es óptima. (b) Demuestra que no existe ninguna instancia de dos tareas, sin
   empates en las duraciones ni en las holguras, donde la más corta primero y la menor
   holgura fallen a la vez.

3. **[demostración]** Demuestra que, si se permite dejar la máquina ociosa entre
   tareas, existe un horario óptimo sin tiempo ocioso. ¿Qué hipótesis del modelo usas?
   El ejercicio 9 la quita.

4. **[traza]** Con una caché de 3 y la sucesión $1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$,
   simula a mano Belady y LRU. Cuenta los fallos de cada uno y señala el primer pedido
   donde desalojan elementos distintos.

5. **[modelar]** Para cada $k$, construye sucesiones arbitrariamente largas donde LRU
   falla en todos los pedidos y el cociente entre sus fallos y los de Belady se acerca
   a $k$. Demuéstralo y mídelo con el código del capítulo para $k = 2, 4, 8$.

6. **[demostración]** Hay $n$ intervalos $[s_i, f_i)$ y se quiere elegir la mayor
   cantidad posible sin que dos se solapen. La regla golosa es tomar el que termina
   primero, descartar los que se solapan con él y repetir. Demuestra por intercambio
   que es óptima. ¿Cuál es la medida que decrece?

7. **[demostración]** Cada tarea tiene una duración $t_i$ y un peso $w_i > 0$, y se
   quiere minimizar $\sum_i w_i f_i$. Demuestra con un intercambio de vecinas que es
   óptimo atenderlas en orden decreciente de $w_i / t_i$ (la regla de Smith). Explica
   qué papel juegan los empates.

8. **[entrada que rompe]** Para dar un cambio con monedas de valores $\{1, 3, 4\}$ y el
   menor número de monedas, la regla golosa toma siempre la moneda más grande que cabe.
   Encuentra el menor monto donde falla. Intenta un argumento de intercambio para esta
   regla y di en qué paso se rompe.

9. **[cambio de hipótesis]** Ahora cada tarea tiene además un instante de liberación
   $r_i$ antes del cual no puede empezar. La regla es: cada vez que la máquina queda
   libre, atender, entre las tareas ya liberadas, la de plazo más cercano. Da una
   instancia donde no es óptima. ¿Qué lema de las secciones 4 y 5 deja de valer, y por
   qué?

10. **[modelar] ★** Hay $n$ clases, cada una un intervalo de tiempo, y se quieren
    repartir en el mínimo de aulas sin que dos clases de una misma aula se solapen. La
    **profundidad** de la instancia es el mayor número de intervalos que contienen a un
    mismo instante. Demuestra que ningún reparto usa menos aulas que la profundidad.
    Diseña un goloso que use exactamente esa cantidad, demuéstralo e impleméntalo en
    $O(n \log n)$.

11. **[implementar y medir]** Implementa Belady en $O(m \log k)$ para $m$ pedidos,
    con el próximo pedido de cada posición precalculado y la caché en un montículo con cambio de clave.
    Compara sus fallos con los de `simular` con `belady` y mide los tiempos de los
    dos para $m = 10^3, 10^4, 10^5$.
