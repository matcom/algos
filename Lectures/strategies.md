# Estrategias de Diseño de Algoritmos

- Constructiva
  - Ad-hoc
  - Greedy
  - Recursiva
    - Divide & Conquer
    - Backtrack
    - Programación dinámica
- Búsqueda
  - Exacta
    - Exhaustiva
    - Binaria
    - Hash
  - Heurística
    - Branch & X
    - Path-finding
    - Local
    - Metaheurística

Muchos problemas se pueden ver de diferentes formas.

## Algoritmos Constructivos

Donde el problema consiste en dado un input, construir un objeto que cumple con ciertas propiedades, optimizando cierto criterio.

De manera general la solución se "construye" tomando decisiones, y se quiere obtener la solución óptima con respecto a cierto criterio.
Por lo tanto, hay que tomar las decisiones locales de forma que la solución global sea óptima.

### Ad-hoc

Explotar características propias del problema.

Ej: Bubble-Sort

### Greedy

Tomar siempre la mejor decisión local, para que sea correcto debe haber subestructura óptima.

Ej: Cambio de monedas, Djikstra, Linear Scheduling.

Forma de resolver:

- Encuentra un formulación recursiva del problema
- Define la decisión greedy
- Demuestra que luego de la decisión greedy, solo hay subproblema que resolver
- Demuestra que la decisión greedy es óptima
- Convierte la formulación recursiva en iterativa

Para que el greedy funcione hay que demostrar que la mejor solución local es mejor global.
Para ello se escoge una solución óptima, y se demuestra que cambiando una decisión por la decisión local óptima, esta no empeora.

### Recursiva

Dividir el problema en subproblemas, tal que la solución del problema general se construye a partir de las soluciones a los subproblemas.
La solución más general es backtrack.

#### Backtrack

Construir de forma exhaustiva todas las posibles soluciones. No hay subestructura óptima.

#### Divide & Conquer

Dividir en subproblemas disjuntos. Resolver cada subproblema de forma óptima, y mezclar las soluciones. Debe haber subestructura óptima.

Ej típico: ordenación (cada subarray debe estar ordenado)
Otro ejemplo: subsecuencia de suma máxima

#### Programación dinámica

Dividir en subproblemas no necesariamente disjuntos, pero donde hay subestructura óptima y problemas independientes.

Ej: Fibonacci y compañia, Matrix-Chain, Cut-Rod.

Dos formas de resolver:

- Memoization (top-down): La forma más fácil, se convierte un algoritmo recursivo directamente en dinámico.
- Bottom-up: Requiere ordenar los subproblemas por algún criterio de "tamaño" de forma que todos los problemas dependan solo de problemas "menores".

El costo dependerá de la cantidad de subproblemas, y del costo de resolver cada subproblema.

### Análisis

#### Cómo saber que hay subestructura óptima?

- Dividir el problema asumiendo que la solución general es óptima
- Asumir que uno de los subproblemas no tiene la solución óptima
- Cambiar el subproblema por la solución óptima
- Llegar a una contradicción mejorando la solución general

#### Cómo saber si hay subproblemas independientes?

- Qué la solución óptima a uno de los subproblemas no implique que la solución óptima a otro subproblema deba cambiar (p.ej. shortest-path vs longest simple path).

#### Greedy vs Dinámica

0-1 Knapsack vs Fraction Knapsack

## Algoritmos de búsqueda

Cuando el problema consiste en encontrar un elemento con ciertas propiedades (o minimizando cierto criterio) en un conjunto de elementos.

### Búsqueda exhaustiva

Analizar todos los elementos. No hay mucho que comentar aquí.

### Búsqueda binaria

Cuando existe algún criterio que permita particionar el espacio de búsqueda en dos subespacios A y B, de forma que se pueda garantizar que solo hay que buscar en A, y |A| es O(|B|).

Ej: binary search en arrays

"Demostrar" que no hay solución mejor.
Ver conexión con ordenación.

```python
def binary_search(A, n, T):
    L = 0
    R = n − 1
    while L ≤ R
        m = floor((L + R) / 2)
        if A[m] < T then
            L = m + 1
        else if A[m] > T then
            R = m − 1
        else:
            return m
    return None
```

Solución alternativa:

```python
def binary_search_alternative(A, n, T):
    L = 0
    R = n − 1
    while L != R do
        m = ceil((L + R) / 2)
        if A[m] > T then
            R = m − 1
        else:
            L = m
    if A[L] = T then
        return L
    return None
```

```python
def binary_search_leftmost(A, n, T):
    L := 0
    R := n - 1
    while L < R:
        m := floor((L + R) / 2)
        if A[m] < T:
            L := m + 1
        else:
            R := m
    return L
```

```python
def binary_search_rightmost(A, n, T):
    L := 0
    R := n
    while L < R:
        m := floor((L + R) / 2)
        if A[m] > T:
            R := m
        else:
            L := m + 1
    return R - 1
```