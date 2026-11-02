# Tema 1 - Problema 10 

 Par más cercano en una dimensión. Demuestra en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión .

## Definición del Problema en Una Dimensión

**Entrada:** Una lista de $n$ números reales $x = (x_1, x_2, \dots, x_n)$ con $n \ge 2$.  
**Salida:** Un par de **índices distintos** $(i, j)$ con $i \neq j$ que minimice la distancia $|x_i - x_j|$.

### Precisiones Formales (Conferencia 2)
1. **Empates:** Si varios pares alcanzan la distancia mínima, se devuelve cualquiera de ellos.
2. **Repetidos:** La entrada es una lista y admite valores repetidos. Si existen elementos iguales, la distancia mínima es $0$ y el par devuelto satisface $x_i = x_j$.
3. **Métrica:** En una dimensión la distancia euclidiana es simplemente el valor absoluto $d(x_i, x_j) = |x_i - x_j|$.

## Demostración de la Cota Inferior $\Omega(n \log n)$ por Reducción

### El Modelo de Árboles de Decisión Algebraicos
Un **árbol de decisión algebraico de grado $d$** sobre $n$ variables reales es un árbol donde:
- Cada **nodo interno** evalúa el signo ($< 0$, $= 0$, $> 0$) de un polinomio $p \in \mathbb{R}[x_1, \dots, x_n]$ de grado $\le d$ y se ramifica en 3 caminos.
- Cada **hoja** contiene una etiqueta de salida (en este problema, un par de índices $(i, j)$).
- El costo en el peor caso es la **profundidad** (altura) del árbol $h$.

### El Teorema Base (Ben-Or, 1983)
> **Teorema (Ben-Or, 1983; C2 §8).** Todo árbol de decisión algebraico de grado $d$ y profundidad $h$ que resuelva el problema de **Distinción de Elementos** (*dados $n$ reales, decidir si existen $i \neq j$ tales que $x_i = x_j$*) cumple $h = \Omega(n \log n)$.

*Origen de la cota:* El conjunto de entradas en las que todos los elementos son distintos tiene $n!$ componentes conexas, una por cada orden posible de los elementos. Mediante un resultado de Milnor y Thom sobre variedades algebraicas, Ben-Or demuestra que un árbol de decisión algebraico de profundidad $h$ no puede distinguir todas esas componentes si $h$ es menor que un orden de $n\log n$. Por tanto, la distinción de elementos requiere $\Omega(n\log n)$.

### Reducción Formal: Distinción de Elementos $\le_P$ Par Más Cercano en 1D

Demostramos por reducción que resolver el Par Más Cercano en 1D requiere la misma cota $\Omega(n \log n)$:

**Construcción del Árbol $\mathcal{T}'$:**
Sea $\mathcal{T}$ un árbol de decisión algebraico de grado $d$ y profundidad $T(n)$ que resuelve el Par Más Cercano en 1D. Construimos un árbol $\mathcal{T}'$ para Distinción de Elementos así:
1. Copiamos la estructura de $\mathcal{T}$ (la transformación de la entrada es la identidad: **0 pruebas de signo**).
2. Cada hoja de $\mathcal{T}$ con la etiqueta $(i, j)$ se reemplaza por **un nodo interno** que evalúa el signo del polinomio de grado 1: $x_i - x_j$.
   - La rama $= 0$ conduce a la hoja de salida `"Hay iguales"`.
   - Las ramas $< 0$ y $> 0$ conducen a la hoja de salida `"Todos distintos"`.

El árbol resultante $\mathcal{T}'$ tiene grado $\max(d, 1)$ y profundidad $T(n) + 1$.

**Demostración de Correctitud de la Reducción:**
Sea $x \in \mathbb{R}^n$ y sea $(i, j)$ el par retornado por $\mathcal{T}$. Dado que $\mathcal{T}$ es correcto, $|x_i - x_j| = \min_{a \neq b} |x_a - x_b|$.
- **Si existen elementos iguales ($x_a = x_b$ para algún $a \neq b$):** La distancia mínima global es $0$, por lo que $|x_i - x_j| = 0 \implies x_i - x_j = 0$. El nodo añadido evalúa la rama $= 0$ y responde correctamente `"Hay iguales"`.
- **Si todos los elementos son distintos:** La distancia mínima es estrictamente positiva ($|x_i - x_j| > 0 \implies x_i - x_j \neq 0$). El nodo añadido evalúa $< 0$ o $> 0$ y responde correctamente `"Todos distintos"`.

**Conclusión de la Cota Inferior:**
Dado que $\mathcal{T}'$ resuelve Distinción de Elementos con profundidad $T(n) + 1$, por el Teorema de Ben-Or se cumple:
$T(n) + 1 = \Omega(n \log n) \implies T(n) = \Omega(n \log n)$

## Algoritmo que Rompe la Cota y su Modelo de Cómputo

### Algoritmo (Conferencia 2, §9)
El algoritmo que rompe la cota es la **Inserción Incremental Aleatoria en Rejilla Hash** (Rabin 1976, Kleinberg-Tardos §13.7). Logra un tiempo esperado de **$O(n)$**.

### Modelo de Cómputo: Word RAM
Este algoritmo no opera en un árbol algebraico, sino en una **Word RAM** equipada con:
1. **Función suelo / Parte entera ($\lfloor q / \delta \rfloor$):** Calcula la celda de un punto en $O(1)$.
2. **Direccionamiento indirecto:** Utiliza el índice calculado como clave para acceder a una tabla hash, cuyas operaciones de búsqueda e inserción tienen costo esperado $O(1)$.
3. **Generador de bits aleatorios:** Permite barajar la entrada con una permutación uniforme.

### Justificación de la Ausencia de Contradicción
No existe contradicción entre la cota $\Omega(n \log n)$ y el tiempo esperado $O(n)$ porque **operan en modelos distintos**:
- La función parte entera $\lfloor q / \delta \rfloor$ **no es un polinomio ni es continua**, por lo que no puede ser implementada en un nodo de decisión algebraico.
- El direccionamiento indirecto en tablas hash no existe en árboles de decisión.

> **Regla fundamental:** *"Toda cota mínima viene con su modelo pegado"*. Romper una cota demostrada es posible cambiando el modelo de cómputo y las herramientas asociadas.

## Adaptación del Algoritmo Incremental Aleatorio a 1 Dimensión

### Estructura de Datos y Rejilla 1D
1. Permutamos aleatoriamente los puntos $p_1, p_2, \dots, p_n$.
2. Mantenemos la distancia mínima actual $\delta$ entre los puntos insertados y una tabla hash de celdas.
3. **Ancho de Celda:** Cada celda es un **intervalo semiabierto de ancho $\delta$** (a diferencia del plano 2D donde se usa un cuadrado de lado $\delta/2$). La celda de un punto $q$ viene dada por $c(q) = \lfloor q / \delta \rfloor$.

### Invariante y Búsqueda en Vecindario (3 Celdas)
* **Invariante:** Cada celda de ancho $\delta$ contiene **a lo sumo 1 punto**.  
  *Demostración:* Si dos puntos pertenecieran a la misma celda de ancho $\delta$, su distancia sería estrictamente menor que $\delta$, lo que contradiría que $\delta$ es la distancia mínima actual entre los puntos ya procesados.
* **Inserción del punto $p_{i+1}$ (Celda $c$):** Cualquier punto a distancia menor que $\delta$ de $p_{i+1}$ debe pertenecer a la celda $c$ o a sus dos celdas adyacentes. En 1D se consultan únicamente **3 celdas vecinas**: $\{c - 1, \, c, \, c + 1\}$ (a diferencia de las 25 celdas del plano 2D).

```python
def par_mas_cercano_rejilla(x, semilla=None):
    import random

    idx = random.Random(semilla).sample(range(len(x)), len(x))
    
    a, b = idx[0], idx[1]
    delta, par = abs(x[a] - x[b]), (a, b)

    if delta == 0:
        return 0, (min(a, b), max(a, b))

    rejilla = {x[q] // delta: q for q in idx[:2]}

    for i in range(2, len(x)):
        p = idx[i]
        c = x[p] // delta
        antes = delta

        # Consultar las tres celdas vecinas
        for dc in (-1, 0, 1):
            q = rejilla.get(c + dc)

            if q is not None and abs(x[p] - x[q]) < delta:
                delta, par = abs(x[p] - x[q]), (p, q)

        if delta < antes:
            if delta == 0:
                return 0, (min(par), max(par))

            # Reconstruir la rejilla con el nuevo ancho
            rejilla = {x[q] // delta: q for q in idx[:i + 1]}
        else:
            rejilla[c] = p

    return delta, (min(par), max(par))
```

### Costo

**Peor caso.** El algoritmo tiene un costo de $\Theta(n^2)$ si el orden de inserción es adverso: si las distancias entre puntos consecutivos insertados van disminuyendo, cada nueva inserción reduce estrictamente $\delta$ y obliga a reconstruir la rejilla. 

Por ejemplo, se puede construir una entrada cuyos huecos consecutivos sean $n,\,n-1,\,n-2,\dots,2$, insertando los puntos en ese mismo orden. En cada paso se reconstruye la rejilla con todos los puntos procesados hasta el momento, por lo que el número total de operaciones de hash es cuadrático. 

**Costo esperado $O(n)$ (análisis hacia atrás de C2).** Sea $q_k=\Pr[\delta_k<\delta_{k-1}]$ la probabilidad de que la distancia mínima disminuya al insertar el punto $k$.

- La rejilla se reconstruye en el paso $k$ si y solo si $\delta$ disminuye estrictamente; es decir, si el mínimo de $S_k$ es menor que el de $S_k\setminus\{p_k\}$.
- Fijemos el conjunto $S_k=\{p_1,\dots,p_k\}$ y olvidemos el orden de inserción. Como el orden es una permutación uniforme, condicionado al conjunto, $p_k$ es uniforme entre sus $k$ elementos.
- Para que $\delta$ disminuya, $p_k$ tiene que pertenecer a **todos** los pares que alcanzan la distancia mínima de $S_k$. Si el par mínimo es único, sus dos extremos son los únicos puntos que pueden provocar una reconstrucción. Si hay empates, a lo sumo dos puntos pertenecen a todos los pares mínimos: si hay varios pares mínimos distintos que comparten un punto, ese punto es el único común; si no comparten ningún punto, ninguno puede provocar la reconstrucción.

Por tanto,

$$
q_k\leq \frac{2}{k}.
$$

La igualdad se alcanza cuando el par mínimo es único.

**Operaciones de tabla hash (lecturas y escrituras).** En el paso $k$, correspondiente a la inserción del $k$-ésimo punto ($3\leq k\leq n$), se realizan siempre 3 lecturas de la tabla hash. Si no hay reconstrucción, se realiza 1 escritura para insertar el nuevo punto. Si hay reconstrucción, se realizan $k$ escrituras, pues se vuelve a insertar en la tabla el conjunto completo de puntos procesados. Además, se realizan 2 escrituras durante la inicialización.

Por tanto, el número esperado de operaciones satisface:

$$
\begin{aligned}
\mathbb{E}[\text{ops}]
&\leq 2+\sum_{k=3}^{n}
\Big(3+(1-q_k)+q_k k\Big)\\
&=2+\sum_{k=3}^{n}\big(4+q_k(k-1)\big)\\
&\leq 2+\sum_{k=3}^{n}
\left(4+\frac{2(k-1)}{k}\right)\\
&\leq 2+6(n-2)\\
&=6n-10.
\end{aligned}
$$

El tamaño total de las reconstrucciones también queda acotado en esperanza:

$$
\mathbb{E}[\text{escrituras por reconstrucciones}]
=\sum_{k=3}^{n}q_k k
\leq \sum_{k=3}^{n}2
=2(n-2).
$$

Asimismo, el número esperado de reconstrucciones satisface:

$$
\mathbb{E}[\text{reconstrucciones}]
=\sum_{k=3}^{n}q_k
\leq 2\sum_{k=3}^{n}\frac{1}{k}
=2\left(H_n-\frac{3}{2}\right),
$$

donde $H_n$ es el $n$-ésimo número armónico. Por tanto, el número esperado de reconstrucciones es $O(\log n)$.

El costo total esperado es $O(n)$: las tres consultas por paso y las inserciones normales tienen costo lineal acumulado, mientras que las reconstrucciones, aunque pueden ser costosas individualmente, también tienen un costo total esperado lineal.

> Cuidado con lo que representa la esperanza. La esperanza se calcula sobre la permutación aleatoria que elige el algoritmo y la garantía vale para cada entrada fija. No se supone que los valores $x_i$ sean aleatorios. Por tanto, una misma entrada puede producir un costo de $\Theta(n^2)$ con un orden de inserción adverso y un costo lineal esperado cuando el algoritmo utiliza una permutación aleatoria.