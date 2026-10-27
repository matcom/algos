# Ejercicio 10 — Par más cercano en una dimensión

> **Enunciado.** Par más cercano en una dimensión. Demuestra $\Omega(n\log n)$ en
> árboles de decisión algebraicos por reducción desde *distinción de elementos*.
> Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo
> a una dimensión.

---

## 1. El problema y su modelo

**Par más cercano en 1D.** Dados $n$ reales $P=\{x_1,\dots,x_n\}$, devolver
$\displaystyle \delta^\* = \min_{i\neq j} |x_i - x_j|$ (y, si se quiere, el par que lo
realiza).

**Modelo de la cota mínima:** el **árbol de decisión algebraico** (C2, §8). Cada nodo
interno evalúa el signo de un polinomio de grado acotado sobre las coordenadas de la
entrada y ramifica en $\{<0,\ =0,\ >0\}$; cada hoja da una respuesta. El costo es la
**profundidad** del árbol, es decir el número de pruebas en el peor caso. Este modelo
capta exactamente comparar, sumar, restar, multiplicar y comparar distancias —todo lo
que necesita un algoritmo "aritmético" para este problema— y es el modelo en el que se
prueba la cota $\Omega(n\log n)$ del par más cercano en el plano.

---

## 2. Algoritmo sencillo y su costo

El par más cercano en 1D es **consecutivo tras ordenar** (C2, §3, Lema de la sección 3):
si $x_{(1)}\le\dots\le x_{(n)}$ es el orden, el mínimo se alcanza entre algún par
$x_{(k)}, x_{(k+1)}$. Demostración: si $(x_i,x_j)$ con, digamos, $x_i<x_j$ y entre
medias hay un $x_k$, entonces $|x_i-x_k|<|x_i-x_j|$, contradiciendo que $(i,j)$ sea el
más cercano. Así que basta ordenar y mirar los $n-1$ gaps:

```python
def par_mas_cercano_1d(P):
    xs = sorted(P)                       # O(n log n)
    mejor = float("inf")
    par = None
    for a, b in zip(xs, xs[1:]):         # O(n): solo gaps consecutivos
        if b - a < mejor:
            mejor, par = b - a, (a, b)
    return mejor, par

if __name__ == "__main__":
    print(par_mas_cercano_1d([0.5, 2.1, 3.4, 5.0, 5.0, 7.2, 8.6]))
```

```
(0.0, (5.0, 5.0))
```

Costo $O(n\log n)$, dominado por el orden. La pregunta de la quinta columna del ciclo
(C2, §1) es: **¿se puede mejor?** En el modelo algebraico, no.

---

## 3. La cota mínima: $\Omega(n\log n)$ por reducción

### El problema del que reducimos

**Distinción de elementos (element distinctness).** Dados $n$ reales, decidir si hay
dos iguales.

**Teorema (Ben-Or, 1983; C2, §8).** Distinción de elementos requiere $\Omega(n\log n)$
en árboles de decisión algebraicos. *(Se cita, no se demuestra: la prueba acota por
$n!$ el número de componentes conexas del conjunto de entradas con respuesta "todos
distintos", vía Milnor–Thom, y un árbol de profundidad $h$ separa a lo sumo $c^h$
componentes, luego $h=\Omega(\log n!)=\Omega(n\log n)$.)*

### La reducción (idéntica en forma a la del plano, C2, §8)

Dada una instancia $x_1,\dots,x_n$ de distinción de elementos, construimos la instancia
de par más cercano
$$P = \{x_1,\ x_2,\ \dots,\ x_n\}$$
**sin tocar nada**: en 1D los reales ya *son* los puntos. La construcción cuesta $O(n)$
y no evalúa ninguna prueba de signo. Entonces

$$\delta^\*(P) = \min_{i\ne j}|x_i - x_j| = 0
\quad\Longleftrightarrow\quad
\exists\, i\ne j:\ x_i = x_j.$$

```
distinción de elementos          par más cercano 1D
x:  0.5  2.1  3.4  5.0  5.0  ──► eje:  ·  ·   ·   ‖   ·        δ*=0  ⇒ hay repetido
                       └┬┘                       └ dos puntos a distancia 0
    x:  0.5  2.1  3.4  5.0  7.2 ──► eje: ·  ·   ·   ·   ·       δ*>0  ⇒ todos distintos
```

> En el plano la reducción incrusta $x_i\mapsto(x_i,0)$; en 1D ni eso hace falta, lo
> que vuelve la reducción todavía más barata.

**Teorema.** Par más cercano en 1D requiere $\Omega(n\log n)$ en árboles de decisión
algebraicos.

*Demostración.* Supongamos que existe un árbol de decisión algebraico $\mathcal A$ para
par más cercano 1D de profundidad $T(n)=o(n\log n)$. Componemos: dada una entrada de
distinción de elementos, aplicamos la construcción ($O(n)$, cero pruebas), corremos
$\mathcal A$ y añadimos **una** prueba de signo final, "¿$\delta^\* = 0$?". El resultado
es un árbol de decisión algebraico para distinción de elementos de profundidad
$T(n)+1 = o(n\log n)$, contra Ben-Or. $\square$

**La reducción se lee en dos direcciones** (C2, §8): "un algoritmo bueno para $B$ da uno
bueno para $A$" (diseño) y "una cota mínima para $A$ da una cota mínima para $B$". Aquí
la usamos en la segunda dirección: $A=$ distinción de elementos es difícil, $A$ se
reduce a $B=$ par más cercano, luego $B$ es difícil.

Conclusión: el algoritmo de ordenar-y-mirar-gaps es **óptimo en el modelo algebraico**.

---

## 4. Romper la cota: el algoritmo aleatorio de la conferencia 2

La cota $\Omega(n\log n)$ es una afirmación **sobre un modelo**. El algoritmo
incremental aleatorio de Rabin (1976), en la versión de Kleinberg–Tardos §13.7 (C2, §9),
corre en **tiempo esperado $O(n)$** porque usa dos cosas que el árbol de decisión
algebraico **no tiene**:

1. **La parte entera** $\lfloor\cdot\rfloor$ (para asignar cada punto a una celda de una
   rejilla). En el modelo algebraico solo hay signos de polinomios: no hay piso.
2. **Una tabla hash** con acceso esperado $O(1)$ (acceso indexado por el valor, no por
   comparación).

El modelo en el que vive el algoritmo rápido es la **word-RAM con parte entera y
hashing**, no el árbol algebraico. No hay contradicción: cada cota viene con su modelo
(C2, §8 y la moraleja del Tema 1, "toda cota viene con un modelo").

### Adaptación a una dimensión

El algoritmo del plano (C2, §9) usa una rejilla de celdas de lado $\delta/2$ y consulta
el bloque $5\times5$ alrededor del punto nuevo. En 1D la rejilla es una recta de
**intervalos** de longitud $\delta/2$, y el bloque que hay que consultar es una ventana
de **5 celdas** (de $-2$ a $+2$), no $25$:

**Invariante.** Cada celda (intervalo de longitud $\delta/2$) contiene a lo sumo un
punto. *(Dos puntos en la misma celda distarían $\le \delta/2 < \delta$, imposible con
$\delta$ = mínimo actual.)*

**Inserción de $p_{i+1}$.** Cualquier punto a distancia $<\delta$ cae en una celda que
difiere en $<2$ índices, luego está en la ventana de 5 celdas centrada en la de
$p_{i+1}$. Consultamos esas 5 celdas (a lo sumo un punto cada una): $O(1)$ accesos al
hash.
- Si ninguno está a $<\delta$: $\delta$ no cambia, insertamos $p_{i+1}$, costo $O(1)$.
- Si lo hay: $\delta$ baja a $\delta'$, reconstruimos la rejilla con lado $\delta'/2$,
  costo $O(i)$.

```python
import random

def par_mas_cercano_1d_aleatorio(P, semilla=0):
    pts = list(P)
    random.Random(semilla).shuffle(pts)        # permutación uniforme
    d = abs(pts[0] - pts[1])
    if d == 0:
        return 0.0
    lado = d / 2
    celda = lambda x: int(x // lado)
    g = {celda(q): q for q in pts[:2]}
    for i in range(2, len(pts)):
        q = pts[i]
        c = celda(q)
        antes = d
        for dc in (-2, -1, 0, 1, 2):           # ventana de 5 celdas (1D), no 25
            v = g.get(c + dc)
            if v is not None:
                d = min(d, abs(q - v))
        if d < antes:                          # bajó delta: reconstruir
            lado = d / 2
            celda = lambda x, l=lado: int(x // l)
            g = {celda(x): x for x in pts[:i + 1]}
        else:
            g[c] = q
    return d

if __name__ == "__main__":
    import random as _r
    _rng = _r.Random(2026)
    pts = [_rng.random() * 1000 for _ in range(100000)]
    exacto = par_mas_cercano_1d(pts)[0]
    aprox = par_mas_cercano_1d_aleatorio(pts, semilla=7)
    print(f"ordenar+gaps: {exacto:.10f}")
    print(f"aleatorio   : {aprox:.10f}")
    print(f"coinciden   : {abs(exacto - aprox) < 1e-12}")
```

```
ordenar+gaps: 0.0000000436
aleatorio   : 0.0000000436
coinciden   : True
```

### Por qué es lineal (análisis hacia atrás, C2, §9)

Fijado el conjunto $S=\{p_1,\dots,p_{i+1}\}$ y olvidado el orden, el paso $i+1$
reconstruye **sii** $p_{i+1}$ es uno de los (a lo sumo dos) puntos que realizan el par
más cercano de $S$. Como el orden es una permutación uniforme,
$$\Pr[\text{reconstruir en el paso } i+1] \le \frac{2}{i+1}.$$
El costo esperado de las reconstrucciones es
$$\sum_{i} O(i)\cdot\frac{2}{i+1} = \sum_i O(1) = O(n),$$
y el resto del trabajo es $O(1)$ por paso. Total **esperado $O(n)$**.

| aspecto | ordenar + gaps | incremental aleatorio |
|---|---|---|
| modelo | árbol de decisión algebraico | word-RAM con $\lfloor\cdot\rfloor$ y hash |
| costo | $\Theta(n\log n)$ peor caso | $O(n)$ **esperado** |
| ventana consultada | — | 5 celdas (en el plano: 25) |
| ¿contradice la cota? | no | no: otro modelo |

---

## 5. Resumen

- **Cota:** $\Omega(n\log n)$ en árboles de decisión algebraicos, por reducción
  $O(n)$ y de cero pruebas desde distinción de elementos (Ben-Or). El par más cercano
  hereda la dureza de distinción de elementos leyendo la reducción en la dirección
  "cota de $A$ ⇒ cota de $B$".
- **Rompiéndola:** el algoritmo incremental aleatorio de la C2 §9, adaptado a 1D
  (rejilla de intervalos, ventana de 5 celdas), corre en **esperado $O(n)$** en la
  word-RAM con parte entera y hashing. No hay contradicción: *toda cota viene con su
  modelo*, y el modelo rápido tiene operaciones que el algebraico prohíbe.
