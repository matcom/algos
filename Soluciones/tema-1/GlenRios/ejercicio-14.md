# Problema 14 ★★★

**Enunciado.** Dado un arreglo $A[0..n-1]$ de enteros no negativos, devolver el **MEX** de $A$: el menor entero no negativo que **no** aparece en $A$. Se permite usar solo $O(1)$ memoria extra además de la entrada.

## Algoritmo

La idea es que el MEX está en $[0, n]$. Cualquier valor fuera de ese rango es irrelevante, y cualquier valor $v \in [0, n)$ que aparezca en $A$ puede colocarse en la posición $v$ mediante intercambios. Después de "normalizar" el arreglo de esta forma, el MEX es simplemente el primer índice $i$ con $A[i] \neq i$ (o $n$ si todos los valores $0..n-1$ están presentes).

```
mex(A):
    n ← len(A)
    i ← 0
    while i < n:
        v ← A[i]
        if 0 ≤ v < n and A[v] ≠ v:
            swap(A[i], A[v])
        else:
            i ← i + 1
    for i from 0 to n-1:
        if A[i] ≠ i:
            return i
    return n
```

El primer bucle coloca cada valor $v \in [0, n)$ en la posición $v$ siempre que no esté ya ahí. El segundo bucle busca el primer índice que no coincide.

## Terminación

En lugar de un invariante complicado, usamos un potencial que cuenta cuántos valores ya están en su posición correcta:

$$
\Phi = \bigl|\{\,j \in [0, n) : A[j] = j\,\}\bigr|.
$$

Claramente $0 \le \Phi \le n$.

**Lema.** Cada swap incrementa $\Phi$ en al menos 1.

*Demostración.* En un swap, $v = A[i]$ con $0 \le v < n$ y $A[v] \neq v$. Después del swap, $A[v] = v$, así que la posición $v$ pasa a estar fija y $\Phi$ aumenta en al menos 1. La posición $i$ puede también pasar a estar fija (si el valor que estaba en $A[v]$ era justamente $i$), pero nunca deja de estarlo, porque antes del swap $A[i] = v \neq i$. Por tanto $\Phi$ aumenta estrictamente. $\square$

**Lema.** El primer bucle ejecuta a lo sumo $2n$ iteraciones.

*Demostración.* Cada iteración o bien hace un swap (a lo sumo $n$ en total, por el lema anterior y $\Phi \le n$) o bien incrementa $i$ (a lo sumo $n$ veces). $\square$

## Correctitud

Al salir del primer bucle se cumple la negación de la condición del bucle: para todo $i \in [0, n)$,

$$
A[i] \notin [0, n) \quad \text{o bien} \quad A[A[i]] = A[i].
\tag{$\ast$}
$$

**Lema.** Si $v \in [0, n)$ aparece en $A$, entonces $A[v] = v$.

*Demostración.* Sea $j$ una posición con $A[j] = v$. Como $v \in [0, n)$, se tiene $A[j] \in [0, n)$, así que por $(\ast)$ aplicado a $i = j$:
$$
A[A[j]] = A[j] \;\Longrightarrow\; A[v] = v. \qquad \square
$$

Con esto ya podemos demostrar que el segundo bucle devuelve el MEX.

**Teorema.** El algoritmo devuelve el MEX de $A$.

*Demostración.* Sea $i^\ast$ el valor devuelto por el segundo bucle.

**Caso 1: $i^\ast < n$.** Entonces $A[i^\ast] \neq i^\ast$. Por el lema, $i^\ast$ no puede aparecer en $A$ (si apareciera, tendríamos $A[i^\ast] = i^\ast$, contradicción). Además, para todo $j < i^\ast$ se tiene $A[j] = j$ por minimalidad de $i^\ast$, así que cada $j < i^\ast$ aparece en $A$ (en la posición $j$). Por lo tanto $i^\ast$ es el menor no negativo que no aparece en $A$: es el MEX.

**Caso 2: $i^\ast = n$.** Entonces $A[i] = i$ para todo $i \in [0, n)$. En particular, todos los valores $0, 1, \ldots, n-1$ aparecen en $A$, así que el MEX es $n$. $\square$

## Costo

- Primer bucle: a lo sumo $n$ swaps y $n$ incrementos de $i$, cada uno $O(1)$. Total $O(n)$.
- Segundo bucle: $n$ iteraciones, cada una $O(1)$. Total $O(n)$.
- Memoria extra: $O(1)$ (solo variables escalares: $i$, $v$, $n$).
- **Costo total:** $O(n)$ tiempo, $O(1)$ memoria extra.

## Cota mínima

**Teorema.** Cualquier algoritmo que resuelva MEX necesita $\Omega(n)$ tiempo en el modelo word RAM.

*Demostración (adversario).* Supongamos que un algoritmo $\mathcal{A}$ resuelve MEX y que existe una posición $i$ que nunca lee. Construimos dos entradas que solo difieren en la posición $i$ y que $\mathcal{A}$ no puede distinguir, pero cuyos MEX son distintos.

Tomemos $X$ con $A[i] = 0$ y $A[j] = 1$ para todo $j \neq i$. El MEX de $X$ es $2$, porque $0$ y $1$ aparecen, y $2$ no.

Tomemos $X'$ con $A[i] = 2$ y $A[j] = 1$ para todo $j \neq i$. El MEX de $X'$ es $0$, porque $0$ no aparece.

Como $\mathcal{A}$ no lee la posición $i$, ve el mismo contenido en ambas entradas y produce la misma respuesta. Pero las respuestas correctas son distintas. Contradicción. Por lo tanto $\mathcal{A}$ debe leer las $n$ posiciones, lo que requiere $\Omega(n)$ operaciones. $\square$
