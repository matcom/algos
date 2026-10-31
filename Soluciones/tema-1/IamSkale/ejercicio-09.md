# Ejercicio 9 ★★ — Una mezcla "optimizada" (C5)

> Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla.

## La variante

`mezcla_optimizada(I, D, cuenta)` es la mezcla de la C5 con un cambio: el ciclo de comparaciones se detiene en cuanto a `I` le queda un solo elemento (o `D` se vacía), y después pega lo que queda de `D` y, al final, el último elemento de `I`. `cuenta` acumula las comparaciones y `registro`, si se pasa, guarda qué pares se compararon.

> Código: [ejercicio-09.py](ejercicio-09.py), parte 1.

Si el ciclo termina porque $D$ se vació, `D[j:]` está vacío y el resultado es el de la mezcla normal. Si termina porque a $I$ le queda un elemento, ese elemento va después de todo lo que queda de $D$.

## Peor caso: $2n-2$ comparaciones

Cada comparación saca exactamente un elemento a la salida. El ciclo puede terminar de dos formas:

- **A $I$ le queda uno.** Salieron $n-1$ elementos de $I$. De $D$ salieron a lo sumo $n-1$: si hubieran salido los $n$, el ciclo habría terminado antes por $D$ vacío. Total $\le2n-2$.
- **$D$ se vació.** Salieron $n$ de $D$ y, como a $I$ le quedan al menos 2, a lo sumo $n-2$ de $I$. Total $\le2n-2$.

La cota se alcanza: con $b_1<a_1<b_2<a_2<\dots<b_n<a_n$ salen $b_1,a_1,\dots,b_{n-1},a_{n-1}$ comparando, es decir $2n-2$ comparaciones. (En esa entrada, además, el resultado es correcto.)

## ¿Es correcta? No, y sin probarla

**Teorema (C5 §6).** Mezclar dos listas ordenadas de largo $n$ requiere $2n-1$ comparaciones en el peor caso.

La variante hace **a lo sumo $2n-2<2n-1$** comparaciones en **todas** las entradas. Por el teorema, existe una entrada en la que se equivoca. Ningún algoritmo correcto puede hacer menos que la cota.

## La entrada en la que falla (adversario)

El adversario de la C5 §6 contesta como si la entrada fuera la **intercalada perfecta**
$$a_1<b_1<a_2<b_2<\dots<a_n<b_n .$$
Esa cadena tiene $2n-1$ pares de vecinos, y un algoritmo correcto tiene que compararlos todos: si no compara un par de vecinos, intercambiar sus valores deja las dos listas ordenadas y todas las respuestas iguales, pero cambia la salida correcta.

Corramos la variante sobre esa entrada. Compara $(a_1,b_1),(a_2,b_1),(a_2,b_2),\dots,(a_{n-1},b_{n-1})$: son $2n-3$ comparaciones. Después de sacar $a_{n-1}$, a $I$ le queda solo $a_n$ y se detiene. **Nunca compara los vecinos $(b_{n-1},a_n)$ ni $(a_n,b_n)$.**

- Entrada intercalada: la variante devuelve $\dots,a_{n-1},b_{n-1},b_n,a_n$. **Mal**: $a_n<b_n$.
- Entrada con $a_n$ y $b_n$ intercambiados (las listas siguen ordenadas): mismas respuestas, misma salida en posiciones, y ahí es correcta.

El algoritmo no distingue las dos entradas, así que se equivoca en una: la intercalada. **Esa es la entrada que falla.**

**Cuándo falla en general.** Exactamente cuando $a_n<b_n$, es decir, cuando el máximo de todo está en la segunda lista. Si $a_n<b_n$, $D$ no puede vaciarse primero (para que $b_n$ salga comparando haría falta un elemento de $I$ mayor o igual que él), así que el ciclo termina con $I=[a_n]$ y $b_n$ todavía en $D$, y $b_n$ queda antes que $a_n$. Si $a_n\ge b_n$, el resultado es correcto. Con entradas al azar, falla la mitad de las veces.

## Casos de prueba y validación

Herramientas de prueba: `correcta(I, D)`, que da el resultado esperado ordenando todo, y `todas_las_entradas(n)`, que genera todas las formas de repartir los valores $0..2n-1$ entre dos listas ordenadas de largo $n$. Esta parte no imprime nada.

> Código: [ejercicio-09.py](ejercicio-09.py), parte 2.

**Peor caso exacto** (recorriendo todas las entradas, como hace la C5 §3 con mergesort):

> Código: [ejercicio-09.py](ejercicio-09.py), parte 3.

```text
  n  peor caso  2n-2  cota 2n-1  entradas  fallan
  1          0     0          1         2       1
  2          2     2          3         6       3
  3          4     4          5        20      10
  4          6     6          7        70      35
  5          8     8          9       252     126
  6         10    10         11       924     462
  7         12    12         13      3432    1716
  8         14    14         15     12870    6435
  9         16    16         17     48620   24310
```

Siempre falla exactamente la mitad de las entradas: las que tienen el máximo en la segunda lista.

**La entrada del adversario:** qué pares de vecinos compara y cuáles no.

> Código: [ejercicio-09.py](ejercicio-09.py), parte 4.

```text
n = 4: 5 comparaciones; pares de vecinos sin comparar: [(5, 6), (6, 7)]
   salida:   [0, 1, 2, 3, 4, 5, 7, 6]
   correcta: [0, 1, 2, 3, 4, 5, 6, 7]
n = 8: 13 comparaciones; pares de vecinos sin comparar: [(13, 14), (14, 15)]
   salida:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14]
   correcta: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```

**Al azar:** las pruebas también lo ven (la mitad de las entradas falla), pero el argumento de la cota no necesitó ninguna.

> Código: [ejercicio-09.py](ejercicio-09.py), parte 5.

```text
falla en 50.7% de 10000 entradas al azar
```

## Resumen

- Peor caso: **$2n-2$** comparaciones.
- Como $2n-2<2n-1$ (cota de la C5 §6), **no puede ser correcta**.
- Entrada del adversario: la intercalada $a_1<b_1<\dots<a_n<b_n$. La variante no compara $a_n$ con $b_n$ y devuelve $\dots,b_n,a_n$.
- En general falla si y solo si $a_n<b_n$: la mitad de las entradas.
