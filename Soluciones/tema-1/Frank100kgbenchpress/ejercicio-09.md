# Ejercicio 9: La mezcla "optimizada" incorrecta

**Enunciado:** Una mezcla "optimizada" de dos listas ordenadas de largo \(n\) deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla. (C5)

**Modelo:** Árboles de decisión por comparaciones. Algoritmo de mezcla (*merge*) estándar modificado.

---

## 1. El algoritmo con el bug

El algoritmo de mezcla tradicional compara los elementos actuales de ambas listas hasta que una de ellas se agota. La versión modificada introduce una condición de parada incorrecta: deja de comparar cuando a la primera lista le queda un solo elemento.

```python
def mezcla_con_bug(A, B):
    n = len(A)
    resultado = []
    i = j = 0

    # Se detiene cuando queda un solo elemento en A
    while i < n - 1 and j < n:
        if A[i] <= B[j]:
            resultado.append(A[i])
            i += 1
        else:
            resultado.append(B[j])
            j += 1

    # Coloca el último elemento de A al final
    if i == n - 1:
        resultado.append(A[i])

    return resultado
```

El error consiste en asumir que, cuando queda un solo elemento en \(A\), ese elemento puede colocarse directamente al final sin comprobar si todavía quedan elementos menores en \(B\).

---

## 2. Número de comparaciones en el peor caso

En cada iteración del ciclo se realiza exactamente una comparación y se extrae un elemento de alguna de las dos listas.

El ciclo termina cuando:

\[
i=n-1\quad\text{o}\quad j=n
\]

Distinguimos dos situaciones:

**Caso 1: Se detiene porque queda un elemento en A.**

Se han extraído \(n-1\) elementos de \(A\). Como el ciclo termina inmediatamente, se han extraído como máximo \(n-1\) elementos de \(B\).

Por tanto:

\[
C(n)\leq(n-1)+(n-1)
\]

**Caso 2: Se detiene porque B se ha agotado.**

Se han extraído los \(n\) elementos de \(B\). Como todavía debe cumplirse \(i<n-1\), se han extraído como máximo \(n-2\) elementos de \(A\).

Por tanto:

\[
C(n)\leq n+(n-2)
\]

En ambos casos obtenemos:

\[
C(n)\leq 2n-2
\]

Esta cota se alcanza cuando las listas están intercaladas de manera que se extraen alternativamente elementos de ambas hasta consumir \(n-1\) elementos de cada una.

Por tanto, el número máximo de comparaciones es:

\[
\boxed{C_{\max}(n)=2n-2}
\]

---

## 3. Decisión de correctitud mediante la cota inferior (Conferencia 5)

Para determinar si el algoritmo puede ser correcto, utilizamos la cota inferior conocida para la mezcla de dos listas ordenadas.

**Cota inferior:** Cualquier algoritmo basado en comparaciones que mezcle correctamente dos listas ordenadas de \(n\) elementos necesita, en el peor caso, al menos:

\[
\boxed{2n-1}
\]

comparaciones.

### Justificación mediante el adversario

Consideremos una posible entrada cuyo orden final sea:

\[
B_0<A_0<B_1<A_1<\cdots<B_{n-1}<A_{n-1}
\]

En el resultado final existen \(2n-1\) pares de elementos consecutivos que pertenecen a listas diferentes:

\[
(B_0,A_0),\ (A_0,B_1),\ (B_1,A_1),\ldots
\]

Para determinar correctamente el orden de salida, el algoritmo debe conocer la relación entre cada uno de estos pares.

Como son elementos consecutivos en el orden final, no puede deducirse su relación mediante la transitividad de comparaciones con otros elementos: no existe ningún elemento intermedio que permita establecerla.

Por tanto, cada uno de esos pares debe compararse directamente.

Esto obliga a realizar al menos:

\[
2n-1
\]

comparaciones en el peor caso.

### Aplicación al algoritmo modificado

Nuestro algoritmo realiza como máximo:

\[
2n-2
\]

comparaciones.

Pero cualquier algoritmo correcto necesita al menos:

\[
2n-1
\]

Por tanto:

\[
2n-2<2n-1
\]

El algoritmo no puede ser correcto para todas las entradas.

En consecuencia:

\[
\boxed{\text{El algoritmo es incorrecto}}
\]

La conclusión se obtiene mediante la cota inferior, sin necesidad de probar todas las entradas posibles.

---

## 4. Construcción de la entrada donde falla (Adversario)

Ahora construimos explícitamente una entrada que obliga al algoritmo a detenerse antes de tiempo.

El adversario establece el siguiente orden:

\[
B_0<A_0<B_1<A_1<\cdots<B_{n-2}<A_{n-2}<B_{n-1}<A_{n-1}
\]

De esta manera, el algoritmo consumirá alternativamente elementos de las dos listas hasta que haya extraído \(n-1\) elementos de cada una.

En ese momento:

- \(A\) todavía tiene su último elemento.
- \(B\) también tiene su último elemento.

Sin embargo, el algoritmo termina de comparar porque:

\[
i=n-1
\]

Y coloca directamente \(A_{n-1}\) al final del resultado, ignorando \(B_{n-1}\).

### Ejemplo concreto con n = 3

Podemos materializar las respuestas del adversario utilizando:

\[
A=[2,4,6]
\]

\[
B=[1,3,5]
\]

Ambas listas están ordenadas y cumplen:

\[
1<2<3<4<5<6
\]

**Ejecución:**

| Comparación | Elementos comparados | Elemento seleccionado |
|:---:|:---:|:---:|
| 1 | \(A[0]=2\), \(B[0]=1\) | 1 |
| 2 | \(A[0]=2\), \(B[1]=3\) | 2 |
| 3 | \(A[1]=4\), \(B[1]=3\) | 3 |
| 4 | \(A[1]=4\), \(B[2]=5\) | 4 |

Después de la cuarta comparación:

\[
i=2,\qquad j=2
\]

Como \(n=3\):

\[
i=n-1
\]

El ciclo termina y se añade directamente \(A[2]=6\).

**Resultado producido por el algoritmo:**

\[
[1,2,3,4,6]
\]

**Resultado correcto:**

\[
[1,2,3,4,5,6]
\]

El algoritmo ha omitido el elemento \(5\), que debía aparecer antes de \(6\).

Por tanto, queda demostrado mediante una entrada concreta que la mezcla modificada es incorrecta.

---

## 5. Conclusión

El algoritmo modificado realiza como máximo:

\[
\boxed{2n-2}
\]

comparaciones.

Sin embargo, la cota inferior para mezclar correctamente dos listas ordenadas de tamaño \(n\) establece que se necesitan al menos:

\[
\boxed{2n-1}
\]

comparaciones en el peor caso.

Por tanto, el algoritmo no puede ser correcto.

El adversario demuestra el fallo construyendo dos listas cuyos elementos están perfectamente intercalados. Cuando quedan los últimos elementos de ambas listas, el algoritmo detiene las comparaciones y coloca incorrectamente el último elemento de \(A\) al final, omitiendo un elemento de \(B\) que debería aparecer antes.

**La lección fundamental:** una reducción en el número de comparaciones inferior a la cota mínima necesaria no representa una optimización, sino que puede indicar que el algoritmo ha dejado de obtener información indispensable para producir una respuesta correcta.