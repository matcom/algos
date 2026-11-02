## Problema 4
El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un
potencial que m  incrementos desde 0 cuestan O(m) pasos en total, aunque uno solo pueda costar O(logm)
. Es la pregunta que la conferencia 1 dejó abierta.

### Respuesta


- Alfabeto de la cinta: $\Gamma = \{0, 1, \square\}$, donde $\square$ es el blanco.
- El número se escribe con el bit más significativo a la izquierda y el menos significativo (LSB) a la derecha. Numero las celdas por su peso: la celda del LSB es la posición $0$, la de su izquierda es la $1$, etc. La celda a la derecha del LSB (posición $-1$) siempre está en blanco.
- A la izquierda del bit más significativo todo es $\square$, y un $\square$ se interpreta como un $0$.
- El 0 inicial es la cinta completamente en blanco, con el cabezal en la posición $0$.


Estados: $q_{\text{inc}}$ (inicial, propagando el acarreo), $q_{\text{vuelta}}$ (regresando al LSB) y $q_f$ (final).

| Estado | Lee | Escribe | Mueve | Nuevo estado |
|---|---|---|---|---|
| $q_{\text{inc}}$ | $1$ | $0$ | $L$ | $q_{\text{inc}}$ |
| $q_{\text{inc}}$ | $0$ | $1$ | $R$ | $q_{\text{vuelta}}$ |
| $q_{\text{inc}}$ | $\square$ | $1$ | $R$ | $q_{\text{vuelta}}$ |
| $q_{\text{vuelta}}$ | $0$ | $0$ | $R$ | $q_{\text{vuelta}}$ |
| $q_{\text{vuelta}}$ | $1$ | $1$ | $R$ | $q_{\text{vuelta}}$ |
| $q_{\text{vuelta}}$ | $\square$ | $\square$ | $L$ | $q_f$ |

Idea. En $q_{\text{inc}}$ la máquina hace la suma de la escuela: cada $1$ que encuentra se vuelve $0$ y el acarreo sigue hacia la izquierda; el primer $0$ (o blanco) se vuelve $1$ y el acarreo muere. Después, en $q_{\text{vuelta}}$, camina a la derecha hasta encontrar el blanco que está justo después del LSB, y retrocede una celda para quedar sobre el LSB.

Correctitud. Si el número termina en exactamente $t$ unos, es de la forma $x\,0\,\underbrace{1\cdots1}_{t}$ (con el $0$ posiblemente un blanco). Sumarle 1 da $x\,1\,\underbrace{0\cdots0}_{t}$, que es justo lo que escribe la fase $q_{\text{inc}}$. En la vuelta, todas las celdas entre la posición $t-1$ y la $0$ contienen $0$ (no blanco, porque se acaban de escribir), así que $q_{\text{vuelta}}$ no se detiene antes de tiempo. La celda $-1$ nunca se escribe, así que es blanco y la máquina se detiene sobre la posición $0$. El invariante "la celda $-1$ es blanco y no hay blancos entre el bit más significativo y el LSB" se conserva en cada incremento.

Costo de un incremento:

Sea $t$ el número de unos al final del número (los unos consecutivos empezando por el LSB).

1. $q_{\text{inc}}$ lee $t$ unos: $t$ pasos, y el cabezal queda en la posición $t$.
2. $q_{\text{inc}}$ escribe el $1$ en la posición $t$ y se mueve a la $t-1$: 1 paso.
3. $q_{\text{vuelta}}$ recorre las posiciones $t-1, \dots, 0$ hacia la derecha: $t$ pasos, y queda en la posición $-1$.
4. $q_{\text{vuelta}}$ lee el blanco y vuelve a la posición $0$: 1 paso.

$$
c(t) = 2t + 2.
$$

(Comprobación con $t = 0$: escribe el 1 en el LSB, pasa a la posición $-1$, lee el blanco y vuelve. Son 2 pasos.)


Si el número tiene $k$ bits, $t \le k$, así que un incremento cuesta a lo sumo $2k + 2 = O(k)$, y la cota se alcanza con $11\cdots1$ (son $k$ unos que se vuelven ceros y el número pasa a tener $k+1$ bits). El peor caso es $\Theta(k)$.

Dentro de una secuencia de $n$ incrementos desde 0, el incremento número $i$ parte del valor $i - 1$. Si ese valor termina en $t$ unos, entonces $i - 1 \ge 2^t - 1$, es decir, $t \le \log_2 i \le \log_2 n$. Y la cota se alcanza: si $n = 2^j$, el último incremento parte de $2^j - 1 = \underbrace{1\cdots1}_{j}$ y cuesta $2j + 2 = \Theta(\log n)$.

Así que un solo incremento puede costar $\Theta(\log n)$, y la cota ingenua para la secuencia completa es $n \cdot O(\log n) = O(n \log n)$. Hay que demostrar que en realidad es $O(n)$.

Sea $D_i$ el contenido de la cinta después del incremento $i$ (con $D_0$ la cinta en blanco). Defino

$$
\Phi(D) = 2 \cdot (\text{número de unos en la cinta}).
$$

Propiedades del potencial:

- $\Phi(D_0) = 0$, porque la cinta empieza en blanco.
- $\Phi(D_i) \ge 0$ para todo $i$, porque cuenta unos.

Cambio de potencial en un incremento. Si el número antes del incremento $i$ termina en $t_i$ unos, el incremento convierte esos $t_i$ unos en ceros y exactamente un $0$ (o blanco) en $1$. Ninguna otra celda cambia. Entonces

$$
\Delta\Phi_i = \Phi(D_i) - \Phi(D_{i-1}) = 2\,(1 - t_i).
$$

Costo amortizado. Con $c_i = 2t_i + 2$ el costo real,

$$
\hat c_i = c_i + \Delta\Phi_i = (2t_i + 2) + (2 - 2t_i) = 4.
$$

El costo amortizado de cada incremento es exactamente 4, sin importar $t_i$. La intuición: cada $1$ que se escribe "guarda" 2 unidades de potencial, y esas son justo las que pagan los 2 pasos (ida y vuelta) que costará convertirlo en $0$ en el futuro.

Suma telescópica.

$$
\sum_{i=1}^{n} \hat c_i = \sum_{i=1}^{n} \bigl(c_i + \Phi(D_i) - \Phi(D_{i-1})\bigr) = \sum_{i=1}^{n} c_i + \Phi(D_n) - \Phi(D_0).
$$

Despejando, y usando $\Phi(D_n) \ge 0$ y $\Phi(D_0) = 0$:

$$
\sum_{i=1}^{n} c_i = \sum_{i=1}^{n} \hat c_i - \Phi(D_n) + \Phi(D_0) \le 4n.
$$

Cota inferior. Cada incremento cuesta al menos $c(0) = 2$ pasos, así que el total es al menos $2n$.

