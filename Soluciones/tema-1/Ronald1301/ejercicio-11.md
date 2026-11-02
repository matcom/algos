# Ejercicio 11 — La mochila entera y el tamaño en bits

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> **Enunciado.** La mochila entera se resuelve con programación dinámica en $O(nW)$,
> donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la
> entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese
> algoritmo? ¿En qué se parece a la primalidad por división?

---

## 1. El problema y el algoritmo

**Mochila 0/1.** Hay $n$ objetos; el objeto $i$ pesa $w_i\in\mathbb Z_{>0}$ y vale
$v_i\in\mathbb Z_{>0}$. Dada una capacidad $W\in\mathbb Z_{>0}$, elegir un subconjunto
$S$ con $\sum_{i\in S} w_i \le W$ que maximice $\sum_{i\in S} v_i$.

**Programación dinámica por capacidad.** $T[i][c]$ = valor óptimo usando los primeros
$i$ objetos con capacidad $c$:
$$T[i][c] = \max\big(\,T[i-1][c],\ \ v_i + T[i-1][c-w_i]\ \text{si } w_i\le c\,\big).$$

```python
def mochila(pesos, valores, W):
    n = len(pesos)
    T = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = pesos[i - 1], valores[i - 1]
        for c in range(W + 1):
            T[i][c] = T[i - 1][c]
            if w <= c and v + T[i - 1][c - w] > T[i][c]:
                T[i][c] = v + T[i - 1][c - w]
    return T[n][W]

if __name__ == "__main__":
    print(mochila([2, 3, 4, 5], [3, 4, 5, 6], 5))   # óptimo: objetos de peso 2 y 3
```

```
7
```

La tabla reserva exactamente $(n+1)(W+1)$ celdas. El código calcula $n(W+1)$ estados
de la recurrencia (una fila por objeto y una columna por capacidad de $0$ a $W$); la fila
base ocupa otras $W+1$ celdas. El tiempo es $\Theta(nW)$.

```
         c=0  c=1  c=2  c=3  c=4  c=5
 i=0      0    0    0    0    0    0
 i=1(2,3) 0    0    3    3    3    3
 i=2(3,4) 0    0    3    4    4    7     ← T[2][5]=v2+T[1][2]=4+3=7
 i=3(4,5) 0    0    3    4    5    7
 i=4(5,6) 0    0    3    4    5    7     ← respuesta = 7
```

Parece un algoritmo "rápido": dos ciclos anidados, nada exponencial a la vista. El
engaño es exactamente el de la primalidad (C1, §1 y §8): **un solo ciclo que recorre
hasta un número puede ser exponencial en el tamaño de la entrada.**

---

## 2. El tamaño de la entrada se mide en bits (C1, §8)

> C1, §8: "$n$ es el valor de la entrada, no su tamaño. Para escribir $n$ en binario
> hacen falta $b=\lfloor\log_2 n\rfloor+1$ bits, y un algoritmo se mide en función del
> tamaño de la entrada, no de su valor."

¿Cuántos bits ocupa una instancia de mochila? Hay que escribir $2n$ enteros (los
$w_i,v_i$) y la capacidad $W$. El tamaño en bits es
$$
b \;=\; \underbrace{\sum_{i}(\lfloor\log_2 w_i\rfloor + \lfloor\log_2 v_i\rfloor)}_{\text{los pesos y valores}}
\;+\; \underbrace{\lfloor\log_2 W\rfloor + 1}_{\text{la capacidad}}
\;+\;\Theta(n).
$$

Lo decisivo es el último sumando que depende de $W$: **$W$ aporta solo
$\log_2 W$ bits a la entrada**, no $W$. Y el costo $\Theta(nW)$ se escribe en función
de $b$ como
$$
\Theta(nW) = \Theta\!\big(n\cdot 2^{b_W}\big),
\qquad b_W := \lfloor\log_2 W\rfloor+1 .
$$

**El costo es exponencial en el número de bits de $W$.** Igual que la primalidad por
división hacía $\sqrt n = 2^{b/2}$ divisiones (C1, §8), aquí el número de pasos crece
como $2^{b_W}$.

---

## 3. ¿Es polinomial? No: es *pseudopolinomial*

**Definición.** Un algoritmo es **polinomial** si su costo está acotado por un polinomio
en el **tamaño en bits** de la entrada. Es **pseudopolinomial** si es polinomial en el
tamaño *y en el valor numérico* de la entrada —polinomial en $n$ y en $W$, pero no en
$\log W$.

El DP de la mochila es $\Theta(nW)$, que es polinomial en $W$ pero **exponencial en
$\log W$**, luego **no es polinomial**: es pseudopolinomial. La demostración es la misma
cuenta de la sección 8 de C1, instanciada con $W$ en el papel de $n$.

### El experimento que lo hace visible

Duplicar $W$ (añadir **un bit** a la entrada) **duplica** el trabajo. Cada tiempo de la
tabla es la mediana de tres ejecuciones del mismo fragmento:

```python
if __name__ == "__main__":
    import time
    from statistics import median
    pesos = [1] * 20
    valores = list(range(1, 21))
    print(f"{'bits de W':>10} {'W':>12} {'estados DP n(W+1)':>20} {'segundos':>10}")
    for exponente in range(14, 21):
        W = 2 ** exponente
        bits = W.bit_length()
        muestras = []
        for _ in range(3):
            t = time.perf_counter()
            mochila(pesos, valores, W)
            muestras.append(time.perf_counter() - t)
        dt = median(muestras)
        print(f"{bits:>10} {W:>12,} {len(pesos) * (W + 1):>20,} {dt:>10.3f}")
```

```
 bits de W            W    estados DP n(W+1)   segundos
        15       16,384               327,700      0.098
        16       32,768               655,380      0.198
        17       65,536             1,310,740      0.412
        18      131,072             2,621,460      0.890
        19      262,144             5,242,900      1.812
        20      524,288            10,485,780      3.612
        21    1,048,576            20,971,540      7.345
```

Cada fila añade **un bit** a $W$ y el tiempo **se duplica**: la firma inconfundible de
un algoritmo exponencial en el tamaño de la entrada. *(Los tiempos absolutos dependen de
la máquina; estos tiempos se midieron al ejecutar el fragmento en este entorno. Lo que
importa es que la razón entre filas consecutivas es aproximadamente 2.)*

---

## 4. En qué se parece a la primalidad por división

| | primalidad por división (C1 §1,§8) | mochila por DP |
|---|---|---|
| entrada | un entero $n$ | $n$ objetos y una capacidad $W$ |
| tamaño en bits | $b=\log_2 n$ | $\approx \log_2 W$ (más $\Theta(n)$ por los objetos) |
| "parece" | un solo ciclo hasta $\sqrt n$ | dos ciclos, tabla $n\times W$ |
| costo real | $\sqrt n = 2^{b/2}$ | $nW = n\,2^{\Theta(b_W)}$ |
| en bits | **exponencial** | **exponencial** en $\log W$ |
| veredicto | no polinomial | no polinomial (pseudopolinomial) |

Las dos comparten el mismo espejismo: **el bucle recorre valores, pero la entrada se
mide en bits**, y el valor es exponencial en su número de bits. En primalidad el bucle
va hasta $\sqrt n$; en la mochila, hasta $W$. Añadir un bit a la entrada (duplicar $n$ o
$W$) duplica el trabajo.

**Matiz importante** (la diferencia, no solo el parecido): para primalidad *sí* existe
un algoritmo polinomial de verdad —AKS, 2002, polinomial en $\log n$— así que el
espejismo era evitable. Para la mochila, en cambio, **no se conoce** ningún algoritmo
polinomial en $\log W$, y hay razones para creer que no existe: la mochila es
NP-completa (Tema posterior), y un algoritmo polinomial en el tamaño en bits daría
$\mathrm P = \mathrm{NP}$. El DP $\Theta(nW)$ es lo mejor "fácil" que hay, y es
pseudopolinomial precisamente porque el problema es duro.

---

## 5. Resumen

- El DP de la mochila cuesta $\Theta(nW)$. Midiendo la entrada en bits (C1, §8),
  $W$ aporta $b_W=\lfloor\log_2 W\rfloor+1$ bits, de modo que $nW$ es **exponencial** en
  el tamaño de la entrada: **no es polinomial**, es *pseudopolinomial*.
- Es el mismo espejismo que la primalidad por división: un bucle que recorre *valores*
  en un problema cuya entrada se mide en *bits*. Añadir un bit duplica el trabajo.
- La diferencia: la primalidad sí admite un algoritmo polinomial real (AKS); para la
  mochila no se conoce ninguno (es NP-completa), así que su pseudopolinomialidad no es
  un descuido de diseño sino un reflejo de la dureza del problema.
