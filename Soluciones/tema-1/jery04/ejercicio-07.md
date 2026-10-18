# Ejercicio 7: Mediana de dos arreglos ordenados

> **Enunciado.** Mediana de dos arreglos ordenados de largo $n$: el $n$-ésimo menor de los $2n$ elementos. Diseña un algoritmo $O(\log n)$, demuestra su correctitud y da la cota de información. (C2, C3, C5)

## 1. Especificación del problema

**Entrada.** Dos arreglos $A[0..n-1]$ y $B[0..n-1]$, con $n \geq 1$, ordenados de forma no decreciente.

**Salida.** El valor del $n$-ésimo menor de los $2n$ elementos: si $s_1 \leq s_2 \leq \cdots \leq s_{2n}$ es la mezcla ordenada de $A$ y $B$, la salida es $s_n$.

**Modelo.** Comparaciones entre un elemento de $A$ y un elemento de $B$. Comparar dos elementos del mismo arreglo es inútil, porque la precondición ya responde. Cada comparación tiene dos respuestas ($\leq$ o $>$) y el costo es el número de comparaciones en el peor caso.

**Precisiones que el enunciado no da y hay que fijar:**

- **Qué "mediana".** Con $2n$ elementos no hay un elemento central. El enunciado fija el $n$-ésimo menor (la mediana inferior), que es lo que se calcula.
- **Duplicados.** Se pide el *valor* $s_n$, no una posición. Los empates no cambian el valor, pero para razonar con rangos hay que fijar un desempate (§2.1).
- **Qué se pide en costo.** Mezclar los dos arreglos y mirar $s_n$ cuesta $\Theta(n)$. El ejercicio pide $O(\log n)$: leer solo una parte mínima de las entradas.

## 2. Observaciones clave

### 2.1. Un orden total con desempate

Los $2n$ elementos son *celdas*: $A[0], \ldots, A[n-1], B[0], \ldots, B[n-1]$. Definimos $u \prec v$ como el orden lexicográfico de la terna (valor, etiqueta con $A < B$, índice):

$$u \prec v \iff \operatorname{val}(u) < \operatorname{val}(v), \ \text{o igual valor y } u \in A,\ v \in B, \ \text{o igual valor, mismo arreglo e índice menor.}$$

Propiedades:

- Es un orden **total** sobre las $2n$ celdas.
- Dentro de un arreglo coincide con el índice: $A[x] \prec A[y] \iff x < y$ (porque el arreglo es no decreciente).
- Es consistente con los valores, así que la lista de celdas ordenadas por $\prec$ tiene los valores en orden no decreciente, y $s_n$ es el valor de la celda de **rango $n$**.
- La comparación del algoritmo, `A[x] <= B[y]`, es exactamente $A[x] \prec B[y]$; y `A[x] > B[y]` es $B[y] \prec A[x]$.

Por tanto, basta razonar con rangos **sin empates**.

### 2.2. Ventanas

Para $a, b \geq 0$ y $s \geq 1$ con $a + s \leq n$ y $b + s \leq n$, la **ventana** es

$$W(a, b, s) = A[a..a+s-1] \cup B[b..b+s-1],$$

que tiene $2s$ celdas. Sea $\operatorname{rg}_W(z) = 1 + \#\{w \in W : w \prec z\}$ el rango de $z$ dentro de $W$, y $\operatorname{med}(W)$ la celda de $\operatorname{rg}_W = s$. El problema original es $\operatorname{med}(W(0, 0, n))$.

### 2.3. Lema de eliminación

**Lema.** Sean $s \geq 2$, $k, l \geq 0$ con $k + l = s - 2$, $W = W(a, b, s)$, $p = A[a+k]$ y $q = B[b+l]$.

1. Si $p \prec q$, entonces las $k+1$ celdas $A[a..a+k]$ tienen rango $< s$ en $W$, las $k+1$ celdas $B[b+l+1..b+s-1]$ tienen rango $> s$, y
$$\operatorname{med}(W(a, b, s)) = \operatorname{med}(W(a + k + 1,\ b,\ s - k - 1)).$$
2. Si $q \prec p$, entonces las $l+1$ celdas $B[b..b+l]$ tienen rango $< s$, las $l+1$ celdas $A[a+k+1..a+s-1]$ tienen rango $> s$, y
$$\operatorname{med}(W(a, b, s)) = \operatorname{med}(W(a,\ b + l + 1,\ k + 1)).$$

**Demostración.**

*Caso 1 ($p \prec q$).*

- *Las celdas de $A[a..a+k]$ están por debajo de la mediana.* Las celdas de $W$ que preceden a $p$ son: de $A$, solo $A[a..a+k-1]$ ($k$ celdas); de $B$, las que preceden a $p$ preceden también a $q$, así que son a lo sumo $B[b..b+l-1]$ ($l$ celdas). Entonces $\operatorname{rg}_W(p) \leq k + l + 1 = s - 1$. Como toda celda de $A[a..a+k]$ es $\preceq p$, todas tienen rango $\leq s - 1 < s$.
- *Las celdas de $B[b+l+1..b+s-1]$ están por encima.* Hay $s - 1 - l = k + 1$ de ellas. Para una de ellas, $z$: todas las $k+1$ celdas $A[a..a+k]$ cumplen $\preceq p \prec q \prec z$, y las $l+1$ celdas $B[b..b+l]$ cumplen $\preceq q \prec z$. Hay al menos $k + l + 2 = s$ celdas que preceden a $z$, así que $\operatorname{rg}_W(z) \geq s + 1$.
- *La mediana se conserva.* Se quitan de $W$ exactamente $k+1$ celdas de rango $< s$ y $k+1$ de rango $> s$. Quedan $2s - 2(k+1) = 2s'$ celdas, con $s' = s - k - 1$, que son $A[a+k+1..a+s-1] \cup B[b..b+l]$ (de tamaños $s - 1 - k = s'$ y $l + 1 = s'$), es decir, $W(a+k+1, b, s')$. La celda de rango $s$ no se quitó, y en el conjunto restante su rango es $s - (k+1) = s'$: es la mediana de la ventana nueva.

*Caso 2 ($q \prec p$).* Es simétrico, intercambiando los papeles de $A$ y $B$ ($k \leftrightarrow l$). Se quitan $l + 1$ celdas por debajo ($B[b..b+l]$) y $l + 1$ por encima ($A[a+k+1..a+s-1]$); queda $W(a, b+l+1, s')$ con $s' = s - l - 1 = k + 1$. ∎

**Elección.** Tomamos $k = \lceil s/2 \rceil - 1$ y $l = \lfloor s/2 \rfloor - 1$, que cumplen $k + l = s - 2$ y $k, l \geq 0$ para $s \geq 2$. Entonces el tamaño nuevo es

$$s' = s - k - 1 = \lfloor s/2 \rfloor \ \ \text{(caso 1)}, \qquad s' = k + 1 = \lceil s/2 \rceil \ \ \text{(caso 2)}.$$

En ambos casos $1 \leq s' \leq \lceil s/2 \rceil < s$.

**Caso base.** Si $s = 1$, $W = \{A[a], B[b]\}$ y la celda de rango $1$ es la menor de las dos: el valor es $\min(A[a], B[b])$, con una comparación.

## 3. Algoritmo

```python
def mediana(A, B):
    n = len(A)
    a = b = 0
    s = n                                   # ventanas A[a:a+s] y B[b:b+s]
    while s > 1:
        k = (s + 1) // 2 - 1                # ⌈s/2⌉ - 1
        l = s // 2 - 1                      # ⌊s/2⌋ - 1      (k + l = s - 2)
        if A[a + k] <= B[b + l]:
            a += k + 1                      # se van A[a..a+k] (bajos) y B[b+l+1..] (altos)
            s = s // 2
        else:
            b += l + 1                      # se van B[b..b+l] (bajos) y A[a+k+1..] (altos)
            s = (s + 1) // 2
    return min(A[a], B[b])
```

**Ejemplo.** $A = [2, 4, 6, 8]$, $B = [1, 3, 5, 7]$ ($n = 4$; el $4$.º menor es $4$).

| Paso | Ventanas | $k, l$ | Comparación | Resultado | Ventanas nuevas |
|---|---|---|---|---|---|
| 1 | $A[0..3]$, $B[0..3]$, $s=4$ | $1, 1$ | $A[1] = 4 \leq B[1] = 3$ | no | $b \leftarrow 2$, $s \leftarrow 2$: $\{2, 4\} \cup \{5, 7\}$ |
| 2 | $A[0..1]$, $B[2..3]$, $s=2$ | $0, 0$ | $A[0] = 2 \leq B[2] = 5$ | sí | $a \leftarrow 1$, $s \leftarrow 1$: $\{4\} \cup \{5\}$ |
| 3 | $A[1]$, $B[2]$, $s=1$ | | $\min(4, 5)$ | | **$4$** ✓ |

Tres comparaciones $= \lceil \log_2 4 \rceil + 1$.

## 4. Invariante (correctitud parcial)

### 4.1. El primer invariante y por qué no alcanza

El primer intento natural es *"la mediana está en $A[a..] \cup B[b..]$"*. Es verdadero, pero no sirve: no dice qué rango buscar en lo que queda, y no controla cuántos elementos se descartaron por cada lado. Es la lección de la conferencia 3: el invariante tiene que ser inductivo y suficiente. Aquí el refuerzo es exigir **ventanas de igual tamaño**, y entonces el rango buscado es siempre el del medio ($s$), sin desplazamientos que llevar cuenta.

### 4.2. El invariante

> **$I(a, b, s)$.** $s \geq 1$, $0 \leq a$, $a + s \leq n$, $0 \leq b$, $b + s \leq n$, y la celda de rango $n$ en $W(0, 0, n)$ es la celda de rango $s$ en $W(a, b, s)$.

### 4.3. Demostración en tres pasos

**Inicialización.** Con $a = b = 0$ y $s = n$, las dos ventanas son $W(0, 0, n)$ y el enunciado es trivial. ✔

**Mantenimiento.** Supongamos $I(a, b, s)$ con $s \geq 2$ (condición del ciclo). Los índices consultados son válidos: $a + k \leq a + s - 1 < n$ y $b + l \leq b + s - 1 < n$. Como $k + l = s - 2$, el Lema de §2.3 aplica.

- Si `A[a+k] <= B[b+l]` (es decir, $p \prec q$), el algoritmo hace $a \leftarrow a + k + 1$ y $s \leftarrow \lfloor s/2 \rfloor = s - k - 1$, y $b$ no cambia. Por el Lema, la celda de rango $s$ en la ventana vieja es la de rango $s'$ en $W(a+k+1, b, s')$. Los rangos de rango $n$ y $s$ coinciden en la ventana vieja por hipótesis, así que valen $I$ para la ventana nueva. Los límites se mantienen: $(a+k+1) + s' = a + s \leq n$ y $b + s' \leq b + s \leq n$.
- Si no (es decir, $q \prec p$), hace $b \leftarrow b + l + 1$ y $s \leftarrow \lceil s/2 \rceil = k + 1$, y $a$ no cambia. Por el Lema, la celda de rango $s$ es la de rango $s' = k+1$ en $W(a, b+l+1, s')$, y $(b + l + 1) + s' = b + s \leq n$. ✔

**Conclusión.** Al salir, $s = 1$. Por $I$, la celda de rango $n$ en $W(0, 0, n)$ es la de rango $1$ en $W(a, b, 1) = \{A[a], B[b]\}$, que es la menor de las dos, con valor $\min(A[a], B[b])$. Por §2.1, ese valor es $s_n$. ∎

## 5. Terminación y costo

### 5.1. Potencial

$$\Phi(s) = \lceil \log_2 s \rceil.$$

- **Entero y no negativo**, porque $s \geq 1$. Vale $0$ exactamente cuando $s = 1$, que es cuando el ciclo termina.
- **Decrece al menos $1$ por vuelta.** El ciclo solo itera con $s \geq 2$, y entonces $s' \leq \lceil s/2 \rceil$, así que
$$\Phi(s') \leq \lceil \log_2 \lceil s/2 \rceil \rceil = \lceil \log_2 s \rceil - 1.$$

Inicialmente $\Phi = \lceil \log_2 n \rceil$. Por tanto el ciclo hace **a lo sumo $\lceil \log_2 n \rceil$ vueltas** y termina. Junto con la correctitud parcial, **hay correctitud total**.

### 5.2. Costo

Cada vuelta hace **una** comparación entre un elemento de $A$ y uno de $B$ y un número constante de operaciones sobre enteros. Después, una comparación final para el $\min$.

$$\boxed{\ \#\text{comparaciones} \leq \lceil \log_2 n \rceil + 1\ }$$

Tiempo $O(\log n)$ y memoria extra $O(1)$ (los enteros $a$, $b$, $s$). Los arreglos no se copian ni se modifican. Si $n$ es potencia de $2$, $s$ es siempre par hasta llegar a $1$, y cada ejecución cuesta *exactamente* $\log_2 n + 1$ comparaciones.

## 6. Cota de información

**Teorema.** Todo algoritmo de comparaciones que calcula el $n$-ésimo menor de $A \cup B$ hace, en el peor caso, al menos

$$\lceil \log_2 (2n) \rceil = \lceil \log_2 n \rceil + 1$$

comparaciones.

**Demostración.** Restrinjamos las entradas a las que tienen $2n$ valores distintos; una cota para esa subfamilia lo es para el problema. Entonces cada comparación tiene exactamente dos respuestas y la ejecución del algoritmo es un **árbol de decisión binario**.

*Hay $2n$ respuestas posibles.* Para cada celda $A[k]$, $0 \leq k \leq n-1$, existe una entrada en la que es el $n$-ésimo menor: basta que la precedan $A[0..k-1]$ y $B[0..n-k-2]$ (que son $k + (n - k - 1) = n - 1$ celdas) y que el resto sea mayor. Igual para cada $B[k]$. En el modelo de comparaciones la salida es una celda de la entrada, y como los valores son distintos, celdas distintas son respuestas distintas.

*Cada hoja tiene una sola respuesta.* Si dos entradas con respuestas distintas llegaran a la misma hoja, el algoritmo daría la misma salida en ambas y fallaría en una.

Por tanto, el árbol tiene al menos $2n$ hojas. Un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas (conferencia 5), así que $2^h \geq 2n$, es decir, $h \geq \log_2(2n)$, y como $h$ es entero, $h \geq \lceil \log_2 (2n) \rceil = \lceil \log_2 n \rceil + 1$. ∎

**Conclusión.** La cota de información coincide con el costo del algoritmo: el peor caso del problema es **exactamente $\lceil \log_2 n \rceil + 1$** comparaciones y el algoritmo de §3 es **óptimo**, sin factor constante.

### 6.1. Observaciones

**(a) La información cuenta salidas, no entradas.** Hay $\binom{2n}{n} \approx 4^n/\sqrt{\pi n}$ formas de entrelazar los arreglos. Una cota que contara entradas daría $\approx 2n$ comparaciones, que es lo que cuesta *mezclar* (conferencia 5). Pero la mediana no necesita distinguir entradas, solo respuestas, y hay $2n$. Es el principio de la conferencia 5 llevado a su extremo: aquí la información es suficiente y no hace falta adversario.

**(b) Contraste con el ejercicio 6.** En la matriz ordenada la información daba solo $\Omega(\log n)$ y la cota verdadera, $\Omega(n)$, necesitó un adversario. Aquí la información ya es exacta. La diferencia es estructural: en la matriz la antidiagonal era una anticadena que ocultaba $n$ posibilidades independientes; en los dos arreglos, cada comparación $A[a+k]$ vs. $B[b+l]$ con $k + l = s - 2$ parte el espacio de respuestas por la mitad.

**(c) La otra formulación clásica.** Se puede buscar por búsqueda binaria el corte $i \in [0, n]$ tal que $A[i-1] \leq B[n-i]$ y $B[n-i-1] \leq A[i]$ (con centinelas $\mp\infty$); la mediana es $\max(A[i-1], B[n-i-1])$. Cuesta $\lceil \log_2 (n+1) \rceil + 1$ comparaciones: coincide con la cota salvo cuando $n$ es potencia de $2$, donde hace una de más (medido para $n \leq 10$). Eliminar ventanas, como en §3, elimina esa diferencia.

## 7. Experimento

### 7.1. Código

El bloque siguiente continúa el de §3 (usa `mediana`). Comprueba el invariante en cada vuelta, mide el peor caso sobre **todos** los entrelazados posibles y planta un error.

```python
import itertools, random

def mediana_vigilada(A, B):
    """Igual que mediana, pero comprueba I(a,b,s) en cada vuelta."""
    n = len(A)
    objetivo = sorted(A + B)[n - 1]
    a = b = 0
    s = n
    while True:
        assert sorted(A[a:a+s] + B[b:b+s])[s - 1] == objetivo, ("I roto", a, b, s)
        if s == 1:
            return min(A[a], B[b])
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        if A[a + k] <= B[b + l]:
            a += k + 1; s = s // 2
        else:
            b += l + 1; s = (s + 1) // 2

def mediana_mutante(A, B):
    """Error plantado: en la rama else se usa s // 2 en lugar de ceil(s/2)."""
    n = len(A)
    a = b = 0
    s = n
    while s > 1:
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        if A[a + k] <= B[b + l]:
            a += k + 1; s = s // 2
        else:
            b += l + 1; s = s // 2                  # <-- error
    return min(A[a], B[b])

def cuenta(A, B):
    """Comparaciones que hace `mediana` (copia instrumentada)."""
    n = len(A); a = b = 0; s = n; c = 0
    while s > 1:
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        c += 1
        if A[a + k] <= B[b + l]:
            a += k + 1; s = s // 2
        else:
            b += l + 1; s = (s + 1) // 2
    return c + 1

def ceil_log2(x):
    return (x - 1).bit_length()

def desde_patron(n, posA):
    """Entrada con valores 0..2n-1 donde A ocupa las posiciones posA de la mezcla."""
    posA = set(posA)
    A, B = [], []
    for p in range(2 * n):
        (A if p in posA else B).append(p)
    return A, B

# 1) Correctitud exhaustiva con duplicados
total = 0
for n, V in [(1, 4), (2, 4), (3, 4), (4, 4), (5, 3), (6, 2)]:
    for A in itertools.combinations_with_replacement(range(V + 1), n):
        for B in itertools.combinations_with_replacement(range(V + 1), n):
            assert mediana(list(A), list(B)) == sorted(A + B)[n - 1]
            assert cuenta(list(A), list(B)) <= ceil_log2(n) + 1
            total += 1
print("exhaustivo con duplicados:", total, "pares")

# 2) Peor caso medido sobre todos los entrelazados; invariante vigilado para n <= 8
for n in range(1, 13):
    mx, cnt = 0, 0
    for posA in itertools.combinations(range(2 * n), n):
        A, B = desde_patron(n, posA)
        assert mediana(A, B) == n - 1
        if n <= 8:
            assert mediana_vigilada(A, B) == n - 1
        mx, cnt = max(mx, cuenta(A, B)), cnt + 1
    assert mx == ceil_log2(n) + 1
    print(f"n={n:2d}  entrelazados={cnt:8d}  peor caso medido={mx}  cota={ceil_log2(n) + 1}")

# 3) Aleatorio con n grande
random.seed(7)
for _ in range(3000):
    n = random.randint(1, 1000)
    A = sorted(random.randint(0, 400) for _ in range(n))
    B = sorted(random.randint(0, 400) for _ in range(n))
    assert mediana(A, B) == sorted(A + B)[n - 1] and cuenta(A, B) <= ceil_log2(n) + 1

# 4) El mutante
for n in range(1, 11):
    f = sum(1 for posA in itertools.combinations(range(2 * n), n)
            if mediana_mutante(*desde_patron(n, posA)) != n - 1)
    print(f"mutante n={n:2d}: {f} fallos de {len(list(itertools.combinations(range(2 * n), n)))}")

random.seed(2026)
for n in (8, 16, 32, 64, 7, 9, 31, 33):
    ens = 5000
    f = 0
    for _ in range(ens):
        A = sorted(random.randint(0, 999) for _ in range(n))
        B = sorted(random.randint(0, 999) for _ in range(n))
        f += mediana_mutante(A, B) != sorted(A + B)[n - 1]
    print(f"mutante aleatorio n={n:2d}: {f}/{ens}")
```

### 7.2. Resultados (ejecutado)

| Comprobación | Casos | Resultado |
|---|---|---|
| Correctitud y $\leq \lceil \log_2 n \rceil + 1$ comparaciones, con duplicados | 10 295 pares de arreglos ($n \leq 6$) | se cumple en todos |
| Invariante $I(a,b,s)$ vigilado en cada vuelta | todos los entrelazados, $n \leq 8$ | nunca se rompe |
| Aleatorio con $n \leq 1000$ | 3000 pares | correcto y dentro de la cota |

Peor caso medido sobre **todos** los entrelazados:

| $n$ | Entrelazados $\binom{2n}{n}$ | Peor caso medido | $\lceil \log_2 n \rceil + 1$ |
|---|---|---|---|
| 1 | 2 | 1 | 1 |
| 2 | 6 | 2 | 2 |
| 3 | 20 | 3 | 3 |
| 4 | 70 | 3 | 3 |
| 5 | 252 | 4 | 4 |
| 6 | 924 | 4 | 4 |
| 7 | 3 432 | 4 | 4 |
| 8 | 12 870 | 4 | 4 |
| 9 | 48 620 | 5 | 5 |
| 10 | 184 756 | 5 | 5 |
| 11 | 705 432 | 5 | 5 |
| 12 | 2 704 156 | 5 | 5 |

El costo medido coincide con la cota de información en todos los $n$ probados.

### 7.3. Una variante con error plantado

Como en las conferencias 2 a 5, plantamos un error en una variante que parece correcta: en la rama `else`, usar `s // 2` en lugar de $\lceil s/2 \rceil$. Con $s$ par no hay diferencia; con $s$ impar, la ventana de $A[a..a+k]$ ($k+1 = \lceil s/2 \rceil$ celdas) queda recortada en una celda, que puede ser justo la mediana.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Fallos (de $\binom{2n}{n}$ entrelazados) | 0 | 0 | 16 | **0** | 186 | 567 | 3424 | **0** | 33 130 | 98 318 |

En pruebas aleatorias:

| $n$ | 8 | 16 | 32 | 64 | 7 | 9 | 31 | 33 |
|---|---|---|---|---|---|---|---|---|
| Fallos (de 5000) | **0** | **0** | **0** | **0** | 4974 | 3363 | 4965 | 2852 |

Una suite que pruebe solo con $n = 2^k$ (la elección más natural al medir $\log n$) no ve ningún fallo, porque con $n$ potencia de $2$ todas las ventanas tienen tamaño par hasta el caso base y $\lfloor s/2 \rfloor = \lceil s/2 \rceil$ siempre. La demostración dice dónde mirar: el caso 2 del Lema exige $s' = k + 1 = \lceil s/2 \rceil$, y es exactamente el paso que la variante rompe.

## 8. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Hallar $s_n$, el $n$-ésimo menor de $A \cup B$, con $A$ y $B$ ordenados de largo $n$. Modelo: comparaciones entre un elemento de $A$ y uno de $B$. |
| ¿Qué algoritmo? | Eliminar ventanas: comparar $A[a+k]$ con $B[b+l]$, $k + l = s - 2$, y descartar $k+1$ celdas por debajo y $k+1$ por encima de la mediana. |
| ¿Es correcto? | **Invariante** $I(a,b,s)$: la celda de rango $n$ de la mezcla es la de rango $s$ en las ventanas $A[a..a+s-1] \cup B[b..b+s-1]$ (de igual tamaño). **Potencial**: $\lceil \log_2 s \rceil$. |
| ¿Cuánto cuesta? | $\lceil \log_2 n \rceil + 1$ comparaciones, $O(\log n)$ en tiempo y $O(1)$ en memoria. |
| ¿Se puede mejor? | No: **cota de información**, $2n$ respuestas $\Rightarrow$ $\lceil \log_2 (2n) \rceil = \lceil \log_2 n \rceil + 1$. Coincide exactamente con el algoritmo. |
