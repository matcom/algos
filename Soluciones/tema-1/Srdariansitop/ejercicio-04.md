# Pregunta 4

El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $O(\log m)$. Es la pregunta que la conferencia 1 dejó abierta.

## Planteamiento

### Convención

El número se escribe con el bit menos significativo (LSB) a la izquierda: la cinta contiene $b_0 b_1 b_2 \dots b_{k-1}$ y a la derecha de $b_{k-1}$ solo hay blancos $\sqcup$. El cabezal empieza sobre $b_0$. Esta orientación hace que el cabezal "empiece y termine en el LSB" sin cálculos extra; si prefieres el LSB a la derecha, es la misma máquina con $L$ y $R$ intercambiados.

### Idea

Es el algoritmo del acarreo: mientras veas un $1$, ponlo a $0$ y avanza (el acarreo se propaga). Al primer $0$ (o blanco), ponlo a $1$ y para la propagación. Después, rebobina hasta el inicio.

Para saber dónde rebobinar sin marcar nada, usamos un truco: **los bits que acabamos de poner a $0$ son exactamente un prefijo de ceros**, y el bit recién puesto a $1$ es el único $1$ de ese prefijo. Pero al volver no podemos distinguir ese prefijo del resto del número, así que necesitamos un marcador de borde. Solución estándar: el primer símbolo de la cinta lleva una marca, es decir, alfabeto $\{0,1,\hat 0,\hat 1,\sqcup\}$, donde $\hat 0,\hat 1$ son los bits en la posición $0$ (inicialmente $\hat 0$ para el número $0$). Así, al retroceder, paramos al leer un símbolo con sombrero.

## Demostración

**Lema 1 (coste de un incremento).** Sea $t$ la longitud del prefijo máximo de unos, es decir, $b_0 = \dots = b_{t-1} = 1$ y $b_t \ne 1$. Entonces el incremento cuesta exactamente
$$c = 2t + 1 \text{ pasos.}$$

*Demostración.* Si $t = 0$, la primera celda contiene $\hat 0$ y se aplica la tercera regla: se ejecuta un único paso, y $2\cdot 0 + 1 = 1$. Si $t \ge 1$, la máquina emplea $t$ pasos en poner a $0$ los unos del prefijo, uno más en escribir $1$ en la posición $t$ y retroceder a la posición $t-1$, otros $t-1$ pasos en alcanzar la posición $0$ y un último paso en leer la marca y detenerse. El total es $t + 1 + (t-1) + 1 = 2t + 1$. ∎

**Corolario (peor caso de una operación).** Si el contador vale $2^k - 1$, todos sus $k$ bits son unos, de modo que $t = k$ y el coste es $2k + 1 = \Theta(k) = \Theta(\log n)$. Una única operación puede, por tanto, costar $\Theta(\log n)$.

**Teorema.** Partiendo de la cinta que representa $0$, $m$ incrementos consecutivos cuestan en total a lo sumo $3m$ pasos; en consecuencia, el coste total es $\Theta(m)$.

**Definición del potencial.** Para una configuración $D$ de la cinta se define
$$\Phi(D) = 2 \cdot \#\{\, j : b_j = 1 \,\}.$$
El potencial mide la deuda acumulada: cada $1$ presente en la cinta representa un acarreo que habrá de pagarse en algún incremento posterior. Se verifican dos propiedades:

1. $\Phi(D_0) = 0$, pues la cinta inicial no contiene unos.
2. $\Phi(D_i) \ge 0$ para todo $i$. Por consiguiente, el potencial termina al menos donde empezó, que es precisamente la condición exigida para que la suma telescópica sea válida.

**Lema 2 (coste amortizado).** Para todo incremento $i$, el coste amortizado $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$ vale exactamente $3$.

*Demostración.* Sea $t$ la longitud del prefijo de unos en el incremento $i$. Los $t$ unos del prefijo pasan a $0$ y el bit de la posición $t$ pasa a $1$, de modo que el número de unos varía en $1 - t$ y
$$\Phi(D_i) - \Phi(D_{i-1}) = 2(1 - t) = 2 - 2t.$$
Por el Lema 1, $c_i = 2t + 1$. Luego
$$\hat c_i = (2t + 1) + (2 - 2t) = 3. \qquad ∎$$

La ponderación por $2$ en la definición de $\Phi$ responde a que cada unidad de $t$ se paga dos veces en la máquina (propagación y rebobinado). Con peso $1$ se obtendría $\hat c_i = t + 2$, que aún depende de $t$.

**Demostración del teorema.** Reordenando la definición de coste amortizado y sumando sobre $i = 1, \dots, m$, los términos del potencial se cancelan por telescopía:
$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat c_i - \sum_{i=1}^{m} \bigl(\Phi(D_i) - \Phi(D_{i-1})\bigr) = 3m - \Phi(D_m) + \Phi(D_0).$$
Como $\Phi(D_0) = 0$ y $\Phi(D_m) \ge 0$, resulta
$$\sum_{i=1}^{m} c_i = 3m - \Phi(D_m) \le 3m.$$
Por otra parte, cada incremento cuesta al menos $1$ paso, de modo que el total es $\ge m$. En consecuencia, el coste total es $\Theta(m)$. ∎

**Verificación numérica.** Para los cuatro primeros incrementos:

| $i$ | cinta (LSB a la izquierda) | $t$ | $c_i$ | $\Phi(D_i)$ | $\hat c_i$ |
|---|---|---|---|---|---|
| $0$ | $000$ | – | – | $0$ | – |
| $1$ | $100$ | $0$ | $1$ | $2$ | $3$ |
| $2$ | $010$ | $1$ | $3$ | $2$ | $3$ |
| $3$ | $110$ | $0$ | $1$ | $4$ | $3$ |
| $4$ | $001$ | $2$ | $5$ | $2$ | $3$ |

La suma real es $1 + 3 + 1 + 5 = 10$, y coincide con $3 \cdot 4 - \Phi(D_4) = 12 - 2 = 10$.

**Interpretación.** Un incremento costoso solo ocurre cuando el prefijo de unos es largo, y esos unos fueron creados en incrementos anteriores, uno por incremento. Cada uno lleva asociadas dos unidades de crédito, una para la propagación y otra para el rebobinado. Cada incremento deposita dos unidades por el uno que crea y consume una por su trabajo fijo, de donde resulta el coste amortizado $3$. La cota obtenida es una garantía de peor caso sobre secuencias: no interviene ninguna noción de promedio ni de probabilidad.

**Conclusión.** En el peor caso, una sola operación cuesta $\Theta(k) = \Theta(\log n)$ pasos. En cambio, $m$ incrementos consecutivos desde $0$ cuestan a lo sumo $3m$ pasos, es decir, $\Theta(m)$ en total y $O(1)$ amortizado por incremento.

# Código (Extra 04)

## Figura 1: traza de un incremento (3 → 4)

Muestra la máquina paso a paso con $t = 2$. Los datos están escritos a mano en `pasos`, sin usar el simulador. El color indica la fase: rojo para la ida, verde para la escritura del 1 y azul para el rebobinado. Las flechas rojas marcan el cabezal. El total son $5 = 2t+1$ pasos. La marca de borde se omite por claridad.

## Figura 2: tabla de 0 a 8

Usa `historial(8, 4)`. Por cada incremento muestra la cinta (verde para 0→1, rojo para 1→0), $t$, el coste real, $\Phi$, $\Delta\Phi$ y el coste amortizado, que es siempre 3. Al pie comprueba $22 = 3\cdot 8 - 2 + 0$. Los incrementos caros (4 y 8) coinciden con $\Delta\Phi < 0$.

## Figura 3: coste por incremento (1 a 32)

Usa `historial(32, 6)` y dibuja los costes reales como barras. Las líneas de referencia son el coste amortizado (3), la media real (≈ 2,94) y el peor caso de una operación ($2k+1 = 13$). Los costes altos son escasos: el incremento con $t$ unos aparece cada $2^t$ pasos.

## Figura 4: potencial y suma telescópica

Usa `historial(40, 7)` y calcula $\Phi(D_i)$ y el coste real acumulado.

- **Panel izquierdo:** $\Phi$ como función escalonada, siempre $\ge 0$ y con $\Phi(D_0) = 0$.
- **Panel derecho:** la recta $3m$ frente al coste acumulado. El hueco entre ambas es exactamente $\Phi(D_m) \ge 0$, lo que visualiza $\sum c_i = 3m - \Phi(D_m) \le 3m$.