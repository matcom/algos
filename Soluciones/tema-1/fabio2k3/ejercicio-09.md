# Solución ejercicio 9

Tenemos que mezclar dos listas ordenada A y B de largo n con el modelo de comparaciones

def mezcla_opt(A, B):
    n = len(A)
    i, j = 0, 0
    R = []

    while i < n - 1 and j < n:
        if A[i] <= B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1

    return R + B[j:] + A[i:]


En el peor de los casos hace 2n - 2 comparaciones.

Cota superior => cada vuelta el ciclo hace una comparación y avanza i o j en 1, así que tras q comparaciones i + j = q.
La vuelta solo se ejecuta si i <= n - 2 y j <= n -1, por lo que antes de la última comparación c - 1 = i + j <= (n-2) + (n-1) 

Entonces => c <= 2n - 2

Se alcanza con A  = [n, n+1, ..., 2n-1] y B = [1,2, ..., n-1, 2n]:

- A[0] = n es mayor que B[0..n-2], así que las primeras n-1 comparaciones sacan dichos elementos de B
- Después A[0], ..., A[n-2] son menores que B[n-1] = 2n y las siguientes n - 1 comparaciones sacan esos elementos de A

Entonces i = n-1 y el ciclo para con q = 2n - 2.

La mezcla normal hace 2n-1 en el peor caso así que esta ahorra exactamente una comparación.

Ahora ¿es correcta?
-------------------

Teorema visto en conferencia: mezclas dos listas de largo n requiere 2*n-1 comparaciones en el peor caso.

La optimizada hace a lo sumo 2n-2 < 2n-1, un algoritmo de comparaciones que hace menos que una cota demostrada está MAL, así que NO es correcta, tiene que fallar en alguna entrada.

Veamos ahora cuál es la que falla:

La del adversario visto en Conferencia es la intercalada ideal.

a1 < b1 < a2 < b2 < ...< an < bn ,es decir A = [0,2, 2*n-2] y B = [1, 3, 5, ..., 2*n-1]

Esta cadena tiene 2n-1 pares de vecinos, si un algoritmo termina sin compara algún par de vecinos, este falla.

Qué hace la optimizada sobre la entrada? => compara los pares de vecinos en orden hasta sacar an-1 y entonces i = n-1 y para. SOn 2n-3 comparaciones, nunca compara an ni bn así quedan sin comparar los pares de elementos: (bn-1, an) y ( an, bn).

En intercambio del adversario, intercambiamos los valores an y bn, que son vecinos en la cadena y no se comparan A' = [0,...,2n-4, 2n-1] y B' = [1, ..., 2n-3, 2n-2]. Ambas listas siguen ordenadas

Todas las comparaciones hechas dan las mismas respuestas en las dos entradas, así que el algoritmo sigue el mismo camino y devuelve los elementos en el mismo orden de posiciones a1, b1,..., a(n-1), b(n-1), bn, an

En la entrada original an < bn, por lo que el orden pone an antes de bn, y en A' ocurre lo contrario. La salida es la misma para las dos, así que es incorrecta en una. En la sale: 0, 1 , ..., 2n-4, 2n-3, 2n-1, 2n-2, que No está ordenada 

Pero, cuándo falla exactamente?
La mezcla optimizada es correcta <=> el máximo de las dos listas está en A ( an > bn)

(=>)Si an < bn, bn nunca sale dentro del ciclo, para salir tendría que ser menor que algún A[i] con i <= (n-2), pero A[i] < an < bn. entonces el ciclo termina con i = (n-1) y la salida acaba en bn, an que está al revés

(<=) Si an > bn, todo elemento de B es menor que an. Si el ciclo termina con i = n-1, R + B[j:] es la mezcla normal de A[0..n-2] con B y an es mayor que todo, así que ponerlo al final es correcto. Si termina con j = n, queda la mezcla normal más la cola de A, que es correcta

Por lo tanto por simetría , fallan exactamente la mitad de las entradas posibles

