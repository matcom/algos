# Mediana de dos arreglos ordenados

**Resumen**: Recordar el metodo `Merge` del `MergeSort` y notar que no necesitamos mezclar los arreglos. Solo necesitamos encontrar una partición que contenga exactamente $n$ elementos en su lado izquierdo, lo cual se puede encontrar usando búsqueda binaria.

## 1. Enunciado formal del problema

**Entrada:**

Dos arreglos ordenados de longitud $n$:

$$
A = [a_1,a_2,\ldots,a_n]
$$

$$
B = [b_1,b_2,\ldots,b_n]
$$

Ambos arreglos están ordenados en orden no decreciente.

**Salida:**

La mediana es el $n$-ésimo elemento más pequeño entre los $2n$ elementos.

Queremos un algoritmo con:

$$
T(n)=O(\log n)
$$

**Supuestos:**
- Ambos arreglos están ordenados en orden no decreciente.
- Los elementos son comparables.
- Se permiten elementos duplicados.
- Podemos acceder a un elemento de un arreglo en tiempo $O(1)$.

---

## 2. Algoritmo

### Observación clave

En lugar de mezclar los arreglos, podemos buscar una partición que divida los elementos en dos grupos:

- Grupo izquierdo: exactamente $n$ elementos.
- Grupo derecho: exactamente $n$ elementos.

La mediana es el **mayor elemento del grupo izquierdo**.

Supongamos que tomamos $i$ elementos de $A$. Para asegurar que el grupo izquierdo contenga exactamente $n$ elementos, debemos tomar $n-i$ elementos de $B$.

Por lo tanto, nuestra partición se ve así:

```text
A:  a1 ... a[i] | a[i+1] ... an
B:  b1 ... b[n-i] | b[n-i+1] ... bn
                  ^
               Partition
```

Para que esta partición sea válida, deben cumplirse las siguientes condiciones:

$$
a_i \leq b_{n-i+1}
$$

$$
b_{n-i} \leq a_{i+1}
$$

Estas condiciones aseguran que cada elemento de la izquierda sea menor o igual que cada elemento de la derecha.

Podemos encontrar tal partición usando búsqueda binaria sobre $A$.

### Estrategia de búsqueda binaria

Hay tres posibilidades:

1. Si $a_i > b_{n-i+1}$, tomamos demasiados elementos de $A$. Debemos disminuir $i$.

2. Si $b_{n-i} > a_{i+1}$, tomamos muy pocos elementos de $A$. Debemos aumentar $i$.

3. En caso contrario, encontramos una partición válida.

Para manejar los límites, definimos:

$$
a_0=b_0=-\infty
$$

$$
a_{n+1}=b_{n+1}=+\infty
$$

Esto elimina los casos especiales para particiones vacías.

### Pseudocódigo

```python
low = 0
high = n

while low <= high:

    i = floor((low + high) / 2)
    j = n - i

    if A[i] > B[j + 1]:
        high = i - 1

    elif B[j] > A[i + 1]:
        low = i + 1

    else:
        if A[i] > B[j]:
            return A[i]
        else:
            return B[j]
```

*Los accesos a los arreglos usan indexación basada en 1. Definimos $A[0]=B[0]=-\infty$ y $A[n+1]=B[n+1]=+\infty$.*

---

## 3. Demostración de correctitud

Probamos que el algoritmo devuelve el $n$-ésimo elemento más pequeño.

### Lema 1: Siempre existe una partición válida.

**Demostración:**

Considere la mezcla conceptual de ambos arreglos ordenados.

Tome los primeros $n$ elementos de esta secuencia mezclada.

Suponga que exactamente $i$ elementos provienen de $A$. Como la partición izquierda contiene exactamente $n$ elementos, los $n-i$ elementos restantes deben provenir de $B$.

Debido a que la secuencia mezclada está ordenada, cada elemento de la partición izquierda es menor o igual que cada elemento de la partición derecha.

En consecuencia:

$$
A[i]\leq B[n-i+1]
$$

$$
B[n-i]\leq A[i+1]
$$

Por lo tanto, siempre existe una partición válida. $\square$

### Lema 2: La búsqueda binaria nunca descarta una partición válida.

**Demostración:**

Considere las dos condiciones.

**Caso 1:**

$$
A[i]>B[n-i+1]
$$

Como ambos arreglos están ordenados, aumentar $i$ solo puede aumentar $A[i]$ y disminuir $B[n-i+1]$.

Por lo tanto, toda partición con $i'\geq i$ también viola la primera condición.

No puede existir ninguna partición válida en esa dirección.

Así, podemos actualizar de forma segura:

$$
high=i-1
$$

**Caso 2:**

$$
B[n-i]>A[i+1]
$$

Aumentar $i$ disminuye $B[n-i]$ y aumenta $A[i+1]$.

Por lo tanto, toda partición con $i'\leq i$ también viola la segunda condición.

No puede existir ninguna partición válida en esa dirección.

Así, podemos actualizar de forma segura:

$$
low=i+1
$$

En ambos casos, el algoritmo preserva al menos una partición válida. $\square$

### Teorema: El algoritmo devuelve la mediana.

**Demostración:**

Cuando el algoritmo encuentra una partición, se cumplen ambas condiciones:

$$
A[i]\leq B[j+1]
$$

$$
B[j]\leq A[i+1]
$$

Como ambos arreglos están ordenados, estas condiciones garantizan que cada elemento de la partición izquierda sea menor o igual que cada elemento de la partición derecha.

La partición izquierda contiene exactamente:

$$
i+j=n
$$

elementos.

Por lo tanto, el mayor elemento de la partición izquierda es precisamente el $n$-ésimo elemento más pequeño entre los $2n$ elementos.

El algoritmo devuelve:

$$
\boxed{\max(A[i],B[j])}
$$

Así, el algoritmo devuelve la mediana requerida. $\square$

### Terminación

En cada iteración, `low` aumenta o `high` disminuye.

Por lo tanto, el intervalo de búsqueda disminuye estrictamente.

Como el intervalo inicial es finito, el algoritmo debe terminar.

Además, el Lema 1 garantiza que existe una partición válida, y el Lema 2 garantiza que nunca se descarta.

En consecuencia, el algoritmo finalmente encuentra una partición válida y devuelve la mediana.

Por lo tanto, el algoritmo es totalmente correcto.

---

## 4. Análisis de complejidad temporal

El algoritmo realiza una búsqueda binaria sobre las posibles particiones del arreglo $A$.

Inicialmente, hay:

$$
n+1
$$

posibles particiones, que corresponden a:

$$
i\in\{0,1,\ldots,n\}
$$

Cada iteración elimina aproximadamente la mitad de los candidatos restantes.

Después de $k$ iteraciones, el número de candidatos es como máximo:

$$
\frac{n+1}{2^k}
$$

El algoritmo termina cuando esta cantidad se vuelve menor o igual que 1.

Por lo tanto:

$$
\frac{n+1}{2^k}\leq 1
$$

Tomando logaritmos:

$$
k\geq \log_2(n+1)
$$

Cada iteración realiza un número constante de comparaciones y accesos a arreglos.

Por lo tanto:

$$
\boxed{T(n)=O(\log n)}
$$

La complejidad espacial auxiliar es:

$$
\boxed{S(n)=O(1)}
$$

---

## 5. Cota inferior desde la teoría de la información

Queremos establecer si un algoritmo puede resolver este problema más rápido que $O(\log n)$.

Trabajamos en el **modelo de comparación**, donde el algoritmo obtiene información sobre los elementos mediante comparaciones.

Suponga que todos los elementos son distintos.

### Observación

Hay $2n$ elementos posibles que podrían ser la mediana.

En particular, cualquier elemento de cualquiera de los dos arreglos puede ser el $n$-ésimo elemento más pequeño para alguna entrada válida.

Por ejemplo, considere un elemento $A[k]$.

Podemos construir arreglos ordenados válidos tales que:

- Exactamente $k-1$ elementos de $A$ son menores que $A[k]$.
- Exactamente $n-k$ elementos de $B$ son menores que $A[k]$.

Así, exactamente:

$$
(k-1)+(n-k)=n-1
$$

elementos son menores que $A[k]$.

Por lo tanto, $A[k]$ es la mediana.

El mismo argumento se aplica a cada elemento de $B$.

### Argumento del árbol de decisión

Un algoritmo basado en comparaciones puede representarse como un árbol de decisión binario.

Cada comparación tiene dos resultados posibles:

- El primer elemento es menor.
- El primer elemento es mayor.

Como hay $2n$ posibles elementos medianos, el árbol de decisión debe tener al menos $2n$ hojas para distinguir todas las respuestas posibles.

Un árbol binario de altura $h$ tiene como máximo:

$$
2^h
$$

hojas.

Por lo tanto:

$$
2^h\geq 2n
$$

Tomando logaritmos:

$$
h\geq\log_2(2n)
$$

En consecuencia:

$$
\boxed{T(n)=\Omega(\log n)}
$$

### Conclusión: optimalidad

Hemos establecido:

**Cota superior:**

$$
T(n)=O(\log n)
$$

**Cota inferior:**

$$
T(n)=\Omega(\log n)
$$

Por lo tanto:

$$
\boxed{T(n)=\Theta(\log n)}
$$

El algoritmo es asintóticamente óptimo en el modelo de comparación.

Ningún algoritmo basado en comparaciones puede resolver este problema en tiempo $o(\log n)$ en el peor caso.

---

## 6. Complejidad final

| Propiedad | Complejidad |
|---|---|
| Complejidad temporal | $O(\log n)$ |
| Cota inferior de información | $\Omega(\log n)$ |
| Complejidad temporal óptima | $\Theta(\log n)$ |
| Espacio auxiliar | $O(1)$ |

