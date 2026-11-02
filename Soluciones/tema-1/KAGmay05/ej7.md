## Problema 7
Mediana de dos arreglos ordenados de largo n: el n-ésimo menor de los 2n elementos. Diseña un algoritmo O(logn), demuestra su correctitud y da la cota de información. 

### Respuesta

Lo primero que pensé fue tomar el mayor de los dos primeros elementos (digamos que es B[0]) siendo una lista B y la otra A, y compararlo con el último de la otra lista, A[n−1]. Si B[0] ≥ A[n−1], todo A va antes que todo B, porque A tiene n elementos y si su elemento número n es menor q el menor de la otra lista entonces los n menores son justo los de A y la respuesta es A[n−1]. Si no, descarto ese par y comparo B[1] con A[n−2], después B[2] con A[n−3], y así.

Los problemas con esa solución:

- Es O(n), no O(log n). En el peor caso hago n comparaciones, por ejemplo con A = [1, 6, 7, 8] y B = [2, 3, 4, 5].
- Cuando paro después de haber avanzado, la respuesta no es siempre el elemento de A del par. Con A = [1, 2, 4] y B = [3, 10, 11] paro en el par (10, 2), pero la respuesta es 3.

Ideas importantes de la solución:

- Los n menores siempre son los primeros i elementos de una lista más los primeros n − i de la otra, para algún i entre 0 y n. O sea que en el fondo no busco un elemento, busco un número: cuánto se toma de cada lista.
- En la comparación de pares B[i] ≥ A[n−1−i], una vez que se cumple se sigue cumpliendo, porque al aumentar i B[i] sube y A[n−1−i] baja. Entonces hay una zona de "no" y después una zona de "sí". Eso es justo lo que permite hacer búsqueda binaria en vez de recorrer uno por uno.

### Pasar a búsqueda binaria comparando los medios

En lugar de ir par por par, comparé el medio de A con el medio de B. Si el medio de A es el menor, la primera mitad de A es demasiado pequeña para ser la respuesta y la segunda mitad de B es demasiado grande. Puedo tirar las dos y seguir con lo que queda.

Detalles a tener en cuenta:

- Hay que tirar la misma cantidad de las dos listas. Si no, el elemento que busco cambia de posición en lo que queda.
- Con n par hay dos medios. Si uso el de arriba, con n = 2 no puedo tirar nada y me quedo atascado. Con el de abajo funciona, pero hay que tirar el medio menor y conservar el mayor, porque el mayor puede ser la respuesta. Por ejemplo, con A = [1, 4] y B = [2, 5] la respuesta es 2, que es el medio de B.
- Cuando queda un elemento en cada lista, la respuesta es el menor de los dos. Ese es el caso base.

---

## 2. La invariante

Lo que se mantiene en cada paso es esto: lo que me queda de cada lista tiene el mismo tamaño (lo llamo m), la respuesta sigue estando ahí dentro, y además es el m-ésimo menor de lo que queda. Funciona porque en cada paso tiro la misma cantidad por debajo de la respuesta que por encima, así que "el del medio" sigue siendo el del medio.

Dicho con los índices del código, al empezar cada vuelta del bucle:

> Las ventanas A[a … a+m−1] y B[b … b+m−1] tienen m elementos cada una, y el n-ésimo menor de A ∪ B es el m-ésimo menor de esas dos ventanas juntas.

---

## 3. Solución

### Algoritmo

Llamo A' y B' a las ventanas actuales, de tamaño m. En cada paso:

1. Calculo k = ⌊m/2⌋, que es cuántos elementos tiro de cada lista, y p = ⌊(m−1)/2⌋, que es la posición del medio de abajo.
2. Comparo A'[p] con B'[p].
3. De la ventana con el medio menor tiro los primeros k, y de la otra los últimos k.
4. El tamaño pasa a m − k = ⌈m/2⌉.
5. Cuando m = 1, devuelvo el menor de los dos elementos que quedan.

Para no copiar listas, que costaría O(n), guardo solo dónde empieza cada ventana (a, b) y su tamaño m. Tirar los primeros k es mover el inicio. Tirar los últimos k es achicar m. Al hacer m -= k, la ventana a la que le moví el inicio conserva su final, y la otra pierde sus últimos k.

```python
def n_esimo_menor(A, B):
    n = len(A)
    a, b, m = 0, 0, n           # ventanas A[a..a+m-1] y B[b..b+m-1]
    while m > 1:
        k = m // 2              # cuántos tiro de cada lista
        p = (m - 1) // 2        # medio de abajo
        if A[a + p] <= B[b + p]:
            a += k              # tiro los primeros k de A
        else:
            b += k              # tiro los primeros k de B
        m -= k                  # y los últimos k de la otra
    return min(A[a], B[b])
```

### Corrección

Uso dos identidades que salen de la definición de k y p:

- k + p = m − 1, o lo que es lo mismo, p + 1 = m − k.
- m − k = ⌈m/2⌉.

Lema 1 (contar). Con 2m elementos distintos, el m-ésimo menor tiene exactamente m − 1 elementos menores y m mayores. Por lo tanto:

- si un elemento tiene al menos m + 1 mayores, está por debajo de la respuesta;
- si un elemento tiene al menos m menores, está por encima de la respuesta.

Lema 2 (qué se puede tirar). Sean A' y B' las ventanas, de tamaño m ≥ 2, y supongamos A'[p] < B'[p]. Entonces:

(a) Los primeros k de A' están por debajo de la respuesta. Tomo i ≤ k − 1. Como 2k ≤ m, se cumple i ≤ p. Son mayores que A'[i]:

- A'[i+1 … m−1], que son m − 1 − i ≥ m − k elementos;
- B'[p … m−1], que son m − p = k + 1 elementos, porque B'[j] ≥ B'[p] > A'[p] ≥ A'[i].

En total tiene al menos (m − k) + (k + 1) = m + 1 mayores. Por el Lema 1, está por debajo.

(b) Los últimos k de B' están por encima de la respuesta. Tomo j ≥ m − k = p + 1, así que j > p. Son menores que B'[j]:

- B'[0 … j−1], que son j ≥ m − k elementos;
- A'[0 … p], que son p + 1 = m − k elementos, porque A'[i] ≤ A'[p] < B'[p] ≤ B'[j].

En total tiene al menos 2(m − k) = 2⌈m/2⌉ ≥ m menores. Por el Lema 1, está por encima.

Si B'[p] < A'[p], el argumento es el mismo cambiando los papeles de A' y B'.

La invariante se cumple:

- Inicio. Con a = b = 0 y m = n, las ventanas son las listas enteras y busco el n-ésimo menor.
- Mantenimiento. Por el Lema 2, tiro k elementos que están por debajo de la respuesta y k que están por encima. Quedan dos ventanas de m − k elementos. Como tiré k por debajo, la respuesta pasa de ser la m-ésima a ser la (m − k)-ésima, que es justo el nuevo tamaño.
- Terminación. Dentro del bucle m ≥ 2, así que k ≥ 1 y m baja en cada vuelta. Al salir, m = 1 y la respuesta es el menor de los dos elementos, es decir, el menor entre A[a] y B[b].

### Complejidad

Cada vuelta hace O(1) operaciones y m pasa a ⌈m/2⌉, así que hay ⌈log₂ n⌉ vueltas. El tiempo es O(log n) y la memoria extra es O(1), porque no se copian listas.

Contando solo comparaciones entre elementos: una por vuelta (A[a+p] con B[b+p]) y una más en el min del final, en total ⌈log₂ n⌉ + 1.



## 4. Cota de información

Modelo: el algoritmo solo obtiene información comparando elementos de A y B entre sí, y tiene que decir cuál de los 2n elementos es el n-ésimo menor. Como en la conferencia 5, todas sus ejecuciones forman un árbol de decisión: cada nodo interno es una comparación y cada hoja devuelve una posición (algún A[j] o B[j]). El peor caso es la altura h del árbol.

### Cualquiera de los 2n elementos puede ser la respuesta

Para que A[j] sea el n-ésimo menor tiene que tener exactamente n − 1 elementos por debajo: los j de A[0 … j−1] y n − 1 − j de B. Una entrada que lo cumple, para 0 ≤ j ≤ n − 1:

- B[0 … n−2−j] = 1, 2, …, n−1−j
- A[0 … n−1] = n−j, …, 2n−1−j
- B[n−1−j … n−1] = 2n−j, …, 2n

Las dos listas están ordenadas, los 2n valores son distintos y A[j] = n. Por debajo de n quedan exactamente los valores 1, …, n−1, así que A[j] es el n-ésimo menor. Cambiando los papeles de A y B sale una entrada donde la respuesta es B[j].

Por ejemplo, con n = 3 y j = 1: A = [2, 3, 4] y B = [1, 5, 6]. Los 3 menores son 1, 2, 3 y la respuesta es A[1] = 3.

Así tengo 2n entradas, cada una con una respuesta distinta.

### Necesitan 2n hojas distintas

Una hoja siempre devuelve la misma posición, así que dos entradas con respuestas distintas no pueden terminar en la misma hoja. El árbol tiene al menos 2n hojas.

Además, en estas entradas todos los valores son distintos, así que ninguna comparación responde "=" y solo se usan dos ramas, como en los huecos de la búsqueda binaria. Por el lema 1 de la conferencia 5, un árbol binario de altura h tiene a lo sumo 2^h hojas:

2^h ≥ 2n  ⟹  h ≥ log₂(2n) = log₂ n + 1.

Como h es entero, h ≥ ⌈log₂ n⌉ + 1. Todo algoritmo de comparaciones necesita al menos ⌈log₂ n⌉ + 1 comparaciones en el peor caso, o sea Ω(log n).

### El algoritmo es óptimo

El algoritmo de la sección 3 hace exactamente ⌈log₂ n⌉ + 1 comparaciones, que es la cota. No solo es óptimo en O(log n): también lo es en la constante, igual que la búsqueda binaria.


