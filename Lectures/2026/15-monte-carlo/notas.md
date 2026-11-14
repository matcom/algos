# Algoritmos aleatorios II: Monte Carlo {#chap-monte-carlo}

```{python echo=false output=asis}
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_15.py
import figuras_15 as F15
```

El capítulo 8 tiró monedas para decidir cuánto trabaja un algoritmo, y nunca dejó que
las monedas tocaran la respuesta. Este capítulo hace el trato contrario: el tiempo
queda fijo y es la respuesta la que puede salir mal, con una probabilidad que el
algoritmo garantiza para toda entrada. Parece un mal negocio. Vamos a ver dos
problemas. En el primero, verificar un producto de matrices, es lo mejor que se conoce.
En el segundo, el corte mínimo de un grafo, el algoritmo aleatorio que veremos no es el
más rápido que hay, pero es la forma más limpia de ver la técnica. Y veremos una
herramienta, la repetición, que convierte un algoritmo que acierta poco en uno que casi
nunca falla. La herramienta tiene una sola
condición, y el error plantado de este capítulo es olvidarla.

## 1. Fijar el tiempo, soltar la respuesta

Un algoritmo **Monte Carlo** corre en un tiempo acotado para toda entrada y toda
sucesión de monedas, y puede devolver una respuesta equivocada. Lo que se garantiza es
cuán probable es equivocarse, con los cuantificadores en el mismo orden que en el
capítulo 8, §1:
$$\max_{x}\ \Pr_r\big[\text{la respuesta con la entrada } x \text{ y las monedas } r \text{ está mal}\big] \le \delta.$$
La entrada la elige un adversario que conoce el código. Las monedas las tira el
algoritmo después. No hay entradas buenas ni malas: para cada una, la mayoría de las
sucesiones de monedas dan la respuesta correcta.

En un problema de decisión, donde la respuesta es "sí" o "no", el error puede caer de
dos maneras. Un algoritmo tiene **error de un solo lado** si una de las dos respuestas
es siempre verdad. Por ejemplo, cuando dice "no" nunca se equivoca y cuando dice "sí"
quizás. Tiene **error de dos lados** si las dos respuestas pueden ser falsas. La
diferencia parece un detalle y decide cómo se reduce el error, como veremos en §7.

Las dos familias se relacionan. El ejercicio 7 del capítulo 8 convierte un algoritmo
Las Vegas en uno Monte Carlo: se corta la ejecución a dos veces el tiempo esperado y,
por Markov, se responde con probabilidad al menos $1/2$. Al revés no siempre se puede.
Para convertir un Monte Carlo en un Las Vegas hay que poder **comprobar** la respuesta,
y repetir hasta que la comprobación pase. En el producto de matrices no se conoce una
comprobación sin azar más barata que la prueba que vamos a hacer, y por eso nos
quedamos con el error.

## 2. Verificar un producto de matrices: el intento que falla

**El problema.** Te dan tres matrices $A$, $B$ y $C$ de $n \times n$ con entradas
enteras, y tienes que decidir si $AB = C$. Es la situación de quien recibe un resultado
calculado por otro y quiere saber si se puede fiar.

Contamos operaciones aritméticas sobre enteros, cada una de costo constante. El
modelo es razonable mientras las entradas tengan un tamaño acotado, porque los números
que aparecen tienen a lo sumo el doble de bits que las entradas, más $O(\log n)$ por
las sumas. El capítulo 1 pidió decir siempre el modelo, y aquí es este.

Recalcular $AB$ con el algoritmo escolar cuesta $n^3$ multiplicaciones. Hay algoritmos
con exponente menor que 3, pero ninguno conocido llega a $n^2$, que es lo que cuesta
leer la entrada. La pregunta del capítulo es si **comprobar** un producto puede costar
menos que **calcularlo**.

**El intento que falla.** Revisar algunas entradas de $C$ al azar: elegir $s$
posiciones $(i, j)$, calcular cada $(AB)_{ij}$ en $n$ multiplicaciones y comparar. Con
$s = n$ cuesta $n^2$. Pero si $C$ está mal en una sola posición, la muestra la encuentra
solo si cae justo ahí.

```{python continue}
n = 20
for s in [n, 5 * n, n * n // 2]:
    print(f"s = {s:>3} posiciones: atrapa un error único con "
          f"probabilidad {1 - (1 - 1 / n ** 2) ** s:.3f}")
```

Con $s = n$, menos de un 5 %. El error puede estar en cualquiera de las $n^2$
posiciones, y una muestra que mira posiciones individuales solo lo ve si cae encima.
Hace falta una prueba en la que **cada** entrada de $C$ influya.

## 3. Freivalds: comprimir con un vector al azar

**Cómo se le ocurre a uno.** Si $AB = C$, entonces $ABx = Cx$ para todo vector $x$. Y
$A(Bx)$ se calcula con dos productos matriz por vector, sin formar $AB$: son $2n^2$
multiplicaciones, y $Cx$ es otro producto de $n^2$. Cada componente de $Cx$ mezcla una
fila entera de $C$, así que una entrada mala no puede esconderse del todo. Falta elegir
$x$. Un $x$ fijo no sirve: para todo $x \ne 0$ hay una matriz $D \ne 0$ con $Dx = 0$,
por ejemplo la que tiene una sola fila no nula, $(x_2, -x_1, 0, \dots, 0)$, o
$(1, 0, \dots, 0)$ si $x_1 = x_2 = 0$. El adversario, que conoce $x$, entrega
$C = AB - D$, y la prueba no ve la diferencia. Hay que sortear $x$ después de recibir
las matrices.

La prueba es de Rūsiņš Freivalds, "Probabilistic machines can use less running time",
en las actas del congreso IFIP de 1977. Cada **ronda** sortea $r \in \{0, 1\}^n$ con
monedas independientes y compara $A(Br)$ con $Cr$.

```{python continue}
def matriz(n, M=9):
    return [[random.randint(-M, M) for _ in range(n)] for _ in range(n)]

def producto(A, B):                               # el escolar: n³ multiplicaciones
    columnas = list(zip(*B))
    return [[sum(a * b for a, b in zip(fila, col)) for col in columnas] for fila in A]

def por_vector(A, x):                             # n² multiplicaciones
    return [sum(a * b for a, b in zip(fila, x)) for fila in A]

def ronda(A, B, C):
    r = [random.randrange(2) for _ in range(len(A))]
    return por_vector(A, por_vector(B, r)) == por_vector(C, r)

def freivalds(A, B, C, k):
    return all(ronda(A, B, C) for _ in range(k))   # "sí" solo si pasa las k rondas

random.seed(15)
for _ in range(200):                               # oráculo: el producto escolar
    m = random.randrange(1, 8)
    A, B = matriz(m), matriz(m)
    C = producto(A, B)
    assert freivalds(A, B, C, 5)                   # si AB = C, siempre "sí"
    C[random.randrange(m)][random.randrange(m)] += 1
    assert not freivalds(A, B, C, 60)              # si no, "no" (falla con 2⁻⁶⁰)
print("200 pruebas contra el producto escolar: iguales")
```

El segundo `assert` puede fallar, con probabilidad $2^{-60}$ por prueba si lo que
demostraremos es cierto. Ahora el experimento: una pareja $A$, $B$ de $20 \times 20$,
y matrices $C$ que difieren de $AB$ en **una sola** entrada, sumando o restando 1 en
una posición al azar. Es el caso que la muestra de §2 casi nunca veía.

```{python continue}
n = 20
A, B = matriz(n), matriz(n)
AB = producto(A, B)

def un_error():
    C = [fila[:] for fila in AB]
    C[random.randrange(n)][random.randrange(n)] += random.choice((-1, 1))
    return C

T = 3000
pasan = sum(ronda(A, B, un_error()) for _ in range(T))
print(f"pasan una ronda: {pasan} de {T}, fracción {pasan / T:.3f}")
print(f"multiplicaciones por ronda: {3 * n * n},  producto escolar: {n ** 3}")
```

Una ronda deja pasar más o menos la mitad de las matrices con un error, y cuesta 1 200
multiplicaciones contra 8 000. El experimento propone el enunciado: la probabilidad de
dejar pasar una $C$ equivocada es $1/2$. La sección siguiente demuestra que nunca es
más.

## 4. Error a lo sumo 1/2

**Teorema.** Si $AB = C$, la ronda dice "sí" siempre. Si $AB \ne C$, la ronda dice "sí"
con probabilidad a lo sumo $1/2$.

*Demostración.* Si $AB = C$, entonces $A(Br) = (AB)r = Cr$ para todo $r$, por la
asociatividad del producto. Esa mitad no tiene azar.

Si $AB \ne C$, sea $D = AB - C$, que no es la matriz cero. La ronda dice "sí" si y solo
si $Dr = 0$. Elegimos una entrada $d_{ij} \ne 0$ y miramos solo la componente $i$:
$$(Dr)_i = d_{ij} r_j + \sum_{l \ne j} d_{il} r_l = d_{ij} r_j + S.$$
El paso que todo el mundo se salta es este: **$S$ depende solo de las monedas
$r_l$ con $l \ne j$, y $r_j$ es independiente de todas ellas.** Así que podemos
imaginar que primero se tiran las otras $n - 1$ monedas, lo que fija $S$, y después
$r_j$. Con $S$ fijo, $(Dr)_i = 0$ pide $r_j = -S/d_{ij}$, que es a lo sumo uno de los
dos valores 0 y 1. Entonces, para cada valor de las otras monedas,
$\Pr[(Dr)_i = 0] \le 1/2$, y promediando sobre ellas también. Como $Dr = 0$ exige
$(Dr)_i = 0$, $\Pr[Dr = 0] \le 1/2$. $\square$

La técnica de tirar al final la moneda que importa se llama **decisiones diferidas**.
La demostración no usa ni el tamaño de las entradas ni dónde están los errores. Por
eso vale para toda $C$.

La cota no se puede mejorar. Si $D$ tiene una sola entrada no nula, en la posición
$(i, j)$, entonces $Dr = 0$ exactamente cuando $r_j = 0$, con probabilidad $1/2$. Es el
caso del experimento. Enumerando todas las $D$ no nulas de $3 \times 3$ con entradas
en $\{-1, 0, 1\}$ y los ocho vectores $r$, el peor caso es $1/2$. Para que la
comprobación pueda fallar, la repetimos con vectores que **no** tienen monedas
independientes: $r = (b, b, b)$ con una sola moneda $b$.

```{python continue}
def peor_caso(vectores, m=3):
    peor = 0
    for entradas in itertools.product((-1, 0, 1), repeat=m * m):
        if any(entradas):
            D = [entradas[i * m:(i + 1) * m] for i in range(m)]
            pasa = sum(not any(por_vector(D, r)) for r in vectores)
            peor = max(peor, pasa / len(vectores))
    return peor

print("r con monedas independientes:", peor_caso(list(itertools.product((0, 1), repeat=3))))
print("r = (b, b, b):               ", peor_caso([(0, 0, 0), (1, 1, 1)]))
```

Con una sola moneda copiada en las tres posiciones, hay matrices $D \ne 0$ que pasan
siempre: la fila $(1, -1, 0)$ anula a $(b, b, b)$ para los dos valores de $b$. La
demostración usó que $r_j$ es independiente de las otras monedas, y sin esa hipótesis
el resultado es falso.

## 5. Amplificar

Una cota de $1/2$ es poca garantía: es una moneda al aire. Pero el error es de un solo
lado. Si una ronda dice "no", encontró un vector $r$ con $A(Br) \ne Cr$, y eso
**demuestra** que $AB \ne C$: el $r$ es un testigo que cualquiera puede comprobar.
Entonces se puede repetir.

**Teorema.** Si $AB \ne C$ y se hacen $k$ rondas con monedas nuevas e independientes,
las $k$ dicen "sí" con probabilidad a lo sumo $2^{-k}$.

*Demostración.* Sea $E_t$ el evento "la ronda $t$ dice sí". Cada ronda sortea su propio
vector, independiente de los anteriores, así que los eventos son independientes y
$\Pr[E_1 \cap \dots \cap E_k] = \prod_t \Pr[E_t] \le (1/2)^k$ por el teorema de §4.
$\square$

El costo es $3kn^2$ multiplicaciones y el error baja exponencialmente en $k$: el error
es un parámetro que elige el usuario, y cada factor 2 menos cuesta una ronda, es
decir, $3n^2$ multiplicaciones más. Un error de $\delta$ cuesta
$\lceil \log_2(1/\delta) \rceil$ rondas, sea cual sea $n$. El ejercicio 2 hace la
cuenta para un $\delta$ concreto.

La medición, con las mismas matrices de §3: cuántas de 3 000 matrices con un error
pasan $k$ rondas seguidas. Para cada matriz basta contar cuántas rondas seguidas pasa.

```{python continue}
K = 10

def rondas_pasadas(A, B, C, K):
    for t in range(K):
        if not ronda(A, B, C):
            return t
    return K

def fraccion_por_k(pasadas):
    return [sum(p >= k for p in pasadas) / len(pasadas) for k in range(1, K + 1)]

random.seed(5)
buena = fraccion_por_k([rondas_pasadas(A, B, un_error(), K) for _ in range(T)])
print(" k   medida   2^-k")
for k in [1, 2, 3, 5, 8, 10]:
    print(f"{k:>2}   {buena[k - 1]:.4f}   {2 ** -k:.4f}")
```

La fracción medida sigue a $2^{-k}$: con una sola entrada mala, cada ronda es
exactamente una moneda justa, y la cota del teorema se alcanza.

## 6. El error plantado: la misma moneda $k$ veces

Una versión "optimizada" sortea el vector una vez y lo reutiliza en las $k$ rondas.
Ahorra bits aleatorios, y el código parece el mismo.

```{python continue}
def rondas_pasadas_mala(A, B, C, K):
    r = [random.randrange(2) for _ in range(len(A))]   # un solo sorteo
    for t in range(K):
        if por_vector(A, por_vector(B, r)) != por_vector(C, r):
            return t
    return K

def muchos_errores():                              # perturba casi todas las entradas
    return [[x + random.randint(-1, 1) for x in fila] for fila in AB]

random.seed(6)
mala = fraccion_por_k([rondas_pasadas_mala(A, B, un_error(), K) for _ in range(T)])
bateria = sum(rondas_pasadas_mala(A, B, muchos_errores(), K) > 0 for _ in range(T))
print(f"un error,  pasan {K} rondas: buena {buena[-1]:.4f}   mala {mala[-1]:.4f}")
print(f"muchos errores, pasan la primera ronda con la mala: {bateria} de {T}")
```

```{python continue echo=false output=asis}
ks = list(range(1, K + 1))
print(F15.grafica_semilog(
    [("monedas nuevas", list(zip(ks, buena)), F15.OSCURO),
     ("el mismo r", list(zip(ks, mala)), F15.ALARMA)],
    ("2⁻ᵏ", [(k, 2 ** -k) for k in ks], F15.CALIDO),
    "rondas k", "fracción que pasa", ident="mc-freivalds",
    pie=f"Fracción de {T} matrices C con una sola entrada distinta de AB (n = {n}) "
        f"que pasan k rondas de Freivalds. Con monedas nuevas en cada ronda la "
        f"fracción sigue a 2⁻ᵏ; con el mismo vector en todas se queda en la mitad. "
        f"Los puntos en cero no se pueden dibujar en escala logarítmica y se omiten."))
```

La @fig-mc-freivalds muestra las dos versiones. Con el mismo $r$, todas las rondas
repiten la primera cuenta, y el error se queda en la mitad con 10 rondas o con mil. Una
batería que perturba muchas entradas, la manera natural de fabricar una $C$
equivocada, no lo nota, porque con muchas entradas malas una sola ronda ya atrapa la
diferencia. Lo delata una sola entrada mala, justo donde se alcanza la cota.

La demostración de §5 lo anunciaba con una palabra: **independientes**. El producto
$\prod_t \Pr[E_t]$ vale para eventos independientes, y con el mismo $r$ los eventos son
el mismo evento, así que $\Pr[E_1 \cap \dots \cap E_k] = \Pr[E_1]$. Es la hipótesis
que se rompió a propósito en §4, ahora entre rondas.

## 7. Un lado y dos lados

La amplificación de §5 usó que el error era de un lado: "no" siempre es verdad, y por
eso la regla "responde no si alguna ronda dice no" no introduce errores nuevos. Con
$AB = C$ todas las rondas dicen "sí" y la respuesta es correcta. Con $AB \ne C$ la
respuesta es incorrecta solo si **todas** las rondas fallan.

Fíjate en la asimetría. Una respuesta "no" viene con un testigo, el vector $r$, que
prueba que el producto está mal. Una respuesta "sí" no viene con nada: dice que $k$
vectores al azar no vieron diferencia. Para convertir Freivalds en un algoritmo Las
Vegas, como pedía §1, habría que comprobar barato que un "sí" es verdad, y eso es
justo el problema con el que empezamos.

Con error de dos lados esa regla se rompe: si "no" también puede ser falso, junta los
errores de todas las rondas. La regla que funciona es votar, y su análisis es el
ejercicio 10. La segunda mitad del capítulo tiene un algoritmo que no
responde sí o no, sino que devuelve un número, y el error de un lado aparece de otra
manera: el número puede salir grande, nunca chico.

## 8. El corte mínimo global

Sea $G = (V, E)$ un multigrafo no dirigido y conexo, con $n$ vértices y $m$ aristas:
puede haber varias aristas entre los mismos dos vértices, pero no lazos. Un **corte**
es una partición de $V$ en dos partes no vacías $S$ y $V \setminus S$, y su valor es el
número de aristas con un extremo en cada parte. El **corte mínimo global** es el de
menor valor entre todos, y su valor se escribe $\lambda(G)$: cuántos enlaces caídos
bastan para partir una red.

El capítulo 13 resolvió un problema parecido. En una red con fuente $s$ y sumidero $t$,
el teorema Max-Flow Min-Cut del capítulo 13, §6, dice que el flujo máximo es igual al
menor corte que separa $s$ de $t$, y Dinic lo calcula en $O(V^2 E)$ (capítulo 13, §11).
Un grafo no dirigido se convierte en red poniendo en cada arista dos arcos de
capacidad 1, uno en cada sentido. Pero el corte global no fija $s$ ni $t$.

**El intento con flujos.** Se fija un vértice $s$ cualquiera. El corte mínimo global
separa a $s$ de algún vértice $t$, porque las dos partes son no vacías. Entonces
$$\lambda(G) = \min_{t \ne s} \big(\text{corte } s\text{-}t \text{ mínimo}\big),$$
y bastan $n - 1$ flujos máximos. Con la cota general de Dinic serían
$O(n \cdot n^2 m) = O(n^3 m)$, pero esa cota es holgada aquí, y con lo que ya tenemos se
puede hacer mejor. Elegimos como $s$ un vértice de grado mínimo $\delta$. Las aristas
que salen de $s$ suman capacidad $\delta$, así que cada flujo $s$-$t$ vale a lo sumo
$\delta$, y Ford-Fulkerson (capítulo 13, §4) hace a lo sumo $\delta$ aumentos. Cada
aumento es una búsqueda de camino en la residual, de costo $O(m)$. Los $n - 1$ flujos
cuestan $O(n \delta m)$, y como la suma de los grados es $2m$, $n\delta \le 2m$: en
total, $O(m^2)$. Esa es la referencia con la que comparamos, y es una cota superior,
no una medida.

```{python echo=false}
# Cadena nueva: los bloques de Karger no re-ejecutan los de Freivalds.
import itertools
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))
import figuras_15 as F15
```

El oráculo es la fuerza bruta: los $2^{n-1} - 1$ cortes, fijando del mismo lado el
vértice $n - 1$ para no contar cada corte dos veces.

```{python continue}
def valor(aristas, lado):
    return sum(lado[u] != lado[v] for u, v in aristas)

def corte_bruto(n, aristas):
    return min(valor(aristas, [(S >> v) & 1 for v in range(n)])
               for S in range(1, 2 ** (n - 1)))
```

## 9. Contraer una arista al azar

**Cómo se le ocurre a uno.** Un corte mínimo tiene pocas aristas: a lo sumo el grado
mínimo, porque aislar un vértice ya es un corte. Así que una arista elegida al azar
casi nunca es del corte mínimo, y lo más probable es que sus dos extremos estén del
mismo lado. Si están del mismo lado, se pueden **fundir** en un solo vértice sin
perder el corte. Repitiendo, el grafo se achica, y cuando quedan dos vértices, las
aristas entre ellos son un corte.

**Contraer** la arista $\{u, v\}$ es reemplazar $u$ y $v$ por un vértice nuevo que
hereda todas sus aristas. Las aristas entre $u$ y $v$ se convertirían en lazos y se
borran. Las aristas paralelas se conservan, porque cuentan en el valor de los cortes.
El **algoritmo de contracción** de David Karger ("Global min-cuts in RNC, and other
ramifications of a simple min-cut algorithm", Fourth Annual ACM-SIAM Symposium on
Discrete Algorithms, SODA 1993) contrae una arista elegida uniformemente entre las que
quedan hasta que quedan dos vértices, y devuelve las aristas entre ellos.

**La implementación** no construye los multigrafos intermedios. Cada vértice
contraído es un conjunto de vértices originales, y los conjuntos se llevan con el
union-find del capítulo 4, §7, con unión por rango y compresión de caminos. Una arista
original es un lazo si sus dos extremos están en el mismo conjunto. Elegir una arista
uniforme entre las que no son lazos es lo mismo que barajar las aristas una vez y
recorrerlas en ese orden, saltando los lazos, como Kruskal en el capítulo 10, §7 con
pesos al azar. La razón tiene dos partes. Primero, las aristas ya recorridas son
todas lazos ahora: las que se saltaron ya lo eran y contraer no deshace un lazo, y las
que se contrajeron lo son desde que se contrajeron. Así que todas las aristas que no
son lazo están en el resto de la baraja. Segundo, dado lo que ya se recorrió, el resto
de la baraja está en un orden uniforme, así que la primera arista del resto que no es
lazo es cualquiera de las que no lo son con la misma probabilidad.

```{python continue}
def karger(n, aristas, registro=None):
    padre, rango = list(range(n)), [0] * n

    def raiz(x):
        r = x
        while padre[r] != r:
            r = padre[r]
        while padre[x] != r:                       # compresión de caminos
            padre[x], x = r, padre[x]
        return r

    orden = aristas[:]
    random.shuffle(orden)
    vertices = n
    for u, v in orden:
        if vertices == 2:
            break
        a, b = raiz(u), raiz(v)
        if a == b:
            continue                               # un lazo: ya no existe
        if rango[a] < rango[b]:
            a, b = b, a
        padre[b] = a                               # contraer {u, v}
        rango[a] += rango[a] == rango[b]
        vertices -= 1
        if registro is not None:
            registro.append((u, v))
    return [(u, v) for u, v in aristas if raiz(u) != raiz(v)]

random.seed(9)
for _ in range(300):                               # oráculo: la fuerza bruta
    nv = random.randrange(5, 9)                    # vértices
    E = [(v, random.randrange(v)) for v in range(1, nv)]           # un árbol: conexo
    E += [tuple(random.sample(range(nv), 2)) for _ in range(random.randrange(10))]
    lam = corte_bruto(nv, E)
    resultados = [len(karger(nv, E)) for _ in range(300)]
    assert min(resultados) == lam      # puede fallar: (27/28)³⁰⁰ < 3·10⁻⁵ por grafo
print("300 multigrafos: nunca por debajo de λ, y λ apareció entre las 300 corridas de cada uno")
```

El valor devuelto nunca baja de $\lambda$, porque las aristas entre los dos vértices
finales son siempre un corte de $G$. Una sola corrida, en cambio, puede no dar el
mínimo, y la @fig-mc-contraccion muestra una que lo dio, en un grafo de 8 vértices
hecho de dos $K_4$ unidos por dos aristas. Su corte mínimo es el de los dos puentes,
con valor 2, y todos los demás cortes valen al menos 3.

```{python continue}
G8 = ([(u, v) for u in range(4) for v in range(u + 1, 4)]
      + [(u, v) for u in range(4, 8) for v in range(u + 1, 8)] + [(0, 4), (3, 7)])
print(f"m = {len(G8)},  λ = {corte_bruto(8, G8)}")
random.seed(8)
R = 10_000
exito_g8 = sum(len(karger(8, G8)) == 2 for _ in range(R)) / R
print(f"éxito de una corrida en {R} corridas: {exito_g8:.3f}")
```

```{python continue echo=false output=asis}
posicion = {0: (1, 1), 1: (0, 1), 2: (0, 0), 3: (1, 0),
            4: (2, 1), 5: (3, 1), 6: (3, 0), 7: (2, 0)}
semilla = next(s for s in range(100)
               if (random.seed(s) or True) and len(karger(8, G8)) == 2)
random.seed(semilla)
contraidas = []
karger(8, G8, contraidas)
print(F15.contraccion(8, G8, posicion, contraidas, ident="mc-contraccion",
      pie=f"Una corrida de la contracción sobre dos K₄ unidos por dos aristas "
          f"(semilla {semilla}, la primera que acierta). En cada cuadro, en azul grueso, "
          f"la arista que se contrae a continuación; en celeste, las ya contraídas, "
          f"que unen los vértices de un mismo grupo; punteadas, las que se volvieron "
          f"lazos. En el último cuadro, en naranja, el corte devuelto."))
```

Al principio solo 2 de las 14 aristas son del corte. Al contraer, las aristas dentro
de un grupo se vuelven lazos, y la fracción de aristas del corte sube. El peligro está
al final: en la @fig-mc-contraccion, con tres grupos vivos, una arista al azar entre
las que quedan es de un puente con una probabilidad que ya no es pequeña.
La sección siguiente convierte esa observación en una cota.

## 10. La cota $2/(n(n-1))$

**Teorema.** Sea $C$ un corte mínimo de $G$, con $|C| = \lambda$ aristas. La
contracción devuelve exactamente $C$ con probabilidad al menos
$$\frac{2}{n(n-1)}.$$

*Demostración.* Primero, cuándo devuelve $C$. Sean $S$ y $V \setminus S$ los dos lados
de $C$. Si ninguna arista de $C$ se contrae nunca, toda contracción une dos grupos del
mismo lado, y cada grupo queda entero dentro de $S$ o entero dentro de
$V \setminus S$. Al final hay dos grupos, y como los dos lados no son vacíos, los
grupos son exactamente $S$ y $V \setminus S$. Las aristas entre ellos son $C$. Basta
entonces acotar la probabilidad de no contraer nunca una arista de $C$.

Consideremos el paso en que quedan $i$ vértices, con $3 \le i \le n$, suponiendo que
hasta ahí ninguna arista de $C$ se contrajo. Cada vértice $w$ del multigrafo actual es
un grupo $W$ de vértices originales, y sus aristas son las de $G$ con un extremo en $W$
y el otro fuera. **Ese es el paso que se salta**: el grado de $w$ en el multigrafo
contraído es el valor del corte $(W, V \setminus W)$ en $G$, y por eso es al menos
$\lambda$. Contraer no crea cortes nuevos, solo borra algunos. Con $i$ vértices de
grado al menos $\lambda$, el multigrafo tiene al menos $i\lambda/2$ aristas. Las
$\lambda$ aristas de $C$ siguen todas ahí, porque ninguna es un lazo: sus extremos
están en grupos de lados distintos. La arista se elige uniforme, así que
$$\Pr[\text{la arista elegida es de } C] \le \frac{\lambda}{i\lambda/2} = \frac{2}{i}.$$
Encadenando los pasos, cada uno condicionado a que los anteriores no tocaron $C$,
$$\Pr[\text{nunca se contrae } C] \ge \prod_{i=3}^{n}\left(1 - \frac2i\right)
= \prod_{i=3}^{n} \frac{i-2}{i} = \frac{1 \cdot 2 \cdot 3 \cdots (n-2)}{3 \cdot 4 \cdot 5 \cdots n}
= \frac{2}{n(n-1)}.$$
En el producto telescópico sobreviven el $1 \cdot 2$ de arriba y el $(n-1)n$ de
abajo. $\square$

El ejercicio 3 saca de aquí un corolario que no tiene nada de aleatorio: cuántos
cortes mínimos puede tener un grafo como máximo.

¿Es buena la cota? La @fig-mc-karger-exito la compara con lo medido en tres familias.
En el ciclo de $n$ vértices medimos cuántas veces sale un corte **fijado**, el de las
aristas 0 y $n/2$. El ciclo con todas las aristas dobles menos esas dos tiene un único
corte mínimo. Y las dos cliques de $n/2$ vértices unidas por una arista tienen otro,
el puente, desde $n = 6$. (Con $n = 4$ las cliques son aristas sueltas y el grafo es un
camino con tres puentes; por eso la tabla empieza en 6.)

```{python continue}
def ciclo(n):
    return [(i, (i + 1) % n) for i in range(n)]

def ciclo_doble(n):                                # dobles, salvo las aristas 0 y n/2
    return [e for i, e in enumerate(ciclo(n)) for _ in range(1 if i in (0, n // 2) else 2)]

def cliques(n):
    h = n // 2
    return ([(u, v) for u in range(h) for v in range(u + 1, h)]
            + [(u, v) for u in range(h, n) for v in range(u + 1, n)] + [(0, h)])

random.seed(10)
R, tamanos = 3000, [6, 8, 10, 12, 14, 16]
medidas = {"ciclo, corte fijado": [], "ciclo doble": [], "dos cliques": []}
for n in tamanos:
    fijado = sorted([ciclo(n)[0], ciclo(n)[n // 2]])
    medidas["ciclo, corte fijado"].append(
        sum(sorted(karger(n, ciclo(n))) == fijado for _ in range(R)) / R)
    for nombre, g in [("ciclo doble", ciclo_doble), ("dos cliques", cliques)]:
        lam = corte_bruto(n, g(n))
        medidas[nombre].append(sum(len(karger(n, g(n))) == lam for _ in range(R)) / R)
print(" n   cota     " + "  ".join(f"{k:>19}" for k in medidas))
for t, n in enumerate(tamanos):
    print(f"{n:>2}  {2 / (n * (n - 1)):.4f}  "
          + "  ".join(f"{v[t]:>19.4f}" for v in medidas.values()))
```

```{python continue echo=false output=asis}
print(F15.grafica_semilog(
    [("ciclo, corte fijado", list(zip(tamanos, medidas["ciclo, corte fijado"])), F15.OSCURO),
     ("ciclo doble", list(zip(tamanos, medidas["ciclo doble"])), F15.ACENTO),
     ("dos cliques", list(zip(tamanos, medidas["dos cliques"])), F15.ALARMA)],
    ("2/(n(n−1))", [(n, 2 / (n * (n - 1))) for n in tamanos], F15.CALIDO),
    "vértices n", "probabilidad de éxito", ident="mc-karger-exito", y0=-3,
    pie=f"Probabilidad de que una corrida de la contracción devuelva un corte mínimo, "
        f"medida con {R} corridas por punto, contra la cota del teorema. En el ciclo se "
        f"cuenta un corte fijado, el de las aristas 0 y n/2, y la medida cae sobre la "
        f"cota. En las otras dos familias el corte mínimo es único y la cota se queda "
        f"por debajo de lo medido."))
```

En el ciclo, la medida del corte fijado cae sobre la cota, dentro del ruido de 3 000
corridas, y el ejercicio 4 pide la probabilidad exacta. En las otras dos
familias la cota es pesimista. Entre $n = 6$ y $n = 16$, lo medido pasa de 3 a 8 veces
la cota en el ciclo doble, y de 5,6 a 74 veces en las dos cliques.
En las dos cliques el puente es una arista entre unas $n^2/4$, y mientras alguna
clique no esté contraída del todo, sus aristas internas superan al puente por mucho.
La cota tiene que valer para todo grafo, y pagó por el peor.

## 11. Repetir hasta alta probabilidad

Una corrida acierta con probabilidad $p \ge 2/(n(n-1))$, que es poca. Pero el error es,
otra vez, de un solo lado, ahora en el valor: lo devuelto es siempre un corte, así que
su valor nunca es menor que $\lambda$. La regla de amplificación es quedarse con el
**menor** corte de $N$ corridas independientes. Se equivoca solo si las $N$ fallan:
$$\Pr[\text{las } N \text{ fallan}] \le (1 - p)^N \le e^{-pN},$$
donde la segunda desigualdad es $1 - x \le e^{-x}$, que vale para todo $x$ real. Con
$$N = \left\lceil \binom n2 \ln\frac1\delta \right\rceil$$
corridas, $pN \ge \ln(1/\delta)$ y el error es a lo sumo $\delta$. Para $n = 8$ y
$\delta = 0{,}01$ son $\lceil 28 \ln 100 \rceil = 129$ corridas. Lo comprobamos sobre
el grafo de la @fig-mc-contraccion.

```{python continue}
n, delta = 8, 0.01
N = math.ceil(math.comb(n, 2) * math.log(1 / delta))
random.seed(11)
fallos = sum(min(len(karger(n, G8)) for _ in range(N)) != 2 for _ in range(300))
print(f"N = {N} corridas;  la cota garantiza fallo ≤ {delta}")
print(f"fallos en 300 repeticiones del mínimo de {N}: {fallos}")
print(f"si cada corrida acertara solo con la cota: (1 - 2/56)^{N} = {(1 - 2 / 56) ** N:.4f}")
print(f"con el éxito medido de §9: (1 - {exito_g8:.3f})^{N} = {(1 - exito_g8) ** N:.1e}")
```

Ninguna de las 300 repeticiones falló, y no es casualidad: la cota tomaba $p = 1/28$, y
en este grafo una corrida acierta con una probabilidad unas seis veces mayor.

**El costo.** Una corrida baraja $m$ aristas y hace a lo sumo $m$ operaciones de
union-find, más una pasada final por las aristas. Con unión por rango y compresión, el
capítulo 4, §8, acota $m$ operaciones por $O(m \log^* n)$. El total con $N$ corridas
es
$$O\!\left(n^2 \log\tfrac1\delta \cdot m \log^* n\right).$$
Con $\delta = 1/n$, eso es $O(n^2 m \log n \log^* n)$. Los flujos de §8 cuestan
$O(m^2)$, y en un grafo sin aristas paralelas $m \le n^2/2$, así que $O(m^2) = O(n^2 m)$:
la cota de los flujos es menor que la de la contracción repetida, por un factor de al
menos $\log n \log^* n$. Las dos son cotas superiores y no dicen cuánto tarda cada uno en un
grafo dado, pero con lo que el libro tiene, la contracción básica repetida no gana a los
flujos, salvo en multigrafos con $m$ mayor que $n^2 \log n \log^* n$. La contracción
está en este capítulo porque su análisis es la técnica entera en una página.

¿Y si se repite con más cuidado? La debilidad de la cota está al final de la
contracción, cuando quedan pocos vértices y cada paso arriesga $2/i$. Los primeros
pasos casi no arriesgan nada. David Karger y Clifford Stein ("A new approach to the
minimum cut problem", *Journal of the ACM* 43(4):601–640, 1996) aprovechan eso: contraen
hasta que quedan unos $n/\sqrt2$ vértices, dos veces de forma independiente, y siguen
por recursión en cada una de las dos copias. Así la parte barata y segura se hace pocas
veces y la arriesgada se repite. Su algoritmo encuentra el corte mínimo con alta
probabilidad en $O(n^2 \log^3 n)$, que sí es menor que los $O(m^2)$ de los flujos en
grafos densos. El ejercicio 5 escribe y resuelve las dos recurrencias.

La historia no terminó ahí. Karger ("Minimum cuts in near-linear time", *Journal of the
ACM* 47(1):46–76, 2000) dio un algoritmo Monte Carlo en $O(m \log^3 n)$, lineal en el
tamaño del grafo salvo factores polilogarítmicos. Del lado determinista, Stoer y Wagner
("A simple min-cut algorithm", *Journal of the ACM* 44(4):585–591, 1997) dieron uno sin
flujos, y la versión determinista casi lineal llegó mucho después: Kawarabayashi y
Thorup para grafos simples (STOC 2015) y Henzinger, Li, Rao y Wang para grafos con pesos
("Deterministic near-linear time minimum cut in weighted graphs", SODA 2024). Para
grafos con pesos, el tiempo lineal salvo factores polilogarítmicos fue solo aleatorio
durante casi tres décadas.

## 12. Cierre {#monte-carlo-12-cierre}

Los dos algoritmos tienen la misma forma: una corrida barata con fallo acotado para
toda entrada, un error de un solo lado que deja combinar corridas ("no" si alguna dice
"no", el menor de los cortes), y la repetición independiente.

La regla que te llevas: **en un algoritmo Monte Carlo la probabilidad de error es parte
de la garantía, igual que el $O(\cdot)$. Se demuestra para toda entrada, se baja
repitiendo, y la repetición solo funciona con monedas nuevas.** El error plantado de
§6 pasa todas las pruebas naturales y deja el error en $1/2$, con cualquier número de
rondas.

Freivalds es además un ejemplo de algo que vuelve en la Parte III: comprobar una
respuesta puede ser mucho más barato que calcularla. El capítulo 16 define la clase NP
justamente con esa asimetría, con certificados que se verifican en tiempo polinomial.
El capítulo 21 vuelve a usar monedas, esta vez para aproximar MAX-3SAT con una
asignación al azar.

## Resumen {#monte-carlo-resumen}

- Un algoritmo **Monte Carlo** corre en tiempo acotado y puede responder mal, con
  probabilidad a lo sumo $\delta$ para toda entrada: el máximo sobre entradas, la
  probabilidad sobre las monedas.
- **Error de un lado**: una de las respuestas es siempre verdad. **De dos lados**:
  ninguna lo es.
- **Freivalds** compara $A(Br)$ con $Cr$ para $r \in \{0,1\}^n$ al azar, con $3n^2$
  multiplicaciones. Si $AB = C$ dice "sí" siempre; si no, dice "sí" con probabilidad
  $\le 1/2$, por decisiones diferidas. La cota es exacta con una sola entrada mala.
- Con error de un lado, $k$ rondas **independientes** llevan el error a $2^{-k}$.
  Reutilizar el vector lo deja en $1/2$, y las pruebas con muchas entradas malas no lo
  detectan.
- Una respuesta "no" de Freivalds trae un testigo; una respuesta "sí", no.
- El **corte mínimo global** se puede calcular con $n - 1$ flujos máximos desde un
  vértice de grado mínimo, en $O(m^2)$ con Ford-Fulkerson.
- La **contracción de Karger** devuelve un corte mínimo fijado con probabilidad
  $\ge 2/(n(n-1))$, porque cada vértice contraído tiene grado al menos $\lambda$ y una
  arista al azar es del corte con probabilidad $\le 2/i$.
- Barajar las aristas una vez y recorrerlas con union-find, saltando los lazos, elige
  cada vez una arista uniforme entre las que no son lazos.
- $\lceil \binom n2 \ln(1/\delta) \rceil$ corridas, quedándose con el menor corte, dan
  error $\le \delta$, en $O(n^2 m \log^* n \log(1/\delta))$.

## Ejercicios {#monte-carlo-ejercicios}

1. En la ronda de Freivalds, sortea cada $r_j$ uniforme e independiente en
   $\{0, 1, \dots, q-1\}$ en lugar de $\{0, 1\}$. Demuestra que si $AB \ne C$ la ronda
   dice "sí" con probabilidad a lo sumo $1/q$, y da, para cada $q$, una matriz
   $D = AB - C$ con la que la probabilidad es exactamente $1/q$. ¿Qué cambia si todas
   las cuentas se hacen módulo un primo $p \ge q$, y qué hay que suponer entonces sobre
   las entradas de $D$?
2. Calcula cuántas rondas independientes de Freivalds con $r \in \{0,1\}^n$ hacen falta
   para que el error sea menor que $10^{-9}$, y cuántos bits aleatorios gasta eso con
   $n = 1\,000$. Repite la cuenta con la versión del ejercicio 1 y $q = 2^{16}$:
   ¿cuántas rondas y cuántos bits? Comprueba con código cada desigualdad que decide un
   número de rondas, la de $k$ y la de $k - 1$.
3. Usa el teorema de §10 para demostrar que un multigrafo conexo de $n$ vértices tiene
   a lo sumo $n(n-1)/2$ cortes mínimos distintos. Para cada $n \ge 3$, da un grafo que
   tenga exactamente esa cantidad y demuéstralo.
4. Enumera con código los $5!$ órdenes de las aristas del ciclo de 5 vértices y corre
   la contracción con cada uno. ¿Con qué probabilidad devuelve un corte mínimo? ¿Con
   qué probabilidad devuelve el corte formado por dos aristas dadas? Demuestra las dos
   respuestas para el ciclo de $n$ vértices y compáralas con la cota de §10. ¿Se puede
   mejorar la cota del teorema, tal como está enunciado?
5. ★ Karger y Stein proponen lo siguiente. Si $n \le 6$, se resuelve por fuerza bruta.
   Si no, sea $t = \lceil 1 + n/\sqrt2 \rceil$: se contrae al azar hasta que quedan $t$
   vértices, dos veces de forma independiente, se aplica el algoritmo por recursión a
   cada uno de los dos multigrafos y se devuelve el menor de los dos cortes. (a)
   Demuestra que un corte mínimo fijado sobrevive a una contracción hasta $t$ vértices
   con probabilidad al menos $1/2$. (b) Suponiendo que contraer hasta $t$ vértices
   cuesta $O(n^2)$, escribe la recurrencia del tiempo y resuélvela. (c) Escribe una
   recurrencia para $P(n)$, la probabilidad de devolver un corte mínimo fijado, y
   demuestra una cota inferior para $P(n)$ en función de $n$. (d) ¿Cuántas repeticiones
   independientes hacen falta para error a lo sumo $1/n$, y cuánto cuesta el total?
   Compáralo con §11.
6. La prueba de Fermat para decidir si un entero impar $n > 2$ es primo elige $a$ al
   azar en $\{1, \dots, n-1\}$ y responde "primo" si $a^{n-1} \equiv 1 \pmod n$. (a)
   Demuestra que si $n$ es primo responde siempre "primo". (b) Comprueba con código que
   $n = 561 = 3 \cdot 11 \cdot 17$ cumple $a^{560} \equiv 1 \pmod{561}$ para todo $a$
   coprimo con 561, y calcula la probabilidad exacta de que la prueba declare primo a
   561. (c) Busca con código todos los compuestos impares menores que 20 000 con la
   misma propiedad, y para cada uno calcula esa probabilidad. ¿Cómo cambia con $n$?
   El teorema de §5 usa una cota del error de una ronda que vale para toda entrada.
   ¿Qué le pasa a la cantidad de rondas que pide un error de $10^{-9}$ si esa cota
   depende de $n$ y se acerca a 1?
7. Te dan dos polinomios $P$ y $Q$ en las variables $x_1, \dots, x_m$, cada uno como
   una expresión con sumas, restas y productos, por ejemplo
   $\big((x_1 + x_2)(x_1 - x_3) + x_2 x_3\big)\,(x_1 + x_2 + x_3)$, de largo $s$ y grado
   total a lo sumo $d$. Expandirlos puede producir un número exponencial de términos.
   Usa sin demostrar el lema de Schwartz-Zippel (J. T. Schwartz, *Journal of the ACM*
   27(4):701–717, 1980; R. Zippel, EUROSAM 1979): si $R$ es un polinomio no nulo de
   grado total $d$ sobre un cuerpo, y $r_1, \dots, r_m$ se eligen uniformes e
   independientes en un conjunto finito $S$ del cuerpo, entonces
   $\Pr[R(r_1, \dots, r_m) = 0] \le d/|S|$. Diseña un algoritmo Monte Carlo que decida
   si $P = Q$ como polinomios: di de qué lado es el error, cuánto cuesta en función de
   $s$, y qué tamaño de $S$ y cuántas rondas pides para error a lo sumo $10^{-6}$. ¿Por
   qué Freivalds es un caso particular, y con qué $d$?
8. Alicia tiene un archivo de $n$ bits, que lee como un entero $x < 2^n$, y Beto otro,
   $y$, en otra ciudad. Quieren saber si $x = y$ sin enviar el archivo. Alicia elige
   un primo $p$ uniforme entre los primos menores o iguales que $T$ y le envía a Beto $p$ y
   $x \bmod p$; Beto responde "iguales" si $y \bmod p$ coincide. (a) ¿De qué lado es el
   error? (b) Demuestra que si $x \ne y$, a lo sumo $n$ primos dividen a $x - y$, y
   acota el error en función de $n$ y del número $\pi(T)$ de primos menores o iguales
   que $T$.
   (c) Con una criba, comprueba que $\pi(T) \ge T / \ln T$ para todo $T$ entre 17 y
   $2 \cdot 10^7$, y úsalo para elegir $T$ de modo que el error sea a lo sumo $1/n$
   con $n = 1\,000$. (d) Suponiendo que esa desigualdad vale para todo $T \ge 17$,
   ¿cuántos bits viajan, en función de $n$?
9. La prueba de Miller-Rabin para un impar $n > 3$ escribe $n - 1 = 2^s d$ con $d$
   impar, elige $a$ al azar en $\{2, \dots, n-2\}$ y calcula $x = a^d \bmod n$. Si
   $x = 1$ o $x = n - 1$, responde "primo". Si no, eleva $x$ al cuadrado hasta $s - 1$
   veces, y responde "primo" si en algún momento obtiene $n - 1$; si nunca, responde
   "compuesto". Impleméntala con `pow(a, d, n)`, y compara su respuesta con 10 rondas
   independientes contra una criba de Eratóstenes para todo $n$ impar con
   $5 \le n < 10^6$. Después, para cada compuesto impar menor que $10^4$, calcula la fracción
   exacta de bases $a \in \{2, \dots, n-2\}$ que lo declaran primo. ¿Cuál es la
   mayor fracción, y en qué $n$? ¿Qué hacen los compuestos del ejercicio 6 con esta prueba?
10. Supón un algoritmo para un problema de decisión con error de dos lados: con
    probabilidad a lo sumo $1/3$ responde "sí" cuando la respuesta es "no", y con
    probabilidad a lo sumo $1/3$ responde "no" cuando es "sí". (a) Muestra con un
    ejemplo concreto que la regla de §7, "no si alguna ronda dice no", puede llevar el
    error hacia 1 cuando crece el número de rondas $k$. (b) Propón la regla de la
    mayoría sobre $k$ rondas independientes, con $k$ impar, y demuestra una cota de su
    error de la forma $c^k$ con $c < 1$, acotando la cola de una binomial término a
    término. (c) ¿Cuántas rondas pide tu cota para error menor que $10^{-9}$? (d) ¿Qué
    pasa con tu cota si el error de cada ronda es $1/2 - \varepsilon$ en lugar de
    $1/3$?
