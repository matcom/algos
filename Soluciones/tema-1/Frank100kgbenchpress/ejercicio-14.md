# Ejercicio 14: El ciclo completo (Máximo y Mínimo Simultáneos)

**Problema:** Dado un arreglo \(A\) de \(n\) elementos, encontrar el valor máximo y el valor mínimo. Supondremos que \(n\) es par para simplificar las cuentas.

**Modelo:** Árboles de decisión por comparaciones. Solo podemos comparar dos elementos entre sí.

---

## 1. El algoritmo (Comparación por parejas)

El algoritmo ingenuo encuentra el máximo con \(n-1\) comparaciones y el mínimo con otras \(n-1\), realizando un total de:

\[
2n-2
\]

comparaciones.

Podemos mejorar este resultado procesando los elementos en parejas. Primero comparamos los elementos de cada pareja entre sí y después utilizamos el mayor para actualizar el máximo y el menor para actualizar el mínimo.

```python
def max_y_min(A):
    n = len(A)

    if n == 0:
        return None, None

    # Inicialización con los dos primeros elementos
    if A[0] > A[1]:
        max_actual, min_actual = A[0], A[1]
    else:
        max_actual, min_actual = A[1], A[0]

    # Procesamos los elementos restantes en parejas
    for i in range(2, n, 2):

        # Primera comparación: ordenamos la pareja
        if A[i] > A[i+1]:
            mayor_par, menor_par = A[i], A[i+1]
        else:
            mayor_par, menor_par = A[i+1], A[i]

        # Segunda comparación: actualizamos el máximo
        if mayor_par > max_actual:
            max_actual = mayor_par

        # Tercera comparación: actualizamos el mínimo
        if menor_par < min_actual:
            min_actual = menor_par

    return max_actual, min_actual
```

El algoritmo procesa primero los dos elementos iniciales y después incorpora las parejas restantes.

---

## 2. Correctitud (Invariante - C3)

Definimos el siguiente invariante:

**Invariante:** Al inicio de cada iteración \(k\) del bucle, después de haber procesado las primeras \(2k\) posiciones, las variables `max_actual` y `min_actual` contienen respectivamente el máximo y el mínimo de esos \(2k\) elementos.

Formalmente:

\[
max\_actual=\max(A[0],\ldots,A[2k-1])
\]

\[
min\_actual=\min(A[0],\ldots,A[2k-1])
\]

### Demostración

La demostración se realiza mediante los tres pasos habituales:

**1. Inicialización:**

Antes de comenzar el bucle, hemos procesado los dos primeros elementos:

\[
A[0],A[1]
\]

Los comparamos y asignamos correctamente el máximo y el mínimo de esa pareja.

Por tanto:

\[
max\_actual=\max(A[0],A[1])
\]

\[
min\_actual=\min(A[0],A[1])
\]

El invariante se cumple inicialmente para \(k=1\).

**2. Mantenimiento:**

Supongamos que el invariante se cumple para los primeros \(2k\) elementos.

En la siguiente iteración incorporamos la pareja:

\[
(A[2k],A[2k+1])
\]

Primero realizamos una comparación entre ambos elementos para determinar:

\[
mayor\_par=\max(A[2k],A[2k+1])
\]

\[
menor\_par=\min(A[2k],A[2k+1])
\]

Después actualizamos el máximo:

\[
max\_actual=
\max(max\_actual,mayor\_par)
\]

De esta manera, obtenemos el máximo de los primeros \(2k+2\) elementos.

Análogamente, actualizamos el mínimo:

\[
min\_actual=
\min(min\_actual,menor\_par)
\]

Obtenemos así el mínimo de los primeros \(2k+2\) elementos.

Por tanto, el invariante se conserva.

**3. Terminación:**

Cuando termina el bucle, se han procesado todas las parejas del arreglo.

Como \(n\) es par, las variables contienen:

\[
\boxed{max\_actual=\max(A)}
\]

\[
\boxed{min\_actual=\min(A)}
\]

Por tanto, el algoritmo devuelve correctamente el máximo y el mínimo globales del arreglo.

---

## 3. Análisis del costo (C2)

Calculamos exactamente el número de comparaciones realizadas.

**1. Inicialización:**

Se compara \(A[0]\) con \(A[1]\):

\[
C_1=1
\]

**2. Procesamiento de las parejas restantes:**

Después de los dos primeros elementos quedan \(n-2\) elementos, que forman:

\[
\frac{n-2}{2}=\frac n2-1
\]

parejas.

**3. Comparaciones por pareja:**

Cada pareja requiere exactamente tres comparaciones:

- Una comparación para determinar el mayor y el menor de la pareja.
- Una comparación para actualizar el máximo global.
- Una comparación para actualizar el mínimo global.

Por tanto:

\[
C_{\text{parejas}}=
3\left(\frac n2-1\right)
\]

**4. Total:**

Sumando la inicialización y el procesamiento de las parejas:

\[
C(n)=1+3\left(\frac n2-1\right)
\]

Desarrollando:

\[
C(n)=1+\frac{3n}{2}-3
\]

Finalmente:

\[
\boxed{C(n)=\frac{3n}{2}-2}
\]

El algoritmo realiza exactamente \(\frac{3n}{2}-2\) comparaciones para \(n\) par.

---

## 4. Cota mínima mediante el adversario (C5)

Para demostrar que el algoritmo es óptimo, debemos probar que ningún algoritmo basado en comparaciones puede encontrar simultáneamente el máximo y el mínimo utilizando menos de:

\[
\frac{3n}{2}-2
\]

comparaciones en el peor caso.

Utilizamos el método del adversario.

### 4.1. Clasificación de los elementos

Inicialmente, todos los elementos pueden ser tanto el máximo como el mínimo.

El adversario mantiene tres categorías:

- **U (Sin clasificar):** elementos que todavía no han ganado ni perdido ninguna comparación.
- **G (Candidatos a máximo):** elementos que han ganado al menos una comparación y, por tanto, no pueden ser el mínimo.
- **P (Candidatos a mínimo):** elementos que han perdido al menos una comparación y, por tanto, no pueden ser el máximo.

Un elemento que pertenece a \(G\) todavía puede ser el máximo global. De igual forma, uno que pertenece a \(P\) todavía puede ser el mínimo global.

### 4.2. Estrategia del adversario

El adversario responde a las comparaciones de la siguiente manera:

**Caso 1: Se comparan dos elementos sin clasificar (U-U).**

El adversario determina que uno sea mayor que el otro.

- El ganador pasa a la categoría \(G\).
- El perdedor pasa a la categoría \(P\).

Una sola comparación clasifica dos elementos.

**Caso 2: Se compara un elemento sin clasificar con uno de la categoría G.**

El adversario responde que el elemento de \(G\) es mayor.

El elemento sin clasificar pasa a \(P\), mientras que el de \(G\) conserva su posibilidad de ser el máximo.

Solo se clasifica un elemento nuevo.

**Caso 3: Se compara un elemento sin clasificar con uno de la categoría P.**

El adversario responde que el elemento sin clasificar es mayor.

Este pasa a \(G\), mientras que el elemento de \(P\) conserva su posibilidad de ser el mínimo.

Nuevamente, solo se clasifica un elemento nuevo.

**Caso 4: Se comparan dos elementos de G.**

El adversario determina cuál es mayor.

El menor queda descartado como máximo global. El mayor conserva su posibilidad de ser el máximo.

**Caso 5: Se comparan dos elementos de P.**

El adversario determina cuál es menor.

El mayor queda descartado como mínimo global. El menor conserva su posibilidad de ser el mínimo.

**Caso 6: Se compara un elemento de G con uno de P.**

El adversario responde que el elemento de \(G\) es mayor.

Esta comparación no elimina ningún candidato a máximo ni a mínimo.

Estas respuestas permiten mantener la consistencia de las comparaciones y obligan al algoritmo a distinguir correctamente los candidatos.

### 4.3. Primera fase: clasificación de los elementos

Inicialmente hay \(n\) elementos sin clasificar.

Para eliminar un elemento de la categoría U:

- Una comparación U-U clasifica dos elementos.
- Una comparación U-G o U-P clasifica solamente uno.

Por tanto, cada comparación puede clasificar como máximo dos elementos nuevos.

Para clasificar los \(n\) elementos se necesitan como mínimo:

\[
\boxed{\frac n2}
\]

comparaciones.

Una vez terminada esta fase, todos los elementos quedan clasificados entre los candidatos a máximo y los candidatos a mínimo.

Sean:

\[
|G|=g,\qquad |P|=p
\]

Como las categorías son disjuntas y contienen todos los elementos:

\[
g+p=n
\]

### 4.4. Segunda fase: encontrar el máximo y el mínimo

Una vez clasificados los elementos:

- El máximo global solamente puede encontrarse entre los \(g\) elementos de \(G\).
- El mínimo global solamente puede encontrarse entre los \(p\) elementos de \(P\).

Para identificar el máximo entre \(g\) candidatos necesitamos al menos:

\[
g-1
\]

comparaciones.

Para identificar el mínimo entre \(p\) candidatos necesitamos al menos:

\[
p-1
\]

comparaciones.

Por tanto, esta segunda fase requiere como mínimo:

\[
(g-1)+(p-1)
\]

Sustituyendo \(g+p=n\):

\[
n-2
\]

comparaciones.

### 4.5. Cota inferior total

Sumando las dos fases:

\[
C_{\min}(n)\geq
\frac n2+(n-2)
\]

Por tanto:

\[
\boxed{C_{\min}(n)\geq\frac{3n}{2}-2}
\]

Esto demuestra que cualquier algoritmo basado en comparaciones necesita al menos \(\frac{3n}{2}-2\) comparaciones en el peor caso.

---

## 5. Conclusión: optimalidad del algoritmo

Hemos obtenido dos resultados:

**Costo del algoritmo de parejas:**

\[
C(n)=\frac{3n}{2}-2
\]

**Cota inferior mediante el adversario:**

\[
C_{\min}(n)\geq\frac{3n}{2}-2
\]

Como ambas cantidades coinciden:

\[
\boxed{C_{\text{óptimo}}(n)=\frac{3n}{2}-2}
\]

Por tanto, el algoritmo de comparación por parejas es óptimo en el modelo de comparaciones para \(n\) par.

La demostración completa sigue el ciclo de análisis de algoritmos:

1. **Diseño:** comparación de elementos por parejas.
2. **Correctitud:** demostración mediante un invariante inductivo.
3. **Complejidad:** conteo exacto de las comparaciones.
4. **Optimalidad:** cota inferior demostrada mediante el adversario.

**Conclusión fundamental:** procesar los elementos en parejas permite aprovechar cada comparación para descartar simultáneamente un candidato a máximo y otro a mínimo. De esta forma se alcanza exactamente la cota mínima teórica.