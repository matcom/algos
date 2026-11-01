# Ejercicio 6: Búsqueda en matriz ordenada por filas y columnas

**Enunciado:** Una matriz \(n\times n\) tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor \(x\) en \(O(n)\) comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en \(o(n)\). (C3, C5)

**Modelo:** Árboles de decisión por comparaciones (solo podemos comparar \(x\) con los elementos de la matriz).

---

## 1. Algoritmo propuesto (Eliminación de filas y columnas)

La idea consiste en aprovechar el orden bidimensional de la matriz. Si comenzamos en la **esquina superior derecha**, cada comparación permite descartar una fila o una columna completa de la región de búsqueda.

```python
def buscar_en_matriz(A, x):
    n = len(A)
    fila = 0
    col = n - 1

    while fila < n and col >= 0:
        if A[fila][col] == x:
            return True
        elif A[fila][col] > x:
            # Los elementos inferiores de esta columna son mayores.
            col -= 1
        else:
            # Los elementos a la izquierda de esta fila son menores.
            fila += 1

    return False
```

### Análisis del costo

En cada iteración ocurre una de estas dos cosas:

- El índice `fila` aumenta en una unidad.
- El índice `col` disminuye en una unidad.

El índice `fila` puede aumentar como máximo \(n\) veces y el índice `col` puede disminuir como máximo \(n\) veces.

Por tanto, el ciclo realiza como máximo \(2n\) iteraciones.

Como en cada iteración se realizan una cantidad constante de comparaciones y operaciones elementales:

\[
\boxed{T(n)=O(n)}
\]

El algoritmo utiliza únicamente dos índices adicionales, por lo que su espacio auxiliar es:

\[
\boxed{S(n)=O(1)}
\]

---

## 2. Correctitud (Invariante)

Para demostrar la correctitud del algoritmo, utilizamos el siguiente invariante inductivo:

**Invariante:** Al inicio de cada iteración del ciclo `while`, si \(x\) se encuentra en la matriz \(A\), entonces debe estar en la submatriz definida por las coordenadas:

\[
[fila,\ldots,n-1]\times[0,\ldots,col]
\]

Todos los elementos que se encuentran fuera de esta submatriz han sido descartados porque se ha demostrado que son estrictamente menores o mayores que \(x\).

### Demostración del invariante

La demostración se realiza mediante los tres pasos habituales:

**1. Inicialización:**

Antes de la primera iteración:

\[
fila=0,\qquad col=n-1
\]

Por tanto, la región de búsqueda es:

\[
[0,\ldots,n-1]\times[0,\ldots,n-1]
\]

Esta región comprende toda la matriz, por lo que el invariante se cumple inicialmente.

**2. Mantenimiento:**

Sea el elemento actual:

\[
v=A[fila][col]
\]

Existen tres posibilidades:

- **Si \(v>x\):**

  Como las columnas están ordenadas de forma creciente, todos los elementos situados debajo de \(v\) en esa columna son mayores o iguales que él.

  Por tanto:

  \[
  A[k][col]\geq A[fila][col]>x
  \]

  para todo \(k\geq fila\).

  Ninguno de esos elementos puede ser igual a \(x\). Por tanto, podemos descartar la columna actual y actualizar:

  \[
  col=col-1
  \]

  El invariante se conserva porque cualquier posible aparición de \(x\) permanece dentro de la nueva submatriz.

- **Si \(v<x\):**

  Como las filas están ordenadas de forma creciente, todos los elementos situados a la izquierda de \(v\) son menores o iguales que él.

  Por tanto:

  \[
  A[fila][k]\leq A[fila][col]<x
  \]

  para todo \(k\leq col\).

  Ninguno de esos elementos puede ser igual a \(x\). Podemos descartar la fila actual y actualizar:

  \[
  fila=fila+1
  \]

  El invariante también se conserva.

- **Si \(v=x\):**

  Hemos encontrado el elemento buscado y el algoritmo devuelve `True`, que es una respuesta correcta.

**3. Terminación:**

El ciclo termina cuando:

\[
fila=n\quad\text{o}\quad col<0
\]

En cualquiera de estos casos, la submatriz de búsqueda está vacía.

Por el invariante, si \(x\) estuviera en la matriz original, tendría que encontrarse dentro de esa submatriz. Como está vacía, concluimos que \(x\) no pertenece a la matriz.

Por tanto, el algoritmo devuelve correctamente `False`.

Así, queda demostrada la correctitud del algoritmo.

---

## 3. Cota mínima (\(\Omega(n)\)) mediante el método del adversario (Conferencia 5)

Para demostrar que ningún algoritmo puede resolver este problema utilizando \(o(n)\) comparaciones en el peor caso, empleamos un argumento de adversario.

La idea es construir situaciones en las que el algoritmo necesite examinar al menos \(n\) posiciones diferentes para estar seguro de si \(x\) aparece o no en la matriz.

### 3.1. Construcción de la anti-diagonal

Consideremos las posiciones de la anti-diagonal:

\[
A[i][n-1-i],\qquad i=0,\ldots,n-1
\]

Existen exactamente \(n\) posiciones.

Observemos que dos posiciones diferentes de esta anti-diagonal nunca pertenecen a la misma fila ni a la misma columna. Por tanto, sus valores pueden modificarse independientemente, siempre que se respeten los valores de las posiciones vecinas.

### 3.2. Construcción de matrices ordenadas válidas

Para demostrar que el adversario puede mantener la consistencia de sus respuestas, construiremos una familia de matrices.

Sea \(s=r+c\). Asignamos los valores de la matriz de la siguiente manera:

\[
A[r][c]=
\begin{cases}
x-2(n-1-s), & s<n-1\\
a_r, & s=n-1\\
x+2(s-(n-1)), & s>n-1
\end{cases}
\]

donde cada valor \(a_r\), correspondiente a una posición de la anti-diagonal, puede elegirse independientemente entre:

\[
a_r\in\{x-1,x,x+1\}
\]

Esta construcción garantiza que las filas y las columnas estén ordenadas de forma creciente.

En efecto:

- Todas las posiciones anteriores a la anti-diagonal tienen valores menores que \(x\).
- Todas las posiciones posteriores tienen valores mayores que \(x\).
- Cada posición de la anti-diagonal puede tomar cualquiera de los tres valores sin violar el orden de su fila o columna.

Por tanto, el adversario puede modificar independientemente las posiciones de la anti-diagonal manteniendo una matriz válida.

### 3.3. Estrategia del adversario

El adversario responde a las comparaciones de la siguiente manera:

1. Si el algoritmo consulta una posición situada por encima y a la izquierda de la anti-diagonal (\(r+c<n-1\)), responde que:

   \[
   A[r][c]<x
   \]

2. Si consulta una posición situada por debajo y a la derecha de la anti-diagonal (\(r+c>n-1\)), responde que:

   \[
   A[r][c]>x
   \]

3. Si consulta una posición de la anti-diagonal (\(r+c=n-1\)), responde que:

   \[
   A[r][c]<x
   \]

   y registra que esa posición ya fue consultada.

Estas respuestas son compatibles con la construcción anterior y, por tanto, el adversario siempre puede mantener una matriz ordenada válida.

### 3.4. Demostración de la cota inferior

Supongamos que un algoritmo realiza menos de \(n\) comparaciones.

Como la anti-diagonal contiene \(n\) posiciones, necesariamente quedará al menos una posición sin consultar.

Sea \(A[i][n-1-i]\) una de esas posiciones.

Podemos construir dos matrices válidas:

**Matriz 1:**

Todas las posiciones de la anti-diagonal tienen valor \(x-1\). Por tanto, la matriz no contiene \(x\).

**Matriz 2:**

Es idéntica a la primera, excepto en la posición no consultada \(A[i][n-1-i]\), donde colocamos:

\[
A[i][n-1-i]=x
\]

Esta segunda matriz sí contiene el elemento buscado.

Ambas matrices mantienen el orden creciente de filas y columnas y producen exactamente las mismas respuestas para todas las comparaciones que el algoritmo ha realizado, porque la única posición diferente no fue consultada.

Por tanto, el algoritmo no puede distinguir entre ambas matrices y no puede decidir correctamente si \(x\) está presente.

Esto contradice la suposición de que puede resolver el problema con menos de \(n\) comparaciones en todos los casos.

En consecuencia, cualquier algoritmo basado en comparaciones necesita, en el peor caso:

\[
\boxed{T(n)=\Omega(n)}
\]

---

## 4. Conclusión: Optimalidad del algoritmo

Hemos demostrado dos resultados:

- Nuestro algoritmo realiza \(O(n)\) comparaciones en el peor caso.
- Mediante el método del adversario demostramos que cualquier algoritmo necesita al menos \(\Omega(n)\) comparaciones en el peor caso.

Por tanto:

\[
O(n)\cap\Omega(n)=\Theta(n)
\]

Así, la complejidad del algoritmo propuesto es:

\[
\boxed{T(n)=\Theta(n)}
\]

Y su espacio auxiliar es:

\[
\boxed{S(n)=O(1)}
\]

**Conclusión final:** El algoritmo de eliminación de filas y columnas es asintóticamente óptimo para la búsqueda de un elemento en una matriz ordenada por filas y columnas, dentro del modelo de comparación establecido.