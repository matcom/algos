## 1. Planteamiento formal

Dado un arreglo $A$ de $n$ elementos, se desea devolver todos los $x$ tales que

$$
\operatorname{frequency}(x,A) > \frac{n}{3}.
$$

Puede haber como máximo dos elementos de este tipo. Si existieran tres elementos distintos $x_1,x_2,x_3$ con frecuencias $f_1,f_2,f_3$, entonces

$$
f_1+f_2+f_3 > \frac{n}{3}+\frac{n}{3}+\frac{n}{3}=n,
$$

lo cual es imposible porque la suma de las frecuencias no puede exceder $n$. Por tanto, mantener dos candidatos es suficiente.

## 2. Algoritmo de Boyer–Moore generalizado

Se mantienen dos candidatos $c_1,c_2$ y dos contadores $\texttt{count1},\texttt{count2}$.

```python
def majority_third(A):
    candidate1 = None
    candidate2 = None
    count1 = 0
    count2 = 0

    for x in A:
        if count1 > 0 and x == candidate1:
            count1 += 1
        elif count2 > 0 and x == candidate2:
            count2 += 1
        elif count1 == 0:
            candidate1 = x
            count1 = 1
        elif count2 == 0:
            candidate2 = x
            count2 = 1
        else:
            count1 -= 1
            count2 -= 1

    return candidate1, candidate2
```

## 3. Invariante reforzada

Sea $A[0:i]$ el prefijo procesado tras $i$ iteraciones. El multiconjunto de elementos de $A[0:i]$ se puede particionar como

$$
A[0:i]
=
T_1 \uplus T_2 \uplus \cdots \uplus T_k
\uplus
\{ c_1^{(\texttt{count1})}, c_2^{(\texttt{count2})} \},
$$

donde cada $T_j$ contiene tres elementos mutuamente distintos y $\uplus$ denota unión de multiconjuntos.

La prueba es por inducción. El caso base es el prefijo vacío. En el paso inductivo, si el nuevo elemento coincide con $c_1$ o $c_2$, se incrementa el contador correspondiente. Si ambos contadores son positivos y el nuevo elemento $x$ no coincide con ninguno, entonces $c_1,c_2,x$ son tres elementos distintos y se agrupan en un nuevo $T_{k+1}$, decrementando ambos contadores. Así se preserva el invariante.

## 4. Correcitud

Sea $x$ tal que

$$
f(x) > \frac{n}{3}.
$$

Por el invariante, la entrada se descompone en $k$ grupos de tres elementos mutuamente distintos y las copias restantes de los candidatos. Como cada grupo tiene tres elementos,

$$
3k \le n \quad\Rightarrow\quad k \le \frac{n}{3}.
$$

Cada grupo puede contener como máximo una aparición de $x$. Por tanto, como máximo $k$ apariciones de $x$ pueden quedar eliminadas en grupos de tres. Pero

$$
f(x) > \frac{n}{3} \ge k.
$$

Luego al menos una aparición de $x$ permanece fuera de esos grupos. Según el invariante, los elementos restantes solo pueden ser copias de los dos candidatos. Por tanto,

$$
f(x) > \frac{n}{3} \implies x \in \{\texttt{candidate1}, \texttt{candidate2}\}.
$$

## 5. Complejidad

Cada elemento se procesa una sola vez y cada iteración realiza una cantidad constante de operaciones. Por tanto,

$$
T(n)=\Theta(n).
$$

El algoritmo usa dos candidatos y dos contadores independientemente de $n$, así que

$$
S(n)=\Theta(1).
$$

Además, en el modelo determinista estándar, cualquier algoritmo exacto debe inspeccionar cada elemento en el peor caso, por lo que una cota inferior es

$$
\Omega(n).
$$

Así, el algoritmo es asintóticamente óptimo.

## 6. Versión sin verificación y falsos positivos

```python
def majority_third_candidates(A):
    candidate1 = None
    candidate2 = None
    count1 = 0
    count2 = 0

    for x in A:
        if count1 > 0 and x == candidate1:
            count1 += 1
        elif count2 > 0 and x == candidate2:
            count2 += 1
        elif count1 == 0:
            candidate1 = x
            count1 = 1
        elif count2 == 0:
            candidate2 = x
            count2 = 1
        else:
            count1 -= 1
            count2 -= 1

    result = []
    if count1 > 0:
        result.append(candidate1)
    if count2 > 0:
        result.append(candidate2)
    return result
```

Se garantiza

$$
\text{Elementos mayoritarios reales} \subseteq \text{Candidatos devueltos},
$$

pero no la igualdad. Por ejemplo, con

$$
A=[a,b,c,d],
$$

el algoritmo devuelve $\{d\}$, pero

$$
f(d)=1 \not> \frac{4}{3}.
$$

Por eso se requiere una segunda pasada de verificación si se necesita la respuesta exacta.

## 7. Generador de casos de prueba

Un generador simple es

$$
G_{\text{miss}}(n)=\{ [x]^n : x \in \{1,\dots,m\} \}.
$$

En Python:

```python
def gen_miss(n, m):
    return [[x] * n for x in range(1, m + 1)]
```

Para $n=5$ y $m=3$:

```python
[[1, 1, 1, 1, 1],
 [2, 2, 2, 2, 2],
 [3, 3, 3, 3, 3]]
```

Este generador no detecta el bug porque en toda entrada $A=[x]^n$ el algoritmo hace que $x$ sea $\texttt{candidate1}$ desde la primera iteración, incrementa $\texttt{count1}$ en todas las siguientes y nunca ejecuta la rama que decrementa ambos contadores. Al final,

$$
\texttt{count1}=n>0, \qquad \texttt{count2}=0,
$$

y devuelve $[x]$. Como

$$
\operatorname{frequency}(x,A)=n > \frac{n}{3},
$$

la salida es correcta. Por eso este generador no ejercita los casos interesantes del algoritmo: dos candidatos, empates o la rama $\texttt{else}$.
