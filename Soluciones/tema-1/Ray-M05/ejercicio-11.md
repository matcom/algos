# Ejercicio 11. La mochila entera, medida en bits

> **Enunciado.** ★★ La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad. Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? (C1)

## Respuesta

- **Tamaño:** con todos los números en binario, la entrada ocupa $L = \sum_i (\text{bits}(w_i) + \text{bits}(v_i)) + \text{bits}(W)$ bits. La capacidad aporta solo $\text{bits}(W) \approx \log_2 W$ de esos bits.
- **No es polinomial.** $W$ puede ser exponencial en $L$: con un objeto y $W = 2^b - 1$, la entrada tiene $L = 2b + 1$ bits y el algoritmo calcula $2^b = 2^{(L-1)/2}$ celdas. Es **pseudopolinomial**: polinomial en el valor de $W$, no en sus bits.
- **Se parece a la primalidad por división** en que las dos cuentan hasta un número de la entrada. La primalidad hace unas $\sqrt N = 2^{b/2}$ divisiones con $b$ bits, y la mochila hace $nW$ pasos con $W < 2^{\text{bits}(W)}$. Las dos son polinomiales en el valor y exponenciales en el tamaño.
- **En qué se diferencian:** en la mochila, si $W$ es pequeño respecto de $n$, el algoritmo sí es polinomial; en la primalidad el número es toda la entrada.

### El problema y el modelo

**Mochila entera.** Hay $n$ objetos con pesos $w_i \ge 1$ y valores $v_i \ge 1$, enteros, y una capacidad entera $W$. Hay que elegir un subconjunto de peso total a lo sumo $W$ y valor total máximo.

**Modelo:** la word RAM de C1, donde cada operación sobre una palabra cuesta 1. Los números de la tabla caben en una palabra en las entradas usuales. Si no cupieran, cada operación costaría un factor polinomial en sus bits, y la conclusión no cambia.

### El algoritmo y su costo en $n$ y $W$

Sea $M(i, c)$ el mejor valor con los $i$ primeros objetos y capacidad $c$. Entonces $M(0, c) = 0$ y

$$
M(i, c) = \begin{cases} M(i-1, c) & \text{si } w_i > c, \\ \max\bigl(M(i-1, c),\; v_i + M(i-1, c - w_i)\bigr) & \text{si } w_i \le c. \end{cases}
$$

La respuesta es $M(n, W)$. Cada una de las $n(W + 1)$ celdas con $i \ge 1$ cuesta $O(1)$, así que el tiempo es $\Theta(nW)$. Guardando una sola fila y recorriendo $c$ de mayor a menor, la memoria es $O(W)$:

<!-- codigo: extra_11/mochila.py mochila -->
```python
def mochila(pesos, valores, W):
    """M[c] es el mejor valor con capacidad c
    usando los objetos ya procesados; se recorre c de mayor a menor para que
    cada objeto se use a lo sumo una vez. Devuelve el mejor valor."""
    M = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, -1, -1):
            if w <= c and v + M[c - w] > M[c]:
                M[c] = v + M[c - w]
    return M[W]
```
<!-- /codigo -->

### El tamaño en bits

Como en C1, §8, el tamaño es lo que ocupa la entrada escrita en binario, no el valor de sus números. Sea $\text{bits}(x) = \lceil \log_2(x + 1) \rceil$ la cantidad de dígitos binarios de $x \ge 1$. La entrada es la lista de los $2n + 1$ números, y ocupa

$$
L = \sum_{i=1}^{n} \bigl(\text{bits}(w_i) + \text{bits}(v_i)\bigr) + \text{bits}(W). \tag{1}
$$

De (1) salen $n \le L$ y $W < 2^{\text{bits}(W)} \le 2^L$. Entonces el costo es a lo sumo $nW < L \cdot 2^L$: como mucho exponencial en el tamaño.

### ¿Es polinomial? No

Hay entradas donde realmente es exponencial. Para cada $b \ge 1$, tomemos un solo objeto con $w_1 = 2^b - 1$, $v_1 = 1$ y capacidad $W = 2^b - 1$. Por (1), la entrada tiene $L = b + 1 + b = 2b + 1$ bits. El algoritmo llena toda la tabla, sean cuales sean los números, así que calcula

$$
n(W + 1) = 2^b = 2^{(L-1)/2} \tag{2}
$$

celdas. Para cualquier polinomio $p$, $2^{(L-1)/2} > p(L)$ cuando $L$ es grande, así que ningún polinomio en el tamaño acota el costo. El algoritmo no es polinomial.

Según la definición de C1, §8, es **pseudopolinomial**. Su costo $\Theta(nW)$ es polinomial en $n$ y en el *valor* de $W$, pero $W$ puede ser exponencial en la cantidad de bits que ocupa. Agregar un bit a $W$ duplica la tabla, aunque la entrada crezca en un solo bit.

### En qué se parece a la primalidad por división

La primalidad por división de C1 prueba los divisores desde 2 hasta $\sqrt N$. Son unas $\sqrt N$ divisiones, polinomiales en el valor $N$. Pero $N$ ocupa $b = \text{bits}(N)$ bits, y $\sqrt N \approx 2^{b/2}$ es exponencial en $b$.

**El parecido.** Es el mismo fenómeno. Los dos algoritmos recorren un rango del tamaño de un número de la entrada (los divisores hasta $\sqrt N$, las capacidades de $0$ a $W$), mientras que la entrada solo guarda los dígitos de ese número. Por eso los dos son polinomiales en el valor y exponenciales en los bits.
- **El crecimiento:** dos bits más en $N$ duplican las divisiones, y un bit más en $W$ duplica la tabla. En la familia de (2), el costo $2^{(L-1)/2}$ crece incluso al mismo ritmo que las $2^{b/2}$ divisiones.
- **Escritos en unario,** con un símbolo por unidad, el tamaño sería el valor, y los dos algoritmos serían polinomiales en ese tamaño.


### Conclusión

Medido en bits, el tamaño de la entrada es (1), y la capacidad aporta solo unos $\log_2 W$ bits. Por eso el algoritmo de $\Theta(nW)$ no es polinomial: con un objeto calcula $2^{(L-1)/2}$ celdas (2). Es pseudopolinomial, como la primalidad por división, que hace unas $2^{b/2}$ divisiones con $b$ bits. Los dos cuentan hasta el valor de un número que la entrada escribe con pocos dígitos.

---

### Cómo reproducir

El código del algoritmo está en `extra_11/mochila.py`. Desde la carpeta del tema:

```
python -m comun.regenerar ejercicio-11.md   # vuelve a copiar el código en este archivo
```
