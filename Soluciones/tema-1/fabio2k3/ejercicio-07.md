# Solución Ejercicio 7:

Tenemos que devolver el n-ésimo menor de dos Arreglos ordenados A y B de largo n, es decir el n-ésimo menor de los 2n elementos.

Los n menores elementos son los primeros i de A y los primeros j = n - i de B, para algún i entre 0 y n, si encontramos ese i, la respuesta es el mayor de los n elegidos, y lo buscamos mediante búsqueda binaria.

Desarrollando nuestra idea, tendríamos el siguiente algoritmo:

def mediana(A, B):
    n = len(A)
    l = 0
    r = n

    while l < r:
        m = (l + r + 1) // 2
        if A[m - 1] <= B[n - m]:
            l = m
        else:
            r = m - 1

    i = l
    j = n - l

    if i > 0 and j > 0:
        return max(A[i - 1], B[j-1])
    return A[i-1] if i > 0 else B[j-1]

Veamos si nuestro algoritmo es correcto:
------------------------------------------

Para 0 <=  i <= n y j = n - i, sea L_i = A[0...i-1] U B[0..j-1] y R_i el resto. La partición i es válida si todo elemento de L_i es menor o  igual todo elemento de R_i

1- Si la partición es i es válida , el n-ésimo menor es max(L_i)

=> Todo elemento de R_i es mayor o igual todo elemento de L_i, así que en el orden de los 2n elementos L_i ocupa las primeras n posiciones y la n-ésima es su máxima.

2- La partición i es válida <=> se cumplen: 

- C1(i): A[i-1] <= B[n-i] (verdadero si i = 0)
- C2(i): B[n-i-1] <= A[i] (verdadero si i = n)

=> Dentro de A y B el orden ya está dado. Los únicos pares que faltan son: 
1. lo mayor de A a la izquierda, lo menor de B a la derecha, que es C1, y 2. lo mayor de B a la izquierda, lo menor de A a la derecha, que es C2

3- Si C1(i) y i' <= i, entonces C1(i'). A[i' - 1] <= A[i - 1] <= B[n - i] <= B[n - i'], ya que A y B están ordenados

4- Sea i* el mayor i con C1(i)

La partición i* es válida, C1(i*) vale por definición. Si i* = n, C2 es vacía. Si i* < n, C1(i* + 1) es falsa, A[i*] > B[n - i* - 1], que implica c2(i*), que por (2) es válida.

Analicemos la invariante de nuestro ciclo:
------------------------------------------

I: l <= i* <= r

Al inicio: l = 0 y r = 0: 0 <= i* <= n

En cada vuelta del ciclo:
l < r, m = (l + r) // 2, que cumple l < m <= r, así que A[m - 1] y B[n - m] existen. Si C1(m), por la def. de i* como máximo, m <= i*, y l' = m conserva I. Si no, por (3) no puede ser i >= m, así que i* <= m - 1 = r', y I se conserva.
 
=> Al salir l = h, así que l = i*. Por (4), la partición es válida, y por (1) la respuesta es max(L_i*): A[i - 1] si j = 0, B[j - 1] si i = 0, y el mayor de los dos si ninguno es 0.

Potencial: P = r - l + 1 es el número de candidatos para i: un entero mayor o igual que 1 que vale n + 1 al inicio. COn P = s >= 2, la nueva P es ⌈s/2⌉ si l = m  y ⌊s/2⌋ si h = m - 1. En ambos casos es ⌈s/2⌉ < s, así que baja estrictamente y el ciclo termina. Tras r vueltas P < ⌈(n+1)/2^r⌉, que llega a 1 cuando 2^r >= n + 1.

Costo: El ciclo hace a lo sumo ⌈log2(n+1)⌉ comparaciones, y la comparación final de los dos máximos solo ocurre si 0 < i < n. Total: a lo sumo ⌈log2(n+1)⌉ + 1 = O(logn) comparaciones, con memoria O(1). Mezclar y quedarse con la posición n cuesta O(n)

Análisis de la cota Información:
--------------------------------

Todo algoritmo de comparaciones hace al menos ⌈log2(n)⌉ + 1 comparaciones en el peor caso.

Hay 2n salidas posibles, la salida es la posición del elemento que es el n-ésimo menor. Cada una de las 2n posiciones puede serlo: para A[k], basta una entrada donde A[0...k-1] y b[0..n-k-2] sean menores que A[k] y todo lo demás sea mayor. Esas k + (n-k-1) = n - 1 menores hacen que A[k] sea el n-ésimo, y los arreglos siguen ordenados, igual para B[k]

Cada salida distinta necesita una hoja distinta, el algoritmo solo ve respuestas , así que dos entradas llegan a la misma hoja reciben la misma salida. Si sus salidas correctas son distintas, se equivoca en una.

El árbol de decisión es binario y tienen al menos 2n hojas, por el lema 1 de la conferencia número 5 , 2^h >= 2n, es decir h >= log2(2n) = log2 (n) + 1. La altura es entera, luego h >= ⌈log2(n)⌉ + 1.