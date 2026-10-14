## Ejercicio 9 ★★ — Una mezcla "optimizada" de dos listas ordenadas

### Enunciado con modelo

> Una mezcla "optimizada" de dos listas ordenadas de largo n deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla. (C5)

**Modelo.** Modelo de comparaciones. Tenemos dos listas ordenadas A = [a₁ < a₂ < … < aₙ] y B = [b₁ < b₂ < … < bₙ]. El algoritmo de mezcla produce una lista ordenada de 2n elementos. El costo es el número de comparaciones entre elementos de A y B. Trabajamos con el modelo de la Conferencia 5, secciones 6 y 7.

**Precisión del problema.** La mezcla óptima hace exactamente 2n-1 comparaciones en el peor caso (sección 6 de la Conferencia 5). La versión "optimizada" que vamos a analizar hace menos, y por lo tanto **debe ser incorrecta** por la cota mínima. El ejercicio pide: (1) contar las comparaciones que hace, (2) decidir si es correcta sin probarla, usando la cota mínima, y (3) construir con el adversario la entrada donde falla.
### La mezcla "optimizada"

La versión optimizada dice: **cuando a la primera lista le queda un solo elemento, deja de comparar y lo pone al final**. El código sería:

```
def mezclar_optimizada(A, B):
    R = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if len(A) - i == 1:  # a A le queda un solo elemento
            break  # deja de comparar y lo pone al final
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    R.extend(A[i:])
    R.extend(B[j:])
    return R
```

**Cuenta de comparaciones en el peor caso.** El ciclo se detiene cuando a A le queda un solo elemento, es decir, después de n-1 elementos de A han salido. En cada vuelta del ciclo, o sale un elemento de A o sale uno de B. Para que salgan n-1 elementos de A, tienen que haber salido a lo sumo n-1 elementos de B (porque cada comparación saca uno). Así que el ciclo hace a lo sumo (n-1) + (n-1) = 2n-2 comparaciones.

**La mezcla optimizada hace a lo sumo 2n-2 comparaciones.** Una menos que la cota mínima 2n-1.

### ¿Es correcta? No, por la cota mínima

**La sección 6 de la Conferencia 5 demuestra que mezclar dos listas ordenadas de largo n requiere 2n-1 comparaciones en el peor caso.** La demostración usa el adversario de la **entrada intercalada perfecta**:

a₁ < b₁ < a₂ < b₂ < … < aₙ < bₙ.

Esa cadena tiene 2n-1 pares de vecinos, cada uno con un elemento de cada lista. Si el algoritmo termina sin haber comparado algún par de vecinos (aᵢ, bᵢ), intercambiar sus valores produce otra entrada con la misma salida pero orden distinto, y el algoritmo se equivoca en una de las dos.

**La mezcla optimizada hace a lo sumo 2n-2 comparaciones, que es menos que 2n-1.** Por la cota mínima, **no puede ser correcta**. No hace falta probarla: la cota lo dice.

### La entrada donde falla (construida con el adversario)

El adversario elige la entrada intercalada perfecta y hace que el algoritmo se salte la comparación del último par de vecinos. Veamos exactamente dónde falla.

Tomemos n = 3:

A = [a₁, a₂, a₃] = [1, 3, 5]
B = [b₁, b₂, b₃] = [2, 4, 6]

La entrada intercalada perfecta es 1 < 2 < 3 < 4 < 5 < 6.

**Traza de la mezcla optimizada:**

- i=0, j=0. len(A) - i = 3 ≠ 1. Compara A[0]=1 con B[0]=2. 1 ≤ 2, saca 1. i=1. R=[1].
- i=1, j=0. len(A) - i = 2 ≠ 1. Compara A[1]=3 con B[0]=2. 3 > 2, saca 2. j=1. R=[1,2].
- i=1, j=1. len(A) - i = 2 ≠ 1. Compara A[1]=3 con B[1]=4. 3 ≤ 4, saca 3. i=2. R=[1,2,3].
- i=2, j=1. len(A) - i = 1. **Break.** Deja de comparar.
- R.extend(A[2:]) → añade 5. R=[1,2,3,5].
- R.extend(B[1:]) → añade 4, 6. R=[1,2,3,5,4,6].

**El resultado es [1, 2, 3, 5, 4, 6], que no está ordenado.** El error: cuando a A le queda un solo elemento (5), el algoritmo lo pone al final, pero B todavía tiene elementos (4, 6) que deberían ir antes que 5. El 4 va antes que 5, y el algoritmo no lo compara.

**La entrada exacta donde falla:** cualquier entrada donde el último elemento de A esté entre dos elementos de B que aún no han salido. Por ejemplo, A = [1, 3, 5], B = [2, 4, 6], donde 5 está entre 4 y 6.

### Costo

- **Peor caso de la mezcla optimizada:** 2n-2 comparaciones.
- **Peor caso de la mezcla óptima:** 2n-1 comparaciones.
- **Diferencia:** 1 comparación. La mezcla optimizada ahorra una comparación a costa de ser incorrecta.

### Cota mínima

La cota de la sección 6 de la Conferencia 5: **mezclar dos listas ordenadas de largo n requiere 2n-1 comparaciones en el peor caso.** La mezcla óptima la alcanza. La mezcla optimizada hace 2n-2, que está por debajo de la cota, y por lo tanto es incorrecta.

### Código

**Archivo:** `codigo/ejercicio-09.py`

### Figura

**Archivo:** ![](figuras/ejercicio-09-intercalada.png)

### Casos de prueba

| n | Mezcla óptima | Mezcla optimizada | 2n-1 | ¿Optimizada ordenada? |
|---|---------------|-------------------|------|----------------------|
| 2 | 3 | 2 | 3 | Depende |
| 3 | 5 | 4 | 5 | **No** (con [1,3,5] y [2,4,6]) |
| 5 | 9 | 8 | 9 | **No** |
| 10 | 19 | 18 | 19 | **No** |
| 100 | 199 | 198 | 199 | **No** |

**La mezcla optimizada siempre hace 2n-2 comparaciones, una menos que la cota. Y falla en la entrada intercalada perfecta.**

### Conclusión

La mezcla optimizada hace 2n-2 comparaciones, una menos que la cota mínima 2n-1. Por la sección 6 de la Conferencia 5, **ningún algoritmo correcto puede hacer menos de 2n-1**, así que la mezcla optimizada es incorrecta. La entrada donde falla es la intercalada perfecta: cuando a A le queda un solo elemento, el algoritmo lo pone al final, pero puede haber elementos de B que deberían ir antes. La cota mínima detectó el error sin necesidad de probar.
