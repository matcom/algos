# Ejercicio 3: pila con operación mínimo en O(1)

**Enunciado.** Una pila con una operación `minimo` que cuesta O(1) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación.

El script `ejercicio-03.py` implementa la estructura y comprueba el invariante en miles de secuencias de operaciones.

## 1. El problema

Queremos una pila con las operaciones de siempre y una más:

- `push(x)`: agrega x arriba.
- `pop()`: saca y devuelve el de arriba.
- `top()`: devuelve el de arriba sin sacarlo.
- `minimo()`: devuelve el menor de todos los elementos que hay en la pila.

La precondición de pop, top y minimo es que la pila no esté vacía. Todas tienen que costar O(1) en el peor caso.

## 2. Idea

Una pila normal hace push, pop y top en O(1). Lo difícil es `minimo`: recorrer toda la pila cuesta O(n).

Mi primera idea fue guardar una variable m con el mínimo y actualizarla en cada push con m = min(m, x). El problema aparece con `pop`. Por ejemplo:

```
push 5, push 3, pop      (la pila queda con solo el 5)
```

Después del pop el mínimo debería ser 5, pero m sigue en 3. Al sacar el mínimo no podemos saber cuál era el mínimo anterior, porque no lo guardamos.

La solución es guardar ese dato: **cada elemento se guarda junto con el mínimo de todo lo que hay debajo de él (incluyéndolo)**. Así, cuando sacamos un elemento, el mínimo de lo que queda ya está guardado en el nuevo elemento de arriba.

## 3. La estructura

Una pila de pares (valor, mínimo hasta aquí):

```python
class PilaMin:
    def __init__(self):
        self.datos = []                      # pares (valor, minimo hasta aqui)

    def push(self, x):
        if self.datos:
            m = min(x, self.datos[-1][1])    # minimo entre x y lo de abajo
        else:
            m = x
        self.datos.append((x, m))

    def pop(self):
        return self.datos.pop()[0]

    def top(self):
        return self.datos[-1][0]

    def minimo(self):
        return self.datos[-1][1]             # el minimo de toda la pila
```

Ejemplo, haciendo `push 5, push 3, push 7, push 2`:

```
posición   valor   mínimo hasta aquí
   3         2          2          <- arriba
   2         7          3
   1         3          3
   0         5          5
```

tenemos que minimo() devuelve 2. Si hacemos pop dos veces, arriba queda el par (3, 3) y minimo() devuelve 3, que es correcto porque la pila tiene 5 y 3.

## 4. Invariante

 Invariante: para cada posición i de la pila, el par guardado es (v_i, m_i) con m_i = mínimo de v_0, v_1, ..., v_i. O sea, m_i es el menor de los elementos desde el fondo hasta la posición i.

Al inicio la pila vacía no tiene posiciones, así que el invariante se cumple.

Cuando se ejecuta el algoritmo:
- `push(x)`: los pares que ya estaban no cambian, así que siguen cumpliendo el invariante. El par nuevo es (x, m) con m = min(x, m_arriba). Por el invariante, m_arriba es el mínimo de todos los de abajo, y entonces min(x, m_arriba) es el mínimo de todos los de abajo junto con x. Si la pila estaba vacía, m = x, que es correcto.
- `pop()`: se quita el par de arriba. Cada m_i solo depende de los elementos que están debajo de la posición i, que no cambian, así que los pares que quedan siguen cumpliendo el invariante.
- `top()` y `minimo()` no modifican la pila.

**Correctitud de `minimo`.** Si la pila no está vacía, el par de arriba es (v_k, m_k) y por el invariante m_k es el mínimo desde el fondo hasta arriba, o sea el mínimo de toda la pila. Eso es lo que devuelve `minimo`.

Como ninguna operación tiene ciclos, cada una termina siempre.

## 5. Costo

Las cuatro operaciones cuestan O(1) en el peor caso. push compara con min y agrega un par al final, pop quita el último par, y top y minimo solo leen el último par. Ninguna tiene ciclos, así que todas hacen siempre la misma cantidad de pasos, sin importar cuántos elementos haya en la pila.

Esto es O(1) en el peor caso si la pila se implementa con una lista enlazada. Si se usa un arreglo dinámico, agregar al final es O(1) amortizado, porque de vez en cuando el arreglo se llena y hay que copiarlo completo a uno más grande. Con un arreglo de tamaño fijo vuelve a ser O(1) en el peor caso.

En memoria se guardan dos números por cada elemento, o sea O(n), el doble que una pila normal. Además, O(1) es lo mejor que se puede lograr, porque cualquier operación cuesta al menos un paso.

## 6. Resultados del script

El script implementa la pila y también la versión con una sola variable `m` . Primero prueba el contraejemplo, y después hace 5000 secuencias de `push` y `pop` al azar, comparando con una lista normal. En cada operación comprueba con `assert` el invariante y que `top` y `minimo` den el valor correcto.

```
Version mala: push 5, push 3, pop -> minimo = 3 (deberia ser 5)

5000 secuencias al azar, 76435 operaciones
PilaMin: invariante y minimo correctos en todas
PilaMala: dio un minimo equivocado en 26252 consultas
```

La pila con pares cumple el invariante en todas las operaciones. La versión con una sola variable falla muchas veces, y se ve que esto no era un caso raro: se equivoca siempre que se saca el mínimo y después se pide `minimo`.

## 7. Respuesta final

- **Estructura:** una pila donde cada elemento se guarda junto con el mínimo de todo lo que tiene debajo.
- **Invariante:** para cada posición i, m_i es el mínimo de los elementos desde el fondo hasta la posición i.
- **Costo:** `push`, `pop`, `top` y `minimo` cuestan O(1) en el peor caso. Se usa O(n) de memoria.

**Conclusión:** guardar solo el mínimo actual no alcanza porque al sacar elementos se pierde el mínimo anterior. Guardando el mínimo en cada elemento, el mínimo de lo que queda ya está calculado, y se logra O(1) en todo a cambio de usar el doble de memoria.
