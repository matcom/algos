# Problema 4 ★★

**Enunciado.** El contador binario en una máquina de Turing. Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(\log m)$.

## Solución formal

**Modelo.** Contador binario en una cinta de máquina de Turing con el bit menos significativo (LSB) en la posición 0. El cabezal comienza en 0 y debe volver a 0 tras cada incremento. La operación `incrementar` suma 1 al número binario.

**Variables.**

- $m$: número total de incrementos, partiendo del contador en 0.
- $k$: número de bits 1 consecutivos al final del contador (bits menos significativos que son 1).
- $\Phi$: potencial, definido como $2 \times (\text{número de bits 1 en el contador})$. Es decir, $\Phi = 2 \cdot \text{popcount}$.
- $c$: costo real de un incremento, medido en pasos de la máquina de Turing.
- $\hat{c}$: costo amortizado, $\hat{c} = c + \Delta\Phi$, con $\Delta\Phi = \Phi_{\text{despues}} - \Phi_{\text{antes}}$.

**Cambio en el número de unos.** Al incrementar, los $k$ bits 1 menos significativos se convierten en 0 (se pierden $k$ unos) y el siguiente bit 0 se convierte en 1 (se gana 1 uno). Por tanto,

$$
\Delta(\#\text{unos}) = 1 - k.
$$

El potencial cambia en

$$
\Delta\Phi = 2(1 - k) = 2 - 2k.
$$

**Costo real de un incremento.** Con $k$ unos finales, el cabezal recorre $k$ posiciones cambiando 1 por 0, luego cambia el 0 por 1 (1 paso), y vuelve $k$ posiciones al LSB. Así,

$$
c = k + 1 + k = 2k + 1.
$$

**Costo amortizado.**

$$
\hat{c} = c + \Delta\Phi = (2k + 1) + (2 - 2k) = 3.
$$

El término $2k$ se cancela, por lo que cada incremento tiene costo amortizado constante $3$.

**Suma total.** Sea $\Phi_i$ el potencial tras el $i$-ésimo incremento. $\Phi_0 = 0$ y $\Phi_i \ge 0$ para todo $i$. Entonces:

$$
\sum_{i=1}^m c_i = \sum_{i=1}^m (\hat{c}_i - \Delta\Phi_i) = \sum_{i=1}^m \hat{c}_i - (\Phi_m - \Phi_0) \le \sum_{i=1}^m \hat{c}_i = 3m = O(m).
$$

Por lo tanto, el costo total real de $m$ incrementos es a lo sumo $3m = O(m)$.

**Conclusión.** Un incremento individual puede costar $\Theta(\log m)$ (por ejemplo, incrementar $2^b-1$ cuesta $2b+1$ pasos), pero el costo amortizado por incremento es constante (3), y el costo total es $O(m)$.
