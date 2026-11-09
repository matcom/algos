# Ejercicio 6: búsqueda en una matriz ordenada

> Una matriz n×n tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor x en O(n) comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en o(n). (C3, C5)

Modelo: comparaciones de x con casillas de la matriz. Índices de 0 a n − 1.

## Algoritmo

Empiezo en la esquina de arriba a la derecha, (f, c) = (0, n − 1), y comparo x con A[f][c]:

- si x = A[f][c], está;
- si x < A[f][c], descarto la columna c: c = c − 1;
- si x > A[f][c], descarto la fila f: f = f + 1.

Sigo hasta encontrarlo o hasta salirme de la matriz (f = n o c = −1). Si me salgo, x no está. No necesariamente termino en la esquina (n − 1, 0): buscando un x más chico que todo, me salgo por la izquierda en la fila 0.

Ejemplo, buscando x = 9:

```
  1   4   7  11
  2   5   8  12
  3   6   9  16
 10  13  14  17
```

Paso por el 11 (mayor que 9, izquierda), el 7 (menor, abajo), el 8 (menor, abajo) y llego al 9.

## Invariante

> Si x está en la matriz, está en las filas f, …, n − 1 y en las columnas 0, …, c.

Es un rectángulo que va desde la casilla actual hacia abajo y hacia la izquierda.

**Inicialización.** Con f = 0 y c = n − 1, el rectángulo es la matriz entera.

**Mantenimiento.** Si A[f][c] = x, el algoritmo termina. Si no:

- **x < A[f][c]**: los valores de la columna c en las filas f, …, n − 1 son mayores o iguales que A[f][c], porque la columna está ordenada, y por tanto mayores que x. x no puede estar ahí. Si x está en la matriz, está en las filas f, …, n − 1 y las columnas 0, …, c − 1, que es el rectángulo nuevo.
- **x > A[f][c]**: igual con la fila. Los valores de la fila f en las columnas 0, …, c son menores o iguales que A[f][c], porque la fila está ordenada, y por tanto menores que x. Si x está, está en las filas f + 1, …, n − 1 y las columnas 0, …, c.

**Conclusión.** Si devuelve "está", encontró A[f][c] = x. Si se sale de la matriz, f = n o c = −1, y el rectángulo del invariante está vacío: x no está.

## Terminación y costo

Cada comparación descarta una fila entera o una columna entera, no casillas sueltas. Siempre me muevo a la izquierda o hacia abajo y nunca me devuelvo.

Potencial: Φ = (n − f) + (c + 1), la cantidad de filas y columnas que quedan. Empieza en 2n, es un entero no negativo mientras estoy dentro de la matriz, y baja exactamente 1 con cada comparación que no encuentra x. Entonces el algoritmo termina, con a lo sumo **2n − 1** comparaciones (la última me saca de la matriz cuando Φ llega a 1). Es **O(n)**. Memoria O(1).

## Cota mínima: no se puede en o(n)

Construyo una matriz trampa en la que el algoritmo está obligado a mirar n casillas distintas. Sea x = n − 1 y

- A[i][j] = i + j, salvo en la antidiagonal (i + j = n − 1),
- donde A[i][j] = n − 1.5: casi x, pero no x.

Con n = 4 y x = 3:

```
  0     1     2    2.5
  1     2    2.5    4
  2    2.5    4     5
 2.5    4     5     6
```

Está ordenada, y x no está: arriba a la izquierda de la antidiagonal todo es menor que x, y abajo a la derecha todo es mayor.

**Cada casilla de la antidiagonal se puede cambiar por x sin desordenar la matriz.** Por ejemplo, la de la fila 1, columna 2: sus vecinos de arriba y de la izquierda valen 2, menor que 3, y los de abajo y de la derecha valen 4, mayor que 3. En general, los vecinos de arriba y de la izquierda de una casilla de la antidiagonal tienen i + j = n − 2 < x, y los de abajo y de la derecha, i + j = n > x. Y cada fila tiene una sola casilla de la antidiagonal, así que cada una se puede cambiar por separado.

**El argumento.** Si un algoritmo responde "no está" sobre la matriz trampa sin haber mirado alguna casilla de la antidiagonal, cambio esa casilla por x. La matriz sigue ordenada, y todas las comparaciones que hizo el algoritmo dan lo mismo, porque no involucraban esa casilla. Hace exactamente lo mismo y dice "no está"… pero ahora sí está. Se equivoca. Entonces todo algoritmo correcto mira las n casillas de la antidiagonal: al menos **n** comparaciones, **Ω(n)**.

Con el algoritmo de arriba (2n − 1), el costo del problema es **Θ(n)**: el algoritmo es óptimo salvo por la constante.

## Experimentos

`ej06_matriz_ordenada.py`:

- 3000 búsquedas en matrices ordenadas al azar, comparadas contra la búsqueda exhaustiva, con el invariante y el potencial comprobados con `assert` en cada paso. Sin fallos, y nunca más de 2n − 1 comparaciones.
- La matriz trampa para n = 2, 4, 8 y 50: comprueba que está ordenada, que x no está, y que al cambiar cualquiera de las n casillas de la antidiagonal por x sigue ordenada y x pasa a estar.
- Cuántas comparaciones hace el algoritmo sobre la trampa:

```
    n  comparaciones en la trampa  cota mínima n  2n - 1
    4                           7              4       7
   16                          31             16      31
   64                         127             64     127
  256                         511            256     511
```

Sobre la trampa el algoritmo alcanza su peor caso, 2n − 1: entre la cota mínima n y el algoritmo hay un factor 2.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones, pistas, la construcción de la matriz trampa y corrección de mi redacción). El algoritmo, el invariante y su mantenimiento son míos.*
