# Ejercicio 10: Par más cercano en una dimensión

**Enunciado:** Par más cercano en una dimensión. Demuestra \(\Omega(n\log n)\) en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión. (C2, C5)

**Modelo inicial:** Árboles de decisión algebraicos (ADT). Las operaciones permitidas sobre las entradas reales son sumas, restas, multiplicaciones, divisiones y comparaciones (\(<,=,>\)). No se permite utilizar operaciones de discretización como la parte entera.

---

## 1. Cota inferior: \(\Omega(n\log n)\) por reducción (C5)

Para demostrar que el problema del par más cercano en una dimensión requiere \(\Omega(n\log n)\) en árboles de decisión algebraicos, utilizamos una reducción desde el problema de la **Distinción de Elementos (Element Distinctness)**.

### Problema de Distinción de Elementos

Dado un conjunto de \(n\) números reales:

\[
x_1,x_2,\ldots,x_n
\]

debemos determinar si todos son distintos.

Se conoce que este problema necesita:

\[
\boxed{\Omega(n\log n)}
\]

operaciones en el modelo de árboles de decisión algebraicos.

### Reducción al problema del par más cercano

Supongamos que disponemos de un algoritmo \(A\) que encuentra el par de elementos más cercano en una dimensión.

Podemos utilizarlo para resolver Distinción de Elementos:

1. Ejecutamos \(A\) sobre los elementos \(x_1,\ldots,x_n\).
2. Obtenemos un par de elementos cuya distancia es mínima.
3. Comprobamos si ambos elementos son iguales.

Si la distancia mínima es cero:

\[
\delta=0
\]

significa que existen dos elementos iguales y, por tanto, la respuesta a Distinción de Elementos es negativa.

Si:

\[
\delta>0
\]

significa que todos los elementos son diferentes y la respuesta es afirmativa.

No es necesario que el valor absoluto sea una operación primitiva del modelo: podemos obtener el par de índices más cercano y comprobar directamente la igualdad de sus coordenadas.

### Conclusión de la reducción

Si pudiéramos resolver el problema del par más cercano en:

\[
o(n\log n)
\]

podríamos resolver Distinción de Elementos en ese mismo tiempo.

Esto contradice la cota inferior conocida para dicho problema.

Por tanto:

\[
\boxed{T(n)=\Omega(n\log n)}
\]

En consecuencia, el problema del par más cercano en una dimensión tiene una cota inferior de \(\Omega(n\log n)\) en el modelo de árboles de decisión algebraicos.

---

## 2. Algoritmo que rompe la cota (C2)

La Conferencia 2 presenta la idea de los **algoritmos aleatorizados de rejilla (grid) y hashing**, asociados a Rabin, para resolver problemas geométricos de proximidad.

Estos algoritmos permiten superar la cota anterior porque utilizan un modelo computacional más potente que el de árboles de decisión algebraicos.

### ¿Qué modelo rompe la cota?

Utilizamos una RAM con soporte para:

- Tablas hash con acceso esperado \(O(1)\).
- Operaciones de discretización mediante `floor`.
- Aleatoriedad para introducir los elementos en un orden aleatorio.

En particular, la operación:

\[
\left\lfloor\frac{x}{\delta}\right\rfloor
\]

permite asignar cada punto a una celda de una rejilla.

Esta operación no pertenece al modelo de árboles de decisión algebraicos. Por ello, la cota inferior de \(\Omega(n\log n)\) no se aplica directamente a este algoritmo.

El hashing permite acceder a las celdas en tiempo esperado constante.

---

## 3. Adaptación del algoritmo aleatorizado a una dimensión

En una dimensión, las celdas de la rejilla se convierten en intervalos de longitud \(\delta\).

La idea es mantener una distancia mínima provisional y utilizar una tabla hash para localizar rápidamente los puntos que podrían estar a una distancia menor.

### 3.1. Construcción de los intervalos

Dada una distancia provisional \(\delta>0\), asignamos cada punto \(x\) a una celda mediante:

\[
\boxed{c(x)=\left\lfloor\frac{x}{\delta}\right\rfloor}
\]

Los intervalos son:

\[
[\ldots,-\delta),\quad
[0,\delta),\quad
[\delta,2\delta),\quad\ldots
\]

Si dos puntos \(x\) e \(y\) tienen una distancia menor que \(\delta\):

\[
|x-y|<\delta
\]

entonces sus índices de celda difieren como máximo en una unidad:

\[
|c(x)-c(y)|\leq1
\]

Por tanto, para encontrar un punto que esté a menos de \(\delta\) de un elemento nuevo, solamente necesitamos examinar:

- Su propia celda.
- La celda anterior.
- La celda siguiente.

Además, mientras \(\delta\) sea la distancia mínima entre los puntos procesados, cada celda puede contener como máximo un punto: dos puntos en un mismo intervalo de longitud \(\delta\) tendrían una distancia estrictamente menor que \(\delta\).

### 3.2. Algoritmo incremental aleatorizado

Primero mezclamos aleatoriamente los puntos. Tomamos los dos primeros para establecer una distancia inicial.

Después incorporamos los demás puntos uno a uno.

Cuando llega un nuevo punto:

1. Calculamos su celda.
2. Consultamos las tres celdas relevantes.
3. Si encontramos una distancia menor, actualizamos \(\delta\) y reconstruimos la tabla hash.
4. Si no encontramos una distancia menor, insertamos el punto directamente.

```python
import random
import math

def par_mas_cercano_1d(P):
    n = len(P)

    if n < 2:
        return None

    # Permutación aleatoria
    Q = list(P)
    random.shuffle(Q)

    # Distancia inicial entre los dos primeros puntos
    delta = abs(Q[0] - Q[1])
    mejor_par = (Q[0], Q[1])

    # Si ya existe una distancia cero, hemos encontrado el mínimo
    if delta == 0:
        return mejor_par, 0

    procesados = Q[:2]

    # Construimos la tabla hash inicial
    tabla = {}

    for x in procesados:
        clave = math.floor(x / delta)
        tabla[clave] = x

    # Incorporación incremental de los restantes puntos
    for x in Q[2:]:

        clave = math.floor(x / delta)

        nueva_distancia = delta
        pareja = None

        # Revisamos la celda actual y sus dos vecinas
        for k in (clave - 1, clave, clave + 1):

            y = tabla.get(k)

            if y is not None:
                distancia = abs(x - y)

                if distancia < nueva_distancia:
                    nueva_distancia = distancia
                    pareja = y

        procesados.append(x)

        if nueva_distancia == 0:
            return (pareja, x), 0

        if nueva_distancia < delta:

            # Encontramos un nuevo mínimo
            delta = nueva_distancia
            mejor_par = (pareja, x)

            # Reconstruimos la tabla con el nuevo tamaño de celda
            tabla = {}

            for y in procesados:
                k = math.floor(y / delta)
                tabla[k] = y

        else:

            # No hay mejora: insertamos directamente
            tabla[clave] = x

    return mejor_par, delta
```

El algoritmo devuelve el par más cercano y su distancia. Si existen puntos repetidos, devuelve inmediatamente una pareja de distancia cero.

---

## 4. Análisis de correctitud

Mantenemos el siguiente invariante:

**Invariante:** Después de procesar los primeros \(i\) puntos, \(\delta\) es exactamente la distancia mínima entre todos los pares de puntos procesados.

Además, la tabla hash contiene todos los puntos procesados, organizados en intervalos de longitud \(\delta\), y cada intervalo contiene como máximo un punto.

### Demostración

**1. Inicialización:**

Comenzamos con dos puntos.

Calculamos:

\[
\delta=|Q[0]-Q[1]|
\]

Por tanto, \(\delta\) es exactamente la distancia mínima entre los dos puntos procesados.

La tabla hash almacena ambos elementos según sus intervalos.

Como la distancia entre ellos es \(\delta\), no pueden encontrarse en el mismo intervalo de longitud \(\delta\).

El invariante se cumple inicialmente.

**2. Mantenimiento:**

Supongamos que el invariante se cumple antes de incorporar un nuevo punto \(x\).

Cualquier punto anterior que esté a una distancia menor que \(\delta\) de \(x\) debe encontrarse en su misma celda o en alguna de sus dos celdas vecinas.

Como cada celda contiene como máximo un punto, basta con realizar tres consultas a la tabla hash.

Existen dos posibilidades:

- **No encontramos ningún punto a distancia menor que \(\delta\).**

  Entonces, ninguna pareja formada por \(x\) y un punto anterior mejora la distancia mínima.

  Por tanto, el mínimo sigue siendo \(\delta\), y simplemente insertamos \(x\) en su celda.

- **Encontramos un punto a distancia menor que \(\delta\).**

  Calculamos la menor distancia entre \(x\) y los puntos de las tres celdas consultadas.

  Como no existen otros puntos a distancia menor que \(\delta\) fuera de esas celdas, el nuevo mínimo global entre los puntos procesados es exactamente esa distancia.

  Actualizamos \(\delta\) y reconstruimos la tabla hash con el nuevo tamaño de intervalo.

En ambos casos, el invariante se conserva.

**3. Conclusión:**

Al finalizar el recorrido, todos los puntos han sido procesados y \(\delta\) representa la distancia mínima entre cualquier pareja de puntos del conjunto original.

Por tanto, el algoritmo devuelve correctamente el par más cercano.

---

## 5. Análisis del tiempo esperado

Cada punto requiere una cantidad constante de trabajo para consultar su propia celda y las dos vecinas.

El único trabajo adicional aparece cuando encontramos una distancia menor que la actual, porque debemos reconstruir la tabla hash con todos los puntos procesados.

La aleatoriedad permite demostrar que el costo esperado de esas reconstrucciones es lineal.

### ¿Con qué frecuencia hay que reconstruir la tabla?

Sea \(\delta_i\) la distancia mínima entre los primeros \(i\) puntos de la permutación aleatoria.

La tabla se reconstruye cuando:

\[
\delta_i<\delta_{i-1}
\]

Esto significa que el último punto incorporado participa en una pareja que establece un nuevo mínimo.

Consideremos los primeros \(i\) puntos como un conjunto fijo. Debido a la permutación aleatoria, el último punto incorporado es igualmente probable entre los \(i\) puntos.

En una dimensión, ordenamos esos puntos:

\[
p_1<p_2<\cdots<p_i
\]

La distancia mínima corresponde a uno o varios pares consecutivos.

Para que el último punto provoque una reducción estricta de la distancia mínima, debe pertenecer a todos los pares que alcanzan esa distancia.

En una dimensión, como máximo existen dos puntos que pueden cumplir esa condición:

- Si existe un único par más cercano, sus dos extremos.
- Si existen dos pares mínimos consecutivos, el punto que comparten.
- Si existen pares mínimos separados, no hay ningún punto común a todos ellos.

Por tanto:

\[
P(\text{reconstrucción en el paso }i)\leq\frac{2}{i}
\]

### Costo esperado de las reconstrucciones

Cuando se produce una reconstrucción, tenemos que insertar nuevamente los \(i\) puntos procesados.

Su costo es:

\[
O(i)
\]

El costo esperado de reconstruir en el paso \(i\) queda acotado por:

\[
O(i)\cdot\frac{2}{i}=O(1)
\]

Sumando para todos los puntos:

\[
E[T(n)]\leq O(n)+
\sum_{i=3}^{n}O(1)
\]

Por tanto:

\[
\boxed{E[T(n)]=O(n)}
\]

Cada consulta de hashing tiene costo esperado \(O(1)\), y solamente hay una cantidad constante de consultas por punto.

### Espacio

Almacenamos los puntos procesados en una lista y en una tabla hash.

Por tanto:

\[
\boxed{S(n)=O(n)}
\]

---

## 6. Conclusión

Hemos demostrado que el problema del par más cercano en una dimensión tiene una cota inferior:

\[
\boxed{\Omega(n\log n)}
\]

en el modelo de árboles de decisión algebraicos, mediante una reducción desde Distinción de Elementos.

Sin embargo, utilizando un modelo RAM con operaciones de discretización, hashing y aleatoriedad, podemos adaptar el algoritmo de rejilla para resolverlo en tiempo esperado lineal.

El algoritmo mantiene una distancia mínima provisional y utiliza intervalos de tamaño \(\delta\) para localizar únicamente los puntos que podrían mejorarla.

La permutación aleatoria garantiza que las reconstrucciones de la tabla hash tienen un costo esperado total lineal.

Por tanto:

\[
\boxed{E[T(n)]=O(n)}
\]

y:

\[
\boxed{S(n)=O(n)}
\]

**La lección fundamental:** una cota inferior siempre depende del modelo de computación. Un algoritmo puede superar una cota de árboles de decisión algebraicos si utiliza operaciones adicionales, como la discretización mediante `floor` y el acceso a tablas hash.