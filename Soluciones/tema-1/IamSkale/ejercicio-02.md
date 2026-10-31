# Ejercicio 2 ★ — Búsqueda binaria: invariante, potencial y cota de información (C3, C5)

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

## Especificación

- **Precondición:** $A[0..n-1]$ ordenado crecientemente ($a_0<a_1<\dots<a_{n-1}$), $x$ un valor.
- **Postcondición:** devuelve `("está", m)` con $A[m]=x$, o `("hueco", lo)` si $x$ no está, donde `lo` es el número de elementos menores que $x$ (el hueco en el que cae $x$).
- **Modelo:** comparaciones de $x$ con elementos del arreglo, con respuesta $<$, $=$ o $>$.

## Algoritmo

La función `busqueda_binaria(A, x, comparar)` mantiene el rango `[lo, hi)` donde puede estar $x$. En cada vuelta compara $x$ con el elemento del medio `A[m]`: si son iguales devuelve su posición; si $x$ es menor sigue por la mitad izquierda (`hi = m`) y si es mayor por la derecha (`lo = m + 1`). Si el rango se vacía, devuelve el número de hueco `lo` donde caería $x$. Las comparaciones pasan por la función `comparar` para poder contarlas en las pruebas.

> Código: [ejercicio-02.py](ejercicio-02.py), parte 1.

## Invariante (correctitud parcial)

Usamos la versión reforzada, que además de decir dónde puede estar $x$ dice en qué hueco cae:

$$I:\quad 0\le lo\le hi\le n,\qquad A[j]<x \text{ para todo } j<lo,\qquad A[j]>x \text{ para todo } j\ge hi.$$

$I$ implica la versión débil: "si $x$ está en $A$, está en $A[lo:hi]$".

- **Inicialización.** $lo=0$, $hi=n$: las dos condiciones hablan de conjuntos vacíos.
- **Mantenimiento.** Sea $m=\lfloor(lo+hi)/2\rfloor$. Como $lo<hi$, $lo\le m<hi$.
  - Si $x=A[m]$, se devuelve $m$, que es correcto.
  - Si $x<A[m]$: para todo $j\ge m$, $A[j]\ge A[m]>x$ por el orden, y se hace $hi=m$. La condición sobre $hi$ se cumple y la de $lo$ no cambió.
  - Si $x>A[m]$: para todo $j\le m$, $A[j]\le A[m]<x$, y se hace $lo=m+1$. Simétrico.
- **Conclusión.** El ciclo sale con $lo\ge hi$, y con $lo\le hi$ eso da $lo=hi$. Todo $A[j]$ con $j<lo$ es menor que $x$ y todo $A[j]$ con $j\ge lo$ es mayor, así que $x$ no está y cae en el hueco $lo$. La salida `("hueco", lo)` es correcta.

## Potencial (terminación y costo)

$$\Phi = hi-lo .$$

Es un entero, y dentro del ciclo $\Phi\ge1$. Con $m=lo+\lfloor\Phi/2\rfloor$:

- si $hi\leftarrow m$: $\Phi' = \lfloor\Phi/2\rfloor$;
- si $lo\leftarrow m+1$: $\Phi'=\Phi-\lfloor\Phi/2\rfloor-1=\lceil\Phi/2\rceil-1\le\lfloor\Phi/2\rfloor$.

En los dos casos $\Phi'\le\lfloor\Phi/2\rfloor<\Phi$: el potencial baja estrictamente, así que el ciclo **termina**. Además, $\Phi$ como mínimo se divide por 2, así que después de $k$ vueltas $\Phi\le\lfloor n/2^k\rfloor$. El ciclo no puede dar más de $\lfloor\log_2 n\rfloor+1=\lceil\log_2(n+1)\rceil$ vueltas.

**Costo:** a lo sumo $\lceil\log_2(n+1)\rceil$ comparaciones, $O(\log n)$ tiempo y $O(1)$ memoria.

## Cota de información (optimalidad)

**Teorema.** Todo algoritmo de comparaciones que busca $x$ en un arreglo ordenado de $n$ elementos hace, en el peor caso, al menos $\lceil\log_2(n+1)\rceil$ comparaciones.

1. Si $x$ no está, cae en uno de los $n+1$ huecos $h_0,\dots,h_n$ (antes de $a_0$, entre $a_0$ y $a_1$, …, después de $a_{n-1}$).
2. Sobre esas entradas ninguna comparación responde "$=$", así que solo se usan dos ramas: es la parte binaria del árbol de decisión.
3. **Dos huecos distintos llevan a hojas distintas.** Si $x_1$ y $x_2$ caen en huecos distintos con $x_1<x_2$, hay un $a_i$ con $x_1<a_i<x_2$. Si los dos llegan a la misma hoja, el algoritmo nunca comparó con $a_i$ (habría separado los caminos). Entonces $x=a_i$ recibe las mismas respuestas que $x_1$ en todas las comparaciones, llega a la misma hoja y el algoritmo dice "no está", que es falso.
4. Un árbol binario con $n+1$ hojas tiene altura $\ge\log_2(n+1)$. Como la altura es entera, $\ge\lceil\log_2(n+1)\rceil$.

La búsqueda binaria hace exactamente $\lceil\log_2(n+1)\rceil$ en el peor caso: **es óptima**.

## Casos de prueba y validación

Herramientas de prueba: `Contador`, un comparador que devuelve $-1$, $0$ o $1$ y lleva la cuenta de las comparaciones hechas, y `oraculo`, que da la respuesta correcta por un camino independiente (`list.index` y `bisect`). Esta parte no imprime nada.

> Código: [ejercicio-02.py](ejercicio-02.py), parte 2.

**Prueba exhaustiva** para $n\le 64$: todos los valores presentes y un valor en cada hueco.

> Código: [ejercicio-02.py](ejercicio-02.py), parte 3.

```text
correcta en todos los casos, y el peor caso es exactamente ceil(log2(n+1)) para n = 0..64
```

**Invariante y potencial vigilados** en cada vuelta (como el "invariante vigilado" de la C3 §4):

> Código: [ejercicio-02.py](ejercicio-02.py), parte 4.

```text
invariante y potencial comprobados en 3000 búsquedas al azar
```

**La cota de información en números:** peor caso de la búsqueda binaria contra $\lceil\log_2(n+1)\rceil$.

> Código: [ejercicio-02.py](ejercicio-02.py), parte 5.

```text
     n  huecos  peor caso medido  ceil(log2(n+1))
     1       2                 1                1
     7       8                 3                3
     8       9                 4                4
   100     101                 7                7
  1000    1001                10               10
100000  100001                17               17
```

**El error que el potencial detecta** (ejercicio 7 de la C3): cambiar `lo = m + 1` por `lo = m`. Cuando $hi-lo=1$ y $x>A[lo]$, $m=lo$ y el potencial no baja: el ciclo no termina.

> Código: [ejercicio-02.py](ejercicio-02.py), parte 6.

```text
no termina   <- con A = [10], x = 20: lo=0, hi=1, m=0 y lo no se mueve
```

## Resumen

| | |
|---|---|
| Invariante | $A[0:lo]<x<A[hi:n]$ (implica "si $x$ está, está en $A[lo:hi]$") |
| Potencial | $\Phi=hi-lo$, entero, $\ge1$ en el ciclo, y al menos se divide por 2 en cada vuelta |
| Costo | $\le\lceil\log_2(n+1)\rceil$ comparaciones, memoria $O(1)$ |
| Cota mínima | $\lceil\log_2(n+1)\rceil$, por información: $n+1$ huecos necesitan $n+1$ hojas en un árbol binario |
| Conclusión | la búsqueda binaria es óptima en el modelo de comparaciones |
