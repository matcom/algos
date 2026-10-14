## Ejercicio 2 ★ — Invariante y potencial de la búsqueda binaria

### Enunciado

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima. (C3, C5)

**Modelo.** Modelo de comparaciones. El algoritmo solo puede comparar x con elementos del arreglo, y cada comparación responde <, = o >. El costo es el número de comparaciones en el peor caso. La entrada es un arreglo ordenado a₁ < a₂ < … < aₙ y un valor x.

### Algoritmo

```
def busqueda_binaria(A, x):
    """Devuelve ("está", posición) o ("hueco", número de hueco)."""
    lo, hi = 0, len(A)          # invariante: si x está, está en A[lo:hi]
    while lo < hi:
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        elif x < A[m]:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)
```

### Correctitud parcial (invariante)

**Invariante.** *Si x está en el arreglo, está en A[lo:hi].* Es decir, el rango [lo, hi) contiene todas las posiciones donde x podría estar.

**Inicialización.** Antes de la primera vuelta, lo = 0 y hi = n. El rango A[0:n] es el arreglo entero, así que si x está, está en A[0:n]. 

**Mantenimiento.** Supongamos que el invariante vale antes de una vuelta, es decir, si x está, está en A[lo:hi]. Sea m = (lo+hi)//2. Hay tres casos:

- Si x == A[m], el algoritmo devuelve ("está", m) y no hay más vueltas. La postcondición se cumple.
- Si x < A[m], entonces x no puede estar en A[m:hi], porque todos los elementos de A[m:hi] son ≥ A[m] > x. Así que si x está, está en A[lo:m]. El algoritmo hace hi = m, y el nuevo rango es A[lo:m], que contiene a x si x está. 
- Si x > A[m], entonces x no puede estar en A[lo:m], porque todos los elementos de A[lo:m] son ≤ A[m] < x. Así que si x está, está en A[m+1:hi]. El algoritmo hace lo = m+1, y el nuevo rango es A[m+1:hi], que contiene a x si x está. 

**Conclusión.** Al terminar, lo = hi. El rango A[lo:hi] es vacío. Por el invariante, si x estuviera en el arreglo, estaría en un rango vacío, lo cual es imposible. Por lo tanto, x no está en el arreglo. El algoritmo devuelve ("hueco", lo), que es la posición donde x debería insertarse para mantener el orden. 

### Terminación (potencial)

**Potencial.** Φ = hi - lo, el tamaño del rango donde x todavía podría estar.

**Demostración.** Φ es un entero no negativo. En cada vuelta, el algoritmo reduce el rango:

- Si x == A[m], el algoritmo termina.
- Si x < A[m], el nuevo rango es [lo, m), y m < hi (porque m = (lo+hi)//2 < hi cuando lo < hi). Así que el nuevo Φ' = m - lo < hi - lo = Φ.
- Si x > A[m], el nuevo rango es [m+1, hi), y m+1 > lo (porque m ≥ lo). Así que el nuevo Φ' = hi - (m+1) < hi - lo = Φ.

En todos los casos, Φ baja estrictamente en cada vuelta (o el algoritmo termina). Como Φ es un entero no negativo, no puede bajar indefinidamente: el ciclo termina después de a lo sumo Φ₀ = n vueltas. De hecho, como el rango se parte por la mitad, termina en ⌈log₂(n+1)⌉ vueltas. 

### Costo

**Peor caso.** ⌈log₂(n+1)⌉ comparaciones. El rango se parte por la mitad en cada vuelta, así que después de k vueltas el rango tiene tamaño a lo sumo n/2^k. El ciclo termina cuando el rango tiene tamaño 0, lo que ocurre después de ⌈log₂(n+1)⌉ vueltas (el +1 viene de que hay n+1 huecos).

**Mejor caso.** 1 comparación, si x está en la posición media.

**Caso promedio.** Θ(log n) comparaciones, asumiendo que x está uniformemente distribuido entre los n+1 huecos.

**Memoria.** O(1) además de la entrada.

### Cota mínima (información)

**Modelo.** Modelo de comparaciones. El algoritmo solo puede comparar x con elementos del arreglo.

**Argumento de información, con el truco de los huecos.** Si x no está en el arreglo, cae en uno de los n+1 huecos: antes de a₁, entre a₁ y a₂, …, o después de aₙ. En esos casos ninguna comparación puede responder =, así que solo se usan dos ramas (< y >). El árbol de decisión restringido a los huecos es un árbol binario.

**Lema.** Si x₁ y x₂ caen en huecos distintos, un algoritmo correcto los lleva a hojas distintas.

**Demostración.** Supongamos que x₁ cae en un hueco a la izquierda del de x₂, y que los dos terminan en la misma hoja. Entre sus huecos hay al menos un elemento aᵢ, con x₁ < aᵢ < x₂. El algoritmo **no comparó con ese aᵢ**. Si lo hubiera hecho, x₁ habría recibido "<" y x₂ habría recibido ">", y habrían seguido caminos distintos. Ahora tomemos x = aᵢ. En cada comparación que el algoritmo hace, con un elemento a la izquierda de los dos huecos o a la derecha, aᵢ recibe la misma respuesta que x₁ y x₂. Así que x = aᵢ recorre el mismo camino y llega a la misma hoja. En esa hoja el algoritmo dice "no está", porque es la hoja de x₁. **Pero aᵢ sí está. El algoritmo se equivoca.** 

**Consecuencia.** Los n+1 huecos necesitan n+1 hojas distintas, en la parte del árbol que solo usa las ramas < y >, que es un árbol binario. Por el lema 1 de la Conferencia 5, un árbol binario de altura h tiene a lo sumo 2^h hojas. Para tener n+1 hojas, hace falta altura al menos ⌈log₂(n+1)⌉.

**La búsqueda binaria las alcanza.** Cada comparación parte por la mitad el rango donde todavía puede estar x, así que después de ⌈log₂(n+1)⌉ comparaciones queda un solo hueco. Con n = 7 hay ocho huecos, y la búsqueda binaria los separa con tres comparaciones, que es exactamente ⌈log₂8⌉ = 3. **Es óptima.**

### Código

La implementación instrumentada está en
[`codigos/ejercicio-02.py`](codigos/ejercicio-02.py).

Puntos clave del código:

- `busqueda_binaria_verificada(A, x)` es la búsqueda binaria con dos
  `assert` que verifican el invariante y el potencial en cada vuelta.
- El primer `assert` comprueba que si x está en A, su posición está en
  `A[lo:hi]`. Esto es el invariante.
- El segundo `assert` comprueba que `hi - lo` baja estrictamente en cada
  vuelta (salvo cuando el ciclo termina). Esto es el potencial.
- El programa corre siete casos de prueba (incluyendo arreglo vacío y
  valores fuera de rango) e imprime la tabla de resultados.

### Casos de prueba

| A                       | x   | Resultado    | Comparaciones |
| ----------------------- | --- | ------------ | ------------- |
| [1, 3, 5, 7, 9, 11, 13] | 7   | ("está", 3)  | 1 (m=3)       |
| [1, 3, 5, 7, 9, 11, 13] | 4   | ("hueco", 2) | 3             |
| [1, 3, 5, 7, 9, 11, 13] | 0   | ("hueco", 0) | 3             |
| [1, 3, 5, 7, 9, 11, 13] | 14  | ("hueco", 7) | 3             |
| [1]                     | 1   | ("está", 0)  | 1             |
| [1]                     | 0   | ("hueco", 0) | 1             |
| []                      | 5   | ("hueco", 0) | 0             |

**Verificación del invariante.** Para A = [1, 3, 5, 7, 9, 11, 13], x = 4:

- Inicio: lo=0, hi=7, rango [0,7). x=4 podría estar en cualquier posición.
- m=3, A[3]=7. 4 < 7, así que hi=3. Rango [0,3). x=4 podría estar en [0,3).
- m=1, A[1]=3. 4 > 3, así que lo=2. Rango [2,3). x=4 podría estar en [2,3).
- m=2, A[2]=5. 4 < 5, así que hi=2. Rango [2,2), vacío. x=4 no está.
- Devuelve ("hueco", 2), que es la posición donde 4 debería insertarse. 

**Figura 1.** Árbol de decisión de la búsqueda binaria para n = 7. Las 8 hojas corresponden a los 8 huecos. La altura es 3 = ⌊log₂ 8⌋, que es la cota del lema 4.
```mermaid
graph TD
    A4["x < a4"] -->|sí| A2["x < a2"]
    A4 -->|no| A6["x < a6"]
    A2 -->|sí| A1["x < a1"]
    A2 -->|no| A3["x < a3"]
    A6 -->|sí| A5["x < a5"]
    A6 -->|no| A7["x < a7"]
    A1 -->|sí| h0["h0"]
    A1 -->|no| h1["h1"]
    A3 -->|sí| h2["h2"]
    A3 -->|no| h3["h3"]
    A5 -->|sí| h4["h4"]
    A5 -->|no| h5["h5"]
    A7 -->|sí| h6["h6"]
    A7 -->|no| h7["h7"]
```

### Conclusión

La búsqueda binaria es **óptima en el modelo de comparaciones**: hace ⌈log₂(n+1)⌉ comparaciones en el peor caso, que es exactamente la cota de información. El invariante "si x está, está en A[lo:hi]" da la correctitud parcial, y el potencial Φ = hi - lo da la terminación y acota el número de vueltas.
