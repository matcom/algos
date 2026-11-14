# Ejercicio 4. El contador binario en una máquina de Turing

Dificultad: ★★ · Código: [`ejercicio-04.py`](ejercicio-04.py)

---

## Enunciado

> El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(\log m)$.

## Qué se pide

1. Calcular el costo real (en pasos de la máquina) de un incremento.
2. Mostrar que un incremento aislado puede costar $\Theta(\log m)$.
3. Definir un potencial y demostrar que el costo amortizado de cada incremento es constante.
4. Concluir que $m$ incrementos desde 0 cuestan $O(m)$.

## Preliminares

**La máquina.** Cinta con un bit por celda. El bit menos significativo (LSB) está en la posición $0$ y los más significativos en $-1, -2, \dots$; el resto es blanco `_`. El cabezal empieza y termina en el LSB. Cada transición cuenta como **un paso**.

| estado | lee | escribe | mueve | estado nuevo |
|---|---|---|---|---|
| `inc` | `1` | `0` | izquierda | `inc` |
| `inc` | `0` | `1` | derecha | `ret` |
| `inc` | `_` | `1` | derecha | `ret` |
| `ret` | `0` | `0` | derecha | `ret` |
| `ret` | `1` | `1` | derecha | `ret` |
| `ret` | `_` | `_` | izquierda | `alto` |

- **Fase 1 (`inc`, acarreo).** Mientras lee `1`, lo cambia por `0` y va a la izquierda. Al leer `0` o blanco lo cambia por `1`, va a la derecha y pasa a `ret`.
- **Fase 2 (`ret`, vuelta).** Avanza a la derecha sin escribir. Al llegar al blanco a la derecha del LSB retrocede una celda y se detiene en el LSB.

**Ejemplo.** El número $0111$ (siete) pasa a $1000$ (ocho):

| fase | qué ocurre | pasos |
|---|---|---|
| 1 | cambia los tres `1` por `0` | 3 |
| 1 | cambia el `0` por `1` | 1 |
| 2 | vuelve por 3 celdas hasta el LSB | 3 |
| 2 | lee el blanco y retrocede | 1 |
| | **total** | **8** |

**Análisis amortizado** (Conferencia 4). Con $c_i$ el costo real de la operación $i$ y $\Phi_i$ el potencial después de ella, el costo amortizado es

$$\hat{c}_i = c_i + \Phi_i - \Phi_{i-1}.$$

---

## Costo real de un incremento

Sea $t$ el número de unos consecutivos al final del número: los $t$ bits menos significativos valen $1$ y el siguiente es $0$ o blanco.

**Lema 1.** Un incremento cuesta exactamente $c = 2t + 2$ pasos.

**Demostración.**

**Paso 1. Fase 1.** Cambia los $t$ unos por ceros ($t$ pasos) y escribe el $1$ en la posición $-t$ (1 paso): $t + 1$ pasos.

**Paso 2. Fase 2.** Desde la posición $-t$ avanza a la derecha. Atraviesa las celdas $-t+1, \dots, 0$ ($t$ pasos) y lee el blanco de la posición $1$ (1 paso, en el que retrocede): $t + 1$ pasos. Esa celda está siempre en blanco, porque la máquina nunca escribe a la derecha del LSB.

**Paso 3.** Total: $(t+1) + (t+1) = 2t + 2$. $\blacksquare$

**Comprobación.** Con $t = 0$ cuesta $2$; con $t = 3$ (ejemplo de arriba), $8$.

**Un incremento puede costar $\Theta(\log m)$.** Pasar de $2^k - 1$ (que son $k$ unos) a $2^k$ cuesta $2k + 2$ pasos. Con $m = 2^k - 1$, $k \approx \log_2 m$: el incremento cuesta unos $2\log_2 m$ pasos.

La cota ingenua «cada incremento cuesta $O(\log m)$, luego $m$ incrementos cuestan $O(m \log m)$» es correcta pero floja. Se verá que la cota real es $O(m)$.

---

## El potencial

El costo real de un incremento depende de cuántos unos finales rompe. Para que el costo promedio no dependa de eso, el potencial guarda de antemano el trabajo que los unos van a causar.

$$\Phi = 2\cdot(\text{número de unos en el contador}).$$

**Intuición.** Cada `1` guarda dos monedas: son el trabajo pendiente de un acarreo futuro que pasará por él (un paso de ida y otro de vuelta).

**Propiedades exigidas por el método** (Conferencia 4):

1. $\Phi_0 = 0$, porque el contador empieza en $0$ y no tiene unos.
2. $\Phi_i \ge 0$ para todo $i$, porque el número de unos no es negativo.

---

## Costo amortizado

Con el costo real y el potencial definidos, se suman para obtener el costo amortizado de un incremento.

**Teorema 1.** Cada incremento tiene costo amortizado $\hat{c} = 4$.

**Demostración.** Sea un incremento con $t$ unos finales.

**Paso 1. Costo real.** $c = 2t + 2$ (Lema 1).

**Paso 2. Cambio en el número de unos.** Los $t$ unos finales pasan a ser ceros y el primer cero (o blanco) pasa a ser uno; el resto no cambia:

$$\Delta(\text{unos}) = -t + 1$$

**Paso 3. Cambio de potencial.**

$$\Delta\Phi = 2(1 - t) = 2 - 2t$$

**Paso 4. Costo amortizado.**

$$\hat{c} = c + \Delta\Phi = (2t + 2) + (2 - 2t) = 4. \qquad\blacksquare$$

La variable $t$ se cancela: cada incremento cuesta $4$ amortizado, sin importar cuántos unos rompa.

**Casos especiales.**

- *Todos los bits son 1.* El acarreo llega a un blanco, que se cambia por `1`. El costo y el cambio de unos son los mismos, luego $\hat{c} = 4$.
- **$t = 0$.** El costo real es $2$ y hay un uno más: $\Delta\Phi = 2$, luego $\hat{c} = 4$.

---

## La suma de $m$ incrementos

El costo amortizado es constante. Falta pasar de ahí al costo total real de los $m$ incrementos.

**Teorema 2.** $m$ incrementos desde $0$ cuestan en total exactamente

$$\sum_{i=1}^{m} c_i = 4m - 2\,s_2(m),$$

donde $s_2(m)$ es el número de unos de la representación binaria de $m$. En particular, el total es menor que $4m$, es decir, $O(m)$.

**Demostración.**

**Paso 1.** Por el Teorema 1, la suma de costos amortizados es

$$\sum_{i=1}^{m} \hat{c}_i = 4m.$$

**Paso 2.** Por la definición de $\hat{c}_i$, la suma de potenciales se telescopa:

$$\sum_{i=1}^{m} \hat{c}_i = \sum_{i=1}^{m} c_i + \Phi_m - \Phi_0.$$

**Paso 3.** Se despeja la suma de costos reales:

$$\sum_{i=1}^{m} c_i = 4m - (\Phi_m - \Phi_0).$$

**Paso 4.** Después de $m$ incrementos desde $0$ el contador vale $m$, así que $\Phi_m = 2\,s_2(m)$, y $\Phi_0 = 0$:

$$\sum_{i=1}^{m} c_i = 4m - 2\,s_2(m).$$

**Paso 5.** Como $s_2(m) \ge 1$ para $m \ge 1$, el total es menor que $4m$. $\blacksquare$

**Comprobación (contando de 0 a 8):**

| incremento | valor antes | $t$ | pasos $2t+2$ | acumulado | $4m - 2s_2(m)$ |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 2 | 2 | 2 |
| 2 | 1 | 1 | 4 | 6 | 6 |
| 3 | 2 | 0 | 2 | 8 | 8 |
| 4 | 3 | 2 | 6 | 14 | 14 |
| 5 | 4 | 0 | 2 | 16 | 16 |
| 6 | 5 | 1 | 4 | 20 | 20 |
| 7 | 6 | 0 | 2 | 22 | 22 |
| 8 | 7 | 3 | 8 | 30 | 30 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-04-costos-oscuro.svg">
  <img src="figuras/ejercicio-04-costos-claro.svg" alt="Costo real, potencial y costo amortizado de cada incremento, y el total acumulado">
</picture>

**Figura 1.** Izquierda: el costo real de los primeros $16$ incrementos (barras) y el potencial después de cada uno. Lo que un incremento caro cuesta por encima de $4$ lo compensa la caída del potencial, y el costo amortizado queda en $4$. Derecha: el total real de $32$ incrementos queda siempre por debajo de $4m$, y en $m = 32$ vale $4 \cdot 32 - 2 = 126$.

**Por qué hace falta empezar desde 0.** El método exige $\Phi_m \ge \Phi_0$. Si el contador empezara con $k$ unos, $\Phi_0 = 2k$ y la cota sería $4m + 2k$.

---

## Verificación con código

El archivo [`ejercicio-04.py`](ejercicio-04.py) simula la máquina de Turing paso a paso sobre la cinta (con la tabla de transiciones de arriba) y cuenta los pasos reales. Resultados (salida del programa):

| $m$ | valor antes | $t$ | pasos $2t+2$ | acumulado | $4m - 2s_2(m)$ |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 2 | 2 | 2 |
| 2 | 1 | 1 | 4 | 6 | 6 |
| 3 | 2 | 0 | 2 | 8 | 8 |
| 4 | 3 | 2 | 6 | 14 | 14 |
| 5 | 4 | 0 | 2 | 16 | 16 |
| 6 | 5 | 1 | 4 | 20 | 20 |
| 7 | 6 | 0 | 2 | 22 | 22 |
| 8 | 7 | 3 | 8 | 30 | 30 |

| $m$ | total de pasos | total$/m$ | incremento más caro hasta ahora |
|---|---|---|---|
| 10 | 36 | 3,600 | 8 pasos |
| 1000 | 3988 | 3,988 | 20 pasos |
| 4096 | 16382 | 4,000 | 26 pasos |
| 65536 | 262142 | 4,000 | 34 pasos |

El total simulado coincide con $4m - 2s_2(m)$ en cada fila. Con $m = 65\,536$ el incremento más caro cuesta $34$ pasos ($\approx 2\log_2 m$), pero el promedio por incremento es $4$.

## Resumen de resultados

1. **Costo real:** un incremento con $t$ unos finales cuesta $2t + 2$ pasos; el peor cuesta $\Theta(\log m)$.
2. **Potencial:** $\Phi = 2\cdot(\text{unos})$, con $\Phi_0 = 0$ y $\Phi \ge 0$.
3. **Costo amortizado:** $(2t+2) + (2-2t) = 4$ para todo incremento.
4. **Total:** $\sum c_i = 4m - 2s_2(m) < 4m = O(m)$.

## Referencias

- Conferencia 1, ejercicio 7: el contador binario en una máquina de Turing.
- Conferencia 4, §2–§3: método del potencial, el requisito $\Phi_m \ge \Phi_0$ y qué es un buen potencial.
