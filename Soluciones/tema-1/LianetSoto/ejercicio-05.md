# Ejercicio 5 — Detección de ciclos en una lista enlazada (algoritmo de Floyd)

> ★★ Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo. (C3)

---

## 1. El problema y su especificación

**Problema.** Dada una lista enlazada simple, decidir si tiene un ciclo. Si lo tiene, devolver el nodo donde empieza el ciclo (el primer nodo que se visita infinitamente al recorrerla). Si no lo tiene, devolver `None`.

**Modelo.** Cada nodo tiene un campo `next` que apunta al siguiente nodo o a `None`. Contamos **pasos** como avances de puntero: un paso es una asignación `p = p.next`. La comparación de dos punteros cuesta 1.

**Especificación (contrato).**

- **Precondición.** La entrada es un nodo `cabeza` de una lista enlazada simple, o `None`. La lista puede o no tener un ciclo.
- **Postcondición.** El valor devuelto `r` cumple:
  - `r = None` y la lista no tiene ciclo, o
  - `r` es el nodo de entrada del ciclo, es decir, el primer nodo que se repite al recorrer la lista.

**Recordatorio del algoritmo de Floyd.** Dos punteros, `lento` y `rapido`, arrancan en la cabeza. En cada paso, `lento` avanza uno y `rapido` avanza dos. Si hay ciclo, se encuentran dentro del ciclo. Después, para encontrar la entrada del ciclo, se pone un puntero en la cabeza y se avanza uno a uno junto con `lento`; el punto donde se encuentran es la entrada del ciclo.

---

## 2. La lista enlazada y la notación

Representamos la lista con nodos:

```python
class Nodo:
    __slots__ = ("valor", "next")
    def __init__(self, valor, next=None):
        self.valor = valor
        self.next = next
```

Si la lista tiene un ciclo, la escribimos como:

```text
cabeza → x₀ → x₁ → … → x_{μ-1} → x_μ → x_{μ+1} → … → x_{μ+λ-1} → x_μ → …
                                    ↑                             │
                                    └─────────────────────────────┘
```

- `μ` = longitud del **tramo** (número de nodos antes de entrar al ciclo). Puede ser 0.
- `λ` = longitud del **ciclo** (número de nodos en el ciclo). Siempre `λ ≥ 1`.
- `x_μ` = **entrada del ciclo** (el nodo que hay que devolver).

Si no hay ciclo, la lista termina en `None`.

Convención sobre posiciones. Definimos la "posición i" de la siguiente forma:
```text
posición i = x_i                         si i < μ       (en el tramo)
posición i = x_{μ + (i−μ) mod λ}         si i ≥ μ       (en el ciclo)
```
Es decir: el tramo no se repite; solo el ciclo se repite, con período `λ`. Por ejemplo, con `μ = 2`, `λ = 4`:
```text
posición 0 → A       posición 4 → E       posición 8 → E
posición 1 → B       posición 5 → F       posición 9 → F
posición 2 → C       posición 6 → C       posición 10 → C
posición 3 → D       posición 7 → D       posición 11 → D
```

---

## 3. El algoritmo

```python
def detectar_ciclo(cabeza):
    lento = rapido = cabeza
    # Fase 1: ¿se encuentran?
    while rapido is not None and rapido.next is not None:
        lento = lento.next
        rapido = rapido.next.next
        if lento is rapido:
            break
    else:
        return None                     # rapido llegó a None: no hay ciclo

    # Fase 2: encontrar la entrada del ciclo
    lento = cabeza
    while lento is not rapido:
        lento = lento.next
        rapido = rapido.next
    return lento
```


---

## 4. Invariante de la fase 1: ¿qué se mantiene?

El invariante de Floyd no es que los punteros estén a cierta distancia; es la **forma del recorrido**. 

**Convención.** Decimos que `lento` está en la posición `i` si ha avanzado `i` pasos desde la cabeza. Análogamente para `rapido`.

**Lema 1 (los punteros están donde dice el conteo).** Después de `k` vueltas de la fase 1, `lento` ha avanzado `k` pasos y `rapido` ha avanzado `2k` pasos.

**Demostración.** Por inducción sobre `k`. 
- Base k = 0: ambos punteros están en cabeza = x_0, que es la posición 0. La afirmación es trivial.

- Paso inductivo: supongamos que tras k vueltas lento está en la posición k y rapido en la posición 2k. En la vuelta k+1, el algoritmo hace lento = lento.next (avanza 1 posición) y rapido = rapido.next.next (avanza 2 posiciones). Por la definición de "posición", un next incrementa la posición en 1 (y respeta el período λ dentro del ciclo). Por tanto, tras la vuelta k+1, lento está en la posición k+1 y rapido en la posición 2k+2 = 2(k+1). □

**Invariante `I₁(k)`.** Después de `k` vueltas de la fase 1, si la lista tiene ciclo, entonces:

1. `lento` está en la posición `k`.
2. `rapido` está en la posición `2k`.
3. Además, `lento` y `rapido` están ambos dentro de la lista, es decir, ni `rapido` ni `rapido.next` son `None`.

### 4.1. Inicialización

Antes de la primera vuelta, `k = 0`. `lento = rapido = cabeza = x_0`, así que las posiciones son `0` y `0 = 2·0`. La lista tiene ciclo, así que `rapido` nunca es `None` y `rapido.next` tampoco. ✔

### 4.2. Mantenimiento

Supongamos `I₁(k)`. El algoritmo avanza `lento` una posición y `rapido` dos. Por el Lema 1, quedan en posiciones `k+1` y `2k+2 = 2(k+1)`. Como hay ciclo, las asignaciones son válidas (no se llega a `None`), así que `I₁(k+1)` se cumple. ✔

### 4.3. Conclusión

Cuando la fase 1 termina con `break`, `lento is rapido`. Por el invariante, después de `k` vueltas, `lento` está en la posición `k` y `rapido` en la posición `2k`. La igualdad de punteros implica:

```text
posición k = posición 2k
```

Si ambos están dentro del ciclo (lo cual ocurre si `k ≥ μ` y `2k ≥ μ`), esta igualdad significa:

```text
μ + (k − μ) mod λ  =  μ + (2k − μ) mod λ
     (k − μ) mod λ  =      (2k − μ) mod λ
               k    ≡  2k  (mod λ)
               k    ≡  0   (mod λ)
```
Es decir, `k` es un múltiplo de `λ`.

Si el ciclo `while` termina sin `break`, entonces `rapido is None` o `rapido.next is None`, lo que significa que la lista se acabó: no hay ciclo. El `else` del `while` lo detecta y devuelve `None`.

---

## 5. Teorema de la fase 1: hay ciclo ⇔ se encuentran

**Teorema 1.** Si la lista tiene ciclo (`μ ≥ 0, λ ≥ 1`), la fase 1 termina con `lento is rapido` en exactamente `k*` vueltas, donde `k*` es el menor entero positivo tal que:

```text
k* ≥ μ    y    k* ≡ 0 (mod λ).
```

Además, `k* ≤ μ + λ ≤ n`.

**Demostración**. Sea `k*` como en el enunciado. Veamos que existe y está acotado:

    Si μ = 0: k* = λ, que cumple k* ≥ 0 = μ y k* ≡ 0 (mod λ).

    Si μ ≥ 1: k* = λ · ⌈μ/λ⌉. Este es el menor múltiplo de λ que es ≥ μ. Además k* < λ · (μ/λ + 1) = μ + λ.

En ambos casos, k* ≤ μ + λ. Como μ + λ ≤ n (el número total de nodos distintos en una lista con ciclo es exactamente μ + λ), tenemos k* ≤ n.

Ahora veamos que en la vuelta k* los punteros coinciden. Por el Lema 1, lento está en la posición k* y rapido en la posición 2k*. Como k* ≥ μ y 2k* ≥ k* ≥ μ, ambos están en el ciclo. Sus posiciones dentro del ciclo son:

```text
lento:  (k* − μ) mod λ  =  (−μ) mod λ        (porque k* ≡ 0 mod λ)
rápido: (2k* − μ) mod λ =  (−μ) mod λ        (ídem)
```

Son iguales. Por tanto `lento is rapido` y el `break` se ejecuta en la vuelta `k*`. ✔

¿Es `k*` el primer momento del encuentro? Sí. Si `lento is rapido` en alguna vuelta `k ≥ 1`, entonces `k ≡ 0 (mod λ)` y ambos están en el ciclo (es decir, `k ≥ μ`). Por definición, `k*` es el menor positivo que cumple ambas condiciones. Así que no puede haber encuentro antes de `k*`. ✔

Caso sin ciclo. Si no hay ciclo, la lista es finita y termina en `None`. `rapido` avanza dos posiciones por vuelta, así que después de `⌈n/2⌉` vueltas llega a `None` o a un nodo cuyo `next` es `None`. La condición `rapido is not None` and `rapido.next is not None` falla y el ciclo termina sin `break`. El `else` del `while` se ejecuta y devuelve `None`. ✔


---
## 6. Potencial de la fase 1: por qué termina

La fase 1 termina en los dos casos, pero la demostración es distinta según haya ciclo o no.

### 6.1. Caso sin ciclo

**Potencial `Φ₁(k) = n − pos(rapido)`**, donde `n` es el número de nodos de la lista y `pos(rapido)` es la posición actual de `rapido`, contada en pasos desde la cabeza.

Propiedades:

- **Entero no negativo.** `pos(rapido) ≤ n` siempre (la lista tiene `n` nodos y termina en `None`), así que `Φ₁(k) ≥ 0`.
- **Decrece en 2 por vuelta.** `rapido` avanza 2 posiciones, así que `Φ₁(k+1) = Φ₁(k) − 2`.
- **Llega a 0 cuando `rapido` sale de la lista.** Cuando `rapido` llega a `None` (o a un nodo con `next = None`), la condición del ciclo falla y la fase 1 termina.

Por tanto, la fase 1 ejecuta a lo sumo `⌈n/2⌉` vueltas antes de que `rapido` llegue al final. El potencial es un entero no negativo que baja estrictamente en cada vuelta, así que el ciclo termina.

### 6.2. Caso con ciclo

En el caso con ciclo **no hay un potencial monótono natural**: `rapido` da vueltas al ciclo y la distancia entre los punteros cicla con período `λ`. Sin embargo, el Teorema 1 da una **cota explícita** del número de vueltas: la fase 1 se detiene exactamente en la vuelta `k*`, donde

```text
k* = λ · ⌈μ / λ⌉   (o k* = λ si μ = 0),
```
y `k* ≤ μ + λ ≤ n`.

Potencial `Φ₁(k) = k* − k`, donde `k*` es el instante de encuentro del Teorema 1.

Propiedades:

    Entero no negativo para k ≤ k*. Φ₁(k) ≥ 0 mientras el ciclo no ha terminado. La cota k* ≤ μ + λ ≤ n garantiza que Φ₁ no se vuelve negativa antes del encuentro.

    Decrece en 1 por vuelta. Φ₁(k+1) = k* − (k+1) = Φ₁(k) − 1.

    Llega a 0 en la vuelta k*. En ese momento lento is rapido (Teorema 1), el break se ejecuta y el ciclo termina.

Por tanto, la fase 1 ejecuta exactamente `k`* vueltas, y `k* ≤ μ + λ ≤ n`. El potencial es un entero no negativo que baja estrictamente en cada vuelta, así que el ciclo termina.


---

## 7. Fase 2: encontrar la entrada del ciclo

Cuando la fase 1 termina con `break`, sabemos que `lento` y `rapido` están en el mismo nodo dentro del ciclo. Sea `k` el número de vueltas de la fase 1, y sea `p` la posición de ambos:

```text
p ≡ k ≡ 2k  (mod λ)
```

La segunda igualdad implica `k ≡ 0 (mod λ)`, es decir, `k` es múltiplo de `λ`.

**Teorema 2.** Si en la fase 2 ponemos `lento = cabeza` y avanzamos ambos punteros de uno en uno, el punto donde se encuentran es exactamente la entrada del ciclo `x_μ`.

**Demostración.** Llamemos `l` a la posición de `lento` en la fase 2 y `r` a la de `rapido`. Al inicio de la fase 2, `l = 0` (en la cabeza) y `r = p`. En cada paso, `l` avanza 1 y `r` avanza 1. Después de `t` pasos:

```text
l = t
r = p + t   (módulo λ)
```

Queremos ver que se encuentran cuando `l = μ`, es decir, cuando `lento` está en la entrada del ciclo. En ese momento `t = μ`, y:

```text
l = μ
r = p + μ   (módulo λ)
```

Como `p ≡ k (mod λ)` y `k ≡ 0 (mod λ)`, tenemos `p ≡ 0 (mod λ)`, así que:

```text
r ≡ 0 + μ = μ  (mod λ)
```

Es decir, la posición de r dentro del ciclo es `μ mod λ`, así que `r` está en el nodo `x_μ`. ✔

---

## 8. Costo

**Fase 1.**

- **Caso sin ciclo.** `rapido` avanza 2 posiciones por vuelta, así que hace a lo sumo `⌈n/2⌉` vueltas. Cada vuelta hace 2 asignaciones de puntero y una comparación. El costo es `O(n)`.
- **Caso con ciclo.** El número de vueltas está acotado por `μ + λ ≤ n`. El costo es `O(n)`.

**Fase 2.** A lo sumo `μ` pasos, y `μ ≤ n`. El costo es `O(n)`.

**Costo total.** `O(n)` tiempo, `O(1)` memoria adicional (solo dos punteros).

**Modelo.** Cada `next` cuenta como un paso. `lento` hace `O(n)` pasos, `rapido` hace `O(n)` pasos. En total `O(n)`.

**Comparación con alternativas.**

- Marcar nodos visitados: `O(n)` tiempo pero `O(n)` memoria (hay que modificar los nodos o usar una tabla hash).
- Floyd: `O(n)` tiempo y `O(1)` memoria. Es la mejor solución en cuanto a memoria.
- **Cota mínima.** Cualquier algoritmo que decida si hay ciclo tiene que visitar al menos los nodos del ciclo una vez si hay ciclo, y todos los nodos si no lo hay. Así que `Ω(n)` pasos es una cota inferior trivial. Floyd es óptimo en tiempo y memoria.

---

## 9. Traza de ejemplo

Lista con `μ = 2`, `λ = 4`:

```text
nodo:   A → B → C → D → E → F
                ↑               │
                └───────────────┘
```

- `μ = 2`: nodos `A, B` antes del ciclo.
- `λ = 4`: ciclo `C → D → E → F → C`.
- Entrada del ciclo: `C = x_2`.

Las posiciones son:
| posición | nodo |
|---:|---|
| `0` | `A` |
| `1` | `B` |
| `2` | `C` |
| `3` | `D` |
| `4` | `E` |
| `5` | `F` |
| `6` | `C` (repite) |
| `7` | `D` |
| `8` | `E` |
| `9` | `F` |

Fase 1. El estado inicial es `k = 0` (`lento` = `rapido` = `A`), pero el chequeo `lento is rapido` no se hace antes de la primera vuelta, así que la primera comparación es en `k = 1`.

| vuelta `k`| `lento` | `rápido` | ¿iguales? |
|---:|---|---|---|
| 1 | B | C | no |
| 2 | C | E | no |
| 3 | D | C | no |
| 4 | E | E | **sí** |

Se encuentran en la vuelta `k* = 4`. Comprobemos la fórmula del Teorema 1:

```text
k* = λ · ⌈μ/λ⌉ = 4 · ⌈2/4⌉ = 4 · 1 = 4.  ✓
k* mod λ = 4 mod 4 = 0.  ✓
k* ≥ μ: 4 ≥ 2.  ✓
k* ≤ μ + λ = 6.  ✓
```

**Fase 2.** Ponemos `lento = cabeza = A` y `rapido = E` (donde se encontraron). Avanzamos de uno en uno:

| paso | `lento` | `rapido` | ¿iguales? |
|---:|---|---|---|
| 0 | A | E | no |
| 1 | B | F | no |
| 2 | C | C | **sí** |

Se encuentran en `C`, que es la entrada del ciclo. ✔

---

## 10. Implementación completa y verificable

```python
class Nodo:
    __slots__ = ("valor", "next")
    def __init__(self, valor, next=None):
        self.valor = valor
        self.next = next


def construir_lista(valores, mu=None):
    """Construye una lista con un tramo de longitud mu y un ciclo de longitud
       n − mu (donde n = len(valores)). Si mu es None, la lista es lineal y
       termina en None.

       Devuelve (cabeza, esperado), donde esperado es la entrada del ciclo
       (nodos[mu]) si hay ciclo, o None si no lo hay."""
    if not valores:
        return None, None
    nodos = [Nodo(v) for v in valores]
    for i in range(len(nodos) - 1):
        nodos[i].next = nodos[i + 1]
    if mu is not None:
        nodos[-1].next = nodos[mu]
        return nodos[0], nodos[mu]
    return nodos[0], None


def detectar_ciclo(cabeza):
    lento = rapido = cabeza
    while rapido is not None and rapido.next is not None:
        lento = lento.next
        rapido = rapido.next.next
        if lento is rapido:
            break
    else:
        return None
    lento = cabeza
    while lento is not rapido:
        lento = lento.next
        rapido = rapido.next
    return lento
```

**Pruebas.**

```python
import random

random.seed(2026)
casos = 0
for _ in range(5000):
    n = random.randint(1, 40)
    valores = list(range(n))
    con_ciclo = random.random() < 0.5
    if con_ciclo:
        mu = random.randint(0, n - 1)
        cabeza, esperado = construir_lista(valores, mu=mu)
        obtenido = detectar_ciclo(cabeza)
        assert obtenido is esperado, f"ciclo mal: mu={mu}"
    else:
        cabeza, _ = construir_lista(valores)
        assert detectar_ciclo(cabeza) is None
    casos += 1
print(f"{casos} listas probadas, sin fallos")
```

```text
5000 listas probadas, sin fallos
```

---

## 11. Invariante vigilado

Comprobamos en cada vuelta de la fase 1 que `lento` está en `k` y `rapido` en `2k` .

```python
def nodo_en(cabeza, pasos):
    """Nodo en la posición `pasos` desde `cabeza`. En una lista con ciclo,
       el recorrido envuelve naturalmente."""
    actual = cabeza
    for _ in range(pasos):
        actual = actual.next
    return actual


def fase1_vigilada(cabeza):
    """Ejecuta la fase 1 comprobando el Lema 1 en cada vuelta.
       Devuelve k*, el número de vueltas hasta el encuentro (o None si no hay ciclo)."""
    lento = rapido = cabeza
    k = 0
    while rapido is not None and rapido.next is not None:
        # invariante: lento en pos k, rapido en pos 2k
        assert lento is nodo_en(cabeza, k), f"lento mal en k={k}"
        assert rapido is nodo_en(cabeza, 2 * k), f"rapido mal en k={k}"
        lento = lento.next
        rapido = rapido.next.next
        k += 1
        if lento is rapido:
            return k
    return None
```

**Medición empírica.** Para muchas listas con ciclo, comprobamos que el número de vueltas `k*` cumple `k* ≡ 0 (mod λ)`:

```python
random.seed(7)
for _ in range(3000):
    n = random.randint(2, 30)
    mu = random.randint(0, n - 1)
    valores = list(range(n))
    cabeza, _ = construir_lista(valores, mu=mu)
    lam = n - mu
    k = fase1_vigilada(cabeza)
    assert k is not None and k % lam == 0, f"k={k}, λ={lam}"
print("en todas las pruebas, k* es múltiplo de λ")
```

```text
en todas las pruebas, k* es múltiplo de λ
```

---

````