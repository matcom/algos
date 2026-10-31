# Ejercicio 11 ★★ — La mochila $O(nW)$ medida en bits (C1)

> La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división?

## El algoritmo

Entrada: $n$ objetos con pesos $w_i$ y valores $v_i$ (enteros positivos) y una capacidad $W$. Salida: el máximo valor de un subconjunto con peso total $\le W$.

$$\text{mejor}[c]=\max\big(\text{mejor}[c],\ \text{mejor}[c-w_i]+v_i\big)\quad\text{para cada objeto } i \text{ y cada } c \text{ de } W \text{ a } w_i .$$

La tabla tiene $W+1$ casillas y se recorre una vez por objeto: $\Theta(nW)$ operaciones.

La función `mochila(pesos, valores, W)` implementa esa recurrencia con una sola tabla `mejor` de $W+1$ casillas, recorrida de $W$ hacia abajo para que cada objeto se use a lo sumo una vez. El parámetro `cuenta` permite contar cuántas veces se ejecuta el paso interno.

> Código: [ejercicio-11.py](ejercicio-11.py), parte 1.

## Tamaño de la entrada en bits

Un entero $x\ge1$ ocupa $\lfloor\log_2 x\rfloor+1$ bits. El tamaño de la entrada es
$$b=\sum_{i=1}^{n}\big(\text{bits}(w_i)+\text{bits}(v_i)\big)+\text{bits}(W)\ \ge\ n+\log_2 W .$$

La capacidad $W$ ocupa solo $\approx\log_2 W$ bits, pero el algoritmo hace $\approx nW = n\cdot 2^{\log_2 W}$ operaciones.

## ¿Es polinomial? No

**Familia que lo muestra:** un solo objeto ($n=1$) con $w_1=v_1=1$ y capacidad $W=2^k-1$ ($k$ bits). Entonces
$$b = 1+1+k = k+2,\qquad T = W = 2^k-1 = 2^{\,b-2}-1 .$$
El tiempo es **exponencial en el tamaño de la entrada**. En general, $T=\Theta(nW)$ y $W$ puede ser tan grande como $2^{b-n}$ (con $b-n$ bits en $W$), así que ningún polinomio en $b$ acota a $T$.

Agregar **un bit** a $W$ (multiplicarla por 2) **duplica** el tiempo. Un algoritmo polinomial en $b$ solo podría multiplicar el tiempo por un factor que tiende a 1.

**Lo que sí es:** polinomial en $n$ y en el **valor** $W$. Eso se llama **pseudopolinomial**. Sería polinomial si los números se escribieran en unario (entonces el tamaño sería $\ge W$), o si se garantiza que $W\le p(n)$ para un polinomio $p$ (por ejemplo, pesos acotados por $n^2$).

## Parecido con la primalidad por división

| | primalidad por división | mochila $O(nW)$ |
|---|---|---|
| costo "a primera vista" | $\sqrt N$ divisiones: parece rápido | $nW$: parece polinomial |
| tamaño de la entrada | $b=\lfloor\log_2 N\rfloor+1$ | $b\ge n+\log_2 W$ |
| costo en función de $b$ | $\sqrt{2^b}=2^{b/2}$ | hasta $n\cdot2^{b-n}$ |
| por qué | recorre un rango definido por el **valor** de un número | recorre un rango definido por el **valor** de un número |
| clasificación | exponencial en bits | exponencial en bits (pseudopolinomial) |

Los dos algoritmos **recorren todos los valores hasta un número de la entrada** (los divisores hasta $\sqrt N$, las capacidades hasta $W$). Un número de $k$ bits puede valer $2^k$. Por eso los dos parecen polinomiales cuando se escriben en función del número, y son exponenciales en función del tamaño.

**Diferencia importante:** para la primalidad existen algoritmos polinomiales en $b$ (Miller-Rabin, aleatorio; AKS 2002, determinista). Para la mochila no se conoce ninguno: es NP-difícil (Tema 3), y uno polinomial implicaría P = NP. En la mochila, lo pseudopolinomial es lo mejor que se sabe hacer en general.

## Código de validación

Correctitud contra fuerza bruta (todos los subconjuntos):

> Código: [ejercicio-11.py](ejercicio-11.py), parte 2.

```text
500 instancias: la programación dinámica coincide con la fuerza bruta
```

**Un bit más en $W$ duplica el trabajo** (con los mismos 20 objetos):

> Código: [ejercicio-11.py](ejercicio-11.py), parte 3.

```text
 bits de W  bits entrada  operaciones  cociente
        10           245       20,360          
        11           246       40,840      2.01
        12           247       81,800      2.00
        13           248      163,720      2.00
        14           249      327,560      2.00
        15           250      655,240      2.00
        16           251    1,310,600      2.00
        17           252    2,621,320      2.00
        18           253    5,242,760      2.00
```

La entrada crece **un bit** por fila y las operaciones se **duplican**: exponencial en el tamaño.

**La tabla de la C1 §8, para la mochila** ($n=100$ objetos, $10^9$ operaciones por segundo):

> Código: [ejercicio-11.py](ejercicio-11.py), parte 4.

```text
 bits de W  operaciones               tiempo
        16     6.55e+06     0.00655 segundos
        32     4.29e+11          0.119 horas
        48     2.81e+16             326 días
        64     1.84e+21        5.85e+04 años
       128      3.4e+40        1.08e+24 años
```

Con capacidades de 64 bits, que caben en una palabra de máquina, la tabla ya no se puede ni recorrer.

## Resumen

- Tamaño: $b\ge n+\log_2 W$. Tiempo: $\Theta(nW)$, que puede ser $n\cdot2^{b-n}$.
- **No es polinomial**: es exponencial en los bits de $W$ (con $n=1$, $T=2^{b-2}-1$). Es **pseudopolinomial**: polinomial en el valor de $W$.
- **Como la primalidad por división:** recorre todos los valores hasta un número de la entrada, y el valor es exponencial en su cantidad de bits. Diferencia: la primalidad tiene algoritmos polinomiales en bits; la mochila es NP-difícil.
