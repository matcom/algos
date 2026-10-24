# Ejercicio 2: búsqueda binaria, invariante, potencial y cota de información

> ★ Da el invariante y el potencial de la búsqueda binaria, y la cota de información
> que la hace óptima. (C3, C5)

**Código:** [`ejercicio-02.py`](ejercicio-02.py). Prueba de forma exhaustiva todos los
$n \le 300$ con el invariante y el potencial vigilados en cada iteración, compara el
peor caso con la cota y prueba dos variantes con errores plantados.

## Problema y modelo

**Entrada:** un arreglo ordenado $A[0..n-1]$ con $A[0] < \dots < A[n-1]$ y un valor
$x$. **Salida:** la posición $i$ si $A[i] = x$. Si $x$ no está, el **hueco** $g \in \lbrace 0, \dots, n \rbrace$ donde cae, es decir, la cantidad de elementos menores que $x$.
**Modelo:** comparaciones de tres vías ($<$, $=$, $>$), cada una de costo 1, como en la
conferencia 5.

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)
```

## Correctitud parcial: el invariante

Al inicio de cada iteración se cumplen las dos partes de este invariante:

$$
\begin{aligned}
I_1 &:\; 0 \le lo \le hi \le n,\\
I_2 &:\; A[j] < x \text{ para todo } j < lo,\quad\text{y}\quad A[j] > x \text{ para todo } j \ge hi.
\end{aligned}
$$

En palabras: todo lo que está a la izquierda de `lo` es menor que $x$, todo lo que está
desde `hi` en adelante es mayor, y solo falta mirar la ventana `A[lo:hi]`.

```
        lo                 hi
  ┌─────┬──────────────────┬─────┐
  │ < x │   sin descartar  │ > x │
  └─────┴──────────────────┴─────┘
```

**Inicialización.** Con $lo = 0$ y $hi = n$ no hay ningún $j < 0$ ni ningún $j \ge n$,
así que $I_2$ se cumple sin condiciones. $I_1$ es inmediato.

**Mantenimiento.** Como $lo < hi$, se cumple $lo \le m < hi$.
- Si $x = A[m]$, se devuelve $m$ y la respuesta es correcta.
- Si $x < A[m]$, como el arreglo está ordenado, $x < A[m] \le A[j]$ para todo
  $j \ge m$. Al asignar `hi = m` se conserva $I_2$, y como $lo \le m$ también se
  conserva $I_1$.
- Si $x > A[m]$, por la misma razón $A[j] \le A[m] < x$ para todo $j \le m$. Al asignar
  `lo = m + 1` se conserva $I_2$, y como $m + 1 \le hi$ también se conserva $I_1$.

**Conclusión.** El ciclo termina sin encontrar $x$ solo cuando $lo = hi$. En ese
momento $I_2$ dice que exactamente $lo$ elementos son menores que $x$ y que el resto
son mayores. Entonces $x$ no está y cae en el hueco $lo$, que es lo que se devuelve.

## Terminación y costo: el potencial

$$\Phi = hi - lo \quad(\text{el tamaño de la ventana}).$$

- Por $I_1$, $\Phi \ge 0$ siempre, y el ciclo corre mientras $\Phi \ge 1$.
- **Baja al menos a la mitad:**
  - Con `hi = m`, la ventana nueva mide $m - lo = \lfloor \Phi/2 \rfloor$.
  - Con `lo = m + 1`, mide $hi - m - 1 = \lceil \Phi/2 \rceil - 1 \le \lfloor \Phi/2 \rfloor$.

Como $\Phi$ es un entero que se reduce estrictamente en cada paso, el ciclo termina.
Además, después de $t$ iteraciones $\Phi \le \lfloor n / 2^t \rfloor$, y el ciclo sigue
mientras $\Phi \ge 1$. Por eso hay como máximo
$\lfloor \log_2 n \rfloor + 1 = \lceil \log_2(n+1) \rceil$ iteraciones, y cada una hace
una sola comparación de tres vías.

$$\boxed{\text{comparaciones en el peor caso} \;\le\; \lceil \log_2 (n+1) \rceil}$$

## Cota mínima: el argumento de información

Esta es la cota de la sección 3 de la conferencia 5 (lema 4). Si $x$ no está en el arreglo, puede
caer en $n + 1$ huecos, y un algoritmo correcto tiene que mandar huecos distintos a
hojas distintas del árbol de decisión. La razón es que si $x_1$ y $x_2$ llegan a la
misma hoja, cualquier $a_i$ entre ellos recorre el mismo camino, y el algoritmo diría
que no está cuando sí está. En esas entradas ninguna comparación responde $=$, así que
esa parte del árbol es binaria. Un árbol binario con $n+1$ hojas tiene altura al menos
$\lceil \log_2 (n+1) \rceil$:

$$\boxed{\text{todo algoritmo de comparaciones necesita} \;\ge\; \lceil \log_2 (n+1) \rceil}$$

La cota superior y la inferior coinciden **exactamente**, sin ni siquiera una
constante de diferencia, así que la búsqueda binaria es óptima.

Hay un detalle que conviene notar: usamos $\log_2$ y no $\log_3$, aunque las
comparaciones tienen tres respuestas posibles. Eso funciona porque contamos solo las
entradas que no están, donde el "$=$" nunca aparece.

## Comprobación

El script busca **todas** las consultas posibles (los $n$ elementos y un valor en cada
uno de los $n+1$ huecos) para cada $n$ de 0 a 300. En cada iteración verifica con
`assert` que se cumplen $I_1$ e $I_2$ y que $\Phi$ bajó a la mitad o menos. Al final
verifica que el peor caso medido sea **igual** a $\lceil\log_2(n+1)\rceil$:

```
     n  huecos  cota ⌈log2(n+1)⌉  peor caso medido
     1       2                 1                 1
     7       8                 3                 3
     8       9                 4                 4
   100     101                 7                 7
  1000    1001                10                10
100000  100001                17                17
```

Los saltos están donde la cota los predice: con $n = 7$ hay 8 huecos y bastan 3
comparaciones, y con $n = 8$ hay 9 huecos y ya hacen falta 4.

## Dos errores plantados: uno para cada herramienta

Hay dos errores típicos al escribir la búsqueda binaria. Cada uno rompe una de las dos
herramientas de la demostración.

**`hi = m - 1` rompe el invariante.** Es el error de mezclar la convención de ventana
cerrada `[lo, hi]` con la de ventana semiabierta `[lo, hi)`. En el paso de
mantenimiento solo sabemos que $A[m] > x$, no que $A[m-1] > x$, así que $I_2$ deja de
valer para la posición $m - 1$. El elemento en esa posición queda fuera de la ventana
sin haberse comparado. Contraejemplo mínimo: `A = [1, 2, 3]`, `x = 1`. Primero se
compara con el 2, se asigna `hi = 0` y el algoritmo responde "hueco 0".

**`lo = m` rompe el potencial.** Con $\Phi = 1$ se tiene $m = lo$, así que `lo = m` no
cambia nada y $\Phi$ no baja. El ciclo no termina. Contraejemplo mínimo: `A = [1, 2]`,
`x = 3`.

Esta tabla muestra cuántas veces los atrapan las pruebas aleatorias (2000 arreglos con
$n \le 100$ y una consulta de cada tipo por arreglo):

| variante   | fallos con x en el arreglo | fallos con x fuera del arreglo | prueba exhaustiva (n ≤ 50) |
|------------|----------------------------|--------------------------------|----------------------------|
| `hi = m-1` | 40,5 %                     | 37,5 %                         | lo detecta                 |
| `lo = m`   | 0,0 %                      | 96,4 %                         | lo detecta                 |

La variante `lo = m` nunca falla si se buscan solo elementos que están en el arreglo,
que es lo primero que uno prueba. Para que $\Phi$ se quede en 1 hace falta descartar el
último candidato por la derecha, y eso solo pasa si $x$ es mayor que él. Si $x$ está en
el arreglo, se encuentra antes. El potencial dice qué hay que probar: entradas donde
$\Phi = 1$ y la comparación responde $>$, es decir, valores que no están en el arreglo.
