# Ejercicio 3 - Una pila con `minimo` en $O(1)$ peor caso

> Diseña una pila con una operación `minimo` que cueste $O(1)$ en el **peor caso**.
> Enuncia el invariante que la hace correcta y da el costo de cada operación.

## 1. El problema

Una pila con `push(x)`, `pop()`, `tope()` y, además, `minimo()` que devuelve el menor
de los elementos presentes. Todo en $O(1)$ **de peor caso por operación** - no
amortizado (conferencia 4, §10: si una aplicación necesita que *cada* operación sea
rápida, el costo amortizado no sirve).

Recorrer la pila para hallar el mínimo cuesta $O(n)$. La idea es **recordar el mínimo
en cada nivel**: junto a cada elemento guardamos el mínimo de la pila hasta ese
elemento (inclusive). Así el mínimo global está siempre en el tope.

## 2. El diseño: una pila de pares

```python
class PilaConMinimo:
    """Cada entrada guarda (valor, min_hasta_aqui)."""

    def __init__(self):
        self._p = []                      # lista de pares (valor, minimo)

    def push(self, x):                    # O(1)
        m = x if not self._p else min(x, self._p[-1][1])
        self._p.append((x, m))

    def pop(self):                        # O(1)
        if not self._p:
            raise IndexError("pop en pila vacia")
        return self._p.pop()[0]

    def tope(self):                       # O(1)
        return self._p[-1][0]

    def minimo(self):                     # O(1)  <- lo que pedia el ejercicio
        if not self._p:
            raise IndexError("minimo en pila vacia")
        return self._p[-1][1]

    def __len__(self):
        return len(self._p)
```

Cada operación hace trabajo constante: un `append`/`pop` de lista y, en `push`, un solo
`min` de dos números. **$O(1)$ de peor caso, siempre.** La memoria es $O(n)$ (un par
por elemento), un factor 2 sobre la pila normal.

## 3. El invariante que la hace correcta

> **Invariante.** En todo momento, para cada posición $i$ (desde el fondo $i=0$),
> `_p[i][1]` es el mínimo de los valores `_p[0..i][0]`. En particular, el segundo
> componente del **tope** es el mínimo de **toda** la pila.

**Inicialización.** Pila vacía: no hay posiciones, el invariante vale por vacuidad.

**Mantenimiento.**
- `push(x)`: sea $t$ el tope anterior. Por el invariante, `_p[t][1]` es el mínimo de
  `_p[0..t]`. Añadimos `(x, min(x, _p[t][1]))`, que por definición es el mínimo de
  `_p[0..t+1]`. Las posiciones anteriores no cambian. El invariante se conserva. (Si
  la pila estaba vacía, guardamos `(x, x)`, que es el mínimo del único elemento.)
- `pop()`: quita el tope; las posiciones $0..t-1$ no cambian, y cada una ya cumplía el
  invariante. Se conserva.

**Conclusión.** Como el invariante vale siempre, `minimo()` devuelve `_p[-1][1]`, que
es el mínimo de todos los valores presentes: correcto. La terminación es trivial (cada
operación no tiene ciclos).

## 4. Figura - el mínimo viaja pegado al tope

Secuencia `push 5, push 3, push 8, push 3, pop, pop`. Cada celda es `(valor | min)`;
el tope está a la derecha, y el mínimo global es siempre el `min` del tope (marcado `◄`).

```
push 5     [ (5|5)◄ ]                              minimo = 5
push 3     [ (5|5)  (3|3)◄ ]                       minimo = 3
push 8     [ (5|5)  (3|3)  (8|3)◄ ]                minimo = 3   (8 no baja el min)
push 3     [ (5|5)  (3|3)  (8|3)  (3|3)◄ ]         minimo = 3
pop  ->3   [ (5|5)  (3|3)  (8|3)◄ ]                minimo = 3   (vuelve el min previo)
pop  ->8   [ (5|5)  (3|3)◄ ]                       minimo = 3
```

Observa `pop -> 8`: al quitar el `8` el mínimo sigue siendo `3` **sin recalcular nada**,
porque cada nivel ya traía su propio mínimo. Ese es la idea: el `pop` restaura el
mínimo del nivel anterior gratis.

## 5. Costos, en una tabla

| operación | trabajo | costo peor caso | memoria extra |
|---|---|---|---|
| `push(x)` | `append` + un `min` | $O(1)$ | $+1$ par |
| `pop()` | `pop` de lista | $O(1)$ | $-1$ par |
| `tope()` | leer `_p[-1][0]` | $O(1)$ |  -  |
| `minimo()` | leer `_p[-1][1]` | $O(1)$ |  -  |

Todo es $O(1)$ **de peor caso**, no amortizado: no hay ninguna operación que a veces
cueste $\Theta(n)$. Memoria total $O(n)$.

## 6. Variante (opcional): dos pilas

En lugar de pares, se puede llevar una pila `datos` y una pila `minimos` donde se
apila $x$ solo si $x \le$ tope de `minimos`. Mismo invariante ("el tope de `minimos` es
el mínimo global"), mismos costos $O(1)$ peor caso, y ahorra memoria cuando hay muchos
mínimos repetidos. La versión de pares es más simple y suficiente.

## 7. Comprobación contra un oráculo

```python
import random

class Oraculo:
    def __init__(self): self.a = []
    def push(self, x): self.a.append(x)
    def pop(self): return self.a.pop()
    def minimo(self): return min(self.a)

random.seed(1)
p, o = PilaConMinimo(), Oraculo()
ops = 0
for _ in range(100_000):
    if len(p) == 0 or random.random() < 0.55:
        x = random.randint(-50, 50)
        p.push(x); o.push(x)
    else:
        assert p.pop() == o.pop()
    if len(p):
        assert p.minimo() == o.minimo()          # el minimo O(1) coincide con el real
    ops += 1
print(f"{ops:,} operaciones, minimo O(1) siempre correcto contra el oraculo")
```

**Salida:**

```
100,000 operaciones, minimo O(1) siempre correcto contra el oraculo
```

## 8. Resumen

- Guardar en cada nivel el **mínimo hasta ese nivel** hace que el mínimo global viva
  siempre en el tope.
- **Invariante:** `_p[i][1] = min(valores _p[0..i])`; el tope trae el mínimo total.
- Todas las operaciones son $O(1)$ **de peor caso** (lo que pedía el ejercicio), con
  memoria $O(n)$.
