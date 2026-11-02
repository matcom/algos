**Resumen:** Mantenga una segunda pila `M` en paralelo con la pila principal `S`, donde `M[i]` almacena el mínimo de `S[0..i]`. Entonces `push`, `pop`, `top` y `min` son todos $O(1)$ en el peor caso, y la estructura usa $\Theta(n)$ espacio. Esto es óptimo en tiempo, ya que cada operación debe realizar al menos un trabajo constante.

## Enunciado formal



Mantener una secuencia $S = (s_0, \dots, s_{n-1})$ de elementos comparables, inicialmente vacía, que soporta:

- `push(x)`: $S \leftarrow (s_0, \dots, s_{n-1}, x)$.
- `pop()`: requiere $n \ge 1$. Elimina y devuelve $s_{n-1}$.
- `top()`: requiere $n \ge 1$. Devuelve $s_{n-1}$.
- `get_min()`: requiere $n \ge 1$. Devuelve $\min\{s_0, \dots, s_{n-1}\}$.

Objetivo: cada operación se ejecuta en tiempo $O(1)$ en el peor caso (no amortizado).

## Diseño


Auxiliares sobre una lista `L`, cada uno de los cuales se supone que toma tiempo $O(1)$ en el peor caso:

- `new_list()`: devuelve una lista vacía.
- `push_back(L, x)`: agrega `x` al final de `L`.
- `pop_back(L)`: elimina y devuelve el último elemento de `L`.
- `last(L)`: devuelve el último elemento de `L` sin eliminarlo.
- `is_empty(L)`: devuelve `True` si y solo si `L` no tiene elementos.

```python
class MinStack:
    def __init__(self):
        self.S = new_list()   # los elementos
        self.M = new_list()   # M[i] = mínimo de S[0..i]

    def push(self, x):
        if is_empty(self.M):
            push_back(self.M, x)
        elif x < last(self.M):
            push_back(self.M, x)
        else:
            push_back(self.M, last(self.M))
        push_back(self.S, x)

    def pop(self):
        pop_back(self.M)
        return pop_back(self.S)

    def top(self):
        return last(self.S)

    def get_min(self):
        return last(self.M)
```

## Invariante



**Invariante $I$:** $|S| = |M|$, y para cada índice $i$ con $0 \le i < |S|$,
$$M[i] = \min\{S[0], \dots, S[i]\}.$$

## Corrección

*Esquema: inicialización, mantenimiento por operación, luego postcondición, luego terminación.*

**Inicialización.** Ambas listas están vacías, así que $I$ se cumple vacuamente.

**Mantenimiento.** Suponga que $I$ se cumple antes de una operación, con $n = |S|$.

- `push(x)`:
  - Si $n = 0$, entonces $M[0] = x = \min\{S[0]\}$.
  - Si $n \ge 1$, la nueva entrada es $\min(x, M[n-1])$. Por $I$, $M[n-1] = \min\{S[0..n-1]\}$, así que la nueva entrada es igual a $\min\{S[0..n-1], x\}$, que es el mínimo del nuevo prefijo.
  - Ambas listas crecen en uno, así que los tamaños siguen siendo iguales.
  - Las entradas en índices menores que $n$ no cambian, así que sus igualdades siguen cumpliéndose.
- `pop()`: ambas listas pierden su último elemento, así que los tamaños siguen siendo iguales. Cada índice restante $i < n-1$ conserva su entrada, y el prefijo $S[0..i]$ no cambia, así que $I$ sigue cumpliéndose.
- `top()` y `get_min()` no modifican nada, así que $I$ se preserva.

**Postcondiciones.**

- `pop` y `top` devuelven `last(S)`, que es $s_{n-1}$ como se especifica.
- `get_min` devuelve $M[n-1] = \min\{S[0..n-1]\}$, que es el mínimo de todos los elementos, por $I$ con $i = n-1$.

**Terminación.** No hay bucles ni recursión. Cada operación ejecuta un número fijo de llamadas auxiliares, cada una de las cuales termina. $\blacksquare$

## Complejidad


| Operación | Tiempo en el peor caso | Espacio extra |
|---|---|---|
| `push` | $O(1)$ | $O(1)$ (una nueva entrada en cada lista) |
| `pop` | $O(1)$ | ninguno |
| `top` | $O(1)$ | ninguno |
| `get_min` | $O(1)$ | ninguno |

Cada operación realiza como máximo tres llamadas auxiliares y una comparación. El espacio total es $2n$ elementos almacenados, por lo que $\Theta(n)$.

## ¿Se puede hacer mejor?


**Tiempo: no.** Cualquier implementación correcta de `push` debe escribir el nuevo elemento, y cualquier `get_min` debe devolver un valor, así que cada operación cuesta $\Omega(1)$. Por lo tanto, $\Theta(1)$ por operación es óptimo.

**Espacio: solo por un factor constante.** La pila principal necesita $\Theta(n)$ espacio para almacenar los elementos, así que el espacio total no puede bajar por debajo de $\Theta(n)$ y nuestro $2n$ ya es asintóticamente óptimo. Se pueden lograr ahorros en factores constantes:

- Hacer push en `M` solo cuando $x \le$ el mínimo actual, y hacer pop de `M` solo cuando el elemento extraído sea igual al mínimo actual. Usar $\le$ en lugar de $<$ es lo que mantiene correctos los duplicados. En el peor caso (una secuencia decreciente) `M` sigue teniendo tamaño $n$.
- Alternativamente, almacenar cada elemento junto con su mínimo de prefijo en una sola pila de pares. Esto tiene el mismo costo de espacio pero un invariante más simple.