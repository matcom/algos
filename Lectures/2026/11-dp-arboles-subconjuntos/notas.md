# Programación dinámica sobre árboles y subconjuntos {#chap-dp-arboles-subconjuntos}

En Estructuras de Datos la programación dinámica trabajó siempre sobre una secuencia.
La subsecuencia común más larga mira dos prefijos, la mochila entera mira un prefijo
de los objetos y una capacidad, la subsecuencia creciente más larga mira dónde termina
la subsecuencia. En los tres casos el estado venía dado por la forma de la entrada, y
lo difícil era la recurrencia. Este capítulo trabaja con dos estructuras donde el
estado hay que **elegirlo**: un árbol y un conjunto. La tesis es una sola. El estado es
lo que una parte de la solución le tiene que contar al resto. Si cuenta menos de lo
necesario, la recurrencia es falsa. Si cuenta más, la tabla crece sin necesidad.

```{python echo=false output=asis}
import gc
import itertools
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_11.py
import figuras_11 as F11
```

## 1. El estado es la frontera

Una programación dinámica descansa en el **principio de optimalidad**, que Bellman
enunció en los años cincuenta: la mejor solución desde un estado se arma con las
mejores soluciones de los estados a los que pasa. Suele leerse como una propiedad del
problema ("el problema tiene subestructura óptima"), pero es una propiedad del estado
que uno eligió. El mismo problema la cumple con un estado y la viola con otro.

El ejemplo clásico de que falla es el camino simple más largo, que CLRS usa con un
grafo de cuatro vértices en ciclo: $q - r - t - s - q$. Busquemos por enumeración el
camino simple más largo entre tres pares de vértices.

```{python continue}
ciclo = {"q": "rs", "r": "qt", "s": "qt", "t": "rs"}

def mas_largo(a, b):
    """El camino simple más largo de a a b, probando todos."""
    mejor = None
    def extender(camino):
        nonlocal mejor
        u = camino[-1]
        if u == b:
            if mejor is None or len(camino) > len(mejor):
                mejor = list(camino)
            return
        for x in ciclo[u]:
            if x not in camino:
                extender(camino + [x])
    extender([a])
    return mejor

for a, b in [("q", "t"), ("q", "r"), ("r", "t")]:
    print(a, "->", b, ":", " ".join(mas_largo(a, b)))
```

El más largo de $q$ a $t$ pasa por $r$. Si el principio valiera con el estado "los
dos extremos", el tramo de $q$ a $r$ sería el más largo de $q$ a $r$ y el tramo de $r$
a $t$ el más largo de $r$ a $t$. Pero esos dos caminos usan cuatro vértices cada uno,
y pegarlos repite $s$ y $t$. Las dos mitades compiten por los mismos vértices, y el
estado "extremos" no dice cuáles gastó cada una. Para el camino **más corto** el
mismo estado sí sirve si las longitudes no son negativas, porque un camino más corto
nunca gana repitiendo vértices: si pegar dos tramos repite un vértice, el ciclo que
se forma se puede quitar sin alargar.

Así que un estado tiene que ser una **frontera**: lo que la parte resuelta le cuenta al
resto, de modo que el resto pueda decidir sin mirar dentro. Las dos secciones largas de
este capítulo buscan esa frontera en dos estructuras. En un árbol la frontera es un
vértice, y basta decir si está tomado. En una gira por ciudades la frontera es el
conjunto visitado y la ciudad donde uno está.

## 2. Conjunto independiente de peso máximo en un árbol

Tenemos un árbol de $n$ vértices con un peso positivo $w(v)$ en cada uno. Un conjunto
de vértices es **independiente** si no tiene dos vecinos, y queremos el de mayor peso.
En un grafo cualquiera este problema es NP-duro: el capítulo 18 lo demuestra
reduciendo desde 3-SAT. Lo que el árbol aporta es que quitar un vértice lo parte en
pedazos que no se tocan, y cada pedazo se puede resolver por su cuenta.

Enraizamos el árbol en el vértice 0 y escribimos $T_v$ para el subárbol que cuelga de
$v$. Como ejemplo usamos un árbol de 10 vértices hecho al azar: el padre de $i$ sale
entre los cuatro vértices anteriores, así que siempre $\text{padre}(i) < i$, y los
pesos van de 1 a 9. El oráculo prueba los $2^n$ subconjuntos.

```{python continue}
def arbol_al_azar(n, rng):
    """padre[0] = -1 y padre[i] < i para i > 0."""
    return [-1] + [rng.randrange(max(0, i - 4), i) for i in range(1, n)]

def hijos_de(padre):
    hijos = [[] for _ in padre]
    for v in range(1, len(padre)):
        hijos[padre[v]].append(v)
    return hijos

def fuerza_bruta(padre, w):
    n, mejor = len(padre), 0
    for m in range(1 << n):
        if any(m >> v & 1 and m >> padre[v] & 1 for v in range(1, n)):
            continue          # v y su padre están los dos: no es independiente
        mejor = max(mejor, sum(w[v] for v in range(n) if m >> v & 1))
    return mejor

rng = random.Random(24)
padre = arbol_al_azar(10, rng)
w = [rng.randint(1, 9) for _ in range(10)]
print("padres:", padre)
print("pesos: ", w)
print("óptimo por fuerza bruta:", fuerza_bruta(padre, w))
```

El primer intento que uno escribe guarda un solo número por vértice: $f(v)$, el peso
del mejor conjunto independiente de $T_v$. Para calcularlo, o tomamos $v$ o no lo
tomamos. Si no lo tomamos, cada hijo queda libre y sumamos los $f(c)$. Si lo tomamos,
ningún hijo puede entrar... y aquí el número se queda corto, porque $f(c)$ no dice
qué parte del mejor conjunto de $T_c$ sobrevive sin $c$. La salida desesperada es
quedarse solo con $v$, $f(v) = \max(w(v), \sum_c f(c))$, y tirar todo lo que hay
debajo de los hijos.

```{python continue}
def un_valor(padre, w):
    hijos, f = hijos_de(padre), [0] * len(padre)
    for v in reversed(range(len(padre))):     # los hijos antes que el padre
        f[v] = max(w[v], sum(f[c] for c in hijos[v]))
    return f[0]

print("un valor por vértice:", un_valor(padre, w))
```

Da 28 contra 35. En una estrella acertaría siempre, porque debajo de las hojas no hay
nada que tirar, y por eso un par de ejemplos a mano no lo delata. El fallo dice qué le
falta al estado: el subárbol de un hijo tiene que contarle al padre **dos** cosas, lo
mejor que puede hacer con $c$ dentro y lo mejor sin $c$.

## 3. Dos valores por vértice

Sean $\text{tom}(v)$ el peso del mejor conjunto independiente de $T_v$ que contiene a
$v$, y $\text{no}(v)$ el del mejor que no lo contiene. Si $v$ está, ningún hijo puede
estar, pero lo que hay debajo de cada hijo sí. Si $v$ no está, cada hijo elige lo que
le convenga:

$$
\text{tom}(v) = w(v) + \sum_{c \text{ hijo de } v} \text{no}(c),
\qquad
\text{no}(v) = \sum_{c \text{ hijo de } v} \max\big(\text{tom}(c), \text{no}(c)\big).
$$

En una hoja, $\text{tom} = w(v)$ y $\text{no} = 0$. La respuesta es
$\max(\text{tom}(0), \text{no}(0))$. Como cada padre tiene índice menor que sus hijos,
recorrer los vértices de mayor a menor calcula cada hijo antes que su padre. Para
reconstruir el conjunto se baja desde la raíz: un vértice entra si su padre no entró y
$\text{tom}(v) > \text{no}(v)$.

```{python continue}
def conjunto_independiente(padre, w):
    hijos = hijos_de(padre)
    tom, no = [0] * len(padre), [0] * len(padre)
    for v in reversed(range(len(padre))):
        tom[v] = w[v] + sum(no[c] for c in hijos[v])
        no[v] = sum(max(tom[c], no[c]) for c in hijos[v])
    return tom, no

def reconstruir(padre, tom, no):
    dentro = set()
    for v in range(len(padre)):               # los padres antes que los hijos
        libre = v == 0 or padre[v] not in dentro
        if libre and tom[v] > no[v]:
            dentro.add(v)
    return dentro

tom, no = conjunto_independiente(padre, w)
optimo = reconstruir(padre, tom, no)
print("tom:", tom)
print("no: ", no)
print("conjunto:", sorted(optimo), "peso", sum(w[v] for v in optimo))
```

Antes de demostrar nada lo probamos contra el oráculo. Usamos cuatro formas de árbol
(al azar, camino, estrella y altura 2) y dos clases de pesos (todos 1, o al azar de 1
a 9), con 100 árboles de hasta 10 vértices por batería. La función `baterias` queda
escrita para volver a usarla en §5.

```{python continue}
def forma(nombre, n, rng):
    if nombre == "azar":
        return [-1] + [rng.randrange(i) for i in range(1, n)]
    if nombre == "camino":
        return [-1] + list(range(n - 1))
    if nombre == "estrella":
        return [-1] + [0] * (n - 1)
    padre = [-1]                             # altura 2: cuelga de 0 o de un hijo de 0
    for i in range(1, n):
        padre.append(rng.choice([0] + [j for j in range(1, i) if padre[j] == 0]))
    return padre

def baterias(resolver, semilla=11, por_bateria=100):
    rng, fallos = random.Random(semilla), {}
    for nombre in ["azar", "camino", "estrella", "altura 2"]:
        for pesos in ["unos", "al azar"]:
            mal = 0
            for _ in range(por_bateria):
                n = rng.randint(1, 10)
                p = forma(nombre, n, rng)
                ws = [1] * n if pesos == "unos" else [rng.randint(1, 9) for _ in range(n)]
                mal += resolver(p, ws) != fuerza_bruta(p, ws)
            fallos[(nombre, pesos)] = mal
    return fallos

def dp(p, ws):
    t, n_ = conjunto_independiente(p, ws)
    return max(t[0], n_[0])

print("fallos de la DP por batería:", baterias(dp))
```

Ningún fallo en 800 árboles. La @fig-dp-arboles-dos-valores muestra el ejemplo con los
dos valores de cada vértice.

```{python continue echo=false output=asis}
print(F11.arbol_dos_valores(
    padre, w, tom, no, optimo,
    pie=f"El árbol de §2. Dentro de cada vértice, su peso; debajo, "
        f"tom | no. Los vértices marcados forman el conjunto que reconstruye el "
        f"código, de peso {sum(w[v] for v in optimo)}. La raíz vale "
        f"{tom[0]} | {no[0]}: el óptimo no la toma."))
```

Hay otra forma de escribir lo mismo con un solo número por vértice: si tomamos $v$,
saltamos a los nietos, $f(v) = \max\big(w(v) + \sum_{g \text{ nieto}} f(g),
\sum_{c} f(c)\big)$. Es correcta, y no contradice lo dicho: el número $f(g)$ de los
nietos sustituye al $\text{no}(c)$ de los hijos, porque $\text{no}(c)$ es justamente la
suma de los $f$ de los hijos de $c$. La información sigue siendo la misma, solo
cambia dónde se guarda.

## 4. La demostración

La recurrencia se apoya en un hecho sobre la estructura, que vale la pena aislar.

**Lema (la frontera).** Sea $v$ un vértice con hijos $c_1, \dots, c_k$. (a) Si $S$ es
un conjunto independiente de $T_v$, cada $S \cap T_{c_i}$ es independiente en
$T_{c_i}$. (b) Si $S_i$ es independiente en $T_{c_i}$ para cada $i$, la unión
$S_1 \cup \dots \cup S_k$ es independiente en $T_v$, y le sigue siéndolo al agregar $v$
siempre que ningún $c_i$ esté en su $S_i$.

*Demostración.* (a) Un subconjunto de un independiente es independiente, y las
aristas de $T_{c_i}$ son aristas de $T_v$. (b) Toda arista de $T_v$ está dentro de un
$T_{c_i}$ o es una de las aristas $v c_i$. No hay aristas entre dos subárboles de
hijos distintos, porque en un árbol eso cerraría un ciclo con $v$. Así que la unión
solo podría violar la independencia en una arista $v c_i$, y eso exige que $v$ y $c_i$
estén los dos. $\square$

**Teorema.** Para todo $v$, $\text{tom}(v)$ y $\text{no}(v)$ calculados por la
recurrencia son los pesos de los mejores conjuntos independientes de $T_v$ con $v$ y
sin $v$.

*Demostración.* Por inducción sobre la altura de $T_v$. En una hoja, el único
conjunto con $v$ es $\{v\}$ y el único sin $v$ es el vacío. Supongamos el enunciado
para los hijos de $v$.

*La fórmula de no(v).* Cota superior: sea $S$ el mejor independiente de $T_v$ sin
$v$. Por el lema (a), $S \cap T_{c_i}$ es independiente en $T_{c_i}$, y contiene o no
contiene a $c_i$. En el primer caso pesa a lo sumo $\text{tom}(c_i)$, en el segundo a
lo sumo $\text{no}(c_i)$, por hipótesis de inducción. En los dos, a lo sumo
$\max(\text{tom}(c_i), \text{no}(c_i))$. Como $v \notin S$, $S$ es la unión disjunta de
los $S \cap T_{c_i}$, y su peso es a lo sumo la suma. Alcanzabilidad: tomamos en cada
$T_{c_i}$ el mejor conjunto con $c_i$ o sin $c_i$, el que pese más. Por el lema (b) la
unión es independiente, no contiene a $v$ y pesa la suma.

*La fórmula de tom(v).* Igual, con dos cambios. Como $v \in S$, ningún $c_i$ está en
$S$, así que cada $S \cap T_{c_i}$ pesa a lo sumo $\text{no}(c_i)$; y para alcanzar la
cota se agrega $v$ a la unión de los mejores conjuntos sin $c_i$, que el lema (b)
permite. $\square$

El paso que se salta casi todo el mundo está en la fórmula de $\text{no}(v)$: cuando
$v$ no está, el hijo $c_i$ queda **libre**, y la cota superior tiene que contemplar los
dos casos para $S \cap T_{c_i}$. Ese es el paso que la sección siguiente rompe a
propósito.

*Costo.* Cada vértice aparece una sola vez como hijo, así que las dos sumas recorren,
sobre todo el árbol, $n - 1$ términos cada una. El algoritmo es $O(n)$ y la
reconstrucción también. Todo algoritmo tiene que mirar todos los pesos, porque
cambiar el peso de un vértice no mirado puede cambiar la respuesta, así que $O(n)$ es
lo mejor posible.

Una advertencia práctica. La versión recursiva, la que uno escribe primero, es más
corta, pero en Python cada nivel de recursión es un marco de pila y el intérprete
corta en una profundidad de 1 000 por omisión. Un camino es un árbol legítimo:

```{python continue}
def recursivo(v, hijos, w):
    t, n_ = w[v], 0
    for c in hijos[v]:
        tc, nc = recursivo(c, hijos, w)
        t, n_ = t + nc, n_ + max(tc, nc)
    return t, n_

camino = [-1] + list(range(2999))
try:
    recursivo(0, hijos_de(camino), [1] * 3000)
except RecursionError as e:
    print("RecursionError:", e)
print("iterativo:", dp(camino, [1] * 3000))
```

El recorrido iterativo funciona porque los padres tienen índice menor. Con un árbol
que llega como lista de aristas, ese orden se obtiene con un BFS desde la raíz, y se
recorre al revés.

## 5. El error plantado

La variante que sigue parece razonable y la escribe mucha gente: "si no tomo $v$, tomo
a sus hijos". Es decir, $\text{no}(v) = \sum_c \text{tom}(c)$. La pasamos por las
mismas ocho baterías de §3.

```{python continue}
def dp_con_error(p, ws):
    hijos = hijos_de(p)
    t, n_ = [0] * len(p), [0] * len(p)
    for v in reversed(range(len(p))):
        t[v] = ws[v] + sum(n_[c] for c in hijos[v])
        n_[v] = sum(t[c] for c in hijos[v])       # el error: el hijo no queda libre
    return max(t[0], n_[0])

for (nombre, pesos), mal in baterias(dp_con_error).items():
    print(f"{nombre:9s} pesos {pesos:8s} fallos: {mal:3d} de 100")
print("en el árbol de §2:", dp_con_error(padre, w), "en lugar de", dp(padre, w))
print("camino con pesos 5, 1, 1, 5:", dp_con_error([-1, 0, 1, 2], [5, 1, 1, 5]),
      "en lugar de", dp([-1, 0, 1, 2], [5, 1, 1, 5]))
```

Las estrellas, con o sin pesos, y los caminos sin pesos no la atrapan nunca. En una
estrella las dos únicas opciones razonables son la raíz o todas las hojas, y la
variante las compara. En un camino sin pesos, alternar es óptimo, y alternar es lo
único que la variante sabe hacer. En ninguno de los dos casos hace falta lo que la
variante prohíbe: dejar fuera a un vértice **y** a su hijo, para tomar algo más abajo.
Un camino con pesos ya lo necesita: con cuatro vértices de pesos $5, 1, 1, 5$, lo
mejor son los dos extremos, que dejan fuera a dos vecinos seguidos. Los árboles al
azar lo necesitan con frecuencia, como muestran sus baterías.

La demostración lo anunciaba. En la cota superior de $\text{no}(v)$ escribimos "contiene
o no contiene a $c_i$". La variante solo contempla el primer caso, así que su
$\text{no}(v)$ no es una cota superior y el teorema deja de valer. Una batería de
pruebas ve los casos que alguien pensó. La demostración obliga a enumerar los que
existen.

## 6. Re-enraizamiento: la pregunta desde todos los vértices

Cambiemos la pregunta. Para **cada** vértice $v$ queremos el peso del mejor conjunto
independiente de todo el árbol que contiene a $v$, y el del mejor que no lo contiene.
Es lo que haría falta, por ejemplo, para saber qué vértices están en algún óptimo.
Para la raíz ya lo tenemos: son $\text{tom}(0)$ y $\text{no}(0)$. Para otro vértice
$v$ bastaría enraizar el árbol en $v$ y repetir §3. Hacerlo para cada vértice cuesta
$n$ veces $O(n)$, o sea $O(n^2)$.

Cómo se le ocurre a uno hacerlo mejor: comparar el árbol enraizado en $0$ con el
enraizado en un hijo $v$ de la raíz. Casi todo es igual. Los subárboles de los hijos
de $v$ no cambiaron, y tampoco los de los otros hijos de la raíz. Lo único nuevo es
que $v$ tiene un hijo más, su antiguo padre, y debajo de él cuelga **todo el árbol
menos $T_v$**. Si conociéramos los dos valores de ese pedazo, $v$ se resolvería con
la fórmula de §3 como si fuera la raíz.

Llamamos $A_v$ al árbol menos $T_v$, enraizado en $\text{padre}(v)$, y
$\text{arr}_\text{tom}(v)$, $\text{arr}_\text{no}(v)$ a sus dos valores (con y sin
$\text{padre}(v)$). Por la arista que une a $v$ con su padre pasan entonces dos pares
de números: $(\text{tom}(v), \text{no}(v))$ **sube**, porque es lo que $T_v$ le
cuenta al padre, y $(\text{arr}_\text{tom}(v), \text{arr}_\text{no}(v))$ **baja**,
porque es lo que el resto del árbol le cuenta a $v$. Con los dos pares,

$$
\text{con}(v) = \text{tom}(v) + \text{arr}_\text{no}(v),
\qquad
\text{sin}(v) = \text{no}(v) + \max\big(\text{arr}_\text{tom}(v), \text{arr}_\text{no}(v)\big),
$$

que es la fórmula de §3 con $A_v$ como un hijo más de $v$. La frontera sigue siendo la
misma: un vértice y si está tomado. Lo único que cambió es de qué lado se mira.

## 7. Re-enraizamiento: fórmulas, demostración y costo

Falta calcular los valores que bajan. Sea $c$ un hijo de $v$. El árbol $A_c$ está
enraizado en $v$, y los hijos de $v$ en $A_c$ son los otros hijos de $v$ y, si $v$ no
es la raíz, el pedazo $A_v$ que cuelga de su padre. Aplicando §3 a $v$ en ese árbol,

$$
\text{arr}_\text{tom}(c) = w(v) + \sum_{c' \neq c} \text{no}(c') + \text{arr}_\text{no}(v),
\qquad
\text{arr}_\text{no}(c) = \sum_{c' \neq c} \max\big(\text{tom}(c'), \text{no}(c')\big)
  + \max\big(\text{arr}_\text{tom}(v), \text{arr}_\text{no}(v)\big),
$$

con las sumas sobre los hijos $c'$ de $v$ distintos de $c$. Para la raíz, $A_0$ es el
árbol vacío, y le damos 0 en los dos valores. No hace falta un $-\infty$ para
"$A_0$ con su raíz", porque $\text{arr}_\text{tom}$ solo entra dentro de un máximo
junto a $\text{arr}_\text{no}$, que vale 0 y es lo correcto para el vacío.

*Demostración.* Por inducción sobre la profundidad de $c$. Los subárboles $T_{c'}$
de los hermanos de $c$ son los mismos en el árbol enraizado en $0$ y en $A_c$, así que
sus valores son los de §3. El pedazo $A_v$ tiene sus valores correctos por hipótesis
de inducción (o es vacío si $v$ es la raíz). El lema de §4 no usó nada de la raíz
salvo que los hijos de $v$ cuelgan de subárboles disjuntos sin aristas entre sí, y
eso vale también en $A_c$. Entonces el teorema de §4, aplicado a $v$ en $A_c$, da
las dos fórmulas. Las de $\text{con}(v)$ y $\text{sin}(v)$ salen igual, con $v$ como
raíz del árbol entero y $A_v$ como uno de sus hijos. $\square$

*Costo.* Escrita así, la suma sobre $c' \neq c$ cuesta el grado de $v$ para cada hijo
$c$, y un vértice con $k$ hijos costaría $k^2$: una estrella volvería a $O(n^2)$. El
arreglo es calcular una vez la suma sobre todos los hijos y **restar** el término de
$c$. Así cada arista cuesta $O(1)$ y el total es $O(n)$. Esto funciona porque la suma
se puede deshacer. Si el agregado fuera un máximo, restar no tendría sentido, y hay que
guardar algo más (el ejercicio 6 es ese caso).

```{python continue}
def reenraizar(padre, w):
    hijos = hijos_de(padre)
    tom, no = conjunto_independiente(padre, w)
    arr_tom, arr_no = [0] * len(padre), [0] * len(padre)   # A_0 vacío: 0 y 0
    for v in range(len(padre)):                            # los padres primero
        suma_no = sum(no[c] for c in hijos[v])
        suma_max = sum(max(tom[c], no[c]) for c in hijos[v])
        arriba = max(arr_tom[v], arr_no[v])
        for c in hijos[v]:
            arr_tom[c] = w[v] + (suma_no - no[c]) + arr_no[v]
            arr_no[c] = (suma_max - max(tom[c], no[c])) + arriba
    con = [tom[v] + arr_no[v] for v in range(len(padre))]
    sin = [no[v] + max(arr_tom[v], arr_no[v]) for v in range(len(padre))]
    return con, sin, arr_tom, arr_no

def enraizar_en_cada_uno(padre, w):
    vecinos = [[] for _ in padre]
    for v in range(1, len(padre)):
        vecinos[v].append(padre[v]); vecinos[padre[v]].append(v)
    con, sin = [], []
    for r in range(len(padre)):
        orden, arriba = [r], {r: None}
        for u in orden:                                    # BFS desde r
            for x in vecinos[u]:
                if x not in arriba:
                    arriba[x] = u; orden.append(x)
        t, n_ = {}, {}
        for u in reversed(orden):
            hs = [x for x in vecinos[u] if x != arriba[u]]
            t[u] = w[u] + sum(n_[x] for x in hs)
            n_[u] = sum(max(t[x], n_[x]) for x in hs)
        con.append(t[r]); sin.append(n_[r])
    return con, sin

rng2, distintos = random.Random(7), 0
for _ in range(200):
    n = rng2.randint(1, 30)
    p = forma("azar", n, rng2)
    ws = [rng2.randint(1, 9) for _ in range(n)]
    distintos += reenraizar(p, ws)[:2] != enraizar_en_cada_uno(p, ws)
print("árboles donde difieren:", distintos, "de 200")

con, sin, arr_tom, arr_no = reenraizar(padre, w)
print("con:", con)
print("sin:", sin)
print("max(con, sin) por vértice:", [max(c, s) for c, s in zip(con, sin)])
print("en algún óptimo:", [v for v in range(10) if con[v] == fuerza_bruta(padre, w)])
```

Las dos versiones coinciden en los 200 árboles, y en el ejemplo cada vértice cumple
$\max(\text{con}(v), \text{sin}(v)) = 35$, como debe: las dos cantidades juntas cubren
todos los conjuntos. La @fig-dp-arboles-reenraizar muestra una arista con lo que sube y
lo que baja.

```{python continue echo=false output=asis}
hijos_ej = hijos_de(padre)
def tamano(v):
    return 1 + sum(tamano(c) for c in hijos_ej[v])
v_fig = max(hijos_ej[0], key=tamano)
print(F11.reenraizar(
    padre, w, tom, no, arr_tom, arr_no, v_fig,
    pie=f"La arista entre v0 y v{v_fig}. Sube el par (tom, no) del subárbol de "
        f"v{v_fig}, en azul; baja el par (arr_tom, arr_no) del resto del árbol, en "
        f"ocre, enraizado en v0. Con los dos, con(v{v_fig}) = {tom[v_fig]} + "
        f"{arr_no[v_fig]} = {con[v_fig]} y sin(v{v_fig}) = {no[v_fig]} + "
        f"max({arr_tom[v_fig]}, {arr_no[v_fig]}) = {sin[v_fig]}."))
```

Falta ver que la diferencia de costo se nota. Medimos las dos versiones en árboles al
azar de tamaño creciente.

```{python continue}
def segundos(f, *args, veces=1):
    """El mínimo de varias corridas, sin el recolector de basura en medio."""
    mejor = math.inf
    gc.disable()
    for _ in range(veces):
        inicio = time.perf_counter()
        f(*args)
        mejor = min(mejor, time.perf_counter() - inicio)
    gc.enable()
    return mejor

rng3, antes = random.Random(5), None
for n in [150, 300, 600]:
    p = forma("azar", n, rng3)
    ws = [rng3.randint(1, 9) for _ in range(n)]
    lento = segundos(enraizar_en_cada_uno, p, ws, veces=2)
    rapido = segundos(reenraizar, p, ws, veces=20)
    crece = "" if antes is None else \
        f"   al duplicar n: x{lento / antes[0]:.1f} y x{rapido / antes[1]:.1f}"
    print(f"n = {n:4d}   en cada uno {lento:6.3f} s   re-enraizado {rapido:6.4f} s{crece}")
    antes = (lento, rapido)
```

$O(n^2)$ predice que al duplicar $n$ el tiempo se multiplica por 4, y $O(n)$ que se
multiplica por 2. Los factores medidos están en la salida. Son tiempos de reloj, el
mínimo de unas pocas corridas, y en el caso del re-enraizado son milisegundos, así
que el ruido los mueve de un render a otro; lo que no cambia es que la distancia entre las dos
columnas crece con $n$.

## 8. Subconjuntos: el viajante

Ahora la segunda estructura. Un viajante sale de la ciudad 0, visita una vez cada una
de las otras $n - 1$ ciudades y vuelve. Ir de $i$ a $j$ cuesta $d(i, j)$, que no tiene
por qué ser igual a $d(j, i)$. Queremos la gira más barata. Es el problema del
viajante (TSP), y el capítulo 19 demuestra que su versión de decisión es NP-completa.
La fuerza bruta fija la ciudad 0 como salida y prueba los $(n-1)!$ órdenes de las
demás.

```{python continue}
def gira_fuerza_bruta(d):
    n = len(d)
    return min(sum(d[a][b] for a, b in zip((0,) + orden, orden + (0,)))
               for orden in itertools.permutations(range(1, n)))
```

Para $n = 15$ son $14! \approx 8{,}7 \cdot 10^{10}$ órdenes. Buscamos un estado.

El primero que uno escribe imita a la mochila: $g(S)$, el costo del camino más barato
que sale de 0 y visita exactamente las ciudades de $S$. Se queda corto por la misma
razón que el único valor de §2. Dos caminos que visitan $S$ pueden terminar en ciudades
distintas, y cuánto cuesta seguir depende de dónde se terminó. El más barato de los
dos puede quedar lejos de todo lo que falta. Un camino parcial tiene que contarle al
resto **dos** cosas: qué ciudades ya no puede usar y desde dónde sale.

Y nada más. Si dos caminos visitan el mismo conjunto $S$ y terminan en la misma
ciudad $j$, cualquier forma de terminar la gira que sirve para uno sirve para el otro,
y el más barato de los dos gana siempre. El orden en que se visitó $S$ no le importa
al resto. Esa es toda la ganancia: los $(|S| - 1)!$ órdenes de un mismo $S$ con el
mismo final se reducen a un número. El estado con el orden completo también sería
correcto, y cuesta $(n-1)!$; el estado sin el final es barato y falso.

La recurrencia la publicaron por separado, el mismo año, Richard Bellman
("Dynamic Programming Treatment of the Travelling Salesman Problem", *Journal of the
ACM* 9(1):61–63, 1962) y Michael Held y Richard M. Karp ("A Dynamic Programming
Approach to Sequencing Problems", *Journal of the Society for Industrial and Applied
Mathematics* 10(1):196–210, 1962). Se la conoce como algoritmo de Held-Karp.

## 9. Held-Karp

Para $S \subseteq \{1, \dots, n-1\}$ no vacío y $j \in S$, sea $g(S, j)$ el costo del
camino más barato que sale de 0, visita exactamente las ciudades de $S$ y termina en
$j$. Entonces

$$
g(\{j\}, j) = d(0, j),
\qquad
g(S, j) = \min_{i \in S \setminus \{j\}} \Big( g(S \setminus \{j\}, i) + d(i, j) \Big)
\quad \text{si } |S| \ge 2,
$$

y la gira óptima cuesta $\min_{j} \big(g(\{1, \dots, n-1\}, j) + d(j, 0)\big)$.

Un conjunto se guarda como un entero: el bit $j - 1$ dice si la ciudad $j$ está. Un
subconjunto propio de $S$ tiene una máscara menor que la de $S$, así que recorrer las
máscaras en orden creciente calcula cada estado después de los que necesita. El código
cuenta estados y transiciones, que usaremos en §10.

```{python continue}
def held_karp(d):
    n, INF = len(d), math.inf
    todas = (1 << (n - 1)) - 1                      # el bit j-1 es la ciudad j
    g = [[INF] * n for _ in range(todas + 1)]
    estados = transiciones = 0
    for j in range(1, n):
        g[1 << (j - 1)][j] = d[0][j]
    for S in range(1, todas + 1):
        for j in range(1, n):
            bit = 1 << (j - 1)
            if not S & bit:
                continue
            estados += 1
            resto = S ^ bit
            if resto == 0:
                continue                             # g({j}, j) ya está
            mejor = INF
            for i in range(1, n):
                if resto >> (i - 1) & 1:
                    transiciones += 1
                    mejor = min(mejor, g[resto][i] + d[i][j])
            g[S][j] = mejor
    costo = min(g[todas][j] + d[j][0] for j in range(1, n))
    return costo, estados, transiciones

def distancias(n, rng):
    return [[0 if i == j else rng.randint(1, 50) for j in range(n)] for i in range(n)]

rng4, mal = random.Random(3), 0
for n in range(2, 9):
    for _ in range(10):
        d = distancias(n, rng4)
        mal += held_karp(d)[0] != gira_fuerza_bruta(d)
print("matrices donde difiere de la fuerza bruta:", mal, "de 70")
```

Las matrices son asimétricas, así que el código no se apoya en que $d(i, j) = d(j, i)$.

**Teorema.** Para todo $S$ no vacío y $j \in S$, la tabla guarda $g(S, j)$.

*Demostración.* Por inducción sobre $|S|$. Con $|S| = 1$ el único camino es la arista
de 0 a $j$. Sea $|S| \ge 2$.

Cota inferior: todo camino que sale de 0, visita $S$ y termina en $j$ tiene una
penúltima ciudad $i \in S \setminus \{j\}$, y su prefijo hasta $i$ es un camino que
sale de 0, visita exactamente $S \setminus \{j\}$ y termina en $i$. Ese prefijo cuesta
al menos $g(S \setminus \{j\}, i)$, que por hipótesis es lo que guarda la tabla, así
que el camino cuesta al menos el término $i$ del mínimo.

Alcanzabilidad: para el $i$ que realiza el mínimo, tomamos el mejor camino de
$(S \setminus \{j\}, i)$ y le agregamos la arista $i \to j$. El resultado es un camino
simple porque $j \notin S \setminus \{j\}$, y visita exactamente $S$. Este es el paso
donde el camino más largo de §1 fallaba: allí los dos tramos podían compartir
vértices, y aquí el estado dice exactamente cuáles gastó el prefijo, así que el
sufijo no puede repetirlos.

La respuesta final sale del mismo argumento con la arista de vuelta $j \to 0$. $\square$

## 10. Cuánto cuesta y hasta dónde llega

Primero el experimento. Cada estado es un par $(S, j)$ con $j \in S$, y cada uno mira
a lo sumo $n - 2$ predecesores. Una cota fácil es $2^{n-1}$ conjuntos por $n - 1$
finales por $n - 1$ predecesores. Comparamos lo que el código contó con esa cota.

```{python continue}
rng5 = random.Random(4)
for n in [4, 6, 8, 10, 12]:
    _, e, t = held_karp(distancias(n, rng5))
    cota = 2 ** (n - 1) * (n - 1) ** 2
    print(f"n = {n:2d}   estados {e:6d}   transiciones {t:7d}   "
          f"transiciones / cota {t / cota:.3f}")
```

La razón crece hacia $1/4$ sin pasarse: la cota fácil sobra por un factor
constante, y el ejercicio 8 pide la fórmula exacta que lo explica. La cota es
suficiente para el orden: el tiempo es $O(2^n n^2)$, porque $2^{n-1}(n-1)^2 \le
2^n n^2$. La memoria es la tabla, $2^{n-1}$ filas de $n$ números, $O(2^n n)$.

Que $2^n n^2$ sea mucho menos que $(n-1)!$ no necesita una cuenta fina: el cociente
$(n-1)! / (2^n n^2)$ crece sin límite, porque al pasar de $n$ a $n+1$ el numerador se
multiplica por $n$ y el denominador por menos de $2 \cdot (1 + 1/n)^2 \le 8$. Pero
conviene verlo en segundos. Medimos los dos algoritmos con la fuerza bruta hasta
$n = 10$, donde ya tarda del orden de un segundo, y Held-Karp hasta $n = 14$.

```{python continue echo=false output=asis}
def mejor_de(f, d, veces):
    return segundos(f, d, veces=veces)

rng6 = random.Random(6)
medidos = {"fuerza bruta": [], "Held-Karp": []}
for n in range(6, 15):
    d = distancias(n, rng6)
    medidos["Held-Karp"].append((n, mejor_de(held_karp, d, 5 if n <= 12 else 3)))
    if n <= 10:
        medidos["fuerza bruta"].append((n, mejor_de(gira_fuerza_bruta, d,
                                                    3 if n <= 9 else 1)))
bruta_10 = medidos["fuerza bruta"][-1][1]
hk_14 = medidos["Held-Karp"][-1][1]
bruta_14 = bruta_10 * math.factorial(13) / math.factorial(9)
fmt = lambda s: f"{s:.4f}".replace(".", ",")
print("| $n$ | fuerza bruta | Held-Karp | Held-Karp, factor sobre $n - 1$ |\n"
      "|---:|---:|---:|---:|")
previo = None
for n, s in medidos["Held-Karp"]:
    b = dict(medidos["fuerza bruta"]).get(n)
    factor = "" if previo is None else f"{s / previo:.1f}".replace(".", ",")
    print(f"| {n} | {fmt(b) + ' s' if b else '—'} | {fmt(s)} s | {factor} |")
    previo = s
print()
print(F11.grafica_semilog(
    medidos, "número de ciudades n", "segundos",
    pie=f"Tiempos medidos, el mínimo de varias repeticiones, con la y en escala "
        f"logarítmica. Una recta en esta escala es una exponencial. Held-Karp "
        f"resuelve n = 14 en {fmt(hk_14)} s. La fuerza bruta tardó {fmt(bruta_10)} s "
        f"en n = 10; multiplicando por 13!/9! = {math.factorial(13) // math.factorial(9)}, "
        f"en n = 14 tardaría unos {bruta_14 / 3600:.0f} horas."))
```

En la @fig-dp-arboles-tiempos la curva de la fuerza bruta se dobla hacia arriba, porque
cada ciudad nueva multiplica su tiempo por $n - 1$. La de Held-Karp es casi una recta,
y la cota de §10 dice cuánto debería subir: al pasar de $n - 1$ a $n$ ciudades,
$2^{n-1}(n-1)^2$ se multiplica por $2 \left(\frac{n-1}{n-2}\right)^2$, algo más de 2
(2,3 en $n = 14$). Como las transiciones son una fracción casi constante de la cota,
el tiempo debería crecer en esa proporción. La última columna de la tabla es el factor medido, con el
ruido del reloj encima.

Held-Karp sigue siendo exponencial. Es el primer algoritmo del curso que resuelve
exacto un problema NP-duro mejorando la fuerza bruta, y no el último. El capítulo 20
vuelve sobre algoritmos exactos para problemas NP-duros y sobre cuánto puede bajar la
base de la exponencial, y el capítulo 22 renuncia a lo exacto en el TSP métrico a
cambio de tiempo polinomial con una garantía de aproximación.

## 11. La regla

Los dos problemas del capítulo pasaron por los mismos tres estados:

| | Árbol | Viajante |
|---|---|---|
| Estado con menos | $f(v)$, un valor | $g(S)$, sin el final |
| | recurrencia falsa | recurrencia falsa |
| Estado justo | $(v, \text{tomado o no})$ | $(S, j)$ |
| | $O(n)$ | $O(2^n n^2)$ |
| Estado con más | qué vértices de $T_v$ se tomaron | el orden del camino |
| | correcto, exponencial | correcto, $(n-1)!$ |

La regla: **el estado es lo que una parte de la solución le tiene que contar al resto,
y nada más**. Para encontrarlo, se pregunta qué tendría que saber el resto del
problema para seguir sin mirar dentro. Si el estado le cuenta menos, aparece una
pareja de soluciones parciales con el mismo estado que el resto no puede tratar igual,
y la recurrencia es falsa: es el camino simple más largo de §1, el valor único de §2 y
$g(S)$ de §8. Si le cuenta más, la tabla distingue soluciones parciales que el resto
trataría igual, y paga por eso.

El capítulo 12 parte de una recurrencia que ya es correcta y baja su costo sin cambiar
el estado.

## Resumen

- El principio de optimalidad es una propiedad del estado elegido, no del problema. El
  camino simple más largo lo viola con el estado "extremos", porque las dos mitades
  compiten por los vértices.
- En un árbol, quitar un vértice deja pedazos sin aristas entre sí. El subárbol de $v$
  le cuenta al padre dos números: lo mejor con $v$ y lo mejor sin $v$.
- Conjunto independiente de peso máximo en un árbol:
  $\text{tom}(v) = w(v) + \sum \text{no}(c)$ y $\text{no}(v) = \sum \max(\text{tom}(c),
  \text{no}(c))$, en $O(n)$, que es óptimo.
- Cuando $v$ no está, sus hijos quedan libres. La variante que los obliga a estar pasa
  las estrellas y los caminos sin pesos y falla en árboles al azar.
- Re-enraizamiento: por cada arista sube el par del subárbol y baja el par del resto.
  Con los dos, la pregunta se responde desde todos los vértices en $O(n)$, siempre que
  el agregado se pueda deshacer (una suma sí, un máximo no).
- En Python, una DP recursiva sobre un árbol se rompe en un camino de más de 1 000
  vértices; el orden de los índices o un BFS la hacen iterativa.
- Held-Karp (Bellman; Held y Karp, 1962): el estado $(S, j)$ olvida el orden en que se
  visitó $S$, que al resto no le importa. Tiempo $O(2^n n^2)$ y memoria $O(2^n n)$,
  frente a $(n-1)!$ de la fuerza bruta.
- El estado justo está entre uno que cuenta menos (recurrencia falsa) y uno que cuenta
  más (tabla más grande que la necesaria).

## Ejercicios

1. **[traza]** El árbol tiene los vértices $0, \dots, 8$, raíz $0$, y estos padres:
   $\text{padre}(1) = \text{padre}(2) = 0$, $\text{padre}(3) = \text{padre}(4) = 1$,
   $\text{padre}(5) = 3$, $\text{padre}(6) = 4$, $\text{padre}(7) = 5$,
   $\text{padre}(8) = 7$. Los pesos de $0$ a $8$ son $7, 4, 2, 8, 1, 7, 7, 1, 8$.
   Calcula a mano $\text{tom}$ y $\text{no}$ de cada vértice, reconstruye el conjunto
   óptimo y calcula lo que devuelve la variante con error de §5.

2. **[entrada que rompe]** Sin pesos, una regla golosa conocida es: mientras queden
   vértices, toma una hoja, agrégala al conjunto y borra la hoja y su vecino. Con
   pesos, la misma regla (con cualquier forma de elegir la hoja) puede equivocarse.
   Da el árbol más pequeño con pesos donde se equivoca para **toda** elección de
   hojas, y demuestra que no hay uno más pequeño.

3. **[demostración]** Demuestra que, sin pesos, la regla del ejercicio 2 encuentra un
   conjunto independiente máximo en cualquier árbol (en cualquier bosque, de hecho).
   Usa un argumento de intercambio como los del capítulo 9: muestra que alguna
   solución óptima contiene a la hoja elegida.

4. **[modelar]** Una **cobertura de vértices** es un conjunto que toca todas las
   aristas. Diseña una DP en $O(n)$ para la cobertura de vértices de peso mínimo en un
   árbol con pesos positivos: di el estado, la recurrencia y la demostración. ¿Qué
   relación hay entre tu respuesta y la de §3 sobre el mismo árbol? Demuéstrala.

5. **[modelar]** En un árbol sin pesos, calcula para cada vértice $v$ la suma de las
   distancias de $v$ a todos los demás, en $O(n)$ en total. Di qué sube y qué baja por
   cada arista, y por qué la fórmula del re-enraizamiento no necesita restar nada que
   no se pueda restar.

6. **[cambio de hipótesis]** Ahora las aristas tienen longitudes positivas. (a) Calcula
   el diámetro (la mayor distancia entre dos vértices) con una DP de una sola pasada
   desde las hojas, y demuéstrala. (b) Calcula la **excentricidad** de cada vértice, la
   distancia al vértice más lejano, en $O(n)$ en total. En §7 restábamos el término de
   un hijo de una suma. Explica qué paso deja de valer cuando el agregado es un
   máximo, y qué hay que guardar en cada vértice para recuperar el $O(n)$.

7. **[traza]** Cuatro ciudades con la matriz de costos (fila de salida, columna de
   llegada):

   | | 0 | 1 | 2 | 3 |
   |---|---:|---:|---:|---:|
   | **0** | 0 | 3 | 9 | 5 |
   | **1** | 4 | 0 | 2 | 8 |
   | **2** | 7 | 6 | 0 | 3 |
   | **3** | 2 | 9 | 4 | 0 |

   Escribe la tabla completa de Held-Karp, $g(S, j)$ para cada $S \subseteq
   \{1, 2, 3\}$ y $j \in S$, con el predecesor que realiza cada mínimo. Reconstruye
   la gira óptima y compárala con las seis giras posibles.

8. **[demostración]** (a) Demuestra que Held-Karp tiene exactamente $(n-1) 2^{n-2}$
   estados y cuenta sus transiciones exactamente, en forma cerrada. Explica con tu
   fórmula por qué la razón de §10 tiende a $1/4$. (b) Para calcular los conjuntos de
   tamaño $k$ solo hacen falta los de tamaño $k - 1$. Si se guardan solo esas dos
   capas, ¿cuánta memoria hace falta? Da el orden exacto en función de $n$, en
   notación $\Theta$.

9. **★ [demostración]** Dada $f$ sobre los subconjuntos de $\{0, \dots, n-1\}$, se
   quiere $F(S) = \sum_{T \subseteq S} f(T)$ para todos los $S$. (a) Demuestra que
   recorrer, para cada $S$, todos sus subconjuntos cuesta $\Theta(3^n)$ sumas. (b)
   Diseña un algoritmo de $O(2^n n)$ que procese un elemento a la vez, y demuéstralo
   con un invariante: di qué guarda la tabla después de procesar los elementos
   $0, \dots, i-1$. (c) ¿Qué es aquí el estado, en el sentido de §11?

10. **[implementar y medir]** Corre el `held_karp` de §9 en tu máquina con $n$
    creciente. ¿Hasta qué $n$ termina en menos de un minuto? Mide la memoria máxima
    en ese $n$ (con `tracemalloc` o con el sistema operativo) y compárala con la que
    predice la tabla, $2^{n-1} n$ números. Después supón una implementación compilada
    cien veces más rápida por transición, con 8 bytes por número: ¿qué se acaba
    primero, un minuto o la memoria de tu máquina, y en qué $n$? Reescribe el código
    por capas, como en el ejercicio 8, y mide de nuevo.
