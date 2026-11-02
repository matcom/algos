# Ejercicio 4 — El contador binario en una máquina de Turing

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1.
> Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total,
> aunque uno solo pueda costar $\Theta(\log m)$. Es la pregunta que la conferencia 1
> dejó abierta.


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

En un incremento se apagan $t_i$ unos finales, se enciende el siguiente bit y el
cabezal vuelve esas $t_i$ posiciones al LSB. Con el modelo de la simulación, el costo es
$$c_i=2t_i+1,$$
donde $t_i$ es la cantidad de unos finales antes del incremento $i$. Basta acotar
$\sum_i(t_i+1)$.

## 3. Análisis amortizado con potencial (C4)

### Guía para redactar el argumento (pendiente)

La demostración de potencial debes escribirla tú. Usa el costo real de la simulación,
$c_i=2t_i+1$, y prueba un potencial $\Phi=c\cdot(\text{número de unos})$.

1. ¿Cuánto cambia el número de unos cuando se apagan $t_i$ bits y se enciende uno?
2. Sustituye ese cambio en $\hat c_i=c_i+\Delta\Phi_i$. ¿Qué valor de la constante
   cancela el término que depende de $t_i$?
3. ¿Por qué el potencial inicial es cero y el final no es negativo? Escribe el
   telescopaje que da el costo total.

No entregues esta sección hasta completar esos pasos con tu propia redacción.

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
 3 |       ●  (i=4)        ●  (i=12: 3 cambios)
 2 |   ●       ●       ●       ●       ... (i=2,6,10,14)
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
amortizado por incremento. La demostración debe usar un potencial proporcional al
número de unos y telescopar los costos amortizados, como indica la guía de §3. Un
incremento aislado cuesta
hasta $\Theta(\log m)$, pero esos son raros — exactamente el fenómeno de la conferencia
4: *el costo amortizado es una garantía sobre la secuencia, no sobre la peor operación*.
