# Ejercicio 3 ★ — Pila con `minimo` en $O(1)$ en el peor caso (C3)

> Una pila con una operación `minimo` que cuesta $O(1)$ en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación.

## Especificación

Una pila de elementos de un orden total con las operaciones:

| operación | precondición | postcondición |
|---|---|---|
| `apilar(x)` | — | $x$ queda en el tope |
| `desapilar()` | pila no vacía | quita y devuelve el tope |
| `tope()` | pila no vacía | devuelve el tope sin quitarlo |
| `minimo()` | pila no vacía | devuelve el menor elemento **de los que están en la pila** |

## Diseño

Cada nodo de la pila guarda, además de su valor, **el mínimo de todos los valores desde el fondo hasta él**. La pila es una lista enlazada (cada nodo apunta al de abajo). Así cada operación hace una cantidad fija de pasos, sin redimensionar ningún arreglo.

La clase `PilaMin` implementa ese diseño. `apilar(x)` crea un nodo nuevo cuyo mínimo es el menor entre $x$ y el mínimo del nodo de arriba (o $x$, si la pila estaba vacía); `desapilar` quita el nodo de arriba; `tope` y `minimo` solo leen el nodo de arriba. Ninguna recorre la pila.

> Código: [ejercicio-03.py](ejercicio-03.py), parte 1.

## Invariante

Numeremos los nodos desde el fondo: $v_1,\dots,v_k$ son los valores (el tope es $v_k$) y $m_1,\dots,m_k$ los mínimos guardados.

$$I:\qquad m_i=\min(v_1,\dots,v_i)\quad\text{para todo } 1\le i\le k .$$

Es un invariante **de la estructura**: vale antes y después de cada operación.

- **Inicialización.** La pila vacía ($k=0$) lo cumple porque no hay nada que cumplir.
- **Mantenimiento.**
  - `apilar(x)`: los nodos $1..k$ no cambian, y sus prefijos tampoco, así que siguen cumpliendo $I$. El nodo nuevo guarda $m_{k+1}=\min(x,m_k)$ (o $x$ si $k=0$). Por $I$, $m_k=\min(v_1..v_k)$, así que $m_{k+1}=\min(v_1,\dots,v_k,x)$.
  - `desapilar()`: quita el nodo $k$. Los nodos $1..k-1$ no cambian y sus prefijos tampoco.
  - `tope()` y `minimo()` no modifican nada.
- **Consecuencia (la postcondición de `minimo`).** Con $k\ge1$, `minimo()` devuelve $m_k$, que por $I$ es $\min(v_1,\dots,v_k)$: el mínimo de toda la pila.

La clave es que una pila **solo cambia por arriba**: cada nodo ve siempre el mismo "debajo", así que el mínimo de su prefijo nunca deja de ser válido. No hay ciclos: la terminación es trivial.

## Costo

| operación | tiempo en el peor caso | qué hace |
|---|---|---|
| `apilar` | $O(1)$ | una comparación y crear un nodo |
| `desapilar` | $O(1)$ | mover un puntero |
| `tope` | $O(1)$ | leer un campo |
| `minimo` | $O(1)$ | leer un campo |

Memoria: $O(k)$, un nodo de tamaño constante por elemento (el doble que una pila normal).

**Por qué lista enlazada y no un arreglo dinámico.** Con un arreglo que duplica su capacidad (como `list` de Python), `apilar` es $O(1)$ **amortizado**, pero una operación suelta puede costar $\Theta(k)$ cuando hay que copiar. El enunciado pide peor caso, y la lista enlazada lo da.


## Casos de prueba y validación

**Caso a mano:**

> Código: [ejercicio-03.py](ejercicio-03.py), parte 2.

```text
 a5: min=5   a3: min=3   a7: min=3   a3: min=3    d: min=3    d: min=3    d: min=5   a1: min=1    d: min=5    d: min=-
```

**Pruebas al azar contra un oráculo**, comprobando el invariante en cada paso:

> Código: [ejercicio-03.py](ejercicio-03.py), parte 3.

```text
30000 operaciones al azar, invariante y oráculo sin fallos
```

**Costo constante:** medimos el tiempo de `minimo()` en pilas de distintos tamaños.

> Código: [ejercicio-03.py](ejercicio-03.py), parte 4.

```text
k =     1,000: minimo() tarda   56.1 ns por llamada
k =   100,000: minimo() tarda   60.1 ns por llamada
k = 1,000,000: minimo() tarda   56.0 ns por llamada
```

El tiempo por llamada no crece con $k$.


## Resumen

- **Estructura:** cada nodo guarda $(v_i,\ m_i)$ con $m_i=\min(v_1..v_i)$; lista enlazada.
- **Invariante:** $m_i=\min(v_1,\dots,v_i)$ para todo nodo. Se mantiene porque la pila solo cambia por arriba.
- **Costo:** `apilar`, `desapilar`, `tope`, `minimo` en $O(1)$ en el peor caso. Memoria $O(k)$.
