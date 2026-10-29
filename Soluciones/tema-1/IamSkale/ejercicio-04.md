# Ejercicio 4 ★★ — El contador binario en una máquina de Turing (C1, C4)

> El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(\log m)$.

## La máquina (ejercicio 7 de la C1)

El número está escrito en binario en la cinta, con el bit más significativo a la izquierda. El cabezal empieza **sobre el bit menos significativo** (LSB) y tiene que volver a él al terminar. Alfabeto $\{0,1,\sqcup\}$, estados $q_{inc}$, $q_{vuelta}$, $q_{fin}$.

| estado | lee | escribe | mueve | nuevo estado |
|---|---|---|---|---|
| $q_{inc}$ | 1 | 0 | ← | $q_{inc}$ |
| $q_{inc}$ | 0 o $\sqcup$ | 1 | → | $q_{vuelta}$ |
| $q_{vuelta}$ | 0 o 1 | (igual) | → | $q_{vuelta}$ |
| $q_{vuelta}$ | $\sqcup$ | $\sqcup$ | ← | $q_{fin}$ |

En $q_{inc}$ se propaga el acarreo hacia la izquierda, cambiando los 1 por 0 hasta encontrar un 0 o un blanco, que pasa a 1. En $q_{vuelta}$ se camina a la derecha hasta el blanco que sigue al LSB y se retrocede uno.

**Costo de un incremento.** Si el número termina en $t$ unos ($t$ = cantidad de 1 finales):
- $t$ pasos cambiando 1→0,
- 1 paso escribiendo el 1,
- $t$ pasos volviendo a la derecha sobre esos bits,
- 1 paso del blanco al LSB.

$$c = 2t+2 .$$

**Peor caso de un incremento.** Si el número es $2^k-1$ (todo unos, $k$ bits), $t=k$ y $c=2k+2$. Entre los primeros $m$ incrementos aparece $i=2^{\lfloor\log_2 m\rfloor}-1$, así que el peor incremento cuesta $2\lfloor\log_2 m\rfloor+2=\Theta(\log m)$. La cota ingenua sería entonces $O(m\log m)$ en total.

## Potencial

$$\Phi = 2\cdot(\text{número de unos en la cinta}).$$

- $\Phi_0=0$ (la cinta empieza con "0") y $\Phi\ge0$ siempre.
- Un incremento con $t$ unos finales convierte $t$ unos en ceros y un 0 (o blanco) en 1, así que la cantidad de unos cambia en $1-t$ y $\Delta\Phi=2(1-t)$.
- Costo amortizado:
$$\hat c = c+\Delta\Phi = (2t+2)+2(1-t) = 4 .$$

Sumando (los potenciales se telescopian):
$$\sum_{i=1}^m c_i=\sum_{i=1}^m\hat c_i-(\Phi_m-\Phi_0)=4m-\Phi_m\le 4m .$$

Como $\Phi_m\ge\Phi_0$, la suma de los amortizados acota la de los reales: **$m$ incrementos cuestan a lo sumo $4m=O(m)$ pasos**. Es más, como $\Phi_m=2\cdot\mathrm{popcount}(m)$, el total es **exactamente**
$$\sum c_i = 4m-2\,\mathrm{popcount}(m).$$

**Qué deuda mide $\Phi$.** Cada 1 de la cinta es trabajo pendiente: algún incremento futuro tendrá que pasar por encima de él dos veces, una para convertirlo en 0 y otra al volver. El potencial guarda 2 unidades por cada 1 para pagar esos dos pasos. La versión del método de contabilidad es la misma: cobrar 4 por incremento, gastar 2 en escribir el 1 y volver sobre él, y dejar 2 de crédito pegados al 1 nuevo.

## Respuesta al ejercicio 7 de la C1

- Peor caso de un incremento sobre un número de $b$ bits: $2b+2=\Theta(b)$ pasos; sobre los primeros $m$, $\Theta(\log m)$.
- $m$ incrementos desde 0: exactamente $4m-2\,\mathrm{popcount}(m)$ pasos, que es $\Theta(m)$.

## Código de validación

Un simulador de máquinas de Turing de una cinta, y la máquina de arriba.

> Código: [ejercicio-04.py](ejercicio-04.py), parte 1.

Comprobamos todo junto: que la máquina incrementa, que vuelve al LSB, que cada paso cuesta $2t+2$, que el amortizado es 4 y que el total es $4m-2\,\mathrm{popcount}(m)$.

> Código: [ejercicio-04.py](ejercicio-04.py), parte 2.

```text
m =    10: total =     36  4m - 2 popcount(m) =     36  peor incremento =  8 = 2*floor(log2 m) + 2
m =   100: total =    394  4m - 2 popcount(m) =    394  peor incremento = 14 = 2*floor(log2 m) + 2
m =  1000: total =   3988  4m - 2 popcount(m) =   3988  peor incremento = 20 = 2*floor(log2 m) + 2
m =  5000: total =  19990  4m - 2 popcount(m) =  19990  peor incremento = 26 = 2*floor(log2 m) + 2
```

La tabla del costo real contra el amortizado en los primeros incrementos (la misma imagen que la Figura 1 de la C4: picos de costo real, amortizado plano):

> Código: [ejercicio-04.py](ejercicio-04.py), parte 3.

```text
  i  binario  real  Phi  amortizado
  1        1     2    2           4
  2       10     4    2           4
  3       11     2    4           4
  4      100     6    2           4
  5      101     2    4           4
  6      110     4    4           4
  7      111     2    6           4
  8     1000     8    2           4
  9     1001     2    4           4
 10     1010     4    4           4
 11     1011     2    6           4
 12     1100     6    4           4
 13     1101     2    6           4
 14     1110     4    6           4
 15     1111     2    8           4
 16    10000    10    2           4
```

## Resumen

- Un incremento con $t$ unos finales cuesta $2t+2$ pasos; el peor es $\Theta(\log m)$.
- $\Phi=2\cdot\#\text{unos}$: $\Phi_0=0$, $\Phi\ge0$, amortizado exactamente 4.
- Total: $4m-2\,\mathrm{popcount}(m)\le4m=O(m)$.
