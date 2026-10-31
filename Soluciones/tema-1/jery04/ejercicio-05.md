# Ejercicio 5: Detección de ciclos con dos punteros (algoritmo de Floyd)

> **Enunciado.** Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo. (C3)

## 1. Especificación del problema

Antes de escribir el algoritmo hay que fijar el contrato, porque el enunciado esconde una decisión: qué quiere decir "se encuentran". Es el primer reflejo del ciclo de la conferencia 2.

**Entrada.** Una referencia `head` al primer nodo de una lista enlazada simple (posiblemente `None`). Cada nodo tiene un único campo `next`, que apunta a otro nodo o vale `None`.

**Salida.** `True` si la lista tiene un ciclo, `False` si no.

**Precondición.** Solo que la estructura esté bien formada: todo `next` es `None` o un nodo de la estructura. No se supone que la lista sea acíclica, que es justamente lo que se pregunta.

**Modelo.** Word RAM, como en la conferencia 1. Leer un campo `next`, asignar un puntero y comparar dos punteros por identidad cuestan $O(1)$. Un nodo solo se obtiene desde `head` o desde un nodo ya obtenido, leyendo su `next` (esto se usa en la cota mínima, §9).

### 1.1. La sucesión de nodos y la forma de la lista

Sea $v_0 = \texttt{head}$ y $v_{i+1} = v_i.\texttt{next}$ mientras $v_i \neq \texttt{None}$. Convenimos que, si la sucesión llega a `None`, todos los términos siguientes también valen `None`. Hay exactamente dos casos:

- **Sin ciclo.** Existe $n \geq 0$ con $v_0, \ldots, v_{n-1}$ nodos y $v_n = \texttt{None}$. Aquí $n$ es el número de nodos alcanzables.
- **Con ciclo.** La sucesión nunca llega a `None`: todos los $v_i$ son nodos.

> **Definición.** La lista *tiene un ciclo* si y solo si la sucesión $(v_i)$ nunca llega a `None`; equivalentemente (Lema 1), si existen $i < j$ con $v_i = v_j$.

Cuando hay ciclo, la lista tiene forma de $\rho$: una **cola** de $\mu$ nodos y un **ciclo** de $\lambda$ nodos. El número de nodos distintos alcanzables es $n = \mu + \lambda$.

```
 cola (μ nodos)                 ciclo (λ nodos)

 v0 → v1 → ⋯ → v(μ-1) → vμ → v(μ+1) → ⋯
                         ↑               ↓
                         v(μ+λ-1) ← ⋯ ←──┘
```

### 1.2. Qué significa "se encuentran"

Ambos punteros parten de `head`, así que en el instante $0$ ya señalan el mismo nodo. Ese instante **no cuenta**: sería un falso positivo en cualquier lista no vacía.

> **Convención.** Los punteros *se encuentran* si existe $t \geq 1$ tal que, tras $t$ iteraciones, ambos señalan el mismo nodo.

Lo que hay que demostrar es:

$$\text{los punteros se encuentran} \iff \text{la lista tiene un ciclo},$$

y, además, que el algoritmo termina siempre (correctitud total = parcial + terminación, conferencia 3).

## 2. Algoritmo

```python
def tiene_ciclo(head):
    lento = rapido = head
    while rapido is not None and rapido.next is not None:   # guarda
        lento  = lento.next             # 1 paso
        rapido = rapido.next.next       # 2 pasos
        if lento is rapido:
            return True
    return False
```

La guarda `rapido.next is not None` protege el doble salto: sin ella, `rapido.next.next` desreferenciaría `None` cuando la lista tiene longitud impar (§10 mide esto).

## 3. Lema estructural: la forma $\rho$

**Lema 1.** Si la sucesión $(v_i)$ nunca llega a `None`, existen $\mu \geq 0$ y $\lambda \geq 1$ tales que, para $i \neq j$,

$$v_i = v_j \iff i, j \geq \mu \ \text{ y } \ \lambda \mid (i - j).$$

Además, hay exactamente $n = \mu + \lambda$ nodos distintos.

**Demostración.**

*Observación (★).* Como `next` es una función, si $v_a = v_b$ entonces $v_{a+k} = v_{b+k}$ para todo $k \geq 0$.

1. Hay finitos nodos y la sucesión es infinita, así que algún nodo se repite. Sea $\mu$ el menor índice tal que $v_\mu = v_j$ para algún $j > \mu$, y sea $\mu + \lambda$ el menor $j > \mu$ con $v_j = v_\mu$.
2. Por (★) con $a = \mu$, $b = \mu + \lambda$: $v_{i+\lambda} = v_i$ para todo $i \geq \mu$. Luego $v_i = v_j$ si $i, j \geq \mu$ y $\lambda \mid (i-j)$.
3. Los nodos $v_\mu, \ldots, v_{\mu+\lambda-1}$ son distintos entre sí. Si no, sea $v_a = v_b$ con $\mu \leq a < b < \mu + \lambda$ y $d = b - a \in (0, \lambda)$. Tomamos $c$ con $k = c\lambda - (a - \mu) \geq 0$. Por (★), $v_{a+k} = v_{b+k}$; por periodicidad, $v_{a+k} = v_{\mu + c\lambda} = v_\mu$ y $v_{b+k} = v_{\mu+c\lambda+d} = v_{\mu+d}$. Entonces $v_\mu = v_{\mu+d}$ con $0 < d < \lambda$, lo que contradice la minimalidad de $\lambda$.
4. Los nodos $v_0, \ldots, v_{\mu-1}$ no se repiten (ni entre sí ni con ningún otro) por la minimalidad de $\mu$.
5. Para $i \geq \mu$, $v_i = v_{\mu + ((i-\mu) \bmod \lambda)}$. Como esos $\lambda$ nodos son distintos, $v_i = v_j \iff (i - \mu) \equiv (j - \mu) \pmod{\lambda} \iff \lambda \mid (i-j)$. Si $i < \mu$, $v_i$ no coincide con ningún otro $v_j$. ∎

**Observación.** Si la sucesión llega a `None` en $n$, los $v_0, \ldots, v_{n-1}$ son distintos: un repetido $v_i = v_j$ ($i<j$) haría la sucesión periódica por (★) y nunca llegaría a `None`. Esto cierra la equivalencia de la definición: *llega a `None`* $\iff$ *no hay $i<j$ con $v_i = v_j$*.

## 4. Invariante (correctitud parcial)

### 4.1. El primer invariante y por qué no alcanza

El primer intento natural es:

> *"`lento` y `rapido` siempre señalan nodos de la lista."*

Es verdadero y se prueba en una línea, pero es el invariante vacío: no relaciona un puntero con el otro, así que no dice nada sobre si coinciden, ni cuándo. Es la lección de la conferencia 3: un invariante tiene que ser inductivo y, además, **suficiente para concluir**. Aquí hay que cuantificar dónde está cada puntero.

### 4.2. El invariante

Sea $t$ el número de iteraciones completadas al evaluar la guarda.

> **$I(t)$.** $\texttt{lento} = v_t$ y $\texttt{rapido} = v_{2t}$.

En particular, `rapido` está exactamente $t$ pasos por delante de `lento`: $\texttt{rapido} = \texttt{next}^{\,t}(\texttt{lento})$. La **brecha** crece exactamente $1$ por iteración (la diferencia de velocidades), y esa es la cantidad que gobierna el encuentro.

### 4.3. Demostración en tres pasos

**Inicialización ($t = 0$).** `lento = rapido = head = `$v_0 = v_{2\cdot 0}$. ✔

**Mantenimiento.** Supongamos $I(t)$ y que la guarda es verdadera: $v_{2t} \neq \texttt{None}$ y $v_{2t+1} = v_{2t}.\texttt{next} \neq \texttt{None}$.

- Como la sucesión llega a `None` a lo sumo una vez y $v_{2t}$ es nodo, todos los $v_i$ con $i \leq 2t$ son nodos; en particular $v_t$ lo es y `lento.next` es válido.
- `lento = lento.next` $= v_t.\texttt{next} = v_{t+1}$.
- `rapido = rapido.next.next` $= v_{2t+1}.\texttt{next} = v_{2t+2}$. El segundo `.next` es seguro porque $v_{2t+1} \neq \texttt{None}$ (es lo que dice la guarda).

Tras el cuerpo, $\texttt{lento} = v_{t+1}$ y $\texttt{rapido} = v_{2(t+1)}$: vale $I(t+1)$. ✔

**Conclusión.** El algoritmo tiene dos salidas.

- **Salida `return True` en la iteración $t \geq 1$.** La guarda de la iteración anterior aseguró que $v_{2t-1}$ es nodo, y $t \leq 2t - 1$, así que $\texttt{lento} = v_t$ es un nodo. La condición `lento is rapido` dice $v_t = v_{2t}$ con $t < 2t$: existen $i < j$ con $v_i = v_j$. Por definición, **hay ciclo**.
- **Salida `return False` por la guarda.** Por $I(t)$, $\texttt{rapido} = v_{2t}$. La guarda es falsa si $v_{2t} = \texttt{None}$ o $v_{2t+1} = \texttt{None}$, y en ambos casos la sucesión llegó a `None`: **no hay ciclo**.

Por tanto, **si el algoritmo termina, su respuesta es correcta**. Falta la terminación y, dentro de ella, el sentido "$\Leftarrow$" del enunciado: que con ciclo los punteros efectivamente se encuentran. ✔

## 5. Cuándo se encuentran

**Lema 2.** Si la lista tiene ciclo, con parámetros $(\mu, \lambda)$, para todo $t \geq 1$:

$$v_t = v_{2t} \iff t \geq \mu \ \text{ y } \ \lambda \mid t.$$

**Demostración.** Como $t \geq 1$, es $t \neq 2t$. Por el Lema 1, $v_t = v_{2t}$ si y solo si $t, 2t \geq \mu$ y $\lambda \mid (2t - t) = t$. Como $2t \geq t$, la condición "$t, 2t \geq \mu$" equivale a $t \geq \mu$. ∎

**Corolario (primer encuentro).** El primer instante de encuentro es

$$t^* = \min\{\, t \geq 1 : t \geq \mu,\ \lambda \mid t \,\} = \lambda \cdot \max\!\left(1, \left\lceil \tfrac{\mu}{\lambda} \right\rceil\right),$$

y cumple

$$\frac{n}{2} \;\leq\; t^* \;\leq\; n, \qquad \text{con } t^* = n \text{ si } \mu = 0 \text{ y } t^* \leq n - 1 \text{ si } \mu \geq 1.$$

*Justificación.*

- Si $\mu = 0$: $t^* = \lambda = n$.
- Si $\mu \geq 1$: $t^* = \mu + \delta$ con $\delta = (-\mu) \bmod \lambda \in [0, \lambda - 1]$, así que $\mu \leq t^* \leq \mu + \lambda - 1 = n - 1$.
- Cota inferior: $t^*$ es un múltiplo positivo de $\lambda$ y además $t^* \geq \mu$, luego $t^* \geq \max(\mu, \lambda) \geq (\mu + \lambda)/2 = n/2$.

**Intuición ($\mu \geq 1$).** Hacen falta $\mu$ iteraciones para que `lento` entre al ciclo (cuando entra, `rapido` ya está dentro) y $\delta$ iteraciones más para que `rapido` cierre la brecha.

## 6. Potencial (terminación)

La terminación se demuestra con un potencial entero, no negativo y estrictamente decreciente, como en Gale-Shapley (conferencia 3). Hay que tratar los dos casos de forma de la lista.

### 6.1. Sin ciclo

$$\Phi(t) = n - 2t,$$

los pasos que le faltan a `rapido` $= v_{2t}$ para llegar a `None` $= v_n$.

- **Entero.** Sí.
- **No negativo.** La guarda es verdadera si y solo si $v_{2t+1} \neq \texttt{None}$, es decir, $2t + 1 \leq n - 1$, es decir, $\Phi(t) \geq 2$. Por tanto, cada vez que se entra al cuerpo, $\Phi(t+1) = \Phi(t) - 2 \geq 0$.
- **Decrece estrictamente:** exactamente $2$ por iteración.

El ciclo `while` se detiene cuando $\Phi(t) \in \{0, 1\}$, o sea, tras exactamente

$$\left\lfloor \frac{n}{2} \right\rfloor \text{ iteraciones}.$$

Por la conclusión del invariante, en este caso nunca se ejecuta `return True`: devuelve `False`. ✔

### 6.2. Con ciclo

La guarda es siempre verdadera (ningún $v_i$ es `None`), así que la única salida es `return True`. Sea $t^*$ el primer encuentro del Corolario y definamos

$$\Phi(t) = t^* - t, \qquad 0 \leq t \leq t^*.$$

- **Entero y no negativo** en el rango, y **decrece exactamente $1$** por iteración.
- **Llega a $0$ con la prueba de igualdad verdadera:** por el Lema 2, $v_{t^*} = v_{2t^*}$, así que en la iteración $t^*$ se ejecuta `return True`.
- **No hay salida prematura:** por la minimalidad de $t^*$ y el Lema 2, para $1 \leq t < t^*$ se tiene $v_t \neq v_{2t}$.

El contenido real de esta prueba no está en la resta sino en el Lema 2: es él quien garantiza que el potencial toca el $0$ con el encuentro, y que no se puede "saltar" sobre la tortuga sin coincidir.

**Interpretación (la brecha).** Para $t \geq \mu$ ambos punteros están en el ciclo. La distancia, avanzando por el ciclo, de `rapido` a `lento` es $d_t = (-t) \bmod \lambda$, y $d_{t+1} = (d_t - 1) \bmod \lambda$. Mientras $d_t > 0$, la brecha baja exactamente $1$ por iteración, y los punteros coinciden cuando $d_t = 0$. Por eso no hay "salto": la diferencia de velocidades es exactamente $1$.

## 7. El teorema

**Teorema.** Para toda lista, `tiene_ciclo` termina, y

$$\texttt{tiene\_ciclo(head)} = \texttt{True} \iff \text{los punteros se encuentran} \iff \text{la lista tiene un ciclo.}$$

**Demostración.**

- *Termina:* §6.1 (sin ciclo) y §6.2 (con ciclo).
- *Se encuentran $\Rightarrow$ hay ciclo:* conclusión del invariante, salida `return True`.
- *Hay ciclo $\Rightarrow$ se encuentran:* la guarda nunca falla, y por el Lema 2 y el Corolario los punteros coinciden por primera vez en $t^*$, donde el algoritmo devuelve `True`.
- *No hay ciclo $\Rightarrow$ no se encuentran:* es la contrapositiva del primer sentido; el algoritmo devuelve `False` tras $\lfloor n/2 \rfloor$ iteraciones. ∎

## 8. Costo

Contamos operaciones elementales del word RAM por iteración completa:

| Fragmento | Operaciones | Costo |
|---|---|---|
| Inicialización | 2 asignaciones | 2 |
| Guarda | 1 lectura de `next`, 2 comparaciones con `None` | 3 |
| Cuerpo | 3 lecturas de `next`, 2 asignaciones, 1 comparación `is` | 6 |
| **Iteración completa** | 4 lecturas, 3 comparaciones, 2 asignaciones | **9** |

El número de iteraciones depende de la forma de la lista:

| Caso | Iteraciones | Tiempo |
|---|---|---|
| Sin ciclo, $n$ nodos | exactamente $\lfloor n/2 \rfloor$ | $9\lfloor n/2 \rfloor + O(1)$ |
| Con ciclo $(\mu, \lambda)$, $n = \mu + \lambda$ | exactamente $t^*$, con $n/2 \leq t^* \leq n$ | $9\,t^* + O(1) \in [4{,}5\,n,\ 9\,n] + O(1)$ |

Por tanto:

$$T(n) = \Theta(n) \text{ en todos los casos, y } T(n) \leq 9n + O(1) \text{ en el peor caso.}$$

Como en el máximo de la conferencia 5, el costo no depende de la suerte: está pegado a $n$ por ambos lados. Aquí $n$ es el número de nodos *distintos* alcanzables, no la "longitud" de la lista (que con ciclo sería infinita). En bits, la entrada ocupa $\Theta(n \cdot w)$ con palabras de $w$ bits, así que el algoritmo es lineal en el tamaño de la entrada.

**Memoria extra.** $O(1)$ palabras: los dos punteros. No modifica la lista.

Comparación con las alternativas:

| Método | Tiempo | Memoria extra | Modifica la lista |
|---|---|---|---|
| Floyd (dos punteros) | $\Theta(n)$ determinista | $O(1)$ | no |
| Conjunto de visitados (tabla hash) | $\Theta(n)$ esperado | $\Theta(n)$ | no |
| Marcar los nodos visitados | $\Theta(n)$ | 1 bit por nodo | sí |

## 9. Cota mínima (con su modelo)

Una cota mínima es una afirmación sobre un modelo (conferencia 2). Fijamos el **modelo de punteros**: el algoritmo conoce `head`; solo puede obtener un nodo leyendo el `next` de otro ya obtenido; puede comparar nodos por igualdad pero no fabricar direcciones. El costo es el número de lecturas de `next`.

**Teorema.** Todo algoritmo determinista que decide si una lista de $n \geq 1$ nodos alcanzables tiene un ciclo hace al menos $n$ lecturas de `next` en el peor caso.

**Demostración (adversario).** Consideremos dos listas con nodos $u_0, \ldots, u_{n-1}$ y $u_i.\texttt{next} = u_{i+1}$ para $i < n - 1$:

- $L_0$: $u_{n-1}.\texttt{next} = \texttt{None}$ (sin ciclo).
- $L_1$: $u_{n-1}.\texttt{next} = u_0$ (con ciclo).

Son idénticas salvo en el campo $u_{n-1}.\texttt{next}$. El adversario responde cada lectura de $u_i.\texttt{next}$, con $i < n-1$, con un nodo nuevo, igual en ambas listas. Al principio el algoritmo solo conoce $u_0$, y cada lectura le revela como mucho un nodo nuevo, el siguiente. Para conocer $u_{n-1}$ necesita leer $u_0.\texttt{next}, \ldots, u_{n-2}.\texttt{next}$: $n - 1$ lecturas. Así que la primera lectura que distingue $L_0$ de $L_1$ es, como pronto, la número $n$. Si el algoritmo se detiene antes, vio exactamente lo mismo en ambas listas y da la misma respuesta, que es incorrecta en una de las dos. ∎

**Conclusión.** Floyd hace a lo sumo $4n$ lecturas ($4$ por iteración, $\leq n$ iteraciones), frente a la cota de $n$: es **óptimo salvo un factor constante** en el modelo de punteros. La cota deja fuera, por ejemplo, listas almacenadas en un arreglo donde se pueda acceder a direcciones arbitrarias.

## 10. Experimento

Siguiendo la conferencia 3, el invariante se vigila en ejecución antes de confiar en él. El código siguiente construye listas con $\mu$ y $\lambda$ dados, comprueba $I(t)$ en cada guarda y compara el número de iteraciones con las fórmulas $\lfloor n/2 \rfloor$ y $t^*$.

```python
from math import ceil

class Nodo:
    __slots__ = ("next",)
    def __init__(self):
        self.next = None

def construir(mu, lam):
    """lam = 0: lista sin ciclo de mu nodos.  lam >= 1: cola de mu nodos + ciclo de lam nodos."""
    nodos = [Nodo() for _ in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.next = b
    if lam > 0:
        nodos[-1].next = nodos[mu]
    return nodos

def floyd(head):
    """Devuelve (hay_ciclo, iteraciones)."""
    lento = rapido = head
    t = 0
    while rapido is not None and rapido.next is not None:
        lento = lento.next
        rapido = rapido.next.next
        t += 1
        if lento is rapido:
            return True, t
    return False, t

def v(head, i):
    """El i-ésimo elemento v_i de la sucesión (None si la lista terminó antes)."""
    x = head
    for _ in range(i):
        if x is None:
            return None
        x = x.next
    return x

def floyd_vigilado(head):
    """Igual que floyd, pero comprueba I(t): lento = v_t y rapido = v_2t en cada guarda."""
    lento = rapido = head
    t = 0
    while True:
        assert lento is v(head, t) and rapido is v(head, 2 * t), f"I({t}) roto"
        if not (rapido is not None and rapido.next is not None):
            return False, t
        lento, rapido = lento.next, rapido.next.next
        t += 1
        if lento is rapido:
            return True, t

def t_estrella(mu, lam):
    return lam * max(1, ceil(mu / lam))

# Con ciclo: todas las formas (mu, lam), 0 <= mu <= 40, 1 <= lam <= 40
for mu in range(41):
    for lam in range(1, 41):
        n, ts = mu + lam, t_estrella(mu, lam)
        assert floyd(construir(mu, lam)[0]) == (True, ts)
        assert n / 2 <= ts <= n and (ts == n if mu == 0 else ts <= n - 1)

# Sin ciclo: longitudes 0..200
for n in range(201):
    nodos = construir(n, 0)
    assert floyd(nodos[0] if nodos else None) == (False, n // 2)

# Invariante vigilado en 256 listas pequeñas (incluye la vacía y el autolazo)
for mu in range(16):
    for lam in range(16):
        nodos = construir(mu, lam)
        head = nodos[0] if nodos else None
        assert floyd_vigilado(head)[0] == (lam > 0)

print("todo correcto")
```

**Resultados** (ejecutado):

| Comprobación | Casos | Resultado |
|---|---|---|
| Con ciclo: iteraciones $= t^*$ y $n/2 \leq t^* \leq n$ | 1640 formas $(\mu, \lambda)$ | se cumple en todas |
| Sin ciclo: iteraciones $= \lfloor n/2 \rfloor$ | 201 longitudes ($n = 0..200$) | se cumple en todas |
| Invariante $I(t)$ vigilado en cada guarda | 256 listas | nunca se rompe |

Casos borde cubiertos: lista vacía ($n = 0$), un solo nodo sin ciclo, un nodo que apunta a sí mismo ($\mu = 0$, $\lambda = 1$) y ciclo sin cola ($\mu = 0$).

Algunos ejemplos de la fórmula $t^*$:

| $(\mu, \lambda)$ | $n$ | $t^*$ | iteraciones medidas |
|---|---|---|---|
| $(0, 7)$ | 7 | 7 | 7 |
| $(5, 3)$ | 8 | 6 | 6 |
| $(12, 5)$ | 17 | 15 | 15 |
| $(10, 1)$ | 11 | 10 | 10 |
| $(1, 100)$ | 101 | 100 | 100 |

### 10.1. Dos variantes con error plantado

Como en las conferencias 2 a 5, plantamos errores en variantes que parecen correctas y vemos qué detectan las pruebas.

| Variante | Qué cambia | Listas con ciclo (1640) | Sin ciclo, $n$ par (101) | Sin ciclo, $n$ impar (100) |
|---|---|---|---|---|
| **A** | la guarda es solo `rapido is not None` | 0 fallos | 0 fallos | **100 fallos** (se desreferencia `None.next`) |
| **B** | se compara `lento is rapido` *antes* de mover | 0 fallos | **100 fallos** | **99 fallos** (falsos positivos; solo pasan $n = 0$ y $n = 1$) |

Las dos variantes superan por completo una suite que solo pruebe listas con ciclo, que es lo primero que uno escribe para probar un detector de ciclos. La demostración dice dónde mirar:

- **A:** el paso de mantenimiento usa que $v_{2t+1} \neq \texttt{None}$ para que `rapido.next.next` sea seguro. Quitar esa cláusula rompe el invariante justo en las listas de longitud impar.
- **B:** la convención de §1.2 y el Lema 2 exigen $t \geq 1$. En $t = 0$ los punteros coinciden trivialmente, así que esa comparación no distingue nada.

## 11. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Decidir si la sucesión $v_0, v_1, \ldots$ de una lista enlazada llega a `None` o se repite. Modelo: word RAM con punteros. |
| ¿Qué algoritmo? | Floyd: `lento` avanza $1$, `rapido` avanza $2$ por iteración; se compara tras mover. |
| ¿Es correcto? | **Invariante** $I(t)$: $\texttt{lento} = v_t$, $\texttt{rapido} = v_{2t}$. **Potencial**: $n - 2t$ sin ciclo, $t^* - t$ con ciclo. Lema 2: $v_t = v_{2t} \iff t \geq \mu \wedge \lambda \mid t$. |
| ¿Cuánto cuesta? | $\lfloor n/2 \rfloor$ iteraciones sin ciclo; $t^*$ con ciclo, con $n/2 \leq t^* \leq n$. Tiempo $\Theta(n)$ y memoria $O(1)$. |
| ¿Se puede mejor? | No asintóticamente: $\Omega(n)$ lecturas de `next` por adversario en el modelo de punteros. Floyd usa a lo sumo $4n$. |
