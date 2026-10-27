# Ejercicio 11 — La mochila entera y el tamaño en bits

> **Enunciado.** La mochila entera se resuelve con programación dinámica en $O(nC)$,
> donde $C$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la
> entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese
> algoritmo? ¿En qué se parece a la primalidad por división?

---

## 1. El problema y el algoritmo

**Mochila 0/1.** Hay $n$ objetos; el objeto $i$ pesa $w_i\in\mathbb Z_{>0}$ y vale
$v_i\in\mathbb Z_{>0}$. Dada una capacidad $C\in\mathbb Z_{>0}$, elegir un subconjunto
$S$ con $\sum_{i\in S} w_i \le C$ que maximice $\sum_{i\in S} v_i$.

**Programación dinámica por capacidad.** $T[i][c]$ = valor óptimo usando los primeros
$i$ objetos con capacidad $c$:
$$T[i][c] = \max\big(\,T[i-1][c],\ \ v_i + T[i-1][c-w_i]\ \text{si } w_i\le c\,\big).$$

```python
def mochila(pesos, valores, C):
    n = len(pesos)
    T = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = pesos[i - 1], valores[i - 1]
        for c in range(C + 1):
            T[i][c] = T[i - 1][c]
            if w <= c and v + T[i - 1][c - w] > T[i][c]:
                T[i][c] = v + T[i - 1][c - w]
    return T[n][C]

if __name__ == "__main__":
    print(mochila([2, 3, 4, 5], [3, 4, 5, 6], 5))   # óptimo: objetos de peso 2 y 3
```

```
7
```

La tabla tiene $(n+1)(C+1)$ celdas y cada una se llena en $O(1)$: **costo $\Theta(nC)$**.

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
$w_i,v_i$) y la capacidad $C$. El tamaño en bits es
$$
b \;=\; \underbrace{\sum_{i}(\lfloor\log_2 w_i\rfloor + \lfloor\log_2 v_i\rfloor)}_{\text{los pesos y valores}}
\;+\; \underbrace{\lfloor\log_2 C\rfloor + 1}_{\text{la capacidad}}
\;+\;\Theta(n).
$$

Lo decisivo es el último sumando que depende de $C$: **$C$ aporta solo
$\log_2 C$ bits a la entrada**, no $C$. Y el costo $\Theta(nC)$ se escribe en función
de $b$ como
$$
\Theta(nC) = \Theta\!\big(n\cdot 2^{\log_2 C}\big) = \Theta\!\big(n\cdot 2^{\,b_C}\big),
\qquad b_C := \log_2 C .
$$

**El costo es exponencial en el número de bits de $C$.** Igual que la primalidad por
división hacía $\sqrt n = 2^{b/2}$ divisiones (C1, §8), aquí el número de pasos crece
como $2^{b_C}$.

---

## 3. ¿Es polinomial? No: es *pseudopolinomial*

**Definición.** Un algoritmo es **polinomial** si su costo está acotado por un polinomio
en el **tamaño en bits** de la entrada. Es **pseudopolinomial** si es polinomial en el
tamaño *y en el valor numérico* de la entrada —polinomial en $n$ y en $C$, pero no en
$\log C$.

El DP de la mochila es $\Theta(nC)$, que es polinomial en $C$ pero **exponencial en
$\log C$**, luego **no es polinomial**: es pseudopolinomial. La demostración es la misma
cuenta de la sección 8 de C1, instanciada con $C$ en el papel de $n$.

### El experimento que lo hace visible

Duplicar $C$ (añadir **un bit** a la entrada) **duplica** el trabajo:

```python
if __name__ == "__main__":
    import time
    pesos = [1] * 20
    valores = list(range(1, 21))
    print(f"{'bits de C':>10} {'C':>12} {'celdas ~ n*C':>14} {'segundos':>10}")
    for b in range(14, 21):
        C = 2 ** b
        t = time.perf_counter()
        mochila(pesos, valores, C)
        dt = time.perf_counter() - t
        print(f"{b:>10} {C:>12,} {len(pesos) * C:>14,} {dt:>10.3f}")
```

```
 bits de C            C   celdas ~ n*C   segundos
        14       16,384        327,680      0.030
        15       32,768        655,360      0.061
        16       65,536      1,310,720      0.121
        17      131,072      2,621,440      0.244
        18      262,144      5,242,880      0.488
        19      524,288     10,485,760      0.983
        20    1,048,576     20,971,520      1.971
```

Cada fila añade **un bit** a $C$ y el tiempo **se duplica**: la firma inconfundible de
un algoritmo exponencial en el tamaño de la entrada. *(Los tiempos absolutos dependen de
la máquina; lo que importa, y es reproducible, es que la razón entre filas consecutivas
es ≈ 2.)*

---

## 4. En qué se parece a la primalidad por división

| | primalidad por división (C1 §1,§8) | mochila por DP |
|---|---|---|
| entrada | un entero $n$ | $n$ objetos y una capacidad $C$ |
| tamaño en bits | $b=\log_2 n$ | $\approx \log_2 C$ (más $\Theta(n)$ por los objetos) |
| "parece" | un solo ciclo hasta $\sqrt n$ | dos ciclos, tabla $n\times C$ |
| costo real | $\sqrt n = 2^{b/2}$ | $nC = n\,2^{\,\log_2 C}$ |
| en bits | **exponencial** | **exponencial** en $\log C$ |
| veredicto | no polinomial | no polinomial (pseudopolinomial) |

Las dos comparten el mismo espejismo: **el bucle recorre valores, pero la entrada se
mide en bits**, y el valor es exponencial en su número de bits. En primalidad el bucle
va hasta $\sqrt n$; en la mochila, hasta $C$. Añadir un bit a la entrada (duplicar $n$ o
$C$) duplica el trabajo.

**Matiz importante** (la diferencia, no solo el parecido): para primalidad *sí* existe
un algoritmo polinomial de verdad —AKS, 2002, polinomial en $\log n$— así que el
espejismo era evitable. Para la mochila, en cambio, **no se conoce** ningún algoritmo
polinomial en $\log C$, y hay razones para creer que no existe: la mochila es
NP-completa (Tema posterior), y un algoritmo polinomial en el tamaño en bits daría
$\mathrm P = \mathrm{NP}$. El DP $\Theta(nC)$ es lo mejor "fácil" que hay, y es
pseudopolinomial precisamente porque el problema es duro.

---

## 5. Resumen

- El DP de la mochila cuesta $\Theta(nC)$. Midiendo la entrada en bits (C1, §8),
  $C$ aporta $\log_2 C$ bits, de modo que $nC = n\,2^{\log_2 C}$ es **exponencial** en
  el tamaño de la entrada: **no es polinomial**, es *pseudopolinomial*.
- Es el mismo espejismo que la primalidad por división: un bucle que recorre *valores*
  en un problema cuya entrada se mide en *bits*. Añadir un bit duplica el trabajo.
- La diferencia: la primalidad sí admite un algoritmo polinomial real (AKS); para la
  mochila no se conoce ninguno (es NP-completa), así que su pseudopolinomialidad no es
  un descuido de diseño sino un reflejo de la dureza del problema.
