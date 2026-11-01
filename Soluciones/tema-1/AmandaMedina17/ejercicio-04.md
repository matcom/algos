**Problema:** El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un
potencial que incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(logm)$.

## Planteamiento del problema y coste real:

Consideramos un contador binario implementado sobre una cinta de una Máquina de Turing, que almacena un número en representación binaria y se incrementa secuencialmente en 1 desde el valor inicial 0.

En una máquina de Turing, el cabezal debe desplazarse y modificar los símbolos de la cinta para realizar el acarreo. El coste de realizar el $i$-ésimo incremento es proporcional al número de bits que cambian de estado.

Cuando el número cambia de $2^k - 1$ a $2^k$ (por ejemplo, al pasar de 0111 a 1000), ocurre un efecto en cadena donde todos los bits $1$ menos significativos se transforman en $0$, y el primer bit $0$ se convierte en $1$. Si este incremento afecta a $k$ bits, el coste real de esa operación específica es $c_i = \Theta(k)$. Como un número $m$ requiere aproximadamente $log_2m$ bits, una operación aislada puede costar $\Theta (log m)$ pasos en el peor de los casos.

## Definición de la función potencial:

- Definición de $\Phi$: Sea $\Phi(D_i)$ igual a la cantidad de bits en $1$ que contiene la representación binaria del contador tras el incremento $i$.
- Estado inicial: Antes de realizar cualquier incremento $(i=0)$, el contador esta en cero $(00...0)$, por lo que no hay bits en $1$ ($\Phi(D_0)=0$).
- Para cualquier estado $i$, el número de bits encendidos es un valor entero no negativo ($$\Phi(D_i) \ge 0 \quad \forall i$$).

## Cálculo del coste amortizado ($c_i^{\text{amortized}}$):

El coste amortizado de la $i$-ésima operación se define formalmante como:
$$c_i^{\text{amortized}} = c_i + \Phi(D_i) - \Phi(D_{i-1})$$

Análisis del $i$-ésimo incremento:

- Supongamos que el incremento provoca que los $k$ bits menos significativos que estaban en $1$ cambien a $0$ (debido al acarreo). Por tanto, se eliminan $k$ unos de la representación.
- Luego, el primer bit de $0$ que se encuentra en el cabezal cambia a $1$. Por tanto, se añade $1$ a la representación.
- El número total de bit que se cambiaron de estado en esta operación es $c_i = k + 1$.
- Antes del incremento había $k$ unos consecutivos que se perdieron, y se añadió un nuevo uno. El cambio de la cantidad de bits en $1$ es $\Phi(D_i) - \Phi(D_{i-1}) = 1 - k$
- Sustituyendo ambos términos en la ecuación del coste amortizado: $$c_i^{\text{amortized}} = (k + 1) + (1 - k) = 2$$

El coste amortizado de cualquier incremento, sin importar cuan costoso sea en la realidad ($c_i = \Theta(\log m)$), es siempre contante: $$c_i^{\text{amortized}} = 2 = {O}(1)$$

## Acotación para m incrementos

Queremos calcular el coste total de realizar $m$ incrementos consecutivos partiendo desde el contador $0$. Sabemos por definición que la suma de los costes reales se relaciona con la suma de los costes amortizados mediante la telescopia del potencial:
$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \left( c_i^{\text{amortized}} - \Phi(D_i) + \Phi(D_{i-1}) \right)$$
Al expandir la sumatoria telescópica, los potenciales intermedios se cancelan mutuamente:$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} c_i^{\text{amortized}} + \Phi(D_m) - \Phi(D_0)$$
Sustituyendo los valores conocidos ($\Phi(D_0) = 0$ y sabiendo que cada coste amortizado está acotado por $2$):$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} 2 + \Phi(D_m) - 0 = 2m + \Phi(D_m)$$
Dado que el potencial final $\Phi(D_m)$ representa la cantidad de bits encendidos que tiene $m$, esta cantidad nunca puede superar el número total de bits de su representación binaria, es decir, $\Phi(D_m) \le \lfloor \log_2 m \rfloor + 1$. Por consiguiente:$$\sum_{i=1}^{m} c_i \le 2m + \log_2 m = {O}(m)$$

## Conclusión:

Aunque una operación individual de incremento en el contador binario de una Máquina de Turing puede requerir un coste en el peor de los casos de $\Theta(\log m)$ pasos debido al arrastre masivo de acarreo, el uso de una función de potencial basada en el número de bits en 1 demuestra que el coste total acumulado de $m$ incrementos sucesivos desde 0 es estrictamente ${O}(m)$.
