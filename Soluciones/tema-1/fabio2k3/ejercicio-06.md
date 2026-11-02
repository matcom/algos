# Solución del Ejercicio 6

dada una matriz n x n, con cada fila y cada columna ordenadas de menor a mayor, y tenemos que decidir si un número x está en nuestra matriz.

DEfinamos nuestra matriz como M.

Algoritmo:
-----------

def search(M, x):
    n = len(M)
    i = 0
    j = n -1

    while i < n  and j >= 0:
        if M[i][j] == x:
            return (i,j)
        if M[i][j] > x:
            j -= 1
        else:
            i += 1

    return None

Vamos a plantear nuestra invariante I:

I => x está en M, está en las filas >= i  y columnas <= j, es decir x no aparece en las filas < i ni en las columnas > j

Con i = 0 y j = n-1 no  hay filas < 0 ni columnas > n-1, así que I se cumple.

Supongamos que I al inicio de una vuelta de ciclo, con i < n y j >= 0, y M[i][j] != x.

Si M[i][j] > x por el orden de las columnas M[q][j] >= M[i][j] > x para todo q >= i. Las filas < i ya están descartadas por I, así que x no está en la columna j. Con j' = j -1, x no está en las columnas mayores que j', y I se conserva

Si M[i][j] < x por el orden de las filas, M[i][p] <= M[i][j] < x para todo p <= j. Las columnas > j ya están descartadas por I, por ende x no está en la fila i. Con i' ? i + 1, x no está en las filas menores que i', I se conserva

Analicemos el potencial:
-------------------------

Sea G = (n-i) + (j+1), el número de filas más el de columnas que quedan, es un entero, que vale 2n al inicio y en cada vuelta i sube en 1 o baja en 1, por lo que G baja exactamente 1. El ciclo exige n-i >= 1 y j + 1 >= 1, es decir, G >= 2 , de modo que hace a lo sumo 2n - 1 vueltas.

Costo => cada vuelta hace una comparación de tres resultados, así que el algoritmo usa a lo sumo 2n-1 comparaciones que es O(n), y memoria sería  O(1)


Cota mínima (que no se puede en o(n)):
--------------------------------------

Todo algoritmo correcto necesita al menos n comparaciones en el peor caso.

Usemos adversario:
Entrada del adversario: M0[i][j] = 10(i+j) y x = 10(n-1)+5. Las filas y columnas son estrictamente crecientes, y x no está en M0. las celdas de la antidiagonal D_k = (k, n-1-k), con K = 0..n-1, valen todas 10(n-1) < x y resto cumple que:

- i+j < n - 1 valen a lo sumo 10(n-2) < x
- i + j > n-1 vale al menos 10n > x

El adversario responde las comparaciones como si la entrada fuera M0

Supongamos que un algoritmo termina sin haber consultado una celda D_k, sea M1 igual a M0 salvo M1[D_k] = x.

1. M1 sigue ordenado => los vecinos de D_k valen 10(n*2) (izquierda y arriba) y 10n (derecha y abajo) y 10(n-2) < x < 10n.

2. Todas las comparaciones hechas dan el mismo resultado en M0 y en M1 porque solo se diferencian en D_k, que no se consultó.

3. El algoritmo da la misma respuesta en las dos, pero M0 la correcta es "no está" y en M1 "sí está", se equivoca en una de las dos.


Por lo tanto un algoritmo correcta consulta n celdas antidiagonal de M0, y hace al menos n comparaciones, es Ω(n) y no o(n)
