# P, NP y reducciones {#chap-p-np}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_16.py
import figuras_16 as F16
```

Hasta aquí cada capítulo contestó la misma pregunta: cuánto cuesta resolver un
problema, y si se puede hacer mejor. Este capítulo empieza el Tema 3 con un problema
para el que nadie sabe contestarla, y cambia la pregunta por otra que sí se puede
responder: si este problema es *tan difícil como* aquel otro. Para hacerla precisa
hacen falta tres definiciones, P, NP y la reducción polinomial, y una receta para
escribir demostraciones con ellas. Los ejemplos son tres problemas de grafos que van a
resultar ser el mismo problema mirado de tres maneras. Al final del capítulo sabremos
que los tres son igual de difíciles. Que lo sean de verdad, es decir, que no se
resuelvan en tiempo polinomial salvo que pase algo muy improbable, lo demuestran los
capítulos 17 y 18.

## 1. Una pregunta que no sabemos contestar

En un grafo $G = (V, E)$, un **conjunto independiente** es un conjunto de vértices sin
ninguna arista entre ellos. El capítulo 11, §2 encontró el de peso máximo en un árbol
en tiempo $O(n)$, con dos valores por vértice. En un grafo cualquiera esa programación
dinámica no funciona, porque no hay un vértice cuya eliminación separe el problema en
partes que no se miran. Lo que queda es probar subconjuntos, $2^n$ en el peor caso, o
mejorar la base de la exponencial, que es lo que hace el capítulo 20.

No es el único caso. El viajante del capítulo 11, §8 bajó de $(n-1)!$ a $O(2^n n^2)$
con Held-Karp, y ahí se quedó. Para miles de problemas de este tipo, de rutas,
horarios, empaquetamientos y circuitos, nadie conoce un algoritmo polinomial, y nadie
ha demostrado que no exista.

Lo que sí se puede hacer es comparar problemas entre sí. En el capítulo 2, §8 usamos
una reducción para transferir una cota mínima de distinción de elementos a par más
cercano, y allí se anunció que el Tema 3 usa la misma herramienta: si $A$ es difícil y
$A$ se reduce a $B$, entonces $B$ es difícil. Este capítulo hace precisa esa frase
cuando "difícil" quiere decir "sin algoritmo polinomial".

## 2. Decisión y optimización

Los tres problemas del capítulo, tal como uno los encuentra, piden un óptimo:

- **Conjunto independiente.** El mayor conjunto de vértices sin aristas entre ellos.
  Su tamaño se escribe $\alpha(G)$.
- **Clique.** El mayor conjunto de vértices con todas las aristas entre ellos. Su
  tamaño es $\omega(G)$.
- **Vertex cover** (cubrimiento por vértices). El menor conjunto de vértices que toca
  todas las aristas: cada arista tiene al menos un extremo dentro. Su tamaño es
  $\tau(G)$.

La teoría de este capítulo trabaja con **problemas de decisión**, que contestan sí o
no. Cada problema de optimización tiene su versión de decisión con un umbral $k$:
"¿tiene $G$ un conjunto independiente de tamaño al menos $k$?", "¿un clique de tamaño
al menos $k$?", "¿un vertex cover de tamaño a lo sumo $k$?". Un problema de decisión
es, formalmente, el conjunto de las entradas cuya respuesta es sí, escritas como
cadenas de bits. Por eso se le llama también un **lenguaje**.

¿Se pierde algo al pasar a la decisión? En un sentido no. Si sabes optimizar, sabes
decidir: calculas $\alpha(G)$ y lo comparas con $k$. Y si sabes decidir, sabes el
valor óptimo, con una búsqueda binaria sobre $k$. La respuesta es monótona (si hay un
independiente de tamaño $k$, también hay uno de tamaño $k - 1$: quita un vértice), y
$\alpha(G)$ está entre $0$ y $n$.

```{python continue}
def grafo_al_azar(n, p):
    return [(u, v) for u, v in itertools.combinations(range(n), 2)
            if random.random() < p]

def es_independiente(S, aristas):
    S = set(S)
    return not any(u in S and v in S for u, v in aristas)

def decide_independiente(n, aristas, k):          # el oráculo: fuerza bruta
    return any(es_independiente(S, aristas)
               for S in itertools.combinations(range(n), k))

def alfa_por_decision(n, aristas):
    lo, hi, llamadas = 0, n, 0                    # con k = 0 la respuesta es sí
    while lo < hi:                                # invariante: lo ≤ α ≤ hi
        k = (lo + hi + 1) // 2
        llamadas += 1
        if decide_independiente(n, aristas, k):
            lo = k
        else:
            hi = k - 1
    return lo, llamadas

random.seed(16)
peor = {}
for _ in range(300):
    n = random.randrange(1, 11)
    E = grafo_al_azar(n, random.random())
    alfa = max(len(S) for r in range(n + 1)
               for S in itertools.combinations(range(n), r) if es_independiente(S, E))
    valor, llamadas = alfa_por_decision(n, E)
    assert valor == alfa
    peor[n] = max(peor.get(n, 0), llamadas)
print("300 grafos: la búsqueda binaria da α(G)")
for n in sorted(peor):
    cota = math.ceil(math.log2(n + 1))
    print(f"n = {n:>2}: a lo sumo {peor[n]} llamadas;  ⌈log₂(n+1)⌉ = {cota}")
```

El intervalo $[0, n]$ tiene $n + 1$ valores posibles y cada llamada descarta la mitad
de los que quedan, así que bastan $\lceil \log_2(n + 1) \rceil$ llamadas. En la tabla,
el máximo observado en los 300 grafos coincide con esa cota para cada $n$. Lo
importante es la forma: un número de llamadas logarítmico en $n$, cada una sobre la
misma entrada. Si la decisión se resolviera en
tiempo polinomial, el valor óptimo también.

Falta una tercera versión, la que de verdad se quiere en la práctica: **encontrar**
el conjunto, no solo su tamaño. También sale del oráculo de decisión, con un poco más
de ingenio, y es el ejercicio 4. Por eso la teoría se escribe para problemas de
decisión sin perder nada que importe: si la versión de decisión es difícil, la de
optimización también, porque resolver esta resuelve aquella.

## 3. La clase P

**Definición.** Un problema de decisión está en **P** si existe un algoritmo que lo
decide en tiempo $O(n^c)$ para alguna constante $c$, donde $n$ es el tamaño de la
entrada en bits.

Las palabras "en bits" son las del capítulo 1, §8, y pesan. Un grafo con $n$ vértices
se escribe con su matriz de adyacencia en $n^2$ bits, o con $n$ seguido de la lista de aristas, en
$O((n + m) \log n)$ bits. Las dos codificaciones son polinomiales una en la otra, así que da
igual cuál se use para decidir si algo es polinomial. Un número, en cambio, no es lo
mismo escrito en binario que en unario. La mochila con capacidad $W$ se resuelve en
$O(nW)$ con la tabla de Estructuras de Datos, pero $W$ se escribe con
$\log_2 W$ bits, y $nW$ es exponencial en esa cantidad. El capítulo 1 llamó a eso
**pseudopolinomial**. La mochila no está en P por esa tabla, y el ejercicio 10 mira qué
quiere decir esto para el problema de suma de subconjuntos.

La otra razón para elegir "polinomial" como frontera es que no depende del modelo. El
capítulo 1, §3 vio que una máquina de Turing con varias cintas que tarda $t$ pasos se
simula con una de una cinta en $O(t^2)$, y lo mismo pasa entre la máquina de Turing y
el modelo RAM con palabras de $O(\log n)$ bits: cada modelo razonable simula a los
otros con un costo polinomial. El exponente cambia de un modelo a otro, y la
pertenencia a P no.

Casi todo lo que hicimos en el Tema 2 está en P, una vez escrito como decisión:
"¿hay un camino de $s$ a $t$ de largo a lo sumo $L$?" (Dijkstra), "¿hay un flujo de
valor al menos $F$?" (capítulo 13), "¿tiene este grafo bipartito un emparejamiento de
tamaño $k$?" (Hopcroft-Karp, capítulo 13, §12), "¿se puede colorear este grafo con dos
colores?" (un BFS que alterna colores).

## 4. NP: soluciones que se comprueban rápido

Conjunto independiente tiene una propiedad que lo distingue de un problema
arbitrario: si alguien te dice "este conjunto $S$ es independiente y tiene $k$
vértices", lo compruebas tú solo, mirando las aristas. Encontrar $S$ parece difícil.
Comprobarlo es fácil.

**Definición.** Un problema de decisión $L$ está en **NP** si existen un polinomio $p$
y un algoritmo $V$, el **verificador**, que corre en tiempo polinomial en el tamaño de
sus dos argumentos, tales que para toda entrada $x$:
$$x \in L \iff \text{existe } c \text{ con } |c| \le p(|x|) \text{ tal que } V(x, c) = \text{sí}.$$
La cadena $c$ se llama **certificado** o testigo.

La definición tiene dos direcciones, y las dos importan. Si la respuesta es sí, hay
un certificado corto que convence al verificador. Si la respuesta es no, **ningún**
certificado lo convence, por astuto que sea. La cota $|c| \le p(|x|)$ también
importa: sin ella, el certificado podría ser la traza entera de un cómputo
exponencial, y la definición no diría nada.

Para conjunto independiente, el certificado es la lista de los $k$ vértices, que mide
$O(k \log n)$ bits, y el verificador comprueba que sean distintos, que sean al menos
$k$ y que ninguna arista tenga los dos extremos dentro. Eso cuesta $O(n + m)$ con un
arreglo de marcas. Otro ejemplo que vuelve en el capítulo 17 es **SAT**: dada una
fórmula booleana en forma normal conjuntiva, una conjunción de cláusulas que son
disyunciones de literales como $(x_1 \lor \lnot x_2 \lor x_3)$, ¿hay una asignación de
verdad que la haga verdadera? El certificado es la asignación, y el verificador evalúa
cada cláusula. Un tercero: "¿es $N$ compuesto?", con certificado un divisor $d$ con
$1 < d < N$, que se comprueba con una división.

El experimento compara el trabajo de buscar con el de comprobar. La búsqueda recorre
los subconjuntos de tamaño $k$. Para que no se detenga en el primer acierto, le damos
una instancia cuya respuesta es no: $k = \alpha(G) + 1$.

```{python continue}
def verifica_independiente(n, aristas, k, S):     # el verificador, O(n + m)
    marca = [False] * n
    for v in S:
        if not 0 <= v < n or marca[v]:
            return False                           # vértice inválido o repetido
        marca[v] = True
    return len(S) >= k and not any(marca[u] and marca[v] for u, v in aristas)

def alfa_lineal(n, aristas):                      # sube k mientras la respuesta es sí
    k = 0
    while k < n and decide_independiente(n, aristas, k + 1):
        k += 1
    return k

random.seed(4)
print(" n    m   α   subconjuntos (búsqueda)   aristas (verificador)")

for n in [8, 11, 14, 17]:
    E = grafo_al_azar(n, 0.3)
    alfa = alfa_lineal(n, E)
    S = next(S for S in itertools.combinations(range(n), alfa)
             if es_independiente(S, E))
    assert verifica_independiente(n, E, alfa, S)
    assert not verifica_independiente(n, E, alfa + 1, S)
    revisados = math.comb(n, alfa + 1)             # todos, porque ninguno sirve
    print(f"{n:>2} {len(E):>4} {alfa:>3} {revisados:>18} {len(E):>20}")
```

La columna de la búsqueda es $\binom{n}{\alpha + 1}$. Crece de forma exponencial
cuando $\alpha$ es una fracción fija de $n$. En estos grafos al azar $\alpha$ crece como
$\log n$, y entonces crece como $n^{\Theta(\log n)}$: no es exponencial, pero sí más
rápida que cualquier polinomio. La del verificador es $m$. Esa brecha entre buscar
y comprobar es todo lo que NP captura.

Dos inclusiones salen directo de la definición. **P ⊆ NP**: si $L$ se decide en tiempo
polinomial, el verificador ignora el certificado y decide $L$ él solo; el certificado
vacío sirve. **NP ⊆ EXP**, donde EXP son los problemas que se deciden en tiempo
$2^{\mathrm{poli}(n)}$: si $L \in NP$, se decide en tiempo $2^{p(n)} \cdot
\mathrm{poli}(n)$ probando todos los certificados de largo a lo sumo $p(n)$. Si P es
igual a NP es la pregunta abierta de la §12.

La N de NP viene de **no determinista**, no de "no polinomial". La definición original
usa máquinas de Turing no deterministas, que en cada paso pueden elegir entre varias
transiciones y aceptan si alguna sucesión de elecciones acepta. Las dos definiciones
son equivalentes: la sucesión de elecciones es un certificado, y una máquina no
determinista puede "adivinar" el certificado bit por bit y después correr el
verificador. Karp lo demuestra en las pp. 91–92 del artículo de 1972 que citamos en la
§12. El capítulo 17 usa la versión con máquinas.

Fíjate en la asimetría. Para "¿tiene $G$ un independiente de tamaño $k$?" el sí tiene
un certificado corto. Para "¿**no** tiene $G$ ningún independiente de tamaño $k$?",
nadie conoce uno: listar los $\binom{n}{k}$ subconjuntos con su arista culpable es
exponencial. Los complementos de los problemas de NP forman la clase **co-NP**, y el
ejercicio 8 la estudia.

## 5. Reducción polinomial

**Definición** (Karp, 1972). Un problema $A$ se **reduce en tiempo polinomial** a $B$,
y se escribe $A \le_p B$, si existe una función $f$ que se calcula en tiempo polinomial
y tal que para toda entrada $x$:
$$x \in A \iff f(x) \in B.$$

La función transforma cada instancia de $A$ en una de $B$ con la misma respuesta. Es
la misma forma que la reducción del capítulo 2, §8, con dos diferencias: el costo
permitido es polinomial y no lineal, y lo que se transfiere es la pertenencia a P, no
una cota en un árbol de decisión. Hay nociones más débiles. Cook, en 1971, permitió
llamar al algoritmo de $B$ muchas veces y combinar las respuestas, como hizo la
búsqueda binaria de la §2. Karp observa en la p. 92 de su artículo que su noción, con
una sola llamada y la misma respuesta, es más fuerte, y que la demostración de Cook la
cumple. Usamos la de Karp, que es la que usa el resto del libro.

**Lema 1.** Si $A \le_p B$ y $B \in P$, entonces $A \in P$.

*Demostración.* Sea $f$ la reducción, calculada en tiempo $q(n)$ con $q$ un polinomio,
y sea $M$ un algoritmo que decide $B$ en tiempo $r(n)$ con $r$ polinomio. Para decidir
si $x \in A$: calcula $y = f(x)$, corre $M$ sobre $y$ y devuelve su respuesta. Es
correcto porque $x \in A \iff y \in B$.

El costo es el paso que todo el mundo se salta. $M$ corre en tiempo $r(|y|)$, y la
cota es en el tamaño de **su** entrada, $y$, no de $x$. Hay que acotar $|y|$. Un
algoritmo que corre $q(|x|)$ pasos escribe a lo sumo una celda por paso en la máquina
de Turing, así que $|y| \le q(|x|)$. En la RAM del capítulo 1 se escribe una palabra de $O(\log |x|)$ bits por paso, y
$|y| = O(q(|x|) \log |x|)$ sigue siendo polinomial. Podemos tomar $r$ creciente, y el total es
$$q(|x|) + r(|y|) \le q(|x|) + r(q(|x|)),$$
que es un polinomio en $|x|$ porque la composición de polinomios es un polinomio. Si
$f$ pudiera producir una salida exponencial, el lema sería falso aunque $M$ fuera
lineal. $\square$

El mismo argumento, con el verificador de $B$ en lugar de $M$ y el mismo certificado,
demuestra que **si $A \le_p B$ y $B \in NP$, entonces $A \in NP$**.

```{python continue echo=false output=asis}
print(F16.direcciones(ident="np-direcciones",
      pie="Una reducción A ≤ₚ B es una tubería: f y un algoritmo para B forman un "
          "algoritmo para A. Solo valen las dos conclusiones de arriba; las de abajo "
          "son el error más común al usar una reducción."))
```

La @fig-np-direcciones lee el lema en las dos direcciones que valen. La de arriba es
la del Tema 2: si sabes resolver $B$, sabes resolver $A$. La segunda es su
contrarrecíproca: **si $A \notin P$ y $A \le_p B$, entonces $B \notin P$**. Es la que
usa el Tema 3. Las dos de abajo no valen, y la figura dice por qué: que $A$ sea fácil
no dice nada de $B$, porque cualquier problema fácil se reduce a cualquier problema con una
instancia sí y una no, resolviéndolo dentro de $f$ (el ejercicio 5 explota esto).

La relación $\le_p$ es **transitiva**: si $A \le_p B$ y $B \le_p C$, entonces
$A \le_p C$. La demostración es la del lema 1 con $f$ y $g$ en lugar de $f$ y $M$, con
el mismo paso sobre el tamaño de la salida intermedia, y es el ejercicio 3.

## 6. NP-duro y NP-completo

**Definición.** Un problema $B$ es **NP-duro** si $A \le_p B$ para todo $A \in NP$. Es
**NP-completo** si además $B \in NP$.

Un problema NP-duro es al menos tan difícil como cualquier problema de NP: un
algoritmo para él da, con una reducción delante, un algoritmo para cada uno de ellos.
Un problema NP-completo es además uno de ellos, y por eso los NP-completos son "los
más difíciles de NP".

**Teorema 2.** Si algún problema NP-completo está en P, entonces $P = NP$.

*Demostración.* Sea $B$ NP-completo y $B \in P$. Para cualquier $A \in NP$, $A \le_p B$
por ser $B$ NP-duro, y el lema 1 da $A \in P$. Así $NP \subseteq P$, y con la
inclusión $P \subseteq NP$ de la §4, $P = NP$. $\square$

Leído al revés: si $P \ne NP$, ningún problema NP-completo tiene un algoritmo
polinomial. Esa es la manera exacta en que una demostración de NP-completitud dice
"difícil". No demuestra que no exista un algoritmo polinomial. Demuestra que encontrar
uno resolvería de golpe todos los problemas de NP, que muchísima gente ha intentado
resolver por separado durante décadas.

Para demostrar que un problema es NP-duro no hace falta reducirle **todos** los de NP,
que son infinitos. Basta uno:

**Lema 3.** Si $A$ es NP-completo, $A \le_p B$ y $B \in NP$, entonces $B$ es
NP-completo.

*Demostración.* Para cualquier $C \in NP$, $C \le_p A$ porque $A$ es NP-duro, y
$A \le_p B$ por hipótesis. Por transitividad, $C \le_p B$. Entonces $B$ es NP-duro, y
como está en NP, es NP-completo. $\square$

El lema necesita un primer problema NP-completo para arrancar, y ese no puede salir de
una reducción desde otro. Es el teorema de Cook (1971): SAT es NP-completo. Su
demostración construye, para cada problema de NP y cada entrada, una fórmula que es
satisfacible si y solo si el verificador acepta algún certificado, y es el capítulo
17 entero.

"NP-duro" no quiere decir "dentro de NP". El **problema de la parada**, dado un
programa y una entrada, decidir si el programa termina, es NP-duro: a una fórmula
$\varphi$ le asociamos el programa "prueba las $2^n$ asignaciones de $\varphi$;
si alguna la satisface, termina; si no, entra en un ciclo infinito". Escribir ese
programa cuesta tiempo polinomial en el tamaño de $\varphi$, porque la fórmula va
copiada dentro y el resto del texto es fijo, y el programa termina si y solo si
$\varphi$ es satisfacible. Así SAT $\le_p$ PARADA. Pero la parada no es decidible, así
que no está en NP. Las versiones de optimización no son lenguajes, así que con la reducción de Karp no
pueden ser NP-duras. Se las llama NP-duras en un sentido más amplio, con la reducción
de Cook de la §5: un algoritmo polinomial para ellas daría uno para cada problema de NP.

## 7. La receta

Con el lema 3, demostrar que un problema nuevo $B$ es NP-completo tiene siempre la
misma forma. Son cuatro pasos, y una demostración a la que le falta uno no demuestra
nada.

1. **$B \in NP$.** Di qué es el certificado, cuánto mide, y qué hace el verificador en
   tiempo polinomial.
2. **Elige un $A$ que ya sepas NP-completo.** Hasta el capítulo 17, no tenemos
   ninguno. Después, SAT y 3-SAT, y luego todo lo que se vaya demostrando.
3. **Construye $f$ de instancias de $A$ a instancias de $B$** y demuestra que se
   calcula en tiempo polinomial. Esto incluye que la salida tenga tamaño polinomial.
4. **Demuestra las dos direcciones**: si $x \in A$ entonces $f(x) \in B$, y si
   $f(x) \in B$ entonces $x \in A$. La segunda se escribe muchas veces por
   contrarrecíproco: si $x \notin A$ entonces $f(x) \notin B$.

El paso 2 tiene la trampa de la dirección. Se reduce **desde** el problema conocido
**hacia** el nuevo: $A \le_p B$, con $A$ el difícil. Si haces la reducción al revés,
$B \le_p A$, demuestras que $B$ no es más difícil que $A$, lo que vale también para
problemas fáciles. El paso 4 tiene la trampa de la mitad: la dirección "sí ⇒ sí" suele
ser obvia, porque la construcción se pensó a partir de una solución, y la otra es la
que de verdad usa la estructura. La §11 muestra una reducción con la primera
dirección bien y la segunda mal.

Este capítulo no tiene todavía el paso 2. Lo que hace es practicar los pasos 1, 3 y 4
sobre tres problemas, y llegar a una conclusión condicionada: los tres están en P o
ninguno lo está.

## 8. El experimento

Antes de construir ninguna reducción, mira los tres números. El **complemento** de un
grafo $G$, que se escribe $\bar G$, tiene los mismos vértices y una arista entre $u$ y
$v$ exactamente cuando $G$ no la tiene. Calculamos $\alpha(G)$, $\omega(\bar G)$ y
$\tau(G)$ en **todos** los grafos con vértices $0, \dots, n - 1$ para $n \le 5$, que
son $2^{\binom{n}{2}}$ para cada $n$. Para que sea rápido, cada conjunto es una
máscara de bits y cada vértice guarda la máscara de sus vecinos.

```{python continue}
def complemento(n, aristas):
    E = {frozenset(e) for e in aristas}
    return [(u, v) for u in range(n) for v in range(u + 1, n)
            if frozenset((u, v)) not in E]

def vecinos(n, aristas):
    ady = [0] * n
    for u, v in aristas:
        ady[u] |= 1 << v
        ady[v] |= 1 << u
    return ady

def numeros(n, aristas):
    ady = vecinos(n, aristas)
    comp = vecinos(n, complemento(n, aristas))
    alfa, omega_comp, tau = 0, 0, n
    for S in range(1 << n):
        dentro = [v for v in range(n) if S >> v & 1]
        if all(ady[v] & S == 0 for v in dentro):         # independiente en G
            alfa = max(alfa, len(dentro))
        if all(S & ~comp[v] == 1 << v for v in dentro):  # clique en el complemento
            omega_comp = max(omega_comp, len(dentro))
        if all(S >> u & 1 or S >> v & 1 for u, v in aristas):  # cubre G
            tau = min(tau, len(dentro))
    return alfa, omega_comp, tau

grafos = iguales = suman_n = 0
for n in range(1, 6):
    pares = list(itertools.combinations(range(n), 2))
    for mascara in range(1 << len(pares)):
        E = [p for i, p in enumerate(pares) if mascara >> i & 1]
        a, w, t = numeros(n, E)
        grafos += 1
        iguales += a == w
        suman_n += a + t == n
print(f"{grafos} grafos con n ≤ 5")
print(f"α(G) = ω(complemento de G) en {iguales};  α(G) + τ(G) = n en {suman_n}")
```

Las dos igualdades se cumplen en los 1 099 grafos. Una búsqueda exhaustiva sobre
grafos de hasta 5 vértices no demuestra nada para 6, pero propone dos enunciados, y la
figura sugiere por qué son ciertos. Tomamos un grafo de 7 vértices, buscamos su
independiente máximo con el oráculo de la §2 y lo dibujamos tres veces.

```{python continue}
random.seed(309)
n7 = 7
E7 = grafo_al_azar(n7, 0.5)
a7 = alfa_lineal(n7, E7)
S7 = next(S for S in itertools.combinations(range(n7), a7) if es_independiente(S, E7))
print(f"{len(E7)} aristas, α = {a7}, un independiente máximo: {set(S7)}")
print(f"el resto, {set(range(n7)) - set(S7)}, tiene {n7 - a7} vértices")
```

```{python continue echo=false output=asis}
print(F16.tres_vistas(n7, E7, S7, ident="np-tres-vistas",
      pie=f"El mismo conjunto S = {set(S7)}, calculado por el código, tres veces. "
          "Ninguna arista de G une dos vértices de S; en el complemento, todas las "
          "aristas entre ellos están (en color). Los otros cuatro vértices tocan "
          "todas las aristas de G."))
```

En la @fig-np-tres-vistas, el panel del medio es el primero visto en negativo: lo que
en $G$ falta, en $\bar G$ está. Y en el tercero, cualquier arista que no tocara a
$V - S$ tendría los dos extremos en $S$, que es lo que el primer panel prohíbe. Las
dos secciones siguientes convierten esas dos frases en reducciones.

## 9. Independiente ≤ₚ clique, y vuelta

**Teorema 4.** CONJUNTO-INDEPENDIENTE $\le_p$ CLIQUE.

*Construcción.* Dada una instancia $(G, k)$ de conjunto independiente, con $G = (V, E)$
y $|V| = n$, la reducción devuelve $(\bar G, k)$. Para calcular $\bar G$ se recorren
los $\binom{n}{2}$ pares y se incluye cada uno que no está en $E$. Con un conjunto de
aristas con búsqueda en tiempo constante esperado o una matriz de adyacencia, cuesta
$O(n^2)$, y la salida tiene a lo sumo $\binom{n}{2}$ aristas: polinomial en la
entrada.

*Si $(G, k)$ es un sí, $(\bar G, k)$ es un sí.* Sea $S$ independiente en $G$ con
$|S| \ge k$. Para dos vértices distintos $u, v \in S$, $\{u, v\} \notin E$ porque $S$
es independiente, así que $\{u, v\}$ es arista de $\bar G$. Todos los pares de $S$
son aristas de $\bar G$: $S$ es un clique de tamaño al menos $k$.

*Si $(\bar G, k)$ es un sí, $(G, k)$ es un sí.* Sea $C$ un clique de $\bar G$ con
$|C| \ge k$. Para dos vértices distintos $u, v \in C$, $\{u, v\}$ es arista de $\bar G$,
**y toda arista de $\bar G$ es un par que no está en $E$**. Así ningún par de $C$ es
arista de $G$, y $C$ es independiente de tamaño al menos $k$. $\square$

La frase en negrita parece demasiado obvia para escribirla. La §11 muestra por qué
hay que escribirla.

La reducción en sentido contrario es la misma: el complemento del complemento es el
grafo original, así que $(G, k) \mapsto (\bar G, k)$ también reduce CLIQUE a
CONJUNTO-INDEPENDIENTE, con la demostración de arriba leída con los papeles cambiados.
La prueba contra el oráculo, en grafos al azar:

```{python continue}
def es_clique(S, aristas):
    E = {frozenset(e) for e in aristas}
    return all(frozenset(par) in E for par in itertools.combinations(S, 2))

def decide_clique(n, aristas, k):
    return any(es_clique(S, aristas) for S in itertools.combinations(range(n), k))

def independiente_a_clique(n, aristas, k):        # la reducción f
    return n, complemento(n, aristas), k

random.seed(9)
casos = 0
for _ in range(200):
    n = random.randrange(1, 9)
    E = grafo_al_azar(n, random.random())
    for k in range(n + 2):
        imagen = independiente_a_clique(n, E, k)
        assert decide_independiente(n, E, k) == decide_clique(*imagen)
        casos += 1
print(f"{casos} instancias (G, k): la respuesta se preserva en todas")
```

## 10. Independiente ≤ₚ vertex cover

**Lema 5.** En un grafo $G = (V, E)$, un conjunto $S \subseteq V$ es independiente si y
solo si $V - S$ es un vertex cover.

*Demostración.* Si $S$ es independiente, toma una arista $\{u, v\}$. No puede tener los
dos extremos en $S$, así que al menos uno está en $V - S$: $V - S$ la cubre. Al revés,
si $V - S$ es un vertex cover y $u, v \in S$, el par $\{u, v\}$ no puede ser arista,
porque una arista con los dos extremos en $S$ no tendría ninguno en $V - S$. $\square$

**Teorema 6.** CONJUNTO-INDEPENDIENTE $\le_p$ VERTEX-COVER.

*Construcción.* $(G, k) \mapsto (G, n - k)$, donde $n = |V|$. Copiar el grafo y restar
cuesta tiempo lineal en la entrada. Si $k > n$, la respuesta de conjunto independiente
es no, y $n - k < 0$ hace que la de vertex cover también lo sea, porque ningún
conjunto tiene tamaño negativo.

*Si $G$ tiene un independiente $S$ con $|S| \ge k$,* por el lema 5, $V - S$ es un
vertex cover con $|V - S| = n - |S| \le n - k$.

*Si $G$ tiene un vertex cover $T$ con $|T| \le n - k$,* por el lema 5 aplicado a
$S = V - T$, que cumple $V - S = T$, el conjunto $V - T$ es independiente, con
$|V - T| = n - |T| \ge k$. $\square$

Las dos direcciones son el mismo lema leído de un lado y del otro, y por eso aquí la
segunda no es más difícil que la primera. En las reducciones de los capítulos 18 y 19
esto ya no pasa: la vuelta exige leer una solución de $B$ y reconstruir con ella una
de $A$, y ese es el paso donde están los gadgets. La prueba contra el oráculo:

```{python continue}
def cubre(S, aristas):
    S = set(S)
    return all(u in S or v in S for u, v in aristas)

def decide_cover(n, aristas, k):
    return k >= 0 and any(cubre(S, aristas)
                          for S in itertools.combinations(range(n), min(k, n)))

def independiente_a_cover(n, aristas, k):
    return n, aristas, n - k

random.seed(10)
casos = 0
for _ in range(200):
    n = random.randrange(1, 9)
    E = grafo_al_azar(n, random.random())
    for k in range(n + 2):
        imagen = independiente_a_cover(n, E, k)
        assert decide_independiente(n, E, k) == decide_cover(*imagen)
        casos += 1
print(f"{casos} instancias (G, k): la respuesta se preserva en todas")
```

`decide_cover` prueba solo los conjuntos de tamaño exactamente $\min(k, n)$, y está
bien: si un conjunto de tamaño menor cubre, agregarle vértices lo sigue haciendo
cubrir, así que hay uno de tamaño exacto.

Con los teoremas 4 y 6 y sus inversos (la de clique es la misma construcción y la de
vertex cover a independiente es $(G, k) \mapsto (G, n - k)$ otra vez), los tres
problemas se reducen entre sí en cualquier orden, por transitividad. Junto con el
lema 1:

**Corolario 7.** CONJUNTO-INDEPENDIENTE, CLIQUE y VERTEX-COVER están los tres en P o
ninguno lo está. Y si uno es NP-completo, los tres lo son.

La segunda frase usa el lema 3 y que los tres están en NP, con el certificado de la
§4 o el mismo para clique y el complemento del conjunto para vertex cover (ejercicio
1). Fíjate en lo que el corolario **no** dice: no dice que ninguno sea difícil. Eso
llega en el capítulo 18, con una reducción desde 3-SAT a conjunto independiente.
Karp, en 1972, puso clique (por reducción desde SAT) y vertex cover (desde clique, con
el nombre *node cover*) en su lista de problemas completos. Conjunto independiente no
está en esa lista, aunque es el mismo problema por el teorema 4.

## 11. El error plantado

Una implementación del complemento que se ve correcta:

```{python continue}
def complemento_dudoso(n, aristas):
    return [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in aristas]
```

Pregunta si el par $(u, v)$ con $u < v$ está en la lista de aristas. Si las aristas
vienen escritas siempre con el menor primero, es el complemento. Si una arista viene
escrita $(5, 2)$, el par $(2, 5)$ "no está", y la función lo agrega al complemento
aunque sea una arista de $G$. El resultado es un supergrafo de $\bar G$.

Probamos la reducción con tres baterías. La primera planta una solución: elige un
conjunto $S$ de $k$ vértices y genera aristas al azar entre los demás pares, nunca
dentro de $S$, así que todas sus instancias son sí. La segunda usa grafos al azar con
las aristas que da `itertools.combinations`, siempre con el menor primero. La tercera
usa los mismos grafos con cada arista escrita en un orden al azar, como llegaría de un
archivo.

```{python continue}
def plantada(n, k, p):
    S = set(random.sample(range(n), k))
    return [(u, v) for u, v in itertools.combinations(range(n), 2)
            if not (u in S and v in S) and random.random() < p]

def desordenar(aristas):
    return [(v, u) if random.random() < 0.5 else (u, v) for u, v in aristas]

def batería(nombre, instancias):
    fallos_si = fallos_no = sies = noes = 0
    for n, E, k in instancias:
        bien = decide_independiente(n, E, k)
        dice = decide_clique(n, complemento_dudoso(n, E), k)
        if bien:
            sies += 1
            fallos_si += dice != bien
        else:
            noes += 1
            fallos_no += dice != bien
    print(f"{nombre:<13} sí: {fallos_si:>3} fallos de {sies:<5} "
          f"no: {fallos_no:>3} fallos de {noes}")

random.seed(11)
grafos8 = [grafo_al_azar(8, 0.5) for _ in range(150)]
batería("plantada", [(8, plantada(8, k, 0.5), k)
                     for k in range(1, 9) for _ in range(20)])
batería("ordenadas", [(8, E, k) for E in grafos8 for k in range(1, 9)])
batería("desordenadas", [(8, desordenar(E), k)
                         for E in grafos8 for k in range(1, 9)])
```

Las dos primeras baterías no encuentran nada. La primera no puede: el supergrafo de
$\bar G$ contiene a $\bar G$, así que un clique de $\bar G$ sigue siendo un clique, y
toda instancia sí sigue dando sí. La segunda no puede tampoco, porque con aristas
ordenadas la función calcula exactamente $\bar G$. La tercera falla en 204 de las 678
instancias no, casi una de cada tres, y en ninguna de las 522 instancias sí.

La demostración del teorema 4 lo anunciaba. La dirección "sí ⇒ sí" usa que **las
aristas que $\bar G$ debe tener están**, y el supergrafo las tiene todas. La dirección
"⇐" usa la frase en negrita: **toda arista del grafo construido es un par que no está
en $E$**. Esa es la frase que el código viola. Un clique del supergrafo puede usar una
arista que en realidad es de $G$, y entonces no es un independiente de $G$. El error
vive entero en la segunda dirección, la que la receta de la §7 obliga a escribir, y
que una batería construida a partir de soluciones nunca ejercita.

## 12. P contra NP

La pregunta de si $P = NP$ la plantearon Cook en 1971 y, de forma independiente,
Levin (el capítulo 17 cuenta los dos trabajos), y en 2000 el Clay Mathematics
Institute la puso entre sus siete Problemas del Milenio, con un millón de dólares
para cada solución. Sigue abierta. La @fig-np-clases muestra las dos posibilidades.

```{python continue echo=false output=asis}
print(F16.clases(ident="np-clases",
      pie="Los dos mundos posibles. Si P ≠ NP, los NP-completos son la parte de NP "
          "dentro de NP-duro, ninguno en P, y por Ladner hay problemas de NP que no "
          "son ni lo uno ni lo otro. Si P = NP, todo problema de NP es NP-completo "
          "salvo el lenguaje vacío y el de todas las cadenas, que ningún problema "
          "puede recibir por reducción."))
```

**Si $P \ne NP$**, el teorema 2 dice que ningún problema NP-completo está en P. Uno
podría pensar que entonces NP se parte en dos: lo que está en P y lo NP-completo.
Ladner demostró en 1975 que no: si $P \ne NP$, hay problemas en NP que no están en P y
no son NP-completos (Richard E. Ladner, "On the Structure of Polynomial Time
Reducibility", *Journal of the ACM* 22(1), 1975). El punto suelto de la figura es uno
de ellos. Ladner construye uno artificial, y de ningún problema natural se sabe que
lo sea, porque eso implicaría $P \ne NP$.

**Si $P = NP$**, el diagrama colapsa casi entero, con una excepción curiosa.

**Proposición 8.** Si $P = NP$, todo problema $B \in NP$ con al menos una instancia sí
$y_1$ y al menos una instancia no $y_0$ es NP-completo.

*Demostración.* $B \in NP$ por hipótesis. Sea $A \in NP$ cualquiera. Como $P = NP$, $A$
se decide en tiempo polinomial con un algoritmo $M$. La reducción es
$f(x) = y_1$ si $M$ acepta $x$, y $f(x) = y_0$ si no. Se calcula en tiempo polinomial,
porque $y_0$ e $y_1$ son constantes, y $x \in A \iff f(x) = y_1 \iff f(x) \in B$.
$\square$

Los dos problemas que quedan fuera son el vacío, $\emptyset$, que no tiene instancias
sí, y el de todas las cadenas, $\Sigma^*$, que no tiene instancias no. No son
NP-completos en ningún mundo: una reducción $f$ desde un problema con instancias sí a
$\emptyset$ tendría que mandar una instancia sí a una instancia sí de $\emptyset$, que
no existe.

Hay más consecuencias de $P = NP$: si la decisión es polinomial, encontrar un
certificado también (ejercicio 9). Pero no quiere decir "rápido en la práctica". Un
algoritmo en $n^{100}$ dejaría la pregunta resuelta y a los problemas tan intratables
como antes. Al revés, $P \ne NP$ no quiere decir que todas las instancias sean
difíciles: la frontera es sobre el peor caso. Los capítulos 20 a 23 viven en ese
espacio, entre lo que la teoría prohíbe y lo que sí se puede garantizar.

## 13. La regla

La regla del capítulo tiene dos partes.

**Una reducción se escribe desde lo que ya sabes difícil hacia lo nuevo.** $A \le_p B$
con $A$ el conocido. Al revés no demuestra nada sobre la dificultad de $B$, y la
@fig-np-direcciones lo tiene como sus dos filas rojas.

**Una reducción se demuestra en las dos direcciones, y se prueba también en las dos.**
La dirección "sí ⇒ sí" casi siempre se ve en la construcción, y la otra es la que se
olvida. Una batería de instancias sí prueba media demostración, como mostró el
complemento de la §11.

Lo que falta para que este capítulo diga "difícil" es un primer problema NP-completo.
El capítulo 17 lo construye desde la definición de NP, con el teorema de Cook-Levin, y
el capítulo 18 reduce 3-SAT a conjunto independiente. Con eso, el corolario 7 hace el
resto.

## Resumen

- Un problema de decisión contesta sí o no. Basta estudiarlos: el valor óptimo sale de
  $\lceil \log_2(n + 1) \rceil$ llamadas a la decisión, y el objeto óptimo también se
  puede recuperar.
- **P**: decidible en tiempo polinomial en el tamaño en bits. Un número cuenta por sus
  bits, no por su valor; $O(nW)$ es pseudopolinomial.
- **NP**: los sí tienen un certificado de tamaño polinomial que un verificador
  polinomial acepta, y los no no tienen ninguno. $P \subseteq NP \subseteq EXP$. La N es
  de no determinista.
- **$A \le_p B$**: $f$ polinomial con $x \in A \iff f(x) \in B$. Si $B \in P$, $A \in P$,
  porque la salida de $f$ tiene tamaño polinomial. Es transitiva.
- **NP-duro**: todo NP se reduce a él. **NP-completo**: NP-duro y en NP. Si uno está en
  P, $P = NP$. NP-duro incluye problemas indecidibles, como la parada.
- La receta: pertenencia a NP, un problema conocido, construcción polinomial, y las dos
  direcciones de la equivalencia.
- $S$ es independiente en $G$ si y solo si es clique en $\bar G$, si y solo si $V - S$
  es vertex cover. Los tres problemas están en P o ninguno lo está.
- Una reducción probada solo con instancias sí prueba media demostración.
- Si $P \ne NP$, hay problemas intermedios (Ladner). Si $P = NP$, todo NP es
  NP-completo salvo $\emptyset$ y $\Sigma^*$.

## Ejercicios

1. Da un certificado y un verificador polinomial para cada problema: clique ("¿tiene
   $G$ un clique de tamaño al menos $k$?"), ciclo hamiltoniano ("¿tiene $G$ un ciclo
   que pasa una vez por cada vértice?") y suma de subconjuntos ("dados enteros
   positivos $a_1, \dots, a_n$ y $T$, ¿hay un subconjunto que sume exactamente $T$?").
   Para cada uno, acota el tamaño del certificado en bits en función del tamaño de la
   entrada, y el tiempo del verificador.

2. Demuestra CLIQUE $\le_p$ VERTEX-COVER directamente, con una sola construcción y sin
   citar los teoremas 4 y 6: escribe $f$, su costo, y las dos direcciones de la
   equivalencia.

3. Demuestra que $\le_p$ es transitiva. Señala en tu demostración el paso equivalente al
   que el lema 1 marca como el que todos se saltan.

4. Tienes un oráculo que, dado $(G, k)$, contesta en un paso si $G$ tiene un vertex
   cover de tamaño a lo sumo $k$. Diseña un algoritmo que **encuentre** un vertex
   cover mínimo con un número polinomial de llamadas al oráculo y trabajo polinomial
   fuera de ellas. Demuestra que es correcto y cuenta las llamadas.

5. Un compañero quiere demostrar que el problema de 2-coloración es NP-completo, y
   escribe una reducción de 2-coloración a SAT. Supón, como demuestra el capítulo 17,
   que SAT es NP-completo, y que su reducción es correcta. ¿Qué demostró y qué no?
   Después, escribe una reducción de 2-coloración a CLIQUE que funcione y que no use
   ninguna propiedad de los cliques, y explica qué dice su existencia sobre las
   reducciones "hacia" un problema difícil.

6. Demuestra CICLO-HAMILTONIANO $\le_p$ CAMINO-HAMILTONIANO, donde el segundo pregunta
   si hay un camino que pasa una vez por cada vértice, entre dos vértices cualesquiera.
   Cuidado con la dirección "⇐": un camino hamiltoniano del grafo construido tiene que
   darte un ciclo del original.

7. ★ En 2-SAT cada cláusula tiene a lo sumo dos literales. Construye el **grafo de
   implicaciones**: un vértice por literal, y por cada cláusula $(a \lor b)$ las aristas
   $\lnot a \to b$ y $\lnot b \to a$; una cláusula $(a)$ cuenta como $(a \lor a)$. Demuestra que la fórmula es satisfacible si y solo
   si ninguna variable $x$ está en la misma componente fuertemente conexa que
   $\lnot x$, y deduce un algoritmo en tiempo lineal en el tamaño de la fórmula (las
   componentes fuertemente conexas se calculan con dos DFS, por el algoritmo de
   Kosaraju). Impleméntalo y pruébalo
   contra la fuerza bruta en fórmulas al azar de hasta 12 variables.

8. TAUTOLOGÍA pregunta si una fórmula booleana es verdadera con **toda** asignación.
   La clase **co-NP** contiene los problemas cuyo complemento está en NP. Demuestra
   que TAUTOLOGÍA está en co-NP, describiendo el certificado de que una fórmula **no**
   es tautología. Después, suponiendo que TAUTOLOGÍA es co-NP-completo (todo problema
   de co-NP se le reduce), demuestra que si TAUTOLOGÍA está en NP, entonces
   $NP = \text{co-NP}$.

9. Supón que $P = NP$. Sea $L \in NP$ con verificador $V$ y cota $p$ para el
   certificado. Demuestra que hay un algoritmo polinomial que, dada $x \in L$,
   **encuentra** un certificado $c$ con $V(x, c) = \text{sí}$. Pista: define un
   problema de decisión sobre pares $(x, w)$, con $w$ un prefijo, y demuestra que está
   en NP. ¿Qué parte de tu argumento usa la hipótesis, y qué parte valdría sin ella?

10. La suma de subconjuntos se resuelve en $O(nT)$ con una tabla de booleanos, y el
    capítulo 19 demuestra que es NP-completo. ¿Contradice esto que $P \ne NP$ sea
    posible? Mide el tamaño de la entrada en bits, explica cuál de las dos afirmaciones
    habla de qué, y di qué pasaría si los números se escribieran en unario.

11. Implementa tu algoritmo del ejercicio 4 con el oráculo de fuerza bruta de la §10, y
    cuenta las llamadas en grafos al azar con $n = 4, 6, 8, 10, 12$. Compara con la
    cota que demostraste. Busca un grafo que la alcance, o explica por qué no se puede.
