# Ejercicio 3 — Pila con mínimo en O(1) peor caso

> ★ Una pila con una operación mínimo que cuesta O(1) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación. (C3)

---

## 1. Especificación

Queremos una estructura `PilaMin` que soporte las operaciones habituales de una pila y, además, consulte el mínimo de todos los elementos que contiene en tiempo constante **en el peor caso**.

**Operaciones:**

| Operación | Descripción |
|---|---|
| `push(x)` | Apila `x` en el tope. |
| `pop()` | Desapila y devuelve el elemento del tope. Error si está vacía. |
| `min()` | Devuelve el mínimo de los elementos apilados. Error si está vacía. |
| `empty()` | Devuelve `True` si la pila está vacía. |

**Precondición:** ninguna especial; la pila puede estar vacía.

**Postcondición:**

- `pop()` devuelve el último elemento apilado que no haya sido desapilado.
- `min()` devuelve `m` tal que `m ≤ x` para todo `x` en la pila.
- `empty()` devuelve `True` si y solo si no hay elementos.

**Modelo de costo:** contamos operaciones elementales (asignaciones, comparaciones, accesos a listas). Queremos `push`, `pop`, `min` y `empty` en `O(1)` **peor caso**, no amortizado.

---

## 2. La idea

Una pila normal no puede dar el mínimo en `O(1)` porque el mínimo puede cambiar al desapilar. La solución es recordar, **para cada nivel de la pila**, cuál era el mínimo hasta ese nivel.

Usamos dos pilas:

- `_datos`: los elementos apilados, en orden.
- `_minimos`: en la misma posición `i`, el mínimo de `_datos[0..i]`.

Así, el mínimo de toda la pila es simplemente `_minimos[-1]`, el tope de la pila de mínimos.

```text
push(3):   datos = [3]          minimos = [3]
push(1):   datos = [3, 1]       minimos = [3, 1]
push(2):   datos = [3, 1, 2]    minimos = [3, 1, 1]
min() -> 1 = minimos[-1]
pop() -> 2: datos = [3, 1]      minimos = [3, 1]
min() -> 1
pop() -> 1: datos = [3]         minimos = [3]
min() -> 3
```

Cada `push` añade un elemento a cada pila; cada `pop` quita uno de cada pila. El mínimo actual siempre está en el tope de `_minimos`.

---

## 3. Implementación

```python
class PilaMin:
    def __init__(self):
        self._datos = []
        self._minimos = []

    def push(self, x):
        self._datos.append(x)
        if not self._minimos:
            self._minimos.append(x)
        else:
            self._minimos.append(min(x, self._minimos[-1]))

    def pop(self):
        if not self._datos:
            raise IndexError("pop de pila vacía")
        self._minimos.pop()
        return self._datos.pop()

    def min(self):
        if not self._minimos:
            raise IndexError("min de pila vacía")
        return self._minimos[-1]

    def empty(self):
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"PilaMin(datos={self._datos}, minimos={self._minimos})"
```

**Variante equivalente:** una sola pila de pares `(valor, minimo_hasta_aqui)`. Las dos pilas son más fáciles de leer y de demostrar.

---

## 4. Invariante

> **Invariante `I`.** Después de cualquier secuencia de operaciones, si la pila tiene `n` elementos, entonces:
>
> 1. `len(self._datos) == len(self._minimos) == n`.
> 2. Para cada `i` con `0 ≤ i < n`, `self._minimos[i] == min(self._datos[0..i])`.
>
> En particular, `self._minimos[-1] == min(self._datos)`.

El índice `0` es el fondo de la pila y `n-1` el tope.

### 4.1. Inicialización

Antes de cualquier operación, `n = 0`, ambas listas están vacías. La condición 1 se cumple (`0 == 0 == 0`) y la condición 2 es vacía. ✔

### 4.2. Mantenimiento

**Caso `push(x)`.** Supongamos el invariante antes de apilar, con `n` elementos.

- La pila de datos pasa a tener `n+1` elementos: `S' = S + [x]`.
- La pila de mínimos añade `min(x, M[-1])` si `n > 0`, o `x` si `n = 0`.

Para `i < n`, `M'[i] = M[i] = min(S[0..i]) = min(S'[0..i])`, porque `S'[0..i] = S[0..i]`.

Para `i = n`:

- Si `n = 0`, `M'[0] = x = min(S'[0..0])`.
- Si `n > 0`, `M'[n] = min(x, M[-1]) = min(x, min(S)) = min(S'[0..n])`.

Así que el invariante se mantiene. ✔

**Caso `pop()`.** Supongamos el invariante antes de desapilar, con `n > 0`. El algoritmo quita el último elemento de ambas listas y devuelve el último elemento de `S`, que es el tope de la pila antes de desapilar, cumpliendo así la postcondición. La pila resultante tiene `n-1` elementos y, para cada `i < n-1`, `M'[i] = M[i] = min(S[0..i]) = min(S'[0..i])`. El invariante se mantiene. ✔

**Caso `min()`.** No modifica el estado. Devuelve `M[-1]`, que por el invariante es `min(S)`. ✔

**Caso `empty()`.** No modifica el estado. Devuelve `len(S) == 0`, que es exactamente “no hay elementos”. ✔

### 4.3. Conclusión

Cuando el algoritmo termina una operación, el invariante sigue siendo verdadero. En particular, `min()` devuelve el mínimo correcto y `pop()` devuelve el tope correcto. La estructura es **correcta parcialmente**.

### 4.4. Terminación

Cada operación ejecuta una cantidad constante de instrucciones, sin ciclos. Por tanto, todas las operaciones terminan. La correctitud es total.

---

## 5. Costo

| Operación | Tiempo | Memoria adicional |
|---|---|---|
| `push(x)` | `O(1)` | `O(1)` |
| `pop()` | `O(1)` | `O(1)` |
| `min()` | `O(1)` | `O(1)` |
| `empty()` | `O(1)` | `O(1)` |

**Memoria total:** `O(n)` para `n` elementos, porque guardamos dos listas de longitud `n`. Es el doble de una pila normal, pero sigue siendo lineal.

**Peor caso, no amortizado.** En el modelo RAM suponemos que las pilas subyacentes son listas enlazadas, de modo que push y pop cuestan O(1) en el peor caso. El código Python usa list por claridad; en CPython, append es O(1) amortizado y puede costar O(n) en una operación aislada por redimensionamiento. Si se exige peor caso también en la implementación, se usan nodos enlazados o se declara que el modelo abstracto cuenta append/pop como operación elemental.

**Comparación con la solución ingenua.** Si guardáramos solo `_datos`, `min()` costaría `O(n)` en el peor caso, porque habría que recorrer toda la pila. La pila auxiliar de mínimos elimina ese recorrido.

---

## 6. Traza de ejemplo

Secuencia: `push(3)`, `push(1)`, `push(2)`, `min()`, `pop()`, `min()`, `push(0)`, `min()`.

| Paso | Operación | `_datos` | `_minimos` | `min()` |
|---|---|---|---|---|
| 0 | inicio | `[]` | `[]` | — |
| 1 | `push(3)` | `[3]` | `[3]` | — |
| 2 | `push(1)` | `[3, 1]` | `[3, 1]` | — |
| 3 | `push(2)` | `[3, 1, 2]` | `[3, 1, 1]` | — |
| 4 | `min()` | `[3, 1, 2]` | `[3, 1, 1]` | `1` |
| 5 | `pop()` | `[3, 1]` | `[3, 1]` | — |
| 6 | `min()` | `[3, 1]` | `[3, 1]` | `1` |
| 7 | `push(0)` | `[3, 1, 0]` | `[3, 1, 0]` | — |
| 8 | `min()` | `[3, 1, 0]` | `[3, 1, 0]` | `0` |

En cada fila, el tope de `_minimos` es el mínimo de `_datos`.

---

## 7. Pruebas

### 7.1. Prueba contra un oráculo ingenuo

Comparamos `PilaMin` con una implementación que guarda una lista y calcula `min(lista)` cada vez. Hacemos muchas secuencias aleatorias de operaciones.

```python
import random

def pila_ingenua_ops(ops):
    datos = []
    salida = []
    for op in ops:
        if op[0] == "push":
            datos.append(op[1])
        elif op[0] == "pop":
            salida.append(datos.pop() if datos else "error")
        elif op[0] == "min":
            salida.append(min(datos) if datos else "error")
        elif op[0] == "empty":
            salida.append(len(datos) == 0)
    return salida

def pila_min_ops(ops):
    p = PilaMin()
    salida = []
    for op in ops:
        if op[0] == "push":
            p.push(op[1])
        elif op[0] == "pop":
            try:
                salida.append(p.pop())
            except IndexError:
                salida.append("error")
        elif op[0] == "min":
            try:
                salida.append(p.min())
            except IndexError:
                salida.append("error")
        elif op[0] == "empty":
            salida.append(p.empty())
    return salida

random.seed(2026)
for prueba in range(5000):
    n_ops = random.randint(0, 30)
    ops = []
    for _ in range(n_ops):
        r = random.random()
        if r < 0.5:
            ops.append(("push", random.randint(-10, 10)))
        elif r < 0.7:
            ops.append(("pop",))
        elif r < 0.9:
            ops.append(("min",))
        else:
            ops.append(("empty",))
    a = pila_ingenua_ops(ops)
    b = pila_min_ops(ops)
    assert a == b, f"Fallo en la prueba {prueba}: {ops}\n{a}\n{b}"
print("5000 secuencias aleatorias comparadas con el oráculo: sin fallos")
```

```text
5000 secuencias aleatorias comparadas con el oráculo: sin fallos
```

### 7.2. Casos borde

```python
p = PilaMin()

# vacía
assert p.empty() is True
try:
    p.min()
    assert False, "min de vacía no lanzó error"
except IndexError:
    pass
try:
    p.pop()
    assert False, "pop de vacía no lanzó error"
except IndexError:
    pass

# un elemento
p.push(42)
assert p.min() == 42
assert p.pop() == 42
assert p.empty() is True

# duplicados
for x in [5, 5, 5]:
    p.push(x)
assert p.min() == 5
assert p.pop() == 5
assert p.min() == 5
assert p.pop() == 5
assert p.min() == 5
assert p.pop() == 5
assert p.empty() is True

# orden decreciente
for x in [9, 7, 5, 3, 1]:
    p.push(x)
assert p.min() == 1
assert p.pop() == 1
assert p.min() == 3
assert p.pop() == 3
assert p.min() == 5
assert p.pop() == 5

# negativos
p = PilaMin()
for x in [-3, -1, -7, 0]:
    p.push(x)
assert p.min() == -7
assert p.pop() == 0
assert p.min() == -7
assert p.pop() == -7
assert p.min() == -3

print("casos borde: sin fallos")
```

```text
casos borde: sin fallos
```

### 7.3. El invariante vigilado

Ejecutamos `PilaMin` y comprobamos el invariante en cada paso.

```python
def verificar_invariante(p):
    S, M = p._datos, p._minimos
    assert len(S) == len(M), "longitudes distintas"
    for i in range(len(S)):
        assert M[i] == min(S[:i+1]), f"minimo incorrecto en {i}: {M[i]} != {min(S[:i+1])}"

random.seed(7)
p = PilaMin()
for _ in range(2000):
    r = random.random()
    if r < 0.6:
        p.push(random.randint(-100, 100))
    elif r < 0.8 and not p.empty():
        p.pop()
    elif r < 0.9 and not p.empty():
        p.min()
    verificar_invariante(p)
print("invariante verificado en 2000 operaciones, sin fallos")
```

```text
invariante verificado en 2000 operaciones, sin fallos
```

---