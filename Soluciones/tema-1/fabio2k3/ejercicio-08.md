# solución ejercicio 8

Dado un arreglo A de n elementos que solo se pueden comparar por igualdad, tenemos que devolver todos los que aparecen más de n/3 veces en O(n) y memoria O(1)

def freccuenter(A):
    c1 = c2 = None
    k1 = k2 = 0

    for x in A:
        if k1 > 0 and x == c1:
            k1 += 1
        elif k2 > 0 and x == c2:
            k += 1
        elif k1 == 0:
            c1 = x
            k1 = 1
        elif k2 == 0:
            c2 = x
            k2 = 1
        else:
            k1 -= 1
            k2 -= 1

    cuenta = Counter(A)
    return sorted(c for c, k in ((c1,k1), (c2,k2)) if k > 0 and 3*cuenta[c] > len(A))

Planteemos nuestra invariante:
-------------------------------
I: tras procesar el prefijo A[1..i] es se puede partir en tripletas de elementos distintos entre sí, más k1 copias de c1 y k2 copias de c2. Además si k1 > 0 y k2 > 0 entonces c1 != c2.

Inicialización del algoritmo => el prefijo es vacío y k1 = k2 = 0, cero tripletas y cero copias

En cada vuelta del ciclo procesamos x, Hay cinco casos, uno por rama del if:

- k1 > 0 y x = c1, k1 sube y x es una copia más de c1.

- k2 > 0, y x = c2, igual con c2

- k1 = 0, x pasa a c1 con k1 = 1, una copia, si k2 > 0, el caso 2 no se aplicó, así que x != c2 y c1 != c2.

- k2 = 0, simétrico al anterior

- Ambos contadores positivos y x distinto de c1 y c2, por I, c1 != c2, así que [x, una copia de cc1, copia de c2] son tres elementos distintos entre sí y forman una tripleta, los contadores bajan 1 y c1 != c2 siguen valiendo


Al terminar A, se divide en t tripletas de distintos más k1 + k2, copias así que n= 3t + k1 + k2, y t <= n/3. Sea v un elemento que aparece más de n/3 veces. Si v no fuera ninguno de los candidatos con contador positivo, todas sus aparciones estarían en tripletas, a lo sumo una por tripleta, es decir v aparecería a lo sumo t <= n/3 veces que es una Contradicción

Por lo tanto todo elemento que aparece más de n/3 veces es un candidato con contador positivo.

La segunda pasada cuenta a los candidatos y se queda con los que cumplen 3*cuenta > n, no devuelve nada que no deba y no pierde nada

Costo => dos pasadas de O(n) de tiempo y O(1)

versión sin verificar:
-----------------------

def atajo(A):
    return [c for c, k in ((c1,k1), (c2,k2)) if k >0 ]

Contraejemplo => A B C D, A y B entran como candidatos C los cancela a los 2 y D ocupa una ranura libre, el atajo devuelve [D], pero nadie aparece 4/3 veces.

Otro contraejemplo M M N Q P devuelve [M, P] y solo A es frecuente.

El generador de pruebas que no la detecta:
---------------------------------------------

El generador binario sí detecta el atajo y la mayoría plantada tampoco sirve, con dos ranuras, el segundo candidato puede ser un elemento sobrante que no es frecuente, y las pruebas con frecuentes plantados lo detectan.

Generador que no lo detecta => tres símbolos, cada uno exactamente n/3 veces, en orden aleatorio

Y ahora, por qué falla? Ningún símbolo aparece más de n/3 veces, así que la respuesta correcta es siempre [], veamos que el atajo devuelve [] también:

1- Por I, las k1+k2 , copias que sobran son de a lo sumo dos símbolos, así que algún símbolo s no está entre ellas.
2-  Las n/3 copias de s están entonces en tripletas, una por tripleta, así que t >= n/3
3- Por 3t <= n, luego t = n/3 y no sobra nada k1 = k2 = 0, el atajo devuelve []