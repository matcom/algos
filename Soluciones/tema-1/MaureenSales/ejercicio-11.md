# Ejercicio 11 — ¿Es polinomial la mochila en $O(nW)$?

**Tema 1 · Diseño y Análisis de Algoritmos · MatCom 2026**
Conferencias que usa: **C1** (tamaño de la entrada en bits) · Dificultad: ★★

---

## Enunciado

> La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división?

---

## 1. El problema y el algoritmo

**Mochila 0/1.** Hay $n$ objetos con pesos $w_1, \dots, w_n$ y valores $v_1, \dots, v_n$ (enteros positivos), y una capacidad $W$. Elegir $S \subseteq \{1..n\}$ con $\sum_{i \in S} w_i \le W$ que maximice $\sum_{i\in S} v_i$.

La programación dinámica de Estructuras de Datos: $M[i][c]$ = mejor valor usando los primeros $i$ objetos con capacidad $c$,

$$
M[i][c] = \max\big( M[i-1][c],\; v_i + M[i-1][c - w_i] \ (\text{si } w_i \le c) \big), \qquad M[0][c] = 0 .
$$

```python
def mochila_dp(pesos, valores, W, contador=None):
    """Programación dinámica O(nW), con una sola fila (se recorre c hacia atrás)."""
    M = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            M[c] = max(M[c], v + M[c - w])
        if contador is not None:
            contador[0] += W + 1            # celdas tocadas en esta fila
    return M[W]
```

Hace $n(W+1)$ actualizaciones de celdas: $\Theta(nW)$ operaciones y $\Theta(W)$ memoria.

## 2. El tamaño de la entrada en bits

Siguiendo C1, escribir un entero $x \ge 1$ en binario ocupa $\lfloor \log_2 x \rfloor + 1$ bits, y el tamaño de una instancia es la cantidad de bits que hacen falta para escribirla:

$$
L \;=\; \sum_{i=1}^{n} \big(\lfloor\log_2 w_i\rfloor + 1 + \lfloor\log_2 v_i\rfloor + 1\big) + \lfloor \log_2 W \rfloor + 1 \;=\; \Theta\Big(n + \sum_i \log w_i + \sum_i \log v_i + \log W\Big).
$$

Lo importante: **$W$ aporta solo $\lfloor \log_2 W \rfloor + 1$ bits**, pero el algoritmo hace $\Theta(W)$ trabajo por objeto.

## 3. No es polinomial

> **Afirmación.** No existe un polinomio $p$ tal que la programación dinámica haga $\le p(L)$ operaciones en toda instancia.

Para probarlo hay que encontrar instancias en las que el trabajo crezca exponencialmente respecto de $L$. Lo hago de dos maneras: primero con una familia mínima de instancias, y después con una técnica que sirve para **cualquier** instancia.

### 3.1 Una familia mínima

Tomo un solo objeto con peso 1 y valor 1, y una capacidad $W = 2^b - 1$, que en binario son $b$ unos: $11\cdots1$.

- **Tamaño de la entrada.** El peso y el valor ocupan 1 bit cada uno y $W$ ocupa $b$ bits, así que $L = b + 2$.
- **Trabajo de la DP.** Llena $n(W+1) = 2^b = 2^{L-2}$ celdas.

| $b$ | $W$ | $L$ (bits) | celdas de la DP |
|---:|---:|---:|---:|
| 8 | 255 | 10 | 256 |
| 16 | 65 535 | 18 | 65 536 |
| 32 | $\approx 4.3\cdot 10^9$ | 34 | $\approx 4.3\cdot 10^9$ |
| 64 | $\approx 1.8\cdot 10^{19}$ | 66 | $\approx 1.8\cdot 10^{19}$ |

Cada bit que se agrega a $W$ duplica las celdas. La función $2^{L-2}$ no está acotada por ningún polinomio en $L$. ∎

La demostración es correcta, pero la instancia es artificial: un solo objeto y una mochila enorme. Queda la sospecha de que la DP solo sufre en casos raros. La técnica del escalado muestra que no es así.

### 3.2 La técnica del escalado: cambiar de unidades

**La idea.** Si pesas los objetos en gramos en vez de kilos, el problema es el mismo, pero la tabla de la DP tiene 1000 veces más columnas. Multiplicar por $2^k$ es lo mismo, con un factor que se lleva bien con el binario.

Se toma una instancia cualquiera y se multiplican **los pesos y la capacidad** por $2^k$. Los valores no se tocan:

$$
w_i' = 2^k\, w_i, \qquad W' = 2^k\, W, \qquad v_i' = v_i .
$$

El análisis tiene cuatro pasos.

**Paso 1: la respuesta no cambia.** Para cualquier subconjunto $S$ de objetos,

$$
\sum_{i\in S} 2^k w_i \;\le\; 2^k W \quad\iff\quad \sum_{i\in S} w_i \;\le\; W
$$

(basta dividir entre $2^k > 0$). Los subconjuntos que caben en la mochila son exactamente los mismos, y sus valores no cambiaron, así que el óptimo es el mismo. Es el mismo problema escrito en otra unidad.

**Paso 2: la entrada crece poco, $k$ bits por número.** En binario, multiplicar por $2^k$ es agregar $k$ ceros a la derecha, igual que multiplicar por $10^k$ en decimal:

```
  5        =    101
  5 · 2^3  = 101000      (= 40)
```

Por eso se usa $2^k$ y no 1000: la cuenta de bits es exacta, porque cada número escalado tiene exactamente $k$ bits más. Se escalan $n + 1$ números ($n$ pesos y $W$), así que

$$
L' = L + (n+1)\,k .
$$

La entrada crece en forma **lineal** en $k$.

**Paso 3: el trabajo crece mucho, se multiplica por $2^k$.** La DP llena

$$
n\,(W' + 1) \;=\; n\,(2^k W + 1) \;\approx\; 2^k \cdot nW \ \text{ celdas.}
$$

El trabajo crece en forma **exponencial** en $k$.

**Paso 4: juntar las dos cosas.** Si se despeja $k = (L' - L)/(n+1)$ del paso 2 y se sustituye en el paso 3, queda

$$
\text{celdas} \;\approx\; nW \cdot 2^{(L' - L)/(n+1)} .
$$

Con la instancia fija, cada $n + 1$ bits que se agregan a la entrada **duplican** el trabajo. Un algoritmo polinomial no puede hacer eso. Si el trabajo fuera $\le c\, L'^{\,d}$, como $L'$ es lineal en $k$, el trabajo estaría acotado por un polinomio en $k$, y $2^k$ le gana a cualquier polinomio.

**Ejemplo.** Pesos $[3, 4, 5]$, valores $[4, 5, 6]$ y $W = 7$. El óptimo es 9 (llevar los objetos de peso 3 y 4). En la tabla, $0^{k}$ abrevia $k$ ceros.

| $k$ | pesos $\cdot\, 2^k$ (binario) | $W \cdot 2^k$ (binario) | $L$ (bits) | celdas de la DP | óptimo |
|---:|---|---|---:|---:|---:|
| 0 | `11`  `100`  `101` | `111` | 20 | 24 | 9 |
| 1 | `110`  `1000`  `1010` | `1110` | 24 | 45 | 9 |
| 2 | `1100`  `10000`  `10100` | `11100` | 28 | 87 | 9 |
| 3 | `11000`  `100000`  `101000` | `111000` | 32 | 171 | 9 |
| 10 | `11`$0^{10}$  `100`$0^{10}$  `101`$0^{10}$ | `111`$0^{10}$ | 60 | 21 507 | 9 |
| 20 | `11`$0^{20}$  `100`$0^{20}$  `101`$0^{20}$ | `111`$0^{20}$ | 100 | 22 020 099 | 9 |

Cada fila agrega un cero a cada uno de los $n + 1 = 4$ números escalados, o sea 4 bits, y casi duplica las celdas. De $k = 0$ a $k = 20$ la entrada pasa de 20 a 100 bits (×5) y el trabajo pasa de 24 a 22 millones de celdas (≈ ×$10^6$). El óptimo nunca cambia.

**Qué enseña.** La DP no paga por la dificultad del problema sino por la **unidad de medida**. Sus columnas recorren todas las capacidades $0, 1, \dots, W$, y esa cantidad es el **valor** de $W$, no su largo. El experimento 2 de la sección 5 usa esta técnica con una instancia de 6 objetos: ahí cada $k$ suma $n + 1 = 7$ bits (de $k=0$ a $k=2$ la entrada pasa de 47 a 61 bits) y las celdas se multiplican por casi 4 cada dos pasos. La fuerza bruta no mira los valores de los pesos, solo cuántos objetos hay, así que no cambia.

### 3.3 ¿Por qué entonces "funciona" en la práctica?

Porque en muchos usos $W$ es chico (una mochila de 1000 kg con pesos enteros en kg). Si $W \le q(n)$ para un polinomio $q$, la DP sí es polinomial: $O(n\cdot q(n))$. El nombre técnico es **pseudopolinomial**.

## 4. El parecido con la primalidad por división

| | primalidad por división | mochila por DP |
|---|---|---|
| entrada | un número $N$ | $n$ objetos y una capacidad $W$ |
| tamaño en bits | $b = \lfloor \log_2 N\rfloor + 1$ | $L \ge \lfloor \log_2 W \rfloor + 1$ |
| trabajo | $\sqrt N = 2^{b/2}$ divisiones | $n \cdot W$, con $W$ hasta $2^{L}$ |
| polinomial en el **valor** | sí ($\sqrt{N}$) | sí ($nW$) |
| polinomial en los **bits** | no | no |
| parece polinomial porque | "es un solo ciclo" | "es una tabla de dos dimensiones" |

En los dos casos el error es el mismo, y es el que C1 llamaba **llamar polinomial a algo exponencial en bits**: confundir el valor de un número con el espacio que ocupa. Un ciclo `for d in range(2, isqrt(N)+1)` y un ciclo `for c in range(W, ...)` tienen la misma enfermedad: el límite del ciclo es un **número de la entrada**, no la cantidad de datos.

---

## 5. Casos de prueba

1. La DP contra fuerza bruta sobre los $2^n$ subconjuntos.
2. El experimento del escalado: multiplico pesos y capacidad por $2^k$, mido los bits de la entrada y las celdas que toca la DP. La fuerza bruta, en cambio, no se entera del escalado.
3. El mismo experimento con la primalidad por división: bits contra divisiones.

```python
import itertools, random, math

def mochila_bruta(pesos, valores, W, contador=None):
    n, mejor = len(pesos), 0
    for S in itertools.product([0, 1], repeat=n):
        if contador is not None: contador[0] += 1
        if sum(p for p, s in zip(pesos, S) if s) <= W:
            mejor = max(mejor, sum(v for v, s in zip(valores, S) if s))
    return mejor

def bits(x):
    return max(1, x.bit_length())

def bits_instancia(pesos, valores, W):
    return sum(bits(p) for p in pesos) + sum(bits(v) for v in valores) + bits(W)

random.seed(11)
# 1) correctitud
for _ in range(400):
    n = random.randint(0, 10)
    pesos = [random.randint(1, 20) for _ in range(n)]
    valores = [random.randint(1, 30) for _ in range(n)]
    W = random.randint(0, 60)
    assert mochila_dp(pesos, valores, W) == mochila_bruta(pesos, valores, W)
print("DP == fuerza bruta en 400 instancias aleatorias")

# 2) escalado por 2^k
pesos, valores, W = [3, 4, 5, 9, 11, 13], [4, 5, 7, 12, 14, 17], 23
base = mochila_dp(pesos, valores, W)
print(f"\ninstancia: pesos={pesos} valores={valores} W={W} -> óptimo {base}")
print(f"{'k':>3} {'bits de la entrada':>19} {'celdas DP':>14} {'subconjuntos (bruta)':>21}")
for k in [0, 2, 4, 6, 8, 10, 12, 14, 16]:
    P = [p << k for p in pesos]; Wk = W << k
    c_dp, c_br = [0], [0]
    r1 = mochila_dp(P, valores, Wk, c_dp)
    r2 = mochila_bruta(P, valores, Wk, c_br)
    assert r1 == r2 == base                      # la respuesta no cambia
    print(f"{k:3} {bits_instancia(P, valores, Wk):19} {c_dp[0]:14,} {c_br[0]:21,}")

# 3) primalidad por división, medida en bits
def primo_division(N, contador):
    if N < 2: return False
    d = 2
    while d * d <= N:
        contador[0] += 1
        if N % d == 0: return False
        d += 1
    return True

def anterior_primo(x):
    while not primo_division(x, [0]):
        x -= 1
    return x

print(f"\n{'bits de N':>10} {'divisiones (N primo)':>21} {'2^(b/2)':>10}")
for b in [8, 12, 16, 20, 24, 28, 32, 36]:
    N = anterior_primo(2 ** b - 1)               # el mayor primo de b bits: N ≈ 2^b
    c = [0]
    assert primo_division(N, c)
    print(f"{N.bit_length():10} {c[0]:21,} {2 ** (b // 2):10,}")
```

### Salida

```text
DP == fuerza bruta en 400 instancias aleatorias

instancia: pesos=[3, 4, 5, 9, 11, 13] valores=[4, 5, 7, 12, 14, 17] W=23 -> óptimo 30
  k  bits de la entrada      celdas DP  subconjuntos (bruta)
  0                  47            144                    64
  2                  61            558                    64
  4                  75          2,214                    64
  6                  89          8,838                    64
  8                 103         35,334                    64
 10                 117        141,318                    64
 12                 131        565,254                    64
 14                 145      2,260,998                    64
 16                 159      9,043,974                    64

 bits de N  divisiones (N primo)    2^(b/2)
         8                    14         16
        12                    62         64
        16                   254        256
        20                 1,022      1,024
        24                 4,094      4,096
        28                16,382     16,384
        32                65,534     65,536
        36               262,142    262,144
```

Las dos tablas tienen la misma forma: cada 2 bits más en la capacidad, la DP hace unas **4 veces** más trabajo (la columna se multiplica por $2^2$); cada 4 bits más en $N$, la división hace **4 veces** más divisiones. Con el mayor primo de $b$ bits, $N$ está justo debajo de $2^b$ y la cuenta da $\lfloor\sqrt N\rfloor - 1 = 2^{b/2} - 2$: es la fórmula $\sqrt{N} = \sqrt{2^b} = 2^{b/2}$ de C1, medida. Mientras tanto la fuerza bruta de la mochila hace siempre $2^6 = 64$ subconjuntos, sin importar el tamaño de los números: es exponencial en $n$, no en los bits de los pesos. Ninguno de los dos algoritmos de mochila es polinomial; simplemente le duelen cosas distintas.

---

**Uso de IA**: implementación de algoritmos, generación de casos de prueba y correcciones de redacción.
