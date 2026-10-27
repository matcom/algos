# Ejercicio 05: detección de ciclos de Floyd

## Enunciado

Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

## Convenciones

- **Modelo:** lista enlazada. Cada nodo `p` tiene un campo `p.sig` que apunta a otro nodo o a `null`. La cabeza puede ser `null` (lista vacía). El algoritmo solo puede seguir `sig`, comparar punteros por igualdad y comparar con `null`.
- **Costo:** el número de vueltas del `while`. Cada vuelta hace como mucho 3 lecturas de `sig` y 3 pruebas, así que es `Θ(1)`. La memoria extra son los dos punteros.
- **Recorrido:** `x_0 = cabeza` y `x_{k+1} = x_k.sig`, con `null.sig = null`. Así `x_k` es el nodo al que se llega con `k` pasos, y una vez que vale `null` se queda en `null`.
- **Hay ciclo** si `x_k != null` para todo `k` (el recorrido nunca termina). **No hay ciclo** si algún `x_k = null`, y entonces `m = min{k : x_k = null}` es el número de nodos.
- **Se encuentran** quiere decir que, después de mover los dos punteros, `lento == rapido`. Eso es exactamente lo que hace que el algoritmo devuelva `true`.
- **`N`** es el número de nodos distintos alcanzables desde `cabeza`: `N = m` sin ciclo, y `N = mu + lam` con ciclo (se define en el Lema 2). Si la lista tiene `n` nodos, `N <= n`.

## Algoritmo

```
detectar_ciclo(cabeza):
    lento = cabeza
    rapido = cabeza
    while rapido != null and rapido.sig != null:
        lento = lento.sig              // avanza 1
        rapido = rapido.sig.sig        // avanza 2
        if lento == rapido:
            return true
    return false
```

## Invariante

Sea `t` el número de vueltas completadas del `while`. No es una variable del código, solo de la prueba. Cada vez que se evalúa la guarda, con `0 <= t`, se cumple `I(t)`:

- **I1.** `lento = x_t` y `rapido = x_{2t}`.
- **I2.** Para todo `s` con `1 <= s <= t`: `x_s != null` y `x_s != x_{2s}`.

I2 dice que en ninguna de las `t` vueltas anteriores los punteros se encontraron, y que `lento` nunca cayó en `null`.

**Inicialización (`t = 0`).** `lento = rapido = cabeza = x_0 = x_{2·0}`, así que I1 vale. I2 es vacío porque no hay `s` con `1 <= s <= 0`.

**Mantenimiento.** Supongamos `I(t)` y la guarda verdadera: `rapido != null` y `rapido.sig != null`. Por I1 eso es `x_{2t} != null` y `x_{2t+1} != null`.

- `lento != null`. Si `t = 0`, `lento = x_0 = x_{2t} != null`. Si `t >= 1`, sale de I2 con `s = t` (hipótesis).
- Entonces `lento.sig` está definido y el nuevo `lento` es `x_{t+1}`. El nuevo `rapido` es `rapido.sig.sig = x_{2t+2}`, que puede ser `null` si `x_{2t+1}` era el último nodo.
- `x_{t+1} != null`, porque `x_{2t+1} != null` y `t + 1 <= 2t + 1`. Esto es una propiedad de los datos: si un nodo del recorrido no es `null`, tampoco lo son los anteriores.

Ahora, la prueba por casos:

- **Caso `lento == rapido`:** la vuelta devuelve `true` y el algoritmo sale. Lo que quedó demostrado es `x_{t+1} = x_{2(t+1)} != null`. Es lo que usa el Corolario A.
- **Caso `lento != rapido`:** entonces `x_{t+1} != x_{2(t+1)}`. Junto con `x_{t+1} != null` (arriba), esto es I2 para `s = t + 1`. Lo recién agregado se justifica con la prueba del `if` y con los datos. Los `s <= t` siguen valiendo por hipótesis, e I1 ya se demostró. Así que vale `I(t+1)`. ∎

## Correctitud

**Corolarios del invariante.** Son correctitud parcial: valen si el algoritmo termina.

- **Hecho 1.** Si `x_a = x_b != null` con `a < b`, hay ciclo. Si no lo hubiera, existe `m` y `b < m`. Pero `x_{a+k} = x_{b+k}` para todo `k >= 0`, y con `k = m - b` queda `x_{a+m-b} = x_m = null` con `a + m - b < m`, que contradice la minimalidad de `m`.
- **Corolario A (`true` ⇒ hay ciclo).** Si devuelve `true`, por el mantenimiento hay `t' = t + 1 >= 1` con `x_{t'} = x_{2t'} != null` y `t' < 2t'`. Por el Hecho 1, hay ciclo.
- **Corolario B (`false` ⇒ no hay ciclo).** Si devuelve `false`, la guarda falló: `x_{2t} = null` o `x_{2t+1} = null`. Algún `x_k` es `null`, así que no hay ciclo. Vale incluso si `t = 0`: la lista vacía y la de un nodo sin ciclo devuelven `false` sin entrar al `while`.

**Estructura de una lista con ciclo.** Hace falta para la terminación.

- **Lema 2.** Si hay ciclo, existen `mu >= 0` y `lam >= 1` tales que, para `a < b`: `x_a = x_b` si y solo si `a >= mu` y `lam` divide a `b - a`. Además `N = mu + lam`.
  - *Definición.* Hay un número finito de nodos y el recorrido es infinito, así que algún nodo se repite. Sea `mu` el menor índice cuyo nodo reaparece más tarde, y `lam` el menor `d >= 1` con `x_{mu+d} = x_mu`.
  - *Periodicidad.* Aplicando `sig` repetidamente a `x_mu = x_{mu+lam}`: `x_i = x_{i+lam}` para todo `i >= mu`.
  - *(⇐)* Si `a >= mu` y `b - a = q·lam`, `x_a = x_b` por la periodicidad.
  - *(⇒)* Si `x_a = x_b` con `a < b`, entonces `a >= mu` por la minimalidad de `mu`. Sea `d = b - a = q·lam + r` con `0 <= r < lam`. Por la periodicidad `x_a = x_{a+d} = x_{a+r}`, y aplicando `sig`, `x_{a+j} = x_{a+r+j}` para todo `j >= 0`. Elijo `j >= 0` con `a + j = mu + s·lam`; entonces `x_mu = x_{mu+r}`. Si `r > 0`, contradice la minimalidad de `lam`. Luego `r = 0`.
  - *`N = mu + lam`.* Los nodos `x_0, ..., x_{mu+lam-1}` son distintos por lo anterior, y todo `x_k` es igual a uno de ellos.
- **Lema 3.** Con ciclo y `t >= 1`: `x_t = x_{2t}` si y solo si `t >= mu` y `lam` divide a `t`. Es el Lema 2 con `a = t`, `b = 2t`. Entonces el primer instante en que coinciden es `t* = lam · ⌈max(mu, 1) / lam⌉`, el menor múltiplo de `lam` que es `>= max(mu, 1)`. Y `t* <= mu + lam`: si `mu >= 1`, ese múltiplo es `<= mu + lam - 1`; si `mu = 0`, es `lam`.

**Terminación (potencial).** Sea `Φ = N - t`.

- Se decrementa: cada vuelta suma 1 a `t`, así que `Φ` baja exactamente 1.
- **Claim:** cada vez que la guarda es verdadera, `Φ >= 1`, es decir `t < N`.
  - **Sin ciclo:** guarda verdadera ⇒ `x_{2t+1} != null` ⇒ `2t + 1 <= m - 1` ⇒ `t <= (m - 2)/2 < m = N`.
  - **Con ciclo:** si la guarda se evaluara con `t >= t*`, I2 con `s = t*` diría `x_{t*} != x_{2t*}`, lo que contradice el Lema 3. Entonces `t < t* <= mu + lam = N`.
- `Φ` empieza en `N`, baja 1 por vuelta y es `>= 1` al entrar a cada una. Luego hay a lo sumo `N` vueltas: el algoritmo termina.

**Conclusión.** El algoritmo termina para toda lista, y devuelve `true` si y solo si hay ciclo:

- **(⇒)** Si devuelve `true`, hay ciclo (Corolario A).
- **(⇐)** Si hay ciclo, no puede devolver `false` (Corolario B), y como termina, devuelve `true`. ∎

## Complejidad

**Vueltas exactas.**

- **Sin ciclo, con `m` nodos:** `⌊m / 2⌋`. La vuelta `t` se ejecuta si y solo si `x_{2t+1} != null`, es decir `2t + 1 <= m - 1`.
- **Con ciclo (`mu`, `lam`):** `t* = lam · ⌈max(mu, 1) / lam⌉`. Todos los `x_k` son no nulos, así que la guarda nunca falla, y el algoritmo devuelve `true` en la primera vuelta `t >= 1` con `x_t = x_{2t}`, que es `t*` por el Lema 3.

**Peor caso con `N` nodos alcanzables: `N` vueltas.** Sin ciclo son `⌊N/2⌋ <= N`. Con ciclo son `t* <= mu + lam = N`, y la igualdad ocurre solo con `mu = 0` (para `mu >= 1`, `t* <= mu + lam - 1`), es decir cuando toda la lista es un ciclo. Allí `rapido` da una vuelta completa antes de alcanzar a `lento`.

**Resumen.** Tiempo `Θ(n)` en el peor caso, con `n` los nodos de la lista, y `O(1)` de memoria extra (los dos punteros). El mejor caso es 0 vueltas (lista vacía o de un nodo sin ciclo). El algoritmo no necesita conocer `n` ni marcar nodos.

## Casos de prueba

| Caso | Lista | ¿ciclo? | Devuelve | Vueltas | Fórmula |
|---|---|---|---|---|---|
| lista vacía | `null` | no | false | 0 | 0 |
| 1 nodo, sin ciclo | `0→null` | no | false | 0 | 0 |
| 1 nodo, se apunta a sí mismo | `0→0` | sí | true | 1 | 1 |
| 2 nodos, sin ciclo | `0→1→null` | no | false | 1 | 1 |
| 2 nodos, ciclo de 2 | `0→1→0` | sí | true | 2 | 2 |
| 5 nodos, sin ciclo | `0→1→2→3→4→null` | no | false | 2 | 2 |
| cola 3, ciclo 4 | `0→1→2→3→4→5→6→3` | sí | true | 4 | 4 |
| cola 5, ciclo 1 | `0→1→2→3→4→5→5` | sí | true | 5 | 5 |
| cola 1, ciclo 2 | `0→1→2→1` | sí | true | 2 | 2 |
| ciclo puro de 6 | `0→1→2→3→4→5→0` | sí | true | 6 | 6 |

Traza sobre `0→1→2→3→4→5→6→3` (cola 3, ciclo 4), con `mu = 3`, `lam = 4` y `t* = 4`:

| t | lento = x_t | rapido = x_2t | ¿lento == rapido? |
|---|---|---|---|
| 0 | 0 | 0 | — |
| 1 | 1 | 2 | no |
| 2 | 2 | 4 | no |
| 3 | 3 | 6 | no |
| 4 | 4 | 4 | sí |

Peor caso¹ (el ciclo puro siempre es el peor):

| N | peor sin ciclo (⌊N/2⌋) | peor en total | forma del peor caso |
|---|---|---|---|
| 1 | 0 | 1 | cola 0, ciclo 1 |
| 4 | 2 | 4 | cola 0, ciclo 4 |
| 8 | 4 | 8 | cola 0, ciclo 8 |
| 12 | 6 | 12 | cola 0, ciclo 12 |

Búsqueda exhaustiva¹ sobre todas las funciones `sig` de `n` nodos y todas las cabezas (incluida `null`):

| n | entradas | con ciclo | sin ciclo | errores |
|---|---|---|---|---|
| 1 | 4 | 1 | 3 | 0 |
| 2 | 27 | 10 | 17 | 0 |
| 3 | 256 | 114 | 142 | 0 |
| 4 | 3125 | 1556 | 1569 | 0 |
| 5 | 46656 | 25080 | 21576 | 0 |
| 6 | 823543 | 468462 | 355081 | 0 |

¹ **Verificación en código** (`verificar_ejercicio_05.py`, Python 3, sin dependencias):

- Casos de prueba fijos y la traza: coinciden con las tablas de arriba.
- **Invariante y potencial ejecutables:** una versión instrumentada del algoritmo comprueba I1, I2, `Φ >= 1` al entrar a cada vuelta, que `Φ` baja en 1, y los dos corolarios. Pasó en todas las listas sin ciclo de hasta 40 nodos, en todas las formas con ciclo con `mu + lam <= 25`, y en la búsqueda exhaustiva para `n <= 5`.
- **Fórmulas de vueltas:** `⌊m/2⌋` sin ciclo y `lam·⌈max(mu,1)/lam⌉` con ciclo coinciden con lo observado en las 1640 formas con cola `mu` entre 0 y 40 y ciclo `lam` entre 1 y 40, y en las 41 listas sin ciclo de 0 a 40 nodos. También se comprobó `max(mu,1) <= t* <= mu + lam`.
- **Peor caso:** para `N = 1..12` el máximo de vueltas es `N`, alcanzado solo por el ciclo puro.
- **Búsqueda exhaustiva** (tabla de arriba, `n <= 6`): el resultado coincide siempre con una fuerza bruta basada en conjuntos de nodos visitados, y el número de vueltas con la fórmula.
- **Pruebas aleatorias** contra la misma fuerza bruta, con dos generadores (formas con cola y ciclo con nodos permutados, y funciones `sig` al azar) y `n = 10, 50, 300` (24 000 listas): 0 errores.
