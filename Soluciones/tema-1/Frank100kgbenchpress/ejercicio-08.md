# Ejercicio 8: El elemento que aparece más de \(n/3\) veces

**Enunciado:** Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa. (C3)

**Modelo:** Modelo RAM. Arreglo de \(n\) elementos. Búsqueda en una sola pasada \(O(n)\) tiempo y \(O(1)\) espacio.

---

## 1. Generalización de Boyer-Moore (Dos Candidatos)

Queremos encontrar los elementos que aparecen estrictamente más de \(n/3\) veces en un arreglo.

Como no pueden existir tres elementos diferentes que aparezcan cada uno más de \(n/3\) veces, sabemos que como máximo pueden existir **dos elementos mayoritarios**.

En efecto, si existieran tres:

\[
f_1>\frac n3,\quad f_2>\frac n3,\quad f_3>\frac n3
\]

entonces:

\[
f_1+f_2+f_3>n
\]

lo cual es imposible.

Por tanto, generalizamos Boyer-Moore utilizando dos candidatos y dos contadores.

### Algoritmo

Mantenemos:

- `cand1`: primer candidato.
- `cand2`: segundo candidato.
- `count1`: contador del primer candidato.
- `count2`: contador del segundo candidato.

Procesamos el arreglo de izquierda a derecha:

```python
def candidatos_mayoritarios(A):
    cand1 = cand2 = None
    count1 = count2 = 0

    for x in A:
        if count1 > 0 and x == cand1:
            count1 += 1

        elif count2 > 0 and x == cand2:
            count2 += 1

        elif count1 == 0:
            cand1 = x
            count1 = 1

        elif count2 == 0:
            cand2 = x
            count2 = 1

        else:
            # Los tres elementos son distintos.
            count1 -= 1
            count2 -= 1

    return cand1, count1, cand2, count2
```

**Idea del algoritmo:**

Cuando encontramos un elemento que no coincide con ninguno de los candidatos y ambos contadores son positivos, eliminamos una ocurrencia de cada candidato y el elemento actual.

Esto equivale a cancelar una tripleta formada por tres elementos diferentes.

Los contadores representan las ocurrencias que permanecen después de estas cancelaciones, no las frecuencias reales de los candidatos en el arreglo original.

---

## 2. Invariante reforzado y demostración (C3)

Para demostrar la correctitud del algoritmo, utilizamos un invariante más fuerte que simplemente afirmar que los elementos mayoritarios están entre los candidatos.

### Invariante reforzado

Después de procesar los primeros \(k\) elementos del arreglo, existe una partición de ese prefijo formada por:

1. Un conjunto de tripletas disjuntas, donde los tres elementos de cada tripleta son diferentes entre sí. Estas tripletas representan los elementos que han sido cancelados.
2. Un conjunto residual formado exclusivamente por:
   - `count1` ocurrencias de `cand1`, si `count1 > 0`.
   - `count2` ocurrencias de `cand2`, si `count2 > 0`.

En otras palabras, todo el prefijo procesado puede descomponerse en tripletas de elementos distintos y un conjunto residual que contiene como máximo dos valores diferentes.

De este invariante se deduce que:

\[
\boxed{
f_k(x)>\frac{k}{3}
\implies
x=cand1\ \text{o}\ x=cand2
}
\]

donde \(f_k(x)\) representa la frecuencia de \(x\) en los primeros \(k\) elementos.

### Demostración del invariante

La demostración se realiza por inducción sobre la cantidad de elementos procesados.

**1. Inicialización:**

Antes de procesar elementos:

\[
k=0
\]

Ambos contadores son cero y no existen elementos cancelados.

El prefijo vacío puede considerarse una partición sin tripletas y sin elementos residuales.

Por tanto, el invariante se cumple inicialmente.

**2. Mantenimiento:**

Supongamos que el invariante se cumple después de procesar los primeros \(k\) elementos. Procesamos ahora un nuevo elemento \(x\).

Existen tres situaciones:

- **Caso 1: \(x\) coincide con alguno de los candidatos activos.**

  Si:

  \[
  x=cand1
  \]

  incrementamos `count1`.

  Si:

  \[
  x=cand2
  \]

  incrementamos `count2`.

  En ambos casos, simplemente añadimos una ocurrencia al conjunto residual.

  La partición continúa siendo válida porque no se modifica ninguna tripleta cancelada.

- **Caso 2: Algún contador es cero.**

  Si `count1 == 0`, podemos asignar:

  \[
  cand1=x,\qquad count1=1
  \]

  Si `count2 == 0`, podemos hacer lo mismo con el segundo candidato.

  De esta manera, añadimos el nuevo elemento al conjunto residual como un nuevo tipo de elemento.

  El conjunto residual sigue conteniendo como máximo dos valores diferentes, por lo que el invariante se conserva.

- **Caso 3: Ambos contadores son positivos y \(x\) es diferente de los dos candidatos.**

  En este caso tenemos tres elementos diferentes:

  \[
  cand1,\quad cand2,\quad x
  \]

  Tomamos una ocurrencia de cada uno y las agrupamos en una nueva tripleta cancelada.

  Para representarlo, decrementamos ambos contadores:

  \[
  count1=count1-1
  \]

  \[
  count2=count2-1
  \]

  Como hemos eliminado tres elementos diferentes del conjunto residual y del elemento actual, el invariante continúa cumpliéndose.

En todos los casos, la propiedad se mantiene después de procesar el nuevo elemento.

**3. Conclusión:**

Por inducción, el invariante se cumple después de procesar cualquier prefijo del arreglo.

### Demostración de que el mayoritario siempre es candidato

Supongamos que un elemento \(y\) aparece \(f_k(y)\) veces entre los primeros \(k\) elementos.

Cada tripleta cancelada contiene tres elementos diferentes y, por tanto, puede eliminar como máximo una ocurrencia de \(y\).

Si se han formado \(q\) tripletas, se cumple:

\[
3q\leq k
\]

Por tanto:

\[
q\leq\frac{k}{3}
\]

Si \(y\) no estuviera entre los candidatos residuales, todas sus ocurrencias habrían sido eliminadas mediante las tripletas canceladas.

En ese caso:

\[
f_k(y)\leq q\leq\frac{k}{3}
\]

Pero si \(y\) aparece más de \(k/3\) veces:

\[
f_k(y)>\frac{k}{3}
\]

obtenemos una contradicción.

Por tanto:

\[
\boxed{
f_k(y)>\frac{k}{3}
\implies
y\in\{cand1,cand2\}
}
\]

Al finalizar el recorrido, cualquier elemento que aparezca más de \(n/3\) veces necesariamente estará entre los dos candidatos.

**Importante:** Esto demuestra que los candidatos contienen todos los posibles mayoritarios, pero no demuestra que ambos sean realmente mayoritarios. Por eso hace falta una segunda pasada de verificación.

---

## 3. Versión defectuosa: devolver los candidatos sin verificar

El algoritmo anterior permite identificar los posibles elementos mayoritarios, pero no garantiza que todos los candidatos con contador positivo aparezcan realmente más de \(n/3\) veces.

Para mostrar el error, implementamos una versión que devuelve directamente los candidatos cuyos contadores residuales son positivos, sin contar sus frecuencias reales.

```python
def mayoritarios_sin_verificar(A):
    cand1, count1, cand2, count2 = candidatos_mayoritarios(A)

    resultado = []

    if count1 > 0:
        resultado.append(cand1)

    if count2 > 0:
        resultado.append(cand2)

    return resultado
```

### ¿Por qué es incorrecta?

Los contadores representan las ocurrencias que sobreviven después de cancelar tripletas, no la frecuencia real de cada elemento en el arreglo.

Por tanto, un candidato puede terminar con contador positivo sin alcanzar la frecuencia necesaria para ser mayoritario.

**Ejemplo:**

Consideremos:

\[
A=[0,0,1]
\]

Tenemos:

\[
n=3,\qquad \frac n3=1
\]

El elemento 0 aparece dos veces, mientras que el elemento 1 aparece una sola vez.

Por tanto, el único mayoritario es 0, porque:

\[
2>1
\]

Sin embargo, el algoritmo termina con:

\[
cand1=0,\quad count1=2
\]

\[
cand2=1,\quad count2=1
\]

La versión sin verificar devuelve:

\[
[0,1]
\]

Esto es incorrecto porque 1 aparece exactamente \(n/3\) veces, no más de \(n/3\).

Se produce un **falso positivo**.

### Versión correcta con verificación

Para corregir el problema, realizamos una segunda pasada que cuenta las frecuencias reales de los candidatos.

```python
def mayoritarios(A):
    n = len(A)

    cand1, count1, cand2, count2 = candidatos_mayoritarios(A)

    resultado = []

    if count1 > 0:
        frecuencia1 = sum(1 for x in A if x == cand1)

        if 3 * frecuencia1 > n:
            resultado.append(cand1)

    if count2 > 0:
        frecuencia2 = sum(1 for x in A if x == cand2)

        if 3 * frecuencia2 > n:
            resultado.append(cand2)

    return resultado
```

Utilizamos la condición \(3f>n\) para evitar problemas de precisión al comparar con \(n/3\).

La primera pasada obtiene los candidatos y la segunda verifica sus frecuencias reales.

El algoritmo completo sigue teniendo:

\[
\boxed{T(n)=O(n)}
\]

y:

\[
\boxed{S(n)=O(1)}
\]

---

## 4. Generador de pruebas que NO atrapa el bug

El objetivo es construir un generador de pruebas que produzca arreglos en los que la versión defectuosa siempre devuelva una respuesta correcta.

Es decir, queremos evitar los falsos positivos.

### 4.1. Por qué un generador binario puede atrapar el bug

Consideremos un arreglo con dos valores distintos:

\[
A=[0,0,1]
\]

Como vimos anteriormente, ambos candidatos terminan con contador positivo, pero solamente uno supera \(n/3\).

Por tanto, la versión sin verificar devuelve un resultado incorrecto.

Otro ejemplo es:

\[
A=[0,0,0,1]
\]

Aquí:

\[
n=4,\qquad \frac n3=\frac43
\]

Las frecuencias son:

\[
f(0)=3,\qquad f(1)=1
\]

Solo 0 es mayoritario, pero ambos candidatos pueden terminar con contador positivo.

**Una precisión:** no todos los arreglos binarios atrapan el bug. Por ejemplo, en `[0,1,0,1]`, ambos elementos aparecen dos veces y:

\[
2>\frac43
\]

Por tanto, los dos son realmente mayoritarios. El problema aparece cuando uno de los valores tiene frecuencia positiva, pero no supera \(n/3\).

### 4.2. Generador que no atrapa el bug: tres valores equilibrados

Construimos arreglos con exactamente tres valores distintos, cada uno repetido la misma cantidad de veces.

Por ejemplo:

\[
A=[1,2,3,1,2,3]
\]

En este caso:

\[
n=6
\]

y las frecuencias son:

\[
f(1)=f(2)=f(3)=2
\]

Como:

\[
2=\frac63
\]

ningún elemento aparece estrictamente más de \(n/3\) veces.

**¿Por qué este generador no detecta el bug?**

El algoritmo cancela tripletas de tres elementos diferentes.

Como solamente existen tres valores posibles y cada uno aparece exactamente \(m\) veces, todas las tripletas canceladas contienen necesariamente una ocurrencia de cada valor.

Si se realizan \(q\) cancelaciones, quedan:

\[
m-q
\]

ocurrencias de cada uno de los tres valores.

Pero el conjunto residual del algoritmo puede contener como máximo dos valores diferentes.

Por tanto, no puede quedar ninguna ocurrencia:

\[
m-q=0
\]

De donde:

\[
q=m
\]

Así, ambos contadores terminan siendo cero:

\[
count1=count2=0
\]

La versión sin verificar devuelve una lista vacía.

Como ningún elemento supera \(n/3\), esta respuesta es correcta.

### 4.3. Implementación del generador

Podemos construir un generador que produzca arreglos equilibrados con tres valores diferentes:

```python
import random

def generar_prueba_no_detecta_bug(m):
    A = [0] * m + [1] * m + [2] * m
    random.shuffle(A)
    return A
```

Este generador produce arreglos de tamaño:

\[
n=3m
\]

Cada valor aparece exactamente:

\[
\frac n3=m
\]

veces.

Por tanto, el generador nunca produce un elemento mayoritario y el algoritmo de cancelación siempre termina con ambos contadores en cero.

La versión defectuosa devuelve una lista vacía, que coincide con el resultado correcto.

**Nota importante:** Esta propiedad depende de utilizar exactamente tres valores diferentes con frecuencias iguales. No se puede generalizar a cuatro o más valores.

Por ejemplo, consideremos:

\[
A=[1,2,3,4,1,2,3,4]
\]

El algoritmo puede terminar con los candidatos 3 y 4, ambos con contador positivo, aunque cada valor aparece solamente dos veces:

\[
2\leq\frac83
\]

En este caso, la versión defectuosa sí devuelve falsos positivos.

---

## 5. Conclusión

La generalización de Boyer-Moore utiliza dos candidatos porque, como máximo, pueden existir dos elementos que aparezcan más de \(n/3\) veces.

El invariante reforzado demuestra que el prefijo procesado puede descomponerse en tripletas de elementos distintos y un conjunto residual con como máximo dos valores. Esto garantiza que cualquier elemento que supere el umbral de \(n/3\) necesariamente estará entre los candidatos.

Sin embargo, los contadores finales no representan las frecuencias reales, por lo que es necesaria una segunda pasada para verificar los candidatos.

Finalmente, hemos construido un generador de pruebas con exactamente tres valores igualmente frecuentes que no detecta el bug, porque todas las ocurrencias terminan cancelándose en tripletas.

Las complejidades son:

| Versión | Tiempo | Espacio |
|---|---:|---:|
| Obtención de candidatos | \(O(n)\) | \(O(1)\) |
| Sin verificación | \(O(n)\) | \(O(1)\) |
| Con verificación | \(O(n)\) | \(O(1)\) |

La lección fundamental es que **ser un candidato posible no significa ser una respuesta válida**. El algoritmo de cancelación reduce el conjunto de posibilidades, pero la verificación de las frecuencias reales sigue siendo necesaria.