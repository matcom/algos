# Cook-Levin: SAT y 3-SAT {#chap-cook-levin}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_17.py
import figuras_17 as F17
```

El capítulo 16 dejó una receta para demostrar que un problema es NP-completo, y le
faltaba un paso: un primer problema que ya se sepa NP-completo. Ese primero no puede
salir de una reducción desde otro. Este capítulo lo construye desde la definición de
NP, con una idea que cabe en una frase: una computación es una tabla, y para saber si
una tabla es correcta basta mirarla por una ventana de dos filas y tres columnas. Con
eso se escribe, para cada problema de NP y cada entrada, una fórmula que es
satisfacible si y solo si la respuesta es sí. Después partimos las cláusulas largas en
cláusulas de tres literales, y 3-SAT queda como punto de partida de los capítulos 18
y 19.

## 1. El primer problema NP-completo

La receta del capítulo 16, §7 dice en su paso 2 "elige un $A$ que ya sepas
NP-completo". El lema 3 de ese capítulo transfiere la NP-completitud con una reducción
$A \le_p B$. Transfiere, pero no crea.

Para el primero hay que reducirle **todos** los problemas de NP, que no se parecen
entre sí. Lo único que tienen en común es la definición: cada uno tiene, por el
capítulo 16, §4, una máquina de Turing no determinista que lo decide en tiempo
polinomial. La demostración toma una máquina y una entrada cualesquiera y produce una
fórmula con la misma respuesta.

Stephen Cook lo hizo en 1971, en "The Complexity of Theorem-Proving Procedures"
(*Proceedings of the Third Annual ACM Symposium on Theory of Computing*, pp. 151–158).
Su teorema 1 toma una máquina no determinista $M$ que acepta en tiempo polinomial y,
para cada entrada $w$, construye una fórmula $A(w)$ en forma normal conjuntiva que es
satisfacible si y solo si $M$ acepta $w$. Leonid Levin publicó un resultado del mismo
tipo en 1973, para problemas de búsqueda, en "Universal Sequential Search Problems"
(*Problemy Peredachi Informatsii* 9(3), pp. 115–116).

La máquina de Turing del capítulo 1, §3 vuelve aquí. Allí la descartamos para medir
costos, porque cambia los exponentes. Aquí la elegimos por una propiedad que la RAM no
tiene: es **local**. Un paso cambia a lo sumo tres símbolos contiguos de su
descripción, y eso es lo que hace que la fórmula tenga tamaño polinomial.

## 2. Máquinas de Turing no deterministas

Una **máquina de Turing no determinista** tiene estados $Q$ con un inicial $q_0$ y uno
de aceptación $q_a$, un alfabeto de cinta $\Gamma$ que contiene la entrada y el blanco
$\_$, y una función de transición $\delta$ que a cada par (estado, símbolo leído) le
asigna un **conjunto** de movidas $(q', b, d)$: pasar a $q'$, escribir $b$ y moverse
una celda en la dirección $d$. En la determinista ese conjunto tiene a lo sumo un
elemento. Tres convenciones simplifican la tabla:

- La máquina se **detiene** cuando $\delta(q, a)$ es vacío, y **acepta** si se detuvo
  en $q_a$, que no tiene transiciones.
- En la primera celda, una movida a la izquierda deja el cabezal donde está.
- $M$ **decide** $L$ en tiempo $t(n)$ si toda sucesión de elecciones se detiene en a lo
  sumo $t(n)$ pasos, y $w \in L$ si y solo si **alguna** termina en $q_a$.

El ejemplo del capítulo acepta las cadenas sobre $\{0, 1\}$ con algún 1, adivinando
cuál. Recorre la entrada hacia la derecha, y en cada 1 elige entre seguir o pasar a
$q_a$. Si llega al blanco sin haber elegido, se detiene en $q_0$ y no acepta.

```{python continue}
BORDE, BLANCO = "#", "_"
ESTADOS, CINTA = ["q0", "qa"], ["0", "1", BLANCO]
SIMBOLOS = ESTADOS + CINTA + [BORDE]               # el alfabeto C de la tabla (§3)
DELTA = {("q0", "0"): [("q0", "0", +1)],
         ("q0", "1"): [("q0", "1", +1), ("qa", "1", +1)]}

def sucesores(c, delta=DELTA):
    """Configuraciones que siguen a c en un paso (c es una tupla, ver §3)."""
    p = next(k for k, s in enumerate(c) if s in ESTADOS)   # columna del estado
    q, a = c[p], c[p + 1]                                   # a: el símbolo leído
    movidas = delta.get((q, a), [])
    if not movidas:
        return [c]                         # detenida: en la tabla la fila se repite
    salida = []
    for q2, b, d in movidas:
        if d == +1:
            if c[p + 2] != BORDE:          # si saliera de la fila, no es un paso
                salida.append(c[:p] + (b, q2) + c[p + 2:])
        elif c[p - 1] == BORDE:            # en la primera celda no se mueve
            salida.append(c[:p] + (q2, b) + c[p + 2:])
        else:
            salida.append(c[:p - 1] + (q2, c[p - 1], b) + c[p + 2:])
    return salida

def inicial(w, t):
    """La configuración inicial, en una fila de t + 4 columnas."""
    return (BORDE, "q0") + tuple(w) + (BLANCO,) * (t + 1 - len(w)) + (BORDE,)

def arbol(w, t):
    """El árbol de cómputo: {nodo: (paso, configuración)} y las aristas."""
    nodos, aristas, nivel = {0: (0, inicial(w, t))}, [], [0]
    for paso in range(1, t + 1):
        siguiente = []
        for v in nivel:
            c = nodos[v][1]
            for c2 in ([] if sucesores(c) == [c] else sucesores(c)):
                nodos[len(nodos)] = (paso, c2)
                aristas.append((v, len(nodos) - 1))
                siguiente.append(len(nodos) - 1)
        nivel = siguiente
    return nodos, aristas

nodos, aristas = arbol("0110", 4)
for v in nodos:
    if all(u != v for u, _ in aristas):            # hojas: ramas detenidas
        paso, c = nodos[v]
        print(f"rama detenida en el paso {paso} en", [s for s in c if s in ESTADOS])
```

Una configuración es una tupla con la cinta y el estado metido justo antes de la
celda que lee el cabezal, entre dos bordes `#`; la §3 explica por qué. El árbol de la
@fig-cl-arbol es el que calculó el código para $w = 0110$. Hay tres ramas: dos aceptan,
en los pasos 2 y 3, y la tercera se detiene en el paso 4 sin aceptar. La máquina
acepta porque **alguna** rama acepta.

```{python continue echo=false output=asis}
print(F17.arbol(nodos, aristas, sucesores, ident="cl-arbol",
                pie="El árbol de cómputo de la máquina sobre 0110, calculado por el "
                    "código. Cada nodo dice el estado y la celda que lee el cabezal. En cada 1 "
                    "la máquina elige entre seguir y aceptar."))
```

El capítulo 16, §4 afirmó que esta definición de NP y la de los verificadores son la
misma. Veamos las dos direcciones.

**Proposición 1.** $L$ tiene un verificador polinomial si y solo si alguna máquina de
Turing no determinista lo decide en tiempo polinomial.

*Demostración.* Si $M$ decide $L$ en tiempo $t(n)$ polinomial, el certificado de $x$
es la sucesión de elecciones de una rama que acepta: $t(n)$ índices en conjuntos de
tamaño acotado por una constante de $M$, es decir $O(t(n))$ bits. El verificador
simula $M$ siguiendo esas elecciones y dice sí si termina en $q_a$. Si $x \notin L$,
ninguna rama acepta y ninguna sucesión de elecciones lo convence.

Al revés, sea $V$ un verificador con cota $p$ para el certificado. $V$ es un algoritmo
RAM, y por el capítulo 1, §3 hay una máquina de Turing determinista que hace lo mismo
en tiempo polinomial. La máquina no determinista escribe a la derecha de $x$ un $c$ de
a lo sumo $p(|x|)$ bits, eligiendo en cada paso entre escribir 0, escribir 1 o
terminar, y después corre esa simulación de $V$ sobre $(x, c)$. Alguna rama acepta si
y solo si algún $c$ convence a $V$, y todas terminan en tiempo polinomial. $\square$

## 3. La tabla de configuraciones

Fija $M$, que decide $L$ en tiempo $t(n)$, y una entrada $w$ de largo $n$. Escribimos
$t$ por $t(n)$. En $t$ pasos el cabezal, que empieza en la celda 1, visita a lo sumo
las celdas 1 a $t + 1$. Una configuración se escribe como la cadena
$\#\,u\,q\,v\,\#$: esas $t + 1$ celdas, el estado $q$ antes de la celda que lee el
cabezal, y un borde a cada lado. Son $t + 4$ símbolos. Si la rama se detiene antes del
paso $t$, la última fila se repite, y toda tabla tiene $(t + 1) \times (t + 4)$
celdas con símbolos de $C = Q \cup \Gamma \cup \{\#\}$, que en el ejemplo son seis.

```{python continue}
def tabla_que_acepta(w, t):
    """Las filas de una rama que acepta, o None si ninguna acepta."""
    nodos, aristas = arbol(w, t)
    padre = {v: u for u, v in aristas}
    for v, (paso, c) in nodos.items():
        if "qa" in c:
            camino = [v]
            while camino[-1] in padre:
                camino.append(padre[camino[-1]])
            filas = [nodos[u][1] for u in reversed(camino)]
            return filas + [filas[-1]] * (t + 1 - len(filas))
    return None

filas = tabla_que_acepta("0110", 4)
for i, f in enumerate(filas):
    print(f"fila {i}:", " ".join(f))
```

```{python continue echo=false output=asis}
print(F17.tabla(filas, ventana=(1, 1), ident="cl-tabla",
      pie="La tabla de la rama que acepta 0110 en el paso 2, con t = 4. La ventana "
          "marcada cubre el paso en que la máquina lee el primer 1 y elige aceptar: "
          "todo lo que cambió en ese paso está dentro de ella."))
```

La @fig-cl-tabla la dibuja. La pregunta cambia de forma: $M$ acepta $w$ si y
solo si existe una tabla en la que cada celda tiene un símbolo, la fila 0 es la
configuración inicial, cada fila sigue de la anterior con un paso de $M$ (o la repite
si estaba detenida), y $q_a$ aparece en alguna parte. Una fórmula describe una tabla
con una variable por celda y por símbolo. La tercera condición es la difícil.

## 4. Ventanas de 2 × 3

El primer intento es escribir "la fila $i + 1$ sigue de la fila $i$" de una vez. Esa
condición depende de $2(t + 4)|C|$ variables, y escrita en FNC sin pensar, con una
cláusula por cada asignación que la falsifica, cuesta hasta $2^{\Theta(t)}$ cláusulas.
La reducción sería exponencial.

Lo que la salva es mirar qué cambia en un paso. Con el estado $q$ en la columna $p$
leyendo el $a$ de la columna $p + 1$, una movida a la derecha cambia $q\,a$ por
$b\,q'$, y una a la izquierda cambia $x\,q\,a$ por $q'\,x\,b$, con $x$ el símbolo de la
columna $p - 1$. Cambian a lo sumo las columnas $p - 1$, $p$ y $p + 1$, y lo que se
escribe en ellas depende solo de lo que había en esas tres. El resto se copia.

Una **ventana** es un rectángulo de 2 filas y 3 columnas de la tabla. Es **legal** si
aparece, en las mismas columnas, en algún par formado por una configuración de $M$ y
una sucesora suya (o una configuración detenida y ella misma), en filas de cualquier
ancho. Hay a lo sumo $|C|^6$ ventanas, así que el conjunto de las legales es finito y
depende solo de $M$, no de $w$: la reducción lo lleva escrito como una tabla fija.
Para el ejemplo lo calculamos enumerando configuraciones con pocas celdas.

```{python continue}
def ventanas_legales(celdas=6, largo=3, delta=DELTA):
    legales = set()
    for cinta in itertools.product(CINTA, repeat=celdas):
        for p in range(celdas):
            for q in ESTADOS:
                c = (BORDE,) + cinta[:p] + (q,) + cinta[p:] + (BORDE,)
                for c2 in sucesores(c, delta):
                    for j in range(len(c) - largo + 1):
                        legales.add((c[j:j + largo], c2[j:j + largo]))
    return legales

LEGALES = ventanas_legales()
print("legales con 5, 6 y 7 celdas:", [len(ventanas_legales(k)) for k in (5, 6, 7)],
      "| iguales:", ventanas_legales(5) == LEGALES == ventanas_legales(7))
print("ventanas posibles:", len(SIMBOLOS) ** 6)
```

De 46 656 ventanas posibles, 182 son legales, y con 5, 6 o 7 celdas sale el mismo
conjunto. El experimento es este: fija una fila de arriba y prueba **todas** las filas
de abajo, quedándote con las que tienen todas sus ventanas legales.

```{python continue}
def ventanas_ok(arriba, abajo, legales=LEGALES, largo=3):
    return all((arriba[j:j + largo], abajo[j:j + largo]) in legales
               for j in range(len(arriba) - largo + 1))

arriba = ("#", "0", "q0", "1", "0", "#")
pasan = [b for b in itertools.product(SIMBOLOS, repeat=6) if ventanas_ok(arriba, b)]
print("pasan:", [" ".join(b) for b in pasan],
      "| son las sucesoras:", sorted(pasan) == sorted(sucesores(arriba)))
```

De las 46 656 filas candidatas pasan dos, y son las dos sucesoras: la que sigue
buscando y la que acepta. Un vistazo local decide una propiedad global de la fila.
Llamamos $W = t + 4$ al número de columnas, de 0 a $W - 1$.

**Lema 2** (de la ventana). Si la fila $i$ es una configuración con el estado en una
columna $p \le W - 4$ y todas las ventanas entre las filas $i$ e $i + 1$ son legales,
la fila $i + 1$ es una sucesora de la fila $i$, o la misma fila si estaba detenida.

*Demostración.* Hay tres clases de columnas.

*Lejos del estado.* Sea $1 \le k \le W - 2$ con $|k - p| \ge 2$. La ventana de columnas
$k - 1, k, k + 1$ no tiene el estado arriba. Es legal, así que aparece en un par real
$(c, c')$, y en $c$ el estado tampoco está en esas tres columnas, sino a distancia al
menos 2 de $k$. Un paso cambia solo las tres columnas alrededor del estado, así que
$c'$ tiene en $k$ lo mismo que $c$, y la fila $i + 1$ tiene en $k$ lo mismo que la
fila $i$.

*Los bordes.* Las columnas 0 y $W - 1$ tienen `#`. La ventana que contiene cada una
aparece en un par real, donde el `#` está en el extremo y no cambia. La fila $i + 1$
tiene `#` en esas columnas.

*La ventana centrada en el estado*, de columnas $p - 1, p, p + 1$, que existe porque
$1 \le p \le W - 4$. Arriba tiene $x\,q\,a$. Es legal, así que aparece en un par real
$(c, c')$ en el que el estado de $c$ está en el centro y lee $a$. Entonces $c'$ salió
de $c$ por una movida $\tau \in \delta(q, a)$, o es $c$ repetida si $\delta(q, a)$ es
vacío, y lo que $c'$ tiene en esas columnas depende solo de $x$, $q$, $a$ y $\tau$. La
fila $i$ tiene los mismos $x$, $q$ y $a$, así que la fila $i + 1$ tiene en esas
columnas lo que da aplicarle $\tau$. Con $p \le W - 4$, una movida a la derecha no
pisa el borde, y $\tau$ es un paso válido para la fila $i$.

Las columnas a distancia menor que 2 del estado son justo $p - 1$, $p$ y $p + 1$, así
que las tres clases cubren todo, y la fila $i + 1$ es la fila $i$ con $\tau$
aplicada. $\square$

El paso que todo el mundo se salta es por qué tres columnas y no dos. La movida a la
izquierda escribe $q'\,x\,b$, y una sola ventana tiene que ver $x$, $q$ y $a$ a la vez
para que el par real que la explica use la misma movida en las tres columnas. Con
ventanas de $2 \times 2$, dos ventanas vecinas pueden explicarse con movidas
distintas. Nuestra máquina solo va a la derecha y no lo muestra; el ejercicio 11 pide
una que sí.

## 5. Las cuatro familias de cláusulas

La fórmula tiene una variable $x_{i,j,s}$ por fila $i \in \{0, \dots, t\}$, columna
$j \in \{0, \dots, W - 1\}$ y símbolo $s \in C$, que dice "en la celda $(i, j)$ está
$s$". Son $(t+1)(t+4)|C|$ variables, y cuatro fórmulas:

- $\varphi_{\text{celda}}$: cada celda tiene **exactamente** un símbolo. Por celda, la
  cláusula "al menos uno", $\bigvee_{s \in C} x_{i,j,s}$, y las cláusulas "a lo sumo
  uno", $(\lnot x_{i,j,s} \lor \lnot x_{i,j,r})$ para cada par $s \ne r$.
- $\varphi_{\text{inicio}}$: la fila 0 es la configuración inicial. Una cláusula de un
  literal por columna: $x_{0,0,\#}$, $x_{0,1,q_0}$, $x_{0,2,w_1}$, y así.
- $\varphi_{\text{acepta}}$: una sola cláusula, $\bigvee_{i,j} x_{i,j,q_a}$, de
  $(t+1)(t+4)$ literales.
- $\varphi_{\text{mov}}$: para cada fila $i < t$ y columna $1 \le j \le W - 2$, la
  ventana de filas $i, i+1$ y columnas $j-1, j, j+1$ es legal.

La fórmula es $\varphi_w = \varphi_{\text{celda}} \land \varphi_{\text{inicio}} \land
\varphi_{\text{acepta}} \land \varphi_{\text{mov}}$. Las tres primeras ya están en
forma normal conjuntiva. La cuarta, escrita tal cual, dice "la ventana es la legal
número 1, o la número 2, o…", una disyunción de conjunciones de seis literales.

## 6. Paso a FNC

La herramienta de siempre es la distributividad: $(a \land b) \lor c$ es
$(a \lor c) \land (b \lor c)$. Sobre una disyunción de muchas conjunciones explota, y
el ejercicio 3 te pide una fórmula de tamaño $2n$ que sale con $2^n$ cláusulas. La
transformación de Tseitin, con variables nuevas, da tamaño lineal, y es el ejercicio 4.

Aquí no hace falta ninguna de las dos, por la misma razón que hizo funcionar la §4:
cada ventana depende de $6|C|$ variables, un número fijo, y una condición sobre un
número fijo de variables tiene una FNC de tamaño fijo. La más simple prohíbe las
ventanas ilegales de a una: para cada 6-tupla $(a_1, a_2, a_3, b_1, b_2, b_3)$ que no
es una ventana legal, la cláusula
$$\lnot x_{i,j-1,a_1} \lor \lnot x_{i,j,a_2} \lor \lnot x_{i,j+1,a_3} \lor
\lnot x_{i+1,j-1,b_1} \lor \lnot x_{i+1,j,b_2} \lor \lnot x_{i+1,j+1,b_3}.$$
Con $\varphi_{\text{celda}}$ forzando un símbolo por celda, la ventana es legal si y
solo si ninguna de estas cláusulas es falsa.

```{python continue}
C = len(SIMBOLOS)
print("cláusulas por ventana, una por 6-tupla ilegal:", C ** 6 - len(LEGALES))
```

Son 46 474 por ventana. Es una constante, porque no depende de $w$, pero una constante
no tiene por qué ser chica. Agrupando por la fila de arriba se hace mucho mejor. Si
ninguna ventana legal tiene arriba $(a_1, a_2, a_3)$, una cláusula de tres literales lo
prohíbe. Si las hay, la fila de abajo tiene que estar en un conjunto $B$: se pide que
cada posición de abajo tenga uno de los símbolos que aparecen ahí en $B$, que es una
implicación "si arriba está esto, abajo está una de estas cosas", y se prohíben de a una
las combinaciones de esos símbolos que no están en $B$.

```{python continue}
def clausulas_ventana(legales, arriba, abajo):
    """FNC de "la ventana es legal". arriba(k, s) y abajo(k, s) son los números de
    las variables de la columna k de la ventana con el símbolo s."""
    por_arriba = {}
    for a, b in legales:
        por_arriba.setdefault(a, set()).add(b)
    clausulas = []
    for a in itertools.product(SIMBOLOS, repeat=3):
        no_a = [-arriba(k, a[k]) for k in range(3)]       # "la fila de arriba no es a"
        B = por_arriba.get(a)
        if not B:
            clausulas.append(no_a)
            continue
        S = [sorted({b[k] for b in B}) for k in range(3)]
        for k in range(3):
            clausulas.append(no_a + [abajo(k, s) for s in S[k]])
        for b in itertools.product(*S):
            if b not in B:
                clausulas.append(no_a + [-abajo(k, b[k]) for k in range(3)])
    return clausulas

arriba = lambda k, s: 1 + k * C + SIMBOLOS.index(s)
abajo = lambda k, s: 1 + (3 + k) * C + SIMBOLOS.index(s)

def compara(legales):
    """6-tuplas que la FNC agrupada de `legales` clasifica distinto que LEGALES."""
    grupos = {}
    for c in clausulas_ventana(legales, arriba, abajo):
        grupos.setdefault(tuple(c[:3]), []).append(c[3:])   # por la fila de arriba
    errores = 0
    for t6 in itertools.product(SIMBOLOS, repeat=6):
        ciertas = {abajo(k, t6[3 + k]) for k in range(3)}
        resto = grupos[tuple(-arriba(k, t6[k]) for k in range(3))]
        fnc = all(any((abs(l) in ciertas) == (l > 0) for l in c) for c in resto)
        errores += fnc != ((t6[:3], t6[3:]) in LEGALES)
    return errores

K = len(clausulas_ventana(LEGALES, arriba, abajo))
print("cláusulas por ventana, agrupadas:", K)
print("6-tuplas mal clasificadas:", compara(LEGALES),
      "| si falta una ventana legal:", compara(LEGALES - {min(LEGALES)}))
```

Agrupadas son 446. La comprobación recorre las 46 656 6-tuplas y no encuentra
ninguna que la FNC agrupada y la lista de legales clasifiquen distinto. La última
cifra dice que esa comprobación puede fallar: con una ventana legal de menos en la
FNC, la tupla que falta sale mal clasificada. Sin ella no sabríamos si `compara` mira
algo.

## 7. El experimento

Para comprobar que la fórmula dice lo que debe hay que decidir si es satisfacible, y
usamos un DPLL corto: elige una variable, prueba sus dos valores, y tras cada
elección propaga las cláusulas que quedaron con un solo literal libre. En el peor caso
es exponencial, y no conocemos nada mejor, que es el punto del capítulo.

```{python continue}
class Formula:
    def __init__(self):
        self.ids, self.clausulas = {}, []

    def x(self, i, j, s):                  # número de la variable x_{i,j,s}
        return self.ids.setdefault((i, j, s), len(self.ids) + 1)

def cook_levin(w, t, como_mucho_uno=True):
    F, T, W = Formula(), t + 1, t + 4
    for i in range(T):                                          # φ_celda
        for j in range(W):
            F.clausulas.append([F.x(i, j, s) for s in SIMBOLOS])
            if como_mucho_uno:
                for s, r in itertools.combinations(SIMBOLOS, 2):
                    F.clausulas.append([-F.x(i, j, s), -F.x(i, j, r)])
    for j, s in enumerate(inicial(w, t)):                       # φ_inicio
        F.clausulas.append([F.x(0, j, s)])
    F.clausulas.append([F.x(i, j, "qa") for i in range(T) for j in range(W)])  # φ_acepta
    for i in range(T - 1):                                      # φ_mov
        for j in range(1, W - 1):
            F.clausulas += clausulas_ventana(
                LEGALES, lambda k, s: F.x(i, j - 1 + k, s),
                lambda k, s: F.x(i + 1, j - 1 + k, s))
    return F

def dpll(clausulas, n):
    """Una asignación {variable: bool} que satisface, o None."""
    afecta = {}                                    # literal -> cláusulas con su negado
    for c in clausulas:
        for l in c:
            afecta.setdefault(-l, []).append(c)
    valor = {}
    cierto = lambda l: None if abs(l) not in valor else valor[abs(l)] == (l > 0)

    def propaga(pendientes, rastro):
        while pendientes:
            l = pendientes.pop()
            if cierto(l) is not None:
                if cierto(l):
                    continue
                return False                       # conflicto
            valor[abs(l)] = l > 0
            rastro.append(abs(l))
            for c in afecta.get(l, []):
                if not any(cierto(m) for m in c):
                    libres = [m for m in c if cierto(m) is None]
                    if not libres:
                        return False               # cláusula falsa
                    if len(libres) == 1:
                        pendientes.append(libres[0])
        return True

    def busca():
        v = next((v for v in range(1, n + 1) if v not in valor), None)
        if v is None:
            return True
        for l in (v, -v):
            rastro = []
            if propaga([l], rastro) and busca():
                return True
            for u in rastro:
                del valor[u]
        return False

    unitarias = [c[0] for c in clausulas if len(c) == 1]
    return dict(valor) if propaga(unitarias, []) and busca() else None
```

La prueba: todas las cadenas de largo 1 a 4, con $t = n$, el tiempo de nuestra
máquina. Para cada una, $\varphi_w$ se decide con DPLL y se compara con la máquina; de
cada asignación se lee la tabla y se comprueba que es una rama.

```{python continue}
def lee_tabla(F, A, t):
    """En cada celda, los símbolos cuya variable es verdadera."""
    return [tuple("".join(s for s in SIMBOLOS if A[F.x(i, j, s)])
                  for j in range(t + 4)) for i in range(t + 1)]

probadas = 0
for n in range(1, 5):
    for w in map("".join, itertools.product("01", repeat=n)):
        F = cook_levin(w, n)
        A = dpll(F.clausulas, len(F.ids))
        assert (A is not None) == (tabla_que_acepta(w, n) is not None)
        if A is not None:
            R = lee_tabla(F, A, n)
            assert R[0] == inicial(w, n) and "qa" in sum(R, ())
            assert all(R[i + 1] in sucesores(R[i]) for i in range(n))
        probadas += 1
print("cadenas:", probadas, "| para n = 4:", len(F.ids), "variables,",
      len(F.clausulas), "cláusulas")
```

En las 30 cadenas, $\varphi_w$ es satisfacible exactamente cuando la máquina acepta,
y la tabla que se lee de cada asignación es una rama que acepta. La asignación **es**
el certificado. Para $n = 4$ ya son 240 variables y 11 353 cláusulas, para una máquina
de dos estados que corre cuatro pasos. ¿Cómo crece con $t$? Cada familia se cuenta.

```{python continue}
def tamano(t):
    celdas, ventanas = (t + 1) * (t + 4), t * (t + 2)
    return celdas * C, celdas * (1 + math.comb(C, 2)) + (t + 4) + 1 + ventanas * K

assert all(tamano(t) == (len(F.ids), len(F.clausulas))
           for t in range(1, 6) for F in [cook_levin("1" * t, t)])
ts = [2, 4, 8, 16, 32, 64, 128]
ingenua = lambda t: t * (t + 2) * (C ** 6 - len(LEGALES))
print("cláusulas en t = 128 sobre t = 64:", round(tamano(128)[1] / tamano(64)[1], 2),
      "| ingenua sobre agrupada en t = 128:", round(ingenua(128) / tamano(128)[1]))
```

```{python continue echo=false output=asis}
print(F17.tamanos(
    {"variables": [(t, tamano(t)[0]) for t in ts],
     "cláusulas": [(t, tamano(t)[1]) for t in ts],
     "ingenua": [(t, ingenua(t)) for t in ts]},
    ident="cl-tamanos",
    pie="Tamaño de la fórmula para la máquina del ejemplo contra los pasos t, contado "
        "por el código. Las tres rectas tienen pendiente 2. La FNC ingenua, una "
        "cláusula por ventana ilegal, es la misma recta subida un factor constante."))
```

La cuenta coincide con la fórmula construida para $t = 1, \dots, 5$. Al doblar $t$
de 64 a 128, las cláusulas se multiplican por 3,94, y en la @fig-cl-tamanos las tres
rectas tienen pendiente 2: la fórmula tiene $\Theta(t^2)$ cláusulas. La ingenua tiene
101 veces más en $t = 128$, y la reducción es correcta con cualquiera de las dos.

## 8. El teorema de Cook-Levin

**Teorema 3** (Cook, 1971; Levin, 1973). SAT es NP-completo.

*Demostración.* SAT está en NP por el capítulo 16, §4. Falta que sea NP-duro. Sea
$L \in NP$. Por la proposición 1, una máquina no determinista $M$ decide $L$ en tiempo
$t(n) \le c\,n^k + c$ con $c$ y $k$ constantes. La reducción manda $w$ a la $\varphi_w$
de la §5 con $t = c\,n^k + c$, con $\varphi_{\text{mov}}$ en FNC como en la §6.

*Tamaño y tiempo.* $|C|$ y $K$ dependen de $M$, no de $w$. La §7 contó
$(t+1)(t+4)|C|$ variables y $(t+1)(t+4)\left(1 + \binom{|C|}{2}\right) + (t+4) + 1 +
t(t+2)K$ cláusulas, todas de a lo sumo $\max(|C|, 6)$ literales salvo la de
$\varphi_{\text{acepta}}$, que tiene $(t+1)(t+4)$. Son $O(t^2)$ literales, cada uno de
$O(\log t)$ bits, y $\varphi_w$ mide $O(t^2 \log t)$ bits; se escribe en ese tiempo
más el de calcular $t$, que es un polinomio en $n$.

*Si $w \in L$, $\varphi_w$ es satisfacible.* Una rama acepta $w$ en $s \le t$ pasos.
Sus configuraciones, con la última repetida, forman una tabla de
$(t+1) \times (t+4)$, porque el cabezal no sale de las columnas (§3). Pon $x_{i,j,s}$
verdadera si y solo si la celda $(i, j)$ tiene el símbolo $s$. Hay un símbolo por
celda, la fila 0 es la inicial y la fila $s$ tiene $q_a$, así que se cumplen
$\varphi_{\text{celda}}$, $\varphi_{\text{inicio}}$ y $\varphi_{\text{acepta}}$. Cada
ventana entre dos filas consecutivas viene de un par real, y es legal por definición.

*Si $\varphi_w$ es satisfacible, $w \in L$.* Toma una asignación que la satisface. Por
$\varphi_{\text{celda}}$, cada celda tiene **exactamente** una variable verdadera, así
que la asignación describe una tabla. Este es el paso que todo el mundo se salta, y la
§9 muestra qué pasa si falta la mitad "a lo sumo uno". Por $\varphi_{\text{inicio}}$,
la fila 0 es la inicial, con el estado en la columna 1. Por inducción: si la fila $i <
t$ es una configuración de una rama con el estado en una columna $p \le i + 1 \le t =
W - 4$, por $\varphi_{\text{mov}}$ y el lema 2 la fila $i + 1$ es una sucesora o una
repetición, con el estado a lo sumo en la columna $i + 2$. Las filas $0$ a $t$ son una
rama de $M$ sobre $w$. Por $\varphi_{\text{acepta}}$, $q_a$ está en alguna celda
$(i, j)$, y como la fila $i$ es una configuración, su único estado es ese: la rama
llega a $q_a$, y $M$ acepta $w$. $\square$

## 9. El error plantado {#cook-levin-9-el-error-plantado}

La variante parece inofensiva: quitar de $\varphi_{\text{celda}}$ las cláusulas "a lo
sumo uno". Uno puede pensar que $\varphi_{\text{inicio}}$ ya fija la fila 0 y que las
ventanas fijan el resto. Probamos las mismas 30 cadenas.

```{python continue}
print("cláusulas 'a lo sumo uno' por celda:", math.comb(C, 2))
for n in range(1, 5):
    mal = [w for w in map("".join, itertools.product("01", repeat=n))
           if (dpll(cook_levin(w, n, como_mucho_uno=False).clausulas,
                    len(cook_levin(w, n).ids)) is not None)
           != (tabla_que_acepta(w, n) is not None)]
    print(f"n = {n}: {len(mal)} de {2 ** n} mal, en {mal}")

F = cook_levin("000", 3, como_mucho_uno=False)
A = dpll(F.clausulas, len(F.ids))
fila0 = [[s for s in SIMBOLOS if A[F.x(0, j, s)]] for j in range(3 + 4)]
print("fila 0:", fila0)
```

Ahorra 15 cláusulas por celda, y en cada largo da una sola respuesta equivocada: la
cadena de ceros, la única instancia no. Las instancias sí siguen bien, porque la
dirección "si $w \in L$, $\varphi_w$ es satisfacible" no usa lo que quitamos. Una batería que solo prueba cadenas aceptadas no ve el
error nunca, y una con cadenas de largo 10 al azar lo ve con probabilidad $1/1024$ por
cadena.

La última línea dice qué pasó: en la fila 0 hay celdas con varios símbolos a la vez, y
entre ellos un 1. La cláusula $x_{0,j,0}$ dice que en la celda hay un 0, no que no haya
otra cosa. Con un 1 de contrabando, las ventanas permiten leerlo y pasar a $q_a$. La
frase que lo anunciaba es "cada celda tiene exactamente una variable verdadera, así que
la asignación describe una tabla", la que parece demasiado obvia para escribirla, como
en el capítulo 16, §11.

## 10. 3-SAT

SAT es incómodo como punto de partida, porque sus cláusulas tienen cualquier largo.
**3-SAT** es SAT con cada cláusula de exactamente tres literales sobre tres variables
distintas, y vamos a reducirle SAT.

Primero se limpia: un literal repetido se escribe una vez, y una cláusula con $x$ y
$\lnot x$ se borra. Una de tres literales queda igual. Una de dos se rellena con una variable nueva: $(a \lor b)$ pasa a
$(a \lor b \lor y) \land (a \lor b \lor \lnot y)$, que es verdadera si y solo si
$a \lor b$ lo es, porque $y$ hace falsa una de las dos. La de un literal es el
ejercicio 5.

El caso interesante es la cláusula larga. El primer intento, partir
$(a \lor b \lor c \lor d)$ en $(a \lor b) \land (c \lor d)$, está mal: con solo $a$
verdadero, la original se cumple y la segunda mitad no. La partición pide un literal
verdadero en **cada** mitad, y la cláusula lo pide en **alguna**. Hace falta que una
mitad le diga a la otra "yo ya estoy cumplida", y eso es una variable nueva:
$(a \lor b \lor y) \land (\lnot y \lor c \lor d)$. Si el literal verdadero está en la
primera mitad, $y$ falsa cumple la segunda; si está en la segunda, $y$ verdadera cumple
la primera; si no hay ninguno, una exige $y$ y la otra $\lnot y$. Con $m > 4$ literales
se encadena con $m - 3$ variables nuevas, en $m - 2$ cláusulas:
$$(\ell_1 \lor \ell_2 \lor y_1) \land (\lnot y_1 \lor \ell_3 \lor y_2) \land \cdots
\land (\lnot y_{m-3} \lor \ell_{m-1} \lor \ell_m).$$

```{python continue}
def a_3sat(clausulas, n):
    """SAT -> 3-SAT. Las variables son 1..n; las nuevas se numeran desde n + 1."""
    salida = []
    def nueva():
        nonlocal n
        n += 1
        return n
    for c in clausulas:
        c = list(dict.fromkeys(c))                  # sin literales repetidos
        if any(-l in c for l in c):
            continue                                # tautología
        if len(c) == 1:
            y, z = nueva(), nueva()
            salida += [[c[0], s * y, r * z] for s in (1, -1) for r in (1, -1)]
        elif len(c) == 2:
            y = nueva()
            salida += [c + [y], c + [-y]]
        elif len(c) == 3:
            salida.append(c)
        else:
            y = nueva()
            salida.append([c[0], c[1], y])
            for l in c[2:-2]:
                y2 = nueva()
                salida.append([-y, l, y2])
                y = y2
            salida.append([-y, c[-2], c[-1]])
    return salida, n

larga = [1, -2, 3, 4, -5, 6]
partes, N = a_3sat([larga], 6)
valor = {1: False, 2: True, 3: False, 4: True, 5: True, 6: False,   # solo x4 cumple
         7: True, 8: True, 9: False}                                 # y1, y2, y3
lit = lambda l: valor[abs(l)] == (l > 0)
print("partes:", partes, "| cumplidas:", [any(map(lit, c)) for c in partes])
```

La @fig-cl-cadena muestra las 4 partes con la asignación del código: $x_4$ es el único
literal verdadero de la original, así que $y_1$ e $y_2$ son verdaderas para cumplir
las partes de antes y $y_3$ es falsa para cumplir la de después.

```{python continue echo=false output=asis}
print(F17.cadena(larga, partes, 6, lit, ident="cl-cadena",
      pie="La cláusula de seis literales partida por el código en cuatro de tres, con "
          "tres variables nuevas (borde naranja). Los literales verdaderos van "
          "rellenos: y₁ e y₂ cumplen las partes antes de x₄, y ¬y₃ la de después."))
```

**Teorema 4.** SAT $\le_p$ 3-SAT.

*Demostración.* La reducción aplica la construcción a cada cláusula, con variables
nuevas propias. Una cláusula de $m$ literales da a lo sumo $\max(m - 2, 4)$ cláusulas,
así que la salida tiene tamaño lineal. Como las variables nuevas de una cláusula no
aparecen en otra, basta ver, cláusula por cláusula, que una asignación de las
variables originales la cumple si y solo si se extiende a sus variables nuevas
cumpliendo todas sus partes. Los casos de 2 y 3 literales están arriba, y el de 1 es
el ejercicio 5. Queda la cadena, con $m \ge 4$.

*Si la asignación cumple la cláusula*, sea $\ell_r$ un literal verdadero. Pon $y_k$
verdadera para $k \le r - 2$ y falsa para $k \ge r - 1$. La parte que contiene a
$\ell_r$ se cumple. Una parte anterior contiene $y_k$ con $k \le r - 2$, que es
verdadera, y una posterior contiene $\lnot y_k$ con $k \ge r - 1$, que también. Es la
asignación del código, con $r = 4$.

*Si no la cumple*, todos los $\ell$ son falsos. La primera parte exige $y_1$, y la
parte $(\lnot y_k \lor \ell_{k+2} \lor y_{k+1})$ con $y_k$ verdadera exige $y_{k+1}$.
Por inducción $y_{m-3}$ es verdadera, y la última parte,
$(\lnot y_{m-3} \lor \ell_{m-1} \lor \ell_m)$, queda falsa. $\square$

El experimento comprueba algo más fuerte que la equisatisfacibilidad: que **cada**
asignación de las variables originales cumple $\varphi$ si y solo si alguna extensión
cumple la fórmula partida. Una variante rota, sin la última parte de la cadena, muestra
que la comprobación puede fallar.

```{python continue}
def malas(phi, psi, n, N):
    """Asignaciones de 1..n donde 'cumple phi' difiere de 'alguna extensión cumple psi'."""
    cumple = lambda F, a: all(any(a[abs(l)] == (l > 0) for l in c) for c in F)
    total = 0
    for bits in itertools.product([False, True], repeat=n):
        a = dict(enumerate(bits, 1))
        ext = any(cumple(psi, {**a, **dict(enumerate(e, n + 1))})
                  for e in itertools.product([False, True], repeat=N - n))
        total += cumple(phi, a) != ext
    return total

random.seed(17)
total = 0
for _ in range(300):
    n = random.randint(1, 5)
    phi = [[random.choice([1, -1]) * random.randint(1, n)
            for _ in range(random.randint(1, 6))] for _ in range(random.randint(1, 4))]
    psi, N = a_3sat(phi, n)
    assert all(len({abs(l) for l in c}) == 3 for c in psi)
    total += malas(phi, psi, n, N)
psi, N = a_3sat([[1, 2, 3, 4, 5]], 5)
print("300 fórmulas al azar:", total, "| rota:", malas([[1, 2, 3, 4, 5]], psi[:-1], 5, N),
      "de", 2 ** 5)
```

En 300 fórmulas al azar no hay ninguna asignación mal. La variante rota se equivoca
en una de 32, la que hace falsos los cinco literales: la dirección "no ⇒ no" otra vez,
como en la §9, y otra vez un solo caso la distingue.

Cook ya había hecho esta partición, en su forma dual. Su teorema 2 reduce las
tautologías en forma normal disyuntiva a las que tienen a lo sumo tres literales por
término (el conjunto que llama $D_3$), partiendo un término largo con un átomo nuevo
$P$, como nuestra $y$.

## 11. 3-SAT como punto de partida

**Corolario 5.** 3-SAT es NP-completo.

*Demostración.* 3-SAT está en NP, con la asignación como certificado. SAT es
NP-completo por el teorema 3, SAT $\le_p$ 3-SAT por el teorema 4, y el lema 3 del
capítulo 16 da el resto. $\square$

La receta del capítulo 16, §7 tiene ya su paso 2. El capítulo 18 reduce 3-SAT a
conjunto independiente con un triángulo por cláusula, y el 19 llega a ciclo
hamiltoniano y a suma de subconjuntos. El tres es lo que hace chicos los gadgets.

¿Por qué tres y no dos? El ejercicio 7 del capítulo 16 resuelve 2-SAT en tiempo lineal,
y Cook ya anotaba en 1971 que su $D_2$ se decide en tiempo polinomial con el
procedimiento de Davis y Putnam. Si la partición llegara a dos literales por cláusula,
el teorema 2 del capítulo 16 daría $P = NP$. El ejercicio 7 te pide encontrar dónde se
rompe.

3-SAT vuelve dos veces más. En el capítulo 20, la hipótesis del tiempo exponencial
(ETH) dice que 3-SAT no se resuelve en tiempo $2^{o(n)}$ con $n$ variables. En el
capítulo 21, una asignación al azar cumple en esperanza $7/8$ de las cláusulas, porque
una cláusula de tres variables distintas es falsa en uno solo de sus ocho casos.

## 12. La regla {#cook-levin-12-la-regla}

**Una fórmula solo dice lo que sus cláusulas prohíben.** La cláusula $x_{0,j,0}$
afirma que la celda tiene un 0 y no prohíbe nada más. "Exactamente uno" son dos
familias, y la que se olvida es "a lo sumo uno", porque ninguna instancia sí la
necesita. Se encuentra como dice el capítulo 16, §13: probando la reducción en las
instancias no.

Y la que hizo posible el teorema: **una condición global se vuelve una fórmula chica
cuando se puede comprobar en pedazos de tamaño fijo.** La fila entera no cabe en una
cláusula de tamaño constante, y la ventana sí.

## Resumen {#cook-levin-resumen}

- El primer NP-completo no sale de una reducción: hay que reducirle todo NP usando solo
  la definición.
- Una máquina no determinista acepta si alguna rama acepta. NP con máquinas y con
  verificadores es la misma clase: el certificado es la sucesión de elecciones.
- Una rama de $t$ pasos es una tabla de $(t+1) \times (t+4)$ con el estado metido en la
  fila.
- Un paso cambia a lo sumo tres columnas contiguas. Si todas las ventanas de
  $2 \times 3$ son legales, cada fila sigue de la anterior (lema 2). Con $2 \times 2$
  no alcanza.
- Cuatro familias: celda, inicio, acepta y movimiento. Cada ventana depende de un
  número fijo de variables, y su FNC tiene tamaño constante: 446 cláusulas en el
  ejemplo, o 46 474 sin agrupar.
- $\Theta(t^2)$ cláusulas, $O(t^2 \log t)$ bits. SAT es NP-completo (Cook, 1971;
  Levin, 1973).
- Sin "a lo sumo uno", la fórmula es satisfacible en instancias no. Una fórmula solo
  dice lo que sus cláusulas prohíben.
- SAT $\le_p$ 3-SAT partiendo una cláusula de $m$ literales en $m - 2$, con $m - 3$
  variables nuevas. 3-SAT es NP-completo; 2-SAT está en P.

## Ejercicios {#cook-levin-ejercicios}

1. Para una máquina con $|Q|$ estados y alfabeto de cinta $\Gamma$ que corre $t$
   pasos, y $K$ cláusulas por ventana, escribe el número exacto de variables, de
   cláusulas y de literales de $\varphi_w$, familia por familia. Comprueba tus cuentas
   contra las 240 variables y 11 353 cláusulas de la §7 para $t = 4$.

2. Diseña una máquina no determinista que acepte las cadenas sobre $\{0, 1\}$ con dos
   ceros seguidos, adivinando dónde empiezan. Escribe la tabla de una rama que acepta
   $1001$. Elige la ventana del paso en que la máquina adivina y muestra que es legal
   dando un par real (configuración y sucesora) donde aparece.

3. Muestra que pasar $(x_1 \land y_1) \lor \cdots \lor (x_n \land y_n)$ a FNC por
   distributividad da $2^n$ cláusulas. Después demuestra que **toda** FNC equivalente
   sobre las mismas $2n$ variables tiene al menos $2^n$ cláusulas. Pista: mira qué
   literales contiene una cláusula que la fórmula implica, y qué asignaciones hacen
   falsa la fórmula.

4. Un circuito booleano es un grafo dirigido acíclico de entradas y compuertas Y, O y
   NO, con una salida. CIRCUIT-SAT pregunta si alguna entrada hace verdadera la
   salida. Con una variable nueva por compuerta (la transformación de Tseitin, de
   1968), demuestra CIRCUIT-SAT $\le_p$ SAT con una fórmula de tamaño lineal en el
   circuito. Impleméntala y mide sus cláusulas sobre el circuito de la fórmula del
   ejercicio 3 para $n = 2, 4, \dots, 16$, contra las $2^n$ de la distributividad.

5. Aplica la §10 a $(x_1 \lor \lnot x_2 \lor x_3 \lor x_4 \lor \lnot x_5)$. Para una
   asignación en la que $x_3$ es el único literal verdadero, da una extensión que
   cumpla todas las partes y di si es única. Después rellena una cláusula de un
   literal $(\ell)$ con dos variables nuevas en cuatro cláusulas de tres literales y
   demuestra las dos direcciones. Por último, generaliza la partición a $k$-SAT con
   $k \ge 3$: ¿cuántas cláusulas y variables nuevas da una cláusula de $m$ literales?

6. Demuestra que 3-SAT sigue siendo NP-completo si cada variable aparece a lo sumo tres
   veces en la fórmula, permitiendo cláusulas de dos o tres literales. Pista: reemplaza
   las apariciones de una variable por copias distintas, y obliga a las copias a valer
   lo mismo con cláusulas de dos literales.

7. Intenta reducir 3-SAT a 2-SAT con la idea de la §10, partiendo $(a \lor b \lor c)$
   en cláusulas de dos literales con variables nuevas. Muestra dónde se rompe la
   demostración del teorema 4 y explica por qué no deberías esperar arreglarlo.

8. ★ En NAE-3SAT ("no todos iguales") una cláusula de tres literales se cumple si
   tiene al menos uno verdadero y al menos uno falso. Demuestra que es NP-completo.
   Antes, observa qué le pasa a una asignación que cumple una instancia si cambias el
   valor de todas las variables.

9. En EXACTAMENTE-UNO-3SAT una cláusula de tres literales se cumple si tiene
   exactamente uno verdadero. Demuestra que es NP-completo reduciendo desde 3-SAT, con
   un número fijo de cláusulas y variables nuevas por cláusula. Comprueba tu gadget con
   fuerza bruta sobre los 8 casos de la cláusula original.

10. Demuestra que SAT está en P si cada variable aparece a lo sumo dos veces en la
    fórmula. Separa el caso de dos apariciones con el mismo signo del de signos
    opuestos, y en el segundo junta las dos cláusulas en una sin la variable. Demuestra
    que eso no cambia la satisfacibilidad y que el proceso es polinomial.

11. Cambia en el código las ventanas de $2 \times 3$ por ventanas de $2 \times 2$
    (`ventanas_legales(largo=2)`). Muestra que para la máquina del ejemplo no cambia
    nada en la fila de la §4, y explica por qué. Después diseña una máquina de dos
    estados con una movida a la izquierda, y encuentra una fila de arriba y una de
    abajo que pasan todas las ventanas de $2 \times 2$ sin que la de abajo sea una
    sucesora. ¿Qué paso del lema 2 falla?
