# Ejercicio 4 — El contador binario en una máquina de Turing

> ★★ El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un potencial que m incrementos desde 0 cuestan O(m) pasos en total, aunque uno solo pueda costar Θ(log m). Es la pregunta que la conferencia 1 dejó abierta. (C1, C4)

---

## 1. El problema y su especificación

**Problema.** Diseñar una máquina de Turing de una cinta que, dado un número natural escrito en binario, le sume 1. El cabezal empieza en el bit menos significativo (LSB) y debe volver a él al terminar.

**Especificación.**

- **Precondición.** La cinta contiene la representación binaria de un número `n ≥ 0`, con el LSB en la posición 0 y los bits más significativos a la izquierda (posiciones 1, 2, …). A la derecha del LSB hay un símbolo de fin de número (blanco `␣`).
- **Postcondición.** La cinta contiene la representación binaria de `n + 1`, y el cabezal está de vuelta en la posición 0 (el LSB).

**Modelo.** Contamos **transiciones** de la máquina de Turing. Cada transición lee un símbolo, escribe uno (posiblemente el mismo), mueve el cabezal una posición a la izquierda o a la derecha, y cambia de estado. Una transición cuesta 1 paso.

**Lo que ya sabemos (Conferencia 1, ejercicio 7).** Un solo incremento en el peor caso (cuando el número es `2^k − 1`, todos unos) cuesta `Θ(k)` pasos, donde `k` es el número de bits. Si el contador vale `n ≈ 2^k`, entonces `k = Θ(log n)`, así que un incremento cuesta `Θ(log n)`. La pregunta es: **¿cuánto cuestan `m` incrementos seguidos desde 0?**

---

## 2. Diseño de la máquina de Turing

### 2.1. Alfabeto y cinta

- **Alfabeto de cinta:** `{0, 1, ␣}`. El símbolo `␣` marca el final del número a la derecha del LSB.
- **Posiciones:** `0` es el LSB, `1` el siguiente bit, etc. La cinta es infinita hacia la izquierda (bits más significativos) y hacia la derecha (blancos).
- **Estado inicial:** `q0`, cabezal en la posición 0.
- **Estados:** `q0` (buscar el primer 0), `q_ret` (volver al LSB), `q_halt` (detenerse).

### 2.2. Transiciones

| Estado | Lee | Escribe | Mueve | Nuevo estado | Comentario |
|---|---|---|---|---|---|
| `q0` | `1` | `0` | ← | `q0` | Acarreo: cambia 1 por 0 y sigue hacia la izquierda. |
| `q0` | `0` | `1` | → | `q_ret` | Encontró el 0: lo cambia por 1 y empieza a volver. |
| `q0` | `␣` | `1` | → | `q_ret` | El número era todo unos: añade un 1 a la izquierda y vuelve. |
| `q_ret` | `0` | `0` | → | `q_ret` | Vuelve al LSB sin cambiar nada. |
| `q_ret` | `1` | `1` | → | `q_ret` | Vuelve al LSB sin cambiar nada. |
| `q_ret` | `␣` | `␣` | ← | `q_halt` | Llegó al blanco a la derecha del LSB: retrocede una y se detiene. |

**Observación.** La transición de `q0` con `␣` no es estrictamente necesaria si se garantiza que la cinta tiene un 0 a la izquierda del número, pero es más limpia así. En la práctica, la cinta es infinita y el blanco actúa como 0.

### 2.3. Funcionamiento

El cabezal empieza en el LSB. Mientras lea `1`, los cambia por `0` y avanza a la izquierda. Cuando encuentra un `0` (o un blanco), lo cambia por `1` y empieza a volver a la derecha, sin cambiar nada, hasta encontrar el blanco que está a la derecha del LSB. Entonces retrocede una posición y se detiene en el LSB.

**Ejemplo: `n = 3` (`...0011`).**

```text
cinta:  ... 0 0 1 1 ␣
posición:   2 1 0
cabezal:         ^
```

1. `q0` lee `1` en pos 0 → escribe `0`, mueve ←. Cinta: `... 0 0 1 0 ␣`, cabezal en 1.
2. `q0` lee `1` en pos 1 → escribe `0`, mueve ←. Cinta: `... 0 0 0 0 ␣`, cabezal en 2.
3. `q0` lee `0` en pos 2 → escribe `1`, mueve →. Cinta: `... 0 1 0 0 ␣`, cabezal en 1, estado `q_ret`.
4. `q_ret` lee `0` en pos 1 → escribe `0`, mueve →. Cabezal en 0.
5. `q_ret` lee `0` en pos 0 → escribe `0`, mueve →. Cabezal en −1 (blanco).
6. `q_ret` lee `␣` en pos −1 → escribe `␣`, mueve ←, estado `q_halt`. Cabezal en 0.

Resultado: `... 0 1 0 0` = 4. ✔

---

## 3. Costo de un incremento

Sea `k` el número de unos consecutivos al final del número (desde el LSB hacia la izquierda). Es decir, el número termina en `k` unos y luego un `0` (o el blanco).

**Costo del incremento:**

- **Avance:** `k` transiciones de `q0` con `1` (cada una escribe `0` y mueve ←).
- **Escritura del 1:** 1 transición de `q0` con `0` o `␣` (escribe `1` y mueve →).
- **Retorno:** `k` transiciones de `q_ret` (mueve → sin cambiar).
- **Detección final:** 1 transición de `q_ret` con `␣` (mueve ← y se detiene).

**Total:** `2k + 2` transiciones.

**Peor caso.** Si `n = 2^k − 1`, todos los bits son 1, y `k` es la longitud del número. Entonces el costo es `2k + 2 = Θ(k)`. Si el contador vale `n`, `k = Θ(log n)`, así que el peor caso de un incremento es `Θ(log n)`.

**Mejor caso.** Si `n` es par, `k = 0`, y el costo es `2` transiciones: `q0` con `0` (escribe `1`, mueve →) y `q_ret` con `␣` (mueve ←, se detiene).

---

## 4. El potencial y la demostración de O(m)

### 4.1. El potencial

Definimos el potencial del contador `n` como

```text
Φ(n) = 2 · popcount(n)
```

donde `popcount(n)` es el número de unos en la representación binaria de `n`.

**Propiedades.**

- `Φ(n) ≥ 0` para todo `n ≥ 0`.
- `Φ(0) = 0`.
- Cuando el contador vale `n`, `Φ(n)` es proporcional al número de unos.

### 4.2. El cambio de potencial en un incremento

Supongamos que el contador vale `n` y termina en `k` unos. Entonces:

- `n` tiene `popcount(n)` unos.
- `n + 1` tiene `popcount(n) − k + 1` unos (los `k` unos finales se convierten en 0, y el 0 siguiente se convierte en 1; si `k` es la longitud total, se añade un 1).

Por tanto:

```text
Φ(n + 1) − Φ(n) = 2 · (popcount(n) − k + 1 − popcount(n)) = 2(1 − k)
```

### 4.3. El costo amortizado

El costo real del incremento es `c = 2k + 2` (sección 3). El costo amortizado es:

```text
ĉ = c + Φ(n + 1) − Φ(n) = (2k + 2) + 2(1 − k) = 4
```

El **costo amortizado es exactamente** `4`, **constante**, independiente de `k`. Cada incremento, por caro que sea en el peor caso, se paga con su propio potencial: los `k` unos que se convierten en ceros bajan el potencial en `2k`, y el nuevo 1 lo sube en `2`, dejando un balance neto de `4` por operación.

### 4.4. La suma telescópica

Para `m` incrementos desde 0, sumamos los costos amortizados:

```text
Σ_{i=1}^{m} ĉ_i = Σ_{i=1}^{m} c_i + Φ(m) − Φ(0) = Σ c_i + 2 · popcount(m)
```

Como `ĉ_i = 4` para todo `i`:
```text
Σ_{i=1}^{m} ĉ_i = 4m
```
Y como Φ(m) ≥ 0:
```text

Σ_{i=1}^{m} c_i = 4m − 2 · popcount(m) ≤ 4m
```

**Conclusión:** `m` incrementos desde 0 cuestan a lo sumo `4m` transiciones, es decir, `O(m)` pasos en total, aunque un solo incremento pueda costar `Θ(log m)`. La forma exacta es `4m − 2·popcount(m)`, que es `Θ(m)` porque `popcount(m) = O(log m)`. ∎

---

## 5. Implementación y simulación

### 5.1. La máquina de Turing

```python
class MTContador:
    def __init__(self, cinta=None, max_pasos=10**6):
        self.cinta = cinta if cinta is not None else {0: 0, -1: '␣'}
        self.cabezal = 0
        self.estado = 'q0'
        self.pasos = 0
        self.max_pasos = max_pasos

    def leer(self):
        return self.cinta.get(self.cabezal, '␣')

    def escribir(self, simbolo):
        self.cinta[self.cabezal] = simbolo

    def mover(self, direccion):
        # "izquierda" = hacia bits más significativos = posición mayor
        # "derecha"   = hacia el LSB = posición menor
        self.cabezal += 1 if direccion == '←' else -1

    def paso(self):
        s = self.leer()
        if self.estado == 'q0':
            if s == 1:
                self.escribir(0); self.mover('←'); self.estado = 'q0'
            elif s == 0:
                self.escribir(1); self.mover('→'); self.estado = 'q_ret'
            elif s == '␣':
                self.escribir(1); self.mover('→'); self.estado = 'q_ret'
            else:
                raise ValueError(f"Símbolo inesperado {s}")
        elif self.estado == 'q_ret':
            if s in (0, 1):
                self.mover('→'); self.estado = 'q_ret'
            elif s == '␣':
                self.mover('←'); self.estado = 'q_halt'
        elif self.estado == 'q_halt':
            return False
        self.pasos += 1
        return True

    def ejecutar(self):
        while self.estado != 'q_halt' and self.pasos < self.max_pasos:
            if not self.paso():
                break
        return self.pasos

    def valor(self):
        """Lee el número de la cinta (asumiendo bits 0/1 y blanco al final)."""
        v = 0
        for pos in range(max(self.cinta.keys()) + 1):
            if self.cinta.get(pos, 0) == 1:
                v += 1 << pos
        return v

    def representacion(self, ancho=10):
        """Devuelve una representación legible de la cinta."""
        posiciones = sorted(self.cinta.keys())
        if not posiciones:
            return ""
        lo, hi = min(posiciones), max(posiciones)
        lo = min(lo, 0)
        hi = max(hi, 0)
        chars = []
        for p in range(lo, hi + 1):
            c = self.cinta.get(p, '␣')
            chars.append(str(c))
        # marcar el cabezal
        idx = self.cabezal - lo
        if 0 <= idx < len(chars):
            chars[idx] = f"[{chars[idx]}]"
        return " ".join(chars)
```

### 5.2. Simulación de un incremento

```python
def incrementar(n, verbose=False):
    """Simula un incremento desde n y devuelve (n+1, pasos, mt)."""
    cinta = {}
    for i in range(n.bit_length()):
        cinta[i] = (n >> i) & 1
    cinta[-1] = '␣'  # blanco a la derecha del LSB
    # Aseguramos que hay un blanco a la izquierda si hace falta
    max_pos = n.bit_length()
    cinta[max_pos] = '␣'
    mt = MTContador(cinta)
    if verbose:
        print(f"inicio:  {mt.representacion()}")
    pasos = mt.ejecutar()
    if verbose:
        print(f"final:   {mt.representacion()}")
        print(f"pasos:   {pasos}")
    return mt.valor(), pasos, mt
```

**Ejemplo: `n = 3`.**

```python
nuevo, pasos, mt = incrementar(3, verbose=True)
print(f"3 + 1 = {nuevo}, {pasos} pasos")
```

```text
inicio:  ␣ [1] 1 ␣
final:   ␣ [0] 0 1
pasos:   6
3 + 1 = 4, 6 pasos
```

El costo es `6 = 2·2 + 2`, con `k = 2` unos finales. ✔

### 5.3. Verificación de la fórmula `2k + 2`

```python
def unos_finales(n):
    """Número de unos consecutivos al final de n (desde el LSB)."""
    k = 0
    while n & 1:
        k += 1
        n >>= 1
    return k

print(f"{'n':>6} {'k':>3} {'pasos':>7} {'2k+2':>6} {'coincide':>10}")
for n in range(0, 32):
    _, pasos, _ = incrementar(n)
    k = unos_finales(n)
    print(f"{n:>6} {k:>3} {pasos:>7} {2*k+2:>6} {str(pasos == 2*k+2):>10}")
```

```text
     n   k   pasos   2k+2  coincide
     0   0       2      2      True
     1   1       4      4      True
     2   0       2      2      True
     3   2       6      6      True
     4   0       2      2      True
     5   1       4      4      True
     6   0       2      2      True
     7   3       8      8      True
     8   0       2      2      True
     9   1       4      4      True
    10   0       2      2      True
    11   2       6      6      True
    12   0       2      2      True
    13   1       4      4      True
    14   0       2      2      True
    15   4      10     10      True
    16   0       2      2      True
    17   1       4      4      True
    18   0       2      2      True
    19   2       6      6      True
    20   0       2      2      True
    21   1       4      4      True
    22   0       2      2      True
    23   3       8      8      True
    24   0       2      2      True
    25   1       4      4      True
    26   0       2      2      True
    27   2       6      6      True
    28   0       2      2      True
    29   1       4      4      True
    30   0       2      2      True
    31   5      12     12      True
```

La fórmula `2k + 2` se cumple para todos los `n` de 0 a 31. ✔

---

## 6. Verificación experimental del potencial y del costo total

### 6.1. El potencial `Φ = 2 · popcount(n)`

```python
def popcount(n):
    return bin(n).count('1')

def potencial(n):
    return 2 * popcount(n)

print(f"{'n':>4} {'popcount':>10} {'Φ(n)':>6}")
for n in range(0, 17):
    print(f"{n:>4} {popcount(n):>10} {potencial(n):>6}")
```

```text
   n   popcount   Φ(n)
   0          0      0
   1          1      2
   2          1      2
   3          2      4
   4          1      2
   5          2      4
   6          2      4
   7          3      6
   8          1      2
   9          2      4
  10          2      4
  11          3      6
  12          2      4
  13          3      6
  14          3      6
  15          4      8
  16          1      2
```

### 6.2. El cambio de potencial en un incremento

```python
print(f"{'n':>4} {'k':>3} {'Φ(n)':>5} {'Φ(n+1)':>7} {'ΔΦ':>4} {'2(1-k)':>7} {'coincide':>10}")
for n in range(0, 16):
    k = unos_finales(n)
    phi_n = potencial(n)
    phi_n1 = potencial(n + 1)
    delta = phi_n1 - phi_n
    print(f"{n:>4} {k:>3} {phi_n:>5} {phi_n1:>7} {delta:>4} {2*(1-k):>7} "
          f"{str(delta == 2*(1-k)):>10}")
```

```text
   n   k  Φ(n)  Φ(n+1)   ΔΦ  2(1-k)  coincide
   0   0     0       2    2      2      True
   1   1     2       2    0      0      True
   2   0     2       4    2      2      True
   3   2     4       2   -2     -2      True
   4   0     2       4    2      2      True
   5   1     4       4    0      0      True
   6   0     4       6    2      2      True
   7   3     6       2   -4     -4      True
   8   0     2       4    2      2      True
   9   1     4       4    0      0      True
  10   0     4       6    2      2      True
  11   2     6       4   -2     -2      True
  12   0     4       6    2      2      True
  13   1     6       6    0      0      True
  14   0     6       8    2      2      True
  15   4     8       2   -6     -6      True
```

La fórmula `ΔΦ = 2(1 − k)` se cumple exactamente. ✔

### 6.3. El costo amortizado y la suma telescópica

```python
m = 30
total_real = 0
total_amortizado = 0
phi_0 = potencial(0)
print(f"{'i':>3} {'n':>3} {'k':>3} {'c':>4} {'Φ':>4} {'ĉ':>4} {'Σc':>6} {'Σĉ':>6}")
for i in range(m):
    n = i
    k = unos_finales(n)
    _, c, _ = incrementar(n)
    phi_n = potencial(n)
    phi_n1 = potencial(n + 1)
    chat = c + phi_n1 - phi_n
    assert c == 2 * k + 2, f"c={c} != 2k+2={2*k+2}"
    assert chat == 4, f"ĉ={chat} != 4"
    total_real += c
    total_amortizado += chat
    if i < 10 or i >= m - 3:
        print(f"{i:>3} {n:>3} {k:>3} {c:>4} {phi_n:>4} {chat:>4} "
              f"{total_real:>6} {total_amortizado:>6}")

print(f"\nTotal real: {total_real}")
print(f"Total amortizado: {total_amortizado}")
print(f"Φ(m) − Φ(0): {potencial(m) - potencial(0)}")
print(f"Σc + Φ(m) − Φ(0) = {total_real + potencial(m) - potencial(0)}")
print(f"¿Σĉ = Σc + Φ(m) − Φ(0)? "
      f"{total_amortizado == total_real + potencial(m) - potencial(0)}")
print(f"¿Σĉ = 4m? {total_amortizado == 4 * m}")
print(f"¿Σc = 4m − 2·popcount(m)? "
      f"{total_real == 4 * m - 2 * popcount(m)}")
```

```text
  i   n   k    c    Φ    ĉ     Σc     Σĉ
  0   0   0    2    0    4      2      4
  1   1   1    4    2    4      6      8
  2   2   0    2    2    4      8     12
  3   3   2    6    4    4     14     16
  4   4   0    2    2    4     16     20
  5   5   1    4    4    4     20     24
  6   6   0    2    4    4     22     28
  7   7   3    8    6    4     30     32
  8   8   0    2    2    4     32     36
  9   9   1    4    4    4     36     40
  ...
 27  27   2    6    8    4    106    112
 28  28   0    2    6    4    108    116
 29  29   1    4    8    4    112    120

Total real: 112
Total amortizado: 120
Φ(m) − Φ(0): 8
Σc + Φ(m) − Φ(0) = 120
¿Σĉ = Σc + Φ(m) − Φ(0)? True
¿Σĉ = 4m? True
¿Σc = 4m − 2·popcount(m)? True
```
Todos los `assert` pasan: `c = 2k+2` en cada paso, ĉ = 4 en cada paso, la telescópica cierra (`Σĉ = Σc + Φ(m) − Φ(0)`), y las formas exactas `Σĉ = 4m` y `Σc = 4m − 2·popcount(m)` se cumplen. La cota `Σc ≤ 4m` se respeta con holgura `(112 ≤ 120)`.

---
