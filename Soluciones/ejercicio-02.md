# Ejercicio 2: Invariante, potencial y cota de información de la búsqueda binaria

**Enunciado:** Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima. (C3, C5)

**Modelo:** Búsqueda en un arreglo ordenado de tamaño \(n\) usando comparaciones.

---

## 1. El algoritmo

Para fijar la notación, consideramos la búsqueda binaria sobre un arreglo ordenado de forma creciente y con índices que comienzan en cero.

```python
def busqueda_binaria(A, x):
    bajo = 0
    alto = len(A) - 1

    while bajo <= alto:
        medio = (bajo + alto) // 2

        if A[medio] == x:
            return medio
        elif A[medio] < x:
            bajo = medio + 1
        else:
            alto = medio - 1

    return -1  # No encontrado
```

---

## 2. Invariante (Conferencia 3)

Para demostrar la correctitud del algoritmo utilizamos un **invariante de ciclo** que establece qué información se conserva al comienzo de cada iteración.

**Invariante:** Al inicio de cada iteración del ciclo `while`, todos los elementos que están a la izquierda del intervalo de búsqueda son estrictamente menores que \(x\), y todos los elementos que están a la derecha son estrictamente mayores que \(x\).

De forma equivalente, si \(x\) se encuentra en el arreglo, entonces al menos una de sus posiciones debe pertenecer al intervalo cerrado \([bajo, alto]\).

### Demostración del invariante

La demostración se realiza mediante los tres pasos habituales:

**1. Inicialización:**

Antes de la primera iteración:

\[
bajo = 0,\qquad alto = n-1
\]

El intervalo de búsqueda comprende todo el arreglo. No existen elementos descartados, por lo que el invariante se cumple inicialmente.

**2. Mantenimiento:**

Sea:

\[
m = \left\lfloor \frac{bajo+alto}{2} \right\rfloor
\]

En cada iteración se compara \(A[m]\) con \(x\).

- Si \(A[m] < x\), como el arreglo está ordenado de forma creciente, todos los elementos de las posiciones comprendidas entre `bajo` y \(m\) son menores que \(x\). Por tanto, ninguno puede contener el valor buscado. Se actualiza:

  \[
  bajo = m+1
  \]

  El intervalo de búsqueda se desplaza hacia la derecha y el invariante se conserva.

- Si \(A[m] > x\), debido al orden del arreglo, todos los elementos desde \(m\) hasta `alto` son mayores que \(x\). Por tanto, ninguno puede contener el valor buscado. Se actualiza:

  \[
  alto = m-1
  \]

  El intervalo se desplaza hacia la izquierda y el invariante también se conserva.

- Si \(A[m] = x\), el algoritmo encuentra el elemento y devuelve su índice, por lo que la respuesta es correcta.

**3. Terminación:**

El ciclo termina cuando:

\[
bajo > alto
\]

Esto significa que el intervalo de búsqueda está vacío. Por el invariante, si \(x\) estuviera en el arreglo, tendría que encontrarse dentro de ese intervalo. Como no quedan posiciones por examinar, se concluye que \(x\) no pertenece al arreglo y se devuelve \(-1\).

Por tanto, el invariante demuestra que el algoritmo devuelve un índice válido cuando encuentra \(x\), y que devuelve \(-1\) cuando el elemento no está presente.

---

## 3. Potencial (Conferencia 3)

Para demostrar la terminación y analizar la cantidad de iteraciones, utilizamos una función de potencial que mida el tamaño del intervalo de búsqueda.

Definimos:

\[
\Phi = alto - bajo + 1
\]

Esta función representa la cantidad de elementos que todavía pueden contener el valor buscado.

### Análisis del potencial

**1. Inicialización:**

Al comienzo del algoritmo, el intervalo comprende los \(n\) elementos del arreglo. Por tanto:

\[
\Phi_0 = n
\]

**2. Decremento:**

En cada iteración se calcula:

\[
m = \left\lfloor \frac{bajo+alto}{2} \right\rfloor
\]

Si el elemento buscado no se encuentra en la posición central, se descarta esa posición y una de las dos mitades del intervalo.

- Si \(A[m] < x\), el nuevo tamaño del intervalo es:

  \[
  \Phi_{\text{nuevo}} = alto-(m+1)+1 = alto-m
  \]

- Si \(A[m] > x\), el nuevo tamaño es:

  \[
  \Phi_{\text{nuevo}} = (m-1)-bajo+1 = m-bajo
  \]

Como \(m\) se calcula mediante la división entera del intervalo entre dos, en ambos casos se cumple:

\[
\Phi_{\text{nuevo}} \leq
\left\lfloor \frac{\Phi}{2} \right\rfloor
\]

Por tanto, el tamaño del intervalo se reduce, como mínimo, a la mitad en cada iteración.

**3. Terminación y cota de iteraciones:**

El potencial es un entero no negativo mientras el ciclo se ejecuta y disminuye estrictamente en cada iteración. Cuando el intervalo queda vacío, su valor llega a cero.

Además, después de \(k\) iteraciones sin encontrar el elemento:

\[
\Phi_k \leq \left\lfloor \frac{n}{2^k} \right\rfloor
\]

El intervalo necesariamente queda vacío cuando:

\[
2^k \geq n+1
\]

Por tanto:

\[
k \geq \lceil \log_2(n+1) \rceil
\]

En consecuencia, el algoritmo realiza como máximo:

\[
\boxed{\lceil \log_2(n+1) \rceil}
\]

iteraciones sin encontrar el elemento. Esto garantiza la terminación y establece una complejidad temporal de:

\[
\boxed{O(\log n)}
\]

---

## 4. Cota de información y optimalidad (Conferencia 5)

Para demostrar que la búsqueda binaria es óptima en el orden asintótico, utilizamos el modelo de **árboles de decisión por comparaciones**.

Suponemos que el arreglo contiene \(n\) elementos distintos y que el algoritmo debe devolver el índice del elemento encontrado o \(-1\) si no existe.

**1. El modelo:**

Cada comparación entre \(x\) y un elemento del arreglo puede producir tres resultados:

- \(x < A[m]\).
- \(x = A[m]\).
- \(x > A[m]\).

Por tanto, las comparaciones generan un árbol de decisión ternario, donde cada nodo interno representa una comparación y cada rama representa uno de sus posibles resultados.

**2. Cantidad de resultados posibles:**

El algoritmo debe distinguir entre las siguientes respuestas:

- \(x\) se encuentra en la posición \(0\).
- \(x\) se encuentra en la posición \(1\).
- ...
- \(x\) se encuentra en la posición \(n-1\).
- \(x\) no se encuentra en el arreglo.

Existen, por tanto, \(n+1\) resultados posibles que el algoritmo debe poder distinguir.

**3. Cota de información:**

Un árbol de decisión ternario de altura \(h\) puede tener como máximo:

\[
3^h
\]

hojas.

Para distinguir los \(n+1\) resultados posibles, necesariamente debe cumplirse:

\[
3^h \geq n+1
\]

Tomando logaritmo en base 3:

\[
h \geq \log_3(n+1)
\]

Por tanto, cualquier algoritmo que resuelva este problema mediante comparaciones necesita, en el peor caso, al menos:

\[
\boxed{\Omega(\log n)}
\]

comparaciones.

**4. Conclusión sobre la optimalidad:**

La búsqueda binaria necesita \(O(\log n)\) comparaciones en el peor caso, mientras que la cota de información demuestra que cualquier algoritmo de búsqueda basado en comparaciones necesita al menos \(\Omega(\log n)\).

Como ambas cotas coinciden en el orden asintótico:

\[
\boxed{T(n)=\Theta(\log n)}
\]

se concluye que la búsqueda binaria es **asintóticamente óptima** en el modelo de comparación considerado.

---

## 5. Resumen

- **Invariante:** Si \(x\) pertenece al arreglo, al menos una de sus posiciones debe permanecer dentro del intervalo \([bajo, alto]\). Todos los elementos descartados son menores o mayores que \(x\), según el lado del intervalo en que se encuentren.

- **Potencial:** Se define como:

  \[
  \Phi = alto-bajo+1
  \]

  Disminuye, como mínimo, a la mitad en cada iteración, garantizando la terminación en \(O(\log n)\) iteraciones.

- **Cota de información:** Existen \(n+1\) resultados posibles y un árbol de decisión ternario de altura \(h\) puede distinguir como máximo \(3^h\) resultados. Por tanto, cualquier algoritmo necesita \(\Omega(\log n)\) comparaciones en el peor caso.

- **Optimalidad:** La búsqueda binaria alcanza una complejidad de \(\Theta(\log n)\), por lo que es asintóticamente óptima.