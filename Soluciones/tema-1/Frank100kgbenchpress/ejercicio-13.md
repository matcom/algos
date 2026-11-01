# Ejercicio 13: Splay Tree con acceso secuencial desde un camino

**Enunciado:** En un Splay Tree que empieza como un camino de \(n\) nodos se accede a las claves \(1,\ldots,n\) en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? (C4)

**Modelo:** Splay Tree (árbol binario de búsqueda autoajustable). Inicialmente, el árbol es un camino de \(n\) nodos. La secuencia de acceso es \(1,2,\ldots,n\), en orden creciente.

---

## 1. Cota mediante el Lema de Acceso (Sección 5)

El **Lema de Acceso (Access Lemma)** establece que, para un Splay Tree con pesos arbitrarios positivos \(w(x)\), el costo amortizado de acceder a un nodo \(x\) está acotado por:

\[
\hat c_i\leq 1+3(r(root)-r(x))
\]

Donde:

\[
r(x)=\log_2(s(x))
\]

y \(s(x)\) es la suma de los pesos de los nodos del subárbol cuya raíz es \(x\).

### Asignación de pesos

Asignamos pesos uniformes:

\[
w(x)=1
\]

para todos los nodos.

Por tanto, el peso total del árbol es:

\[
W=n
\]

La raíz tiene rango:

\[
r(root)=\log_2 n
\]

Además, como cada nodo tiene al menos su propio peso:

\[
s(x)\geq1
\]

y, por tanto:

\[
r(x)\geq0
\]

Sustituyendo estos valores en el lema de acceso:

\[
\hat c_i\leq1+3(\log_2 n-0)
\]

Por tanto, cada acceso tiene un costo amortizado acotado por:

\[
\boxed{\hat c_i=O(\log n)}
\]

### Costo amortizado de los \(n\) accesos

Como realizamos \(n\) accesos, podemos sumar las cotas individuales:

\[
\sum_{i=1}^{n}\hat c_i
\leq n(1+3\log_2 n)
\]

Por tanto:

\[
\boxed{\sum_{i=1}^{n}\hat c_i=O(n\log n)}
\]

Esta es la cota superior que obtenemos directamente del Lema de Acceso.

### Relación entre el costo amortizado y el costo real

Debemos recordar que:

\[
\hat c_i=c_i+\Phi_i-\Phi_{i-1}
\]

donde \(c_i\) es el costo real de la operación y \(\Phi_i\) es el potencial después del acceso.

Sumando los \(n\) accesos:

\[
\sum_{i=1}^{n}\hat c_i
=
\sum_{i=1}^{n}c_i+\Phi_n-\Phi_0
\]

Despejando:

\[
\sum_{i=1}^{n}c_i
=
\sum_{i=1}^{n}\hat c_i+\Phi_0-\Phi_n
\]

La función de potencial es no negativa, por lo que:

\[
\Phi_n\geq0
\]

Entonces:

\[
\sum_{i=1}^{n}c_i
\leq
\sum_{i=1}^{n}\hat c_i+\Phi_0
\]

### Cálculo del potencial inicial

El árbol comienza como un camino de \(n\) nodos.

Los tamaños de sus subárboles son:

\[
1,2,3,\ldots,n
\]

Por tanto, su potencial inicial es:

\[
\Phi_0=\sum_{k=1}^{n}\log_2 k
\]

Aplicando la propiedad del logaritmo:

\[
\Phi_0=\log_2(n!)
\]

Utilizando la aproximación de Stirling:

\[
\log_2(n!)=\Theta(n\log n)
\]

Por tanto:

\[
\boxed{\Phi_0=\Theta(n\log n)}
\]

Finalmente, el costo real total queda acotado por:

\[
\sum_{i=1}^{n}c_i
\leq O(n\log n)+O(n\log n)
\]

De donde obtenemos:

\[
\boxed{T(n)=O(n\log n)}
\]

Esta es la cota superior demostrada mediante el Lema de Acceso y el análisis del potencial.

---

## 2. Costo real para el acceso secuencial

Ahora debemos analizar la secuencia específica:

\[
1,2,3,\ldots,n
\]

El árbol comienza como un camino. Supongamos que es un camino hacia la izquierda, cuya raíz contiene la clave \(n\):

\[
n\rightarrow n-1\rightarrow\cdots\rightarrow2\rightarrow1
\]

**Primer acceso:**

El nodo 1 se encuentra en la posición más profunda del camino.

Para llevarlo a la raíz, el Splay Tree realiza una serie de rotaciones zig-zig y, si corresponde, una rotación zig final.

El costo del primer acceso es:

\[
c_1=O(n)
\]

**Accesos posteriores:**

Después del primer acceso, el árbol queda reorganizado.

Es importante observar que no necesariamente todos los nodos siguientes quedan como hijos directos de la raíz. Algunos pueden permanecer a mayor profundidad y necesitar varias rotaciones cuando sean accedidos.

Por tanto, no podemos justificar el costo total afirmando que cada acceso posterior cuesta \(O(1)\) individualmente.

Sin embargo, existe una propiedad fundamental de los Splay Trees:

### Teorema de acceso secuencial (Sequential Access Theorem)

Acceder a los \(n\) elementos de un Splay Tree en orden creciente requiere un costo total de:

\[
\boxed{O(n)}
\]

Esta propiedad se cumple independientemente de la estructura inicial del árbol.

Por tanto, para nuestra secuencia:

\[
1,2,3,\ldots,n
\]

el costo real total está acotado por:

\[
\boxed{T(n)=O(n)}
\]

Además, como se realizan \(n\) accesos y cada uno necesita al menos un costo constante, existe una cota inferior:

\[
T(n)=\Omega(n)
\]

Combinando ambas cotas:

\[
\boxed{T(n)=\Theta(n)}
\]

---

## 3. Comparación con la sección 6

La sección 6 permite observar el comportamiento de los Splay Trees frente a otras heurísticas de reorganización, como `move-to-root`.

La diferencia fundamental está en cómo se realizan las rotaciones.

- **Splay Tree:** utiliza las operaciones zig, zig-zig y zig-zag, reorganizando el árbol de manera que los accesos secuenciales tienen un costo total lineal.

- **Move-to-root:** utiliza rotaciones simples para llevar el nodo accedido a la raíz. En el camino inicial considerado, esta estrategia puede mantener una estructura que obliga a recorrer y reorganizar una cantidad lineal de nodos en muchos accesos.

Para la secuencia creciente sobre el camino inicial, el costo de `move-to-root` puede llegar a:

\[
\boxed{\Theta(n^2)}
\]

Mientras que el Splay Tree consigue:

\[
\boxed{\Theta(n)}
\]

Por tanto, el Splay Tree aprovecha la secuencia de accesos de una manera que la estrategia de rotaciones simples no consigue.

**Nota:** Si la sección 6 presenta resultados experimentales, estos permiten observar la diferencia entre ambas estrategias, pero la garantía de costo lineal del acceso secuencial se fundamenta en el teorema correspondiente.

---

## 4. ¿Es ajustada la cota?

**No. La cota \(O(n\log n)\) obtenida directamente mediante el Lema de Acceso no es ajustada para esta secuencia específica.**

Tenemos dos resultados:

**Mediante el Lema de Acceso:**

\[
T(n)=O(n\log n)
\]

**Mediante la propiedad de acceso secuencial:**

\[
T(n)=\Theta(n)
\]

Por tanto, para esta secuencia concreta, la cota del Lema de Acceso sobreestima el costo real.

La diferencia se debe a que el Lema de Acceso proporciona una cota general que funciona para cualquier secuencia de accesos, mientras que el acceso secuencial presenta una estructura particular que permite obtener un costo total inferior.

La diferencia entre ambas cotas es un factor de:

\[
\frac{n\log n}{n}=\log n
\]

Por tanto, la cota general es un factor \(\log n\) mayor que el costo real de esta secuencia.

---

## 5. Conclusión

El Lema de Acceso permite establecer una cota superior general de:

\[
\boxed{O(n\log n)}
\]

para los \(n\) accesos.

Sin embargo, cuando los elementos se acceden secuencialmente en orden creciente, el Splay Tree presenta una propiedad más fuerte: el costo total es:

\[
\boxed{\Theta(n)}
\]

Por tanto, la cota obtenida directamente mediante el Lema de Acceso no es ajustada para este caso particular.

**La lección fundamental:** una cota general de un algoritmo puede ser correcta sin representar su comportamiento para una secuencia específica. Los Splay Trees aprovechan determinados patrones de acceso y pueden conseguir costos significativamente inferiores a los que garantiza el análisis general.