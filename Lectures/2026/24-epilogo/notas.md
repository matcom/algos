# Epílogo: problemas abiertos {.unnumbered #epilogo}

*Redactado el 13 de noviembre de 2026. Cada afirmación sobre el estado del arte se
comprobó ese día en su fuente primaria: el artículo, las actas, el repositorio o la
página del autor. Lo que no se pudo comprobar no está aquí. Si lees esto más tarde,
algunas de estas preguntas ya tendrán otra respuesta, y alguna de las respuestas
habrá resultado falsa.*

Este epílogo tiene más preguntas que respuestas. Los veintitrés capítulos anteriores
recorrieron el ciclo del capítulo 2 sobre problemas cuyo final se conoce. Aquí
miramos dónde el ciclo todavía no se cerró: las cotas superiores que nadie sabe si se
pueden bajar, las cotas mínimas que nadie sabe demostrar, y las hipótesis con las que
la investigación trabaja mientras tanto.

El momento es raro. Desde finales de septiembre de 2026 hay manuscritos, escritos por
un modelo de lenguaje y publicados por OpenAI, los más viejos fechados el 23 de
septiembre, que dicen resolver varias de las
preguntas que este epílogo iba a dejar abiertas. Algunos vienen con una demostración
verificada por computadora y otros no. Ninguno ha pasado todavía por la revisión de
una revista. Por eso este epílogo empieza por explicar cómo leer una afirmación según
el estado en que esté.

```{python echo=false output=asis}
import math
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # Lectures/2026: figuras.py y figuras_24.py
import figuras_24 as F24
```

## 1. Cómo leer una afirmación

Una afirmación sobre el estado del arte puede estar en tres estados, y cada uno pide
una confianza distinta.

- **Publicada.** Salió en una revista o en las actas de un congreso con revisión,
  como STOC, FOCS o SODA. Alguien que no es el autor leyó la demostración. No es una
  garantía, pero es la base sobre la que trabaja el área.
- **Preprint.** El autor la subió a arXiv o a ECCC. Nadie la revisó todavía. La mayor
  parte de los resultados de este epílogo empezaron así, y los más recientes siguen
  así.
- **Manuscrito sin revisar, con o sin verificación formal.** Es el caso de la
  colección de OpenAI ([github.com/openai/math](https://github.com/openai/math)). En
  la fecha de este epílogo, su README habla de 721 manuscritos agrupados en 373
  familias de resultados, aunque el índice ya numera familias hasta la 378. El README
  dice que los produjo "an unnamed internal OpenAI model", que
  hay que entenderlos "as a form of raw research data, rather than polished academic
  papers", y que alrededor del 42 % de los resultados principales tienen una
  demostración formal en Lean. El historial del repositorio registra, el 7 de
  octubre de 2026, la retirada de tres manuscritos por un error de signo.

¿Qué garantiza una demostración en Lean? Que el enunciado **tal como está escrito en
Lean** se deduce de los axiomas, sin huecos. Lo que no garantiza es que ese enunciado
diga lo que dice el título del artículo. Si el modelo de cómputo está mal codificado,
o una definición es un poco distinta de la usual, la demostración es correcta y el
teorema es otro. Comprobar eso es trabajo de una persona que lea el enunciado formal.
Es la lección del capítulo 3, §11: cada herramienta atrapa una clase de errores.

En lo que sigue, cada resultado lleva su estado. Cuando un resultado es un manuscrito
de OpenAI, lo decimos, y decimos si tiene demostración formal.

## 2. P contra NP y las tres barreras

El capítulo 16, §12, dejó la pregunta abierta, y sigue abierta: en la colección de
OpenAI no encontramos ningún manuscrito sobre ella. Lo que sí se sabe es por qué es difícil.
Hay tres familias enteras de demostraciones de las que se sabe que no pueden
resolverla.

**Relativización.** Theodore Baker, John Gill y Robert Solovay ("Relativizations of
the P =? NP Question", *SIAM Journal on Computing* 4, 1975)
construyeron dos oráculos. Un oráculo es una caja que contesta en un paso si una
cadena está en un conjunto fijo $A$. Con un oráculo $A$ se cumple $P^A = NP^A$, y con
otro $B$ se cumple $P^B \ne NP^B$. Casi todas las demostraciones de la teoría de la
computabilidad, como la diagonalización que demuestra que el problema de la parada es
indecidible, siguen valiendo si a todas las máquinas se les da el mismo oráculo. Una
demostración así de $P \ne NP$ demostraría también $P^A \ne NP^A$, que es falso. Una
de $P = NP$ demostraría $P^B = NP^B$, también falso. Así que la diagonalización sola
no alcanza.

**Pruebas naturales.** Alexander Razborov y Steven Rudich ("Natural Proofs",
*Journal of Computer and System Sciences* 55(1), 1997, pp. 24–35) miraron las cotas
mínimas para circuitos. Las que se conocían seguían todas el mismo patrón: encontrar
una propiedad combinatoria que tienen muchas funciones, que se puede comprobar
rápido, y que ninguna función con circuitos chicos tiene. Demostraron que, si existen
funciones pseudoaleatorias seguras, que es lo que la criptografía supone, una
propiedad así no puede separar P de NP. Una demostración de $P \ne NP$ por ese camino
serviría para romper la criptografía que se cree segura.

**Algebrización.** Scott Aaronson y Avi Wigderson ("Algebrization: A New Barrier in
Complexity Theory", *ACM Transactions on Computation Theory* 1(1), 2009; STOC 2008)
miraron las técnicas que sí escaparon de la relativización, como las que demostraron
$IP = PSPACE$. Esas técnicas usan que una fórmula booleana se puede extender a un
polinomio sobre un cuerpo finito. Definieron una versión de oráculo que también se
extiende así, y demostraron que esas técnicas tampoco resuelven P contra NP.

Las tres barreras dicen que una demostración de $P \ne NP$
tiene que usar algo que no relativice, que no sea natural y que no algebrice.

## 3. La complejidad de grano fino

Mientras P contra NP sigue abierta, una pregunta más modesta tiene mucho trabajo
detrás: si un problema se resuelve en $O(n^2)$ y nadie lo baja, ¿se puede explicar por
qué? La respuesta del área son tres hipótesis, cada una con su familia de problemas
equivalentes bajo reducciones que conservan el exponente.

**3SUM.** Dados $n$ enteros, ¿hay tres que sumen cero? El capítulo 5, §9, dio el
algoritmo cuadrático, la cota mínima $\Omega(n^2)$ de Erickson para un modelo de
árboles de decisión y el algoritmo de Grønlund y Pettie, que baja de $n^2$ en un
factor subpolinomial. El mejor que encontramos es de Timothy Chan ("More
Logarithmic-Factor Speedups for 3SUM, (median,+)-Convolution, and Some Geometric
3SUM-Hard Problems", SODA 2018; *ACM Transactions on Algorithms* 16(1)), con tiempo
$O((n^2/\log^2 n)(\log\log n)^{O(1)})$. La **hipótesis 3SUM** dice que no hay
algoritmo en $O(n^{2-\varepsilon})$ para ningún $\varepsilon > 0$. Anka Gajentaan y
Mark Overmars ("On a class of $O(n^2)$ problems in computational geometry",
*Computational Geometry* 5, 1995) mostraron que muchos problemas de geometría, como
decidir si tres puntos de un conjunto están alineados, son al menos tan difíciles.

La hipótesis habla de enteros grandes, y la herramienta del capítulo 7, §12, muestra
por qué tiene que hacerlo. Si los números están en $[-U, U]$, se codifican como el polinomio
$P(x) = \sum_i x^{a_i + U}$, y el coeficiente de $x^{3U}$ en $P(x)^3$ cuenta las ternas
ordenadas $(i, j, k)$ con $a_i + a_j + a_k = 0$. Ese cubo cuenta también las ternas con
índices repetidos, y hay que restarlas. Las que tienen exactamente dos índices iguales
las cuenta $P(x^2)P(x)$, y las que tienen los tres iguales, $P(x^3)$. Por inclusión y
exclusión, las ternas de índices distintos son

$$[x^{3U}]\left(P(x)^3 - 3P(x^2)P(x) + 2P(x^3)\right).$$

El código multiplica polinomios con enteros de Python: cada coeficiente ocupa $B$
bits de un entero grande, con $B$ suficiente para que ninguno desborde en el
siguiente.

```{python continue}
def tres_suma_fuerza_bruta(A):
    n = len(A)
    return any(A[i] + A[j] + A[k] == 0
               for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))

def tres_suma_cuadratica(A):                       # capítulo 5, §9
    B = sorted(A)
    for i in range(len(B) - 2):
        j, k = i + 1, len(B) - 1
        while j < k:
            s = B[i] + B[j] + B[k]
            if s == 0:
                return True
            j, k = (j + 1, k) if s < 0 else (j, k - 1)
    return False

def ternas_por_polinomios(A, U, con_triples=True):
    """A: enteros distintos en [-U, U]. Ternas ordenadas de índices distintos."""
    B = 3 * len(A).bit_length() + 2                # n^3 cabe en B bits
    e = [a + U for a in A]                         # exponentes en [0, 2U]
    P1 = sum(1 << (B * x) for x in e)
    P2 = sum(1 << (B * 2 * x) for x in e)
    P3 = sum(1 << (B * 3 * x) for x in e)
    coef = lambda N: (N >> (B * 3 * U)) & ((1 << B) - 1)
    return coef(P1 ** 3) - 3 * coef(P2 * P1) + (2 * coef(P3) if con_triples else 0)

random.seed(24)
casos = acuerdos = exactas = rotas = 0
for _ in range(400):
    n = random.randint(3, 12)
    U = random.randint(n, 40)
    A = random.sample(range(-U, U + 1), n)
    fb = tres_suma_fuerza_bruta(A)
    t = ternas_por_polinomios(A, U)
    contadas = sum(1 for i in range(n) for j in range(n) for k in range(n)
                   if len({i, j, k}) == 3 and A[i] + A[j] + A[k] == 0)
    casos += 1
    exactas += t == contadas
    rotas += ternas_por_polinomios(A, U, con_triples=False) != contadas
    acuerdos += (tres_suma_cuadratica(A) == fb) and ((t > 0) == fb)
print(f"{casos} instancias: cuenta exacta en {exactas}, las tres respuestas "
      f"coinciden en {acuerdos}; sin el término 2P(x^3) falla en {rotas}")
```

Las 400 instancias dan la cuenta exacta. Una comprobación así solo vale si puede
fallar, y por eso el bloque también la rompe: sin el término $2P(x^3)$ falla en 68 de
las 400 instancias, las que tienen un 0 en la entrada.

El costo es el de una multiplicación de polinomios de grado $O(U)$. Con la FFT del
capítulo 7 son $O(n + U \log U)$ operaciones sobre coeficientes, y cuando
$U = O(n)$ eso es $O(n \log n)$, mucho menos que $n^2$. Python multiplica enteros
con Karatsuba (capítulo 6), no con la FFT, así que este código no tiene ese costo. Con la FFT, el tiempo $O(n + U \log U)$ es
subcuadrático mientras $U \le n^{2-\varepsilon}$, así que la hipótesis 3SUM solo puede
ser cierta para números de al menos unos $2 \log_2 n$ bits.

**Caminos mínimos entre todos los pares (APSP).** Floyd-Warshall cuesta $O(n^3)$.
Ryan Williams ("Faster all-pairs shortest paths via circuit complexity", STOC 2014;
*SIAM Journal on Computing* 47, 2018) lo bajó a $n^3 / 2^{\Omega(\sqrt{\log n})}$,
que es menos que $n^3/\log^c n$ para toda constante $c$ y más que
$n^{3-\varepsilon}$ para todo $\varepsilon > 0$. La **hipótesis APSP** dice que no hay
$O(n^{3-\varepsilon})$. Virginia Vassilevska Williams y Ryan Williams ("Subcubic
Equivalences Between Path, Matrix, and Triangle Problems", FOCS 2010; *Journal of the
ACM* 65, 2018) demostraron que APSP, el producto de matrices en el semianillo
$(\min, +)$ y decidir si un grafo con pesos tiene un triángulo de peso negativo son
equivalentes: si uno baja de $n^3$ por un factor polinomial, bajan todos.

**SETH.** El capítulo 20, §12, la definió: para todo $\varepsilon > 0$ hay un $k$ tal
que $k$-SAT no se resuelve en $O(2^{(1-\varepsilon)n})$. De ella salen cotas
condicionales para problemas polinomiales. Arturs Backurs y Piotr Indyk ("Edit
Distance Cannot Be Computed in Strongly Subquadratic Time (unless SETH is false)",
STOC 2015; *SIAM Journal on Computing* 47, 2018) demostraron que si la distancia
de edición entre dos cadenas de largo $n$ se calcula en $O(n^{2-\delta})$, entonces la
satisfacibilidad de una fórmula en forma normal conjuntiva con $N$ variables y $M$
cláusulas se decide en $M^{O(1)} 2^{(1-\varepsilon)N}$. La tabla cuadrática de la
distancia de edición, prima de la subsecuencia común del capítulo 12, §8, sería
entonces casi óptima.

Ninguno de estos resultados dice "este problema no se puede resolver más rápido".
Dicen "si este se resuelve más rápido, aquel también": son reducciones como las del
capítulo 16 con el exponente medido, y valen lo que vale su hipótesis. La sección
siguiente es lo que pasa cuando una de ellas cae.

## 4. Un manuscrito que refuta la ETH (octubre de 2026)

El capítulo 20, §12, definió para cada $k$ el número $s_k$, el ínfimo de los $\delta$
para los que $k$-SAT se resuelve en $O(2^{\delta n})$, y la **hipótesis del tiempo
exponencial** (ETH): $s_3 > 0$. El teorema 8 de ese capítulo dedujo de ella que
conjunto independiente no se resuelve en $2^{o(N)}$.

El 26 de octubre de 2026 OpenAI agregó a su colección el manuscrito "The Exponential
Time Hypothesis is False", fechado el 25 de octubre. El resumen promete un algoritmo
determinista que **cuenta** las asignaciones que satisfacen una fórmula $k$-CNF con
$n$ variables y $m$ cláusulas, para todo $k \ge 2$ fijo, en tiempo

$$(n + m)^{O_k(1)} \, 2^{n / (\log n)^{1/2 + o(1)}}$$

y con memoria polinomial. Como $(\log n)^{1/2+o(1)} \to \infty$, el exponente es $o(n)$, y eso da $s_3 = 0$. El
resultado tiene demostración en Lean. Según su documentación, lo que Lean demuestra
es una cota algo más débil, $(L+1)^{O_k(1)} 2^{O_k(n (\log \log n)^2 / \sqrt{\log n})}$
con $L$ el largo de la codificación, que también es $2^{o(n)}$ y basta para refutar
la ETH. El historial del repositorio dice que un grupo de trabajo encabezado por
Russell Impagliazzo y Ramamohan Paturi, que propusieron la hipótesis, y por Ryan
Williams, examinará y explicará la demostración, y que el material se hizo público
enseguida a pedido del grupo. En la fecha de este epílogo no encontramos un informe
de ese grupo.

Supongamos que es correcto, y miremos qué cambia y qué no.

**SETH cae también.** Una fórmula de $k$-CNF con $n$ variables tiene a lo sumo
$(2n)^k$ cláusulas distintas, así que $m$ es polinomial en $n$ para $k$ fijo y el
factor $(n+m)^{O_k(1)}$ es $2^{O_k(\log n)}$. El tiempo total es
$2^{O_k(\log n) + n/(\log n)^{1/2+o(1)}} = 2^{o(n)}$, y eso da $s_k = 0$ para **todo**
$k$. Entonces $s_\infty = 0$, y SETH, que dice $s_\infty = 1$, es falsa.

**Las reducciones no caen.** El teorema 8 del capítulo 20 sigue siendo un teorema: es
una implicación con hipótesis falsa, y no dice nada. Para conjunto independiente no
se obtiene ningún algoritmo en $2^{o(N)}$, porque la reducción va de 3-SAT a conjunto
independiente, en la dirección contraria. Lo mismo pasa con Backurs e Indyk. Su
enunciado habla de fórmulas CNF **sin cota en el ancho de las cláusulas**, y el
algoritmo nuevo es para $k$ fijo, con un exponente del polinomio que crece con $k$.
Que CNF-SAT general no se resuelva en $M^{O(1)} 2^{(1-\varepsilon)N}$ es una hipótesis
más débil que SETH, y el manuscrito no dice nada sobre ella. La cota condicional para
la distancia de edición sigue en pie con esa hipótesis, mientras nadie la refute.

**Sigue siendo exponencial, y es galáctico.** $2^{n/\sqrt{\log n}}$ crece más rápido
que cualquier polinomio, así que nada de esto toca P contra NP. ¿Y desde qué $n$
empieza a ganarle a $2^{\delta n}$? El $o(1)$ del resumen no es un misterio: según la
documentación de Lean, el manuscrito demuestra en detalle
$2^{O_k(n \log\log n / \sqrt{\log n})}$, y lo formalizado es
$2^{O_k(n (\log\log n)^2 / \sqrt{\log n})}$. Lo que ninguno de los dos da es la
constante escondida en el $O_k$. Tomemos 1 solo para tener números: la constante no se
conoce, y puede ser mayor o menor, y hasta la base del logaritmo la mueve. La misma
documentación da una cota mejor para fórmulas ralas, con $m \le Dn$ y $D$ fijo:
$2^{O_{k,D}(n / \sqrt{\log n})}$, sin el $\log\log n$. Buscamos el primer $n$ con
exponente a lo sumo $\delta n$:

```{python continue}
def exponente(n, potencia):          # fracción de n en el exponente, constante 1
    L = math.log2(n)
    return math.log2(L) ** potencia / math.sqrt(L)

def desde(potencia, delta):          # menor log2 n, en pasos de 1 %, con exponente <= delta n
    L = 16.0
    while math.log2(L) ** potencia / math.sqrt(L) > delta:
        L *= 1.01
    return L

for potencia, cual in ((0, "ralas"), (1, "manuscrito"), (2, "Lean")):
    print(f"{cual}: con n = 10^6 el exponente es {exponente(10**6, potencia):.3f} n; "
          f"le gana a 2^(n/10) desde log2 n ≈ {desde(potencia, 0.1):.3g}")
```

Con constante 1 y un millón de variables, la cota general da $0{,}967\,n$, casi la
fuerza bruta, la formalizada da $4{,}174\,n$, peor que la fuerza bruta, y la de
fórmulas ralas, $0{,}224\,n$. Para ganarle a $2^{n/10}$ hacen falta
$\log_2 n \approx 101$, $2{,}07 \cdot 10^4$ y $4{,}1 \cdot 10^7$ respectivamente.
Con una constante mayor que 1 los umbrales suben, y con una menor bajan. Como la
constante no se conoce, no hay ningún tamaño de fórmula
para el que se pueda afirmar que este algoritmo ahorra algo. Lo que cambió es el mapa
de lo que se puede demostrar, no los programas que usamos para resolver SAT.

El manuscrito saca además una consecuencia que va en la dirección contraria. De un
algoritmo rápido para contar deduce una cota mínima: cotas superlineales para
circuitos que calculan cierto lenguaje de $\mathsf{E}^{\mathsf{NP}}$, en infinitas
longitudes de la entrada. Un algoritmo mejor permite demostrar una cota mínima.

**Pregunta.** Si la demostración resiste, ¿qué hipótesis de grano fino quedan en pie,
y cuáles de las cotas condicionales que conoces se pueden volver a demostrar desde
ellas?

## 5. Problemas clásicos que se movieron

Cuatro resultados recientes vuelven sobre capítulos de este libro. Los cuatro están
publicados en actas con revisión.

**Flujo máximo en tiempo casi lineal.** El capítulo 13 terminó con él: Li Chen,
Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg y Sushant Sachdeva
("Maximum Flow and Minimum-Cost Flow in Almost-Linear Time", FOCS 2022; *Journal of
the ACM* 72(3), 2025) calculan un flujo máximo y uno de costo mínimo exactos en
$m^{1+o(1)}$, con capacidades y costos enteros acotados por un polinomio. Dinic
(capítulo 13) y push-relabel (capítulo 14) aumentan el flujo por caminos o lo empujan
por aristas. Este algoritmo construye el flujo con $m^{1+o(1)}$ ciclos aproximados de
razón mínima, y cada uno cuesta $m^{o(1)}$ amortizado gracias a una estructura de
datos dinámica sobre el grafo. El análisis amortizado del capítulo 4 está en el
centro del resultado.

**Caminos mínimos por debajo de la barrera del ordenamiento.** Dijkstra con un
montículo de Fibonacci cuesta $O(m + n \log n)$, y si devuelve los vértices en orden
de distancia, ordena $n$ números. El capítulo 5 dice que ordenar con comparaciones
cuesta $\Omega(n \log n)$, así que **esa versión** de Dijkstra no puede mejorar. Pero
el problema pide las distancias, no el orden. Ran Duan, Jiayi Mao, Xiao Mao, Xinkai
Shu y Longhui Yin ("Breaking the Sorting Barrier for Directed Single-Source Shortest
Paths", STOC 2025, premio al mejor artículo, arXiv 2504.17033) dan un
algoritmo determinista en $O(m \log^{2/3} n)$ para grafos dirigidos con pesos reales
no negativos, en el modelo de comparaciones y sumas. Es el primero que le gana a
Dijkstra en grafos ralos. En febrero de 2026, Duan, Mao, Shu y Yin ("A Faster
Directed Single-Source Shortest Path Algorithm", arXiv 2602.07868, ICALP 2026)
bajaron a $O(m \sqrt{\log n} + \sqrt{mn \log n \log\log n})$. Es la lección del
capítulo 5, §9: una cota mínima viene con su modelo pegado, y también con el problema
exacto que resuelve.

**Dijkstra es universalmente óptimo.** Bernhard Haeupler, Richard Hladík, Václav
Rozhoň, Robert Tarjan y Jakub Tětek ("Universal Optimality of Dijkstra via
Beyond-Worst-Case Heaps", FOCS 2024, uno de los premios al mejor artículo) demostraron
algo que parece contradecir lo anterior y no lo hace. Fija un grafo y deja que un
adversario elija los pesos. Un algoritmo es **universalmente óptimo** si en **cada**
grafo hace, salvo una constante, lo mismo que el mejor algoritmo posible para ese
grafo. Es más fuerte que la optimalidad en el peor caso, que solo compara en el peor
grafo. Dijkstra, con un montículo nuevo cuyo costo de extraer el mínimo depende de
cuántos elementos entraron después que él, es universalmente óptimo para el problema
de **ordenar** los vértices por distancia. Por eso no choca con Duan y otros, que no
ordenan.

**Tiempo en espacio de raíz cuadrada.** El capítulo 1, §3 y §6, presentó la máquina
de Turing y la relación entre tiempo y memoria. Ryan Williams ("Simulating Time with
Square-Root Space", STOC 2025, pp. 13–23; *Journal of the ACM* 73(3), 2026) demostró que toda máquina de Turing de
varias cintas que corre en tiempo $t \ge n$ se simula en espacio
$O(\sqrt{t \log t})$. La mejor simulación anterior, de Hopcroft, Paul y Valiant
(1975), usaba espacio $O(t/\log t)$. Como corolario hay problemas explícitos que se
resuelven en espacio $O(n)$ y que piden tiempo $n^{2-\varepsilon}$ en una máquina de
varias cintas, para todo $\varepsilon > 0$. La pregunta 7 vuelve sobre esa cota
mínima sin condiciones.

## 6. El exponente de la multiplicación de matrices

El capítulo 5 citó a Strassen ("Gaussian elimination is not optimal", *Numerische
Mathematik* 13, 1969), que multiplica matrices de $n \times n$ con siete productos
por bloque de $2 \times 2$, en $O(n^{\log_2 7})$. El **exponente de la multiplicación
de matrices** $\omega$ es el ínfimo de los $c$ para los que se pueden multiplicar en
$O(n^c)$ operaciones aritméticas. Leer la entrada da $\omega \ge 2$, y nadie sabe si
$\omega = 2$.

Hay dos maneras de bajar el exponente. La primera es la de Strassen: un esquema fijo
para un bloque chico, aplicado por recursión. Un esquema de $r$ productos para bloques
de $k \times k$ da exponente $\log_k r$. En 2025 AlphaEvolve, un sistema de Google
DeepMind que modifica programas con un modelo de lenguaje y se queda con los que
mejor puntúa un evaluador automático (Novikov y otros, "AlphaEvolve: A coding agent
for scientific and algorithmic discovery", arXiv 2506.13131), encontró un esquema
para matrices complejas de $4 \times 4$ con 48 productos. Strassen aplicado dos veces
usa 49. Jean-Guillaume Dumas, Clément Pernet y Alexandre Sedoglavic ("A
non-commutative algorithm for multiplying 4x4 matrices using 48 non-complex
multiplications", arXiv 2506.13242) lo llevaron a coeficientes racionales, válido en
cualquier anillo de característica distinta de 2.

```{python continue}
print(f"Strassen: log2 7 = {math.log2(7):.4f}   49 para 4x4: log4 49 = {math.log(49, 4):.4f}"
      f"   48 para 4x4: log4 48 = {math.log(48, 4):.4f}")
for k in (1, 5, 10):
    print(f"n = 4^{k:<2} = {4**k:>8}: 49^k = {49**k:.3e}, 48^k = {48**k:.3e}, "
          f"razón {(48 / 49)**k:.3f}")
```

El esquema de 48 sí se puede usar: con $n = 4^{10}$, un poco más de un millón, hace
el 81 % de los productos. Pero su exponente, $2{,}7925$, está muy lejos de las cotas
que da la segunda manera.

La segunda manera es el **método láser**, que no construye un esquema chico sino que
analiza potencias de un tensor fijo, el de Coppersmith y Winograd, y saca el exponente
de un problema de optimización. Las cotas que da son asintóticas, y los algoritmos
que las alcanzan son galácticos. La tabla tiene las que comprobamos:

```{python continue}
COTAS_OMEGA = [   # (año, cota superior de ω, quién, estado)
    (1969, math.log2(7), "Strassen, 2,8074", "publicada"),
    (1990, 2.376, "Coppersmith y Winograd, 2,376", "publicada"),
    (2024, 2.371552, "Vassilevska Williams, Xu, Xu y Zhou, 2,371552", "publicada"),
    (2025, 2.371339, "Alman, Duan, Vassilevska Williams y otros, 2,371339", "publicada"),
    (2026, 2.371177, "Dupont y otros, con AlphaEvolve, 2,371177", "preprint"),
    (2026, 2.37115924, "Zadeh, 2,37115924", "preprint"),
    (2026, 2.371054886006746, "OpenAI, sobre todo cuerpo, 2,371054886", "sin revisar"),
    (2026, 9 / 4, "OpenAI, sobre ℂ, 9/4", "sin revisar"),
]
for anio, w, quien, estado in COTAS_OMEGA:
    print(f"{anio}  ω < {w:.9f}  {quien}  [{estado}]")
print(f"de 1990 a 2025 bajó {2.376 - 2.371339:.4f}; de 2,371339 a 9/4 son "
      f"{2.371339 - 9 / 4:.3f}")
```

Las fuentes: Coppersmith y Winograd, "Matrix multiplication via arithmetic
progressions", *Journal of Symbolic Computation* 9, 1990; Vassilevska Williams, Xu,
Xu y Zhou, "New Bounds for Matrix Multiplication: from Alpha to Omega", SODA 2024;
Alman, Duan, Vassilevska Williams, Xu, Xu y Zhou, "More Asymmetry Yields Faster Matrix
Multiplication", SODA 2025; Dupont y otros, "Improving the matrix multiplication
exponent with modern optimization and AlphaEvolve", arXiv 2608.16884, agosto de 2026,
entre cuyos autores están Josh Alman y Virginia Vassilevska Williams; Reza Zadeh, "A
faster matrix multiplication algorithm through structured optimization", arXiv
2610.10593, 6 de octubre de 2026; y los manuscritos de OpenAI "Staggered extraction
for exact matrix multiplication over every field", del 24 de septiembre de 2026, y "An
Upper Bound of 9/4 for the Matrix Multiplication Exponent", del 2 de octubre de 2026,
y el enunciado de los dos está formalizado en Lean.

```{python continue echo=false output=asis}
print(F24.omega(COTAS_OMEGA, ident="epi-omega",
      pie="Las cotas superiores de ω de la tabla, por año. Entre 1990 y 2025 el "
          "exponente bajó 0,0047; el manuscrito de OpenAI sobre ℂ lo baja 0,121 de un "
          "golpe. La línea de trazos es la cota mínima trivial. El color dice el "
          "estado de cada cota el 13 de noviembre de 2026."))
```

La @fig-epi-omega muestra lo raro de este momento. De 1990 a 2025 el exponente bajó
menos de cinco milésimas, con el método láser refinado una y otra vez. Manuscritos
de OpenAI del 24 de septiembre y del 2 de octubre lo bajan a $9/4$ sobre los complejos. A diferencia de la
ETH, este resultado ya tiene dos demostraciones escritas por personas. Amir Shpilka
("Exposition of OpenAI's Matrix Multiplication in Exponent 9/4 (and an explicit
algorithm)", ECCC TR26-281, 27 de octubre de 2026) da una demostración elemental y
autocontenida, y algoritmos explícitos de exponente menor que $9/4 + \varepsilon$
para cada $\varepsilon > 0$. Alimzhan Amanov, Maxim van den Berg y Jeroen Zuiddam
("Multiplying matrices via polynomials: exposition and barriers", arXiv 2610.30054,
21 de octubre de 2026) dan otra versión, válida sobre cualquier cuerpo, y demuestran
una barrera: el análisis actual de estas construcciones es óptimo, y para bajar de
$9/4$ con ellas hacen falta técnicas nuevas. Las dos siguen siendo preprints.

Ninguna de estas cotas cambia cómo se multiplican matrices en la práctica. En los
algoritmos explícitos de Shpilka, el tamaño de la matriz base puede llegar a
$2^{(1/\varepsilon)^{O(1)}}$ para exponente $9/4 + \varepsilon$.

**Pregunta.** ¿Es $\omega = 2$? Y si la barrera de Amanov, van den Berg y Zuiddam
dice que estas construcciones no bajan de $9/4$, ¿qué tendría que tener una
construcción nueva?

## 7. Búsqueda automática y algoritmos galácticos

Hay dos maneras de usar una computadora para encontrar un algoritmo.

AlphaEvolve **busca**. Un modelo de lenguaje propone cambios a un programa, un
evaluador automático los puntúa, y el sistema guarda los mejores. Un esquema de
multiplicación se comprueba sin demostrar nada nuevo: que dé el producto correcto es
una identidad entre polinomios que se verifica, y sus productos se cuentan. En la cota
2,371177, AlphaEvolve mejoró el programa de optimización que calcula el exponente, y
el teorema que convierte esa solución en una cota es el del método láser, que ya
estaba demostrado. En los dos casos la correctitud no depende de la búsqueda, y la
búsqueda solo tiene que encontrar algo que pase la comprobación. Es el ciclo del
capítulo 2 con la segunda pregunta automatizada y la tercera reducida a una
comprobación mecánica.

Los manuscritos de OpenAI **demuestran**. El modelo escribe un artículo con su
demostración, y en un 42 % de los casos una demostración en Lean del enunciado
principal. Aquí no hay un evaluador que
puntúe en cada paso. La comprobación es la de Lean, con el límite que vimos en la §1,
o la de una persona que lee el artículo.

¿Cuándo una cota encontrada así es una idea nueva? En el esquema de 48 productos, la
idea que se puede reutilizar salió después, cuando Dumas, Pernet y Sedoglavic
explicaron por qué existe una versión racional. En la cota 2,371177 la idea es del
método láser y la búsqueda ajustó parámetros. Con $9/4$, la técnica y su
alcance los hicieron visibles las dos reescrituras humanas. Un número mejor sin una
explicación que alguien pueda aprender es un resultado, pero todavía no una técnica.

Varios de estos resultados son **galácticos**: mejores asintóticamente e inútiles en
cualquier computadora. Dos manuscritos de OpenAI, sin revisar, lo muestran al
extremo. Uno multiplica enteros de $n$ bits en tiempo $O(n (\log n)^{1-\kappa})$ en
una máquina de Turing de varias cintas, con $\kappa = 2^{-182}$. Eso baja de la cota
$O(n \log n)$ de Harvey y van der Hoeven que citan el capítulo 1, §9, y el capítulo
7, §12, y refutaría la conjetura de Schönhage y Strassen de que $n \log n$ es óptimo
en ese modelo. Ese manuscrito no tiene demostración en Lean. El otro calcula la
transformada discreta de Fourier de largo $n$ en $O(n (\log n)^{1-\delta})$
operaciones con $\delta = 10^{-13}$, con aritmética compleja exacta, y sí tiene
demostración en Lean. ¿Cuánto ahorran?

```{python continue}
print(f"multiplicación: el ahorro (log n)^kappa llega a 2 cuando log2 log2 n = 2^182 "
      f"≈ {2.0**182:.2e}")
print(f"Fourier: el ahorro (log n)^delta llega a 2 cuando log2 log2 n = 10^13")
print(f"con n = 2^64, el factor ahorrado es {2 ** (6 * 2.0**-182):.15f} y "
      f"{2 ** (6 * 1e-13):.15f}")
```

El factor que ahorran, $(\log n)^\kappa$, llega a 2 cuando $\log_2 \log_2 n = 2^{182}$.
Con $n = 2^{64}$, el mayor tamaño que se puede direccionar con una palabra de 64 bits,
el factor de la multiplicación es 1 en las quince cifras que imprime el código, y el
de Fourier se separa de 1 en la decimotercera. Si las demostraciones son correctas,
estos resultados cambian lo que sabemos sobre los modelos de los capítulos 1 y 7, y
no cambian ningún programa.

## 8. Juegos únicos y los umbrales de aproximación

El capítulo 21 dio una 2-aproximación para vertex cover, y el capítulo 23, §12, dijo
dónde estaba la imposibilidad: aproximarlo con razón $\sqrt 2 - \varepsilon$ es
NP-duro por el teorema de Khot, Minzer y Safra (*Annals of Mathematics* 198(1),
2023), y "entre $\sqrt 2$ y 2 no se sabe".

Subhash Khot ("On the power of unique 2-prover 1-round games", STOC 2002) propuso la
**conjetura de los juegos únicos**. Un juego único es un sistema de restricciones
sobre un alfabeto finito, una por arista de un grafo, donde cada restricción es una
biyección: el valor de un extremo fija el del otro. Decidir si **todas** se pueden
satisfacer es fácil, porque basta fijar un vértice y propagar. La conjetura dice que,
para todo $\varepsilon, \delta > 0$, es NP-duro distinguir los juegos donde se puede
satisfacer una fracción $1 - \varepsilon$ de las restricciones de los juegos donde no
se puede satisfacer más de $\delta$. Si es cierta, decide el umbral exacto de varios
problemas: vertex cover no tiene razón $2 - \varepsilon$, y para corte máximo la razón
$\alpha_{GW}$ de Goemans y Williamson ("Improved approximation algorithms for maximum
cut and satisfiability problems using semidefinite programming", *Journal of the ACM*
42, 1995) es óptima.

```{python continue}
alfa = min((2 / math.pi) * t / (1 - math.cos(t))
           for t in (i * math.pi / 200000 for i in range(1, 200001)))
print(f"alfa_GW = min sobre theta de (2/pi) theta / (1 - cos theta) ≈ {alfa:.5f}")
```

En la colección de OpenAI está "The Unique Games Theorem", fechado el 23 de septiembre
de 2026: una reducción
determinista y polinomial de 3-SAT a juegos únicos sobre un alfabeto fijo, con
completitud al menos $1 - \varepsilon$ y solidez a lo sumo $\delta$, para todo
$\varepsilon, \delta \in (0, 1/2)$ fijos. Con ella vienen demostraciones directas de
que aproximar vertex cover con cualquier razón fija menor que 2 es NP-duro, y de que
aproximar corte máximo mejor que $\alpha_{GW}$ también. Todo tiene demostración en
Lean, y el repositorio incluye un resumen del razonamiento del modelo para esta
familia de resultados.

Si es correcto, la 2-aproximación del capítulo 21, §3, que es el emparejamiento
maximal que cualquiera inventa en una tarde, es la mejor posible salvo que P = NP. Y
el capítulo 23, §12, tendría que decir que ya se sabe.

**Pregunta.** ¿Qué otros umbrales de aproximación, que hoy dependen de la conjetura,
pasarían a ser teoremas?

## 9. Lo que el libro no trató

Para cada área, qué estudia y un resultado comprobado por donde empezar.

- **Algoritmos en línea y análisis competitivo.** El capítulo 9, §11, lo rozó con la
  caché: el algoritmo recibe la entrada de a poco y se compara con el mejor que la
  conoce entera. El problema de los $k$ servidores es su pregunta clásica, y la
  colección de OpenAI tiene un manuscrito, sin revisar y con demostración en Lean, que
  da razón competitiva aleatoria $O(\log^2 k)$ en todo espacio métrico.
- **Streaming y algoritmos sublineales.** El algoritmo ve los datos una vez y guarda
  mucho menos que la entrada. Noga Alon, Yossi Matias y Mario Szegedy ("The space
  complexity of approximating the frequency moments", STOC 1996; *Journal of Computer
  and System Sciences* 58, 1999) fundaron el área.
- **Algoritmos con predicciones.** El algoritmo recibe una predicción, por ejemplo de
  un modelo aprendido, que puede estar mal. Se le pide que sea casi óptimo si la
  predicción es buena y que no empeore mucho si es mala. Thodoris Lykouris y Sergei
  Vassilvitskii ("Competitive Caching with Machine Learned Advice", *Journal of the ACM* 68,
  2021) lo hicieron con la caché del capítulo 9.
- **Análisis suavizado.** El capítulo 22, §11, usó el simplex sin explicar por qué
  funciona. Victor Klee y George Minty ("How good is the simplex algorithm?")
  construyeron poliedros donde la regla de pivote de Dantzig visita exponencialmente
  muchos vértices, y sin embargo el simplex es rápido en la práctica. Daniel Spielman
  y Shang-Hua Teng ("Smoothed analysis of algorithms: Why the simplex algorithm usually
  takes polynomial time", STOC 2001; *Journal of the ACM* 51, 2004) lo explicaron
  para una variante del simplex: si a los datos de un programa lineal cualquiera se les suma un ruido gaussiano de
  desviación $\sigma$, el número esperado de pasos es polinomial en el tamaño y en
  $1/\sigma$. Eleon Bach
  y Sophie Huiberts ("Optimal Smoothed Analysis of the Simplex Method", FOCS 2025)
  dan una variante cuya cota es de $O(\sigma^{-1/2} d^{11/4} \log(n)^{7/4})$ pasos de pivote, con $d$
  variables y $n$ restricciones, y demostraron que la dependencia en $\sigma$ es
  óptima salvo factores polilogarítmicos.
- **Algoritmos paralelos y distribuidos.** El costo se mide en profundidad o en
  rondas de comunicación. El RNC del título de Karger (capítulo 15) es una clase de
  algoritmos paralelos aleatorios.
- **Algoritmos cuánticos.** Peter Shor ("Polynomial-Time Algorithms for Prime
  Factorization and Discrete Logarithms on a Quantum Computer", FOCS 1994; *SIAM
  Journal on Computing* 26, 1997) factoriza enteros en tiempo polinomial en una
  computadora cuántica, y Lov Grover ("A fast quantum mechanical algorithm for database
  search", STOC 1996) busca en una lista de $N$ elementos sin estructura con
  $O(\sqrt N)$ consultas.
- **Complejidad en el caso promedio.** El capítulo 8, §7, separó costo esperado de
  costo promedio. Cuándo un problema es difícil para entradas al azar es la pregunta
  de la que depende la criptografía.

## 10. El ciclo, otra vez

El capítulo 2 propuso cinco preguntas y un ciclo: el problema, el algoritmo, la
correctitud, el costo y si se puede hacer mejor. Los resultados de este epílogo son
vueltas completas del mismo ciclo, hechas por gente que aprendió lo que este libro
enseña.

Duan y sus coautores empezaron por la quinta pregunta. La cota $\Omega(n \log n)$ de
Dijkstra era real, pero era la cota de otro problema, el de ordenar, y releer el
enunciado abrió el camino. La refutación de la ETH responde la quinta pregunta en
contra de lo que casi todos creían, y obliga a releer cuáles cotas condicionales
dependían de esa hipótesis y cuáles de otra más débil. La cota $9/4$ recorrió el
ciclo en un orden nuevo: primero el resultado, con una demostración formal, y
después personas que la reescribieron para entender qué técnica se había usado.

La regla del epílogo extiende la del capítulo 5: **una cota viene con su modelo y su
hipótesis pegados, y con el estado de su demostración.** Antes de usar una cota,
pregunta en qué modelo vale, de qué hipótesis depende y quién comprobó la
demostración.

## Resumen {#epilogo-resumen}

- Las tres barreras (relativización, pruebas naturales y algebrización) descartan
  familias enteras de demostraciones de $P \ne NP$. Ninguna dice que la pregunta no
  tenga respuesta.
- La complejidad de grano fino explica por qué algunos algoritmos polinomiales no
  mejoran, con reducciones que conservan el exponente desde 3SUM, APSP y SETH. Sus
  resultados son implicaciones, y valen lo que vale su hipótesis.
- 3SUM con números chicos se resuelve rápido con polinomios (capítulo 7). La hipótesis
  3SUM es sobre números grandes.
- Un manuscrito de OpenAI de octubre de 2026, con demostración en Lean y todavía sin
  revisión, refuta la ETH, y con ella SETH. El algoritmo sigue siendo exponencial, y
  con su constante desconocida no se puede afirmar que ahorre nada en ningún tamaño. Las reducciones no caen:
  quedan sin hipótesis, o pasan a depender de una más débil.
- Flujo máximo en $m^{1+o(1)}$, caminos mínimos dirigidos más rápidos que Dijkstra en
  grafos ralos, Dijkstra universalmente óptimo para ordenar, y tiempo $t$ en espacio
  $O(\sqrt{t \log t})$ son resultados publicados de 2022 a 2026.
- La cota superior de $\omega$ bajó de 2,376 a 2,371339 entre 1990 y 2025. Un
  manuscrito de OpenAI la baja a $9/4$ sobre los complejos, ya con dos exposiciones
  independientes en preprint.
- Una búsqueda automática con un evaluador garantiza la correctitud de lo que
  encuentra, pero no da por sí misma una técnica que se pueda reutilizar.
- Un algoritmo galáctico es asintóticamente mejor e inútil en la práctica. Con
  $\kappa = 2^{-182}$, el ahorro llega a 2 cuando $\log_2 \log_2 n = 2^{182}$.
- La conjetura de los juegos únicos fija umbrales exactos de aproximación. Un
  manuscrito de OpenAI con demostración en Lean dice demostrarla, y con ella que la
  razón 2 de vertex cover es óptima si P ≠ NP.
- Una cota viene con su modelo, su hipótesis y el estado de su demostración.

## Preguntas para seguir

En lugar de ejercicios, diez preguntas abiertas o recién movidas. Cada una dice dónde
empezar a leer.

1. **¿Se pueden ordenar $n$ enteros de una palabra en $O(n)$ en el modelo RAM?** El
   capítulo 5 demostró $\Omega(n \log n)$ para comparaciones, y el ordenamiento por
   conteo le gana cuando los números son chicos. Para números de una palabra
   arbitrarios, Yijie Han y Mikkel Thorup ("Integer Sorting in
   $O(n\sqrt{\log \log n})$ Expected Time and Linear Space", FOCS 2002) dan tiempo
   esperado $O(n \sqrt{\log\log n})$, y Yijie Han ("Deterministic sorting in
   $O(n \log \log n)$ time and linear space", *Journal of Algorithms* 50),
   $O(n \log\log n)$ determinista. No encontramos un resultado que cierre la
   pregunta. Empieza por el artículo de Han y Thorup.

2. **¿Es $\omega = 2$?** Lee la §6 y después la exposición de Shpilka (ECCC
   TR26-281), que es elemental. La barrera de Amanov, van den Berg y Zuiddam (arXiv
   2610.30054) dice qué tendría que cambiar para bajar de $9/4$.

3. **¿Está isomorfismo de grafos en P?** László Babai ("Graph Isomorphism in
   Quasipolynomial Time", STOC 2016, arXiv 1512.03547) lo resolvió en tiempo
   $\exp((\log n)^{O(1)})$, cuando lo mejor anterior era $\exp(O(\sqrt{n \log n}))$, de
   Luks (1983). Empieza por la introducción del artículo de Babai.

4. **¿Es correcta la demostración de la conjetura de los juegos únicos, y qué
   umbrales de aproximación quedan fijados?** Lee primero la introducción de Khot
   (STOC 2002) y el artículo de Khot, Minzer y Safra (*Annals of Mathematics*
   198(1), 2023). Después "The Unique Games Theorem" en
   [github.com/openai/math](https://github.com/openai/math), con su documentación de
   Lean y el resumen del razonamiento del modelo.

5. **¿Se resuelve 3SUM en $O(n^{2-\varepsilon})$?** Empieza por Chan (SODA 2018) y
   Grønlund y Pettie ("Threesomes, Degenerates, and Love Triangles", FOCS 2014;
   *Journal of the ACM* 65, 2018), y pregúntate por qué el truco de la §3 no
   escala a números de $3 \log_2 n$ bits.

6. **¿Hay un algoritmo determinista de corte mínimo global tan simple como el de
   Karger?** El capítulo 15 dio la contracción al azar. Los deterministas existen:
   Ken-ichi Kawarabayashi y Mikkel Thorup ("Deterministic Edge Connectivity in
   Near-Linear Time", *Journal of the ACM* 66; en STOC 2015, "Deterministic Global
   Minimum Cut of a Simple Graph in Near-Linear Time") para grafos sin
   pesos, Jason Li ("Deterministic mincut in almost-linear time", STOC 2021) y Monika
   Henzinger, Jason Li, Satish Rao y Di Wang ("Deterministic Near-Linear Time Minimum
   Cut in Weighted Graphs", SODA 2024) para grafos con pesos. Ninguno cabe en una
   página. ¿Qué haría falta para que uno quepa?

7. **¿Qué cotas mínimas sin condiciones sabemos demostrar, y por qué son tan pocas?**
   El capítulo 5 las dio en modelos restringidos. Para circuitos generales, la mejor
   cota para una función explícita es $3{,}1n - o(n)$, de Jiatu Li y Tianqi Yang
   ("3.1n − o(n) Circuit Lower Bounds for Explicit Functions", STOC 2022). El $3n$ de
   Blum, de 1984, solo lo había mejorado antes el $(3 + 1/86)n$ de Find, Golovnev,
   Hirsch y Kulikov (FOCS 2016). La §2 explica parte del porqué. Lee también el corolario
   de Williams (STOC 2025) en la §5 y piensa por qué es tan raro que un algoritmo de
   simulación dé una cota mínima.

8. **Si la refutación de la ETH es correcta, ¿qué queda en pie?** Lee "The
   Exponential Time Hypothesis is False" y su documentación de Lean en
   [github.com/openai/math](https://github.com/openai/math), el capítulo 20, §12, y
   Backurs e Indyk (STOC 2015). Para cada cota condicional que conozcas, averigua si
   usa SETH, la hipótesis más débil sobre CNF-SAT general, o otra.

9. **¿Cuándo una cota encontrada por búsqueda automática es una idea nueva?** Compara
   tres casos: el esquema de 48 productos (Novikov y otros, arXiv 2506.13131) con su
   versión racional (Dumas, Pernet y Sedoglavic, arXiv 2506.13242), la cota 2,371177
   (Dupont y otros, arXiv 2608.16884), y la cota $9/4$ con sus dos exposiciones. ¿En
   cuál apareció una técnica que alguien pueda reutilizar, y quién la hizo visible?

10. **¿Por qué el simplex funciona en la práctica, y qué explica el análisis
    suavizado?** Empieza por Spielman y Teng (*Journal of the ACM* 51, 2004) y
    sigue con Bach y Huiberts (FOCS 2025, arXiv 2504.04197), cuyo resumen cuenta la
    historia de las mejoras. ¿Qué parte del comportamiento del simplex en problemas
    reales sigue sin explicar el modelo de ruido gaussiano?
