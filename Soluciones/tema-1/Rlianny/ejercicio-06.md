# Ejercicio 6: Búsqueda en matriz n×n con filas y columnas ordenadas

## Enunciado
Una matriz n×n tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor x en O(n) comparaciones, demuestra su correctitud con un invariante y demuestra con un adversario que no se puede en o(n).

## Convenciones
- `A` es una matriz n×n. Las posiciones se escriben (fila, columna), con índices de 1 a `n`.
- "Ordenadas de forma creciente" se entiende en sentido no estricto (≤): `A[i][j] ≤ A[i][j+1]` y `A[i][j] ≤ A[i+1][j]`. Puede haber valores repetidos.
- Se busca el valor `x`. Se cuenta como una comparación cada vez que se compara un elemento de `A` con `x`, y su resultado puede ser <, = o >.

## Idea
La posición (1,n) es la que más información aporta: es el mayor de su fila y el menor de su columna. Ahí se coloca un único puntero. Cada comparación permite descartar una fila o una columna completa (de la parte que aún no se ha descartado).

## Algoritmo
```
r = 1; c = n
while r ≤ n and c ≥ 1:
    if A[r][c] = x:  return "sí"
    if A[r][c] > x:  c = c - 1      // se descarta la columna c, el puntero va a la izquierda
    else:            r = r + 1      // se descarta la fila r, el puntero va hacia abajo
return "no"                         // el puntero salió de la matriz
```

## Por qué funciona
- **`A[r][c] > x`:** todo lo que está debajo en la columna `c` es ≥ `A[r][c]`, luego > `x`. La columna `c` no contiene a `x`, y el puntero se mueve hacia la izquierda.
- **`A[r][c] < x`:** todo lo que está a la izquierda en la fila `r` es ≤ `A[r][c]`, luego < `x`. La fila `r` no contiene a `x`, y el puntero se mueve hacia abajo.
- **`A[r][c] = x`:** el algoritmo se detiene y responde "sí".
- **El puntero sale de la matriz** (`r > n` o `c < 1`): no queda región viva y `x` no está.

## Ejemplo ilustrado

### Ejemplo 1: el valor está en la matriz
![Ejemplo 1, frame 1](ejercicio-06-ejemplo01-01.png)

![Ejemplo 1, frame 2](ejercicio-06-ejemplo01-02.png)

![Ejemplo 1, frame 3](ejercicio-06-ejemplo01-03.png)

![Ejemplo 1, frame 4](ejercicio-06-ejemplo01-04.png)

![Ejemplo 1, frame 5](ejercicio-06-ejemplo01-05.png)

![Ejemplo 1, frame 6](ejercicio-06-ejemplo01-06.png)

### Ejemplo 2: el valor no está en la matriz
![Ejemplo 2, frame 1](ejercicio-06-ejemplo02-01.png)

![Ejemplo 2, frame 2](ejercicio-06-ejemplo02-02.png)

![Ejemplo 2, frame 3](ejercicio-06-ejemplo02-03.png)

![Ejemplo 2, frame 4](ejercicio-06-ejemplo02-04.png)

![Ejemplo 2, frame 5](ejercicio-06-ejemplo02-05.png)

![Ejemplo 2, frame 6](ejercicio-06-ejemplo02-06.png)

## Invariante


## Correctitud


## Complejidad
Los elementos de las filas y columnas descartadas se consideran "tachados". La región viva es siempre un rectángulo: las filas `r..n` por las columnas `1..c`. Se define

> `s = (n − r + 1) + c`

que es el número de filas vivas más el de columnas vivas del rectángulo (puede valer 0 en una de las dos partes).

- Al inicio `r = 1` y `c = n`, así que `s = 2n`.
- Cada comparación que no termina el algoritmo reduce `s` exactamente en 1: o bien `c` baja en 1, o bien `r` sube en 1. Esto vale también en el último paso, cuando el rectángulo se queda sin filas o sin columnas.
- El ciclo solo corre mientras `r ≤ n` y `c ≥ 1`, es decir, con al menos 1 fila y 1 columna vivas, luego `s ≥ 2` antes de cada comparación y `s ≥ 1` después.

Entonces:
- Comparaciones que reducen `s`: a lo sumo 2n − 1.
- Más una comparación final si se encuentra el valor.

Así que el número de comparaciones está acotado por 2n y es O(n).


## Casos de prueba
Todos usan la matriz del ejemplo ilustrado (n = 3), salvo que se indique otra:

```
2   5   9
4   6  10
7   8  12
```

| ID | Qué prueba | `x` | Resultado | Comparaciones | Recorrido del puntero |
|----|------------|-----|-----------|---------------|-----------------------|
| C1 | `x` presente en posición intermedia | 6 | sí | 3 | (1,3) → (1,2) → (2,2) |
| C2 | `x` menor que el mínimo | 1 | no | 3 | (1,3) → (1,2) → (1,1) → fuera |
| C3 | `x` mayor que el máximo | 13 | no | 3 | (1,3) → (2,3) → (3,3) → fuera |
| C4 | `x` en la esquina superior izquierda | 2 | sí | 3 | (1,3) → (1,2) → (1,1) |
| C5 | `x` ausente, valor intermedio | 3 | no | 4 | ver ejemplo ilustrado |
| C6 | valores repetidos | (otra matriz) | ... | ... | ... |
| C7 | peor caso | ... | ... | 2n − 1 | ... |

Todos los casos cumplen `comparaciones ≤ 2n`, como se demostró en Complejidad.

## Cota inferior (adversario)