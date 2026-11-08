# Ejercicio 9: la mezcla "optimizada"

> Una mezcla "optimizada" de dos listas ordenadas de largo n deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla. (C5)

Modelo: comparaciones entre elementos.

## La mezcla normal

Dadas dos listas ordenadas A y B, el más chico de todos es el primero de A o el primero de B. Se comparan los primeros, se saca el menor, y se repite; cuando una lista se vacía, se pega lo que queda de la otra. Con A = [1, 4, 6] y B = [2, 3, 5]:

| comparo | saco | resultado |
|---|---|---|
| 1 vs 2 | 1 | 1 |
| 4 vs 2 | 2 | 1 2 |
| 4 vs 3 | 3 | 1 2 3 |
| 4 vs 5 | 4 | 1 2 3 4 |
| 6 vs 5 | 5 | 1 2 3 4 5 |
| B vacía: pego el 6 | 6 | 1 2 3 4 5 6 |

Cada comparación saca un elemento, y el último sale sin comparar: 2n − 1 comparaciones en el peor caso.

## La versión optimizada

Hace lo mismo, pero cuando a A le queda un solo elemento deja de comparar: pega lo que queda de B y pone ese último elemento de A al final de todo. Supone que el último de A es el más grande. Con el ejemplo de arriba funciona, y con 4 comparaciones en vez de 5.

## Comparaciones en el peor caso: 2n − 2

Cada comparación saca un elemento. De A saca, comparando, como mucho n − 1 elementos, porque para cuando le queda uno. De B saca como mucho n − 1: si sacara los n, B se vaciaría y ya no habría con qué comparar. En total, a lo sumo **2n − 2**, y se alcanza (por ejemplo, cuando el último de A es el máximo y B se va sacando hasta su último elemento).

## Sin probarla: tiene que estar mal

La sección 6 de la conferencia 5 demuestra que todo algoritmo correcto que mezcla dos listas ordenadas de largo n hace al menos **2n − 1** comparaciones en el peor caso. El argumento es un adversario sobre la entrada intercalada a₁ < b₁ < a₂ < b₂ < … < aₙ < bₙ: si el algoritmo no compara algún par de vecinos de ese orden, se intercambian sus valores, las dos listas siguen ordenadas, todas las comparaciones hechas dan lo mismo, pero la salida correcta cambia. El algoritmo da la misma salida para las dos entradas, así que se equivoca en una. Hay 2n − 1 pares de vecinos, y hay que compararlos todos.

La versión optimizada hace 2n − 2 en el peor caso, una menos que la cota. Entonces **no puede ser correcta**: tiene que fallar en alguna entrada.

## La entrada en la que falla

El ejemplo más chico: A = [1, 3] y B = [2, 4]. Compara 1 con 2 y saca el 1; a A le queda solo el 3, así que para, pega lo que queda de B (2, 4) y pone el 3 al final: **[1, 2, 4, 3]**. No está ordenado: el 4 va antes que el 3. Hizo una sola comparación, y la mezcla correcta necesita 2n − 1 = 3.

**La construcción del adversario.** Tomo la entrada intercalada, A = [1, 3, 5, 7] y B = [2, 4, 6, 8]. La versión optimizada compara 1–2, 3–2, 3–4, 5–4 y 5–6, y ahí a A le queda solo el 7: para. Los pares de vecinos del orden final que quedan sin comparar son (6, 7) y (7, 8). El resultado es

```
1 2 3 4 5 | lo que queda de B: 6 8 | el último de A: 7
→ 1 2 3 4 5 6 8 7   (mal: el 8 va antes que el 7)
```

Si intercambio los valores del par (7, 8), A = [1, 3, 5, 8] y B = [2, 4, 6, 7], las dos listas siguen ordenadas y las cinco comparaciones dan lo mismo, porque ninguna tocaba el 7 ni el 8. El algoritmo hace exactamente lo mismo, y aquí el resultado sale bien: 1 2 3 4 5 6 7 8. Pero en las dos entradas el orden correcto del 7 y el 8 es distinto, y el algoritmo no puede distinguirlas: en una de las dos falla.

**Cuándo falla en general.** Exactamente cuando el máximo de todo está en B. Si el máximo está en A, es el último de A, y ponerlo al final es correcto. Si está en B, el último de A queda al final por encima del máximo. Por simetría, eso pasa en la mitad de las entradas.

## Experimentos

`ej09_mezcla_optimizada.py` recorre todas las formas de repartir los números 0, …, 2n − 1 en dos listas ordenadas de largo n, para n de 1 a 7, y comprueba que la versión optimizada falla exactamente cuando el máximo está en B:

```
  n  peor normal  peor optimizada  cota 2n-1       falla en
  1            1                0          1      1/2
  2            3                2          3      3/6
  3            5                4          5     10/20
  4            7                6          7     35/70
  5            9                8          9    126/252
  6           11               10         11    462/924
  7           13               12         13   1716/3432
```

El peor caso de la versión optimizada es siempre 2n − 2, una menos que la cota, y falla en exactamente la mitad de las entradas. Después corre la entrada intercalada del adversario:

```
intercalada A=[1, 3, 5, 7] B=[2, 4, 6, 8]
  resultado [1, 2, 3, 4, 5, 6, 8, 7] con 5 comparaciones: MAL
  pares de vecinos que nunca comparó: [(6, 7), (7, 8)]
intercambiando 7 y 8: A=[1, 3, 5, 8] B=[2, 4, 6, 7]
  mismas comparaciones: True; resultado [1, 2, 3, 4, 5, 6, 7, 8]: bien
```

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones de la mezcla y del adversario de la conferencia 5, pistas y corrección de mi redacción). La cuenta del peor caso, la entrada que falla y los pares sin comparar son míos.*
