**Problema:** El elemento que aparece más de n/3 veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape.

## Algoritmo y generalización de Boyer-Moore
El problema exige identificar todos los elementos que aparecen estrictamente más de $\lfloor n/3 \rfloor$ veces en un arreglo $A[0...n-1]$.
* Matemáticamente, pueden existir a lo sumo dos elementos que aparezcan más de $n/3$ veces ya que $3 \times (\lfloor n/3 \rfloor + 1) > n$. Por tanto, el algoritmo de Boyer-Moore se generaliza utilizando dos candidatos $(c_1, c_2)$ y dos contadores $(k_1,k_2)$.

## Invariante reforzado y demostración:
Definición de variable de estado en el paso $i$:
Procesado el subarreglo $A[0...i-1]$(de lingitud $i$), el estado se define por $(c_1, k_1, c_2, k_2)$, con $c_1!=c_2$.

### Invariante reforzado: 
Al procesar el subarreglo $A[0...i-1]$, el multiconjunto de elementos de dicho prefijo puede particionarse en:
* $k_1$ copias del candidato $c_1$.
* $k_2$ copias del candidato $c_2$.
* Un conjunto de $3*k$ elementos que han sido cancelados en triadas compuestas por tres elementos distintos entre sí.

Entonces, si un elemento $x$ aparece más de $i/3$ veces en el subarreglo $A[0...i-1]$, necesariamente $x=c_1$ o $x=c_2$.

### Demostración por inducción:
* Caso Base $(i=0)$: El subarreglo esta vacío. $k_1 = 0$, $k_2 =  0$, $k = 0$.El invariante se cumple.
* Paso inductivo $(i -> i+1)$: Asumimos que el invariante en $i$ es cierto para $A[0...i-1]$. Analizamos la llegada del nuevo elemente $x = A[i]$.
    - Caso en que $x == c_1$ o $x == c_2$: Si $x == c_1$, incrementamos $k_1$ en 1. Las copias no canceladas de $c_1$ se incrementan en 1, mientras que las triadas canceladas $(k)$ no se alteran. Se preserva el invariante en $i+1$. Análogo para $x == c_2$.
    - Caso en que $x != c_1$ y $x != c_2$ y ($k_1 == 0$ o $k_2 == 0$): Si $k_1 == 0$, asignamos $c_1 = x$ y $k_1 = 1$. Como el contador era 0, el número total de elementos cancelados en triadas no cambia, simplemente se asigna un nuevo candidato no cancelado. Se preserva el invariante en $i+1$. Análogo para $k_2 == 0$.
    - Caso en que $x != c_1$ y $x != c_2$ y $k_1 > 0$ y $k_2 > 0$: El nuevo elemento $x$ es distinto de $c_1$ y $c_2$, y ambos contadores son positivos. Decrementamos $k_1$ en 1 y $k_2$ en 1. Hemos tomado una copia de $c_1$, una copia de $c_2$ y el nuevo elemento $x$ y los hemos descartado juntos. Esto incrementa el número de triada canceladas $k$ en 1. Por la hipótesis inductiva, como $x$ no pertenece a ninguna triada anterior ni coincide con $c_1$, $c_2$, la partición se mantiene exacta. Se preserva el invariante en $i+1$. 

## Algoritmo sin verificación directa:
La versión que devuelve los candidatos con contador positivo al finalizar el bucle se encuentra en `boyer_moore_n3_unverified.py`.

## El generador de pruebas:
Vamos a diseñar un generador de casos de prueba que demuestre que devolver únicamente los candidatos con contador positivo sin realizar una segunda pasada de verificación conduce a errores.

El Boyer-Moore clásico $(>n/2)$, el generador binario que alterna elementos de la forma $[A,B,A,B,C]$ deja un candidato final con contador 1, pero que no supera la frecuencia de $n/2$. Para el caso de dos candidatos $(> n/3)$, dicho patrón no siempre logra engañar a la rutina si las frecuencias relativas coinciden con las cancelaciones simples.

Para engañar al algoritmo sin verificación, debemos construir una secuencia donde dos elementos que $NO$ son las mayoria $(> n/3)$ terminen con contadores positivos $(k_1>0, k_2>0)$.

**Estructura del generador:**

Construimos un arreglo $A$ compuesto la concatenación repetida de un bloque base de cancelación $B$: $$A = B + B + ... + B$$
* Ejemplo concreto ($n=8$, umbral $n.3 = 2,7$ entonces requiere $>=3$ repeticiones): $A = [1, 2, 3, 4, 1, 2, 3, 4]$
* Implementación del generador: `generate_failing_test_case.py`
* Trazado paso a paso: `boyer_moore_n3_falso_positivo.png`
* Resultado final de la función sin verificar: Devuelve $[3,4]$ con $k_1=1$, $k_2=1$.
* Conclusión: Ningún elemento aparace más de $n/3$ veces. Sin embargo, el algoritmo sin verificación devuelve los candidatos $[3,4]$ como válidos.

