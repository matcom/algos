# Ejercicio 11: La mochila entera por programación dinámica, ¿es polinomial?

> **Enunciado.** La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

## 1. Especificación del problema

**Entrada.** Enteros $n \geq 1$ y $W \geq 0$ (la capacidad), pesos $w_1, \ldots, w_n \geq 1$ y valores $v_1, \ldots, v_n \geq 0$.

**Salida.** El valor máximo $\sum_{j \in S} v_j$ sobre los subconjuntos $S \subseteq \{1, \ldots, n\}$ con $\sum_{j \in S} w_j \leq W$. Cada objeto se toma entero una vez o no se toma (mochila 0/1).

**Modelo.** Word RAM, como en la conferencia 1: palabras de $w$ bits y operaciones de costo $1$ sobre ellas. Se supone que cada número de la entrada cabe en una palabra.

**Precisiones que el enunciado no da y hay que fijar:**

- **Qué se mide.** El costo es el número de operaciones de la word RAM. Eso es lo que $O(nW)$ cuenta.
- **Qué es el tamaño de la entrada.** La conferencia 1 (§8) lo fija: la cantidad de **bits** que ocupa. Un entero $m \geq 1$ escrito en binario ocupa $\operatorname{bits}(m) = \lfloor \log_2 m \rfloor + 1$ bits. Una instancia $I$ tiene tamaño
$$\ell(I) = \operatorname{bits}(n) + \operatorname{bits}(W) + \sum_{j=1}^{n} \operatorname{bits}(w_j) + \sum_{j=1}^{n} \operatorname{bits}(v_j)$$
(se ignoran los $O(n)$ separadores, que cambian $\ell$ solo por un factor constante).
- **Qué quiere decir "polinomial".** Un algoritmo es **polinomial** si existe un polinomio $p$ con $T(I) \leq p(\ell(I))$ para toda instancia $I$. Es **pseudopolinomial** si $T(I)$ está acotado por un polinomio en $\ell(I)$ *y en los valores numéricos* de la entrada (aquí, $W$).

## 2. El algoritmo y su correctitud

```python
def mochila(pesos, valores, W):
    dp = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):          # de mayor a menor capacidad
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]
```

### 2.1. Invariante

Sea $F(i, c) = \max\{\sum_{j \in S} v_j : S \subseteq \{1, \ldots, i\},\ \sum_{j \in S} w_j \leq c\}$, el mejor valor usando solo los primeros $i$ objetos con capacidad $c$.

> **Invariante externo $I(i)$.** Tras procesar $i$ objetos, $\texttt{dp}[c] = F(i, c)$ para todo $c \in [0, W]$.

> **Invariante interno.** Durante el procesamiento del objeto $i$, justo antes de actualizar $\texttt{dp}[c]$: para $c' \leq c$, $\texttt{dp}[c'] = F(i-1, c')$ (aún sin actualizar), y para $c' > c$, $\texttt{dp}[c'] = F(i, c')$.

### 2.2. Demostración en tres pasos

**Inicialización.** Con $i = 0$, ningún objeto: $\texttt{dp}[c] = 0 = F(0, c)$. ✔

**Mantenimiento.** El objeto $i$ está o no en una solución óptima para $(i, c)$, así que

$$F(i, c) = \begin{cases} \max\bigl(F(i-1, c),\ F(i-1, c - w_i) + v_i\bigr) & \text{si } c \geq w_i, \\ F(i-1, c) & \text{si } c < w_i. \end{cases}$$

El ciclo interno recorre $c$ **de mayor a menor**. Como $w_i \geq 1$, el índice $c - w_i < c$ todavía no se ha actualizado en esta pasada, así que por el invariante interno `dp[c - w]` vale $F(i-1, c - w_i)$, y la asignación escribe exactamente $F(i, c)$. Las capacidades $c < w_i$ no se tocan y ya valen $F(i-1, c) = F(i, c)$. Con esto se restablecen los dos invariantes. ✔

**Conclusión.** Tras los $n$ objetos, $\texttt{dp}[W] = F(n, W)$, el valor óptimo. Termina porque los dos ciclos recorren rangos finitos. ∎

(El orden descendente es esencial: con orden ascendente, `dp[c - w]` ya incluiría al objeto $i$ y el algoritmo resolvería la mochila con repetición.)

### 2.3. Costo en operaciones

El ciclo interno hace $\max(0, W - w_i + 1)$ iteraciones por objeto, cada una con $O(1)$ operaciones de la word RAM (dos lecturas, una suma, una comparación, una escritura):

$$\#\text{iteraciones} = \sum_{i=1}^{n} \max(0, W - w_i + 1) \leq nW.$$

Si $w_i \leq W/2$ para todo $i$, es al menos $nW/2$. Por tanto el costo es $\Theta(nW)$ y la **memoria** es $\Theta(W)$ palabras.

## 3. El tamaño de la entrada en bits

El número $W$ aparece en la entrada **escrito en binario**, y por eso ocupa solo $\operatorname{bits}(W) = \lfloor \log_2 W \rfloor + 1$ bits, no $W$ símbolos. Dicho al revés: de $\operatorname{bits}(W) = b$ solo se sabe $2^{b-1} \leq W < 2^b$.

| $W$ | Bits de $W$ | Valor de $W$ comparado con sus bits |
|---|---|---|
| $1000$ | $10$ | $W \approx 2^{10}$ |
| $10^6$ | $20$ | $W \approx 2^{20}$ |
| $10^9$ | $30$ | $W \approx 2^{30}$ |
| $2^{64}$ | $65$ (cabe en dos palabras; $2^{64} - 1$ en una) | $W \approx 2^{64}$ |

De la definición de $\ell$:

$$\operatorname{bits}(W) \leq \ell(I) \qquad\text{y por tanto}\qquad W < 2^{\ell(I)}.$$

Es la misma observación de la conferencia 1 (§8) sobre probar divisores: un ciclo que cuenta hasta un número cuenta hasta algo que es **exponencial** en la cantidad de bits que lo escriben.

## 4. ¿Es polinomial? No: es pseudopolinomial

**Teorema 1 (el algoritmo no es polinomial).** No existe un polinomio $p$ tal que $T(I) \leq p(\ell(I))$ para toda instancia.

**Demostración.** Sea $I_b$ la instancia con $n = 2$, pesos $w = (1, 1)$, valores $v = (1, 1)$ y capacidad $W = 2^b - 1$.

- **Tamaño.** $\ell(I_b) = \operatorname{bits}(2) + \operatorname{bits}(2^b - 1) + 1 + 1 + 1 + 1 = b + 6$.
- **Costo.** Como $w_i = 1$, el ciclo interno recorre $c = W, W-1, \ldots, 1$: $W$ iteraciones por objeto. El total es
$$T(I_b) = 2(2^b - 1) = 2^{\ell(I_b) - 5} - 2.$$

Si $T(I) \leq p(\ell(I))$ para un polinomio $p$ de grado $k$, entonces $2^{b+1} - 2 \leq p(b + 6) = O(b^k)$ para todo $b$. Pero $2^b / b^k \to \infty$. Contradicción. ∎

**Teorema 2 (cota superior exponencial, ajustada).** Para toda instancia, $T(I) \leq n \cdot W < n \cdot 2^{\ell(I)}$.

Con el Teorema 1, el costo es $2^{\Theta(\ell)}$ en el peor caso: exponencial en el tamaño de la entrada, aunque el código sea "dos ciclos anidados".

**Teorema 3 (en qué sentido sí es "polinomial").**

1. **Es polinomial en $n$ y en $W$** (los *valores*): $T \leq nW$.
2. **Es polinomial en el tamaño unario.** Si los números se escribieran en unario, el tamaño sería $\ell_u \geq n + W$, y $nW \leq \ell_u^2$.
3. **Es polinomial en $\ell$ cuando $W \leq n^k$ para una constante $k$**: como $n \leq \ell$, $T \leq n^{k+1} \leq \ell^{k+1}$.

A un algoritmo con esta propiedad se le llama **pseudopolinomial**.

**Costo real.** A $10^9$ operaciones por segundo, con $n = 100$ objetos y $W \approx 2^b$:

| Bits de $W$ | Iteraciones $\approx nW$ | Tiempo | Tabla `dp` ($W + 1$ palabras de 8 bytes) |
|---|---|---|---|
| $20$ | $1{,}05 \times 10^{8}$ | $0{,}1$ s | $8$ MB |
| $30$ | $1{,}07 \times 10^{11}$ | $1{,}8$ min | $8$ GB |
| $40$ | $1{,}10 \times 10^{14}$ | $1{,}3$ días | $8$ TB |
| $50$ | $1{,}13 \times 10^{17}$ | $3{,}6$ años | $8$ PB |
| $64$ | $1{,}85 \times 10^{21}$ | $58\,450$ años | $\approx 1{,}5 \times 10^{20}$ bytes |

Con una capacidad que cabe en **una sola palabra** de la máquina, el algoritmo no se puede ejecutar. Es lo que significa ser exponencial en bits.

## 5. En qué se parece a la primalidad por división

**La primalidad por división:**

```python
def es_primo(N):
    d = 2
    while d * d <= N:
        if N % d == 0:
            return False
        d += 1
    return True
```

Hace $\Theta(\sqrt{N})$ divisiones. Parece un solo ciclo, y es polinomial en el *valor* $N$. Pero $N$ ocupa $b = \operatorname{bits}(N)$ bits y $\sqrt{N} \approx 2^{b/2}$: **exponencial en el tamaño de la entrada** (conferencia 1, §8).

**El parecido.** Los dos algoritmos tienen la misma forma:

| | Primalidad por división | Mochila por PD |
|---|---|---|
| **Número en la entrada** | $N$, con $b$ bits | $W$, con $b$ bits |
| **Lo que cuenta el ciclo** | hasta $\lfloor \sqrt{N} \rfloor$ | hasta $W$, $n$ veces |
| **Pasos** | $\Theta(\sqrt{N}) = \Theta(2^{b/2})$ | $\Theta(nW) = \Theta(n \, 2^{b})$ |
| **Polinomial en el valor del número** | sí | sí |
| **Polinomial en su cantidad de bits** | **no** | **no** |
| **Si el número se escribiera en unario** | polinomial ($\sqrt{N} \leq N$) | polinomial ($nW \leq \ell_u^2$) |
| **Al añadir un bit al número** | el costo se multiplica por $\sqrt{2}$ | el costo se multiplica por $2$ |

En los dos casos se confunde **"polinomial en el valor"** con **"polinomial en el tamaño"**, que es justo el error que la conferencia 1 señala ("llamar polinomial a algo exponencial en bits"). El tamaño de un número es su longitud, no su magnitud.

**Dónde se diferencian.**

- **El problema.** *Primalidad está en P*: AKS (2002) la decide en tiempo polinomial en $b$, y Miller–Rabin en tiempo polinomial aleatorio. La división es simplemente un mal algoritmo para un problema fácil. En cambio, la versión de decisión de la mochila es **NP-completa** (Karp, 1972): no se conoce ningún algoritmo polinomial en bits, y encontrarlo probaría $\mathrm{P} = \mathrm{NP}$.
- **¿Contradice esto a la PD?** No. Un algoritmo pseudopolinomial no es polinomial. La mochila es NP-difícil en el sentido *débil*: su dificultad viene de que los números pueden ser exponencialmente grandes; si $W$ está acotado polinomialmente en $n$, es fácil (Teorema 3, punto 3). Los problemas NP-difíciles en sentido *fuerte* no admiten algoritmo pseudopolinomial, salvo que $\mathrm{P} = \mathrm{NP}$.
- **Las alternativas clásicas tampoco son polinomiales en bits.** La PD sobre valores, $O(n \cdot V)$ con $V = \sum v_i$, es igualmente pseudopolinomial, y la búsqueda por mitades (*meet in the middle*) hace $O(2^{n/2})$ pasos hasta factores polinomiales.

## 6. Experimento

### 6.1. Código

```python
import random, time

def mochila(pesos, valores, W, contar=False):
    dp = [0] * (W + 1)
    it = 0
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
            it += 1
    return (dp[W], it) if contar else dp[W]

def fuerza_bruta(pesos, valores, W):
    n = len(pesos); best = 0
    for mask in range(1 << n):
        pw = sum(pesos[i] for i in range(n) if mask >> i & 1)
        if pw <= W:
            best = max(best, sum(valores[i] for i in range(n) if mask >> i & 1))
    return best

def bits(m):
    return m.bit_length()

# 1) Correctitud y conteo exacto de iteraciones
random.seed(3)
casos = 0
for _ in range(20000):
    n = random.randint(1, 10)
    W = random.randint(0, 40)
    pesos = [random.randint(1, 45) for _ in range(n)]
    valores = [random.randint(0, 30) for _ in range(n)]
    v, it = mochila(pesos, valores, W, True)
    assert v == fuerza_bruta(pesos, valores, W)
    assert it == sum(max(0, W - w + 1) for w in pesos)      # §2.3: la fórmula exacta
    casos += 1
print("correctitud OK:", casos)

# 2) La familia I_b del Teorema 1: tamaño en bits y costo
print("b  l(I_b)  iteraciones  2(2^b - 1)")
for b in range(1, 17):
    W = 2**b - 1
    v, it = mochila([1, 1], [1, 1], W, True)
    l = bits(2) + bits(W) + 4 * bits(1)
    assert l == b + 6 and it == 2 * (2**b - 1) and v == min(2, W)
    if b in (1, 2, 4, 8, 12, 16):
        print(b, l, it, 2 * (2**b - 1))

# 3) Tiempo de pared con n = 5 y W = 2^b - 1 (los tiempos varían de una ejecución a otra)
print("b  iteraciones  segundos  razón")
prev = None
for b in range(12, 19):
    W = 2**b - 1
    t = time.time()
    mochila([1] * 5, [1] * 5, W)
    dt = time.time() - t
    print(b, 5 * W, f"{dt:.3f}", "" if prev is None else f"{dt / prev:.2f}")
    prev = dt

# 4) Estimación para n = 100 a 1e9 operaciones por segundo
for b in (20, 30, 40, 50, 64):
    it = 100 * (2**b - 1)
    print(b, f"{it:.3e} iteraciones", f"{it / 1e9:.3e} s")
```

El segundo bloque cuenta las divisiones de la primalidad por división sobre números primos de $b$ bits (para un primo $N$, el ciclo recorre todos los $d \leq \sqrt{N}$).

```python
import time

def es_primo_mr(n):                       # Miller-Rabin determinista, solo para elegir primos
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def primo_bajo(b):                        # el mayor primo menor que 2^b
    n = 2**b - 1
    while not es_primo_mr(n):
        n -= 2
    return n

def primo_por_division(N):
    d, cnt = 2, 0
    while d * d <= N:
        cnt += 1
        if N % d == 0:
            return False, cnt
        d += 1
    return True, cnt

print("b  N  divisiones  2^(b/2)  razón respecto a b-2")
prev = None
for b in range(10, 51, 2):
    N = primo_bajo(b)
    ok, cnt = primo_por_division(N)
    assert ok
    print(b, N, cnt, round(2 ** (b / 2)), "" if prev is None else f"{cnt / prev:.3f}")
    prev = cnt
```

### 6.2. Resultados (ejecutado)

| Comprobación | Casos | Resultado |
|---|---|---|
| PD correcta frente a fuerza bruta, y número de iteraciones $= \sum_i \max(0, W - w_i + 1)$ | 20 000 instancias aleatorias ($n \leq 10$, $W \leq 40$) | se cumple |
| Familia $I_b$: $\ell(I_b) = b + 6$ e iteraciones $= 2(2^b - 1)$ | $b = 1, \ldots, 16$ | se cumple |

**La familia $I_b$** (el tamaño crece linealmente en $b$; el costo, exponencialmente):

| $b$ | $\ell(I_b)$ (bits) | Iteraciones $= 2(2^b - 1)$ |
|---|---|---|
| 1 | 7 | 2 |
| 2 | 8 | 6 |
| 4 | 10 | 30 |
| 8 | 14 | 510 |
| 12 | 18 | 8190 |
| 16 | 22 | 131 070 |

**Tiempo de pared** ($n = 5$, $W = 2^b - 1$; los tiempos varían entre ejecuciones):

| $b$ | Iteraciones | Segundos | Razón respecto a $b - 1$ |
|---|---|---|---|
| 12 | 20 475 | 0,003 | |
| 13 | 40 955 | 0,006 | 2,06 |
| 14 | 81 915 | 0,012 | 1,99 |
| 15 | 163 835 | 0,024 | 2,05 |
| 16 | 327 675 | 0,047 | 1,95 |
| 17 | 655 355 | 0,094 | 1,99 |
| 18 | 1 310 715 | 0,189 | 2,00 |

Cada bit más en $W$ **duplica** el tiempo. (Para $b \geq 19$ los tiempos se vuelven irregulares: la tabla ya ocupa varios MB y su tamaño crece con $W$.)

**Primalidad por división** (número primo menor que $2^b$):

| $b$ | $N$ | Divisiones | $2^{b/2}$ | Razón respecto a $b - 2$ |
|---|---|---|---|---|
| 10 | 1021 | 30 | 32 | |
| 16 | 65 521 | 254 | 256 | 2,016 |
| 20 | 1 048 573 | 1022 | 1024 | 2,004 |
| 30 | 1 073 741 789 | 32 766 | 32 768 | 2,000 |
| 40 | 1 099 511 627 689 | 1 048 574 | 1 048 576 | 2,000 |
| 50 | 1 125 899 906 842 597 | 33 554 430 | 33 554 432 | 2,000 |

Dos bits más en $N$ **duplican** el costo, es decir, cada bit lo multiplica por $\sqrt{2}$. El conteo es $\approx 2^{b/2} - 2$ en todos los tamaños.

**La comparación.** El costo de la PD de la mochila se duplica con cada bit de $W$; el de la primalidad por división se duplica con cada *dos* bits de $N$. Las dos curvas son exponenciales en el número de bits; solo cambia la base ($2$ frente a $\sqrt{2}$).

## 7. Resumen

| Pregunta | Respuesta |
|---|---|
| ¿Qué algoritmo y cuánto cuesta? | PD sobre capacidades: $\Theta(nW)$ operaciones y $\Theta(W)$ palabras. Invariante: tras $i$ objetos, $\texttt{dp}[c] = F(i, c)$; el orden descendente protege a $\texttt{dp}[c - w]$. |
| ¿Cuánto mide la entrada? | $\ell = \operatorname{bits}(n) + \operatorname{bits}(W) + \sum \operatorname{bits}(w_j) + \sum \operatorname{bits}(v_j)$. $W$ ocupa $\log_2 W$ bits, así que $W < 2^{\ell}$. |
| ¿Es polinomial? | **No.** La familia $I_b$ tiene $\ell = b + 6$ bits y cuesta $2^{\ell - 5} - 2$. Es **pseudopolinomial**: polinomial en $n$ y en el valor $W$, o en el tamaño unario, o en $\ell$ cuando $W \leq n^k$. |
| ¿En qué se parece a la primalidad por división? | En que cuenta hasta un **número** y es polinomial en su valor pero exponencial en sus bits (conferencia 1, §8). Cada bit de $W$ duplica el costo; cada bit de $N$ lo multiplica por $\sqrt{2}$. |
| ¿En qué se diferencia? | Primalidad está en P (AKS); la mochila (decisión) es NP-completa y débilmente NP-difícil: el algoritmo pseudopolinomial no contradice $\mathrm{P} \neq \mathrm{NP}$. |
