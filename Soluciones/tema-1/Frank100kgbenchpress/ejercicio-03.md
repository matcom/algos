# Ejercicio 3: Pila con operación mínimo en \(O(1)\)

**Enunciado:** Una pila con una operación mínimo que cuesta \(O(1)\) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación. (C3)

**Modelo:** Modelo RAM (operaciones básicas de pila como `push` y `pop` cuestan \(O(1)\)).

---

## 1. Diseño de la estructura

Para conseguir que la operación `min()` tenga un costo \(O(1)\) en el peor caso, sin necesidad de recorrer todos los elementos de la pila, utilizamos **dos pilas**:

1. **Pila Principal (\(P\)):** Almacena todos los elementos como una pila convencional.
2. **Pila de Mínimos (\(M\)):** Almacena los mínimos de la pila principal, incluyendo los mínimos anteriores que pueden volver a ser necesarios cuando se eliminen elementos.

### Operaciones

**`push(x)`:**

1. Insertamos \(x\) en la pila principal \(P\).
2. Si \(M\) está vacía o \(x \leq M.top()\), insertamos también \(x\) en \(M\).

Utilizamos \(\leq\) en lugar de \(<\) para manejar correctamente los elementos duplicados.

**`pop()`:**

1. Extraemos el elemento superior \(y\) de \(P\).
2. Si \(y = M.top()\), también extraemos el elemento superior de \(M\), porque estamos eliminando una ocurrencia del mínimo actual.

**`min()`:**

1. Devolvemos el elemento superior de \(M\), sin modificar ninguna de las pilas.

Se supone que `pop()` y `min()` solamente se ejecutan cuando la pila principal no está vacía.

---

## 2. Invariante (Conferencia 3)

Para demostrar la correctitud de la estructura, definimos un invariante que debe mantenerse después de cada operación.

**Invariante:**

La pila \(M\) contiene exactamente los elementos de \(P\) que, al ser insertados, eran menores o iguales que todos los elementos que estaban debajo de ellos en la pila principal.

Por tanto, se cumplen las siguientes propiedades:

1. Si \(P\) está vacía, \(M\) también está vacía, y viceversa.
2. Si \(P\) no está vacía, el elemento superior de \(M\) es el mínimo de \(P\):

   \[
   M.top()=\min(P)
   \]

3. Los elementos de \(M\) están ordenados de forma monótona no creciente desde la base hasta el tope. Por tanto, el elemento superior siempre es el menor o igual a los anteriores.

### Demostración del invariante por inducción

**1. Inicialización:**

Al comienzo, ambas pilas están vacías:

\[
P=\varnothing,\qquad M=\varnothing
\]

No existen elementos que incumplan las propiedades del invariante. Por tanto, se cumple inicialmente.

**2. Mantenimiento (operación `push(x)`):**

Al insertar \(x\) en \(P\), pueden ocurrir dos situaciones:

- Si \(M\) está vacía o \(x\leq M.top()\), entonces \(x\) es menor o igual que todos los elementos de \(P\). Por tanto, se inserta también en \(M\). De esta manera, el nuevo elemento pasa a ser el mínimo de la pila principal y el invariante se conserva.

- Si \(x>M.top()\), significa que existe un elemento anterior menor que \(x\). Por tanto, \(x\) no es un nuevo mínimo y no necesita insertarse en \(M\). El mínimo anterior continúa siendo el mínimo de \(P\), por lo que el invariante se mantiene.

En ambos casos, las propiedades del invariante permanecen válidas.

**3. Mantenimiento (operación `pop()`):**

Sea \(y\) el elemento extraído de la pila principal \(P\).

Podemos distinguir dos situaciones:

- **Si \(y=M.top()\):** El elemento eliminado es una de las ocurrencias del mínimo actual. Como la pila \(M\) almacena los mínimos de prefijo, incluyendo los duplicados, corresponde eliminar también su ocurrencia superior de \(M\). El nuevo tope de \(M\), si existe, representa el mínimo de los elementos restantes de \(P\).

- **Si \(y\neq M.top()\):** El elemento eliminado no era el mínimo actual. Por tanto, al eliminarlo, el mínimo de \(P\) no cambia y no es necesario modificar \(M\).

En ambos casos, las dos pilas siguen cumpliendo el invariante.

**4. Operación `min()`:**

Esta operación simplemente consulta el elemento superior de \(M\), sin modificar ninguna de las pilas.

Por la propiedad del invariante:

\[
M.top()=\min(P)
\]

Por tanto, la operación siempre devuelve el mínimo correcto.

Así, por inducción sobre la secuencia de operaciones, el invariante se conserva y la estructura funciona correctamente.

---

## 3. Costo de cada operación

Trabajamos bajo el modelo RAM, donde las operaciones básicas de las pilas (`push`, `pop`, `top` y comprobación de vacío) y las comparaciones cuestan \(O(1)\).

- **`push(x)`:** Realiza una inserción en \(P\), una comprobación del tope de \(M\), una comparación y, como máximo, otra inserción en \(M\). Su costo es:

  \[
  \boxed{O(1)}
  \]

- **`pop()`:** Realiza una extracción de \(P\), una comparación con el tope de \(M\) y, como máximo, otra extracción de \(M\). Su costo es:

  \[
  \boxed{O(1)}
  \]

- **`min()`:** Únicamente consulta el tope de \(M\), sin recorrer ningún elemento. Su costo es:

  \[
  \boxed{O(1)}
  \]

- **Memoria (espacio):** La pila principal almacena los \(n\) elementos. En el peor caso, la pila de mínimos también puede almacenar los \(n\) elementos, por ejemplo, cuando se insertan en orden estrictamente decreciente. Por tanto, el espacio auxiliar adicional es:

  \[
  \boxed{O(n)}
  \]

---

## 4. Conclusión

La estructura propuesta utiliza dos pilas: una para almacenar todos los elementos y otra para mantener los mínimos históricos.

El invariante garantiza que el tope de la pila de mínimos siempre representa el mínimo actual de la pila principal. Además, al conservar los mínimos anteriores y manejar correctamente los duplicados, podemos actualizar el mínimo en tiempo constante cuando se insertan o eliminan elementos.

Por tanto, se garantiza que las tres operaciones principales:

\[
\boxed{
push(x)=O(1),\quad pop()=O(1),\quad min()=O(1)
}
\]

se ejecuten en tiempo constante en el peor caso, utilizando \(O(n)\) de espacio auxiliar adicional.

No se necesita análisis amortizado, ya que cada operación realiza un número constante de operaciones primitivas.