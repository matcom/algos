# Ejercicio 14 — El pico de un arreglo unimodal

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2
> y consigue que el algoritmo y la cota mínima coincidan.

## 1. Problema y modelo

**Entrada:** un arreglo no vacío $A[0..n-1]$ que primero crece estrictamente y luego
decrece estrictamente. Su pico es el índice $p$ tal que
$$A[0]<A[1]<\cdots<A[p]>\cdots>A[n-1].$$
Si el arreglo es monótono, el pico puede ser el primer o el último índice.

**Salida:** el índice del pico. Medimos comparaciones entre elementos de $A$.

Este problema no aparece en las conferencias del Tema 1 revisadas para esta solución.

## 2. Algoritmo

Comparamos dos elementos vecinos en el punto medio. Si el de la derecha es mayor, el
pico queda a la derecha; en otro caso, queda en el punto medio o a su izquierda.

~~~python
def pico(A):
    if not A:
        raise ValueError("el arreglo no puede estar vacío")
    lo, hi = 0, len(A) - 1
    comparaciones = 0
    while lo < hi:
        m = (lo + hi) // 2
        comparaciones += 1
        if A[m] < A[m + 1]:
            lo = m + 1
        else:
            hi = m
    return lo, comparaciones

if __name__ == "__main__":
    for A in ([1, 4, 9, 7, 2], [8, 5, 1], [1, 3, 6]):
        i, c = pico(A)
        print(f"A={list(A)}, pico en índice {i}, valor {A[i]}, comparaciones={c}")
~~~

~~~
A=[1, 4, 9, 7, 2], pico en índice 2, valor 9, comparaciones=2
A=[8, 5, 1], pico en índice 0, valor 8, comparaciones=2
A=[1, 3, 6], pico en índice 2, valor 6, comparaciones=1
~~~

## 3. Correctitud — guía para redactar la prueba (pendiente)

La prueba debes escribirla tú.

- Formula el invariante sobre el intervalo $[lo,hi]$: ¿qué sabes del pico antes de cada
  comparación?
- Si $A[m]<A[m+1]$, ¿por qué el pico no puede estar en $m$ ni a su izquierda?
- Si $A[m]>A[m+1]$, ¿por qué el pico no puede estar a la derecha de $m$?
- ¿Qué ocurre cuando el intervalo tiene un solo índice?

## 4. Costo

Cada vuelta hace una comparación y reduce el intervalo al menos a la mitad. El algoritmo
usa $O(\log n)$ comparaciones y $O(1)$ memoria adicional.

~~~python
import math

def pico_con_cuenta(A):
    i, comparaciones = pico(A)
    return i, comparaciones

casos = 0
max_comparaciones = 0
for n in range(1, 129):
    for p in range(n):
        izquierda = list(range(p + 1))
        derecha = list(range(p - 1, p - 1 - (n - p - 1), -1))
        A = izquierda + derecha
        i, c = pico_con_cuenta(A)
        assert i == p
        assert c <= math.ceil(math.log2(n)) if n > 1 else c == 0
        casos += 1
        max_comparaciones = max(max_comparaciones, c)
print(f"{casos} picos probados; máximo {max_comparaciones} comparaciones")
~~~

~~~
8256 picos probados; máximo 7 comparaciones
~~~

## 5. Cota mínima — guía para redactar el argumento (pendiente)

Redacta tú la cota de información en el modelo de comparaciones:

1. Para cada índice $p\in\{0,\dots,n-1\}$, construye un arreglo unimodal cuyo pico esté
   exactamente en $p$. ¿Cuántas respuestas posibles debe distinguir un algoritmo?
2. ¿Cuántos resultados puede tener una comparación? Usa el número de hojas que necesita
   el árbol y su altura mínima para obtener una cota en función de $n$.
3. Compara esa cota con el costo del algoritmo y concluye en qué sentido es óptimo.

## 6. Ciclo completo

| pregunta | respuesta |
|---|---|
| ¿Qué problema? | Encontrar el índice del pico en un arreglo estrictamente unimodal |
| ¿Qué algoritmo? | Búsqueda binaria sobre comparaciones de vecinos |
| ¿Es correcto? | Pendiente: prueba propia del invariante indicada en §3 |
| ¿Cuánto cuesta? | $O(\log n)$ comparaciones, $O(1)$ memoria |
| ¿Se puede mejor? | Pendiente: cota de información propia indicada en §5 |
