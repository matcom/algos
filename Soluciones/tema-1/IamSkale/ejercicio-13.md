# Ejercicio 13 ★★ — Splay tree: acceso secuencial sobre un camino (C4)

> En un splay tree que empieza como un camino de $n$ nodos se accede a las claves $1,\dots,n$ en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota?

## Datos

- Árbol inicial: el camino de la C4 (`camino(n)`): $n$ en la raíz y cada clave $k$ hija izquierda de $k+1$. La clave 1 está a profundidad $n-1$.
- Costo de un acceso: el número de rotaciones del splay (1 si el nodo ya es la raíz).
- Potencial: $\Phi=\sum_x r(x)$, con $r(x)=\log_2 s(x)$ y $s(x)$ el tamaño del subárbol de $x$.
- **Lema de acceso (Sleator y Tarjan):** el costo amortizado de un splay de $x$ es $\le 3(r(t)-r(x))+1\le 3\log_2 n+1$.

## La cota (la cuenta de la C4 §5)

Con $\hat c_i=c_i+\Phi_i-\Phi_{i-1}$ y sumando sobre los $n$ accesos:
$$\sum_{i=1}^n c_i=\sum_{i=1}^n\hat c_i-(\Phi_n-\Phi_0)\le n(3\log_2 n+1)+\Phi_0-\Phi_n .$$

- **Potencial inicial:** en el camino, los subárboles tienen tamaños $1,2,\dots,n$, así que $\Phi_0=\sum_{k=1}^n\log_2 k=\log_2 n!\le n\log_2 n$.
- **Potencial final:** $\Phi_n\ge0$. (De hecho, después de acceder a $1,\dots,n$ en orden el árbol vuelve a ser un camino con $n$ en la raíz, así que $\Phi_n=\Phi_0$. El código lo comprueba.)

Entonces
$$\boxed{\sum c_i\ \le\ n(3\log_2 n+1)+\log_2 n!\ \le\ 4n\log_2 n+n = O(n\log n).}$$

Usando $\Phi_n=\Phi_0$ se obtiene la versión más fina $\sum c_i\le n(3\log_2 n+1)$, que sigue siendo $\Theta(n\log n)$.

## Lo que mide la sección 6

La C4 §6 midió, recorriendo las claves en orden durante tres rondas, **4,2 / 4,2 / 4,3 / 4,4 rotaciones por acceso** para $n=100,200,400,800$, contra $n/2$ de "subir a la raíz". Medimos abajo una sola ronda desde el camino y sale lo mismo: unas **4,2–4,4 por acceso**, es decir, un **costo total $\approx4{,}3n=\Theta(n)$**.

| $n$ | real (rotaciones) | cota del lema con los rangos exactos | cota $n(3\log_2 n+1)+\log_2 n!$ |
|---|---|---|---|
| 100 | ≈ 416 | ≈ 1442 | ≈ 2618 |
| 1600 | ≈ 7024 | ≈ 34835 | ≈ 67419 |

(Los valores exactos los imprime el código de abajo.)

## ¿Es ajustada la cota? No, para esta secuencia

- **Asintóticamente:** la cota es $\Theta(n\log n)$ y el costo real es $\Theta(n)$. El cociente cota/real crece como $\log n$.
- **Dónde se pierde:** como $\Phi_n=\Phi_0$, la suma de los amortizados reales es igual a la suma de los costos reales, $\approx4{,}3n$. El lema, en cambio, le asigna a cada acceso hasta $3\log_2 n+1$. En esta secuencia el amortizado real de cada acceso es $O(1)$ en promedio, y el lema no lo ve, porque solo usa $r(x)\ge0$ y $r(t)=\log_2 n$.
- **El resultado correcto** para esta secuencia es el **teorema de acceso secuencial** (Tarjan, 1985): acceder a las $n$ claves en orden cuesta $O(n)$ en total, sea cual sea el árbol inicial. Su demostración necesita un argumento más fino que el lema de acceso.
- **El lema sí es ajustado en general:** hay secuencias (por ejemplo, accesos al azar) en las que el splay cuesta $\Theta(\log n)$ por acceso. Abajo se ve cómo crece el costo con accesos al azar.
- **Un acceso suelto sí alcanza el orden de la cota:** el primero (a la clave 1) cuesta $n-1$ rotaciones. El potencial lo paga: el lema le asigna solo $3\log_2 n+1$ amortizado, y la caída de $\Phi$ cubre el resto.

## Código de validación

Es el código de la C4 §4–5, con los recorridos escritos de forma iterativa (para $n$ grande la recursión de Python se queda corta en un camino).

> Código: [ejercicio-13.py](ejercicio-13.py), parte 1.

**El experimento:** una ronda de accesos $1..n$ desde el camino. Medimos el costo real, comprobamos el lema en cada acceso y calculamos las dos cotas.

> Código: [ejercicio-13.py](ejercicio-13.py), parte 2.

```text
    n   real  real/n  lema exacto  cota C4 §5  cota/real  Phi_n = Phi_0
  100    416    4.16         1442        2618        6.3           True
  200    840    4.20         3240        6032        7.2           True
  400   1732    4.33         7211       13659        7.9           True
  800   3490    4.36        15909       30512        8.7           True
 1600   7024    4.39        34835       67419        9.6           True
```

La columna `cota/real` crece con $n$ (como $\log n$): la cota no es ajustada.

**Comparación con la C4 §6** (tres rondas, splay y subir a la raíz):

> Código: [ejercicio-13.py](ejercicio-13.py), parte 3.

```text
     n    splay  subir a la raíz  3 log2 n + 1
   100      4.2             50.5          20.9
   200      4.2            100.5          23.9
   400      4.3            200.5          26.9
   800      4.4            400.5          29.9
```

Son los mismos números de la tabla de la C4 §6.

**El lema sí es ajustado para otras secuencias.** Con accesos al azar el costo por acceso crece con $\log n$:

> Código: [ejercicio-13.py](ejercicio-13.py), parte 4.

```text
     n  rotaciones por acceso (al azar)  log2 n
   100                             6.79    6.64
   400                             9.70    8.64
  1600                            12.70   10.64
  6400                            15.60   12.64
```

## Resumen

- **Cota (lema + C4 §5):** $\sum c\le n(3\log_2 n+1)+\Phi_0-\Phi_n\le n(3\log_2 n+1)+\log_2 n!=O(n\log n)$.
- **Medido (C4 §6):** $\approx4{,}2$–$4{,}4$ rotaciones por acceso, $\Theta(n)$ en total.
- **No es ajustada** para esta secuencia: el cociente crece como $\log n$. El costo real $O(n)$ es el teorema de acceso secuencial, que el lema de acceso no alcanza a demostrar. El lema sí es ajustado para otras secuencias (accesos al azar).
