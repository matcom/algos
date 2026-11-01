# Pregunta 3: 

Una pila con una operación mínimo que cuesta O(1) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación.

**Planteamiento.** Queremos un TAD pila que soporte las operaciones `push(x)` (apilar `x`), `pop()` (desapilar y devolver el tope), `top()` (devolver el tope sin quitarlo) y `min()` (devolver el menor elemento actualmente en la pila). La dificultad es que el mínimo cambia al hacer `pop`: si apilas `[5, 3, 8]` el mínimo es `3`; si haces `pop` dos veces, el mínimo pasa a ser `5`, y recalcular el mínimo tras cada `pop` recorriendo la pila costaría `Θ(n)`. Necesitamos, por tanto, que la pila “recuerde” cuál era el mínimo en cada momento del pasado. La idea central es que el mínimo de una pila es una función del prefijo de la pila (de la base hasta cada posición); como `push`/`pop` solo modifican el extremo, los prefijos intermedios nunca cambian mientras existan, así que basta guardar el mínimo de cada prefijo.

### 1. Diseño de la estructura

Cada nodo guarda dos cosas: el valor y el mínimo de todo lo que hay de él hacia la base (incluyéndolo).

```
Nodo = ⟨ val : T,  m : T ⟩
Pila = lista enlazada simple, con puntero `cima`

Estado: cima : Nodo* (nulo si la pila está vacía).
```

**Pseudocódigo.**

```
push(x):
    si cima = nil:
        m ← x
    sino:
        m ← menor(x, cima.m)
    cima ← nuevo Nodo⟨val = x, m = m, sig = cima⟩

pop():
    pre: cima ≠ nil
    x ← cima.val
    cima ← cima.sig
    devolver x

top():
    pre: cima ≠ nil
    devolver cima.val

min():
    pre: cima ≠ nil
    devolver cima.m
```

**Traza** (se ve la idea de un vistazo).

```
push(5)   push(3)   push(8)   push(2)      pop()  pop()

                      [8 | m=3]  [2 | m=2]
          [3 | m=3]   [3 | m=3]  [8 | m=3]  [8|3]
[5 | m=5] [5 | m=5]   [5 | m=5]  [3 | m=3]  [3|3]  [3|3]  ← min() = 3
                                 [5 | m=5]  [5|5]  [5|5]
 min=5     min=3       min=3      min=2     min=3  → sigue 3
```

Observa que al hacer `pop` del `2` el mínimo "vuelve" a `3` sin calcular nada: ese `3` ya estaba escrito en el nodo de abajo.

### 2. El invariante

Sea la pila con elementos, de la base a la cima, $a_1, a_2, \dots, a_n$ y sea $m_i$ el campo `m` del nodo que contiene a $a_i$.

$$
\boxed{\;\text{INV}(P):\quad \forall\, i \in \{1,\dots,n\}:\; m_i = \min\{a_1, a_2, \dots, a_i\}\;}
$$

En palabras: el campo `m` de cada nodo es el mínimo del segmento que va desde la base hasta ese nodo.

**Corolario (lo que da la corrección de `min`).** Si $n \ge 1$, entonces $m_n = \min\{a_1,\dots,a_n\}$, que es exactamente el mínimo de toda la pila. Por eso `min()` solo lee `cima.m`.

### 3. Demostración formal de corrección

Demostramos que `INV` se cumple siempre, por inducción sobre la secuencia de operaciones. Esto es el esquema clásico de invariante de representación: base + preservación por cada operación que modifica el estado.

**Inicialización (pila vacía).** Al crear la pila, $n = 0$. El cuantificador $\forall i \in \emptyset$ es vacuamente verdadero. ∎

**Conservación por `push(x)`.** Hipótesis: `INV` vale para $P = \langle a_1,\dots,a_n\rangle$. Después de `push(x)`: la pila es $\langle a_1,\dots,a_n, a_{n+1}\rangle$ con $a_{n+1}=x$. Hay que verificar los $n+1$ nodos:

- **(a) Nodos $i \le n$.** `push` no los toca: ni su `val` ni su `m`. Su segmento $\{a_1,\dots,a_i\}$ tampoco cambió. Luego $m_i = \min\{a_1..a_i\}$ sigue valiendo por hipótesis.
- **(b) Nodo nuevo $i = n+1$.** Dos casos según el código:
  - Si $n = 0$: el código asigna $m_1 = x$. Y $\min\{a_1\} = \min\{x\} = x$. ✓
  - Si $n \ge 1$: el código asigna $m_{n+1} = \min(x,\, m_n)$. Por hipótesis, $m_n = \min\{a_1..a_n\}$. Entonces:
    $$
    m_{n+1} = \min\bigl(x,\ \min\{a_1,\dots,a_n\}\bigr) = \min\{a_1,\dots,a_n, x\} = \min\{a_1,\dots,a_{n+1}\}
    $$
    La igualdad central usa que `min` es asociativa y conmutativa (el mínimo de una unión es el mínimo de los mínimos). ✓

Los $n+1$ nodos cumplen `INV`. ∎

**Conservación por `pop()`.** Hipótesis: `INV` vale para $\langle a_1,\dots,a_n\rangle$, con $n\ge1$. Después de `pop()`: la pila es $\langle a_1,\dots,a_{n-1}\rangle$. `pop` solo elimina el nodo $n$ y no modifica ninguno de los restantes. Para cada $i \le n-1$, el nodo conserva su $m_i$ y su segmento $\{a_1..a_i\}$ es el mismo, así que $m_i=\min\{a_1..a_i\}$ sigue valiendo por hipótesis. (Si $n-1=0$ queda vacuamente cierto.) ∎

> **Aquí está el corazón de la demostración.** `pop` es "gratis" porque `INV` es una propiedad de prefijos, y quitar el último elemento no altera ningún prefijo anterior. Eso es lo que falla en una pila con un solo campo `min` global: ese valor depende de toda la pila y `pop` lo invalida.

**`top` y `min` son observadoras.** No modifican el estado ⇒ preservan `INV` trivialmente. Su corrección funcional:
- `top()` devuelve `cima.val` $= a_n$, el tope por definición.
- `min()` devuelve $m_n = \min\{a_1..a_n\}$ por `INV` con $i=n$. ∎

**Conclusión.** Por inducción sobre el número de operaciones, `INV` es verdadero en todo estado alcanzable, y por tanto `min()` es siempre correcta. $\blacksquare$

### 4. Costos (peor caso)

Cada operación ejecuta un número constante de pasos elementales, independiente de $n$:

| Operación | Qué hace | Costo peor caso |
|-----------|----------|-----------------|
| `push` | 1 comparación + 1 alocación + 2 asignaciones | $\Theta(1)$ |
| `pop` | leer, mover puntero | $\Theta(1)$ |
| `top` | leer un campo | $\Theta(1)$ |
| `min` | leer un campo | $\Theta(1)$ |

**Justificación.** No hay bucles ni recursión en ninguna operación. Por eso el costo es $O(1)$ en el peor caso real, no amortizado ni esperado. Esto importa: una cola con dos pilas, por ejemplo, solo da $O(1)$ amortizado. Aquí el límite es duro, operación por operación.

**Espacio.** $\Theta(n)$ nodos, cada uno con 2 valores + 1 puntero, es decir, un factor constante (≈ 2×) sobre una pila normal.

Aquí tienes la sección final redactada con rigor técnico y claridad didáctica, lista para ser integrada al final de tu documento. Explica detalladamente qué hace tu código en Python y cómo construye el material visual (`pila_min.gif` y `pila_min_explicacion.png`).

---

### 5. Implementación y Visualización Gráfica en Python 

Para complementar el análisis teórico y facilitar una comprensión intuitiva del comportamiento de la estructura, el script en Python adjunto en la carpeta extra 03 genera **dos recursos visuales didácticos** utilizando la librería `Pillow` (PIL):

1. **`pila_min.gif`**: Una animación fotograma a fotograma que simula una secuencia real de operaciones (`push` y `pop`), mostrando cómo evoluciona la pila, el desplazamiento de la cima y la actualización instantánea del mínimo.
2. **`pila_min_explicacion.png`**: Una infografía estática tipo resumen que desglosa la anatomía del nodo y el mantenimiento del invariante con una pila de ejemplo de cuatro elementos.

