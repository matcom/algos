# Ejercicio 10 ★★ — Par más cercano en una dimensión (C2, C5)

> Par más cercano en una dimensión. Demuestra $\Omega(n\log n)$ en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión.

## Problema

Dados $n\ge2$ reales $x_1,\dots,x_n$, encontrar $i\ne j$ que minimicen $|x_i-x_j|$ (con repetidos, la respuesta es 0).

## 1. Cota mínima: $\Omega(n\log n)$ en árboles de decisión algebraicos

**Modelo.** Árbol de decisión algebraico: cada nodo interno evalúa el signo ($<0$, $=0$, $>0$) de un polinomio de grado acotado en las entradas, y el costo es la profundidad.

**Teorema (Ben-Or, 1983).** Distinción de elementos (¿hay $i\ne j$ con $x_i=x_j$?) requiere $\Omega(n\log n)$ en ese modelo.

**Teorema.** Par más cercano en 1D requiere $\Omega(n\log n)$ en árboles de decisión algebraicos.

**Demostración (reducción).** Supongamos un árbol $T$ que resuelve par más cercano en 1D con profundidad $h(n)=o(n\log n)$. Construimos uno para distinción:

1. Dada la entrada $x_1,\dots,x_n$ de distinción, la entrada de par más cercano es **la misma lista**. La transformación no cuesta ninguna prueba de signo.
2. Corremos $T$. Llega a una hoja que declara un par $(i,j)$.
3. Agregamos **una** prueba más: el signo de $x_i-x_j$, un polinomio de grado 1. Respondemos "hay repetidos" si y solo si da 0.

Es correcto porque la distancia mínima es 0 si y solo si hay dos valores iguales, y el par declarado es uno que alcanza la mínima. La profundidad es $h(n)+1=o(n\log n)$, lo que contradice a Ben-Or. ∎

(Es la reducción de la C2 §8 con $x_i\mapsto(x_i,0)$; en una dimensión ni siquiera hace falta transformar.)

**El algoritmo que la alcanza:** ordenar y mirar los $n-1$ pares consecutivos (lema de la C2 §3), $O(n\log n)$. Es óptimo en ese modelo.

## 2. Qué algoritmo rompe la cota, y en qué modelo

El algoritmo **incremental aleatorio con rejilla** de la C2 §9 (Rabin 1976; Kleinberg y Tardos §13.7). Costo **esperado $O(n)$**.

**Modelo:** la RAM (word RAM de la C1 §9) con aleatoriedad. Tiene dos herramientas que el árbol de decisión algebraico no tiene:

- la **parte entera** $\lfloor x/(\delta/2)\rfloor$, que no es un polinomio ni es continua;
- el **direccionamiento indirecto**: usar ese número como clave de una tabla hash.

No hay contradicción: la cota es sobre otro modelo.

## 3. Adaptación a una dimensión

- **Rejilla:** celdas de largo $\delta/2$; la celda de $x$ es $\lfloor x/(\delta/2)\rfloor$, guardada en una tabla hash (diccionario).
- **Invariante:** cada celda tiene a lo sumo un punto, porque dos puntos en la misma celda estarían a distancia $<\delta/2<\delta$.
- **Insertar $p$:** todo punto a distancia $<\delta$ de $p$ está a menos de 2 celdas. Se miran las **5 celdas** $c-2,\dots,c+2$ (en el plano eran $5\times5=25$), cada una con a lo sumo un punto: $O(1)$.
  - Si nadie está más cerca que $\delta$, se inserta $p$: $O(1)$.
  - Si alguien está más cerca, $\delta$ baja y se **reconstruye** la rejilla con los $i$ puntos insertados: $O(i)$.
  - Si la distancia nueva es 0 (repetidos), se termina: no se puede bajar más.
- **Análisis hacia atrás (igual que en 2D):** fijado el conjunto de los primeros $i+1$ puntos, el par más cercano está determinado, y el paso $i+1$ reconstruye solo si el punto insertado es uno de esos dos. Con permutación uniforme, $\Pr\le2/(i+1)$. Entonces
$$\mathbb E[\text{costo}]=O(n)+\sum_{i}\frac{2}{i+1}\,O(i)=O(n).$$
  El número esperado de reconstrucciones es $\le\sum_i 2/(i+1)\approx2\ln n$.

La función `par_mas_cercano_1d_aleatorio(xs)` implementa esta adaptación: permuta los puntos al azar, toma como $\delta$ la distancia entre los dos primeros e inserta los demás uno a uno en la rejilla (un diccionario), revisando las 5 celdas vecinas y reconstruyendo cuando $\delta$ baja. Devuelve la distancia mínima, el par que la logra y cuántas reconstrucciones hizo; el parámetro `accesos` permite contar los accesos a la tabla.

> Código: [ejercicio-10.py](ejercicio-10.py), parte 1.

## Casos de prueba y validación

Oráculos: fuerza bruta $\Theta(n^2)$ y el algoritmo por ordenamiento. Con ellos comprobamos el algoritmo en algunos casos pequeños, incluido uno con un punto repetido (distancia 0).

> Código: [ejercicio-10.py](ejercicio-10.py), parte 2.

```text
[3.0, 1.0]                   -> distancia 2.0, par (3.0, 1.0)
[5, 1, 9, 3]                 -> distancia 2, par (1, 3)
[1, 2, 3, 4]                 -> distancia 1, par (1, 2)
[7, 7]                       -> distancia 0, par (7, 7)
[0.5, -2.0, 10.0, 0.75]      -> distancia 0.25, par (0.5, 0.75)
[-5, 5, -5.5, 100]           -> distancia 0.5, par (-5.5, -5)
```

Al azar, con repetidos, negativos y distintas escalas:

> Código: [ejercicio-10.py](ejercicio-10.py), parte 3.

```text
3000 pruebas contra la fuerza bruta: sin fallos
```

**La reducción en código:** distinción de elementos resuelta con el par más cercano y una prueba de signo al final.

> Código: [ejercicio-10.py](ejercicio-10.py), parte 4.

```text
distinción de elementos resuelta correctamente mediante la reducción
```

**Reconstrucciones contra $2\ln n$, y accesos a la tabla por punto.** Contamos operaciones del modelo, como la C2 (*"25 accesos a la tabla hash"*), en vez de segundos (C1 §2). Si el costo es lineal, los accesos por punto se mantienen acotados:

> Código: [ejercicio-10.py](ejercicio-10.py), parte 5.

```text
        n  reconstrucciones  2 ln n  accesos / n
    1,000              13.3    13.8         8.54
   10,000              17.7    18.4         8.98
  100,000              20.7    23.0         8.48
1,000,000              23.3    27.6         7.90
```

Los accesos por punto no crecen con $n$: hay 6 por punto (5 consultas y una inserción), más las reconstrucciones, que en esperanza cuestan $\sum_i \frac{2}{i+1}(i+1)\le 2n$, o sea a lo sumo 2 más por punto. Con solo 3 corridas la media fluctúa alrededor de ese 8, porque una reconstrucción tardía cuesta casi $n$ accesos de una sola vez. Las reconstrucciones siguen a $2\ln n$, un poco por debajo, porque $2/(i+1)$ es una cota y no una igualdad.

## Resumen

- **Cota:** distinción de elementos se reduce a par más cercano 1D con la identidad y una prueba de signo ⇒ $\Omega(n\log n)$ en árboles de decisión algebraicos (Ben-Or). Ordenar + consecutivos la alcanza.
- **Quién la rompe:** el algoritmo incremental aleatorio con rejilla de la C2 §9, en la RAM con parte entera, tabla hash y aleatoriedad. Costo esperado $O(n)$.
- **En 1D:** celdas de largo $\delta/2$, 5 celdas vecinas, reconstrucción con probabilidad $\le2/(i+1)$, $\approx2\ln n$ reconstrucciones.
