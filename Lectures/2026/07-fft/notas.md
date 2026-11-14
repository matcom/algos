# Divide y vencerás: la transformada rápida de Fourier {#chap-fft}

El capítulo 6 bajó el costo de multiplicar de $n^2$ a $n^{\log_2 3}$ partiendo cada
número en dos mitades. Este capítulo lo baja a $O(n \log n)$, para polinomios, con dos
ideas nuevas. La primera es partir de otra manera: no en la mitad de arriba y la de
abajo, sino en los coeficientes pares y los impares. La segunda es no multiplicar donde
multiplicar es caro. Un polinomio se puede escribir con sus coeficientes o con sus
valores en unos cuantos puntos, y en valores multiplicar cuesta $O(n)$. El algoritmo
cambia de representación, multiplica y vuelve, y paga los dos cambios con divide y
vencerás.

```{python echo=false output=asis}
import cmath
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(".."))   # donde viven figuras.py y figuras_07.py
import figuras_07 as F7
```

## 1. Multiplicar polinomios

Un polinomio de grado $n - 1$ es la lista de sus $n$ coeficientes,
$A(x) = a_0 + a_1 x + \dots + a_{n-1} x^{n-1}$, y en el código es la lista
`[a0, a1, ..., a(n-1)]`. El producto $C = AB$ de dos polinomios con $n_A$ y $n_B$
coeficientes tiene $n_A + n_B - 1$ coeficientes, y cada uno es una suma:
$$c_k = \sum_{i + j = k} a_i \, b_j .$$
Esa operación entre dos listas se llama **convolución**. El algoritmo directo hace un
producto por cada par $(i, j)$:

```{python continue}
def ingenua(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c

print(ingenua([1, 2], [3, 1, 4]))      # (1 + 2x)(3 + x + 4x²)
```

Con $n$ coeficientes cada uno son $n^2$ multiplicaciones. Va a ser el oráculo del
capítulo: cada algoritmo nuevo se prueba contra él.

El modelo de costo: cada operación entre dos coeficientes cuesta 1, sin importar su
tamaño, como en la RAM del capítulo 1 con aritmética de costo unitario. La §10 muestra
dónde la máquina deja de cumplirlo, y la §12 vuelve sobre los enteros grandes, que el
capítulo 1 (§9) mide en bits.

Con esa cuenta, el Karatsuba del capítulo 6 ya multiplica polinomios en
$\Theta(n^{\log_2 3})$: un entero en base 10 es un polinomio evaluado en $x = 10$, más
los acarreos. El ejercicio 10 del capítulo 6 (Toom-3) dejaba la pista que sigue este
capítulo: evaluar los factores en unos puntos y reconstruir el producto a partir de
los valores.

## 2. Coeficientes y valores

Dos puntos determinan una recta y tres determinan una parábola. En general:

**Teorema.** Sean $x_0, \dots, x_d$ números distintos y $y_0, \dots, y_d$ cualesquiera.
Existe un único polinomio $P$ de grado a lo sumo $d$ con $P(x_i) = y_i$ para todo $i$.

*Demostración.* Existencia: el polinomio de Lagrange
$$P(x) = \sum_{i=0}^{d} y_i \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}$$
tiene grado a lo sumo $d$, porque cada producto tiene $d$ factores lineales. En $x_i$
el término $i$ vale $y_i$ y todos los demás valen 0, porque contienen el factor
$x_i - x_i$. Unicidad: si $P$ y $Q$ cumplen las dos condiciones, $P - Q$ tiene grado a
lo sumo $d$ y se anula en los $d + 1$ puntos $x_i$. Un polinomio no nulo de grado a lo
sumo $d$ tiene a lo sumo $d$ raíces, que es el teorema del factor de Álgebra: cada raíz
$r$ saca un factor $(x - r)$ y el grado baja en uno. Así que $P - Q = 0$. $\square$

Un polinomio de grado $d$ se puede guardar, entonces, como sus valores en $d + 1$
puntos fijos. En esa representación el producto es barato: si conocemos $A(x_i)$ y
$B(x_i)$, entonces $C(x_i) = A(x_i) B(x_i)$, con una multiplicación por punto. Pero hay
una condición que es fácil pasar por alto, y que el teorema dice con todas las letras:
$C$ tiene grado $d = (n_A - 1) + (n_B - 1)$, así que necesita $d + 1$ puntos. Para dos
factores de $n$ coeficientes son $2n - 1$ puntos, no $n$. La §8 muestra qué pasa cuando
falta uno.

El plan queda así:

1. **Evaluar** $A$ y $B$ en $N \ge d + 1$ puntos.
2. **Multiplicar** punto a punto: $N$ productos.
3. **Interpolar**: volver de los $N$ valores de $C$ a sus coeficientes.

El paso 2 cuesta $O(n)$. El paso 1 no: con Horner, evaluar en un punto cuesta $n$
multiplicaciones, y en $N \approx 2n$ puntos, $\Theta(n^2)$. Con puntos cualesquiera el
plan empata con la ingenua. Falta elegir los puntos.

## 3. Cómo se le ocurre a uno: pares e impares

Los puntos se pueden elegir. Hay que buscar unos donde evaluar en muchos puntos cueste
menos que evaluar en cada uno por separado. Separemos los coeficientes de índice par de
los de índice impar:
$$A(x) = (a_0 + a_2 x^2 + a_4 x^4 + \dots) + x\,(a_1 + a_3 x^2 + a_5 x^4 + \dots)
       = A_{\text{par}}(x^2) + x\,A_{\text{impar}}(x^2),$$
donde $A_{\text{par}}$ tiene los coeficientes $(a_0, a_2, \dots)$ y $A_{\text{impar}}$
los $(a_1, a_3, \dots)$. Cada uno tiene la mitad de coeficientes que $A$. Fíjate en lo
que pasa en $x$ y en $-x$:
$$A(x) = A_{\text{par}}(x^2) + x\,A_{\text{impar}}(x^2), \qquad
  A(-x) = A_{\text{par}}(x^2) - x\,A_{\text{impar}}(x^2).$$
Los dos valores usan los mismos dos números, $A_{\text{par}}(x^2)$ y
$A_{\text{impar}}(x^2)$. Si los $n$ puntos vienen en parejas $\pm x$, evaluar $A$ en
ellos se reduce a evaluar dos polinomios de la mitad de tamaño en los $n/2$ cuadrados,
más $O(n)$ para combinar. Eso es $T(n) = 2T(n/2) + O(n)$, la recurrencia de mergesort.

Pero la recursión tiene que poder seguir: los $n/2$ cuadrados también tienen que venir
en parejas $\pm$. Probemos con números reales:

```{python continue}
puntos = [1, -1, 2, -2]
print("puntos:", puntos, " cuadrados:", sorted({x * x for x in puntos}))
```

El segundo nivel falla, porque un cuadrado real nunca es negativo: ningún conjunto de
reales sirve para más de un nivel. Busquemos de abajo hacia arriba. Si el último nivel
es $\{1\}$, el anterior es $\{1, -1\}$, y el anterior, sus raíces cuadradas:
$\pm 1$ y $\pm i$. Hay que salir de los reales.

## 4. Las raíces de la unidad y el lema de la mitad

Una **raíz $n$-ésima de la unidad** es un complejo $z$ con $z^n = 1$. Hay exactamente
$n$, repartidas a distancias iguales en el círculo de radio 1:
$$\omega_n^k = e^{2\pi i k/n} = \cos\frac{2\pi k}{n} + i \sin\frac{2\pi k}{n},
  \qquad k = 0, 1, \dots, n - 1,$$
donde $\omega_n = e^{2\pi i/n}$ es la **raíz principal**. Multiplicar por $\omega_n$
es girar $1/n$ de vuelta. Antes de demostrar nada, veamos a qué raíz cuarta va a parar el
cuadrado de cada raíz octava:

```{python continue}
def raiz(n, k):
    return cmath.exp(2j * math.pi * k / n)

def cuadrados(n):
    """Para cada k, el j tal que (ω_n^k)² = ω_{n/2}^j."""
    destino = {}
    for k in range(n):
        z = raiz(n, k) ** 2
        destino[k] = [j for j in range(n // 2) if abs(z - raiz(n // 2, j)) < 1e-12]
    return destino

dest8 = cuadrados(8)
print({k: d for k, d in dest8.items()})
for n in [2, 4, 8, 16, 32, 64]:
    d = cuadrados(n)
    assert all(len(v) == 1 for v in d.values())            # cae en una raíz n/2-ésima
    assert all(sum(v == [j] for v in d.values()) == 2      # y cada una, dos veces
               for j in range(n // 2))
print("comprobado para n = 2 a 64")
```

```{python continue echo=false output=asis}
print(F7.raices([raiz(8, k) for k in range(8)], {k: v[0] for k, v in dest8.items()},
      pie="Las 8 raíces octavas de la unidad, a la izquierda, y sus cuadrados, a la "
          "derecha. Cada raíz cuarta recibe dos cuadrados, el de ω<sup>k</sup> y el de "
          "ω<sup>k+4</sup> = −ω<sup>k</sup>. Las posiciones y las etiquetas salen de la "
          "función <code>cuadrados</code>."))
```

La @fig-fft-raices muestra lo que dice la salida: los 8 cuadrados caen en las 4 raíces
cuartas, dos en cada una, y las dos que caen juntas son opuestas. Eso es lo que hacía
falta.

**Lema de la mitad.** Sea $n$ par. Entonces $\omega_n^{k + n/2} = -\omega_n^k$, y los
cuadrados de las $n$ raíces $n$-ésimas de la unidad son las $n/2$ raíces $n/2$-ésimas,
cada una exactamente dos veces.

*Demostración.* Primero, $\omega_n^{n/2} = e^{\pi i} = -1$, así que
$\omega_n^{k + n/2} = \omega_n^k \omega_n^{n/2} = -\omega_n^k$. Segundo,
$(\omega_n^k)^2 = e^{2\pi i \cdot 2k/n} = e^{2\pi i k/(n/2)} = \omega_{n/2}^k$. Como
$\omega_{n/2}^{n/2} = 1$, el valor $\omega_{n/2}^k$ depende solo del resto de $k$
módulo $n/2$. Cuando $k$ recorre $0, \dots, n - 1$, ese resto toma cada valor
$j \in \{0, \dots, n/2 - 1\}$ exactamente dos veces, en $k = j$ y en $k = j + n/2$. Y
las $\omega_{n/2}^j$ con $j < n/2$ son distintas, porque son puntos distintos del
círculo. $\square$

No basta con que los cuadrados sean la mitad de puntos: los reales
$\{1, -1, 2, -2\}$ también daban la mitad. Lo que hace seguir a la recursión es que el
conjunto de abajo vuelve a ser de raíces de la unidad, y por la primera parte del lema
vuelve a venir en parejas $\pm$. Con $n$ potencia de dos, eso se repite hasta $n = 1$.

## 5. La FFT

La **transformada discreta de Fourier** (DFT) de $(a_0, \dots, a_{n-1})$ es la lista de
valores de $A$ en las $n$ raíces $n$-ésimas:
$$y_k = A(\omega_n^k) = \sum_{j=0}^{n-1} a_j \, \omega_n^{jk},
  \qquad k = 0, \dots, n - 1.$$
(Otros textos usan $e^{-2\pi i/n}$; cambia solo cuál transformada se llama directa.)
La definición, escrita tal cual, cuesta $n^2$ y es el oráculo:

```{python continue}
def dft(a, signo=1):
    n = len(a)
    return [sum(a[j] * raiz(n, signo * j * k) for j in range(n)) for k in range(n)]
```

La **transformada rápida** (FFT) es el divide y vencerás de la §3 sobre esos puntos.
Si $P$ es la DFT de los pares e $I$ la de los impares, las dos de tamaño $n/2$, para
$k < n/2$:
$$y_k = P_k + \omega_n^k I_k, \qquad y_{k + n/2} = P_k - \omega_n^k I_k.$$

*Demostración.* Por la separación de la §3,
$y_k = A_{\text{par}}(\omega_n^{2k}) + \omega_n^k A_{\text{impar}}(\omega_n^{2k})$. Por
el lema, $\omega_n^{2k} = \omega_{n/2}^k$, así que $A_{\text{par}}(\omega_n^{2k}) = P_k$
y $A_{\text{impar}}(\omega_n^{2k}) = I_k$ para $k < n/2$. Para $k + n/2$, el cuadrado
es el mismo, $\omega_n^{2k + n} = \omega_n^{2k}$, y el factor cambia de signo por la
primera parte del lema. Con eso, la corrección de la FFT sale por inducción en $n$: el
caso $n = 1$ es $y_0 = a_0$. $\square$

```{python continue}
def fft(a, signo=1):
    n = len(a)                         # n es potencia de dos
    if n == 1:
        return a[:]
    pares, impares = fft(a[0::2], signo), fft(a[1::2], signo)
    y = [0] * n
    for k in range(n // 2):
        t = raiz(n, signo * k) * impares[k]
        y[k], y[k + n // 2] = pares[k] + t, pares[k] - t
    return y

random.seed(1)
for n in [1, 2, 4, 8, 16, 64, 256]:
    a = [random.uniform(-1, 1) for _ in range(n)]
    assert max(abs(u - v) for u, v in zip(fft(a), dft(a))) < 1e-9
print("fft == dft para n = 1 a 256")
print("DFT de (1, 1, 0, 0):", [complex(round(z.real, 12), round(z.imag, 12))
                               for z in fft([1, 1, 0, 0])])
```

Hagamos la última a mano: $A(x) = 1 + x$, $n = 4$, $\omega_4 = i$. Pares e impares son
$(1, 0)$, cuya DFT de tamaño 2 es $(1, 1)$. Al combinar, con $k = 0$: $y_0 = 1 + 1 \cdot 1 = 2$ y
$y_2 = 1 - 1 = 0$. Con $k = 1$: $y_1 = 1 + i \cdot 1 = 1 + i$ e $y_3 = 1 - i$. Es
$1 + i^k$ para $k = 0, 1, 2, 3$, como tenía que ser.

El costo es $T(n) = 2T(n/2) + \Theta(n)$: el ciclo de combinar hace $n/2$
multiplicaciones y $n$ sumas, y cada $\omega_n^k$ cuesta $O(1)$ en el modelo aritmético
(la §9 los precalcula). Por el Teorema Maestro del capítulo 6, con $a = b = 2$ y
$d = 1$, $T(n) = \Theta(n \log n)$.

## 6. La inversa

Falta el paso 3: volver de los valores a los coeficientes. Escrita como matriz, la DFT
es $y = V a$, con $V_{kj} = \omega_n^{kj}$, la matriz de Vandermonde de los puntos
$\omega_n^0, \dots, \omega_n^{n-1}$. Por el teorema de la §2, $V$ es invertible.
Resulta que su inversa es casi ella misma. Para verlo hace falta un lema.

**Lema de la suma.** Para todo entero $k$,
$\sum_{j=0}^{n-1} \omega_n^{jk}$ vale $n$ si $n$ divide a $k$, y $0$ si no.

*Demostración.* Si $n \mid k$, cada término es $\omega_n^{jk} = 1$ y la suma es $n$. Si
no, $q = \omega_n^k \ne 1$, porque las únicas potencias de $\omega_n$ que valen 1 son
las de exponente múltiplo de $n$. Entonces es una serie geométrica de razón $q \ne 1$:
$$\sum_{j=0}^{n-1} q^j = \frac{q^n - 1}{q - 1} = \frac{(\omega_n^n)^k - 1}{q - 1}
  = \frac{1 - 1}{q - 1} = 0. \qquad \square$$

**Teorema.** $(V^{-1})_{jl} = \omega_n^{-jl}/n$. Es decir, interpolar en las raíces de
la unidad es aplicar la DFT con $\omega_n^{-1}$ en lugar de $\omega_n$ y dividir entre
$n$.

*Demostración.* Sea $W_{jl} = \omega_n^{-jl}/n$. La entrada $(k, l)$ de $VW$ es
$$\sum_{j=0}^{n-1} \omega_n^{kj} \frac{\omega_n^{-jl}}{n}
  = \frac{1}{n} \sum_{j=0}^{n-1} \omega_n^{j(k - l)} .$$
Como $0 \le k, l < n$, se tiene $-n < k - l < n$, y $n$ divide a $k - l$ solo si
$k = l$. Por el lema de la suma, la entrada vale $1$ si $k = l$ y $0$ si no:
$VW = I$. $\square$

La inversa es la misma `fft` con `signo=-1` y una división entre $N$. El plan de la §2
cabe en unas líneas, con $N$ la menor potencia de dos $\ge d + 1$:

```{python continue}
def multiplicar(a, b):
    m = len(a) + len(b) - 1            # coeficientes de C: grado d = m - 1
    N = 1
    while N < m:                       # N >= d + 1 puntos
        N *= 2
    fa = fft(a + [0] * (N - len(a)))
    fb = fft(b + [0] * (N - len(b)))
    c = fft([u * v for u, v in zip(fa, fb)], signo=-1)
    return [round((z / N).real) for z in c[:m]]

random.seed(2)
for _ in range(300):
    a = [random.randint(-9, 9) for _ in range(random.randint(1, 40))]
    b = [random.randint(-9, 9) for _ in range(random.randint(1, 40))]
    assert multiplicar(a, b) == ingenua(a, b)
print("multiplicar == ingenua en 300 pares al azar")
```

Son tres FFT de tamaño $N < 2m$ y $N$ productos: $\Theta(n \log n)$ operaciones sobre
coeficientes. El `round` está porque el producto de enteros es entero, y el punto
flotante solo lo aproxima. La §10 mide cuándo el redondeo deja de dar el entero bueno.

La FFT se suele atribuir a Cooley y Tukey, "An algorithm for the machine calculation of
complex Fourier series" (*Mathematics of Computation*, 1965). Heideman, Johnson y
Burrus ("Gauss and the history of the fast Fourier transform", *IEEE ASSP Magazine*,
1984) mostraron que Gauss ya había descrito el método hacia 1805, en un trabajo que no
publicó en vida.

## 7. El experimento: cuándo gana

El $O(n \log n)$ esconde constantes. La `fft` hace una llamada recursiva por cada
elemento, crea listas nuevas en cada nivel y calcula exponenciales complejas. La
ingenua solo multiplica enteros chicos. Midamos:

```{python continue}
def mejor_de(veces, f, *args):         # el menor de varios tiempos: el menos ruidoso
    mejor = float("inf")
    for _ in range(veces):
        t = time.perf_counter(); f(*args); mejor = min(mejor, time.perf_counter() - t)
    return mejor

tiempos = []
print(f"{'n':>6} {'ingenua (s)':>12} {'fft (s)':>9}")
for n in [64, 128, 256, 512, 1024, 2048]:
    a = [random.randrange(10) for _ in range(n)]
    b = [random.randrange(10) for _ in range(n)]
    t1, t2 = mejor_de(3, ingenua, a, b), mejor_de(3, multiplicar, a, b)
    tiempos.append((n, t1, t2))
    print(f"{n:>6} {t1:>12.4f} {t2:>9.4f}")
desde = None                       # la menor n desde la que la fft gana en todas las filas
for n_fila, t1_fila, t2_fila in reversed(tiempos):
    if t2_fila >= t1_fila:
        break
    desde = n_fila
print("la fft gana en todas las filas desde n =", desde if desde else "ninguna",
      f"| en n = {n}, {t1 / t2:.1f} veces más rápida")
```

La última línea dice desde qué fila gana la FFT en todas las siguientes, y por cuánto
gana con 2048. Los tiempos cambian de una medición a otra; lo que se repite es la
forma: con $n$ chico no hay un
ganador claro, y desde unos cientos de coeficientes la ventaja de la FFT crece con $n$,
porque una curva es cuadrática y la otra casi lineal.

Es la lección de Karatsuba en el capítulo 6: el exponente decide a la larga y la
constante decide dónde empieza a decidir.

## 8. El error plantado

Esta variante cambia un solo carácter: `while N < m - 1` en lugar de `while N < m`. Es
decir, toma la menor potencia de dos $N \ge d$ en vez de $N \ge d + 1$, con
$d = n_A + n_B - 2$, el grado del producto. Es un error natural, porque uno piensa en el
grado y no en el número de coeficientes.

```{python continue}
def multiplicar_mal(a, b):
    m = len(a) + len(b) - 1
    N = 1
    while N < m - 1:                   # N >= d: un punto menos
        N *= 2
    fa = fft(a + [0] * (N - len(a)))
    fb = fft(b + [0] * (N - len(b)))
    c = fft([u * v for u, v in zip(fa, fb)], signo=-1)
    return [round((z / N).real) for z in c[:m]]

def falla(a, b):
    try:
        return multiplicar_mal(a, b) != ingenua(a, b)
    except Exception:
        return True

for L in [4, 8, 16, 64, 256, 1024]:     # largos iguales, potencias de dos
    a = [random.randint(-9, 9) for _ in range(L)]
    b = [random.randint(-9, 9) for _ in range(L)]
    assert not falla(a, b)
print("largos iguales 4 a 1024: ninguna falla")
print("(1 + x)(1 + x):", multiplicar_mal([1, 1], [1, 1]), "en vez de", ingenua([1, 1], [1, 1]))
```

La batería que uno escribe primero para una FFT, con largos que son potencias de dos, no
la ve. Pero $(1 + x)^2$ sale mal: el coeficiente de $x^2$ se sumó al de $x^0$, y la
lista tiene un coeficiente de menos. ¿Cuándo falla, exactamente?

**Teorema.** Sea $d = n_A + n_B - 2 \ge 0$. `multiplicar_mal` falla si y solo si $d$
es una potencia de dos (contando $d = 1$).

*Demostración.* `multiplicar` es correcta para cualquier potencia de dos $N \ge d + 1$,
no solo para la menor: el teorema de la §2 pide $d + 1$ puntos distintos, y las $N$
raíces lo son. La variante elige la menor potencia de dos $N \ge d$. Si $d$ no es
potencia de dos (o $d = 0$, donde $N = 1 = d + 1$), esa potencia cumple $N > d$, es
decir, $N \ge d + 1$, y el resultado es correcto.

Si $d \ge 1$ es potencia de dos, $N = d$, y la respuesta tiene un coeficiente de menos.
El factor más corto tiene a lo sumo $N$ coeficientes. Con $d = 1$ los largos son 1 y
2. Con $d \ge 2$, el más corto tiene $\min(n_A, n_B) \le (n_A + n_B)/2 = d/2 + 1 \le d$.
Ese factor se rellena hasta $N$ y su transformada tiene $N$ valores. El otro puede
tener más, $d + 1$ cuando el corto tiene un solo coeficiente, y entonces no se rellena;
pero `zip` corta el producto punto a punto en el largo menor, $N$. La inversa devuelve
$N = d$ valores, y `c[:m]` no los alarga: la lista tiene $d$ coeficientes y la correcta
$d + 1$. $\square$

En el caso de siempre, con los dos factores rellenados, se ve además qué valor sale.
En las raíces $N$-ésimas, $x^N = 1$, así que $C$ y $C - c_d x^d + c_d$ tienen los
mismos valores. El segundo tiene grado menor que $N$, y es el que devuelve la
interpolación: $c_d$ se suma a $c_0$.

Con largos iguales $L = 2^j$, $d = 2^{j+1} - 2 = 2(2^j - 1)$, que es potencia de dos
solo para $j = 1$. Por eso la batería de arriba nunca podía fallar. Comprobemos la
caracterización contra la ejecución, y contemos qué fracción de pruebas al azar la
atrapa:

```{python continue}
def es_potencia_de_dos(d):
    return d >= 1 and d & (d - 1) == 0

for na in range(1, 20):
    for nb in range(1, 20):
        a = [random.randint(1, 9) for _ in range(na)]
        b = [random.randint(1, 9) for _ in range(nb)]
        assert falla(a, b) == es_potencia_de_dos(na + nb - 2)
print("caracterización comprobada en los 361 pares de largos de 1 a 19")

for L in [10, 100, 1000]:
    malos = sum(es_potencia_de_dos(na + nb - 2)
                for na in range(1, L + 1) for nb in range(1, L + 1))
    print(f"largos al azar en [1, {L}]: falla el {100 * malos / L**2:.2f} % de las pruebas")
```

Una prueba al azar con largos de hasta 1000 lo atrapa una vez cada 500. El teorema de
la §2 lo decía sin correr nada, como en el capítulo 3: la demostración dice dónde
buscar el error, y la batería lo encuentra solo si alguien le apunta a ese sitio.

## 9. La FFT iterativa

Para escribir la FFT sin recursión, miremos en qué orden quedan los coeficientes en
las hojas. El primer nivel separa por
el último bit del índice (par o impar), el segundo por el penúltimo, y así. Para
$n = 8$ las hojas quedan en el orden $a_0, a_4, a_2, a_6, a_1, a_5, a_3, a_7$: la
posición $p$ tiene el $a$ cuyo índice es $p$ con sus 3 bits leídos al revés
($1 = 001 \to 100 = 4$). Es la **permutación por inversión de bits**.

La versión iterativa reordena una vez y recorre el árbol de abajo hacia arriba. En la
etapa de bloques de tamaño $m$, la primera mitad de cada bloque tiene la DFT de los
pares y la segunda la de los impares, y se combinan con la fórmula de la §5. Cada
combinación de dos posiciones es una **mariposa**. El código las registra para
dibujarlas:

```{python continue}
def invertir_bits(n):
    b = n.bit_length() - 1
    return [int(format(p, f"0{b}b")[::-1], 2) if b else 0 for p in range(n)]

def fft_iter(a, signo=1, registro=None):
    n = len(a)
    a = [a[r] for r in invertir_bits(n)]
    m = 2
    while m <= n:
        w = [raiz(m, signo * k) for k in range(m // 2)]     # precalculados
        etapa = []
        for s in range(0, n, m):
            for k in range(m // 2):
                i, j = s + k, s + k + m // 2
                t = w[k] * a[j]
                a[i], a[j] = a[i] + t, a[i] - t
                etapa.append((i, j, k, m))
        if registro is not None:
            registro.append(etapa)
        m *= 2
    return a

for n in [1, 2, 4, 8, 64, 1024]:
    x = [random.uniform(-1, 1) for _ in range(n)]
    assert max(abs(u - v) for u, v in zip(fft_iter(x), fft(x))) < 1e-9
print("fft_iter == fft para n = 1 a 1024")
print("orden de las hojas para n = 8:", invertir_bits(8))
mariposas = []
fft_iter([0] * 8, registro=mariposas)
```

```{python continue echo=false output=asis}
print(F7.mariposa(8, mariposas, invertir_bits(8),
      pie="Las 12 mariposas de la FFT iterativa de 8 puntos, en sus tres etapas, tal "
          "como las ejecutó <code>fft_iter</code>. A la izquierda, los coeficientes en "
          "el orden de inversión de bits. Cada mariposa combina dos posiciones: la de "
          "abajo se multiplica por el factor ω<sub>m</sub><sup>k</sup> escrito a su "
          "lado, se suma a la de arriba para dar la posición de arriba y se resta para "
          "dar la de abajo."))
```

La @fig-fft-mariposa tiene $\log_2 8 = 3$ etapas de $8/2 = 4$ mariposas, y cada
mariposa hace una multiplicación compleja: en general, $(n/2)\log_2 n$. La correctitud
es la de la recursiva vista desde abajo: después de la etapa de bloques de tamaño $m$,
cada bloque contiene la DFT de los coeficientes que la recursión habría juntado en ese
subárbol. Escribir ese invariante con cuidado y demostrarlo es el ejercicio 9. Midamos
qué se gana:

```{python continue}
for n in [2 ** 10, 2 ** 12]:
    x = [random.uniform(-1, 1) for _ in range(n)]
    t1, t2 = mejor_de(3, fft, x), mejor_de(3, fft_iter, x)
    print(f"n = {n}: recursiva {t1:.4f} s, iterativa {t2:.4f} s")
```

En Python la diferencia es chica y no tiene un signo fijo. Las dos hacen las mismas
$(n/2)\log_2 n$ mariposas; la iterativa calcula solo $n - 1$ raíces ($m/2$ por etapa)
en lugar de una llamada a `cmath.exp` por mariposa, y no crea listas intermedias. Que
aun así no gane siempre dice que en Python manda el costo del intérprete por
mariposa.

## 10. Los números de punto flotante

La §1 contó cada operación como exacta. Un `float` tiene 53 bits de mantisa, cada
operación de la FFT redondea, y `multiplicar` confía en que el error acumulado quede
por debajo de $1/2$, para que `round` dé el entero bueno.

¿Cuándo deja de quedar? El experimento multiplica factores de $N/2$ coeficientes al
azar en $[0, 10^k)$, como quien multiplica enteros grandes con "dígitos" en base
$10^k$. El producto exacto sale de los enteros de Python por **sustitución de
Kronecker**: se pegan los coeficientes en un solo entero, con espacio para que no se
mezclen, se multiplican los dos enteros y se recortan los coeficientes.

```{python continue}
def exacto(a, b):
    s = (max(max(a), max(b)) ** 2 * min(len(a), len(b))).bit_length() + 1
    A = B = 0
    for x in reversed(a):
        A = (A << s) | x
    for x in reversed(b):
        B = (B << s) | x
    C, mascara = A * B, (1 << s) - 1
    return [(C >> (s * i)) & mascara for i in range(len(a) + len(b) - 1)]

def con_floats(a, b):
    m = len(a) + len(b) - 1
    N = 1
    while N < m:
        N *= 2
    fa, fb = fft_iter(a + [0] * (N - len(a))), fft_iter(b + [0] * (N - len(b)))
    return [(z / N).real for z in fft_iter([u * v for u, v in zip(fa, fb)], -1)[:m]]

a = [random.randrange(1000) for _ in range(50)]
b = [random.randrange(1000) for _ in range(70)]
assert exacto(a, b) == ingenua(a, b)

errores, rotos = {}, set()
for k in [3, 4, 5, 6]:
    errores[k] = []
    for e in range(4, 15, 2):
        N = 2 ** e
        random.seed(10 * e + k)
        a = [random.randrange(10 ** k) for _ in range(N // 2)]
        b = [random.randrange(10 ** k) for _ in range(N // 2)]
        aprox, bueno = con_floats(a, b), exacto(a, b)
        err = max(abs(x - y) for x, y in zip(aprox, bueno))
        malos = sum(round(x) != y for x, y in zip(aprox, bueno))
        errores[k].append((N, err))
        if malos:
            rotos.add((k, N))
            print(f"base 10^{k}, N = 2^{e}: {malos} coeficientes equivocados; "
                  f"el mayor coeficiente es {max(bueno):.2e}")
print("2^53 =", f"{2 ** 53:.2e}")
print("última corrida: suma de los coeficientes del producto, C(1) =",
      f"{sum(bueno):.2e}")
```

```{python continue echo=false output=asis}
print(F7.error_redondeo(errores, rotos,
      pie="El error máximo de la multiplicación con FFT de punto flotante contra el "
          "producto exacto, para coeficientes al azar en base 10<sup>k</sup>. Cada "
          "punto es una corrida. En rojo, las corridas con algún coeficiente "
          "redondeado al entero equivocado. Por encima de la línea, el redondeo ya "
          "no se puede confiar."))
```

La @fig-fft-error muestra que el error crece con $N$ y con la base. En base $10^3$ y
$10^4$ queda lejos de $1/2$ en todos los tamaños medidos. En base $10^6$, con
$N = 2^{14}$, salieron 2629 coeficientes equivocados. El coeficiente más grande del
producto era $2{,}07 \cdot 10^{15}$, una cuarta parte de $2^{53} \approx 9{,}01 \cdot
10^{15}$: el resultado cabía exacto en un `float`. Lo que no cabe son los valores
intermedios. Con coeficientes no negativos, ningún valor de una transformada pasa de su
valor en $\omega^0 = 1$, por la desigualdad triangular: $|A(\omega^k)| \le A(1)$. Así
que el mayor producto punto a punto es $A(1)B(1) = C(1)$, la suma de todos los
coeficientes del producto. En la última corrida fue $1{,}68 \cdot 10^{19}$, mucho más
que $2^{53}$. Cada operación de la FFT redondea con un error proporcional al tamaño de
los números que toca, y la inversa mezcla los errores de los $N$ valores en cada
coeficiente. Es una explicación del orden de magnitud, no una cota (la da el análisis de
error de la FFT, fuera de este libro): lo que se afirma es lo medido.

La $O(n \log n)$ de la §6 sigue valiendo en el modelo aritmético, pero `multiplicar`
no sirve para todo tamaño: para cada base hay un $N$ desde el cual devuelve basura. Las
salidas son más precisión, que cuesta más por operación, o una aritmética sin
redondeo, que es la de la sección siguiente.

## 11. La NTT: raíces de la unidad módulo un primo

Las demostraciones de las §4 a §6 usaron de $\omega$ cuatro cosas: $\omega^n = 1$,
potencias $\omega^0, \dots, \omega^{n-1}$ distintas, $\omega^{n/2} = -1$, y poder
dividir entre $\omega^k - 1$ (lema de la suma) y entre $n$ (la inversa). Nada de eso es
propio de los complejos. Vale en $\mathbb{Z}_p$, los enteros módulo un primo $p$, que
es un cuerpo; el teorema de la §2 también, porque el del factor vale en cualquier
cuerpo.

**Lema.** Sea $p$ un primo impar y $\omega \in \mathbb{Z}_p$ de orden exactamente $n$,
con $n$ par: $\omega^n = 1$ y $\omega^k \ne 1$ para $0 < k < n$. Entonces
$\omega^{n/2} = -1$, y $\omega^2$ tiene orden exactamente $n/2$.

*Demostración.* $(\omega^{n/2})^2 = 1$, así que $\omega^{n/2}$ es raíz de
$x^2 - 1 = (x - 1)(x + 1)$. En un cuerpo, un producto es cero solo si un factor lo es,
así que $\omega^{n/2} = \pm 1$. No es $1$, porque $0 < n/2 < n$. Y $-1 \ne 1$ porque
$p$ es impar. Para lo segundo, $(\omega^2)^{n/2} = \omega^n = 1$, y si
$(\omega^2)^k = 1$ con $0 < k < n/2$, entonces $\omega^{2k} = 1$ con $0 < 2k < n$, en
contra del orden de $\omega$. $\square$

Eso da el lema de la mitad; además $\omega^k - 1 \ne 0$ es invertible si $n \nmid k$,
y $n$ lo es si $n < p$. La FFT sobre $\mathbb{Z}_p$ es la **transformada numérica**
(NTT). Pollard la estudió en "The fast Fourier transform in a finite field"
(*Mathematics of Computation*, 1971).

¿Existe un $\omega$ de orden $n$? Un teorema de Álgebra, que no demostramos, dice que
hay una **raíz primitiva** $g$, cuyas potencias recorren los $p - 1$ elementos no
nulos. Si $n \mid p - 1$, $\omega = g^{(p-1)/n}$ tiene orden exactamente $n$. Con
$p = 17$, $p - 1 = 2^4$ y hay NTT de tamaño hasta 16. Para encontrar $g$ basta probar
candidatos: $g$ es primitiva si $g^{(p-1)/q} \ne 1$ para cada primo $q$ que divide a
$p - 1$.

```{python continue}
def factores_primos(n):
    f, q = [], 2
    while q * q <= n:
        if n % q == 0:
            f.append(q)
            while n % q == 0:
                n //= q
        q += 1
    return f + [n] if n > 1 else f

def raiz_primitiva(p):
    g = 2
    while any(pow(g, (p - 1) // q, p) == 1 for q in factores_primos(p - 1)):
        g += 1
    return g

def ntt(a, w, p):
    n = len(a)
    if n == 1:
        return a[:]
    pares, impares = ntt(a[0::2], w * w % p, p), ntt(a[1::2], w * w % p, p)
    y, x = [0] * n, 1                      # x recorre w^k
    for k in range(n // 2):
        t = x * impares[k] % p
        y[k], y[k + n // 2] = (pares[k] + t) % p, (pares[k] - t) % p
        x = x * w % p
    return y

g = raiz_primitiva(17)
w4 = pow(g, 16 // 4, 17)
print("p = 17: g =", g, " ω de orden 4 =", w4, " potencias:", [pow(w4, k, 17) for k in range(4)])
print("NTT de (1, 2, 3, 4) en Z_17:", ntt([1, 2, 3, 4], w4, 17))
```

En $\mathbb{Z}_{17}$ el papel de $i$ lo hace $13$: $13^2 = 169 = 16 = -1$. La NTT de
$(1, 2, 3, 4)$ son los valores de $1 + 2x + 3x^2 + 4x^3$ en $1, 13, 16, 4$, módulo 17.
Compruébalo para $x = 16 = -1$: $1 - 2 + 3 - 4 = -2 = 15$.

Para tamaños grandes hace falta un primo con $p - 1$ divisible por una potencia de
dos grande, como $998244353$:

```{python continue}
P = 998244353
print("primos que dividen a P - 1:", factores_primos(P - 1))
print("P - 1 = 119 · 2^23:", P - 1 == 119 * 2 ** 23)
print("raíz primitiva:", raiz_primitiva(P))

def multiplicar_ntt(a, b, p=P):
    m = len(a) + len(b) - 1
    N = 1
    while N < m:
        N *= 2
    assert (p - 1) % N == 0, "no hay raíz de orden N"
    w = pow(raiz_primitiva(p), (p - 1) // N, p)
    fa, fb = ntt(a + [0] * (N - len(a)), w, p), ntt(b + [0] * (N - len(b)), w, p)
    c = ntt([u * v % p for u, v in zip(fa, fb)], pow(w, p - 2, p), p)   # ω^(-1)
    n_inv = pow(N, p - 2, p)                                            # 1/N
    return [x * n_inv % p for x in c[:m]]

for _ in range(200):
    a = [random.randrange(1000) for _ in range(random.randint(1, 50))]
    b = [random.randrange(1000) for _ in range(random.randint(1, 50))]
    assert multiplicar_ntt(a, b) == ingenua(a, b)
print("multiplicar_ntt == ingenua en 200 pares al azar")
```

Los inversos salen del pequeño teorema de Fermat: $x^{p-2} = x^{-1}$ en
$\mathbb{Z}_p$. La NTT calcula cada $c_k$ **módulo $p$**, sin error, y si
$0 \le c_k < p$ el resto es el número. Con coeficientes en $[0, B)$ y factores de $n$
coeficientes, $c_k < n B^2$, así que basta $n B^2 \le p$.

## 12. Aplicaciones: enteros grandes y sumas de pares

**Enteros grandes.** Con los dígitos de las unidades primero, como en el capítulo 6,
el producto es la convolución de los dígitos más los acarreos, que cuestan $O(n)$:

```{python continue}
def multiplicar_enteros(x, y):
    a = [int(c) for c in reversed(str(x))]
    b = [int(c) for c in reversed(str(y))]
    assert 81 * min(len(a), len(b)) < P            # cada c_k cabe en Z_P
    c, r, acarreo = multiplicar_ntt(a, b), [], 0
    for v in c:
        acarreo, digito = divmod(v + acarreo, 10)
        r.append(digito)
    while acarreo:
        acarreo, digito = divmod(acarreo, 10)
        r.append(digito)
    return int("".join(map(str, reversed(r))))

for _ in range(20):
    x, y = random.randrange(10 ** 1500), random.randrange(10 ** 1500)
    assert multiplicar_enteros(x, y) == x * y
print("multiplicar_enteros == * de Python en 20 pares de 1500 dígitos")
```

¿Cuánto cuesta eso en el modelo por bit del capítulo 1? La versión del capítulo tiene
un tamaño máximo: los $c_k$ tienen que caber en $\mathbb{Z}_P$ y $N$ no puede pasar de
$2^{23}$. Sin tope, el primo o la precisión tienen que crecer con $b$, y la operación
sobre coeficientes deja de costar 1. Por eso el capítulo 1 (§9) no pone la multiplicación con
la transformada de Fourier en $O(b \log b)$. Schönhage y Strassen ("Schnelle
Multiplikation großer Zahlen", *Computing*, 1971) llegaron a $O(b \log b \log \log b)$
operaciones de bits, con una transformada sobre un anillo de enteros módulo
$2^K + 1$. Harvey y van der Hoeven ("Integer multiplication in time $O(n \log n)$",
*Annals of Mathematics*, 2021) llegaron a $O(b \log b)$. No las demostramos.

**Sumas de pares.** Dados dos conjuntos $A, B \subseteq \{0, 1, \dots, n\}$, queremos
saber, para cada $c$, cuántas parejas $(a, b) \in A \times B$ cumplen $a + b = c$. La
fuerza bruta mira hasta $(n+1)^2$ parejas. A cada conjunto le corresponde un polinomio
con un $1$ en cada exponente del conjunto, $P_A(x) = \sum_{a \in A} x^a$. Entonces
$$P_A(x) \, P_B(x) = \sum_{a \in A} \sum_{b \in B} x^{a + b},$$ y el coeficiente de
$x^c$ es exactamente el número de parejas con $a + b = c$. La multiplicación de
exponentes se volvió una suma:

```{python continue}
def sumas_de_pares(A, B):
    n = max(max(A), max(B))
    pa = [1 if v in A else 0 for v in range(n + 1)]
    pb = [1 if v in B else 0 for v in range(n + 1)]
    return {c: k for c, k in enumerate(multiplicar_ntt(pa, pb)) if k}

print(sumas_de_pares({1, 3, 4}, {0, 2, 5}))
```

El $3$ y el $6$ salen dos veces cada uno: $3 = 1 + 2 = 3 + 0$ y $6 = 1 + 5 = 4 + 2$. El
costo es $O(n \log n)$ aunque haya $\Theta(n^2)$ parejas: nunca se miran una por una.

## 13. La regla {#fft-13-la-regla}

La regla del capítulo es esta: **si una operación es cara en una representación,
busca otra donde sea barata y paga el cambio con un algoritmo rápido**. Con puntos
cualesquiera el cambio costaba $n^2$; con raíces de la unidad, $n \log n$, porque hay
parejas en cada nivel.

La segunda mitad es la del capítulo 5: un costo viene con su modelo pegado. El
$O(n \log n)$ es en operaciones sobre coeficientes; la §10 midió dónde dejan de
alcanzar 53 bits, y para enteros medidos en bits el resultado es otro teorema.

Hacia adelante, el teorema de la §2 vuelve en el capítulo 15. Dos polinomios distintos
de grado a lo sumo $d$ coinciden en a lo sumo $d$ puntos, así que para comprobar
$C = AB$ basta evaluar en un punto al azar de $\mathbb{Z}_p$, con error a lo sumo
$d/p$. El capítulo 15 lo hace con matrices (Freivalds). Y las sumas de
pares reaparecen en el capítulo 24, con el problema 3SUM.

## Resumen {#fft-resumen}

- Un polinomio de grado $d$ queda determinado por $d + 1$ valores. En valores,
  multiplicar cuesta una operación por punto, pero el producto pide
  $\deg A + \deg B + 1$ puntos.
- $A(x) = A_{\text{par}}(x^2) + x A_{\text{impar}}(x^2)$ evalúa en $x$ y en $-x$ con el
  mismo trabajo. Las raíces de la unidad son los puntos donde eso se repite en cada
  nivel (lema de la mitad).
- La FFT evalúa en las $n$ raíces en $\Theta(n \log n)$, con la recurrencia de
  mergesort. La inversa es la misma FFT con $\omega^{-1}$, dividida entre $n$ (lema de
  la suma).
- Multiplicar polinomios cuesta $\Theta(n \log n)$ operaciones sobre coeficientes.
- Rellenar hasta $N \ge d$ en vez de $N \ge d + 1$ falla solo cuando $d$ es potencia
  de dos, y ninguna batería con largos iguales potencia de dos (desde 4) lo ve.
- La FFT iterativa reordena por inversión de bits y hace $(n/2) \log_2 n$ mariposas.
- Con `float`, el error crece con los valores intermedios y llega a redondear al
  entero equivocado. La NTT trabaja
  en $\mathbb{Z}_p$ sin error, mientras los coeficientes sean menores que $p$.
- Para enteros en el modelo por bit: $O(b \log b \log \log b)$ (Schönhage y Strassen)
  y $O(b \log b)$ (Harvey y van der Hoeven).

## Ejercicios {#fft-ejercicios}

1. Calcula a mano la DFT de $(1, 2, 3, 4)$ con la recursión de la §5, escribiendo las
   DFT de los pares y de los impares antes de combinarlas.
2. Demuestra que la `fft` de la §5 hace exactamente $(n/2)\log_2 n$ multiplicaciones
   por potencias de $\omega_n$ para $n$ potencia de dos. Escribe la recurrencia exacta,
   sin $O$, y resuélvela.
3. Demuestra que aplicar la DFT dos veces a $(a_0, a_1, \dots, a_{n-1})$ da
   $n \cdot (a_0, a_{n-1}, a_{n-2}, \dots, a_1)$. Usa el resultado para decir qué
   devuelve `multiplicar` si la tercera FFT usa `signo=1` en lugar de `signo=-1`, y
   para qué productos ese error pasaría inadvertido.
4. Comprueba que $998244353 = 119 \cdot 2^{23} + 1$ admite una NTT de tamaño $2^{23}$
   y no de tamaño $2^{24}$. Halla una raíz de orden 8 en $\mathbb{Z}_{998244353}$ y
   comprueba que su orden es exactamente 8, no un divisor de 8.
5. Multiplica enteros de un millón de dígitos con la FFT de punto flotante (puedes usar
   `numpy.fft`), agrupando los dígitos en base $10^k$. Mide, para $k = 1, 2, \dots$,
   el error máximo antes de redondear y el primer $k$ con el que el producto sale
   equivocado. (Desde Python 3.11, pasar de `str` a `int` con más de 4300 dígitos pide
   `sys.set_int_max_str_digits(0)`.)
6. En la figura de la §10, la base $10^6$ redondea mal recién con $N = 2^{14}$.
   Construye entradas en base $10^6$ para las que `con_floats` redondea algún
   coeficiente al entero equivocado con un $N$ menor. Explica por qué tus entradas son
   peores que las de la figura.
7. Supón que $n = 3^k$ en lugar de una potencia de dos. Parte $A$ en tres polinomios
   según el resto del índice módulo 3. Enuncia y demuestra el lema que reemplaza al de
   la mitad, escribe la fórmula de combinación y la recurrencia, y di cuántas
   multiplicaciones hace por nivel.
8. Un texto $t$ y un patrón $p$ son listas de enteros positivos, y el $0$ es un comodín
   que coincide con cualquier cosa, en los dos. Encuentra todas las posiciones $i$ donde
   $p$ aparece en $t$ con $O(|t| \log |t|)$ operaciones aritméticas, usando tres
   convoluciones. (Pista: busca una suma de términos no negativos que valga 0 justo
   cuando hay coincidencia en la posición $i$.)
9. Enuncia el invariante de `fft_iter`: qué contiene cada bloque de tamaño $m$ después
   de la etapa de bloques de tamaño $m$. Demuéstralo por inducción en las etapas, usando
   la fórmula de combinación de la §5 y la permutación por inversión de bits.
10. ★ Dados $r_1, \dots, r_n$, calcula los coeficientes de
    $(x - r_1)(x - r_2) \cdots (x - r_n)$ con $O(n \log^2 n)$ operaciones aritméticas.
    Escribe la recurrencia y resuélvela con el árbol de recursión del capítulo 6.
    ¿Por qué no sale $O(n \log n)$?
