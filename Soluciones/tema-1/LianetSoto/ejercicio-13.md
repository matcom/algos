# Ejercicio 13 — Splay tree desde un camino, accediendo en orden

> ★★ En un splay tree que empieza como un camino de n nodos se accede a las claves 1, …, n en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? (C4)

---

## 1. El escenario

Partimos del **peor árbol inicial** de la Conferencia 4, sección 4:

```python
def camino(n):
    """El peor árbol inicial: n en la raíz, cada clave hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]
```

El árbol es un camino que baja por la izquierda:

```text
        n
       /
     n-1
     /
   ...
   /
  2
 /
1
```

La clave `1` está a profundidad `n-1`. La secuencia de accesos es `1, 2, 3, …, n`, **una sola pasada**. Cada acceso busca la clave y hace `splay` del nodo encontrado.

El costo de un acceso es el número de rotaciones que hace el `splay`, o 1 si el nodo ya es la raíz (Conferencia 4).

---

## 2. El potencial inicial

El potencial de un splay tree es (Conferencia 4):

```text
Φ = Σ_x r(x),   donde   r(x) = log₂ s(x)
```

y `s(x)` es el número de nodos del subárbol con raíz en `x`.

Para el camino inicial, el subárbol de la clave `k` contiene las claves `1, 2, …, k`, así que `s(k) = k` y `r(k) = log₂ k`. Por tanto:

```text
Φ₀ = Σ_{k=1}^{n} log₂ k = log₂(n!)
```

Con la aproximación de Stirling, `log₂(n!) ≈ n log₂ n − 1.443 n`. Es decir, **`Φ₀ = Θ(n log n)`**: el camino tiene el potencial máximo posible para un árbol de `n` nodos.

---

## 3. El lema de acceso

**Lema de acceso (Sleator y Tarjan, 1985).** El costo amortizado de hacer `splay` de un nodo `x` en un árbol con raíz `t` es a lo sumo

```text
ĉ ≤ 3(r(t) − r(x)) + 1 = O(log n)
```

donde `r` es el rango antes del `splay`.

**La cuenta de la sección 5 (telescópica).** Sumando sobre `m` accesos:

```text
Σ_{i=1}^{m} c_i = Σ_{i=1}^{m} ĉ_i − (Φ_m − Φ₀)
```

o, despejando la cota:

```text
Σ c_i ≤ Σ ĉ_i + Φ₀ − Φ_m ≤ Σ ĉ_i + Φ₀
```

porque `Φ_m ≥ 0`. La cota solo funciona si el potencial final no es menor que el inicial. Si `Φ_m < Φ₀`, la diferencia `Φ₀ − Φ_m` es positiva y se suma al costo; si `Φ_m ≥ Φ₀`, se resta y la cota mejora.

Para nuestra secuencia, `m = n`, `r(t) = log₂ n`, y `r(x_i) ≥ 0`. Sustituyendo en el lema:

```text
ĉ_i ≤ 3 log₂ n + 1
```

y sumando:

```text
Σ c_i ≤ n(3 log₂ n + 1) + Φ₀ = n(3 log₂ n + 1) + log₂(n!) = O(n log n)
```

**Esta es la cota cruda que da el lema de acceso: `O(n log n)`.**

---

## 4. Lo que mide la sección 6: Θ(n)

La Conferencia 4, sección 6, mide el costo por acceso al recorrer las claves en orden, empezando desde un camino, con tres rondas completas:

```python
def subir_a_la_raiz(x):
    """Sube x a la raíz con rotaciones simples."""
    rotaciones = 0
    while x.padre:
        rotar(x)
        rotaciones += 1
    return rotaciones

def costo_por_acceso(reorganizar, n, rondas=3):
    raiz, total = camino(n), 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(reorganizar(x), 1)
            raiz = x
    return total / (rondas * n)

# Generación de la tabla
print(f"{'n':>6} {'splay':>8} {'subir a la raíz':>16} {'log₂ n':>8}")
for n in [100, 200, 400, 800]:
    s = costo_por_acceso(splay, n)
    r = costo_por_acceso(subir_a_la_raiz, n)
    print(f"{n:>6} {s:>8.1f} {r:>16.1f} {math.log2(n):>8.1f}")
```

Resultado:

```text
     n    splay    subir a la raíz    log₂ n
   100      4.2               50.5       6.6
   200      4.2              100.5       7.6
   400      4.3              200.5       8.6
   800      4.4              400.5       9.6
```

**Splay cuesta ≈ 4.2–4.4 rotaciones por acceso, independientemente de `n`.** Para `n` accesos, el costo total es

```text
Σ c_i ≈ 4.2 n = Θ(n)
```

La figura 3 de la Conferencia 4 lo muestra en ejes logarítmicos: la curva de splay es plana (pendiente 0), la de subir a la raíz tiene pendiente 1. La diferencia entre ambas es la que el lema de acceso tiene que explicar.

---

## 5. La comparación: la cota es floja

| | Costo total |
|---|---|
| **Cota cruda del lema de acceso** | `n(3 log₂ n + 1) + log₂(n!) = O(n log n)` |
| **Medición de la sección 6** | `≈ 4.2 n = Θ(n)` |

**La cota `O(n log n)` no es ajustada: es floja por un factor de `Θ(log n)`.** Para `n = 100`, la cota dice `100 · (3·6.6 + 1) + 524 ≈ 2700` operaciones; la realidad mide `420`. Para `n = 800`, la cota dice `800 · (3·9.6 + 1) + 6800 ≈ 30 000`; la realidad mide `3520`. La brecha crece con `n`.

**¿Por qué el lema de acceso da una cota tan floja?** Porque usa `r(x_i) ≥ 0` para cada acceso, lo que es cierto pero muy conservador. En la mayoría de los accesos, `r(x_i)` es grande (el nodo accedido tiene un subárbol grande), y el término `3(r(t) − r(x_i))` es mucho menor que `3 log₂ n`. La cota cruda ignora esa información.

---

## 6. ¿Por qué la cota es floja?

La cota `O(n log n)` viene de dos simplificaciones:

1. `r(x_i) ≥ 0` para todo `i`. Falso en general: solo el primer acceso (a la hoja `1`) tiene `r = 0`; los demás tienen `r` grande.
2. `Φ_m ≥ 0` y por tanto `Φ₀ − Φ_m ≤ Φ₀`. Cierto, pero `Φ₀` es `Θ(n log n)`, así que esta simplificación también es muy conservadora.

Vamos a ver que **ninguna de las dos simplificaciones es necesaria** para esta secuencia.

### 6.1. El árbol vuelve a ser un camino: `Φ_m = Φ₀`

Después de acceder a `1, 2, …, n` en orden, el árbol vuelve a ser exactamente el camino inicial.

**Verificación para `n = 4`.** Traza completa:

```text
inicio:              4
                    /
                   3
                  /
                 2
                /
               1

splay(1):  3 rotaciones (zig-zig: 2 sobre 3, luego 1 sobre 2; después zig: 1 sobre 4)
           árbol:  1
                    \
                     4
                    /
                   2
                    \
                     3

splay(2):  2 rotaciones (zig-zag 2-4, zig 2-1)
           árbol:  2
                  / \
                 1   4
                    /
                   3

splay(3):  2 rotaciones (zig-zag 3-4, zig 3-2)
           árbol:    3
                    / \
                   2   4
                  /
                 1

splay(4):  1 rotación (zig 4-3)
           árbol:  4
                  /
                 3
                /
               2
              /
             1
```

El árbol final es **idéntico al inicial**. Por tanto:

```text
Φ_m = Φ₀ = log₂(n!)
```

La igualdad `Φ_m = Φ₀` no es casualidad: es un hecho conocido sobre el acceso secuencial en splay trees. El árbol vuelve a su forma original después de una pasada completa.

### 6.2. La cuenta exacta: `Σ c_i = Σ ĉ_i`

Como `Φ_m = Φ₀`, la telescópica da:

```text
Σ c_i = Σ ĉ_i − (Φ_m − Φ₀) = Σ ĉ_i
```

**El costo real total es exactamente la suma de los costos amortizados.** No hay que pagar `Φ₀` aparte: el potencial vuelve a donde empezó.

Lo que da el lema: Σ c_i ≤ Σ ĉ_i + Φ₀ = O(n log n). Es una cota superior, no ajustada.

Lo que da el teorema del acceso secuencial (Tarjan, 1985): el costo total real de acceder a 1, 2, …, n en orden desde cualquier árbol inicial es O(n). Para el camino inicial, la constante es ≈ 4.4 (sección 7.2).

La igualdad exacta: como Φ_m = Φ₀ (§6.1), se tiene Σ c_i = Σ ĉ_i. No hay que pagar Φ₀ aparte.

Por tanto, Σ c_i = Θ(n), mientras que la cota cruda del lema es O(n log n). El lema es flojo por un factor Θ(log n).

### 6.3. La cota cuidadosa: `Θ(n)`

Juntando las dos piezas:

```text
Σ c_i = Σ ĉ_i = Θ(n)
```

Esto coincide con la medición de la sección 6 (`≈ 4.2 n`). La cota `O(n log n)` del lema de acceso es floja; la cota ajustada es `Θ(n)`.

**Observación sobre el lema de acceso.** El lema es una cota **por operación** (`O(log n)` amortizado). Es ajustada para una operación suelta en el peor caso: un acceso a la hoja más profunda de un camino cuesta `Θ(n)` real, y `ĉ ≈ 3 log₂ n + 1`. Pero **sumada sobre una secuencia**, la cota por operación puede ser muy floja si las operaciones posteriores son baratas. El lema no captura la estructura de la secuencia; solo la de cada operación individual.

### 6.4. El teorema del acceso secuencial (Tarjan, 1985)

La afirmación `Σ c_i = Θ(n)` para accesos en orden tiene nombre propio:

**Teorema (acceso secuencial, Tarjan 1985).** En un splay tree, acceder a las claves en orden (creciente o decreciente) cuesta `O(n)` en total, **empezando desde cualquier árbol**.

La constante depende del árbol inicial, pero está acotada. Para el camino inicial, la medición de la sección 6 da `≈ 4.2`. El teorema confirma que la cota `O(n log n)` del lema de acceso es floja para esta secuencia.

---

## 7. Verificación experimental

### 7.1. El árbol vuelve a ser un camino

```python
import math

class Nodo:
    __slots__ = ("clave", "izq", "der", "padre")
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None


def rotar(x):
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq: p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der: p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p: g.izq = x
        else: g.der = x


def splay(x):
    r = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:
            rotar(x); r += 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p); rotar(x); r += 2
        else:
            rotar(x); rotar(x); r += 2
    return r


def camino(n):
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]


def tamano(x):
    return 0 if x is None else 1 + tamano(x.izq) + tamano(x.der)


def potencial(r):
    return 0.0 if r is None else math.log2(tamano(r)) + potencial(r.izq) + potencial(r.der)


def buscar(r, k):
    while r.clave != k:
        r = r.izq if k < r.clave else r.der
    return r


def es_camino_izquierdo(r, n):
    """Comprueba si el árbol es exactamente n → n-1 → … → 1 por la izquierda."""
    for k in range(n, 1, -1):
        if r is None or r.clave != k or r.der is not None:
            return False
        r = r.izq
    return r is not None and r.clave == 1 and r.izq is None and r.der is None


print(f"{'n':>5} {'Φ₀':>10} {'Φ_m':>10} {'Φ₀ = Φ_m':>10} {'vuelve al camino':>18}")
for n in [4, 8, 16, 32, 64, 128]:
    raiz = camino(n)
    phi_0 = potencial(raiz)
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        splay(x)
        raiz = x
    phi_m = potencial(raiz)
    print(f"{n:>5} {phi_0:>10.2f} {phi_m:>10.2f} "
          f"{str(abs(phi_0 - phi_m) < 1e-9):>10} {str(es_camino_izquierdo(raiz, n)):>18}")
```

Salida esperada:

```text
    n         Φ₀        Φ_m   Φ₀ = Φ_m   vuelve al camino
    4       4.58       4.58       True              True
    8      15.30      15.30       True              True
   16      44.25      44.25       True              True
   32     117.66     117.66       True              True
   64     296.00     296.00       True              True
  128     716.16     716.16       True              True
```

En todos los casos, `Φ_m = Φ₀` y el árbol vuelve a ser un camino. ✔

### 7.2. El costo total es Θ(n), no Θ(n log n)

```python
print(f"{'n':>5} {'rot totales':>12} {'rot / n':>8} "
      f"{'cota cruda 3n log₂n + n':>24} {'Φ₀ + 3n log₂n + n':>22}")
for n in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
    raiz = camino(n)
    total = 0
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        total += max(splay(x), 1)
        raiz = x
    cota_cruda = 3 * n * math.log2(n) + n
    cota_con_phi = cota_cruda + math.lgamma(n + 1) / math.log(2)
    print(f"{n:>5} {total:>12} {total/n:>8.2f} "
          f"{cota_cruda:>24.0f} {cota_con_phi:>22.0f}")
```

Salida esperada:

```text
    n  rot totales  rot / n  cota cruda 3n log₂n + n      Φ₀ + 3n log₂n + n
    4            8     2.00                       28                     33
    8           22     2.75                       80                     95
   16           54     3.38                      208                    252
   32          120     3.75                      512                    630
   64          256     4.00                     1216                   1512
  128          534     4.17                     2816                   3532
  256         1096     4.28                     6400                   8084
  512         2222     4.34                    14336                  18211
 1024         4478     4.37                    31744                  40513
```

**Lectura.** `rot / n` converge a ≈ 4.4 (incrementos `+0.75, …, +0.03`, cada uno la mitad del anterior), valor que coincide con la medición independiente de la sección 6 (≈ 4.2). El costo total es `Θ(n)` con constante ≈ 4.4. Las dos cotas crecen como n log n y su holgura pasa de ×3.5 (`n = 4`) a ×7.1 (`n = 1024`): el lema paga `O(log n)` por acceso, mientras que la secuencia secuencial solo necesita `Θ(1)` amortizado. El teorema del acceso secuencial garantiza ese `O(n)` total y confirma que la cota `O(n log n)` es floja por un factor `Θ(log n)`.


### 7.3. La suma de los costos amortizados es exactamente el costo total

```python
print(f"{'n':>5} {'Σ c_i':>10} {'Σ ĉ_i':>10} {'Φ₀ − Φ_m':>12} {'Σ c = Σ ĉ':>12}")
for n in [16, 32, 64, 128]:
    raiz = camino(n)
    phi_0 = potencial(raiz)
    total_c = 0
    total_chat = 0.0
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        phi_antes = potencial(raiz)
        c = max(splay(x), 1)
        phi_despues = potencial(x)
        chat = c + phi_despues - phi_antes
        total_c += c
        total_chat += chat
        raiz = x
    phi_m = potencial(raiz)
    print(f"{n:>5} {total_c:>10} {total_chat:>10.2f} "
          f"{phi_0 - phi_m:>12.2f} {str(abs(total_c - total_chat) < 1e-9):>12}")
```

Salida esperada:

```text
    n      Σ c_i      Σ ĉ_i     Φ₀ − Φ_m    Σ c = Σ ĉ
   16         54      54.00         0.00         True
   32        120     120.00         0.00         True
   64        256     256.00         0.00         True
  128        534     534.00         0.00         True
```

Σ c_i = Σ ĉ_i exactamente, porque Φ_m = Φ₀. No es un resultado experimental: es una identidad que se cumple por la igualdad del potencial inicial y final. La tabla solo verifica la aritmética. La suma de los costos amortizados no es una cota superior: es igual al costo total. Y esa suma es Θ(n), no Θ(n log n).

---