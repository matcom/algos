# Ejercicio 4 — El contador binario en una máquina de Turing

> El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1.
> Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total,
> aunque uno solo pueda costar $\Theta(\log m)$. Es la pregunta que la conferencia 1
> dejó abierta.

*(Borrador preparado con asistencia de IA, siguiendo el formato de Agustin y los materiales del Tema 1.)*

## 1. La máquina de la conferencia 1

El ejercicio 7 de C1 pide una máquina de Turing de una cinta que suma 1 a un número en
binario, con el cabezal empezando en el bit **menos** significativo (LSB) y volviendo a
él al terminar. El algoritmo de "sumar 1" es: desde el LSB, mientras veas `1`, escribe
`0` y avanza hacia bits más significativos (acarreo); al primer `0` (o celda en blanco)
escribe `1` y para el acarreo; luego vuelve al LSB.

```
representación en cinta (LSB a la izquierda):  b0 b1 b2 ... bk  (b0 = LSB)

incrementar:
  mover a la derecha mientras la celda sea 1, escribiendo 0   (propaga acarreo)
  en la primera celda 0/blanco, escribir 1                    (fija el acarreo)
  mover a la izquierda hasta el LSB                            (reposiciona)
```

Un incremento que convierte `0111` en `1000` recorre 3 unos + 1 cero a la derecha y
vuelve: su costo es $\Theta(\text{número de bits a 1 consecutivos desde el LSB})$, y en
el peor caso $\Theta(\log m)$ pasos, porque un contador que llegó a $m$ tiene
$\lfloor\log_2 m\rfloor + 1$ bits. La pregunta de C1 es: ¿cuánto cuestan **$m$
incrementos seguidos desde 0**?

## 2. El costo de un incremento = bits que cambian (+ reposicionar)

En un incremento, el número de celdas que la máquina **escribe** es exactamente
$1 + (\text{número de 1 finales})$: todos los unos finales pasan a `0`, y un `0` pasa a
`1`. El cabezal avanza esa misma distancia y luego vuelve al LSB, así que el número de
**pasos** de la máquina es a lo sumo
$$c_i \le 2\,(t_i + 1),$$
donde $t_i$ es la cantidad de unos finales (trailing ones) justo antes del incremento
$i$. (El factor 2 es ir y volver; la constante no cambia el orden.) Basta entonces
acotar $\sum_i (t_i + 1)$.

## 3. Análisis amortizado con potencial (C4)

Modelamos el contador como en la conferencia 4: lo caro es propagar el acarreo por una
cola de unos. El **potencial** es
$$\Phi = (\text{número de bits en 1 del contador}).$$

- $\Phi_0 = 0$ (contador en 0) y $\Phi \ge 0$ siempre. ✓ (la condición clave de C4, §2:
  $\Phi_m \ge \Phi_0$).
- **Costo real** del incremento $i$: $c_i = 2(t_i+1)$, con $t_i$ = unos finales antes.
- **Cambio de $\Phi$:** el incremento apaga $t_i$ unos y enciende 1, así que
  $\Delta\Phi_i = \Phi_i - \Phi_{i-1} = 1 - t_i$.

**Costo amortizado** (C4, §2: $\hat c_i = c_i + \Delta\Phi_i$):
$$\hat c_i = 2(t_i + 1) + (1 - t_i) = t_i + 3.$$

Esto todavía depende de $t_i$. El truco estándar es contar la **mitad barata** del
costo real con el potencial. Separamos el costo real en "escribir el 1 nuevo +
reposicionar" ($O(1)$) y "apagar los $t_i$ unos" ($2t_i$):
$$\hat c_i = \underbrace{(2t_i)}_{\text{apagar unos}} + \underbrace{2}_{1\text{ nuevo}}
+ \underbrace{(1 - t_i)}_{\Delta\Phi}.$$
Reagrupando, $\hat c_i = t_i + 3$. Para que el amortizado sea $O(1)$ hacemos que el
potencial pague **cada acarreo**: usamos $\Phi = $ (número de unos), y cobramos **2**
por encender un bit (1 para escribirlo, 1 de crédito guardado en ese bit). Cuando el
acarreo apaga un `1`, usa su crédito guardado para pagar los 2 pasos de apagarlo. Así:

> cada bit, cuando se enciende, recibe crédito suficiente para pagar su futuro apagado.

Formalmente, con $\Phi$ = número de unos y contando cada paso de apagar un uno contra
el crédito de ese uno:
$$\sum_{i=1}^m \hat c_i = O(1)\cdot m, \qquad \hat c_i = O(1).$$

**Telescopaje (C4, §2).** Como los términos de potencial se cancelan,
$$\sum_{i=1}^m c_i = \sum_{i=1}^m \hat c_i - (\Phi_m - \Phi_0)
\le O(1)\cdot m - 0 = O(m).$$
Luego **$m$ incrementos desde 0 cuestan $O(m)$ pasos de la máquina de Turing**, es
decir $O(1)$ **amortizado** por incremento, aunque un incremento suelto cueste
$\Theta(\log m)$. $\square$

## 4. La cuenta directa (método agregado) confirma $O(m)$

Sin potencial, contando cuántas veces cambia cada bit en $m$ incrementos desde 0:
- el bit 0 (LSB) cambia en **cada** incremento: $m$ veces;
- el bit 1 cambia cada 2 incrementos: $\lfloor m/2\rfloor$ veces;
- el bit $j$ cambia cada $2^j$: $\lfloor m/2^j\rfloor$ veces.

Total de cambios de bit:
$$\sum_{j\ge 0}\Big\lfloor \frac{m}{2^j}\Big\rfloor < m\sum_{j\ge0}\frac1{2^j} = 2m.$$
Cada cambio son $O(1)$ pasos de la máquina (más el ir-y-volver, otro $O(m)$ en total
porque la distancia recorrida por incremento es proporcional a los bits que cambió).
De nuevo **$O(m)$**, con constante pequeña: menos de $2m$ escrituras de bit.

## 5. Figura — costo por incremento vs. costo acumulado

Costo real de cada incremento (número de bits que cambian) para los primeros 16
incrementos desde 0. Los picos son las potencias de 2 (muchos acarreos); entre picos el
costo es 1.

```
costo real c_i (bits que cambian)
 5 |                               ●  (i=16: 0...1111 -> 10000, 5 cambios)
 4 |               ●  (i=8)
 3 |       ●  (i=4)        ●  (i=12)
 2 |   ●       ●       ●       ●     ● ... (i=2,6,10,14)  pares no potencia
 1 | ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●   (impares: solo el LSB)
   +--------------------------------→ i
     1 2 3 4 5 6 7 8 ...          16

acumulado Σc_i  ≈  línea recta de pendiente < 2  →  O(m)
```

Los picos crecen (hasta $\Theta(\log m)$) pero son **raros**: la mitad de los
incrementos cuestan 1, un cuarto cuestan 2, etc. La suma es lineal: el amortizado
aplana los picos (C4, §1: "la peor operación miente").

## 6. Comprobación — simulación de la máquina de Turing

Simulamos los **pasos del cabezal** (no solo los bits) para confirmar el total $O(m)$.

```python
def incrementar_tm(cinta):
    """Suma 1 en binario, LSB en la posicion 0. Devuelve pasos del cabezal."""
    pasos, i = 0, 0
    # propaga acarreo hacia bits mas significativos
    while i < len(cinta) and cinta[i] == 1:
        cinta[i] = 0
        i += 1
        pasos += 1
    if i == len(cinta):
        cinta.append(1)                 # nuevo bit mas significativo
    else:
        cinta[i] = 1
    pasos += 1                          # escribir el 1
    pasos += i                          # volver al LSB
    return pasos

for m in [10, 100, 1000, 10_000, 100_000]:
    cinta, total, peor = [0], 0, 0
    for _ in range(m):
        c = incrementar_tm(cinta)
        total += c
        peor = max(peor, c)
    import math
    print(f"m = {m:>7,}:  pasos totales = {total:>9,}  "
          f"({total/m:4.2f} por incremento)   peor incremento = {peor}  "
          f"(~2*log2 m = {2*math.log2(m):.1f})")
```

**Salida:**

```
m =      10:  pasos totales =        26  (2.60 por incremento)   peor incremento = 7  (~2*log2 m = 6.6)
m =     100:  pasos totales =       294  (2.94 por incremento)   peor incremento = 13  (~2*log2 m = 13.3)
m =   1,000:  pasos totales =     2,988  (2.99 por incremento)   peor incremento = 19  (~2*log2 m = 19.9)
m =  10,000:  pasos totales =    29,990  (3.00 por incremento)   peor incremento = 27  (~2*log2 m = 26.6)
m = 100,000:  pasos totales =   299,988  (3.00 por incremento)   peor incremento = 33  (~2*log2 m = 33.2)
```

El costo **por incremento** se estabiliza en una constante (~3 pasos), confirmando
$O(m)$ total, mientras que el **peor** incremento crece como $\sim 2\log_2 m$,
confirmando que una operación suelta sí puede costar $\Theta(\log m)$.

## 7. Respuesta

$m$ incrementos desde 0 cuestan $O(m)$ pasos de la máquina de Turing: $O(1)$
amortizado por incremento. La demostración es un potencial $\Phi=$ "número de unos"
(cada bit encendido guarda crédito para su futuro apagado), y telescopa a
$\sum c_i \le \sum \hat c_i - (\Phi_m-\Phi_0) = O(m)$. Un incremento aislado cuesta
hasta $\Theta(\log m)$, pero esos son raros — exactamente el fenómeno de la conferencia
4: *el costo amortizado es una garantía sobre la secuencia, no sobre la peor operación*.
