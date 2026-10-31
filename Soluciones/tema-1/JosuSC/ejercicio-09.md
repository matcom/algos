# Ejercicio 9: Una mezcla "optimizada" que ahorra una comparación

> **Enunciado.** Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla. (C5)

## 1. Especificación del problema

**Entrada.** Dos listas $A = (a_1, \ldots, a_n)$ y $B = (b_1, \ldots, b_n)$ ordenadas de forma no decreciente.

**Salida.** La lista de los $2n$ elementos ordenada de forma no decreciente.

**Modelo.** Comparaciones entre un elemento de $A$ y uno de $B$ (comparar elementos de la misma lista no aporta, porque la precondición ya responde). El costo es el número de comparaciones en el peor caso.

### 1.1. La mezcla estándar

```python
def mezcla(A, B):
    n = len(A)
    i = j = 0
    out = []
    while i < n and j < n:
        if A[i] <= B[j]:
            out.append(A[i]); i += 1
        else:
            out.append(B[j]); j += 1
    return out + A[i:] + B[j:]          # uno de los dos restos es vacío
```

### 1.2. La versión "optimizada"

```python
def mezcla_opt(A, B):
    n = len(A)
    i = j = 0
    out = []
    while i < n - 1 and j < n:          # se detiene cuando a A le queda un solo elemento
        if A[i] <= B[j]:
            out.append(A[i]); i += 1
        else:
            out.append(B[j]); j += 1
    if j == n:                          # se acabó B: se copia el resto de A
        return out + A[i:]
    return out + B[j:] + [A[n - 1]]     # a A le queda uno: se copia B y se pone ese al final
```

**Precisiones que el enunciado no da y hay que fijar:**

- **"La primera lista"** es $A$, la primera de la entrada.
- **"Lo pone al final"** significa al final de la salida, es decir, después de copiar sin comparar lo que le quede a $B$.
- **Si se acaba $B$ primero**, el resto de $A$ se copia como en la mezcla estándar.

## 2. Cuántas comparaciones hace

Cada vuelta del ciclo hace exactamente una comparación, así que el número de comparaciones es el número de vueltas $= i_f + j_f$ (los valores finales de los índices).

**Teorema.**

- La mezcla estándar hace a lo sumo $2n - 1$ comparaciones, y las alcanza.
- La mezcla "optimizada" hace a lo sumo $\mathbf{2n - 2}$ comparaciones, y las alcanza (para $n = 1$ hace $0$).

**Demostración.**

*Estándar.* El ciclo para cuando una lista se agota. En la última vuelta, una de las dos listas pasa a estar agotada ($i = n$ o $j = n$) y la otra tiene índice $\leq n - 1$. Por tanto $i_f + j_f \leq n + (n - 1) = 2n - 1$. La entrada $A = (1, 3, \ldots, 2n-1)$, $B = (2, 4, \ldots, 2n)$ lo alcanza.

*Optimizada.* El ciclo se detiene cuando $i = n - 1$ o $j = n$. Antes de la última vuelta se tenía $i \leq n - 2$ y $j \leq n - 1$. Después de ella:

- si $i = n - 1$, entonces $j \leq n - 1$, y el total es $\leq (n - 1) + (n - 1) = 2n - 2$;
- si $j = n$, entonces $i \leq n - 2$, y el total es $\leq (n - 2) + n = 2n - 2$.

*Se alcanza.* Con $A = (2, 4, \ldots, 2n)$ y $B = (1, 3, \ldots, 2n-1)$, la mezcla intercala $b_1 < a_1 < b_2 < a_2 < \cdots$ y el ciclo sigue hasta sacar $a_{n-1}$, con $j = n - 1$: son $2n - 2$ vueltas. ∎

La "optimización" ahorra una comparación en el peor caso: de $2n - 1$ a $2n - 2$.

## 3. Decidir sin probar: la cota de mezclar

**Teorema (cota mínima de mezclar, conferencia 5).** Todo algoritmo de comparaciones que mezcla dos listas ordenadas de $n$ elementos distintos hace **al menos $2n - 1$ comparaciones** en el peor caso.

Se incluye la demostración, por el adversario, porque es la que se usará en §4.

**Demostración.** Sea la entrada

$$I:\quad a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n.$$

Su orden total $c_1 < c_2 < \cdots < c_{2n}$ tiene $2n - 1$ **pares adyacentes** $\{c_t, c_{t+1}\}$, y cada uno mezcla un elemento de $A$ con uno de $B$ (alternan).

*Afirmación: un algoritmo correcto compara directamente cada par adyacente.* Supongamos que no compara el par $\{x, y\}$, con $x < y$ adyacentes. Sea $I'$ la entrada que resulta de **intercambiar los valores** de $x$ e $y$.

1. **$I'$ es una entrada válida.** Como $x$ e $y$ son adyacentes en el orden, ningún elemento cae entre ellos: para todo otro elemento $z$, $z < x \iff z < y$. Además $x$ e $y$ están en listas distintas, así que en la lista que contiene a uno, el vecino compara con el nuevo valor igual que comparaba con el viejo. Ambas listas siguen ordenadas.
2. **El algoritmo no distingue $I$ de $I'$.** Las únicas respuestas que cambian son las de comparar $x$ con $y$, que no se hizo. Un algoritmo determinista que recibe las mismas respuestas hace las mismas preguntas y produce la misma salida.
3. **Pero las salidas correctas son distintas:** en $I$ el elemento $x$ va antes que $y$, y en $I'$ después.

Contradicción. Como cada comparación cubre a lo sumo un par, hacen falta al menos $2n - 1$ comparaciones. ∎

**Conclusión sin ejecutar nada.** La mezcla "optimizada" hace a lo sumo $2n - 2 < 2n - 1$ comparaciones **en todas las entradas** (§2). Si fuera correcta, contradiría el teorema. Por tanto **no es correcta**: existe una entrada en la que falla. Es el uso de una cota mínima demostrada para detectar un algoritmo que está mal (conferencia 5).

## 4. Construyendo la entrada que falla

### 4.1. Se ejecuta la "optimizada" contra el adversario

Sobre la entrada del adversario $I$ ($A = (1, 3, \ldots, 2n-1)$, $B = (2, 4, \ldots, 2n)$), el algoritmo saca $a_1, b_1, a_2, b_2, \ldots, a_{n-1}$ y, al sacar $a_{n-1}$, a $A$ le queda un solo elemento ($a_n$) y el ciclo se detiene. Hizo $2n - 3$ comparaciones: se saltó **dos** pares adyacentes de los $2n - 1$:

$$\{b_{n-1}, a_n\} \quad \text{y} \quad \{a_n, b_n\}.$$

**Ejemplo con $n = 3$:** $A = (1, 3, 5)$, $B = (2, 4, 6)$. Las comparaciones son $1{:}2$, $3{:}2$, $3{:}4$ (tres, $= 2n - 3$). Luego $A$ tiene un solo elemento ($5$): se copia $B$ restante, $4, 6$, y se pone $5$ al final. La salida es

$$[1, 2, 3, 4, 6, 5] \quad \text{(incorrecta).}$$

Los pares no comparados son $\{4, 5\}$ y $\{5, 6\}$.

### 4.2. La entrada gemela y la entrada que falla

El adversario intercambia los valores de un par no comparado. Con el par $\{a_n, b_n\}$ se obtiene

$$I':\quad A = (1, 3, \ldots, 2n-3,\ 2n), \qquad B = (2, 4, \ldots, 2n-2,\ 2n-1).$$

La "optimizada" hace **exactamente lo mismo** sobre $I$ e $I'$ (mismas comparaciones, mismas respuestas, misma salida por posiciones). En $I'$ esa salida es correcta (en $I'$ es $b_n < a_n$); en $I$ no lo es. Por tanto:

> **La entrada que falla es $I$:** $A = (1, 3, \ldots, 2n-1)$, $B = (2, 4, \ldots, 2n)$, con salida $1, 2, \ldots, 2n-2,\ 2n,\ 2n-1$.

Con el otro par no comparado, $\{b_{n-1}, a_n\}$, se obtiene una segunda entrada que falla: $A = (1, 3, \ldots, 2n-3,\ 2n-2)$ y $B = (2, 4, \ldots, 2n-4,\ 2n-1,\ 2n)$.

**Ejemplo con $n = 4$:**

| Entrada | $A$ | $B$ | Salida de `mezcla_opt` | Comparaciones |
|---|---|---|---|---|
| $I$ | $[1,3,5,7]$ | $[2,4,6,8]$ | $[1,2,3,4,5,6,\mathbf{8,7}]$ ✗ | 5 |
| $I'$ (gemela) | $[1,3,5,8]$ | $[2,4,6,7]$ | $[1,2,3,4,5,6,7,8]$ ✓ | 5 |
| $I''$ (otro par) | $[1,3,5,6]$ | $[2,4,7,8]$ | $[1,2,3,4,5,\mathbf{7,8,6}]$ ✗ | 5 |

### 4.3. Caracterización exacta del fallo

La cota dice que hay entradas que fallan, pero no cuáles. Se puede decir exactamente.

**Lema (invariante de la mezcla estándar).** Al evaluar la guarda, con $i$ y $j$ elementos sacados de $A$ y $B$, lo que se sacó es una lista ordenada y cada elemento sacado es $\leq$ cada elemento que queda.

*Demostración.* Inicialmente no se ha sacado nada. Si $A[i] \leq B[j]$ y se saca $A[i]$: $A[i] \leq A[i']$ para $i' > i$ (la lista es ordenada) y $A[i] \leq B[j] \leq B[j']$ para $j' \geq j$, así que es $\leq$ todo lo que queda. Además, por hipótesis, es $\geq$ el último sacado (que era $\leq$ todo lo que quedaba). El caso de $B[j]$ es simétrico. ∎

**Teorema.** La mezcla "optimizada" es correcta sobre una entrada **si y solo si** $a_n \geq b_n$ (el último de $A$ es $\geq$ el último de $B$).

**Demostración.**

*($\Leftarrow$)* Si el ciclo sale por $j = n$, se copia el resto de $A$: la salida coincide con la estándar. Si sale por $i = n - 1$ con $j < n$, por el Lema lo sacado es ordenado y $\leq$ lo que queda; la salida sigue con $B[j..n-1]$ (ordenado) y luego $a_n \geq b_n \geq B[j..n-1]$, que queda ordenado.

*($\Rightarrow$, por contrarrecíproca)* Si $a_n < b_n$: durante el ciclo $i \leq n - 2$, así que $A[i] \leq a_n < b_n$ y por tanto $b_n$ nunca se saca ($b_n$ solo saldría si $b_n < A[i]$). Entonces $j < n$ siempre, el ciclo termina por $i = n - 1$, y la salida acaba en $\ldots, b_n, a_n$ con $b_n > a_n$: **no está ordenada**. (Para $n = 1$, el ciclo no corre y la salida es $[b_1, a_1]$, incorrecta si $b_1 > a_1$.) ∎

**Consecuencia.** Con valores distintos, $a_n < b_n$ equivale a que el máximo de las $2n$ entradas está en $B$. Eso ocurre en $\binom{2n-1}{n}$ de los $\binom{2n}{n}$ entrelazados: **exactamente la mitad**. Es un error que casi cualquier prueba aleatoria encuentra, pero a un generador que siempre ponga el mayor elemento en $A$ no lo vería.

### 4.4. ¿Se puede reparar?

No hay reparación que baje de $2n - 1$ en el peor caso: la cota de §3 vale para cualquier algoritmo. Si se arregla comparando $a_n$ contra lo que queda de $B$, se recuperan las comparaciones y se vuelve a la mezcla estándar, que es **óptima**: $2n - 1$ comparaciones, y no hay mezcla más rápida en el peor caso.

## 5. Experimento

### 5.1. Código

```python
import itertools, random
from math import comb

def mezcla(A, B):
    """Mezcla estándar. Devuelve (salida como celdas, comparaciones hechas)."""
    n = len(A); i = j = 0; out = []; cmps = []
    while i < n and j < n:
        cmps.append((("A", i), ("B", j)))
        if A[i] <= B[j]:
            out.append(("A", i)); i += 1
        else:
            out.append(("B", j)); j += 1
    out += [("A", k) for k in range(i, n)] + [("B", k) for k in range(j, n)]
    return out, cmps

def mezcla_opt(A, B):
    """'Optimizada': deja de comparar cuando a A le queda un elemento y lo pone al final."""
    n = len(A); i = j = 0; out = []; cmps = []
    while i < n - 1 and j < n:
        cmps.append((("A", i), ("B", j)))
        if A[i] <= B[j]:
            out.append(("A", i)); i += 1
        else:
            out.append(("B", j)); j += 1
    if j == n:
        out += [("A", k) for k in range(i, n)]
    else:
        out += [("B", k) for k in range(j, n)] + [("A", n - 1)]
    return out, cmps

def valores(A, B, out):
    return [A[k] if t == "A" else B[k] for t, k in out]

def desde_patron(n, posA):
    """Entrada con valores 0..2n-1 donde A ocupa las posiciones posA de la mezcla."""
    posA = set(posA); A, B = [], []
    for p in range(2 * n):
        (A if p in posA else B).append(p)
    return A, B

# 1) Todos los entrelazados: peor caso de cada una y caracterización del fallo
print("n  entrelazados  max_estándar  max_opt  fallos_opt  C(2n-1,n)")
for n in range(1, 9):
    mx_s = mx_o = fallos = tot = 0
    for posA in itertools.combinations(range(2 * n), n):
        A, B = desde_patron(n, posA); tot += 1
        os_, cs = mezcla(A, B); oo, co = mezcla_opt(A, B)
        assert valores(A, B, os_) == sorted(A + B)
        mx_s, mx_o = max(mx_s, len(cs)), max(mx_o, len(co))
        correcta = valores(A, B, oo) == sorted(A + B)
        assert correcta == (A[-1] >= B[-1])                  # el teorema de §4.3
        fallos += not correcta
    assert mx_s == 2 * n - 1 and mx_o == 2 * n - 2 and fallos == comb(2 * n - 1, n)
    print(n, tot, mx_s, mx_o, fallos, comb(2 * n - 1, n))

# 2) Con duplicados: la caracterización sigue valiendo
cnt = 0
for n, V in [(1, 4), (2, 4), (3, 4), (4, 3), (5, 2)]:
    for A in itertools.combinations_with_replacement(range(V + 1), n):
        for B in itertools.combinations_with_replacement(range(V + 1), n):
            A_, B_ = list(A), list(B)
            oo, co = mezcla_opt(A_, B_)
            assert (valores(A_, B_, oo) == sorted(A + B)) == (A[-1] >= B[-1])
            assert len(co) <= 2 * n - 2
            cnt += 1
print("con duplicados OK:", cnt, "pares")

# 3) El adversario
def pares_adyacentes(n):
    orden = []
    for k in range(n):
        orden += [("A", k), ("B", k)]                        # a1 b1 a2 b2 ... an bn
    return {frozenset((orden[t], orden[t + 1])) for t in range(2 * n - 1)}

for n in range(2, 9):
    A = [2 * k + 1 for k in range(n)]; B = [2 * k + 2 for k in range(n)]          # I
    pares = pares_adyacentes(n)
    _, cs = mezcla(A, B)
    assert {frozenset(c) for c in cs} == pares and len(cs) == 2 * n - 1           # la estándar los compara todos
    oo, co = mezcla_opt(A, B)
    faltan = pares - {frozenset(c) for c in co}
    assert len(co) == 2 * n - 3 and faltan == {frozenset((("B", n - 2), ("A", n - 1))),
                                                frozenset((("A", n - 1), ("B", n - 1)))}
    A2 = A[:-1] + [B[-1]]; B2 = B[:-1] + [A[-1]]                                  # I'
    oo2, co2 = mezcla_opt(A2, B2)
    assert co2 == co and oo2 == oo                                                # mismo comportamiento
    assert valores(A2, B2, oo2) == sorted(A2 + B2)                                # correcta en I'
    assert valores(A, B, oo) != sorted(A + B)                                     # incorrecta en I
print("adversario OK")

n = 4
for nombre, A, B in [("I  ", [1, 3, 5, 7], [2, 4, 6, 8]), ("I' ", [1, 3, 5, 8], [2, 4, 6, 7]),
                     ("I''", [1, 3, 5, 6], [2, 4, 7, 8])]:
    oo, co = mezcla_opt(A, B)
    print(nombre, A, B, "->", valores(A, B, oo), len(co), "comparaciones")

# 4) La entrada de 2n-2 comparaciones (y correcta)
for n in (2, 3, 4, 5):
    B = [2 * k + 1 for k in range(n - 1)] + [2 * n - 1]
    A = [2 * k + 2 for k in range(n - 1)] + [2 * n]
    oo, co = mezcla_opt(A, B)
    assert len(co) == 2 * n - 2 and valores(A, B, oo) == sorted(A + B)

# 5) Pruebas aleatorias
random.seed(2026)
for n in (4, 8, 16):
    ens, f = 20000, 0
    for _ in range(ens):
        A = sorted(random.randint(0, 99) for _ in range(n))
        B = sorted(random.randint(0, 99) for _ in range(n))
        oo, _ = mezcla_opt(A, B)
        f += valores(A, B, oo) != sorted(A + B)
    print(f"aleatorio n={n}: {f}/{ens} fallos")
```

### 5.2. Resultados (ejecutado)

Sobre **todos** los entrelazados de valores distintos:

| $n$ | Entrelazados $\binom{2n}{n}$ | Peor caso estándar | Peor caso "optimizada" | Entradas donde falla | $\binom{2n-1}{n}$ |
|---|---|---|---|---|---|
| 1 | 2 | 1 | 0 | 1 | 1 |
| 2 | 6 | 3 | 2 | 3 | 3 |
| 3 | 20 | 5 | 4 | 10 | 10 |
| 4 | 70 | 7 | 6 | 35 | 35 |
| 5 | 252 | 9 | 8 | 126 | 126 |
| 6 | 924 | 11 | 10 | 462 | 462 |
| 7 | 3 432 | 13 | 12 | 1716 | 1716 |
| 8 | 12 870 | 15 | 14 | 6435 | 6435 |

| Comprobación | Casos | Resultado |
|---|---|---|
| Peor caso estándar $= 2n - 1$, "optimizada" $= 2n - 2$ | $n = 1..8$, todos los entrelazados | se cumple |
| Correcta $\iff a_n \geq b_n$ | todos los entrelazados ($n \leq 8$) y 3141 pares con duplicados | se cumple siempre |
| La estándar compara los $2n - 1$ pares adyacentes de $I$ | $n = 2..8$ | se cumple |
| La "optimizada" sobre $I$: $2n - 3$ comparaciones y exactamente los dos pares $\{b_{n-1}, a_n\}$, $\{a_n, b_n\}$ sin comparar | $n = 2..8$ | se cumple |
| Misma traza sobre $I$ e $I'$; correcta en $I'$, incorrecta en $I$ | $n = 2..8$ | se cumple |

Pruebas aleatorias (valores en $0..99$, 20 000 pares por $n$): fallan **48,3 %** ($n = 4$), **48,5 %** ($n = 8$) y **45,9 %** ($n = 16$). Estar por debajo del $50$ % se explica por los empates: con valores repetidos, $a_n = b_n$ no falla.

## 6. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Mezclar dos listas ordenadas de largo $n$. Modelo: comparaciones entre un elemento de $A$ y uno de $B$. |
| ¿Qué algoritmo? | La "optimizada": no compara cuando a $A$ le queda un elemento y lo pone al final. |
| ¿Cuánto cuesta? | A lo sumo $2n - 2$ comparaciones, una menos que la estándar ($2n - 1$). |
| ¿Es correcta? | **No.** La cota de mezclar ($\geq 2n - 1$) lo decide sin ejecutar nada. |
| ¿Dónde falla? | Se construye con el adversario: $I = (a_1 < b_1 < \cdots < a_n < b_n)$ deja sin comparar $\{b_{n-1}, a_n\}$ y $\{a_n, b_n\}$. Exactamente falla cuando $a_n < b_n$, la mitad de los entrelazados. |
| ¿Se puede mejor? | No: la mezcla estándar con $2n - 1$ comparaciones es óptima. |
