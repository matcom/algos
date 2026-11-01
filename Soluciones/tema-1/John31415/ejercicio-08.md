## Problema

Dada la variante del problema de la mayoría en la que se busca identificar todos los elementos que aparecen estrictamente más de $\frac{n}{3}$ veces en un arreglo de tamaño $n$:

1. **Generalización:** Extienda el algoritmo clásico de Boyer-Moore utilizando **dos candidatos y dos contadores** para cancelar simultáneamente grupos de tres elementos distintos.
2. **Invariante:** Enuncie el **invariante reforzado** que describe el estado de la estructura tras procesar cualquier prefijo.
3. **Demostración:** Demuestre formalmente el invariante mediante inducción matemática.
4. **Variante con Atajo:** Escriba la versión del algoritmo que omite la segunda pasada de verificación y retorna directamente los candidatos con contadores positivos.
5. **Generador de Pruebas:** Diseñe o analice un generador de instancias de prueba que **no logre atrapar** los falsos positivos generados por la versión con atajo (explicando por qué el generador binario clásico de la conferencia previa sí los detectaría).

---

## Solución

### 1. Generalización del Algoritmo de Boyer-Moore ($\frac{n}{3}$)

Para hallar elementos con frecuencia superior a $\frac{n}{3}$, el principio de cancelación se amplía: en lugar de eliminar pares de elementos distintos, cancelamos **tripletes de elementos distintos** ($x, c_1, c_2$). Si un elemento aparece más de $\frac{n}{3}$ veces, su frecuencia excede la cantidad total de grupos de tres elementos distintos que pueden ser eliminados, garantizando que sobrevivirá al proceso como uno de los dos candidatos finales.

#### Implementación del Algoritmo (Con Verificación)

```python
def mayorias_dos(A):
    c1, cc1 = None, 0
    c2, cc2 = None, 0

    # Primera pasada: selección de candidatos mediante cancelación por tripletes
    for x in A:
        if cc1 > 0 and x == c1:
            cc1 += 1
        elif cc2 > 0 and x == c2:
            cc2 += 1
        elif cc1 == 0:
            c1, cc1 = x, 1
        elif cc2 == 0:
            c2, cc2 = x, 1
        else:
            cc1 -= 1
            cc2 -= 1

    # Segunda pasada: verificación estricta de candidatos
    f1 = sum(1 for x in A if cc1 > 0 and x == c1)
    f2 = sum(1 for x in A if cc2 > 0 and x == c2)

    resultado = []
    if f1 > len(A) // 3:
        resultado.append(c1)
    if cc2 > 0 and c2 != c1 and f2 > len(A) // 3:
        resultado.append(c2)

    return resultado

```

---

### 2. Invariante Reforzado

> *"Después de procesar cualquier prefijo del arreglo, sus elementos pueden particionarse en grupos disjuntos de tres elementos distintos entre sí, y en dos conjuntos residuales que contienen exactamente $cc_1$ copias del candidato $c_1$ y $cc_2$ copias del candidato $c_2$, respectivamente."*

Este invariante establece formalmente que los contadores representan de manera exacta las apariciones remanentes de los candidatos que no han sido destruidas por las cancelaciones de tripletes.

---

### 3. Demostración del Invariante por Inducción

#### A. Inicialización

Antes de procesar el primer elemento del arreglo, el prefijo está vacío y ambos contadores valen cero ($cc_1 = 0, cc_2 = 0$). No existen grupos de tres elementos ni elementos residuales, por lo que el invariante se cumple de forma trivial.

#### B. Mantenimiento

Asumimos que el invariante es válido tras procesar un prefijo dado, y evaluamos la llegada de un nuevo elemento $x$:

1. **Si $x = c_1$:** Se incrementa $cc_1$. Esto equivale a añadir una copia adicional de $c_1$ al conjunto residual correspondiente, manteniendo el invariante.
2. **Si $x = c_2$:** Se incrementa $cc_2$, añadiendo una copia de $c_2$ al conjunto residual correspondiente.
3. **Si $cc_1 = 0$:** Se asigna $c_1 = x$ y $cc_1 = 1$. El elemento actual pasa a formar parte del conjunto residual del primer candidato.
4. **Si $cc_2 = 0$:** Se asigna $c_2 = x$ y $cc_2 = 1$. El elemento actual pasa a formar parte del conjunto residual del segundo candidato.
5. **Caso general de cancelación:** Ambos contadores son estrictamente positivos y $x$ es distinto de ambos candidatos ($x \neq c_1$ y $x \neq c_2$). Seleccionamos una copia de $c_1$, una copia de $c_2$ y el elemento actual $x$. Como estos tres elementos son mutuamente distintos, forman un nuevo grupo de tres elementos distintos. Al decrementar ambos contadores ($cc_1$ y $cc_2$), eliminamos exactamente esas dos copias residuales, mientras que $x$ queda eliminado mediante la nueva formación del triplete. El invariante se preserva.

#### C. Conclusión de la Demostración

Al finalizar el recorrido, el arreglo completo queda particionado en grupos disjuntos de tres elementos distintos y dos conjuntos residuales asociados a los candidatos finales.

Si existiera un elemento $y$ con una frecuencia superior a $\frac{n}{3}$, cada grupo de tres elementos distintos puede contener como máximo una única aparición de $y$. Como existen a lo sumo $\lfloor n/3 \rfloor$ grupos de tripletes, estos no pueden contener todas las apariciones de $y$. Por consiguiente, al menos una aparición de $y$ debe obligatoriamente permanecer en alguno de los conjuntos residuales, demostrando que $y$ será capturado como uno de los candidatos finales. La segunda pasada filtra los falsos positivos verificando las frecuencias reales.

---

### 4. Versión con Atajo (Sin Verificación de Candidatos)

Omitir la segunda pasada de verificación reduce el costo operacional, pero introduce vulnerabilidades a falsos positivos, ya que un contador positivo solo indica supervivencia al proceso de cancelación, no mayoría estricta:

```python
def mayorias_dos_atajo(A):
    c1, cc1 = None, 0
    c2, cc2 = None, 0

    for x in A:
        if cc1 > 0 and x == c1:
            cc1 += 1
        elif cc2 > 0 and x == c2:
            cc2 += 1
        elif cc1 == 0:
            c1, cc1 = x, 1
        elif cc2 == 0:
            c2, cc2 = x, 1
        else:
            cc1 -= 1
            cc2 -= 1

    resultado = []
    if cc1 > 0:
        resultado.append(c1)
    if cc2 > 0 and c2 != c1:
        resultado.append(c2)

    return resultado

```

---

### 5. Generador de Pruebas que No Atrapa el Error del Atajo

Para construir un generador que falle en detectar los falsos positivos de la versión con atajo, podemos restringir las instancias a arreglos compuestos por un **único símbolo repetido**:

```python
def generador_que_no_atrapa(n):
    return ["A"] * n

```

#### Análisis del Comportamiento

* Este generador produce arreglos en los que absolutamente todos los elementos son idénticos (`"A"`).
* Al procesarlos, el primer candidato ($c_1$) acumula un contador de $cc_1 = n$, mientras que el segundo candidato permanece sin inicializar ($cc_2 = 0$).
* El atajo devuelve únicamente el elemento `"A"`, el cual aparece $n$ veces (cumpliendo sobradamente la condición de aparecer más de $\frac{n}{3}$ veces).
