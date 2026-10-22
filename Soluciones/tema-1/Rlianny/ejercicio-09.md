
# Ejercicio 09: mezcla "optimizada"

## Enunciado

Una mezcla "optimizada" de dos listas ordenadas de largo `n` deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la cota inferior de la mezcla (`2n - 1`) para decidir si es correcta, y construye con el adversario la entrada en la que falla.

## Convenciones

- **Modelo:** comparaciones. El algoritmo solo conoce los valores por preguntas del tipo `A[i] <= B[j]`. Todo el cómputo con índices y respuestas es gratis.
- **Costo:** el número de comparaciones. Una comparación entre `A[i]` y `B[j]` cuenta como una, tenga el resultado que tenga.
- **Entrada:** `A` y `B` ordenadas de menor a mayor, ambas de largo `n`, con valores distintos.
- **Notación:** en la prosa uso `a_1, ..., a_n` y `b_1, ..., b_n` (desde 1). En el código `a_k = A[k-1]`.
- **Alcance de la cota inferior:** vale solo en este modelo.


## Estructura o Algoritmo

```
mezcla_optimizada(A, B):          // largo n cada una
    R = []
    i = 0
    j = 0
    while n - i >= 2 and j < n:   // a A le quedan al menos 2 elementos
        if A[i] <= B[j]:          // 1 comparación
            R = R + [A[i]]
            i = i + 1
        else:
            R = R + [B[j]]
            j = j + 1
    // aquí i = n - 1 o j = n
    return R + B[j..n-1] + A[i..n-1]   // si queda uno en A, va al final
```

## Complejidad

**Peor caso: `2n - 2` comparaciones**, una menos que la mezcla normal (`2n - 1`).

**Cota superior.** Cada vuelta hace una comparación y saca un elemento, así que al salir `comparaciones = |R| = i + j`. La última vuelta empezó con `i <= n - 2` y `j <= n - 1` y subió una de las dos en 1, así que `i + j <= (n - 2) + (n - 1) + 1 = 2n - 2`.

**Se alcanza.** Con `b_1 < a_1 < b_2 < a_2 < ... < b_n < a_n`, por ejemplo `A = [1, 3, ..., 2n-1]` y `B = [0, 2, ..., 2n-2]`. Salen `b_1, a_1, ..., b_{n-1}, a_{n-1}`, que son `2n - 2` comparaciones, y queda `a_n` en `A`. Esa entrada se mezcla bien, porque `a_n` es el máximo.

## Casos de prueba

| Caso | A | B | Salida | Comparaciones | ¿Correcta? |
|---|---|---|---|---|---|
| n = 1, a < b (falla) | [0] | [1] | [1, 0] | 0 | **no** |
| n = 1, b < a | [1] | [0] | [0, 1] | 0 | sí |
| n = 2, cadena (falla) | [0, 2] | [1, 3] | [0, 1, 3, 2] | 1 | **no** |
| n = 2, máximo en A | [1, 3] | [0, 2] | [0, 1, 2, 3] | 2 | sí |
| n = 5, cadena (falla) | [0, 2, 4, 6, 8] | [1, 3, 5, 7, 9] | [0, 1, 2, 3, 4, 5, 6, 7, 9, 8] | 7 | **no** |
| n = 5, peor caso (2n-2) | [1, 3, 5, 7, 9] | [0, 2, 4, 6, 8] | [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | 8 | sí |

Peor caso por búsqueda exhaustiva¹:

| n | entradas | peor caso | 2n-2 |
|---|---|---|---|
| 1 | 2 | 0 | 0 |
| 2 | 6 | 2 | 2 |
| 3 | 20 | 4 | 4 |
| 4 | 70 | 6 | 6 |
| 5 | 252 | 8 | 8 |
| 6 | 924 | 10 | 10 |
| 7 | 3432 | 12 | 12 |
| 8 | 12870 | 14 | 14 |

## Cota inferior (adversario)

**Teorema.** Todo algoritmo correcto de comparaciones que mezcla dos listas ordenadas de largo `n` hace, en el peor caso, al menos `2n - 1` comparaciones.

**Adversario.** Contesta como si la entrada fuera la cadena intercalada

```
a_1 < b_1 < a_2 < b_2 < ... < a_n < b_n
```

Tiene `2n - 1` pares de vecinos, y cada par tiene un elemento de `A` y uno de `B`.

**Demostración.** Supongamos que el algoritmo termina sin haber comparado un par de vecinos `x, y`. Intercambiemos los valores de `x` e `y`.

1. Las dos listas siguen ordenadas, porque `x` e `y` son vecinos en la cadena y no hay ningún valor entre ellos.
2. Toda comparación que el algoritmo hizo da la misma respuesta. Ninguna comparó a `x` con `y`, y para cualquier otro elemento `z`, `x` y `y` quedan del mismo lado de `z`.
3. Entonces el algoritmo recorre el mismo camino y da la misma salida en posiciones, pero la salida correcta cambió: `x` e `y` están en el orden contrario.

Se equivoca en una de las dos entradas. Por tanto, un algoritmo correcto compara los `2n - 1` pares. ∎

**Aplicación.** Sobre la cadena, con `n >= 2`, la mezcla optimizada hace solo `2n - 3` comparaciones. Los dos pares que se salta son `(b_{n-1}, a_n)` y `(a_n, b_n)`. Como `2n - 3 < 2n - 1`, **no puede ser correcta**, sin ejecutarla.

**La entrada que falla.** Es la propia cadena: la optimizada saca `a_1, b_1, ..., a_{n-1}`, se detiene porque a `A` le queda solo `a_n`, y devuelve `... a_{n-1}, b_n, a_n` con `a_n < b_n`. Si intercambias `a_n` y `b_n` (un par que no se comparó), el algoritmo da la misma salida en posiciones, y para esa otra entrada sí es correcta. Por eso solo falla en una de las dos.

¹ **Verificación en código** (`verificar_ejercicio_NN.py`, Python 3, sin dependencias, generado con un LLM a partir de pseudocódigo, generado con un LLM a partir del pseudocódigo):

- Casos de prueba fijos: coinciden con la tabla de arriba.
- Búsqueda exhaustiva sobre todas las `C(2n, n)` entradas para `n = 1..8`: el peor caso es `2n - 2`.
- Cadena intercalada para `n = 2, 3, 4, 5, 8, 16, 64`: la mezcla normal hace `2n - 1` comparaciones y sale bien; la optimizada hace `2n - 3` y sale mal.
- Argumento del intercambio para `n = 2..6`: la cadena y la entrada con `a_n` y `b_n` intercambiados dan la misma salida en posiciones, y exactamente una de las dos es correcta.
- Cota inferior exacta por minimax sobre todos los algoritmos de comparaciones: el mínimo del peor caso es `1, 3, 5, 7` para `n = 1, 2, 3, 4`, es decir `2n - 1`.
- Pruebas aleatorias contra `sorted` (`n = 5, 20, 100`): la optimizada falla en cerca de la mitad de las entradas y nunca supera `2n - 2` comparaciones.
