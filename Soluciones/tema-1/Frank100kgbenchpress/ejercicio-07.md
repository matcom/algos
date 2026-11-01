# Ejercicio 7: Mediana de dos arreglos ordenados de largo \(n\)

**Enunciado:** Mediana de dos arreglos ordenados de largo \(n\): el \(n\)-ésimo menor de los \(2n\) elementos. Diseña un algoritmo \(O(\log n)\), demuestra su correctitud y da la cota de información. (C2, C3, C5)

**Modelo:** Árboles de decisión por comparaciones. Tenemos dos arreglos \(A\) y \(B\), ambos de tamaño \(n\), ordenados de forma creciente. Queremos encontrar el \(n\)-ésimo elemento más pequeño de la unión de ambos (la mediana inferior).

---

## 1. Algoritmo propuesto (Partición binaria)

En lugar de mezclar los dos arreglos, lo cual tomaría \(O(n)\), utilizamos una búsqueda binaria sobre el punto de partición del arreglo \(A\).

La idea consiste en dividir ambos arreglos en dos mitades, izquierda y derecha, de forma que:

1. La mitad izquierda contenga exactamente \(n\) elementos.
2. Todos los elementos de la mitad izquierda sean menores o iguales que todos los elementos de la mitad derecha.

Si conseguimos esta partición, la mediana será el máximo elemento de la mitad izquierda.

```python
def mediana_dos_arreglos(A, B):
    n = len(A)
    low = 0
    high = n

    while low <= high:
        # Cantidad de elementos de A en la mitad izquierda
        i = (low + high) // 2

        # Cantidad de elementos de B en la mitad izquierda
        j = n - i

        # Elementos en los bordes de la partición
        A_izq = A[i-1] if i > 0 else float('-inf')
        A_der = A[i] if i < n else float('inf')

        B_izq = B[j-1] if j > 0 else float('-inf')
        B_der = B[j] if j < n else float('inf')

        # Comprobamos si la partición es válida
        if A_izq <= B_der and B_izq <= A_der:
            return max(A_izq, B_izq)

        elif A_izq > B_der:
            # Hay demasiados elementos de A en la izquierda
            high = i - 1

        else:
            # Hay muy pocos elementos de A en la izquierda
            low = i + 1

    raise RuntimeError("No se encontró una partición válida")
```

El último `raise` es una protección: con dos arreglos válidos, ordenados y de igual tamaño, siempre existe una partición válida, por lo que esa instrucción no debería ejecutarse.

### Análisis del costo

El intervalo inicial de búsqueda tiene \(n+1\) posiciones posibles:

\[
i\in\{0,1,\ldots,n\}
\]

En cada iteración, la búsqueda binaria elimina aproximadamente la mitad de las posiciones posibles.

Por tanto, el número de iteraciones está acotado por:

\[
O(\log_2(n+1))
\]

En cada iteración se realizan una cantidad constante de comparaciones y operaciones elementales.

Por tanto:

\[
\boxed{T(n)=O(\log n)}
\]

El algoritmo solamente utiliza índices y variables auxiliares, sin crear estructuras adicionales:

\[
\boxed{S(n)=O(1)}
\]

---

## 2. Correctitud (Invariante)

Para demostrar la correctitud del algoritmo, definimos el siguiente invariante:

**Invariante:** Al inicio de cada iteración del ciclo `while`, existe al menos un índice de partición válido \(i^*\) dentro del intervalo \([low,high]\), tal que, definiendo \(j^*=n-i^*\), se cumplen las dos condiciones:

\[
A[i^*-1]\leq B[j^*]
\]

\[
B[j^*-1]\leq A[i^*]
\]

Los elementos inexistentes en los extremos se interpretan mediante los valores centinela \(-\infty\) y \(+\infty\).

Estas dos condiciones garantizan que los \(n\) elementos de la mitad izquierda son menores o iguales que los \(n\) elementos de la mitad derecha.

### Demostración del invariante

La demostración se realiza mediante los tres pasos habituales:

**1. Inicialización:**

Al comienzo:

\[
low=0,\qquad high=n
\]

Por tanto, el intervalo contiene todas las particiones posibles:

\[
[0,n]
\]

Como los dos arreglos están ordenados, siempre existe una partición que coloca los \(n\) elementos más pequeños en la mitad izquierda y los \(n\) restantes en la mitad derecha.

Si \(i^*\) es la cantidad de elementos de \(A\) entre los primeros \(n\) elementos de la unión, entonces:

\[
j^*=n-i^*
\]

Esta partición cumple las dos condiciones del invariante.

Por tanto, inicialmente existe una partición válida dentro de \([low,high]\).

**2. Mantenimiento:**

En cada iteración calculamos:

\[
i=\left\lfloor\frac{low+high}{2}\right\rfloor
\]

\[
j=n-i
\]

Analizamos las condiciones de la partición.

- **Caso 1: \(A[i-1]>B[j]\).**

  Esto significa que el último elemento de la mitad izquierda de \(A\) es mayor que el primer elemento de la mitad derecha de \(B\).

  Por tanto, hay demasiados elementos de \(A\) en la mitad izquierda y debemos reducir \(i\).

  Además, debido al orden de los arreglos, para cualquier partición \(k\geq i\):

  \[
  A[k-1]\geq A[i-1]
  \]

  \[
  B[n-k]\leq B[n-i]
  \]

  Por tanto:

  \[
  A[k-1]>B[n-k]
  \]

  Ninguna partición con \(k\geq i\) puede ser válida.

  En consecuencia, cualquier partición válida debe estar a la izquierda de \(i\). Actualizamos:

  \[
  high=i-1
  \]

  El invariante se conserva.

- **Caso 2: \(B[j-1]>A[i]\).**

  Esto significa que el último elemento de la mitad izquierda de \(B\) es mayor que el primer elemento de la mitad derecha de \(A\).

  Por tanto, hay pocos elementos de \(A\) en la mitad izquierda y debemos aumentar \(i\).

  Debido al orden de los arreglos, para cualquier partición \(k\leq i\):

  \[
  B[n-k-1]\geq B[n-i-1]
  \]

  \[
  A[k]\leq A[i]
  \]

  Por tanto:

  \[
  B[n-k-1]>A[k]
  \]

  Ninguna partición con \(k\leq i\) puede ser válida.

  En consecuencia, cualquier partición válida debe estar a la derecha de \(i\). Actualizamos:

  \[
  low=i+1
  \]

  El invariante también se conserva.

- **Caso 3: Se cumplen ambas condiciones.**

  Si:

  \[
  A[i-1]\leq B[j]
  \]

  y:

  \[
  B[j-1]\leq A[i]
  \]

  hemos encontrado una partición válida.

  Como cada arreglo está ordenado internamente, estas condiciones garantizan que todos los elementos de la mitad izquierda son menores o iguales que todos los de la mitad derecha.

  La mitad izquierda contiene exactamente \(n\) elementos, por lo que el \(n\)-ésimo menor es el máximo de dicha mitad:

  \[
  \boxed{\text{Mediana}=\max(A[i-1],B[j-1])}
  \]

  El algoritmo devuelve este valor correctamente.

**3. Terminación:**

En cada iteración se reduce el intervalo de búsqueda eliminando al menos la posición actual \(i\).

Por tanto, el intervalo \([low,high]\) disminuye hasta que se encuentra una partición válida.

Como el invariante garantiza que siempre existe al menos una partición válida dentro del intervalo mientras el algoritmo continúa ejecutándose, no es posible que el intervalo quede vacío.

Por tanto, el algoritmo necesariamente encuentra una partición válida y termina devolviendo la mediana correcta.

---

## 3. Cota de información (Conferencia 5)

Para demostrar que el algoritmo es óptimo, utilizamos la teoría de la información y los árboles de decisión por comparaciones.

Consideramos instancias con elementos distintos, lo cual es suficiente para establecer una cota inferior en el peor caso.

**1. El modelo:**

El algoritmo obtiene información comparando elementos de los arreglos \(A\) y \(B\).

Como consideramos elementos distintos, cada comparación tiene dos resultados posibles:

- El primer elemento es menor que el segundo.
- El primer elemento es mayor que el segundo.

Por tanto, las comparaciones generan un árbol de decisión binario.

**2. Cantidad de resultados posibles:**

El elemento que ocupa la posición \(n\)-ésima de la unión puede ser cualquiera de los \(2n\) elementos de los arreglos.

Es decir, la mediana puede corresponder a:

\[
A[0],A[1],\ldots,A[n-1]
\]

o a:

\[
B[0],B[1],\ldots,B[n-1]
\]

Todos estos casos son posibles. Para cualquier elemento de uno de los arreglos, podemos construir una intercalación de ambos arreglos ordenados en la que ese elemento ocupe la posición \(n\)-ésima.

Por tanto, existen al menos \(2n\) resultados distintos que el algoritmo debe ser capaz de distinguir.

**3. Cota de información:**

Un árbol de decisión binario de altura \(h\) puede tener como máximo:

\[
2^h
\]

hojas.

Como necesitamos distinguir al menos \(2n\) posibles elementos que pueden ser la mediana, debe cumplirse:

\[
2^h\geq2n
\]

Tomando logaritmo en base 2:

\[
h\geq\log_2(2n)
\]

Por tanto:

\[
\boxed{h=\Omega(\log n)}
\]

Esto significa que cualquier algoritmo basado en comparaciones necesita al menos un número de comparaciones del orden de \(\log n\) en el peor caso.

### Conclusión sobre la optimalidad

Nuestro algoritmo realiza:

\[
O(\log n)
\]

comparaciones, mientras que la cota de información establece que cualquier algoritmo necesita:

\[
\Omega(\log n)
\]

Por tanto:

\[
\boxed{T(n)=\Theta(\log n)}
\]

El algoritmo de partición binaria es asintóticamente óptimo para encontrar la mediana inferior de dos arreglos ordenados de igual tamaño.

---

## 4. Conclusión

La estrategia de partición binaria permite encontrar el \(n\)-ésimo elemento más pequeño de dos arreglos ordenados sin necesidad de mezclarlos completamente.

El invariante garantiza que siempre existe una partición válida dentro del intervalo de búsqueda, mientras que las comparaciones permiten determinar hacia qué lado debe desplazarse el punto de partición.

La cota de información demuestra que cualquier algoritmo basado en comparaciones necesita \(\Omega(\log n)\) en el peor caso.

Por tanto, el algoritmo propuesto alcanza la complejidad óptima:

\[
\boxed{T(n)=\Theta(\log n)}
\]

y utiliza espacio auxiliar constante:

\[
\boxed{S(n)=O(1)}
\]