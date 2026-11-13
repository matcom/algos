# Divide y vencerás y recurrencias {#chap-divide-y-venceras}

Con este capítulo empieza la Parte II, que se organiza por técnica de diseño. La
primera es divide y vencerás: **partir** la entrada en subproblemas del mismo tipo y
más pequeños, **resolverlos** por recursión y **combinar** sus soluciones. Lo difícil
casi nunca es la idea, sino la cuenta: el costo es una **recurrencia**, y hay que
resolverla.

```{python echo=false output=asis}
import math
import os
import random
import sys
import time
from collections import defaultdict
from functools import lru_cache

sys.path.insert(0, os.path.abspath(".."))   # Lectures/2026: figuras.py y figuras_06.py
import figuras_06 as F6
```

## 1. La técnica y su cuenta

Ya usamos divide y vencerás: en el capítulo 2, §5, partimos los puntos por la
mediana, resolvimos cada mitad y combinamos mirando la franja, y en la §7 dijimos sin
demostrarlo que $T(n) = 2T(n/2) + O(n \log n)$ "da $O(n \log^2 n)$". El
capítulo 1, §9, dejó otra deuda: una tabla con el costo de multiplicar dos números de
$b$ bits, donde Karatsuba aparecía con $O(b^{1{,}585})$ y ninguna explicación. Este
capítulo paga las dos.

La recurrencia se escribe sola; lo que no sale solo es su valor. En Estructuras de
Datos viste el Teorema Maestro, que la resuelve en un caso particular. Aquí lo
demostramos como corolario de un método más general, el árbol de recursión, con dos
algoritmos: uno cuyo trabajo se concentra en las hojas del árbol (Karatsuba) y otro
cuyo trabajo se concentra en la raíz (la selección en tiempo lineal).

## 2. Multiplicar: la escolar y el primer intento

Cada número es una lista de dígitos decimales, el de las unidades primero, y contamos
**multiplicaciones de un dígito**; sumar dos números de $n$ dígitos cuesta $O(n)$
aparte. Es el costo por bit del capítulo 1, §9, en base 10 para seguirlo a mano.

```{python continue}
def a_digitos(x):
    return [int(c) for c in reversed(str(x))]       # 1234 -> [4, 3, 2, 1]

def a_entero(d):
    return int("".join(map(str, reversed(d))))

def recortar(r):                                     # quita ceros a la izquierda
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r

def sumar(x, y):
    r, acarreo = [], 0
    for i in range(max(len(x), len(y))):
        s = (x[i] if i < len(x) else 0) + (y[i] if i < len(y) else 0) + acarreo
        r.append(s % 10)
        acarreo = s // 10
    return r + [acarreo] if acarreo else r

def restar(x, y):                                    # supone x >= y
    r, prestado = [], 0
    for i in range(len(x)):
        s = x[i] - (y[i] if i < len(y) else 0) - prestado
        prestado = 1 if s < 0 else 0
        r.append(s + 10 * prestado)
    return recortar(r)

def desplazar(x, k):                                 # x por 10^k
    return [0] * k + x

def escolar(x, y, cuenta):
    r = [0] * (len(x) + len(y))
    for i, xi in enumerate(x):
        acarreo = 0
        for j, yj in enumerate(y):
            cuenta[0] += 1                           # una multiplicación de un dígito
            s = r[i + j] + xi * yj + acarreo
            r[i + j], acarreo = s % 10, s // 10
        r[i + len(y)] += acarreo
    return recortar(r)
```

La escolar hace exactamente $n^2$ multiplicaciones de un dígito: cada dígito de un
número por cada dígito del otro.

**Cómo se le ocurre a uno.** El primer intento de divide y vencerás es partir cada
número en dos mitades de $m = \lfloor n/2 \rfloor$ dígitos (la de arriba se queda con
uno más si $n$ es impar):
$$x = a \cdot 10^m + b, \qquad y = c \cdot 10^m + d,$$
$$xy = ac \cdot 10^{2m} + (ad + bc) \cdot 10^m + bd.$$
Son cuatro productos de la mitad, más sumas y desplazamientos de costo $O(n)$.

```{python continue}
def partir(x, y):
    n = max(len(x), len(y))
    x, y = x + [0] * (n - len(x)), y + [0] * (n - len(y))
    m = n // 2
    return n, m, x[m:], x[:m], y[m:], y[:m]          # x = a·10^m + b, y = c·10^m + d

def cuatro_productos(x, y, cuenta):
    if max(len(x), len(y)) == 1:
        return escolar(x, y, cuenta)
    n, m, a, b, c, d = partir(x, y)
    ac, ad = cuatro_productos(a, c, cuenta), cuatro_productos(a, d, cuenta)
    bc, bd = cuatro_productos(b, c, cuenta), cuatro_productos(b, d, cuenta)
    r = sumar(sumar(desplazar(ac, 2 * m), desplazar(sumar(ad, bc), m)), bd)
    return recortar(r)

def numero(n):                                       # n dígitos al azar
    return a_digitos(random.randrange(10 ** (n - 1), 10 ** n))

random.seed(6)
print(f"{'n':>4} {'escolar':>8} {'cuatro productos':>17}")
for n in [16, 64, 256]:
    x, y = numero(n), numero(n)
    c1, c2 = [0], [0]
    assert a_entero(escolar(x, y, c1)) == a_entero(cuatro_productos(x, y, c2)) \
        == a_entero(x) * a_entero(y)
    print(f"{n:>4} {c1[0]:>8} {c2[0]:>17}")
```

Exactamente lo mismo, y tiene que ser así: la recurrencia es $T(n) = 4T(n/2) + O(n)$,
y cuatro subproblemas de la mitad, con la cuarta parte de trabajo cada uno, suman lo
mismo que el problema entero. Partir no ahorra nada si después se resuelven todas las
partes. La pregunta es si hacen falta $ad$ y $bc$ por separado, o basta con su suma.

## 3. Karatsuba: tres productos en vez de cuatro

Basta con la suma, y la suma sale de un solo producto:
$$(a + b)(c + d) = ac + ad + bc + bd, \qquad\text{así que}\qquad ad + bc = (a + b)(c + d) - ac - bd.$$
Con $ac$, $bd$ y un producto más, $(a+b)(c+d)$, tenemos el término del medio: tres
productos de la mitad en lugar de cuatro.

**Hazlo a mano** con $21 \times 34$. Las mitades son $a = 2$, $b = 1$, $c = 3$,
$d = 4$. Tres multiplicaciones de un dígito: $ac = 6$, $bd = 4$ y
$(a + b)(c + d) = 3 \cdot 7 = 21$. El término del medio es $21 - 6 - 4 = 11$, y el
resultado es $600 + 110 + 4 = 714$.

```{python continue}
def karatsuba(x, y, cuenta, umbral=1, niveles=None, prof=0):
    n = max(len(x), len(y))
    if niveles is not None:
        niveles[prof].append(n)                      # para la figura del árbol
    if n <= umbral:
        return escolar(x, y, cuenta)
    n, m, a, b, c, d = partir(x, y)
    ac = karatsuba(a, c, cuenta, umbral, niveles, prof + 1)
    bd = karatsuba(b, d, cuenta, umbral, niveles, prof + 1)
    s = karatsuba(sumar(a, b), sumar(c, d), cuenta, umbral, niveles, prof + 1)
    medio = restar(restar(s, ac), bd)                # ad + bc
    return recortar(sumar(sumar(desplazar(ac, 2 * m), desplazar(medio, m)), bd))

cuenta = [0]
print("21 × 34 =", a_entero(karatsuba(a_digitos(21), a_digitos(34), cuenta)),
      " multiplicaciones de un dígito:", cuenta[0])

random.seed(1)
for _ in range(1000):                                # oráculo: el * de Python
    p, q = random.randrange(10 ** random.randint(1, 24)), random.randrange(10 ** 24)
    assert a_entero(karatsuba(a_digitos(p), a_digitos(q), [0])) == p * q
for p, q in [(0, 0), (0, 123), (9999, 9999), (10 ** 20, 10 ** 19)]:
    assert a_entero(karatsuba(a_digitos(p), a_digitos(q), [0])) == p * q
print("1000 pares al azar y 4 casos borde: iguales al * de Python")
```

El algoritmo es de Anatoli Karatsuba, y se publicó con Yuri Ofman en 1962 en
*Doklady Akademii Nauk SSSR* (vol. 145, núm. 2, págs. 293–294). Los parámetros `umbral` y `niveles` los usan la §5 y la
figura de la §4.

## 4. El árbol de recursión de Karatsuba

Antes de demostrar, contemos. La tabla corre Karatsuba sobre números al azar y sobre
números hechos solo de nueves, los que más acarreos producen, y compara contra $n^2$ y
contra $n^{\log_2 3}$.

```{python continue}
random.seed(6)
conteos = []
print(f"{'n':>4} {'n²':>7} {'al azar':>8} {'nueves':>7} {'n^log₂3':>8} {'razón':>6}")
for k in range(1, 10):
    n = 2 ** k
    c_azar, c_nueves = [0], [0]
    karatsuba(numero(n), numero(n), c_azar)
    karatsuba([9] * n, [9] * n, c_nueves)
    conteos.append((n, c_azar[0]))
    peor = max(c_azar[0], c_nueves[0])
    print(f"{n:>4} {n * n:>7} {c_azar[0]:>8} {c_nueves[0]:>7} {3 ** k:>8} "
          f"{peor / 3 ** k:>6.2f}")
```

Al duplicar $n$ el conteo se multiplica por casi 3, no por 4, y desde $n = 8$ está
por debajo de $n^2$. La razón contra $n^{\log_2 3}$ va de 1,67
a 2,50 y ahí se queda. El experimento propone que Karatsuba hace
$\Theta(n^{\log_2 3})$ multiplicaciones; ahora hay que demostrarlo.

```{python continue echo=false output=asis}
random.seed(1)
niveles64 = defaultdict(list)
karatsuba(numero(64), numero(64), [0], niveles=niveles64)
niveles64 = [niveles64[d] for d in sorted(niveles64)]
print(F6.arbol_karatsuba(niveles64, ident="divide-y-venceras-arbol-karatsuba",
      pie=f"El árbol de una corrida real con dos números de 64 dígitos. Arriba, los "
          f"tres primeros niveles con el tamaño de cada llamada; en naranja, las que el "
          f"acarreo de a + b alargó un dígito. Abajo, las llamadas y la suma de tamaños "
          f"de cada uno de los {len(niveles64)} niveles."))
```

**La demostración.** Supongamos por ahora que $n$ es potencia de 2 y que las mitades
miden exactamente $n/2$. Partir, sumar, restar y desplazar cuesta a lo sumo $cn$ para
alguna constante $c$, así que
$$T(n) = 3T(n/2) + cn, \qquad T(1) = 1.$$
En el árbol de recursión (@fig-divide-y-venceras-arbol-karatsuba), el nivel $i$ tiene
$3^i$ llamadas de tamaño $n/2^i$, cada una trabaja $c n / 2^i$ sin contar a sus hijos,
y el nivel entero trabaja
$$3^i \cdot \frac{cn}{2^i} = cn \left(\frac{3}{2}\right)^i.$$
Hay $\log_2 n$ niveles internos, y el último tiene $3^{\log_2 n}$ hojas, cada una de
costo 1. Sumando,
$$T(n) = cn \sum_{i=0}^{\log_2 n - 1} \left(\frac32\right)^i + 3^{\log_2 n}
= cn \cdot \frac{(3/2)^{\log_2 n} - 1}{3/2 - 1} + 3^{\log_2 n}
\le 2cn \cdot \frac{3^{\log_2 n}}{n} + 3^{\log_2 n} = (2c + 1)\, 3^{\log_2 n}.$$
La serie es geométrica y **creciente**, así que la domina su último término: el
trabajo se concentra en las hojas.

**El paso que todos se saltan.** ¿Cuánto es $3^{\log_2 n}$? Tomando $\log_2$,
$$\log_2\left(3^{\log_2 n}\right) = \log_2 n \cdot \log_2 3 = \log_2\left(n^{\log_2 3}\right),$$
así que $3^{\log_2 n} = n^{\log_2 3} \approx n^{1{,}585}$. En general
$a^{\log_b n} = n^{\log_b a}$, el número de hojas de un árbol con $a$ hijos por nodo
y $\log_b n$ niveles, y esa identidad es la mitad del Teorema Maestro.

**El otro paso que todos se saltan: el acarreo.** Mira los cuadros naranja de la
figura. La suma $a + b$ de dos números de $\lceil n/2 \rceil$ dígitos
puede tener $\lceil n/2 \rceil + 1$ dígitos, y el tercer producto es un poco más grande
que la mitad; por eso el árbol de la figura tiene más de $\log_2 64 = 6$ niveles. La
recurrencia verdadera es
$$T(n) \le 3T(\lceil n/2 \rceil + 1) + cn.$$
No tiene la forma $aT(n/b)$, pero se arregla con un **cambio de variable**. Definimos
$S(n) = T(n + 2)$. Entonces
$$S(n) = T(n + 2) \le 3T\left(\left\lceil \tfrac{n + 2}{2} \right\rceil + 1\right) + c(n + 2)
= 3T\left(\left\lceil \tfrac{n}{2} \right\rceil + 2\right) + c(n + 2)
= 3S\left(\left\lceil \tfrac{n}{2} \right\rceil\right) + c(n + 2),$$
que tiene la forma de antes salvo por dos cosas: el techo y los casos base.

**El techo.** Tomemos $T(n)$ como el peor costo sobre los pares de *a lo sumo* $n$
dígitos. Así $T$, y con ella $S$, es no decreciente: agrandar $n$ solo agrega pares.
Para $n = 2^k$ el techo desaparece, y como $c(2^k + 2) \le 2c \cdot 2^k$ cuando
$k \ge 1$, el cálculo del árbol de arriba, con $2c$ en lugar de $c$ y hojas de costo
$S(1)$, da $S(2^k) \le (4c + S(1))\, 3^k$. Para un $n \ge 2$ cualquiera ($S(1)$ es
una constante, como se ve abajo), sea $2^k$ la menor potencia de 2 que no es menor que
$n$. Entonces $2^k < 2n$, así que
$3^k = (2^k)^{\log_2 3} < 3\, n^{\log_2 3}$, y por monotonía
$$S(n) \le S(2^k) < 3\,(4c + S(1))\, n^{\log_2 3}.$$
Redondear a una potencia de 2 cuesta un factor 3 en la constante, no en el exponente,
y con $T(n) = S(n - 2) \le S(n)$, también $T(n) = O(n^{\log_2 3})$. La cota es
ajustada: con $n = 2^k$, cada llamada interna tiene tres hijos de al menos la mitad de
dígitos ($a + b$ tiene al menos tantos como $a$), así que hay al menos
$3^k = n^{\log_2 3}$ hojas, con una multiplicación cada una.

**Los casos base.** La recurrencia de $S$ no achica en $n = 1$: dice
$S(1) \le 3S(1) + 3c$, que no acota nada. Es el caso $T(3)$: un número de 3 dígitos
parte en 2 y 1, la suma de las mitades llega a $99 + 9 = 108$, y el tercer producto
vuelve a tener 3 dígitos. Con $T(2) = S(0)$ pasa lo mismo. Que esas llamadas terminan
se ve por los valores: ¿cuánto llega a valer la suma de las mitades?

```{python continue}
def suma_mitades(x, n):                      # a + b al partir x como lo hace partir()
    d = a_digitos(x) + [0] * (n - len(str(x)))
    return a_entero(sumar(d[n // 2:], d[:n // 2]))

for n, tope in [(3, 999), (3, 108), (2, 99), (2, 18)]:
    print(f"n = {n}, operandos hasta {tope:>3}: a + b llega a "
          f"{max(suma_mitades(x, n) for x in range(tope + 1))}")
```

Con 3 dígitos, el tercer producto recibe operandos hasta 108, todavía de 3 dígitos,
y el suyo, hasta 18. Con 2 dígitos, de 99 se pasa a 18 y de 18 a 9, un dígito. Los
productos $ac$ y $bd$ reciben partes de a lo sumo 2 dígitos. Desde 3 dígitos la
recursión llega a uno en a lo sumo tres niveles, así que $T(2)$ y $T(3)$ son
constantes, y la demostración queda completa: la fila de Karatsuba de la tabla del
capítulo 1, $O(n^{\log_2 3})$ operaciones de un dígito, está demostrada.

## 5. Segundos, no multiplicaciones

Midamos segundos: la escolar, Karatsuba puro y Karatsuba con `umbral=16`, que usa la
escolar hasta 16 dígitos.

```{python continue}
def medir(f, x, y, repeticiones):
    mejor = float("inf")
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        f(x, y, [0])
        mejor = min(mejor, time.perf_counter() - inicio)
    return mejor

metodos = {
    "escolar": escolar,
    "Karatsuba puro": karatsuba,
    "Karatsuba, umbral 16": lambda x, y, c: karatsuba(x, y, c, umbral=16),
}
tiempos = {nombre: [] for nombre in metodos}
random.seed(3)
for n in [8, 16, 32, 64, 128, 256, 512]:
    x, y = numero(n), numero(n)
    for nombre, f in metodos.items():
        s = medir(f, x, y, 5 if n <= 128 else 3 if n == 256 else 2)
        tiempos[nombre].append((n, s))

def cruce(lento, rapido):
    """El menor n > 16 desde el que `rapido` gana siempre (hasta 16, mismo código)."""
    desde = None
    for (n, a), (_, b) in zip(tiempos[lento], tiempos[rapido]):
        if n <= 16:
            continue
        if b >= a:
            desde = None
        elif desde is None:
            desde = n
    return desde

cruce_umbral = cruce("escolar", "Karatsuba, umbral 16")
cruce_puro = cruce("escolar", "Karatsuba puro")
```

```{python continue echo=false output=asis}
ms = lambda t: f"{1000 * t:.3f}".replace(".", ",")
print("| $n$ | " + " | ".join(metodos) + " |\n|---:|" + "---:|" * len(metodos))
for i, (n, _) in enumerate(tiempos["escolar"]):
    print(f"| {n} | " + " | ".join(f"{ms(tiempos[m][i][1])} ms" for m in metodos) + " |")
print()
print(F6.grafica_log_log_marca(
      {nombre: puntos for nombre, puntos in tiempos.items()},
      "dígitos de cada factor", "segundos",
      marca=(cruce_umbral, f"cruce: {cruce_umbral}") if cruce_umbral else None,
      ident="divide-y-venceras-tiempos",
      pie=f"Tiempos medidos, el mínimo de varias repeticiones. Con umbral 16, Karatsuba "
          f"le gana a la escolar desde {cruce_umbral} dígitos; el puro, "
          f"{'en ningún tamaño medido' if not cruce_puro else f'desde {cruce_puro}'}."))
```

En multiplicaciones de un dígito, Karatsuba gana desde $n = 8$. En segundos, la
@fig-divide-y-venceras-tiempos muestra a Karatsuba puro perdiendo en todo el rango
medido: cada llamada crea listas nuevas, suma, resta y desplaza, y con números chicos
ese trabajo cuesta más que las multiplicaciones que se ahorra. Es lo que advertía el
capítulo 1, §2 y §4: contar operaciones esconde constantes. Con su pendiente menor,
Karatsuba puro termina ganando, pero quizá muy lejos.

La solución es el híbrido: recursión con números grandes y la escolar con los chicos,
que solo cambia la constante, porque la escolar se usa en hojas de tamaño acotado. Así
lo hace el Python que usamos de oráculo: CPython (`Objects/longobject.c`) usa la escolar mientras alguno de los dos
factores tenga a lo sumo 70 dígitos internos (`KARATSUBA_CUTOFF`), de 30 bits cada
uno.

```{python continue}
print("bits por dígito interno de Python:", sys.int_info.bits_per_digit,
      "→ umbral de Karatsuba en CPython:", 70 * sys.int_info.bits_per_digit, "bits")
```

El capítulo 7 multiplica dos polinomios de grado $n$ en $O(n \log n)$ operaciones
aritméticas con la transformada rápida de Fourier. Para enteros, en el modelo por bit,
cada operación sobre los coeficientes tiene su costo, y con esa idea Schönhage y
Strassen llegaron a $O(n \log n \log\log n)$ (*Schnelle Multiplikation großer Zahlen*, *Computing*,
1971). El $O(n \log n)$ para enteros llegó medio siglo después, con Harvey y van der
Hoeven (*Integer multiplication in time O(n log n)*, *Annals of Mathematics*,
2021).

## 6. El método general: árbol de recursión y Teorema Maestro

Lo que hicimos con Karatsuba sirve para cualquier recurrencia de la forma
$$T(n) = aT(n/b) + f(n),$$
con $a \ge 1$ subproblemas de tamaño $n/b$, $b > 1$, y $f(n)$ el trabajo de partir y
combinar. El nivel $i$ del árbol tiene $a^i$ nodos de tamaño $n/b^i$, así que trabaja
$a^i f(n/b^i)$, y el costo total es la suma por niveles.

**El experimento.** El trabajo de cada nivel con $f(n) = n^d$, para la búsqueda
binaria, mergesort, Karatsuba y una búsqueda que descarta la mitad con trabajo lineal.

```{python continue}
def trabajo_por_nivel(a, b, d, n):
    """El trabajo de cada nivel del árbol de aT(n/b) + n^d, hasta tamaño 1."""
    niveles, tam, nodos = [], n, 1
    while tam >= 1:
        niveles.append(nodos * tam ** d)
        tam, nodos = tam / b, nodos * a
    return niveles

n = 2 ** 10
print(f"{'recurrencia':>14} {'a/b^d':>6}   trabajo de los niveles 0, 1, 2, …, 10")
for a, b, d, nombre in [(1, 2, 0, "T(n/2) + 1"), (2, 2, 1, "2T(n/2) + n"),
                        (3, 2, 1, "3T(n/2) + n"), (1, 2, 1, "T(n/2) + n")]:
    w = trabajo_por_nivel(a, b, d, n)
    print(f"{nombre:>14} {a / b ** d:>6.2f}   "
          + " ".join(f"{v:.0f}" for v in w[:4]) + " … " + f"{w[-1]:.0f}"
          + f"   total {sum(w):.0f}")
```

En cada fila, cada nivel trabaja $r = a / b^d$ veces lo que el anterior. Con razón 1
el total es un nivel por la altura. Con razón mayor que 1, el último nivel es al menos
una fracción fija del total, $1 - 1/r$; con razón menor que 1 lo es el primero, al
menos $1 - r$. En $3T(n/2) + n$, el último nivel es un tercio del total.

**Teorema (Maestro, con potencias).** Sea $T(n) = aT(n/b) + \Theta(n^d)$ con $a \ge 1$,
$b > 1$, $d \ge 0$, y sea $r = a/b^d$. Entonces
$$T(n) = \begin{cases}
\Theta(n^d) & \text{si } r < 1, \\
\Theta(n^d \log n) & \text{si } r = 1, \\
\Theta(n^{\log_b a}) & \text{si } r > 1.
\end{cases}$$

*Demostración.* El nivel $i$ trabaja $a^i \cdot \Theta\left((n/b^i)^d\right) =
\Theta\left(n^d r^i\right)$, y hay $L + 1$ niveles, del 0 al $L = \log_b n$. El total es
$\Theta\left(n^d \sum_{i=0}^{L} r^i\right)$, y la suma geométrica vale:

- si $r < 1$, entre 1 y $1/(1 - r)$, una constante: el total es $\Theta(n^d)$;
- si $r = 1$, exactamente $L + 1$: el total es $\Theta(n^d \log n)$;
- si $r > 1$, entre $r^L$ y $r^L \cdot r/(r - 1)$: el total es $\Theta(n^d r^L)$, y
  $n^d r^{\log_b n} = n^d \cdot n^{\log_b a} / n^d = n^{\log_b a}$, por la identidad
  de la §4. $\square$

Para recordarlo: **compara el trabajo de la raíz, $n^d$, con el número de hojas,
$n^{\log_b a}$**. Gana el mayor, y si empatan se multiplica por $\log n$.

El teorema pide tres cosas que casi siempre se olvidan: **un solo tamaño** de
subproblema, un trabajo $f(n)$ que sea **una potencia** de $n$, y tamaños $n/b$
exactos. El redondeo se arregla con monotonía, y un corrimiento como el $+1$ del
acarreo con un cambio de variable, los dos como en la §4. Las otras dos hipótesis no
se arreglan, y las secciones siguientes muestran qué pasa sin ellas.

## 7. Lo que la versión con potencias no cubre: el $n \log^2 n$

En el capítulo 2, §7, ordenar la franja en cada nivel dio
$$T(n) = 2T(n/2) + n \log_2 n.$$
Aquí $f(n) = n \log n$ no es $\Theta(n^d)$ para ningún $d$, y el teorema de la §6 no
dice nada. (Hay versiones del Teorema Maestro que admiten $f(n) = n^d \log^k n$; salen
del mismo árbol, como este caso.)

El árbol sí: con $n = 2^L$, el nivel $i$ tiene $2^i$ nodos de tamaño $n/2^i$, y trabaja
$$2^i \cdot \frac{n}{2^i} \log_2 \frac{n}{2^i} = n(L - i).$$
Ya no es una serie geométrica: el trabajo **baja de a poco**, $nL, n(L-1), \dots, n$,
y la suma es
$$n \sum_{i=0}^{L-1} (L - i) = n \cdot \frac{L(L+1)}{2} = \Theta(n \log^2 n).$$
Con $T(1) = 0$ el resultado es exacto, y se puede comprobar contra la recurrencia.

```{python continue}
for L in range(1, 21):
    T = 0                                    # T(1) = 0
    for i in range(1, L + 1):                # T(2^i) = 2 T(2^(i-1)) + 2^i · i
        T = 2 * T + 2 ** i * i
    assert T == 2 ** L * L * (L + 1) // 2
    if L in (4, 10, 20):
        print(f"n = 2^{L}: T(n) = {T:,}  =  n·L(L+1)/2")
```

La deuda del capítulo 2 queda pagada: ordenar la franja en cada nivel cuesta
$\Theta(n \log^2 n)$, un factor $\log n$ más que repartir la lista ya ordenada. La
hipótesis de un solo tamaño la rompe el segundo algoritmo del capítulo.

## 8. Selección: el problema y el pivote

**El problema.** Dados $n$ elementos y un $k$ entre 0 y $n - 1$, encontrar el
$k$-ésimo menor, el que quedaría en la posición $k$ al ordenarlos; con
$k = \lfloor (n-1)/2 \rfloor$ es la mediana. Ordenar cuesta $O(n \log n)$, y nada baja
de $\Omega(n)$: a un elemento que nunca se comparó, el adversario puede darle un valor
que lo convierta en la respuesta o la saque de ella, como con el máximo del
capítulo 5, §5.

**Cómo se le ocurre a uno.** Como en quicksort, elegimos un pivote $x$ y repartimos
en menores que $x$, iguales y mayores; contando cada cubeta sabemos dónde está el
$k$-ésimo, y seguimos **solo en esa**. Con un pivote que parta por la mitad sería
$T(n) = T(n/2) + O(n)$, la cuarta fila de la §6: manda la raíz, $O(n)$.

**El intento que falla.** El pivote más fácil es el primer elemento. Sobre una entrada
ya ordenada, cada reparto quita un solo elemento.

```{python continue}
def seleccionar_ingenuo(A, k, cuenta):
    while True:                              # sin recursión: la entrada ordenada
        x = A[0]                             # la haría de profundidad n
        menores = [a for a in A if a < x]
        iguales = [a for a in A if a == x]
        cuenta[0] += len(A)                  # una comparación por elemento y ronda
        if k < len(menores):
            A = menores
        elif k < len(menores) + len(iguales):
            return x
        else:
            k -= len(menores) + len(iguales)
            A = [a for a in A if a > x]

for n in [500, 1000, 2000]:
    cuenta = [0]
    assert seleccionar_ingenuo(list(range(n)), n // 2, cuenta) == n // 2
    print(f"n = {n:>4}, entrada ordenada: {cuenta[0]:>9,} comparaciones  "
          f"({cuenta[0] / n ** 2:.3f} n²)")
```

Cuadrático. El pivote no tiene que ser la mediana: basta que deje fuera una
**fracción fija** de los elementos en el peor caso. El capítulo 8 lo consigue al azar,
con $O(n)$ en esperanza; aquí, sin azar y en el peor caso.

## 9. La mediana de las medianas

El pivote se calcula así:

1. Partir los $n$ elementos en grupos de 5 (el último puede tener menos).
2. Ordenar cada grupo y tomar su mediana, con un número constante de comparaciones
   por grupo.
3. Calcular la mediana de esas $\lceil n/5 \rceil$ medianas **con el mismo algoritmo**,
   por recursión.

Después se reparte por ese pivote en tres cubetas y se sigue en una. Son dos llamadas
recursivas de tamaños distintos.

```{python continue}
def ordenar_grupo(G, cuenta):                # inserción, contando comparaciones
    G = list(G)
    for i in range(1, len(G)):
        j = i
        while j > 0:
            cuenta[0] += 1
            if G[j] >= G[j - 1]:
                break
            G[j], G[j - 1] = G[j - 1], G[j]
            j -= 1
    return G

def pivote(A, cuenta, g=5, niveles=None, prof=0):
    """La mediana de las medianas de los grupos de g."""
    medianas = []
    for i in range(0, len(A), g):
        G = ordenar_grupo(A[i:i + g], cuenta)
        medianas.append(G[(len(G) - 1) // 2])
    return seleccionar(medianas, (len(medianas) - 1) // 2, cuenta, g, niveles, prof)

def seleccionar(A, k, cuenta, g=5, niveles=None, prof=0):
    """El k-ésimo menor de A; k = 0 es el mínimo."""
    if niveles is not None:
        niveles[prof] += len(A)              # para la figura del final
    if len(A) <= g:
        return ordenar_grupo(A, cuenta)[k]
    x = pivote(A, cuenta, g, niveles, prof + 1)
    menores, iguales, mayores = [], [], []
    for a in A:
        cuenta[0] += 1
        if a < x:
            menores.append(a)
        else:
            cuenta[0] += 1
            (iguales if a == x else mayores).append(a)
    if k < len(menores):
        return seleccionar(menores, k, cuenta, g, niveles, prof + 1)
    if k < len(menores) + len(iguales):
        return x
    return seleccionar(mayores, k - len(menores) - len(iguales), cuenta, g,
                       niveles, prof + 1)

random.seed(5)
for _ in range(3000):                        # oráculo: ordenar, con repetidos
    n = random.randint(1, 150)
    A = [random.randrange(random.choice([3, 20, 10 ** 6])) for _ in range(n)]
    k = random.randrange(n)
    assert seleccionar(A, k, [0]) == sorted(A)[k]
print("3000 instancias con repetidos: igual que sorted(A)[k]")
```

La cubeta de los iguales no es un adorno: con muchos repetidos, todos los iguales al
pivote salen del problema de una vez (ejercicio 5).

**Cuántos descarta.** Ordena cada grupo de abajo hacia arriba, pon las columnas en
orden de su mediana, y mira la @fig-divide-y-venceras-grupos, que sale de correr
`pivote` sobre 37 elementos al azar.

```{python continue echo=false output=asis}
random.seed(17)
_A = random.sample(range(10, 100), 37)
_grupos = [_A[i:i + 5] for i in range(0, len(_A), 5)]
_x = pivote(_A, [0])
_menores = sum(a < _x for a in _A)
_mayores = sum(a > _x for a in _A)
print(F6.grupos_medianas(_grupos, _x, ident="divide-y-venceras-grupos",
      pie=f"37 elementos en {len(_grupos)} grupos, cada uno ordenado de abajo hacia "
          f"arriba y en orden de su mediana; x = {_x} es la mediana de las medianas. Los "
          f"azules son ≥ x sin mirar nada más, los naranja ≤ x. De verdad quedaron "
          f"{_menores} menores y {_mayores} mayores."))
```

El argumento de la figura, en general: hay $\lceil n/5 \rceil$ medianas y $x$ es la
mediana de ellas, así que al menos $\lceil \frac12 \lceil n/5 \rceil \rceil$ son
mayores o iguales que $x$. Cada una tiene en su grupo dos elementos más que son
mayores o iguales que ella, y por tanto que $x$: tres por grupo.

**El paso que todos se saltan.** No todos esos grupos dan tres: el último puede estar
incompleto. El grupo del propio $x$ sí da tres, contando a $x$, pero lo quitamos
también para no distinguir casos; quitar grupos solo empeora la cota. Sin esos dos,
al menos
$$3\left(\left\lceil \tfrac12 \left\lceil \tfrac{n}{5} \right\rceil \right\rceil - 2\right)
\ \ge\ \frac{3n}{10} - 6$$
elementos son mayores o iguales que $x$. Ninguno está entre los menores, así que la
cubeta de los menores tiene a lo sumo $7n/10 + 6$ elementos, y por simetría la de los
mayores también. "Mayores o iguales" incluye a los iguales: el conteo funciona porque
los iguales tienen su propia cubeta.

Comprobemos la cota con miles de repartos al azar, y con una entrada construida para
el peor reparto: la mitad de los grupos con sus cinco elementos chicos, la otra mitad
con dos chicos y tres grandes.

```{python continue}
def reparto(A, g=5):
    """El tamaño de las cubetas de menores y de mayores en el primer nivel."""
    x = pivote(A, [0], g)
    return sum(a < x for a in A), sum(a > x for a in A)

random.seed(8)
peor = 0.0
for _ in range(3000):
    n = random.randint(6, 2000)
    A = random.sample(range(10 * n), n)
    lado = max(reparto(A))
    assert lado <= 7 * n / 10 + 6
    if n >= 200:
        peor = max(peor, lado / n)
print("3000 repartos al azar: ninguno pasa de 7n/10 + 6")
print(f"el peor con n >= 200 dejó {peor:.3f} n en un lado")

def construida(g, grupos):
    """grupos impar: (grupos-1)/2 grupos todo chicos, el resto con (g-1)/2 chicos."""
    A, chico, grande = [], 0, 10 ** 6
    for t in range(grupos):
        chicos = g if t < (grupos - 1) // 2 else (g - 1) // 2
        A += list(range(chico, chico + chicos))
        A += list(range(grande, grande + g - chicos))
        chico, grande = chico + chicos, grande + g - chicos
    return A

A = construida(5, 201)
print(f"construida, n = {len(A)}: menores = {reparto(A)[0]} = "
      f"{reparto(A)[0] / len(A):.3f} n")
```

Al azar, con $n \ge 200$, el peor reparto dejó $0{,}558\,n$ en un lado. La entrada construida deja 702 de 1005, casi $0{,}7\,n$: la cota se alcanza.

El algoritmo es de Blum, Floyd, Pratt, Rivest y Tarjan, *Time bounds for selection*,
*Journal of Computer and System Sciences*, 1973.

## 10. La recurrencia que el Teorema Maestro no resuelve

Con $a$ la constante del trabajo lineal (ordenar los grupos y repartir),
$$T(n) \le T(\lceil n/5 \rceil) + T(7n/10 + 6) + an.$$
Con dos tamaños distintos, no hay un $a$ ni un $b$ que poner en el Teorema Maestro.

**El experimento.** Comparaciones por elemento sobre entradas al azar y ordenadas: si
el algoritmo es lineal, las columnas se quedan quietas.

```{python continue}
def comparaciones_por_elemento(g, n, tipo):
    """Seleccionar la mediana; la entrada al azar depende solo de n."""
    A = random.Random(n).sample(range(10 * n), n) if tipo == "azar" else list(range(n))
    cuenta = [0]
    assert seleccionar(A, n // 2, cuenta, g) == sorted(A)[n // 2]
    return cuenta[0] / n

print(f"{'n':>6} {'al azar':>8} {'ordenada':>9}")
for n in [1000, 4000, 16000]:
    print(f"{n:>6} {comparaciones_por_elemento(5, n, 'azar'):>8.2f} "
          f"{comparaciones_por_elemento(5, n, 'ordenada'):>9.2f}")
```

Se mueve poco, y siempre por debajo de 10.

**El árbol.** Olvidemos un momento el techo y el $+6$. La raíz trabaja $an$. Sus dos
hijos tienen tamaños $n/5$ y $7n/10$, que suman $9n/10$, así que juntos trabajan
$\frac{9}{10}an$. Cada nodo reparte su tamaño de la misma manera, así que el nivel $i$
trabaja a lo sumo $(9/10)^i an$. La serie es geométrica y **decreciente**:
$$T(n) \le an \sum_{i \ge 0} \left(\frac{9}{10}\right)^i = 10an.$$
Manda la raíz, aunque el árbol no sea regular.

**La demostración por sustitución**, con lo que el árbol olvidó. Probamos por
inducción fuerte que $T(n) \le cn$ para todo $n \ge 1$, con $c$ por
elegir. Para $n < 140$, $T(n)$ es una constante y basta con tomar $c$ grande. Para
$n \ge 140$, los dos tamaños, $\lceil n/5 \rceil$ y $7n/10 + 6$, son menores que $n$,
y por hipótesis de inducción
$$T(n) \le c\left(\frac{n}{5} + 1\right) + c\left(\frac{7n}{10} + 6\right) + an
= \frac{9cn}{10} + 7c + an.$$
Queremos que eso sea a lo sumo $cn$, es decir, $c\left(\frac{n}{10} - 7\right) \ge an$.
Con $n \ge 140$, $\frac{n}{10} - 7 \ge \frac{n}{20}$, así que basta $c \ge 20a$.
$\square$

**El paso que todos se saltan.** Todo depende de que $\frac15 + \frac{7}{10} =
\frac{9}{10}$ sea **menor que 1**. Ese décimo que sobra paga las constantes: el $+1$
del techo y el $+6$ suman $7c$, y $\frac{cn}{10}$ las cubre en cuanto $n \ge 140$. Si
la suma fuera 1 no habría margen, y la sustitución no cerraría con ningún $c$.

Evaluemos la recurrencia con el conteo exacto de la §9, $a = 1$ y $T(n) = n$ para
$n < 140$.

```{python continue}
@lru_cache(None)
def cota(n, g):
    """La recurrencia de la mediana de medianas con grupos de g."""
    if n < 140:
        return n
    medianas = -(-n // g)                                # techo de n / g
    lado = n - (g + 1) // 2 * (-(-medianas // 2) - 2)    # n menos los descartados
    return cota(medianas, g) + cota(lado, g) + n

assert all(cota(n, 5) <= 20 * n for n in range(1, 30_000))
print("T(n) <= 20 n para todo n < 30 000")
for n in [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]:
    print(f"n = {n:>10,}   T(n)/n = {cota(n, 5) / n:.2f}")
```

La razón crece cada vez más despacio, de 4,18 a 8,66, y no pasa del $c = 20a$ de la
demostración en ningún $n$ comprobado. El árbol había dado 10; la sustitución es más
holgada porque paga el techo y el $+6$.

## 11. El error plantado: grupos de 3

¿Por qué 5? Con grupos de 3 la mediana de cada grupo cuesta menos comparaciones, y el
código es el mismo con `g=3`.

```{python continue}
random.seed(5)
for _ in range(3000):
    n = random.randint(1, 150)
    A = [random.randrange(random.choice([3, 20, 10 ** 6])) for _ in range(n)]
    k = random.randrange(n)
    assert seleccionar(A, k, [0], g=3) == sorted(A)[k]
print("grupos de 3, 3000 instancias: igual que sorted(A)[k]")

print(f"{'n':>6} {'g=3 azar':>9} {'g=5 azar':>9} {'g=3 ordenada':>13} {'g=5 ordenada':>13}")
for n in [1000, 4000, 16000]:
    print(f"{n:>6} {comparaciones_por_elemento(3, n, 'azar'):>9.2f} "
          f"{comparaciones_por_elemento(5, n, 'azar'):>9.2f} "
          f"{comparaciones_por_elemento(3, n, 'ordenada'):>13.2f} "
          f"{comparaciones_por_elemento(5, n, 'ordenada'):>13.2f}")
```

Ninguna prueba lo atrapa: la variante **es** correcta. Su columna al azar sube algo más que la de grupos de 5, de 10,58 a 12,30 contra 8,78 a 9,73, pero
con tres puntos no se distingue un $\log n$ que crece despacio de una curva que se
aplana.

Lo que se rompió está en la demostración. Rehaz el conteo de la §9 con grupos de 3:
cada mediana mayor o igual que $x$ arrastra **una** más de su grupo, no dos. Al menos
$2\left(\lceil \frac12 \lceil n/3 \rceil \rceil - 2\right) \ge n/3 - 4$ elementos son
mayores o iguales que $x$, y la cubeta de la recursión puede tener $2n/3 + 4$. La
recurrencia es
$$T(n) \le T(\lceil n/3 \rceil) + T(2n/3 + 4) + an,$$
y ahora $\frac13 + \frac23 = 1$: no hay margen. En el árbol, cada nivel trabaja $an$
mientras ninguna rama se haya acabado, y la rama más larga, la que siempre toma los
$2/3$, tiene $\log_{3/2} n$ niveles. La cota que sale es $O(n \log n)$, y la
sustitución de la §10 no cierra con ningún $c$: queda
$c\left(\frac{n}{3} + \frac{2n}{3}\right) + \dots = cn + \dots$, que nunca es
$\le cn$.

La recurrencia evaluada con la función de la §10, para grupos de 3, 5 y 7:

```{python continue}
print(f"{'n':>12} {'g = 3':>7} {'g = 5':>7} {'g = 7':>7}")
for n in [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]:
    print(f"{n:>12,} {cota(n, 3) / n:>7.2f} {cota(n, 5) / n:>7.2f} "
          f"{cota(n, 7) / n:>7.2f}")

print(f"g = 3, n < 30 000: T(n) <= 20 n en todos; el máximo de T(n)/n es "
      f"{max(cota(n, 3) / n for n in range(1, 30_000)):.2f}")

A = construida(3, 201)
print(f"construida con grupos de 3, n = {len(A)}: menores = {reparto(A, 3)[0]} = "
      f"{reparto(A, 3)[0] / len(A):.3f} n")
```

```{python continue echo=false output=asis}
_ns = [int(10 ** (e / 2)) for e in range(4, 15)]
print(F6.grafica_log_lineal(
      {f"g = {g}": [(n, cota(n, g) / n) for n in _ns] for g in (3, 5, 7)},
      "n", "T(n) / n", ident="divide-y-venceras-cotas-grupos",
      pie=f"La recurrencia de la mediana de medianas evaluada exactamente. Con grupos de "
          f"3, T(n)/n llega a {f'{cota(10 ** 7, 3) / 10 ** 7:.1f}'.replace('.', ',')} en n = 10⁷ y sigue "
          f"subiendo; con 5 y con 7 se aplana."))
```

En la @fig-divide-y-venceras-cotas-grupos, con 5 y con 7 la cota por elemento se
aplana y con 3 sube como $\log n$. (Que 7 quede por debajo de 5 no es una ventaja
medida: `cota` cobra $a = 1$ por elemento con cualquier $g$, y ordenar grupos de 7
cuesta más.) La entrada construida muestra que el reparto de $2/3$ se alcanza, al
menos en un nivel. Y la comprobación de la §10, $T(n) \le 20n$ para $n < 30\,000$,
también pasa con grupos de 3: una comprobación finita no distingue lineal de
$n \log n$, y por eso hacía falta la sustitución.

Seamos precisos: **la demostración ya no garantiza $O(n)$**, pero no dice que haya
entradas en las que la variante tarde $\Theta(n \log n)$. Para eso habría que
forzar el peor reparto en todos los niveles a la vez, también en la llamada sobre las
medianas, y no lo hemos construido. Una cota superior que deja de valer no es una cota
mínima.

En los capítulos 2 y 3 el error plantado estaba en la respuesta, y una batería de
pruebas bien pensada lo atrapaba. Aquí falla una **garantía de costo en el peor
caso**, y las pruebas miden las entradas que alguien eligió, mientras que el peor caso
es justo la que nadie eligió. Solo la demostración lo verifica, y dice qué vigilar:
que las fracciones sumen menos de 1.

## 12. La regla

```{python continue echo=false output=asis}
random.seed(4)
_niv_sel = defaultdict(int)
seleccionar(random.sample(range(10 ** 6), 4096), 2048, [0], niveles=_niv_sel)
_perfil_sel = [_niv_sel[d] for d in sorted(_niv_sel)]
print(F6.perfiles_nivel(
      {"Karatsuba": [sum(v) for v in niveles64],
       "mergesort": trabajo_por_nivel(2, 2, 1, 64),
       "selección": _perfil_sel},
      ident="divide-y-venceras-perfiles",
      pie=f"El trabajo por nivel, relativo al nivel 0 (la línea de puntos). Karatsuba "
          f"es la corrida de la §4, la selección busca la mediana de 4096 elementos y "
          f"mergesort sale de su recurrencia."))
```

La @fig-divide-y-venceras-perfiles pone juntos los tres comportamientos del capítulo:
en Karatsuba el trabajo de un nivel crece hacia abajo (los dos últimos niveles caen
porque son las pocas ramas que el acarreo alargó), en mergesort se queda igual y en
la selección decrece. La regla es esa: **el costo de un divide y vencerás lo decide cómo cambia el trabajo
de un nivel al siguiente**. Si decrece geométricamente, manda la raíz; si crece
geométricamente, mandan las hojas; si se queda igual, se multiplica por la altura. El
Teorema Maestro es esta regla cuando el cambio es una razón fija $a/b^d$, y el árbol
la aplica también cuando no lo es: la selección, con dos tamaños, y el $n \log^2 n$,
donde el trabajo baja de a poco.

Las recurrencias vuelven: la FFT del capítulo 7 tiene la de mergesort,
$2T(n/2) + O(n)$; el capítulo 8 hace la selección con un pivote al azar; el 12 usa
divide y vencerás dentro de una programación dinámica (Hirschberg), y el 20 analiza
recurrencias que restan en lugar de dividir, como $T(n) = T(n-1) + T(n-4)$.

## Resumen

- Divide y vencerás: partir, resolver por recursión, combinar. Su costo es una
  recurrencia, y lo difícil es resolverla.
- Karatsuba calcula $ad + bc$ como $(a + b)(c + d) - ac - bd$: tres productos de la
  mitad en vez de cuatro, y $\Theta(n^{\log_2 3})$ en vez de $\Theta(n^2)$. El acarreo
  se resuelve con un cambio de variable, y el techo con monotonía.
- El árbol de recursión suma el trabajo por niveles. El Teorema Maestro es su
  corolario para $aT(n/b) + \Theta(n^d)$: compara la raíz, $n^d$, con las hojas,
  $n^{\log_b a}$. Esa versión no cubre $2T(n/2) + n \log n = \Theta(n \log^2 n)$ ni
  tamaños distintos; el árbol sí.
- La mediana de las medianas descarta al menos $3n/10 - 6$ elementos: la selección es
  $O(n)$ porque $\frac15 + \frac{7}{10} < 1$.
- Con grupos de 3 la suma es 1 y la demostración ya no da $O(n)$, aunque la respuesta
  siga siendo correcta: una garantía de peor caso solo la da la demostración.

## Ejercicios

1. Multiplica $1234 \times 5678$ a mano con el Karatsuba de la §3, que rellena con
   ceros el factor más corto antes de partir. Dibuja el árbol de llamadas con sus
   tamaños y cuenta las multiplicaciones de un dígito. ¿Aparece alguna llamada más grande que la mitad de
   su padre? ¿Por qué?
2. Resuelve $T(n) = 2T(n/2) + n / \log_2 n$ con el árbol de recursión, para $n$
   potencia de 2. ¿A qué caso del teorema de la §6 se parece, y por qué no se aplica?
3. Resuelve $T(n) = 2T(\sqrt n) + \log_2 n$ con un cambio de variable. (Pista: mira
   la recurrencia como función de $m = \log_2 n$.)
4. La §11 dio con el árbol la cota superior $O(n \log n)$ para
   $T(n) = T(n/3) + T(2n/3) + n$. Demuestra que también es $\Omega(n \log n)$. Cuidado:
   las ramas del árbol tienen largos distintos. ¿Hasta qué nivel existen todos los
   nodos?
5. Una versión de la selección reparte los elementos en menores que $x$ y mayores que
   $x$, sin cubeta de iguales. Si $k$ es el número de menores devuelve $x$; si es
   menor, sigue en los menores; si no, sigue en los mayores con $k$ menos los menores
   menos 1. Pasa miles de pruebas con elementos distintos. Construye la entrada más
   corta en la que falla, y explica qué hace la cubeta de iguales de la §9 que esta
   versión no hace.
6. Con grupos de 7, rehaz el conteo de la §9 y la recurrencia de la §10. ¿Sigue siendo
   lineal? ¿Cómo cambian la razón con que decrece el árbol y el trabajo por elemento de
   cada nivel?
7. Con el parámetro `umbral` de Karatsuba, mide para varios umbrales y varios $n$ cuál
   es el mejor en tu máquina. ¿Coincide con el
   cruce de la @fig-divide-y-venceras-tiempos? ¿Por qué no tendría que coincidir?
8. Una inversión de $A$ es un par $i < j$ con $A[i] > A[j]$. Cuéntalas en
   $O(n \log n)$, y demuestra que el paso de combinar cuenta bien las que cruzan de una
   mitad a la otra.
9. Dados dos arreglos ordenados de largo $n$, encuentra el $k$-ésimo menor de su unión
   en $O(\log n)$ comparaciones, con su recurrencia.
10. ★ Toom-3 parte cada número en tres, $x = x_2 \cdot 10^{2m} + x_1 \cdot 10^m + x_0$,
    y calcula el producto con 5 productos de un tercio del tamaño. Escribe la
    recurrencia y su exponente, y compáralo con el de Karatsuba. Explica por qué no
    alcanzan 4 productos con la misma idea de evaluar e interpolar. (Pista: mira $x$ y $y$ como
    polinomios de grado 2 en $10^m$. ¿Qué grado tiene su producto, y cuántos valores
    lo determinan?)
