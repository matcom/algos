# Ejercicio 3: Pila con operación mínimo en $O(1)$ peor caso

> **Enunciado:** Una pila con una operación minimo que cuesta $O(1)$ en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación. 

## 1. Especificación

Queremos una estructura `PilaMin` con estas operaciones:

- **`push(x)`**: apila el elemento `x`.
- **`pop()`**: desapila y devuelve el tope.
  *Precondición:* la pila no está vacía.
- **`top()`**: devuelve el tope sin desapilar.
  *Precondición:* la pila no está vacía.
- **`min()`**: devuelve el mínimo de todos los elementos actuales.
  *Precondición:* la pila no está vacía.
- **`empty()`**: indica si la pila está vacía.

**Postcondición:** la estructura se comporta como una pila LIFO y `min()` devuelve el mínimo de los elementos que contiene en ese momento.

**Modelo:** word RAM, como en la conferencia 1. Cada operación elemental sobre una palabra cuesta $O(1)$. Queremos que `min()` sea $O(1)$ en el peor caso, no amortizado.

## 2. Diseño de la estructura

Usamos dos pilas:

- $P$: guarda los elementos en el orden normal de la pila.
- $M$: guarda, en su tope, el mínimo de todos los elementos que hay en $P$ hasta ese momento.

**Pseudocódigo:**

```python
class PilaMin:
    def __init__(self):
        self.P = []   # elementos
        self.M = []   # mínimos

    def push(self, x):
        self.P.append(x)
        if not self.M or x <= self.M[-1]:
            self.M.append(x)
        else:
            self.M.append(self.M[-1])

    def pop(self):
        self.M.pop()
        return self.P.pop()

    def top(self):
        return self.P[-1]

    def min(self):
        return self.M[-1]

    def empty(self):
        return len(self.P) == 0
```
La idea es que $M[i]$ siempre sea el mínimo de $P[1..i]$, donde $P[1]$ es el fondo y $P[k]$ el tope.

## 3. Invariante

Después de cualquier secuencia de operaciones, si la pila tiene $k$ elementos, entonces:

- $P$ tiene $k$ elementos y $M$ tiene $k$ elementos.
- Para cada $i = 1, \ldots, k$,

$$M[i] = \min(P[1..i]).$$

Es decir, $M[i]$ es el mínimo de los primeros $i$ elementos de $P$.

En particular, en el tope:

$$M[k] = \min(P[1..k]) = \min(\text{todos los elementos actuales}).$$

Por eso `min()` puede devolver simplemente `M.top()`.

## 4. Correctitud

Demostramos correctitud parcial con el invariante y terminación por inspección.

**Inicialización.** La pila está vacía: $k = 0$. No hay elementos en $P$ ni en $M$. El invariante se cumple trivialmente.

**Mantenimiento.** Supongamos que el invariante se cumple antes de una operación.

- **`push(x)`:** Antes hay $k$ elementos. $P$ pasa a tener $k+1$ elementos, con $P[k+1] = x$. El nuevo mínimo debe ser:

$$\min(P[1..k+1]) = \min(\min(P[1..k]), x) = \min(M[k], x).$$

El código hace exactamente eso:

- si $M$ está vacía, apila $x$;
- si no, compara $x$ con `M.top()` y apila el menor (con `<=`, si $x$ es menor o igual apila $x$; si no, apila el mínimo anterior).

Por tanto, el nuevo tope de $M$ es el mínimo de todo $P$, y los elementos anteriores de $M$ no cambian. El invariante se mantiene.

- **`pop()`:** Antes hay $k > 0$ elementos. Se eliminan el tope de $P$ y el tope de $M$. Quedan $k-1$ elementos. Para $i = 1, \ldots, k-1$, los valores $M[i]$ no cambiaron y, por el invariante anterior, siguen siendo el mínimo de $P[1..i]$. El invariante se mantiene.

- **`top()`, `min()`, `empty()`:** No modifican el estado. `min()` devuelve `M.top()`, que por el invariante es el mínimo de todos los elementos. Correcto.

**Terminación.** Cada operación es directa: no hay ciclos ni recursión. `push`, `pop`, `top`, `min` y `empty` terminan siempre. Por tanto, hay correctitud total.

## 5. Costo de cada operación

En el modelo word RAM:

| Operación | Operaciones elementales | Costo real (constante) | Costo asintótico |
|---|---|---|---|
| `push(x)` | 1 `append` en $P$; 1 chequeo `not self.M` (acceso a $M$ y negación); si no está vacía, 1 acceso a `M[-1]`, 1 comparación `x <= M[-1]`, 1 `append` en $M$ con el valor elegido | 4–6 operaciones $O(1)$ | $O(1)$ |
| `pop()` | 1 `pop` en $M$; 1 `pop` en $P$ | 2 operaciones $O(1)$ | $O(1)$ |
| `top()` | 1 acceso a `P[-1]` | 1 operación $O(1)$ | $O(1)$ |
| `min()` | 1 acceso a `M[-1]` | 1 operación $O(1)$ | $O(1)$ |
| `empty()` | 1 acceso a `len(P)` y 1 comparación con 0 | 2 operaciones $O(1)$ | $O(1)$ |

Lo importante es que todas esas operaciones son $O(1)$, así que el costo asintótico de cada método sigue siendo $O(1)$ en el peor caso.