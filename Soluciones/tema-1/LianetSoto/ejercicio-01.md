# Ejercicio 1 — Una computadora mil veces más rápida

## Enunciado

> ★ Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo `Θ(n²)`? ¿Y con uno `Θ(n log n)`? Estima los dos factores. (C1)

---

## 1. Supuestos

- El costo del algoritmo es `T(n) = c · f(n)`, donde `c > 0` es una constante que depende de cómo contamos.
- La computadora vieja hace `B` operaciones en una hora.
- La computadora nueva hace `1000B` operaciones en la misma hora.
- Para `Θ(n²)` tomamos el representante `T(n) = c · n²`. En ese caso el factor es exactamente `√1000`; si solo se sabe que `T(n) ∈ Θ(n²)`, el factor es el mismo salvo constantes.
- Para `Θ(n log n)` tomamos el representante `T(n) = c · n log₂ n`. La constante `c` se cancela en la ecuación del factor, pero el valor numérico del factor depende de `n_v`, y por tanto del presupuesto efectivo `B/c`. En el cálculo concreto fijamos `c = 1`.
- Usamos logaritmo en base 2. Cambiar la base solo multiplica los logaritmos por una constante, y esa constante se cancela al comparar las dos máquinas para el mismo algoritmo.

La pregunta es: si antes resolvíamos entradas de tamaño `n_v`, ¿cuál es el nuevo tamaño máximo `n_n`?

```text
factor = n_n / n_v

## 2. Caso `Θ(n²)`

Sea

```text
T(n) = c * n^2
```

En la máquina vieja, en una hora se puede resolver un tamaño `n_v` tal que

```text
c * n_v^2 = B
```

En la máquina nueva, que es 1000 veces más rápida,

```text
c * n_n^2 = 1000B
```

Dividiendo las dos ecuaciones:

```text
n_n^2 / n_v^2 = 1000
```

y por tanto

```text
n_n / n_v = sqrt(1000) = 10 * sqrt(10) ≈ 31.62
```

### Resultado

> Para `Θ(n²)`, el tamaño de entrada crece un factor `≈ 31.62`.

Este factor **no depende** del presupuesto `B` ni del valor concreto de `n_v`. Siempre es `sqrt(1000)`.

---
## 2. Caso `Θ(n²)`

Sea

```text
T(n) = c · n²
```
En la máquina vieja, en una hora se puede resolver un tamaño `n_v` tal que

```text
c · n_v² = B
```
En la máquina nueva, que es 1000 veces más rápida,
```text
c · n_n² = 1000B
```
Dividiendo las dos ecuaciones:
```text
n_n² / n_v² = 1000
```
y por tanto
```text
n_n / n_v = sqrt(1000) = 10 · sqrt(10) ≈ 31.62
```

### Resultado
    Para Θ(n²), el tamaño de entrada crece un factor ≈ 31.62.

Este factor no depende del presupuesto B ni del valor concreto de n_v. Siempre es sqrt(1000).


---

## 3. Caso `Θ(n log n)`

Sea

```text
T(n) = c * n * log2(n)
```

En la máquina vieja:

```text
c * n_v * log2(n_v) = B
```

En la máquina nueva:

```text
c * n_n * log2(n_n) = 1000B
```

Dividiendo:

```text
n_n * log2(n_n) = 1000 * n_v * log2(n_v)
```

Sea

```text
k = n_n / n_v
```

Entonces `n_n = k * n_v`, y sustituyendo:

```text
k * n_v * log2(k * n_v) = 1000 * n_v * log2(n_v)
```

Cancelamos `n_v`:

```text
k * ( log2(n_v) + log2(k) ) = 1000 * log2(n_v)
```

Despejando `k`:

```text
k = 1000 * log2(n_v) / ( log2(n_v) + log2(k) )
```

Esta es una ecuación implícita: `k` aparece en los dos lados. Lo importante es que

```text
k < 1000
```

porque `log2(n_n) > log2(n_v)`. Además, cuando `n_v → ∞`, el término `log2(k)` se vuelve despreciable frente a `log2(n_v)`, y entonces

```text
k → 1000
```

Pero para un presupuesto realista, `k` es un poco menor que 1000.

---

## 4. Cálculo concreto para una hora

Tomemos la misma computadora de la Conferencia 1:

```text
10^9 operaciones por segundo
```

En una hora:

```text
B = 10^9 * 3600 = 3.6e12 operaciones
```

La computadora nueva hace

```text
1000B = 3.6e15 operaciones
```

### 4.1. Para `n log2 n`

Resolviendo numéricamente

```text
n_v * log2(n_v) = 3.6e12
```

se obtiene

```text
n_v ≈ 9.8575e10
log2(n_v) ≈ 36.52
```

Resolviendo

```text
n_n * log2(n_n) = 3.6e15
```

se obtiene

```text
n_n ≈ 7.8009e13
```

Por tanto:

```text
k = n_n / n_v
  ≈ 7.8009e13 / 9.8575e10
  ≈ 791.3
```

Comprobación rápida: si `k = 791`, entonces

```text
log2(k) ≈ 9.63
```

y

```text
1000 * 36.52 / (36.52 + 9.63) ≈ 791.3
```

### Resultado

> Para `Θ(n log n)`, el factor es aproximadamente `791` para una hora.

--- 

## 5. Sensibilidad del factor para `n log n`

El factor `791.3` no es universal: depende de `n_v`. Para entradas viejas más grandes, el factor se acerca más a `1000`. La siguiente tabla se obtiene resolviendo la ecuación implícita para distintos valores de `n_v`, siempre con una mejora de hardware de `1000` veces.

| `n_v` | `log₂(n_v)` | Factor aproximado `k` |
|---:|---:|---:|
| `10³` | `9.97` | `≈ 524` |
| `10⁶` | `19.93` | `≈ 679` |
| `10⁹` | `29.90` | `≈ 758` |
| `10¹²` | `39.86` | `≈ 805` |
| `10¹⁵` | `49.83` | `≈ 837` |

Para el presupuesto concreto de una hora con `10⁹` operaciones por segundo, `n_v ≈ 9.8575 · 10¹⁰`, y por eso el factor es `≈ 791.3`.

---

## 6. Tabla resumen

| Complejidad | `n_v` con `B = 3.6e12` | `n_n` con `1000B` | Factor `n_n/n_v` |
|---|---:|---:|---:|
| `Θ(n²)` | `1,897,366` | `60,000,000` | `31.62` |
| `Θ(n log2 n)` | `≈ 9.86e10` | `≈ 7.80e13` | `≈ 791.3` |

---

## 7. Verificación experimental

El siguiente programa modifica el de la sección 7 de la Conferencia 1 para calcular los factores exactos por búsqueda binaria.

```python
import math

def mayor_n(costo, presupuesto):
    """Mayor n tal que costo(n) <= presupuesto."""
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2

    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


B = 10**9 * 3600          # una hora a 10^9 operaciones/segundo
S = 1000                  # computadora 1000 veces más rápida

costos = {
    "n^2": lambda n: n ** 2,
    "n log2 n": lambda n: n * math.log2(n),
}

print(f"{'algoritmo':>10} {'n_viejo':>18} {'n_nuevo':>18} {'factor':>10}")
for nombre, f in costos.items():
    n_viejo = mayor_n(f, B)
    n_nuevo = mayor_n(f, S * B)
    factor = n_nuevo / n_viejo
    print(f"{nombre:>10} {n_viejo:>18,} {n_nuevo:>18,} {factor:>10.3f}")
```

Salida aproximada:

```text
 algoritmo            n_viejo            n_nuevo     factor
       n^2          1,897,366         60,000,000     31.623
  n log2 n     98,575,000,000 78,009,000,000,000    791.300
```
---

## 8. Interpretación

- Para un algoritmo **cuadrático**, el factor es exactamente `sqrt(1000) ≈ 31.62`. No importa cuál sea el presupuesto ni el tamaño viejo.
- Para un algoritmo **`n log n`**, el factor depende del tamaño viejo `n_v`. Para `n_v` grande, el factor se acerca a 1000.
- Con el presupuesto de una hora, el factor es aproximadamente **791**, no 1000.
- Si solo se pide una estimación gruesa, se puede decir:
  - `Θ(n²)`: crece unas **32 veces**.
  - `Θ(n log n)`: crece **casi 1000 veces**, en la práctica alrededor de **791 veces** para una hora.

---

## 9. Conclusión

```text
Θ(n²)      => factor sqrt(1000) ≈ 31.62

Θ(n log n) => factor ≈ 791 para una hora,
              y tiende a 1000 cuando n → ∞.
```

La diferencia entre ambos casos muestra por qué la complejidad importa: una mejora de hardware multiplica por 1000 la potencia, pero un algoritmo cuadrático solo aprovecha la raíz cuadrada de esa mejora, mientras que uno `n log n` aprovecha casi toda.