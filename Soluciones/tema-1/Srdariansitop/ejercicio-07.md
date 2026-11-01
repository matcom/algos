# Pregunta 7
Mediana de dos arreglos ordenados de largo n: el -ésimo menor de los 2n elementos. Diseña un algoritmo O(log n) , demuestra su correctitud y da la cota de información.

**Convención.** Sean A[1..n] y B[1..n] ordenados de forma creciente. Buscamos el n‑ésimo menor de los 2n elementos. Suponemos **elementos distintos**. Si hay repetidos, se reemplaza cada elemento por la tupla (valor, id del arreglo, índice) con orden lexicográfico. Eso los hace distintos, conserva el orden de cada arreglo y no cambia el valor de la mediana.

---

## Sección 1: Entender el problema y proponer el algoritmo

### Reformular: la mediana es un "corte"

Pensemos en el arreglo mezclado y ordenado de 2n elementos. La mediana es el elemento en la posición n. A su izquierda quedan los n elementos más pequeños (el conjunto L) y a su derecha los otros n (el conjunto R).

La observación clave es que **L está formado por un prefijo de A y un prefijo de B**. Si un elemento de A está entre los n menores, todos los anteriores de A también lo están, porque son más pequeños. Lo mismo vale para B.

Entonces basta decidir **cuántos elementos de A hay en L**. Llamemos i a ese número, con i ∈ {0,…,n}. Como L tiene n elementos, de B tomamos j = n − i. Así:

- L = A[1..i] ∪ B[1..j], con j = n − i
- R = A[i+1..n] ∪ B[j+1..n]

El problema pasa de "buscar entre 2n elementos" a "buscar un entero i entre 0 y n", y eso se puede hacer con búsqueda binaria.

### ¿Cuándo un corte i es el correcto?

Usamos centinelas A[0] = B[0] = −∞ y A[n+1] = B[n+1] = +∞, para no tratar casos borde por separado.

Un corte i es correcto si todo elemento de L es menor que todo elemento de R. Comparando los máximos de cada prefijo con los mínimos de cada sufijo, hay cuatro desigualdades:

| Comparación | ¿Se cumple siempre? |
|---|---|
| A[i] < A[i+1] | Sí, A está ordenado |
| B[j] < B[j+1] | Sí, B está ordenado |
| **A[i] < B[j+1]** (C1) | No, hay que verificarla |
| **B[j] < A[i+1]** (C2) | No, hay que verificarla |

Entonces el corte i es correcto ⟺ se cumplen **C1 y C2**. En ese caso la mediana es **max(A[i], B[n−i])**, que es el mayor elemento de L.

### Monotonía: lo que permite la búsqueda binaria

Definimos para i ∈ {0,…,n} el predicado

  **g(i) ≡ A[i+1] > B[n−i]**

Cuando i crece:
- A[i+1] **sube**, porque A está ordenado creciente.
- B[n−i] **baja**, porque su índice disminuye.

Por lo tanto, si g(i) es verdadero, g(i+1) también lo es. La secuencia g(0), g(1), …, g(n) tiene la forma FALSO…FALSO VERDADERO…VERDADERO. Además g(n) es siempre verdadero, ya que A[n+1] = +∞ > B[0] = −∞.

Sea **i\* = el menor i con g(i) verdadero**. Veremos en la Sección 2 que i\* es exactamente el corte correcto.

Intuición de la decisión en cada paso. Probamos un i:
- Si g(i) es verdadero, A[i+1] es demasiado grande para estar en L. Ya tomamos demasiados elementos de A (o justo los necesarios), así que i\* ≤ i y bajamos el extremo superior.
- Si g(i) es falso, A[i+1] < B[n−i], así que A[i+1] debe estar en L y necesitamos más elementos de A. Entonces i\* > i y subimos el extremo inferior.

### El algoritmo

```
MEDIANA(A[1..n], B[1..n]):
    lo ← 0 ; hi ← n
    mientras lo < hi:
        i ← ⌊(lo + hi) / 2⌋
        si A[i+1] > B[n−i]:      // g(i) verdadero
            hi ← i
        sino:
            lo ← i + 1
    i ← lo
    devolver max(A[i], B[n−i])   // con A[0] = B[0] = −∞
```

Dentro del bucle, i < hi ≤ n, por lo que i+1 ≤ n y n−i ≥ 1. Los índices son siempre válidos y no hacen falta centinelas dentro del ciclo. Solo se usan al final, cuando i = 0 o i = n.

### Ejemplo completo

A = [1, 3, 5, 7], B = [2, 4, 6, 8], n = 4. El arreglo mezclado es 1,2,3,4,5,6,7,8, y la mediana (4.º menor) es **4**.

| Iteración | lo | hi | i | A[i+1] vs B[4−i] | Decisión |
|---|---|---|---|---|---|
| 1 | 0 | 4 | 2 | A[3]=5 > B[2]=4 ✔ | hi = 2 |
| 2 | 0 | 2 | 1 | A[2]=3 > B[3]=6 ✘ | lo = 2 |
| fin | 2 | 2 | | | |

Con i = 2 y j = 2, L = {1,3} ∪ {2,4} = {1,2,3,4} y la mediana es max(A[2], B[2]) = max(3,4) = **4** ✓.

### Complejidad

Cada iteración usa una comparación y trabajo O(1). El intervalo [lo, hi] tiene m = hi − lo + 1 candidatos y tras cada iteración queda con a lo sumo ⌈m/2⌉:

- Si hi ← i, quedan ⌊(m−1)/2⌋ + 1 = ⌈m/2⌉ candidatos.
- Si lo ← i+1, quedan ⌊m/2⌋ candidatos.

Se empieza con m = n+1, así que hay a lo sumo **⌈log₂(n+1)⌉ iteraciones**. Con la comparación final del max, el total es **⌈log₂(n+1)⌉ + 1 comparaciones y tiempo O(log n)**.

---

## Sección 2: Demostración formal de correctitud

Se prueban tres cosas: (a) i\* existe, (b) el corte i\* cumple C1 y C2, y (c) un corte que cumple C1 y C2 produce la mediana. Luego se muestra que el algoritmo encuentra i\*.

### Lema (monotonía y existencia de i\*)

*Enunciado.* Para i ∈ {0,…,n}, g(i) ≡ A[i+1] > B[n−i] es monótona (g(i) ⟹ g(i+1) para i < n) y g(n) es verdadero. Por lo tanto existe i\* = min{ i : g(i) }.

*Prueba.* Sea g(i) verdadero con i < n. Como A es creciente, A[i+2] > A[i+1]. Como B es creciente, B[n−i−1] < B[n−i]. Entonces
 A[i+2] > A[i+1] > B[n−i] > B[n−i−1],
que es g(i+1). Además g(n) ≡ A[n+1] > B[0] ≡ +∞ > −∞, que es verdadero. El conjunto {i : g(i)} es no vacío y está acotado inferiormente por 0, así que tiene mínimo. ∎

### Lema (el corte i\* satisface C1 y C2)

*Enunciado.* Sea j\* = n − i\*. Entonces A[i\*] < B[j\*+1] (C1) y B[j\*] < A[i\*+1] (C2).

*Prueba.*
- **C2.** Es exactamente g(i\*), que es verdadero: A[i\*+1] > B[n−i\*] = B[j\*].
- **C1.** Hay dos casos.
  - *i\* = 0.* Entonces A[0] = −∞ < B[n+1] = +∞, y se cumple.
  - *i\* > 0.* Por minimalidad, g(i\*−1) es falso: no se cumple A[i\*] > B[n−i\*+1]. Como los elementos son distintos, vale A[i\*] < B[n−i\*+1] = B[j\*+1]. ∎

### Lema (un corte que cumple C1 y C2 da la mediana)

*Enunciado.* Si i cumple C1 y C2 (con j = n − i), entonces L = A[1..i] ∪ B[1..j] es el conjunto de los n menores elementos de A ∪ B, y el n‑ésimo menor es max(A[i], B[j]).

*Prueba.* |L| = i + j = n y |R| = 2n − n = n. Probamos que todo x ∈ L es menor que todo y ∈ R, tomando cuatro casos:

1. x ∈ A[1..i], y ∈ A[i+1..n]: x ≤ A[i] < A[i+1] ≤ y, por orden de A.
2. x ∈ B[1..j], y ∈ B[j+1..n]: análogo, por orden de B.
3. x ∈ A[1..i], y ∈ B[j+1..n]: x ≤ A[i] < B[j+1] ≤ y, por C1.
4. x ∈ B[1..j], y ∈ A[i+1..n]: x ≤ B[j] < A[i+1] ≤ y, por C2.

Como L tiene n elementos y todos son menores que los n de R, L son exactamente los n menores. El n‑ésimo menor es el mayor de L, que es max(A[i], B[j]), porque los mayores de cada prefijo son A[i] y B[j] (con −∞ si el prefijo es vacío; no pueden ser ambos vacíos porque i + j = n ≥ 1). ∎

### Lema (invariante del bucle)

*Enunciado.* En cada evaluación de la condición lo < hi se cumple **lo ≤ i\* ≤ hi**.

*Prueba por inducción.*

- *Base.* Inicialmente lo = 0, hi = n, e i\* ∈ {0,…,n} por el lema de monotonía y existencia de i\*.
- *Paso.* Suponemos lo ≤ i\* ≤ hi y lo < hi. Sea i = ⌊(lo+hi)/2⌋, de modo que lo ≤ i < hi.
  - *Si g(i) es verdadero.* Por definición de mínimo, i\* ≤ i. El algoritmo hace hi ← i y sigue valiendo lo ≤ i\* ≤ hi.
  - *Si g(i) es falso.* Por monotonía (véase el lema de monotonía y existencia de i\*), g(k) es falso para todo k ≤ i, así que i\* > i, es decir i\* ≥ i+1. El algoritmo hace lo ← i+1 y sigue valiendo lo ≤ i\* ≤ hi. ∎

### Teorema (correctitud)

*El algoritmo termina y devuelve el n‑ésimo menor de A ∪ B.*

*Prueba.*

- **Terminación.** En cada iteración hi − lo disminuye estrictamente: la longitud pasa de hi − lo a i − lo < hi − lo, o a hi − (i+1) < hi − lo. Es un entero no negativo, así que el bucle termina. (La cota de ⌈log₂(n+1)⌉ iteraciones se vio en la subsección de complejidad.)
- **Valor devuelto.** Al salir, lo ≥ hi. Con el lema del invariante del bucle, lo ≤ i\* ≤ hi, luego lo = hi = i\*. El algoritmo devuelve max(A[i\*], B[n−i\*]). Por el lema del corte i\*, i\* cumple C1 y C2, y por el lema del corte que da la mediana ese valor es el n‑ésimo menor de los 2n elementos. ∎

**Nota sobre los índices.** Mientras lo < hi, se tiene 0 ≤ i < n. Así, A[i+1] y B[n−i] son accesos válidos (1 ≤ i+1 ≤ n y 1 ≤ n−i ≤ n). Los centinelas solo aparecen al final, y están definidos allí.

---

## Sección 3: Cota de información

### Modelo

Trabajamos en el **modelo de comparaciones**: el algoritmo solo obtiene información sobre los datos comparando pares de elementos (x < y, con respuesta sí o no). Cualquier algoritmo determinista de este tipo se puede representar como un **árbol de decisión binario**:

- cada nodo interno es una comparación,
- cada hijo corresponde a una respuesta (sí/no),
- cada hoja es una respuesta final del algoritmo.

El número de comparaciones en el peor caso es la **altura** del árbol.

### La idea: contar respuestas posibles

La idea es contar los resultados posibles que el algoritmo debe distinguir. Cada comparación entrega a lo sumo 1 bit, así que para distinguir R resultados hacen falta al menos log₂ R comparaciones.

**Afirmación:** la respuesta "¿qué elemento es la mediana?" puede ser cualquiera de los 2n elementos.

- *A[k] puede ser la mediana (1 ≤ k ≤ n).* Para que A[k] sea el n‑ésimo menor, necesitamos que n − k elementos de B sean menores que él y los otros k elementos de B mayores. Como 0 ≤ n−k ≤ n−1, es posible. Basta construir una entrada con B[1..n−k] < A[k] < B[n−k+1..n], por ejemplo con enteros alejados entre sí. Además, A[k] tiene k−1 elementos menores en A, de modo que su posición total es (k−1) + (n−k) + 1 = n ✓.
- *B[k] puede ser la mediana.* Se obtiene por simetría intercambiando los papeles de A y B.

### La cota

Un algoritmo correcto debe devolver, para cada una de esas 2n posibilidades, el elemento correcto. Como entradas distintas pueden tener respuestas distintas, el árbol de decisión necesita **al menos una hoja por cada respuesta posible**: al menos 2n hojas.

Un árbol binario de altura h tiene a lo sumo 2^h hojas. Entonces

  2^h ≥ 2n  ⟹  **h ≥ ⌈log₂(2n)⌉ = 1 + ⌈log₂ n⌉ = Ω(log n)**.

Es decir, **todo algoritmo basado en comparaciones necesita Ω(log n) comparaciones en el peor caso**.

### Comparación con nuestro algoritmo

| | Comparaciones en el peor caso |
|---|---|
| Cota inferior (información) | ⌈log₂ n⌉ + 1 |
| Nuestro algoritmo | ⌈log₂(n+1)⌉ + 1 |

La diferencia entre ambas es a lo sumo 1 comparación. Es 0 salvo cuando n es potencia de 2, donde vale 1. Por lo tanto el algoritmo es **óptimo**: Θ(log n) comparaciones, y asintóticamente no se puede mejorar.

### Una interpretación complementaria

Otra forma de ver la cota es mirar el "parámetro oculto" que el algoritmo debe descubrir. Es el corte i\* ∈ {0,…,n}, es decir **n+1 posibilidades**. Con cada comparación de la búsqueda binaria el conjunto de candidatos se reduce a la mitad, y esa es la mejor reducción posible por comparación. De ahí viene el ⌈log₂(n+1)⌉ del algoritmo. La comparación extra, max(A[i], B[n−i]), cubre el último bit, que decide entre los dos candidatos A[i\*] y B[n−i\*], y eso explica el "+1" en ambas columnas de la tabla.

**Por qué no se puede hacer en tiempo sublogarítmico:** además de lo anterior, ni siquiera se puede "leer" una fracción sustancial de la entrada, porque el tiempo sería Ω(n). El argumento del árbol de decisión muestra que log n es el piso, y la búsqueda binaria sobre i lo alcanza.

## Código(Extra 07)

**`s1_corte.png` (función `s1_corte`).** Usa A = [1,2,3,4,10,12] y B = [5,6,7,8,9,11] con n = 6. Dibuja ambos arreglos con el prefijo en azul (L) y el sufijo en naranja (R), con una línea gruesa en el corte i = 4, j = n − i = 2. Debajo muestra la mezcla ordenada, con la mediana (6) resaltada en dorado. Así se ve que la mediana es un corte: L está formado por un prefijo de A y un prefijo de B.

**`s1_busqueda.gif` (función `s1_busqueda`).** Corre `trace` sobre dos arreglos con n = 8 y arma una secuencia de cuadros. Por cada iteración hay dos cuadros. En el primero se muestra el valor de i probado, el corte correspondiente y los dos elementos a comparar. En el segundo se muestra el resultado de `A[i+1] > B[n−i]` y cómo cambia lo o hi. La franja superior marca en amarillo los valores de i que siguen siendo candidatos. El último cuadro muestra i\* y la mediana.

**`s1_monotonia.png` (función `s1_monotonia`).** Grafica A[i+1] (sube) y B[n−i] (baja) en función de i. El punto donde se cruzan separa la zona roja (g falso) de la verde (g verdadero). Debajo hay una fila de casillas F…F V…V con el primer V marcado como i\*. Muestra por qué g es monótona y por qué se puede aplicar búsqueda binaria.

**`s2_cuatro_casos.png` (función `s2_cuatro_casos`).** Dibuja los arreglos con el corte (i = 4, j = 2) y cuatro flechas de colores sobre ellos: A[i] < A[i+1], B[j] < B[j+1], C1: A[i] < B[j+1] y C2: B[j] < A[i+1]. A la derecha hay un cuadro por cada caso con su desigualdad. Ilustra la prueba del Lema 3: los cuatro casos cubren todos los pares (x ∈ L, y ∈ R), así que L son los n menores.

**`s2_invariante.gif` (función `s2_invariante`).** Usa n = 16 con arreglos aleatorios (semilla fija) y una fila de casillas que representan g(0..n), todas con "?" al inicio. Una ventana azul marca [lo, hi]. En cada paso se prueba un i y se revela g(i). Luego, por monotonía, se rellenan todas las casillas hacia la izquierda con F, o hacia la derecha con V, y la ventana se achica. Debajo se muestra la desigualdad `lo ≤ i* ≤ hi` con sus valores y el motivo del cambio. Es la demostración del Lema 4, hecha visible.

**`s3_arbol_decision.png` (función `s3_arbol`).** Construye con coordenadas manuales un árbol binario de decisión de altura 3 con 2n = 8 hojas (A1…A4, B1…B4). Cada nodo interno es una comparación con ramas "sí" y "no". Un camino en rojo lleva hasta la hoja B3. Debajo aparece la cuenta: 2^h ≥ 2n implica h ≥ log₂(2n) = Ω(log n).

**`s3_cota_informacion.gif` (función `s3_cota`).** Muestra 16 casillas (A1…A8, B1…B8), una por cada candidato a mediana. Cada cuadro simula una comparación que descarta la mitad de los candidatos que quedan (16 → 8 → 4 → 2 → 1), mostrando cuántos bits faltan. Al final queda un solo candidato tras log₂(16) = 4 comparaciones, lo que explica por qué ningún algoritmo puede hacerlo en menos.

