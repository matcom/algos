# Algoritmos aleatorios I: Las Vegas y costo esperado {#chap-las-vegas}

```{python echo=false output=asis}
import math
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_08.py
sys.setrecursionlimit(20_000)
import figuras_08 as F8
```

Hasta aquí, el costo de un algoritmo era un número para cada entrada, y de todas las
entradas de tamaño $n$ nos quedábamos con la peor. En este capítulo el algoritmo tira
monedas. Para una entrada fija, su costo deja de ser un número y pasa a ser una
variable aleatoria. Su respuesta, en cambio, es siempre la correcta. Vamos a ver tres
algoritmos así: ordenar, seleccionar y guardar en una tabla hash. Los tres se analizan
con la misma herramienta, y los tres responden la misma pregunta: qué se gana cuando el
azar lo pone el algoritmo y no la entrada.

## 1. El azar dentro del algoritmo

Ya vimos un algoritmo de este tipo. El par más cercano por inserción incremental del
capítulo 2, §9, baraja los puntos y los inserta uno por uno en una rejilla. La
respuesta es siempre el par más cercano, sea cual sea el orden. Lo que depende del
orden es cuántas veces se reconstruye la rejilla, y el análisis hacia atrás mostró que
en esperanza son unas $2 \ln n$. Un algoritmo que siempre responde bien y cuyo tiempo
es aleatorio se llama **Las Vegas**. El capítulo 15 trata los otros, los **Monte
Carlo**, que corren en un tiempo acotado y pueden equivocarse con una probabilidad
controlada.

Hay que fijar qué significa "el costo esperado es $O(f(n))$", porque el orden de los
cuantificadores es todo. Sea $T(x, r)$ el costo con la entrada $x$ y las monedas $r$.
Decimos que el algoritmo cuesta $O(f(n))$ esperado si
$$\max_{|x| = n}\ \mathbb{E}_r\big[T(x, r)\big] = O(f(n)).$$
Primero se fija la entrada, la peor que haya, y después se promedia sobre las monedas
del algoritmo. La entrada no es aleatoria: la puede elegir un adversario que conoce el
código, pero no las monedas. Esto no es el caso promedio de Estructuras de Datos, donde
la entrada es la que se supone aleatoria. La sección 7 vuelve sobre la diferencia.

La herramienta es la que usó el capítulo 2 para contar reconstrucciones. Una
**variable indicadora** $X_A$ vale 1 si ocurre el evento $A$ y 0 si no, así que
$\mathbb{E}[X_A] = \Pr[A]$. Y la esperanza de una suma es la suma de las esperanzas,
$\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]$, **aunque $X$ e $Y$ dependan una
de la otra**. Esa última frase es la que hace funcionar todo el capítulo: vamos a
sumar miles de indicadoras muy dependientes entre sí, y no hará falta saber nada de
cómo dependen.

## 2. Quicksort con pivote fijo

Quicksort elige un **pivote** $x$, reparte los elementos en los menores que $x$, los
iguales y los mayores, ordena los menores y los mayores por recursión y concatena. Lo
vieron en Estructuras de Datos. Aquí lo escribimos de modo que la regla para elegir el
pivote sea un parámetro, y contamos **comparaciones**: cada elemento se compara una vez
con el pivote en cada partición, así que partir $m$ elementos cuesta $m - 1$.

```{python continue}
def quicksort(A, pivote, cuenta, registro=None):
    if len(A) <= 1:
        return list(A)
    x = pivote(A)
    cuenta[0] += len(A) - 1                      # x contra cada uno de los demás
    if registro is not None:
        registro.append((x, list(A)))            # para la figura de la sección 4
    menores = [a for a in A if a < x]
    iguales = [a for a in A if a == x]
    mayores = [a for a in A if a > x]
    return (quicksort(menores, pivote, cuenta, registro) + iguales
            + quicksort(mayores, pivote, cuenta, registro))

def comparaciones(A, pivote):
    cuenta = [0]
    assert quicksort(A, pivote, cuenta) == sorted(A)
    return cuenta[0]
```

**El intento que falla.** La regla más simple es tomar el primer elemento. Sobre una
permutación al azar funciona bien. Sobre una entrada ya ordenada, cada pivote es el
mínimo de lo que queda, cada partición quita un solo elemento, y el costo es
$(n-1) + (n-2) + \dots + 1 = n(n-1)/2$.

```{python continue}
primero = lambda A: A[0]
random.seed(8)
print(f"{'n':>5} {'ordenada':>9} {'al azar':>8} {'n(n-1)/2':>9}")
for n in [500, 1000, 2000]:
    ordenada = list(range(n))
    barajada = random.sample(ordenada, n)
    print(f"{n:>5} {comparaciones(ordenada, primero):>9} "
          f"{comparaciones(barajada, primero):>8} {n * (n - 1) // 2:>9}")
```

Cuadrático justo en la entrada más inocente que hay. Y no es mala suerte de la regla
"el primero": el ejercicio 6 construye la entrada mala para la regla "el del medio".
Quien conoce la regla fabrica la entrada. La mediana de las medianas del capítulo 6 da
un pivote bueno sin azar, pero cuesta un trabajo lineal y una constante grande en
cada partición.

La salida barata es que la regla no se pueda conocer: elegir el pivote **al azar**
entre los elementos del subarreglo. Ahora ninguna entrada es mala de antemano, porque
lo que decide el costo son las monedas, y las tira el algoritmo después de recibir la
entrada.

## 3. Quicksort aleatorio: el experimento

El código es el mismo con otra regla. La entrada queda fija y lo que se repite son las
monedas: 10 000 corridas sobre la misma permutación de 200 elementos.

```{python continue}
al_azar = random.choice

random.seed(1)
for _ in range(500):                             # oráculo: sorted, con repetidos
    A = [random.randrange(20) for _ in range(random.randrange(60))]
    comparaciones(A, al_azar)

n = 200
A = random.sample(range(10 ** 6), n)
corridas = [comparaciones(A, al_azar) for _ in range(10_000)]
media = sum(corridas) / len(corridas)
print(f"media {media:.1f}   mínimo {min(corridas)}   máximo {max(corridas)}")
print(f"2 n ln n = {2 * n * math.log(n):.1f}   n(n-1)/2 = {n * (n - 1) // 2}")
```

```{python continue echo=false output=asis}
exacta = 2 * (n + 1) * sum(1 / k for k in range(1, n + 1)) - 4 * n
print(F8.histograma(corridas, [("media medida", media, F8.TINTA),
                               ("2(n+1)Hₙ − 4n", exacta, F8.CALIDO),
                               ("2n ln n", 2 * n * math.log(n), F8.ALARMA)],
      ident="lv-histograma",
      pie=f"Comparaciones de quicksort aleatorio en 10 000 corridas sobre la misma "
          f"entrada de {n} elementos. La fórmula exacta de la sección 5 cae sobre la "
          f"media. La cota 2n ln n queda a la derecha de casi todas las corridas, y "
          f"el peor caso, n(n−1)/2 = {n * (n - 1) // 2}, muy fuera del dibujo."))
```

Tres cosas se ven en la @fig-lv-histograma. Ninguna corrida se acercó al peor caso
de 19 900. Las corridas se amontonan cerca de la media. Y la media, 1 561, queda bien
por debajo de $2n \ln n \approx 2\,119$. El experimento sugiere que $2n\ln n$ es una
cota y no el valor, y que hay una fórmula exacta. Las dos secciones siguientes la
deducen.

## 4. Cuándo se comparan dos elementos

Llamemos $z_1 < z_2 < \dots < z_n$ a los elementos en orden, **suponiendo que son
distintos**. Cada comparación es entre un pivote y otro elemento, y dos elementos se
comparan a lo sumo una vez: después de compararse con el pivote, el otro elemento
queda en un subarreglo que no contiene al pivote. El número de comparaciones es
entonces
$$C = \sum_{i < j} X_{ij}, \qquad X_{ij} = 1 \text{ si } z_i \text{ y } z_j \text{ se comparan alguna vez}.$$

Por linealidad, $\mathbb{E}[C] = \sum_{i<j} \Pr[z_i \text{ y } z_j \text{ se comparan}]$.
Todo se reduce a esa probabilidad, y la idea para calcularla está en la
@fig-lv-pivotes, que sale de una corrida real con 12 elementos.

```{python continue echo=false output=asis}
random.seed(4)
registro = []
quicksort(list(range(1, 13)), al_azar, [0], registro)
orden = {x: t + 1 for t, (x, _) in enumerate(registro)}   # las hojas no están
comparados = {frozenset((x, a)) for x, B in registro for a in B if a != x}

def primer_pivote(i, j):
    return min(range(i, j + 1), key=lambda r: orden.get(r, math.inf))

pares = [(i, j) for i in range(1, 13) for j in range(i + 3, 13)]
for i, j in pares:                               # el lema, en esta corrida
    assert (frozenset((i, j)) in comparados) == (primer_pivote(i, j) in (i, j))
par_si = next((i, j) for i, j in pares if primer_pivote(i, j) in (i, j) and j - i >= 4)
par_no = next((i, j) for i, j in pares if primer_pivote(i, j) not in (i, j)
              and j - i >= 4 and i > par_si[1] - 3)
print(F8.pivotes_intervalo(12, orden, par_si, par_no, ident="lv-pivotes",
      pie="Una corrida real de quicksort aleatorio con 12 elementos. Arriba, el turno "
          "en que cada elemento fue elegido pivote; los marcados con un punto nunca lo "
          "fueron, porque quedaron solos en su subarreglo. "
          "Para cada intervalo, el punto marca el primer "
          "pivote elegido dentro de él: si es un extremo, los extremos se comparan; si "
          "es interior, los separa para siempre."))
```

**Lema.** Para $i < j$, los elementos $z_i$ y $z_j$ se comparan si y solo si el primer
pivote elegido entre $z_i, z_{i+1}, \dots, z_j$ es $z_i$ o $z_j$. En consecuencia,
$$\Pr[z_i \text{ y } z_j \text{ se comparan}] = \frac{2}{j - i + 1}.$$

*Demostración.* Sea $I = \{z_i, \dots, z_j\}$. El paso que todo el mundo se salta es
este: **mientras ningún elemento de $I$ haya sido pivote, los elementos de $I$ están
todos en el mismo subarreglo.** Por inducción sobre las particiones: al principio
están todos en el arreglo entero. Si están juntos en un subarreglo y el pivote $x$ no
está en $I$, entonces $x < z_i$ o $x > z_j$, y en los dos casos todo $I$ cae del mismo
lado, porque $I$ es un intervalo del orden.

Ahora sea $x$ el primer pivote elegido dentro de $I$. En ese momento todo $I$ está en
el subarreglo que $x$ parte.

- Si $x = z_i$, el pivote se compara con todos los de su subarreglo, $z_j$ incluido.
  Lo mismo si $x = z_j$.
- Si $z_i < x < z_j$, esta partición manda a $z_i$ a los menores y a $z_j$ a los
  mayores. No se comparan ahora, porque ninguno de los dos es el pivote, y no se
  comparan nunca más, porque desde ahora están en subarreglos distintos. Antes tampoco
  se compararon: una comparación necesita que uno de los dos sea pivote, y $x$ fue el
  primer pivote de $I$.

Falta la probabilidad. Mientras $I$ viaja junto, cada pivote se elige uniforme entre
los elementos del subarreglo, que contiene a $I$ entero. Condicionado a que el pivote
cae en $I$, es uniforme en $I$. Así que el primer pivote de $I$ es cada uno de sus
$j - i + 1$ elementos con la misma probabilidad, y dos de ellos son los extremos.
$\square$

Fíjate en lo que el lema dice de los vecinos: $z_i$ y $z_{i+1}$ se comparan con
probabilidad $2/2 = 1$. Tiene que ser así, porque ningún algoritmo de comparaciones
puede ordenar sin comparar dos elementos consecutivos: es el argumento del adversario
del capítulo 5, §6, con la cadena de la mezcla.

## 5. La suma

Sumamos el lema sobre todos los pares, agrupando por la distancia $d = j - i$, que va
de 1 a $n - 1$ y aparece en $n - d$ pares. Con $k = d + 1$:
$$\mathbb{E}[C] = \sum_{d=1}^{n-1} (n - d)\,\frac{2}{d + 1}
= \sum_{k=2}^{n} \frac{2(n + 1 - k)}{k}
= 2(n+1)\sum_{k=2}^{n} \frac1k - 2(n-1)
= 2(n+1)H_n - 4n,$$
donde $H_n = 1 + \frac12 + \dots + \frac1n$ es el número armónico, y el último paso usa
$\sum_{k=2}^n 1/k = H_n - 1$.

**Teorema.** Para todo $n \ge 1$ y toda entrada de $n$ elementos distintos, quicksort
aleatorio hace en esperanza exactamente $2(n+1)H_n - 4n$ comparaciones, y eso es a lo
sumo $2n \ln n$.

*Demostración de la cota.* Como $1/k \le \int_{k-1}^{k} dt/t$ para $k \ge 2$, se tiene
$H_n \le 1 + \int_1^n dt/t = 1 + \ln n$. Entonces
$$2(n+1)H_n - 4n \le 2(n+1)(1 + \ln n) - 4n = 2n\ln n + 2\ln n - 2n + 2,$$
y los tres últimos términos suman $2(\ln n - (n - 1)) \le 0$, porque $\ln n \le n - 1$
para todo $n \ge 1$. $\square$

La cota tira dos cosas: el término $-2(n - 1 - \ln n)$ y lo que $H_n$ queda por
debajo de $1 + \ln n$. Usando $H_n = \ln n + \gamma + O(1/n)$, con
$\gamma \approx 0{,}5772$, la fórmula exacta es $2n\ln n - (4 - 2\gamma)n + O(\log n)$:
la cota se pasa en un término lineal, unas $2{,}85\,n$ comparaciones. Es la razón por
la que la media medida quedó tan por debajo de $2n \ln n$.

Ahora el experimento contra la fórmula. Para que la comprobación pueda fallar, ponemos
al lado la suma con una probabilidad equivocada, $1/(j - i + 1)$, que es la que sale si
uno olvida que sirven los dos extremos.

```{python continue}
def suma_pares(n, p):
    return sum(p(j - i) for i in range(n) for j in range(i + 1, n))

H = sum(1 / k for k in range(1, n + 1))
error = (sum((c - media) ** 2 for c in corridas) / (len(corridas) - 1)) ** 0.5 / 100
print(f"media medida:            {media:8.1f}  ± {error:.1f}")
print(f"2(n+1)H_n - 4n:          {2 * (n + 1) * H - 4 * n:8.1f}")
print(f"suma de 2/(j-i+1):       {suma_pares(n, lambda d: 2 / (d + 1)):8.1f}")
print(f"suma de 1/(j-i+1):       {suma_pares(n, lambda d: 1 / (d + 1)):8.1f}")
print(f"2 n ln n:                {2 * n * math.log(n):8.1f}")
print(f"2 n ln n - exacta:       {2 * n * math.log(n) - (2 * (n + 1) * H - 4 * n):8.1f}"
      f"   (2,85 n = {2.845 * n:.1f})")
```

La media cae a menos de dos errores estándar de la fórmula (el $\pm$ es la desviación
estándar de las corridas dividida por $\sqrt{10\,000} = 100$), y la probabilidad
equivocada queda a la mitad, muy lejos. La diferencia con $2n\ln n$ es la que predice
el término lineal, salvo el $O(\log n)$. Para tener una idea del tamaño:
$2n\ln n = (2\ln 2)\, n\log_2 n \approx 1{,}39\, n \log_2 n$. El término principal de
quicksort aleatorio es un 39 % mayor que el de la cota mínima de peor caso
$n\log_2 n - O(n)$ del capítulo 5, §3, y vale para cualquier entrada. (El capítulo 5
demostró esa cota para algoritmos deterministas. Para algoritmos aleatorios, en
esperanza, hace falta otro argumento, que este libro no da.)

## 6. El error plantado: claves repetidas

Una variante que se ve en muchos libros reparte en dos partes: los menores que el
pivote a un lado, y los mayores **o iguales** al otro. Parece lo mismo con una lista
menos.

```{python continue}
def quicksort_dos(A, cuenta):
    if len(A) <= 1:
        return list(A)
    i = random.randrange(len(A))
    x, resto = A[i], A[:i] + A[i + 1:]
    cuenta[0] += len(resto)
    return (quicksort_dos([a for a in resto if a < x], cuenta) + [x]
            + quicksort_dos([a for a in resto if a >= x], cuenta))

random.seed(2)
for _ in range(500):                             # permutaciones al azar: todo verde
    A = random.sample(range(1000), random.randrange(60))
    assert quicksort_dos(A, [0]) == sorted(A)
print("500 permutaciones al azar: iguales a sorted")

n2 = 2000
for nombre, B in [("todos iguales", [7] * n2),
                  ("enteros del 0 al 9", [random.randrange(10) for _ in range(n2)])]:
    c2, c3 = [0], [0]
    assert quicksort_dos(B, c2) == quicksort(B, al_azar, c3) == sorted(B)
    print(f"{nombre:>19}: dos partes {c2[0]:>9,}   tres partes {c3[0]:>6,}"
          .replace(",", " "))
print(f"{'n(n-1)/2':>19}: {n2 * (n2 - 1) // 2:>20,}".replace(",", " "))
```

Ordena bien, porque la correctitud de quicksort no depende del pivote. Pero con todos
los elementos iguales cada partición deja $m - 1$ elementos del mismo lado, y el costo
es exactamente $n(n-1)/2$, con pivotes al azar y todo. Una batería de pruebas hecha
con permutaciones, que es lo natural para probar un ordenamiento, no lo ve nunca, y si
mide tiempos tampoco: todas sus entradas tienen claves distintas.

La demostración lo anunciaba. La sección 4 empieza con "suponiendo que son
distintos", y el paso clave usa que $I$ es un intervalo que el pivote **separa**: si
$z_i < x < z_j$, los manda a lados distintos. Con claves repetidas, un pivote igual a
dos copias de un valor no las separa en la versión de dos partes: las dos van a los
mayores o iguales, quedan siempre del mismo lado, y el par termina comparándose. Cada
par se sigue comparando a lo sumo una vez, porque el pivote sale de la recursión, pero
ahora con probabilidad 1 y no $2/(j - i + 1)$. Con todas las claves iguales eso son
los $n(n-1)/2$ pares. La versión de tres partes saca a todos los iguales en la primera
partición que los toca. Para ella la demostración no se aplica tal cual, porque el
orden $z_1 < \dots < z_n$ ya no existe. Lo que sí muestra la tabla es que, medida, no
sufre con repetidos.

La moraleja es la del capítulo 3: la hipótesis que una demostración usa es
la lista de entradas que hay que probar.

## 7. Esperado, promedio y amortizado

Tenemos ya tres garantías que se parecen y no son iguales.

| Garantía | Qué es aleatorio | Para qué entradas vale | Ejemplo |
|---|---|---|---|
| Caso promedio | la entrada | en promedio sobre entradas de una distribución supuesta | quicksort con el primer pivote |
| Costo esperado | las monedas del algoritmo | para toda entrada, incluida la peor | quicksort aleatorio |
| Costo amortizado | nada | para toda secuencia de operaciones | la cola con dos pilas, capítulo 4 |

Quicksort con el primer elemento como pivote, sobre una permutación uniforme, hace en
promedio exactamente las mismas $2(n+1)H_n - 4n$ comparaciones: el primer elemento de
una permutación al azar es un pivote al azar, y como la partición conserva el orden
relativo, cada sublista vuelve a ser una permutación al azar de sus elementos. La
cuenta es la misma y la garantía no:
el promedio vale si la entrada viene al azar, y un adversario que manda la lista
ordenada la rompe. En el aleatorio, el adversario puede mandar lo que quiera.

El amortizado del capítulo 4, §1, es otra cosa: es una cota de peor caso sobre la suma
de una secuencia, sin probabilidad en ninguna parte. Una garantía esperada, en cambio,
no dice nada seguro sobre una corrida: es posible, aunque improbable, que quicksort
aleatorio haga $n(n-1)/2$ comparaciones. Lo que sí se puede decir es cuán improbable.

**Desigualdad de Markov.** Si $X \ge 0$ y $t > 0$, entonces
$\Pr[X \ge t\,\mathbb{E}[X]] \le 1/t$.

*Demostración.* $\mathbb{E}[X] \ge \mathbb{E}[X \cdot [X \ge t\mathbb{E}[X]]] \ge t\,\mathbb{E}[X] \cdot \Pr[X \ge t\mathbb{E}[X]]$,
la primera porque $X \ge 0$ y la segunda porque donde la indicadora vale 1, $X$ vale al
menos $t\mathbb{E}[X]$. Se divide por $t\mathbb{E}[X]$. $\square$

Markov solo usa la media, así que es débil. Las 10 000 corridas de la sección 3 lo
muestran:

```{python continue}
for t in [1.1, 1.2, 1.5]:
    fraccion = sum(c >= t * media for c in corridas) / len(corridas)
    print(f"Pr[C >= {t} media]: medido {fraccion:.4f}   Markov {1 / t:.3f}")
print(f"la peor corrida: {max(corridas) / media:.2f} veces la media")
```

La cola real es mucho más delgada que la que Markov garantiza. Aun así, Markov basta
para algo útil: el ejercicio 7 convierte un algoritmo Las Vegas en uno que termina
siempre a tiempo y, a cambio, a veces no responde. Esa conversión es el puente al
capítulo 15.

## 8. Quickselect

**El problema** es el del capítulo 6: dados $n$ elementos y un $k$ entre 0 y $n - 1$,
hallar el que quedaría en la posición $k$ si los ordenáramos. Allí se resolvió en
tiempo lineal en el peor caso con la mediana de las medianas.

**Cómo se le ocurre a uno.** Después de partir con un pivote, quicksort sigue por los
dos lados. Pero contando cuántos menores e iguales hay se sabe en qué lado está el
$k$-ésimo, y basta seguir **por ese solo**. La idea es de C. A. R. Hoare, que la
publicó como "Algorithm 65: Find" en *Communications of the ACM* 4(7), 1961, al lado
de "Algorithm 64: Quicksort". Aquí la escribimos con el pivote al azar.

```{python echo=false}
import math
import random
```

```{python continue}
def quickselect(A, k, cuenta):
    while True:
        x = random.choice(A)
        cuenta[0] += len(A) - 1
        menores = [a for a in A if a < x]
        iguales = sum(1 for a in A if a == x)
        if k < len(menores):
            A = menores
        elif k < len(menores) + iguales:
            return x
        else:
            k -= len(menores) + iguales
            A = [a for a in A if a > x]

random.seed(3)
for _ in range(2000):                            # oráculo: sorted
    A = [random.randrange(30) for _ in range(random.randrange(1, 60))]
    k = random.randrange(len(A))
    assert quickselect(A, k, [0]) == sorted(A)[k]
print("2000 pruebas contra sorted: iguales")

n = 1000
A = random.sample(range(10 ** 6), n)
print(f"{'k':>5} {'comparaciones / n':>18}")
for k in [0, 100, 250, 500, 750, 999]:
    c = [0]
    for _ in range(200):
        quickselect(A, k, c)
    print(f"{k:>5} {c[0] / 200 / n:>18.2f}")
```

El experimento propone que quickselect es lineal: unas 2 comparaciones por
elemento para el mínimo y para el máximo (1,88 y 2,01), y la mayor cuenta en la
mediana, con 3,29. El peor caso sigue
siendo $n(n-1)/2$, con las mismas monedas desgraciadas que en quicksort. Falta
demostrar que en esperanza es $O(n)$.

## 9. Quickselect cuesta $O(n)$ esperado

La idea es que un pivote al azar es "bueno" la mitad de las veces, y un pivote bueno
achica el arreglo en una fracción fija.

Digamos que un pivote es **central** en un subarreglo de $m$ elementos si los dos lados
que deja, los menores y los mayores, tienen a lo sumo $3m/4$ elementos cada uno.
Suponemos elementos distintos (el caso con repetidos solo achica los lados).

**Lema.** En un subarreglo de $m \ge 1$ elementos distintos hay al menos $m/2$
pivotes centrales.

*Demostración.* Si el pivote tiene rango $r$ (de 0 a $m-1$), deja $r$ menores y
$m - 1 - r$ mayores. Es central si $r \le 3m/4$ y $r \ge m/4 - 1$. Los rangos enteros
en ese intervalo son al menos $\lfloor 3m/4 \rfloor - \lceil m/4 - 1 \rceil + 1$.
Escribiendo $m = 4q + s$ con $0 \le s \le 3$, eso es $2q + 1$, $2q + 1$, $2q + 2$ y
$2q + 3$ para $s = 0, 1, 2, 3$ (para $s = 0$, por ejemplo, $3q - (q - 1) + 1$), y en
los cuatro casos es al menos $(4q + s)/2$. $\square$

El código lo comprueba para todo $m$ hasta 2 000, y la comprobación se puede romper:
con "a lo sumo $m/2$" en lugar de $3m/4$ deja de valer.

```{python continue}
def centrales(m, fraccion):
    return sum(1 for r in range(m) if r <= fraccion * m and m - 1 - r <= fraccion * m)

print("3/4:", min(centrales(m, 3 / 4) / m for m in range(1, 2001)))
print("1/2:", min(centrales(m, 1 / 2) / m for m in range(1, 2001)))
```

**Teorema.** Quickselect hace a lo sumo $8n$ comparaciones esperadas, para todo $k$ y
toda entrada de $n$ elementos distintos.

*Demostración.* Partimos la ejecución en **fases**: el algoritmo está en la fase $j$
mientras el tamaño $m$ del arreglo que procesa cumple
$(3/4)^{j+1} n < m \le (3/4)^j n$. Cada vuelta del ciclo cuesta $m - 1 < (3/4)^j n$
comparaciones en la fase $j$. Si el pivote de una vuelta es central, el lado por el
que se sigue tiene a lo sumo $3m/4 \le (3/4)^{j+1} n$ elementos, y la fase $j$
termina (o el algoritmo termina, si el pivote era la respuesta). Por el lema, cada
vuelta es central con probabilidad al menos $1/2$, con monedas nuevas e independientes
de lo que pasó antes. El número de vueltas en la fase $j$ está dominado entonces por
el número de lanzamientos de una moneda con éxito $\ge 1/2$ hasta el primer éxito,
cuya esperanza es a lo sumo 2. Sea $V_j$ ese número de vueltas. Por linealidad,
$$\mathbb{E}[C] \le \sum_{j \ge 0} \mathbb{E}[V_j] \cdot \left(\tfrac34\right)^j n
\le 2n \sum_{j \ge 0} \left(\tfrac34\right)^j = 2n \cdot 4 = 8n. \qquad \square$$

La cota es $8n$ y lo medido no pasó de 3,29 por elemento. La demostración regaló
mucho: un pivote no central también achica, y uno central casi siempre achica más de
$1/4$. Que $8n$ sea una cota superior no dice que quickselect haga $8n$, ni siquiera
en el peor $k$. El ejercicio 3 baja la cota a $4n$ con otra cuenta, y tampoco esa es
el valor.

Frente a la mediana de las medianas del capítulo 6, quickselect cambia una garantía
de peor caso por una esperada, a cambio de un código de diez líneas y una constante
menor. Las dos son lineales, y la que conviene depende de si se puede tolerar una
corrida mala con probabilidad pequeña.

## 10. Hashing: toda función fija tiene una mala entrada

Una tabla hash con **encadenamiento** tiene $m$ cubetas, cada una con una lista. Una
función $h$ manda cada clave del universo $U$ a una cubeta, y buscar $x$ cuesta
recorrer la lista de la cubeta $h(x)$. En Estructuras de Datos se dijo que eso es
$O(1)$ "si la función es buena". Hay que decir qué significa, porque para una función
fija no hay forma de que lo sea siempre.

**Toda función fija tiene una mala entrada.** Si $|U| > (n - 1)m$, por el principio
del palomar alguna cubeta recibe al menos $n$ claves de $U$. Un adversario que conoce
$h$ inserta justo esas $n$, y la tabla es una lista. En CPython, por ejemplo, el hash
de un entero chico es el propio entero.

```{python echo=false}
import random
from collections import Counter
import os, sys
sys.path.insert(0, os.path.abspath(".."))
import figuras_08 as F8
```

```{python continue}
print([hash(x) for x in [0, 1, 1000, 123456]])
```

La salida es la misma idea que el pivote al azar. **La función se elige al azar,
después de recibir las claves**, de una familia de funciones con una propiedad que
alcance para el análisis.

**Definición.** Una familia $\mathcal H$ de funciones $U \to \{0, \dots, m-1\}$ es
**universal** si para todo par de claves distintas $x \ne y$,
$$\Pr_{h \in \mathcal H}[h(x) = h(y)] \le \frac1m.$$
La probabilidad es sobre la elección de $h$, uniforme en $\mathcal H$. Las claves
están fijas. La definición y el nombre son de J. Lawrence Carter y Mark N. Wegman,
"Universal classes of hash functions", *Journal of Computer and System Sciences*
18(2):143–154, 1979.

**Teorema.** Sea $S$ un conjunto de $n$ claves guardado en una tabla de $m$ cubetas
con una función elegida de una familia universal. Para toda clave $x$, el largo
esperado de la lista de la cubeta $h(x)$ es a lo sumo $1 + (n-1)/m$ si $x \in S$, y a
lo sumo $n/m$ si $x \notin S$.

*Demostración.* El largo de la lista de $h(x)$ es $\sum_{y \in S} [h(y) = h(x)]$. Si
$x \in S$, el término $y = x$ vale 1, y cada uno de los otros $n - 1$ tiene esperanza
$\Pr[h(y) = h(x)] \le 1/m$. Si $x \notin S$, son $n$ términos de esperanza $\le 1/m$.
Linealidad. $\square$

Con $m \ge n$, una búsqueda cuesta en esperanza a lo sumo 2 posiciones de lista, **para
todo conjunto de claves**: el adversario elige $S$ pero no $h$. Es una garantía
Las Vegas: la búsqueda siempre responde bien, y lo aleatorio es cuánto recorre.

## 11. Una familia universal

**El intento que falla.** La familia que se le ocurre a uno primero es la de las
funciones lineales, $h_{a,b}(x) = (ax + b) \bmod m$ con $a, b$ al azar entre 0 y
$m - 1$. Pero si $x \equiv y \pmod m$, entonces $ax + b \equiv ay + b$ para todo $a$ y
todo $b$: esas claves chocan con probabilidad 1. La aritmética módulo $m$ no ve más
que $x \bmod m$.

**La familia.** Se arregla haciendo la cuenta módulo un primo $p$ mayor que toda clave,
y reduciendo a $m$ solo al final:
$$h_{a,b}(x) = \big((ax + b) \bmod p\big) \bmod m, \qquad a \in \{1, \dots, p-1\},\ b \in \{0, \dots, p-1\}.$$

**Teorema.** Si $p$ es primo y $U = \{0, \dots, p-1\}$, esta familia es universal.

*Demostración.* Fijemos $x \ne y$ en $U$ y escribamos $r = (ax + b) \bmod p$ y
$s = (ay + b) \bmod p$. Primero, $r \ne s$: su diferencia es $a(x - y) \bmod p$, y un
producto de dos números no divisibles por el primo $p$ no es divisible por $p$. Segundo,
el par $(a, b)$ se recupera de $(r, s)$: $a = (r - s)(x - y)^{-1} \bmod p$ y
$b = (r - ax) \bmod p$, donde el inverso existe porque $p$ es primo. Así que la
correspondencia $(a, b) \mapsto (r, s)$ es una biyección entre los $p(p-1)$ pares con
$a \ne 0$ y los $p(p-1)$ pares con $r \ne s$, y elegir $(a, b)$ uniforme es elegir
$(r, s)$ uniforme entre los pares con $r \ne s$.

Las claves chocan si y solo si $r \equiv s \pmod m$. Para cada $r$, los $s \ne r$ en
$\{0, \dots, p-1\}$ con $s \equiv r \pmod m$ son a lo sumo $\lceil p/m \rceil - 1$, y
$\lceil p/m \rceil - 1 \le (p + m - 1)/m - 1 = (p - 1)/m$. Hay entonces a lo sumo
$p(p-1)/m$ pares $(r, s)$ que chocan, de $p(p-1)$. $\square$

El paso que se salta es por qué hace falta $a \ne 0$: con $a = 0$, todas las claves
van a la cubeta $b \bmod m$, y el ejercicio 4 pregunta qué pasa entonces con la
universalidad. Y $p$ tiene que ser primo para que exista $(x - y)^{-1}$.

La @fig-lv-colisiones enumera las dos familias sobre el universo $\{0, \dots, 31\}$ con
$m = 8$: para cada par, la fracción exacta de funciones con que choca.

```{python continue}
def prob_choque(familia, x, y):
    return sum(h(x) == h(y) for h in familia) / len(familia)

m, p, u = 8, 37, 32
lineal = [lambda x, a=a, b=b: (a * x + b) % m for a in range(m) for b in range(m)]
universal = [lambda x, a=a, b=b: ((a * x + b) % p) % m
             for a in range(1, p) for b in range(p)]
matrices = {}
for nombre, familia in [("lineal mod m", lineal), ("con el primo", universal)]:
    M = [[prob_choque(familia, x, y) if x != y else 0 for y in range(u)]
         for x in range(u)]
    matrices[nombre] = M
    peor = max(max(fila) for fila in M)
    print(f"{nombre:>13}: {len(familia):>5} funciones, peor par {peor:.3f}, 1/m = {1 / m}")
```

```{python continue echo=false output=asis}
print(F8.colisiones(list(matrices.items()), m, ident="lv-colisiones",
      pie=f"Probabilidad exacta de que cada par de claves de 0 a {u - 1} choque, "
          f"enumerando todas las funciones de cada familia, con m = {m} cubetas. A la "
          f"izquierda, (ax + b) mod m: en rojo, los pares que pasan de 1/{m}; los de "
          f"x ≡ y (mod {m}) chocan siempre. A la derecha, la familia con p = {p}: "
          f"ningún par pasa de 1/{m}."))
```

En la familia lineal algunos pares chocan siempre, pero también hay muchos que no
chocan nunca: el promedio sobre todos los pares no es malo. La universalidad no habla
del promedio sobre pares, que una función fija también puede tener bueno, sino de
**cada** par. Es lo que impide al adversario elegir el suyo.

Ahora con números de verdad: 1 000 claves, todas múltiplos de $m = 1\,024$, en una
tabla de $m$ cubetas. Para la familia lineal, $ax + b \equiv b \pmod{1024}$ para
todas.

```{python continue}
def es_primo(q):
    return q > 1 and all(q % d for d in range(2, int(q ** 0.5) + 1))

m, p = 1024, 2_000_003
assert es_primo(p) and p > 1000 * m
claves = [i * m for i in range(1000)]
random.seed(5)
for nombre, sortear in [
        ("lineal mod m", lambda: (random.randrange(m), random.randrange(m), None)),
        ("con el primo", lambda: (random.randrange(1, p), random.randrange(p), p))]:
    largos = []
    for _ in range(20):
        a, b, q = sortear()
        if q is None:
            h = lambda x: (a * x + b) % m
        else:
            h = lambda x: ((a * x + b) % q) % m
        largos.append(max(Counter(h(x) for x in claves).values()))
    print(f"{nombre:>13}: lista más larga en 20 sorteos, {min(largos)} a {max(largos)}")
```

Con la familia lineal, la tabla es una lista de 1 000 en cada uno de los sorteos. Con
el primo, la lista más larga midió entre 2 y 8. El teorema de la sección 10 habla del
largo esperado de la lista de **una** clave, no de la más larga, y de la más larga la
universalidad sola dice poco. Sea $L$ su largo. Los pares de claves que chocan son al
menos $\binom{L}{2}$, los de esa lista, y en esperanza son a lo sumo
$\binom{n}{2}/m$, uno por par con probabilidad $\le 1/m$. Así que
$\mathbb{E}[L(L-1)] \le n(n-1)/m$. Con $m = n$, y como
$\mathbb{E}[L]^2 \le \mathbb{E}[L^2]$, sale $\mathbb{E}[L]^2 - \mathbb{E}[L] \le n - 1$,
es decir, $\mathbb{E}[L] \le \sqrt n + 1/2$. Es todo lo que demuestra la
universalidad. Si cada clave cayera en una cubeta uniforme e independiente de las
demás, un modelo ideal y más exigente que la universalidad, la lista más larga sería mucho
menor: el ejercicio 9 la mide en ese modelo.

## 12. Cierre

El algoritmo del capítulo 2, §9, tenía en realidad dos monedas. Una es la permutación
de los puntos, que hace que se esperen pocas reconstrucciones. La otra está escondida
en la tabla hash de la rejilla: cada consulta cuesta $O(1)$ esperado si la función de
hash se elige, por ejemplo, al azar de una familia universal. Pero el teorema de la
sección 10 vale para un conjunto de claves **fijo**, y aquí las celdas ocupadas las
decide la permutación. Para usarlo hay que fijar primero la permutación y promediar
después sobre la función, y eso exige que la función se elija **independiente** de la
permutación. Con esa independencia, cada consulta y cada reconstrucción tienen costo
esperado acotado dado el orden, y la linealidad suma todas las contribuciones: el
costo esperado es $O(n)$ para todo conjunto de puntos. La linealidad permite sumar
términos dependientes. No permite acotar cada término sin la hipótesis que su propia
cota necesita.

Las tres herramientas del capítulo son una sola: escribir el costo como suma de
indicadoras y sumar probabilidades. Lo que cambió fue el evento: "estos dos se
comparan", "esta vuelta tiene un pivote central", "estas dos claves chocan". El trabajo
está siempre en encontrar el evento cuya probabilidad se puede calcular.

La regla que te llevas: **una garantía esperada vale para toda entrada mientras el
azar lo ponga el algoritmo y el adversario no lo vea.** Si el azar viene de la entrada,
es un caso promedio y un adversario lo rompe. Si el adversario ve las monedas, el
ejercicio 10 dice qué queda.

Hacia adelante, el capítulo 15 trata los algoritmos Monte Carlo, que fijan el tiempo y
dejan que la respuesta falle, y la amplificación por repetición. El capítulo 21 vuelve
a la linealidad de la esperanza con una asignación al azar para MAX-3SAT.

## Resumen

- Un algoritmo **Las Vegas** siempre responde bien. Su tiempo es una variable
  aleatoria, y se garantiza $\max_x \mathbb{E}_r[T(x, r)]$: la peor entrada, el
  promedio sobre las monedas.
- La linealidad de la esperanza no pide independencia. Escribir el costo como suma de
  indicadoras es el método del capítulo.
- En quicksort aleatorio, $z_i$ y $z_j$ se comparan si y solo si el primer pivote del
  intervalo $z_i, \dots, z_j$ es uno de los dos, con probabilidad $2/(j-i+1)$.
- El número esperado de comparaciones es exactamente $2(n+1)H_n - 4n \le 2n\ln n$ para
  claves distintas, para toda entrada.
- La partición en dos con los iguales a un lado cuesta $n(n-1)/2$ con todas las claves
  iguales. La hipótesis "claves distintas" de la demostración señalaba ese caso.
- Caso promedio (entrada al azar), costo esperado (monedas del algoritmo) y costo
  amortizado (sin azar, toda secuencia) son tres garantías distintas.
- Markov: $\Pr[X \ge t\mathbb{E}[X]] \le 1/t$ para $X \ge 0$. Es débil, pero solo pide
  la media.
- Quickselect sigue por un solo lado y hace $O(n)$ comparaciones esperadas: a lo sumo
  $8n$ por el argumento de fases, que es una cota floja.
- Toda función de hash fija tiene un conjunto de $n$ claves que caen en una sola
  cubeta. Una familia universal da largo esperado $\le 1 + (n-1)/m$ para todo
  conjunto.
- $((ax + b) \bmod p) \bmod m$, con $p$ primo y $a \ne 0$, es universal. Sin el primo,
  las claves congruentes módulo $m$ chocan siempre.

## Ejercicios

1. Para $n = 3$ elementos distintos, enumera todas las maneras en que quicksort
   aleatorio puede elegir sus pivotes, con la probabilidad de cada una, y calcula
   exacto el número esperado de comparaciones. Compáralo con la fórmula de la sección
   5.
2. Sea $P_k$ el número de comparaciones en que participa el elemento de rango $k$
   (como pivote o como comparado) en quicksort aleatorio sobre $n$ elementos
   distintos. Calcula $\mathbb{E}[P_k]$ en forma cerrada con números armónicos. ¿Qué
   rango participa en más comparaciones esperadas, y en cuál menos? Comprueba que
   $\sum_k \mathbb{E}[P_k]$ es el doble de la fórmula de la sección 5, y explica por
   qué el doble.
3. ★ Demuestra que quickselect hace a lo sumo $4n$ comparaciones esperadas para todo
   $k$. Sugerencia: escribe una recurrencia para $T(n)$, el máximo sobre $k$ de la
   esperanza, acotando el lado por el que se sigue por el mayor de los dos, y demuestra
   $T(n) \le 4n$ por sustitución, sin ignorar pisos ni techos.
4. Si en la familia de la sección 11 se permite $a = 0$, ¿sigue siendo universal? Da
   valores de $p$, $m$, $x$ e $y$ que respondan, y demuestra que de todos modos la
   probabilidad de colisión de cualquier par es a lo sumo $1/m + 1/p$.
5. Quita el término $b$: $h_a(x) = (ax \bmod p) \bmod m$, con $a$ entre 1 y $p - 1$.
   Para $p \in \{5, 7, 11, 13\}$ y todo $m$ entre 2 y $p - 1$, enumera la probabilidad
   de colisión de cada par de claves de $\{0, \dots, p-1\}$. ¿Es universal? Si no, da el
   par y los valores que lo muestran, y busca la mayor razón entre la probabilidad de
   colisión y $1/m$ en lo que enumeraste.
6. Con el pivote en la posición del medio del subarreglo (`A[len(A) // 2]`) y la
   partición del código de la sección 2, que conserva el orden relativo, construye
   para cada $n$ una permutación de $\{0, \dots, n-1\}$ con la que quicksort hace
   $n(n-1)/2$ comparaciones. Comprueba tu construcción con código para $n$ hasta 1 000.
7. Un algoritmo Las Vegas tiene tiempo esperado a lo sumo $T$ para toda entrada.
   Usando Markov, construye un algoritmo que siempre termina en tiempo $2T$ y responde
   bien con probabilidad al menos $1/2$ (y si no, dice "no sé"). Después, repitiendo
   con monedas nuevas, uno que termina en tiempo $2kT$ y responde con probabilidad al
   menos $1 - 2^{-k}$. ¿Qué tienen que cumplir las repeticiones para que la cuenta
   valga?
8. Un servidor reparte peticiones entre $n$ réplicas eligiendo una al azar para cada
   petición, y se quiere saber cuántas peticiones hacen falta en promedio hasta que
   cada réplica recibió al menos una. Modela el problema con variables aleatorias
   (sugerencia: cuántas peticiones hacen falta para pasar de $i$ réplicas vistas a
   $i+1$), calcula la esperanza exacta en función de $n$ y compárala con una simulación
   para $n = 50$.
9. Inserta $n$ claves en $n$ cubetas eligiendo la cubeta de cada una uniforme e
   independiente, y mide la lista más larga para $n = 10^3, 10^4, 10^5, 10^6$, con 20
   repeticiones cada una. Compárala con $\ln n / \ln \ln n$. ¿Crece igual? ¿La
   constante se estabiliza en esos tamaños? ¿Por qué el teorema de la sección 10 no
   dice nada sobre esta cantidad?
10. Supón que el adversario ve los bits aleatorios de quicksort antes de elegir la
    entrada. ¿Qué queda de la garantía de la sección 5? Responde construyendo, a partir
    de una sucesión fija de monedas, la entrada que el adversario elegiría. ¿Es mejor
    un quicksort que baraja la entrada con `random.seed(0)` escrito en el código, antes
    de ordenarla con el primer elemento como pivote?
