## Problema 9

Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Contar cuántas comparaciones hace en el peor caso. Sin probarla, usar la sección 6 de la conferencia 5 para decidir si es correcta, y construir con el adversario la entrada en la que falla.

### Respuesta

```python
def mezclar_optimizada(I, D, cuenta):
    R, i, j = [], 0, 0
    while i < len(I) - 1 and j < len(D):   
        cuenta[0] += 1
        if I[i] <= D[j]:
            R.append(I[i]); i += 1
        else:
            R.append(D[j]); j += 1
    if j == len(D):                         
        return R + I[i:]
    return R + D[j:] + [I[-1]]             
```

La "optimización" es suponer que el último elemento de I va después de todo lo que queda en D.

### Comparaciones en el peor caso

Igual que en la mezcla normal, cada comparación saca un elemento a la salida: o sube i o sube j. Entonces el número de comparaciones es $i + j$ al salir del while.

El while termina en uno de dos casos:

- Se llegó a $i = n-1$. Como seguía siendo $j < n$, se tiene $j \le n-1$. Total: $i + j \le (n-1) + (n-1) = 2n-2$.
- Se llegó a $j = n$. Como seguía siendo $i < n-1$, se tiene $i \le n-2$. Total: $i + j \le (n-2) + n = 2n-2$.

En los dos casos son a lo sumo $2n-2$ comparaciones, y se alcanza: por ejemplo con $b_1 < a_1 < b_2 < a_2 < \dots < b_{n-1} < a_{n-1}$ (y $a_n, b_n$ más grandes), el algoritmo alterna y saca $n-1$ de cada lista antes de parar.

$$\text{peor caso} = 2n - 2.$$

### Correctitud (sección 6)

La sección 6 demuestra que:

 Mezclar dos listas ordenadas de largo $n$ requiere $2n-1$ comparaciones en el peor caso.

Es una cota mínima en el modelo de comparaciones, o sea, vale para todo algoritmo correcto. Nuestro algoritmo es de comparaciones y en el peor caso hace

$$2n - 2 < 2n - 1.$$

Por lo tanto no puede ser correcto: existe al menos una entrada en la que da una salida mal. Esto lo decidimos sin correrlo, igual que con el torneo que se salta un rival en la sección 8.

El adversario de la sección 6 contesta como si la entrada fuera la intercalada perfecta

$$a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n .$$

Esa cadena tiene $2n-1$ pares de vecinos, y un algoritmo correcto tiene que comparar todos. Veamos qué hace el nuestro con esas respuestas:

| comparación | respuesta | sale |
|---|---|---|
| $a_1$ vs $b_1$ | $a_1 < b_1$ | $a_1$ |
| $a_2$ vs $b_1$ | $b_1 < a_2$ | $b_1$ |
| $a_2$ vs $b_2$ | $a_2 < b_2$ | $a_2$ |
| … | … | … |
| $a_{n-1}$ vs $b_{n-1}$ | $a_{n-1} < b_{n-1}$ | $a_{n-1}$ → ahora $i = n-1$, para |

Hizo $(n-1) + (n-2) = 2n-3$ comparaciones. Los pares de vecinos que nunca comparó son:

$$(b_{n-1}, a_n) \quad\text{y}\quad (a_n, b_n).$$

Tomo el par $(a_n, b_n)$ y hago lo de la demostración: intercambio sus valores.

- Las dos listas siguen ordenadas, porque $a_n$ y $b_n$ son vecinos en la cadena y no hay nada entre ellos.
- Todas las comparaciones que hizo el algoritmo dan la misma respuesta, porque ninguna involucraba a $a_n$ ni a $b_n$.
- Pero la salida correcta cambia: en la intercalada $a_n$ va antes que $b_n$; en la intercambiada va después.

El algoritmo recorre el mismo camino en las dos entradas, así que da la misma salida: $\dots, b_{n-1}, b_n, a_n$ (pone $a_n$ al final). Eso es correcto para la intercambiada y está mal para la intercalada.

La entrada en la que falla es la intercalada perfecta. Pot ejemplo con $n = 4$:

```
I = [1, 3, 5, 7]
D = [2, 4, 6, 8]

salida del algoritmo:  1 2 3 4 5 6 8 7
salida correcta:       1 2 3 4 5 6 7 8
```

Comparó $1\text{-}2,\ 3\text{-}2,\ 3\text{-}4,\ 5\text{-}4,\ 5\text{-}6$ (son $2n-3 = 5$), y nunca comparó $7$ con $6$ ni con $8$.


